import sys
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
        "| Stage | Gate Key | Status | Order | Action | Artifact |\n"
        "| -- | -- | -- | -- | -- | -- |\n"
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
        "- LOOKDEV_PROMPTS_APPROVED: 人工确认 lookdev prompts\n"
        "- LOOKDEV_REVIEW_APPROVED: 人工确认 lookdev review\n"
        "- AUDIO_PLAN_APPROVED: 人工确认 audio plan\n"
        "- AUDIO_PROMPTS_APPROVED: 人工确认 audio prompt packs\n"
        "- AUDIO_REVIEW_APPROVED: 人工确认 audio review\n"
        "- COLOR_QC_APPROVED: 人工确认 color QC\n"
        "- COLOR_REVIEW_APPROVED: 人工确认 color review\n"
        "- EXEC_PLAN_APPROVED: 人工确认 exec plan\n"
    ),
    "00_human/DECISIONS.md": "# DECISIONS\n\n- 无\n",
    "00_human/NEEDED_INPUTS.md": "# NEEDED INPUTS\n\n- None\n",
    "00_human/PRODUCTION.md": "# PRODUCTION\n\n- None\n",
}

STAGE_GATE_DEFINITIONS = [
    {
        "stage": "Stage S",
        "key": "SOURCE_SCRIPT_APPROVED",
        "artifact": "30_project/inputs/script/source_script.md",
        "action": "上传/确认权威剧本",
    },
    {
        "stage": "Stage B",
        "key": "SCRIPT_BREAKDOWN_APPROVED",
        "artifact": "30_project/docs/1_story/script_breakdown_v1.yaml",
        "action": "确认 script_breakdown 初版",
    },
    {
        "stage": "Stage C",
        "key": "STAGE_C_DECISION_APPROVED",
        "artifact": "00_human/DECISIONS.md",
        "action": "确认方向性/制片决策",
    },
    {
        "stage": "Stage A1",
        "key": "AUDIO_PLAN_APPROVED",
        "artifact": "30_project/docs/2_audio/_artifacts/audio_plan_v1.yaml",
        "action": "确认音频计划",
    },
    {
        "stage": "Stage A2",
        "key": "AUDIO_PROMPTS_APPROVED",
        "artifact": "30_project/docs/2_audio/_artifacts/prompt_packs/dialogue_vo_prompt_pack_v1.yaml + 30_project/docs/2_audio/_artifacts/prompt_packs/sfx_prompt_pack_v1.yaml + 30_project/docs/2_audio/_artifacts/prompt_packs/music_prompt_pack_v1.yaml",
        "action": "确认音频提示词",
    },
    {
        "stage": "Stage A3",
        "key": "AUDIO_REVIEW_APPROVED",
        "artifact": "30_project/docs/2_audio/_artifacts/reports/audio_review_v1.md",
        "action": "确认音频验收",
    },
    {
        "stage": "Stage D",
        "key": "CINEMATIC_INTENT_APPROVED",
        "artifact": "30_project/docs/2_layout/_artifacts/inputs/2-1_cinematic_intent_v1.yaml",
        "action": "确认 cinematic intent",
    },
    {
        "stage": "Stage P1.5",
        "key": "SHOT_MAP_SRT_XML_APPROVED",
        "artifact": "30_project/docs/2_layout/_artifacts/editing_bridge/shot_map_v1.srt + 30_project/docs/2_layout/_artifacts/editing_bridge/timeline_plan_v1.xml",
        "action": "确认 shot map SRT 与规划 XML",
    },
    {
        "stage": "Stage E",
        "key": "LAYOUT_FREEZE_APPROVED",
        "artifact": "30_project/docs/2_layout/2-2_layout_freeze.yaml",
        "action": "确认 layout freeze",
    },
    {
        "stage": "Stage LR",
        "key": "LAYOUT_REVIEW_APPROVED",
        "artifact": "30_project/docs/2_layout/_artifacts/reports/layout_review_v1.md",
        "action": "确认 layout review",
    },
    {
        "stage": "Stage K",
        "key": "LOOKDEV_PROMPTS_APPROVED",
        "artifact": "30_project/docs/2_layout/_artifacts/prompt_packs/branch_lookdev_shot_prompt_pack_v1.yaml",
        "action": "确认 lookdev prompt pack",
    },
    {
        "stage": "Stage K_R",
        "key": "LOOKDEV_REVIEW_APPROVED",
        "artifact": "30_project/docs/2_layout/_artifacts/reports/lookdev_review_v1.md",
        "action": "确认 lookdev review 报告",
    },
    {
        "stage": "Stage F",
        "key": "EXEC_PLAN_APPROVED",
        "artifact": "20_runtime/exec/execution_plan.json",
        "action": "确认执行计划",
    },
    {
        "stage": "Stage G1",
        "key": "COLOR_QC_APPROVED",
        "artifact": "30_project/docs/5_color/_artifacts/reports/color_qc_v1.md",
        "action": "确认 color QC 检测",
    },
    {
        "stage": "Stage G2",
        "key": "COLOR_REVIEW_APPROVED",
        "artifact": "30_project/docs/5_color/_artifacts/reports/color_review_v1.md",
        "action": "确认 color review 报告",
    },
]


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


