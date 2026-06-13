from __future__ import annotations

from pydantic import BaseModel, Field


class EvidenceCard(BaseModel):
    evidence_id: str
    source_type: str
    source_name: str
    entity: str | None = None
    related_product: str | None = None
    risk_tags: list[str] = Field(default_factory=list)
    event_type: str | None = None
    summary: str
    publish_date: str | None = None
    credibility_score: float = Field(default=0.7, ge=0, le=1)
    freshness_score: float = Field(default=0.7, ge=0, le=1)
    supporting_sub_questions: list[str] = Field(default_factory=list)
    raw_content: str = ""
    url: str = ""

