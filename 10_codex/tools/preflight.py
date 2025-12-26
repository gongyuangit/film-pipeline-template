import sys
from datetime import datetime
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "10_codex" / "TEMPLATE_MANIFEST.yaml"
INBOX_PATH = REPO_ROOT / "00_human" / "INBOX.md"
SOURCE_SCRIPT_PATH = REPO_ROOT / "30_project" / "inputs" / "script" / "source_script.md"


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
    if not source_exists and not row_exists:
        gate_row = "| 6 | pending | 请先将 `30_project/inputs/script/source_script.md` 提供为权威剧本文本，或继续在 `30_project/docs/0-source/raw/` 投递碎片供 Source Synthesis 合成；之后再继续 1_story。 |  |"
        rows.append(gate_row)
    return lines[:start] + header + rows + lines[end:]


def main():
    entries = load_manifest()
    created = ensure_structure(entries)
    append_preflight_summary(created)
    INBOX_TEXT = INBOX_PATH.read_text(encoding="utf-8")
    if "## Preflight" not in INBOX_TEXT:
        ensure_preflight_section()
    update_source_script_gate()
    if not SOURCE_SCRIPT_PATH.exists():
        print("缺失 30_project/inputs/script/source_script.md，暂停 1_story 生成，等待人工上传或通过 0-source/raw 补全。")
        sys.exit(1)


if __name__ == "__main__":
    main()
