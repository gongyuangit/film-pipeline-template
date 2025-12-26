# Tools Audit

## 1. `10_codex/tools/` scripts
| Script | Entry point / purpose | Called by | Still in use? | Notes |
| -- | -- | -- | -- | -- |
| `preflight.py` | Builds INBOX/NOW, enforces gates, runs template-index check | `make preflight` (default via repo root `Makefile`), `check_inputs`, various automation flows | ✅ | Central gate control; drives dashboards & gating logic |
| `check_inputs.py` | Inspect `30_project/inputs/` and refresh INBOX markers | `make check-inputs` | ✅ | Relies on `preflight` output; handles materials detection text only |
| `generate_plan.py` | Produce `20_runtime/plan/shot_list.json` from `index.yaml` | `make plan` (preflight + this target) | ✅ | Distinct `plan` output; no overlap |
| `generate_exec_plan.py` | Convert shot plan into `20_runtime/exec/execution_plan.json` | `make exec-plan` | ✅ | Sequence continues `plan` output; essential for execution placeholder |
| `gen_template_index.py` | Regenerates `10_codex/TEMPLATE_INDEX.md` | `make docs-index`, `make docs-index-check`, `preflight` (via reflect) | ✅ | Now canonical index generator; no duplicates |

## 2. Duplication check
- Every capability has a single canonical script; plan/execution generation is intentionally split (`generate_plan.py` → `generate_exec_plan.py`), `preflight`/`check_inputs` remain unique, and the new `gen_template_index.py` centralizes index generation. No redundant entrypoints exist.

## 3. Recommendation
- Keep `preflight.py`, `check_inputs.py`, `generate_plan.py`, `generate_exec_plan.py`, and `gen_template_index.py` as the canonical tools. No script consolidation needed today—just ensure future additions add one well-documented entry per capability to avoid duplication.