def parse_product_paths(product: str):
    if not product:
        return []
    parts = [part.strip() for part in product.split("+")]
    return [part for part in parts if part]


def artifact_exists(paths):
    if not paths:
        return False
    return all((REPO_ROOT / path).exists() for path in paths)


def parse_approvals_table(text):
    lines = text.splitlines()
    data = {}
    start = None
    for idx, line in enumerate(lines):
        if line.startswith("| Approval Key"):
            start = idx
            break
    if start is None:
        return data
    for line in lines[start + 2:]:
        if not line.startswith("|"):
            break
        if line.startswith("| --"):
            continue
        parts = [part.strip() for part in line.strip().split("|")[1:-1]]
        if len(parts) < 4:
            continue
        key, artifact, status, notes = parts[:4]
        data[key] = {"artifact": artifact, "status": status, "notes": notes}
    return data


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


def write_inbox_table(approvals_data, stages):
    stage_lookup = {stage["name"]: stage for stage in stages}
    stage_order = {stage["name"]: idx + 1 for idx, stage in enumerate(stages)}
    rows = [
        "# INBOX",
        "",
        "| Stage | Gate Key | Status | Order | Action | Artifact |",
        "| -- | -- | -- | -- | -- | -- |",
    ]
    actionable_found = False
    for stage_def in sorted(
        STAGE_GATE_DEFINITIONS, key=lambda item: stage_order.get(item["stage"], float("inf"))
    ):
        stage_info = stage_lookup.get(stage_def["stage"])
        if not stage_info:
            continue
        product_paths = parse_product_paths(stage_info.get("product", ""))
        exists = artifact_exists(product_paths)
        prereqs = stage_info.get("requires", [])
        prereq_ok = all(
            approvals_data.get(req, {}).get("status", "").lower() == "approved"
            for req in prereqs
        )
        entry = approvals_data.get(stage_def["key"])
        status = entry.get("status") if entry else "pending"
        approved = str(status).lower() == "approved"
        if exists and prereq_ok and not approved:
            order = stage_order.get(stage_def["stage"], 0)
            rows.append(
                f"| {stage_def['stage']} | {stage_def['key']} | {status} | {order} | {stage_def['action']} | {stage_def['artifact']} |"
            )
            actionable_found = True
    if not actionable_found:
        rows.append("| - | - | - | - | - | - |")
        rows.append("> 当前无可行动的 gate，等待下一步。")
    with INBOX_PATH.open("w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")


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
    ensure_structure(entries)
    ensure_human_templates()
    approvals_text = load_approvals()
    approvals_data = parse_approvals_table(approvals_text)
    stages = load_pipeline_stages()
    write_inbox_table(approvals_data, stages)
    if not SOURCE_SCRIPT_PATH.exists():
        print("缺失 30_project/inputs/script/source_script.md，暂停 1_story 生成，等待人工上传或通过 0-source/raw 补全。")
        sys.exit(1)
    enforce_stage_gates(stages, approvals_text)


if __name__ == "__main__":
    main()
