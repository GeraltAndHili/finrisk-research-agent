from __future__ import annotations

from src.critic.answer_model import assess_answerability
from src.critic.question_model import propose_missing_questions
from src.critic.question_tree import build_question_tree
from src.schemas.critic_schema import CriticResult, MissingQuestion
from src.schemas.evidence_schema import EvidenceCard
from src.schemas.planner_schema import PlannerResult


FACT_SOURCE_TYPES = {"news", "industry_report", "local_doc", "external_stub", "mock_db"}
DATA_SOURCE_NAMES = {"product_risk_metrics", "holdings", "issuer_profile", "market_indicators"}


def critique(planner_result: PlannerResult, evidence: list[EvidenceCard]) -> CriticResult:
    question_tree = build_question_tree(planner_result.selected_sub_questions, evidence)
    missing: list[MissingQuestion] = []
    covered_questions = 0
    for question in planner_result.selected_sub_questions:
        assessment = assess_answerability(question, evidence)
        if assessment["answerability"] == "answerable":
            covered_questions += 1
        missing.extend(propose_missing_questions(question.risk_dimension, assessment["missing_evidence_types"]))

    fact_sufficiency = ratio(
        sum(1 for card in evidence if card.source_type in FACT_SOURCE_TYPES and card.credibility_score >= 0.55),
        max(3, len(planner_result.selected_sub_questions)),
    )
    data_sufficiency = ratio(
        sum(1 for card in evidence if card.source_name in DATA_SOURCE_NAMES),
        max(2, len(planner_result.selected_sub_questions) // 2),
    )
    evidence_coverage = ratio(covered_questions, max(1, len(planner_result.selected_sub_questions)))
    risk_chain_completeness = score_risk_chain(evidence)
    passed = fact_sufficiency >= 0.65 and data_sufficiency >= 0.65 and evidence_coverage >= 0.55 and risk_chain_completeness >= 0.55
    reason = "当前证据已覆盖主要事实、数据和风险链路。" if passed else "当前证据不足以完全支撑风险归因判断，需要补充关键事实或数据。"
    return CriticResult(
        critic_pass=passed,
        reason=reason,
        fact_sufficiency=fact_sufficiency,
        data_sufficiency=data_sufficiency,
        evidence_coverage=evidence_coverage,
        risk_chain_completeness=risk_chain_completeness,
        question_tree=question_tree,
        missing_questions=missing[:5],
        suggested_return_to=None if passed else "planner",
    )


def ratio(numerator: int, denominator: int) -> float:
    return round(min(numerator / denominator, 1.0), 2)


def score_risk_chain(evidence: list[EvidenceCard]) -> float:
    tags = {tag for card in evidence for tag in card.risk_tags}
    steps = [
        bool(tags & {"industry_risk", "public_opinion_risk"}),
        bool(tags & {"credit_risk", "liquidity_risk"}),
        bool(tags & {"market_risk"}),
        bool(tags & {"portfolio_exposure", "product_risk"}),
    ]
    return round(sum(steps) / len(steps), 2)

