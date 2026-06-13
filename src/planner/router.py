from __future__ import annotations

import hashlib
import re

from src.planner.question_pool import QUESTION_POOL, render_question
from src.planner.submodular_selector import select_sub_questions
from src.schemas.planner_schema import PlannerResult, SubQuestion, ToolCall


def plan_query(raw_query: str) -> PlannerResult:
    entities = extract_entities(raw_query)
    route = classify_route(raw_query)
    risk_types = infer_risk_types(raw_query, route)
    candidates = build_candidates(raw_query, entities, risk_types)
    selected = select_sub_questions(candidates, max_items=5 if route == "open_research" else 3)
    tool_plan = build_tool_plan(route, entities, selected, raw_query)

    return PlannerResult(
        query_id=make_query_id(raw_query),
        raw_query=raw_query,
        route=route,
        main_task=normalize_task(raw_query),
        entities=entities,
        risk_types=risk_types,
        candidate_sub_questions=candidates,
        selected_sub_questions=selected,
        tool_plan=tool_plan,
    )


def classify_route(query: str) -> str:
    if any(word in query for word in ("比较", "对比", "产品A和产品B", "产品A与产品B")):
        return "react"
    if any(word in query for word in ("分析", "归因", "是否存在", "影响", "为什么", "上升")):
        return "open_research"
    return "direct"


def extract_entities(query: str) -> dict[str, list[str]]:
    entities: dict[str, list[str]] = {
        "product": [],
        "issuer": [],
        "asset": [],
        "industry": [],
    }
    products = sorted(set(re.findall(r"产品[A-ZＡ-Ｚ]", query)))
    if "产品A" in query or "产品Ａ" in query:
        products.append("产品A")
    if "产品B" in query or "产品Ｂ" in query:
        products.append("产品B")
    entities["product"] = sorted(set(products))

    issuer_aliases = {"万科": "万科", "碧桂园": "碧桂园", "龙湖": "龙湖"}
    for key, value in issuer_aliases.items():
        if key in query:
            entities["issuer"].append(value)
    if "万科债券" in query:
        entities["asset"].append("万科债券")
        entities["issuer"].append("万科")
        entities["industry"].append("房地产")
    if any(word in query for word in ("地产", "房地产")):
        entities["industry"].append("房地产")
    return {key: sorted(set(value)) for key, value in entities.items()}


def infer_risk_types(query: str, route: str) -> list[str]:
    tags = []
    mapping = {
        "信用": "credit_risk",
        "流动性": "liquidity_risk",
        "回撤": "market_risk",
        "波动": "market_risk",
        "集中": "concentration_risk",
        "行业": "industry_risk",
        "舆情": "public_opinion_risk",
    }
    for keyword, tag in mapping.items():
        if keyword in query:
            tags.append(tag)
    if route == "open_research":
        tags.extend(["credit_risk", "liquidity_risk", "industry_risk", "portfolio_exposure"])
    if not tags:
        tags = ["product_risk"]
    return sorted(set(tags))


def build_candidates(query: str, entities: dict[str, list[str]], risk_types: list[str]) -> list[SubQuestion]:
    candidates = []
    for index, template in enumerate(QUESTION_POOL, start=1):
        question = render_question(template, entities)
        relevance = score_relevance(query, template.keywords, template.dimension, risk_types)
        evidence = 0.78 if template.evidence_types else 0.5
        coverage = 0.85 if template.dimension in risk_types or template.dimension == "portfolio_exposure" else 0.62
        kg_path = 0.8 if template.dimension in {"industry_risk", "portfolio_exposure", "related_party_risk"} else 0.65
        score = 0.30 * coverage + 0.25 * relevance + 0.20 * evidence + 0.15 * kg_path
        candidates.append(
            SubQuestion(
                question_id=f"SQ{index}",
                question=question,
                risk_dimension=template.dimension,
                priority=round(min(score, 0.99), 2),
            )
        )
    return candidates


def score_relevance(query: str, keywords: tuple[str, ...], dimension: str, risk_types: list[str]) -> float:
    hit = sum(1 for word in keywords if word in query)
    base = min(0.45 + hit * 0.12, 0.92)
    if dimension in risk_types:
        base += 0.12
    return min(base, 1.0)


def build_tool_plan(route: str, entities: dict[str, list[str]], selected: list[SubQuestion], query: str) -> list[ToolCall]:
    product = (entities.get("product") or ["产品A"])[0]
    issuer = (entities.get("issuer") or [""])[0]
    industry = (entities.get("industry") or [""])[0]
    calls: list[ToolCall] = []
    if route == "direct":
        calls.append(ToolCall(tool_name="product_risk_query", arguments={"top_n": 5}))
        return calls
    calls.append(ToolCall(tool_name="product_risk_query", arguments={"product": entities.get("product", [])}))
    calls.append(ToolCall(tool_name="holding_query", arguments={"product": product, "issuer": issuer}))
    if issuer:
        calls.append(ToolCall(tool_name="issuer_profile_query", arguments={"issuer": issuer}))
        calls.append(ToolCall(tool_name="risk_event_search", arguments={"entity": issuer, "time_range": "last_90_days"}))
        calls.append(ToolCall(tool_name="market_indicator_query", arguments={"issuer": issuer}))
        calls.append(ToolCall(tool_name="kg_expand", arguments={"entity": issuer, "depth": 2}))
    if industry:
        calls.append(ToolCall(tool_name="risk_event_search", arguments={"entity": industry, "time_range": "last_90_days"}))
    if route == "open_research":
        calls.append(ToolCall(tool_name="rag_retrieve", arguments={"query": query, "top_k": 5}))
        calls.append(ToolCall(tool_name="external_search", arguments={"query": query, "source_type": ["news", "announcement"]}))
    return calls


def normalize_task(query: str) -> str:
    return query.strip("。！？ \n\t")


def make_query_id(query: str) -> str:
    digest = hashlib.md5(query.encode("utf-8")).hexdigest()[:8].upper()
    return f"Q20260613_{digest}"
