from __future__ import annotations

from src.kg.kg_expand import kg_expand
from src.retriever.db_tools import (
    holding_query,
    issuer_profile_query,
    market_indicator_query,
    product_risk_query,
    risk_event_search,
)
from src.retriever.rag_tools import external_search, rag_retrieve
from src.schemas.evidence_schema import EvidenceCard
from src.schemas.planner_schema import ToolCall


TOOLS = {
    "product_risk_query": product_risk_query,
    "holding_query": holding_query,
    "issuer_profile_query": issuer_profile_query,
    "risk_event_search": risk_event_search,
    "market_indicator_query": market_indicator_query,
    "kg_expand": kg_expand,
    "rag_retrieve": rag_retrieve,
    "external_search": external_search,
}


def execute_tool_plan(tool_plan: list[ToolCall]) -> list[EvidenceCard]:
    evidence: list[EvidenceCard] = []
    for call in tool_plan:
        tool = TOOLS.get(call.tool_name)
        if not tool:
            continue
        evidence.extend(tool(call.arguments))
    return evidence

