#!/usr/bin/env python3
"""Generate TEMPLATE_INDEX.md from current template structure."""
from pathlib import Path
import argparse

REPO_ROOT = Path(__file__).resolve().parents[2]
TARGET = REPO_ROOT / "10_codex" / "TEMPLATE_INDEX.md"
BASE_ROOTS = [
    (Path("00_human"), "00_human"),
    (Path("10_codex"), "10_codex"),
    (Path("30_project") / "docs", "30_project/docs"),
]

TABLE_ROWS = [
    ("00_human/INBOX.md", "Human", "All-gate board", "Regenerated via preflight", "Shows each stage in PIPELINE_STAGES"),
    ("00_human/NOW.md", "Human", "Actionable gate list", "Regenerated via preflight", "Empty in template mode"),
    ("00_human/APPROVALS.md", "Human", "Approvals unlock gates", "Manual edits only", "Approvals are sole source of approved status"),
    ("10_codex/PIPELINE_STAGES.yaml", "Codex", "Defines gate order/prereqs/products", "Updated with new stages", "Drives dashboards"),
    ("10_codex/TEMPLATE_MANIFEST.yaml", "Codex", "Structure manifest", "Preflight enforces listed entries", "Includes placeholders"),
    ("10_codex/tools/preflight.py", "Codex", "Preflight / dashboards", "Run before other flow", "Loads manifest/stages and checks template index"),
    ("30_project/inputs/index.yaml", "Human", "project_mode switch", "Default template, change to project", "Keeps NOW empty until project mode"),
    ("30_project/docs/0-source/", "Codex", "Source fragments + registry", "Feeds Stage S", "raw/ -> structured shards"),
    ("30_project/docs/1_story/script_breakdown_v1.yaml", "Codex", "Script breakdown", "Feeds layout/audio", "Placeholder until populated"),
    ("30_project/docs/2_layout/_artifacts/", "Codex", "Layout/lookdev artifacts", "All layout outputs live here", "Includes editing_bridge + CURRENT pointer"),
    ("30_project/docs/2_audio/_artifacts/", "Codex", "Audio planning + prompts + review", "Parallel to layout", "Shares editing_bridge facts"),
    ("30_project/docs/5_color/_artifacts/", "Codex", "Color QC + review", "After exec plan", "Editing bridge anchors XML/SRT"),
    ("20_runtime/exec/execution_plan.json", "Codex", "Execution plan placeholder", "Tracked despite being ignored", "Placeholder flagged until real plan exists"),
]

KEY_RULES = [
    "Approvals only come from `00_human/APPROVALS.md`; artifacts never auto-approve.",
    "In `project_mode: template`, artifact_ready is forced false (outside whitelist) and NOW shows a reminder.",
    "`TEMPLATE_PLACEHOLDER: true` + `content_nontrivial` heuristics guard readiness for YAML/MD/SRT/XML/JSON inputs.",
    "XML/SRT files represent timeline facts; trust track IDs and durations, not track names, and keep them under `_artifacts/editing_bridge/`.",
    "Every generated product must live inside the stage’s `_artifacts/` directory; layout uses `CURRENT.yaml` as the pointer.",
    "`90_archive/` is archive-only and is intentionally excluded from manifests, dashboards, and gate enforcement.",
]

NO_DRIFT = [
    "New stages must sync `PIPELINE_STAGES.yaml`, `TEMPLATE_MANIFEST.yaml`, dashboards (INBOX/NOW), and `preflight.py` gating logic.",
    "Every required file/directory must be listed in `TEMPLATE_MANIFEST.yaml`; preflight recreates placeholders when missing.",
    "Any structural change must document updates in `10_codex/TEMPLATE_INDEX.md` and, if archiving content, log it under `90_archive/docs_migration_log.md`.",
]


def dir_tree_block(root: Path, label: str, max_depth: int = 3) -> list[str]:
    lines = [f"- `{label}`"]

    def visit(path: Path, depth: int, prefix: str):
        if depth > max_depth:
            return
        try:
            entries = sorted([p for p in path.iterdir() if p.is_dir()])
        except PermissionError:
            return
        for entry in entries:
            indent = "  " * depth
            lines.append(f"{indent}- `{entry.relative_to(REPO_ROOT)}`")
            visit(entry, depth + 1, prefix + "  ")

    visit(root, 1, "")
    return lines


def build_tree_section() -> str:
    lines = ["## A. Directory tree (depth ≤3)"]
    for root_path, label in BASE_ROOTS:
        lines.extend(dir_tree_block(REPO_ROOT / root_path, label, 2))
    return "\n".join(lines)


def build_table_section() -> str:
    lines = ["## B. Purpose table", "", "| Path | Owner | Purpose | Lifecycle | Notes |", "| -- | -- | -- | -- | -- |"]
    for row in TABLE_ROWS:
        lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)


def build_rules_section() -> str:
    lines = ["## C. Key rules"]
    lines += [f"- {rule}" for rule in KEY_RULES]
    lines += ["", "## D. No-drift rules"]
    lines += [f"- {rule}" for rule in NO_DRIFT]
    return "\n".join(lines)


def render_index() -> str:
    head = "# Template Structure Index\n\n"
    return head + build_tree_section() + "\n\n" + build_table_section() + "\n\n" + build_rules_section() + "\n"


def write_index(check: bool = False) -> int:
    content = render_index()
    if check:
        if TARGET.exists() and TARGET.read_text() == content:
            return 0
        print("TEMPLATE_INDEX.md is out of sync. Run `make docs-index` to regenerate.")
        return 1
    TARGET.write_text(content, encoding="utf-8")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate template index")
    parser.add_argument("--check", action="store_true", help="only check alignment")
    args = parser.parse_args()
    return write_index(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
