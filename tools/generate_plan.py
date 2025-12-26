#!/usr/bin/env python3
"""Generate a lightweight shot-plan JSON from the centralized index.yaml entry."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml  # type: ignore
except ImportError:
    sys.exit("PyYAML is required by tools/generate_plan.py: install via requirements.txt")

ROOT = Path(__file__).resolve().parents[1]
INDEX_PATH = ROOT / "index.yaml"
OUTPUT_PATH = ROOT / "02_outputs" / "plan" / "shot_list.json"

def locate_shots(index_data: dict) -> list[dict]:
    result = []
    for stage in index_data.get("stages", []):
        stage_id = stage.get("id")
        for doc in stage.get("docs", []):
            path_value = doc.get("path", "")
            if "shot" not in path_value.lower():
                continue
            result.append(
                {
                    "stage_id": stage_id,
                    "doc_id": doc.get("id"),
                    "path": path_value,
                }
            )
    return result


def main() -> None:
    if not INDEX_PATH.exists():
        sys.exit(f"Missing index file at {INDEX_PATH}")

    with INDEX_PATH.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}

    shots = locate_shots(data)
    notes = [
        f"Found {len(shots)} shot entries derived from {INDEX_PATH.name}.",
        "This plan is derived from the top-level index and can be regenerated via make plan.",
    ]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_index": str(INDEX_PATH.relative_to(ROOT)),
        "shots": shots,
        "notes": notes,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
