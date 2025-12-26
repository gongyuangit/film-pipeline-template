import sys
from datetime import datetime
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "10_codex" / "TEMPLATE_MANIFEST.yaml"
INBOX_PATH = REPO_ROOT / "00_human" / "INBOX.md"
SOURCE_SCRIPT_PATH = REPO_ROOT / "30_project" / "inputs" / "script" / "source_script.md"
STAGE_PATH = REPO_ROOT / "10_codex" / "PIPELINE_STAGES.yaml"
APPROVALS_PATH = REPO_ROOT / "00_human" / "APPROVALS.md"


HUMAN_TEMPLATES = {
    "00_human/INBOX.md": (
        "# INBOX\n"
        "| ID | Status | Description | 备注 |\n"
        "| -- | -- | -- | -- |\n"
    ),
    "00_human/APPROVALS.md": (
        "# APPROVALS\n"
        "| Approval Key | Artifact | Status | Notes |\n"
        "| -- | -- | -- | -- |\n"
        "## Stage approvals\n"
        "- SOURCE_SCRIPT_APPROVED: 人工确认剧本文本\n"
        "- SCRIPT_BREAKDOWN_APPROVED: 人工确认 script_breakdown_v1\n"
        "- STAGE_C_DECISION_APPROVED: 人工确认方向性决策\n"
        "- CINEMATIC_INTENT_APPROVED: 人工确认 cinematic intent\n"
        "- SHOT_MAP_SRT_XML_APPROVED: 人工确认 layout shot map SRT + planning XML\n"
        "- LAYOUT_FREEZE_APPROVED: 人工确认 layout freeze\n"
        "- LAYOUT_REVIEW_APPROVED: 人工确认 layout review\n"
        "- LOOKDEV_PROMPTS_APPROVED: 人工确认 lookdev shot prompts\n"
        "- EXEC_PLAN_APPROVED: 人工确认 exec plan\n"
    ),
    "00_human/DECISIONS.md": "# DECISIONS\n\n- 无\n",
    "00_human/NEEDED_INPUTS.md": "# NEEDED INPUTS\n\n- None\n",
    "00_human/PRODUCTION.md": "# PRODUCTION\n\n- None\n",
}


def load_manifest():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("entries", [])


def ensure_structure(entries):
    created = []
    for entry in entries:
        relative = entry["path"]
        target = REPO_ROOT / relative
        entry_type = entry.get("type", "file")
        if entry_type == "dir":
            if not target.exists():
                target.mkdir(parents=True, exist_ok=True)
                created.append(relative)
        else:
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.touch()
                created.append(relative)
    return created


def ensure_human_templates():
    for relative, template in HUMAN_TEMPLATES.items():
        target = REPO_ROOT / relative
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(template, encoding="utf-8")
            continue
        text = target.read_text(encoding="utf-8")
        header = template.splitlines()[0]
        if header not in text:
            updated = template
            if text.strip():
                updated += "\n" + text.lstrip("\n")
            target.write_text(updated, encoding="utf-8")


def ensure_preflight_section():
    content = INBOX_PATH.read_text(encoding="utf-8")
    if "## Preflight" not in content:
        with INBOX_PATH.open("a", encoding="utf-8") as f:
            f.write("\n## Preflight\n")
            f.write("- 尚无结构更新\n")


def append_preflight_summary(created):
    if not created:
        return
    ensure_preflight_section()
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    bullet = f"- {timestamp} 已补齐：{', '.join(created)}\n"
    text = INBOX_PATH.read_text(encoding="utf-8")
    if "## Preflight" not in text:
        text += "\n## Preflight\n"
    parts = text.split("## Preflight", 1)
    before = parts[0]
    after = parts[1]
    updated_after = "## Preflight\n" + bullet + after.lstrip("\n")
    with INBOX_PATH.open("w", encoding="utf-8") as f:
        f.write(before + updated_after)


def update_source_script_gate():
    text = INBOX_PATH.read_text(encoding="utf-8")
    lines = text.splitlines()
    if pipe := _update_table(lines):
        new_text = "\n".join(pipe)
        INBOX_PATH.write_text(new_text, encoding="utf-8")


