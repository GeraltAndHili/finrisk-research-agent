from __future__ import annotations

from pydantic import BaseModel, Field

from src.schemas.critic_schema import CriticResult
from src.schemas.evidence_schema import EvidenceCard
from src.schemas.planner_schema import PlannerResult


class ResearchPackage(BaseModel):
    query_id: str
    main_task: str
    route: str
    planner_result: PlannerResult
    final_sub_questions: list[str]
    evidence_cards: list[EvidenceCard]
    critic_result: CriticResult
    risk_chain: list[str] = Field(default_factory=list)
    reporter_ready: bool

