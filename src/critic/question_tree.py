from __future__ import annotations

from src.critic.answer_model import assess_answerability
from src.schemas.critic_schema import QuestionNode
from src.schemas.evidence_schema import EvidenceCard
from src.schemas.planner_schema import SubQuestion


def build_question_tree(questions: list[SubQuestion], evidence: list[EvidenceCard]) -> list[QuestionNode]:
    nodes: list[QuestionNode] = []
    for question in questions:
        assessment = assess_answerability(question, evidence)
        nodes.append(
            QuestionNode(
                node_id=question.question_id,
                parent_id=None,
                depth=1,
                question=question.question,
                risk_dimension=question.risk_dimension,
                required_evidence=assessment["required_evidence"],
                mapped_tools=map_tools(assessment["required_evidence"]),
                answerability=assessment["answerability"],
                status="closed" if assessment["answerability"] == "answerable" else "open",
            )
        )
    return nodes


def map_tools(evidence_types: list[str]) -> list[str]:
    mapping = {
        "holding_exposure": "holding_query",
        "product_metric": "product_risk_query",
        "issuer_profile": "issuer_profile_query",
        "bond_market_indicator": "market_indicator_query",
        "financing_pressure": "risk_event_search",
        "sales_pressure": "risk_event_search",
        "research_note": "rag_retrieve",
        "kg_path": "kg_expand",
        "external_fact_stub": "external_search",
    }
    return sorted({mapping[item] for item in evidence_types if item in mapping})