STAGE_D_ROW = "| 6 | pending | `30_project/docs/2_layout/_artifacts/2-1_cinematic_intent_v1.yaml` 已基于 `source_script.md` 与 `script_breakdown_v1.yaml` 生成，请确认后再进入 shot map / layout freeze。 |  |"
STAGE_P1_5_ROW = "| 7 | pending | `30_project/docs/2_layout/_artifacts/editing_bridge/shot_map_v1.srt` 与 `30_project/docs/2_layout/_artifacts/editing_bridge/timeline_plan_v1.xml` 均已生成镜头管理 SRT 与规划 XML，请确认后再进入 layout 或 prompt 生成。 |  |"
STAGE_LR_ROW = "| 8 | pending | `30_project/docs/2_layout/_artifacts/reports/layout_review_v1.md` 已生成 layout review 验收记录，请确认后再进入 lookdev prompt Pack。 |  |"
STAGE_K_ROW = "| 9 | pending | `30_project/docs/2_layout/_artifacts/branch_lookdev_shot_prompt_pack_v1.yaml` 已生成 Lookdev shot prompt Pack，请确认后再进入 lookdev review。 |  |"
STAGE_KR_ROW = "| 10 | pending | `30_project/docs/2_layout/_artifacts/reports/lookdev_review_v1.md` 已生成 Lookdev review 验收，请确认后再进入执行计划。 |  |"


def _update_table(lines):
    start = next((i for i, line in enumerate(lines) if line.startswith("| ID |")), None)
    if start is None:
        return None
    end = start
    while end < len(lines) and lines[end].strip():
        end += 1
    table = lines[start:end]
    header = table[:2]
    rows = table[2:]
    row_keyword = "source_script.md"
    row_exists = any(row_keyword in row for row in rows)
    source_exists = SOURCE_SCRIPT_PATH.exists()
    if source_exists and row_exists:
        rows = [row for row in rows if row_keyword not in row]
    stage_rows = [STAGE_D_ROW, STAGE_P1_5_ROW, STAGE_LR_ROW, STAGE_K_ROW]
    stage_rows.append(STAGE_KR_ROW)
    if not source_exists and not row_exists:
        gate_row = "| 6 | pending | 请先将 `30_project/inputs/script/source_script.md` 提供为权威剧本文本，或继续在 `30_project/docs/0-source/raw/` 投递碎片供 Source Synthesis 合成；之后再继续 1_story。 |  |"
        rows.append(gate_row)
    for row in stage_rows:
        if row not in rows:
            rows.append(row)
    return lines[:start] + header + rows + lines[end:]


def load_pipeline_stages():
    if not STAGE_PATH.exists():
        return []
    with STAGE_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("stages", [])


def load_approvals():
    if not APPROVALS_PATH.exists():
        return ""
    return APPROVALS_PATH.read_text(encoding="utf-8")


def enforce_stage_gates(stages, approvals_text):
    for stage in stages:
        missing = [req for req in stage.get("requires", []) if req not in approvals_text]
        if missing:
            print(
                f"Stage '{stage['name']}' ({stage['description']}) 需等待下列 approvals：{', '.join(missing)}；"
                f"请在 {APPROVALS_PATH.name} 中记录以继续。参阅 {STAGE_PATH.relative_to(REPO_ROOT)}。"
            )
            sys.exit(1)


def main():
    entries = load_manifest()
    created = ensure_structure(entries)
    ensure_human_templates()
    append_preflight_summary(created)
    INBOX_TEXT = INBOX_PATH.read_text(encoding="utf-8")
    if "## Preflight" not in INBOX_TEXT:
        ensure_preflight_section()
    update_source_script_gate()
    if not SOURCE_SCRIPT_PATH.exists():
        print("缺失 30_project/inputs/script/source_script.md，暂停 1_story 生成，等待人工上传或通过 0-source/raw 补全。")
        sys.exit(1)
    stages = load_pipeline_stages()
    approvals_text = load_approvals()
    enforce_stage_gates(stages, approvals_text)


if __name__ == "__main__":
    main()
