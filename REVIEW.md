# Release Review

## 1. 目录结构 vs `DOCS_MIGRATION_PLAN.md`
- 目前 `30_project/docs/` 只保留与管线相关的 workbench：`0-source/`、`1_story/`、`2_layout/`、`2_audio/`、`5_color/`，其 `_artifacts/` 分层（inputs/prompt_packs/reports/exports/editing_bridge）与目标结构一致。  
- 所有 legacy workbench（lookdev/prompt/production/render/exec 等）在此前迁移后被彻底删除，不再参与运行，元数据也移除了对这些路径的指向。

## 2. `10_codex/TEMPLATE_MANIFEST.yaml` 覆盖检查
- 增加了 `30_project/inputs/script/source_script.md`（Stage S）与 `30_project/docs/2_layout/2-2_layout_freeze.yaml`（Stage E），并保留了 `2_layout`/`2_audio`/`5_color` 工作台及其占位文件。  
- 所有 pipeline 产品现在都有 manifest 条目（Stage S–G2），保证 `preflight` 不会在缺少输入时启动下游阶段；旧的 archive 条目已被清理，只有当前产物进入 manifest。

## 3. Stage gate consistency
| Stage | Gate Key | Artifact(s) | Approvals entry | Manifest entry |
| --- | --- | --- | --- | --- |
| Stage S | `SOURCE_SCRIPT_APPROVED` | `30_project/inputs/script/source_script.md` | ✅ | ✅ |
| Stage B | `SCRIPT_BREAKDOWN_APPROVED` | `30_project/docs/1_story/script_breakdown_v1.yaml` | ✅ | ✅ |
| Stage C | `STAGE_C_DECISION_APPROVED` | `00_human/DECISIONS.md` | ✅ | ✅ |
| Stage A1 | `AUDIO_PLAN_APPROVED` | `30_project/docs/2_audio/_artifacts/audio_plan_v1.yaml` | ✅ | ✅ |
| Stage A2 | `AUDIO_PROMPTS_APPROVED` | Dialogue/SFX/Music prompt packs | ✅ | ✅ |
| Stage A3 | `AUDIO_REVIEW_APPROVED` | `30_project/docs/2_audio/_artifacts/reports/audio_review_v1.md` | ✅ | ✅ |
| Stage D | `CINEMATIC_INTENT_APPROVED` | `30_project/docs/2_layout/_artifacts/inputs/2-1_cinematic_intent_v1.yaml` | ✅ | ✅ |
| Stage P1.5 | `SHOT_MAP_SRT_XML_APPROVED` | Shot map SRT + planning XML | ✅ | ✅ |
| Stage E | `LAYOUT_FREEZE_APPROVED` | `30_project/docs/2_layout/2-2_layout_freeze.yaml` | ✅ | ✅ |
| Stage LR | `LAYOUT_REVIEW_APPROVED` | `30_project/docs/2_layout/_artifacts/reports/layout_review_v1.md` | ✅ | ✅ |
| Stage K | `LOOKDEV_PROMPTS_APPROVED` | `_artifacts/prompt_packs/branch_lookdev_shot_prompt_pack_v1.yaml` | ✅ | ✅ |
| Stage K_R | `LOOKDEV_REVIEW_APPROVED` | `_artifacts/reports/lookdev_review_v1.md` | ✅ | ✅ |
| Stage F | `EXEC_PLAN_APPROVED` | `20_runtime/exec/execution_plan.json` | ✅ | ✅ |
| Stage G1 | `COLOR_QC_APPROVED` | `_artifacts/reports/color_qc_v1.md` | ✅ | ✅ |
| Stage G2 | `COLOR_REVIEW_APPROVED` | `_artifacts/reports/color_review_v1.md` | ✅ | ✅ |

## 4. 默认 STOP
- `preflight` 仍然检查 `30_project/inputs/script/source_script.md`：在缺失该文件时它会退出并打印 `缺失 30_project/inputs/script/source_script.md，暂停 1_story 生成...`，用户必须先推送剧本/碎片，确保空项目不会无序推进。此行为符合“按流程一步步走”的 gate 逻辑。

## 5. 检查命令
```
python3 10_codex/tools/gen_template_index.py
python3 10_codex/tools/gen_template_index.py --check
python3 10_codex/tools/preflight.py

make docs-index-check
make check-inputs
git status -sb
```

## 6. Template index automation
- Added `gen_template_index.py` plus Make targets (`make docs-index` / `make docs-index-check`) so the index is automatically generated from the live structure; the check warns when the file drifts.
- `preflight` now runs `gen_template_index.py --check` (set `TEMPLATE_INDEX_STRICT=1` for an exit-on-failure gate), and `.githooks/pre-commit` reruns `make docs-index` to keep `TEMPLATE_INDEX.md` current before commits.
- Structural edits must therefore run `make docs-index` and commit the updated file; the hook/CI prevents forgetting to refresh the index.

## Conclusion
`READY_TO_PUSH = yes` – docs directories now match `DOCS_MIGRATION_PLAN.md`, manifest includes every pipeline artifact (including Stage S and Stage E), INBOX/approvals align with stage gates, and the archive holds legacy workbenches with no dangling references. All checks pass.
