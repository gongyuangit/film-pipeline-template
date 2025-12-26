import os
import re
import subprocess
import sys
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "10_codex" / "TEMPLATE_MANIFEST.yaml"
INBOX_PATH = REPO_ROOT / "00_human" / "INBOX.md"
SOURCE_SCRIPT_PATH = REPO_ROOT / "30_project" / "inputs" / "script" / "source_script.md"
STAGE_PATH = REPO_ROOT / "10_codex" / "PIPELINE_STAGES.yaml"
APPROVALS_PATH = REPO_ROOT / "00_human" / "APPROVALS.md"
PROJECT_MODE_PATH = REPO_ROOT / "30_project" / "inputs" / "index.yaml"


HUMAN_TEMPLATES = {
    "00_human/INBOX.md": (
        "# INBOX\n"
        "| Order | Stage | Gate Key | Status | Action | Artifact | Prereq | Artifact Exists | Artifact Ready | Notes |\n"
        "| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |\n"
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
    "00_human/NOW.md": (
        "# NOW\n"
        "| Order | Stage | Gate Key | Status | Action | Artifact |\n"
        "| -- | -- | -- | -- | -- | -- |\n"
    ),
}

TEMPLATE_READY_WHITELIST = {"STAGE_C_DECISION_APPROVED"}
DEFAULT_PROJECT_MODE = "template"

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


def file_has_placeholder(path):
    target = REPO_ROOT / path
    if not target.exists():
        return False
    try:
        with open(target, "r", encoding="utf-8", errors="ignore") as f:
            for _ in range(5):
                line = f.readline()
                if not line:
                    break
                if "TEMPLATE_PLACEHOLDER" in line:
                    return True
    except (OSError, UnicodeDecodeError):
        return False
    return False


def content_nontrivial(target: Path):
    try:
        text = target.read_text(encoding="utf-8", errors="ignore")
    except (OSError, UnicodeDecodeError):
        return False
    lines = [line for line in text.splitlines() if "TEMPLATE_PLACEHOLDER" not in line]
    cleaned = [line.strip() for line in lines if line.strip()]
    suffix = target.suffix.lower()
    joined = "\n".join(cleaned)
    if suffix in {".yaml", ".yml", ".md", ".json"}:
        return len(cleaned) >= 5 or len(joined) >= 50
    if suffix == ".srt":
        for idx in range(len(lines) - 1):
            if lines[idx].strip().isdigit() and "-->" in lines[idx + 1]:
                return True
        return False
    if suffix == ".xml":
        lower = joined.lower()
        return "<timeline" in lower and len(joined) >= 40
    return len(joined) >= 50


def artifact_ready_info(paths):
    missing = []
    placeholders = []
    insufficient = []
    if not paths:
        return False, missing, placeholders, insufficient
    for path in paths:
        target = REPO_ROOT / path
        if not target.exists():
            missing.append(path)
            continue
        if file_has_placeholder(path):
            placeholders.append(path)
            continue
        if not content_nontrivial(target):
            insufficient.append(path)
    ready = not (missing or placeholders or insufficient)
    return ready, missing, placeholders, insufficient


def load_project_mode():
    if not PROJECT_MODE_PATH.exists():
        return DEFAULT_PROJECT_MODE
    try:
        data = yaml.safe_load(PROJECT_MODE_PATH.read_text())
        if isinstance(data, dict):
            return data.get("project_mode", DEFAULT_PROJECT_MODE)
    except yaml.YAMLError:
        pass
    return DEFAULT_PROJECT_MODE


def run_template_index_check(strict: bool = False):
    script = REPO_ROOT / "10_codex" / "tools" / "gen_template_index.py"
    if not script.exists():
        return True
    cmd = [sys.executable, str(script), "--check"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return True
    print("template index is out of sync. Run `make docs-index` and commit the result.")
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip())
    if strict:
        sys.exit(result.returncode)
    return False

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


def build_stage_status(stage, approvals_data, project_mode):
    gate_key = stage.get("approval_key") or stage.get("name")
    product = stage.get("product", "").strip() or "-"
    product_paths = parse_product_paths(product)
    exists_flag = artifact_exists(product_paths)
    artifact_ready_flag, missing_ready, placeholder_paths, insufficient = artifact_ready_info(
        product_paths
    )
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
    if product == "-":
        artifact_display = "-"
        artifact_exists_col = "-"
        artifact_ready_display = "-"
    else:
        missing_paths = [path for path in product_paths if not (REPO_ROOT / path).exists()]
        artifact_display = (
            f"{product} (missing: {', '.join(missing_paths)})"
            if missing_paths
            else f"{product} (exists)"
        )
        artifact_exists_col = (
            "yes" if exists_flag else f"no (missing: {', '.join(missing_paths)})"
        )
        reasons = []
        if missing_ready:
            reasons.append(f"missing: {', '.join(missing_ready)}")
        if placeholder_paths:
            reasons.append(f"placeholder: {', '.join(placeholder_paths)}")
        if insufficient:
            reasons.append(f"insufficient content: {', '.join(insufficient)}")
        artifact_ready_display = (
            "yes" if artifact_ready_flag else f"no ({'; '.join(reasons)})"
        )
    template_override = (
        project_mode == "template" and gate_key not in TEMPLATE_READY_WHITELIST
    )
    if template_override:
        artifact_ready_flag = False
        if artifact_ready_display == "yes":
            artifact_ready_display = "no (template mode)"
        elif "template mode" not in artifact_ready_display:
            artifact_ready_display = f"{artifact_ready_display}；template mode"
    prereq_display = "yes" if prereq_ok else f"missing: {', '.join(missing_prereqs)}"
    action_description = stage.get("description", "").strip() or stage.get("name")
    notes_parts = [stage.get("description", "").strip()]
    if not notes_parts[0]:
        notes_parts = []
    if status == "pending" and not exists_flag:
        notes_parts.append("waiting artifact")
    elif status == "pending" and placeholder_paths:
        notes_parts.append("waiting placeholder resolution")
    notes = "；".join(part for part in notes_parts if part)
    return {
        "stage_name": stage.get("name"),
        "gate_key": gate_key,
        "status": status,
        "action": action_description,
        "artifact": artifact_display,
        "prereq": prereq_display,
        "artifact_exists": artifact_exists_col,
        "artifact_ready": artifact_ready_display,
        "artifact_ready_flag": artifact_ready_flag,
        "prereq_ok": prereq_ok,
        "exists": exists_flag,
        "notes": notes,
    }


def write_inbox_table(approvals_data, stages, project_mode):
    rows = [
        "# INBOX",
        "",
        "| Order | Stage | Gate Key | Status | Action | Artifact | Prereq | Artifact Exists | Artifact Ready | Notes |",
        "| -- | -- | -- | -- | -- | -- | -- | -- | -- | -- |",
    ]
    for order, stage in enumerate(stages, start=1):
        stage_status = build_stage_status(stage, approvals_data, project_mode)
        rows.append(
            f"| {order} | {stage_status['stage_name']} | {stage_status['gate_key']} | {stage_status['status']} | "
            f"{stage_status['action']} | {stage_status['artifact']} | {stage_status['prereq']} | {stage_status['artifact_exists']} | {stage_status['artifact_ready']} | {stage_status['notes']} |"
        )
    with INBOX_PATH.open("w", encoding="utf-8") as f:
        f.write("\n".join(rows) + "\n")


def write_now_table(approvals_data, stages, project_mode):
    rows = [
        "# NOW",
        "",
        "| Order | Stage | Gate Key | Status | Action | Artifact |",
        "| -- | -- | -- | -- | -- | -- |",
    ]
    actionable_found = False
    for order, stage in enumerate(stages, start=1):
        stage_status = build_stage_status(stage, approvals_data, project_mode)
        if (
            project_mode == "template"
            or stage_status["status"] != "pending"
            or not stage_status["prereq_ok"]
            or not stage_status["artifact_ready_flag"]
        ):
            continue
        actionable_found = True
        rows.append(
            f"| {order} | {stage_status['stage_name']} | {stage_status['gate_key']} | {stage_status['status']} | "
            f"{stage_status['action']} | {stage_status['artifact']} |"
        )
    if project_mode == "template":
        rows.append("| - | - | - | - | - | - |")
        rows.append("> 当前为模板模式（project_mode=template），请复制项目并设置 project_mode 为 project 后再继续。")
    elif not actionable_found:
        rows.append("| - | - | - | - | - | - |")
        rows.append("> 当前无可行动的 gate。")
    NOW_PATH = REPO_ROOT / "00_human" / "NOW.md"
    with NOW_PATH.open("w", encoding="utf-8") as f:
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
    strict_mode = os.environ.get("TEMPLATE_INDEX_STRICT") == "1"
    run_template_index_check(strict=strict_mode)
    approvals_text = load_approvals()
    approvals_data = parse_approvals_table(approvals_text)
    stages = load_pipeline_stages()
    project_mode = load_project_mode()
    write_inbox_table(approvals_data, stages, project_mode)
    write_now_table(approvals_data, stages, project_mode)
    if not SOURCE_SCRIPT_PATH.exists():
        print("缺失 30_project/inputs/script/source_script.md，暂停 1_story 生成，等待人工上传或通过 0-source/raw 补全。")
        sys.exit(1)
    enforce_stage_gates(stages, approvals_text)


if __name__ == "__main__":
    main()
