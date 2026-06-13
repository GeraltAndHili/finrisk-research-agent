from __future__ import annotations

from src.kg.graph_loader import load_edges
from src.retriever.evidence_card import make_card
from src.schemas.evidence_schema import EvidenceCard


def kg_expand(arguments: dict) -> list[EvidenceCard]:
    entity = arguments.get("entity", "")
    depth = int(arguments.get("depth", 2))
    edges = load_edges()
    frontier = {entity}
    seen = {entity}
    paths: list[str] = []
    for _ in range(depth):
        next_frontier = set()
        for edge in edges:
            if edge["head"] in frontier or edge["tail"] in frontier:
                paths.append(f"{edge['head']} -{edge['relation']}-> {edge['tail']}")
                if edge["head"] not in seen:
                    next_frontier.add(edge["head"])
                if edge["tail"] not in seen:
                    next_frontier.add(edge["tail"])
        seen |= next_frontier
        frontier = next_frontier
    if not paths:
        return []
    return [
        make_card(
            source_type="kg",
            source_name="kg_edges.json",
            entity=entity,
            risk_tags=["risk_chain"],
            event_type="kg_path",
            credibility_score=0.76,
            freshness_score=0.7,
            summary="知识图谱扩展路径：" + "；".join(paths[:6]),
            raw_content="\n".join(paths),
        )
    ]

