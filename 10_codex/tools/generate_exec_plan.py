#!/usr/bin/env python3
"""Build a lightweight execution plan from the shot list export."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PLAN_SOURCE = ROOT / "20_runtime" / "plan" / "shot_list.json"
OUTPUT_PATH = ROOT / "20_runtime" / "exec" / "execution_plan.json"

def build_steps(shots: list[dict]) -> list[dict]:
    template = ["validate_inputs", "generate_assets", "render"]
    steps = []
    for idx, shot in enumerate(shots, start=1):
        shot_id = shot.get("doc_id") or shot.get("path") or f"shot_{idx}"
        for action in template:
            steps.append(
                {
                    "shot_id": shot_id,
                    "step_id": f"{shot_id}_{action}",
                    "name": action,
                    "description": f"{action.replace('_', ' ').capitalize()} for {shot.get('path', shot_id)}",
                }
            )
    return steps


def main() -> None:
    if not PLAN_SOURCE.exists():
        sys.exit(f"Missing shot list at {PLAN_SOURCE}; run `make plan` first")

    with PLAN_SOURCE.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    shots = data.get("shots", [])
    steps = build_steps(shots)

    notes = [
        f"Derived {len(steps)} steps from {len(shots)} shots in {PLAN_SOURCE.name}.",
        "Regenerate via make exec-plan.",
    ]

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "source_plan": str(PLAN_SOURCE.relative_to(ROOT)),
        "steps": steps,
        "notes": notes,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
