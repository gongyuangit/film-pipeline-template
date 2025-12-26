#!/usr/bin/env python3
"""Inspect `30_project/inputs/` and keep `00_human/INBOX.md` in sync with the detected state."""

from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_INPUTS_ROOT = ROOT / "30_project" / "inputs"
DEFAULT_INBOX_PATH = ROOT / "00_human" / "INBOX.md"
KEY_INPUT_DIRS = ["script", "storyboard", "reference", "assets"]
IGNORED_FILENAMES = {".gitkeep", ".DS_Store"}
MARKER_START = "<!-- inputs-detection:start -->"
MARKER_END = "<!-- inputs-detection:end -->"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check for provided inputs and refresh INBOX material status."
    )
    parser.add_argument(
        "-i",
        "--inputs-root",
        type=Path,
        default=DEFAULT_INPUTS_ROOT,
        help="Inputs directory root to scan (default: %(default)s).",
    )
    parser.add_argument(
        "--inbox-path",
        type=Path,
        default=DEFAULT_INBOX_PATH,
        help="INBOX.md to update with the latest detection summary.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the generated section without writing back to INBOX.md.",
    )
    return parser.parse_args()


def collect_material_paths(inputs_root: Path) -> list[Path]:
    candidates = set()
    if inputs_root.exists():
        # capture files directly inside inputs root
        for child in inputs_root.iterdir():
            if child.is_file():
                if child.name in IGNORED_FILENAMES:
                    continue
                candidates.add(child.relative_to(inputs_root))
        # capture files under each key directory (case-insensitive match)
        for child in inputs_root.iterdir():
            if not child.is_dir():
                continue
            if child.name.lower() not in KEY_INPUT_DIRS:
                continue
            for candidate in child.rglob("*"):
                if not candidate.is_file():
                    continue
                if candidate.name in IGNORED_FILENAMES:
                    continue
                candidates.add(candidate.relative_to(inputs_root))
    return sorted(candidates, key=lambda item: item.as_posix())


def format_detected_section(found: list[Path], inputs_root: Path) -> str:
    if not found:
        return textwrap.dedent(
            """\
            **状态**：pending  
            **说明**：尚未检测到 `30_project/inputs/` 下的素材，请在以下路径添加相应内容后重新运行 `make check-inputs`。`index.yaml` 可选但不再作为启动阻塞。
            
            | 内容名称 | 是否必需 | 放置路径 | 简短备注 |
            | 剧本/脚本 | 必需 | `30_project/inputs/script/` | 提供完整脚本或文本（如 `script.pdf`, `剧本.md`），包含镜头/对白/节奏 |
            | 分镜/故事板 | 必需 | `30_project/inputs/storyboard/` | 提供分镜或视觉概念文件，标注镜头编号与时长参考 |
            | 拍摄/视觉参考 | 必需 | `30_project/inputs/reference/` | 放置关键参考图、参考片段说明（支持 `.jpg`, `.png`, `.txt` 等） |
            | 素材/已有镜头 | 可选 | `30_project/inputs/assets/` | 若已有素材片段，可放入此目录并保持可读格式（如 `mp4`, `mov`） |
            """
        )

    lines = "\n".join(f"- `{path.as_posix()}`" for path in found)
    index_status = (
        "已提供"
        if (inputs_root / "index.yaml").is_file()
        else "未提供（可选，非阻塞）"
    )
    return textwrap.dedent(
        f"""\
        **状态**：resolved  
        **说明**：检测到如下素材，已满足“空项目”前置条件，Codex 仅在得到进一步明确指令后才会继续生成内容。  
        {lines}
        
        `index.yaml`：{index_status}
        """
    )


def rewrite_section(inbox_text: str, replacement: str) -> str:
    if MARKER_START not in inbox_text or MARKER_END not in inbox_text:
        raise RuntimeError(
            "INBOX.md is missing inputs-detection markers; please add them before running this script."
        )
    start_idx = inbox_text.index(MARKER_START) + len(MARKER_START)
    end_idx = inbox_text.index(MARKER_END)
    replaced = inbox_text[:start_idx] + "\n" + replacement.strip() + "\n" + inbox_text[end_idx:]
    return replaced


def main() -> None:
    args = parse_args()
    inputs_root = args.inputs_root.expanduser()
    if not inputs_root.is_absolute():
        inputs_root = (Path.cwd() / inputs_root).resolve(strict=False)
    else:
        inputs_root = inputs_root.resolve(strict=False)
    inbox_path = args.inbox_path.expanduser().resolve(strict=False)

    found = collect_material_paths(inputs_root)
    section = format_detected_section(found, inputs_root)
    print("=== 素材检测结果 ===")
    print(section.strip())
    print("====================")

    if args.dry_run:
        return

    text = inbox_path.read_text(encoding="utf-8")
    updated = rewrite_section(text, section)
    inbox_path.write_text(updated, encoding="utf-8")
    try:
        inbox_ref = inbox_path.relative_to(ROOT)
    except ValueError:
        inbox_ref = inbox_path
    print(f"已更新 {inbox_ref}")


if __name__ == "__main__":
    main()
