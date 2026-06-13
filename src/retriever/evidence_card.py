from __future__ import annotations

from itertools import count

from src.schemas.evidence_schema import EvidenceCard


_COUNTER = count(1)


def make_card(
    *,
    source_type: str,
    source_name: str,
    summary: str,
    entity: str | None = None,
    related_product: str | None = None,
    risk_tags: list[str] | None = None,
    event_type: str | None = None,
    publish_date: str | None = None,
    credibility_score: float = 0.75,
    freshness_score: float = 0.75,
    raw_content: str = "",
    supporting_sub_questions: list[str] | None = None,
    url: str = "",
) -> EvidenceCard:
    return EvidenceCard(
        evidence_id=f"E{next(_COUNTER):03d}",
        source_type=source_type,
        source_name=source_name,
        entity=entity,
        related_product=related_product,
        risk_tags=risk_tags or [],
        event_type=event_type,
        summary=summary,
        publish_date=publish_date,
        credibility_score=credibility_score,
        freshness_score=freshness_score,
        supporting_sub_questions=supporting_sub_questions or [],
        raw_content=raw_content,
        url=url,
    )

