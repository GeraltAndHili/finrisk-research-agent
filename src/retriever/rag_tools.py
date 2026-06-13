from __future__ import annotations

from pathlib import Path

from src.retriever.evidence_card import make_card
from src.schemas.evidence_schema import EvidenceCard


ROOT = Path(__file__).resolve().parents[2]
DOC_DIR = ROOT / "data" / "documents"


def rag_retrieve(arguments: dict) -> list[EvidenceCard]:
    query = arguments.get("query", "")
    cards = []
    for path in DOC_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in split_terms(query)):
            cards.append(
                make_card(
                    source_type="local_doc",
                    source_name=path.name,
                    risk_tags=["credit_risk", "liquidity_risk", "market_risk", "portfolio_exposure"],
                    event_type="research_note",
                    credibility_score=0.72,
                    freshness_score=0.68,
                    summary=text.replace("\n", " ")[:180],
                    raw_content=text,
                )
            )
    return cards


def external_search(arguments: dict) -> list[EvidenceCard]:
    query = arguments.get("query", "")
    return [
        make_card(
            source_type="external_stub",
            source_name="external_search_stub",
            entity="万科" if "万科" in query else None,
            risk_tags=["public_opinion_risk", "credit_risk"],
            event_type="external_fact_stub",
            credibility_score=0.55,
            freshness_score=0.6,
            summary="外部检索接口占位：当前离线 MVP 不联网，后续可接搜索 API、公告源或新闻源，并复用 Evidence Card 协议。",
            raw_content=query,
        )
    ]


def split_terms(query: str) -> list[str]:
    terms = ["信用", "风险", "债券", "万科", "产品", "房地产", "融资", "利差", "持仓"]
    return [term for term in terms if term in query] or list(query[:4])

