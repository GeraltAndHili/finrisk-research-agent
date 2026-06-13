from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
KG_PATH = ROOT / "data" / "kg" / "kg_edges.json"


def load_edges() -> list[dict]:
    if not KG_PATH.exists():
        return []
    return json.loads(KG_PATH.read_text(encoding="utf-8"))

