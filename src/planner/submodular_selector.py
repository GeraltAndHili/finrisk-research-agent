from __future__ import annotations

from src.schemas.planner_schema import SubQuestion


def select_sub_questions(candidates: list[SubQuestion], max_items: int = 5) -> list[SubQuestion]:
    selected: list[SubQuestion] = []
    used_dimensions: set[str] = set()
    for question in sorted(candidates, key=lambda item: item.priority, reverse=True):
        if question.risk_dimension in used_dimensions:
            continue
        selected.append(question)
        used_dimensions.add(question.risk_dimension)
        if len(selected) >= max_items:
            break
    return selected

