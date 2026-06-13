from __future__ import annotations

from src.schemas.evidence_schema import EvidenceCard
from src.schemas.planner_schema import SubQuestion


REQUIRED_BY_DIMENSION = {
    "portfolio_exposure": ["holding_exposure", "product_metric"],
    "credit_risk": ["issuer_profile", "bond_market_indicator", "financing_pressure"],
    "liquidity_risk": ["financing_pressure", "issuer_profile"],
    "industry_risk": ["sales_pressure", "research_note", "kg_path"],
    "market_risk": ["bond_market_indicator"],
    "public_opinion_risk": ["external_fact_stub", "financing_pressure"],
    "product_risk": ["product_metric"],
}


def assess_answerability(question: SubQuestion, evidence: list[EvidenceCard]) -> dict:
    required = REQUIRED_BY_DIMENSION.get(question.risk_dimension, ["research_note"])
    present = {card.event_type for card in evidence}
    missing = [item for item in required if item not in present]
    if not missing:
        answerability = "answerable"
    elif len(missing) < len(required):
        answerability = "partially_answerable"
    else:
        answerability = "need_evidence"
    return {
        "answerability": answerability,
        "required_evidence": required,
        "missing_evidence_types": missing,
    }
