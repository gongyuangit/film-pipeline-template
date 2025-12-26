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
        "| Order | Stage | Gate Key | Status | Prereq | Artifact | Notes |\n"
        "| -- | -- | -- | -- | -- | -- | -- |\n"
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
    rows = [
        "# INBOX",
        "",
        "| Order | Stage | Gate Key | Status | Prereq | Artifact | Notes |",
        "| -- | -- | -- | -- | -- | -- | -- |",
    ]
    for order, stage in enumerate(stages, start=1):
        gate_key = stage.get("approval_key") or stage.get("name")
        product = stage.get("product", "-")
        product_paths = parse_product_paths(product)
        exists = artifact_exists(product_paths)
        missing_prereqs = [
            req
            for req in stage.get("requires", [])
            if approvals_data.get(req, {}).get("status", "").lower() != "approved"
        ]
        prereq_ok = not missing_prereqs
        entry = approvals_data.get(gate_key, {})
        raw_status = entry.get("status", "pending")
        approved = str(raw_status).lower() == "approved"
        if approved:
            status = "approved"
        elif not prereq_ok:
            status = "blocked"
        else:
            status = "pending"
        prereq_display = "yes" if prereq_ok else f"missing: {', '.join(missing_prereqs)}"
        if product:
            missing_paths = [
                path for path in product_paths if not (REPO_ROOT / path).exists()
            ]
            if missing_paths:
                artifact_display = f"{product} (missing: {', '.join(missing_paths)})"
            else:
                artifact_display = f"{product} (exists)"
        else:
            artifact_display = "-"
        notes_parts = [stage.get("description", "").strip()]
        if not notes_parts[0]:
            notes_parts = []
        if status == "pending" and not exists:
            notes_parts.append("waiting artifact")
        notes = "；".join(part for part in notes_parts if part)
        rows.append(
            f"| {order} | {stage.get('name')} | {gate_key} | {status} | {prereq_display} | {artifact_display} | {notes} |"
        )
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
