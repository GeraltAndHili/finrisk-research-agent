from __future__ import annotations

from src.schemas.planner_schema import SubQuestion


def group_by_risk_dimension(questions: list[SubQuestion]) -> dict[str, list[SubQuestion]]:
    groups: dict[str, list[SubQuestion]] = {}
    for question in questions:
        groups.setdefault(question.risk_dimension, []).append(question)
    return groups

