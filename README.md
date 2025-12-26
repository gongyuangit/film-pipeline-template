# Smoke Test（已废弃）
- 该机制仅用于早期验证，现已移除；模板不再生成 `20_runtime/smoke`，且无需运行 `make smoke`。

## Plan Generation
1. Run `make plan`.
2. Check `20_runtime/plan/shot_list.json` for the generated shot list export.

## Exec Plan Generation
1. Run `make exec-plan`.
2. Review `20_runtime/exec/execution_plan.json` for the derived execution steps.

## Notes
- Codex-managed tooling now lives under `10_codex/`; `00_human/` is the only directory needing manual attention.
- Core project content resides in `30_project/` and is subject to human review per the inbox (see `00_human/README.md`).
