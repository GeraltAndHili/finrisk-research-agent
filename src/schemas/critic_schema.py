from __future__ import annotations

from pydantic import BaseModel, Field


class QuestionNode(BaseModel):
    node_id: str
    parent_id: str | None = None
    depth: int = 0
    question: str
    risk_dimension: str
    required_evidence: list[str] = Field(default_factory=list)
    mapped_tools: list[str] = Field(default_factory=list)
    answerability: str = "need_evidence"
    status: str = "open"


class MissingQuestion(BaseModel):
    question: str
    risk_dimension: str
    missing_evidence_type: str


class CriticResult(BaseModel):
    critic_pass: bool
    reason: str
    fact_sufficiency: float = Field(ge=0, le=1)
    data_sufficiency: float = Field(ge=0, le=1)
    evidence_coverage: float = Field(ge=0, le=1)
    risk_chain_completeness: float = Field(ge=0, le=1)
    question_tree: list[QuestionNode] = Field(default_factory=list)
    missing_questions: list[MissingQuestion] = Field(default_factory=list)
    suggested_return_to: str | None = None

