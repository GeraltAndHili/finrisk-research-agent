from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


Route = Literal["direct", "react", "open_research"]


class SubQuestion(BaseModel):
    question_id: str
    question: str
    risk_dimension: str
    priority: float = Field(ge=0, le=1)


class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any] = Field(default_factory=dict)


class PlannerResult(BaseModel):
    query_id: str
    raw_query: str
    route: Route
    main_task: str
    entities: dict[str, list[str]]
    risk_types: list[str]
    candidate_sub_questions: list[SubQuestion] = Field(default_factory=list)
    selected_sub_questions: list[SubQuestion] = Field(default_factory=list)
    tool_plan: list[ToolCall] = Field(default_factory=list)

