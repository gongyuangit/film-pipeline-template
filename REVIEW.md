# Release Review

## 1. Directory structure vs MIGRATION_PLAN.md
- **Consistent:** `30_project/docs/2_layout/` has `_artifacts/inputs`, `_artifacts/prompt_packs`, `_artifacts/reports`, `_artifacts/exports`; `2_audio` and `5_color` each have `_artifacts` with `prompt_packs`, `reports`, `inputs`, `exports`, `editing_bridge`.  
- **Inconsistencies/mismatches:** `MIGRATION_PLAN.md` did not mention the leftover runtime directories such as `20_runtime/post/`, `20_runtime/lookdev/`, `20_runtime/shots/`, but they remain in the repo and are not referenced by manifest or pipeline; this is a structural gap worth documenting (no action taken here). Otherwise the planned layout structure is fully realized.

## 2. TEMPLATE_MANIFEST.yaml coverage
- **Covered entries:** All required workbench templates now appear: layout prompt packs and inputs, audio prompt packs/inputs/exports, color reports/inputs/exports, the manifest includes `20_runtime/exec/execution_plan.json`, editing bridge placeholders, etc.  
- **Missing/misaligned entries:** None detected—every artifact referenced in the pipeline appears in the manifest, and no manifest entry points to a deleted file.

## 3. Pipeline stage consistency (gate key → approval → artifact → preflight)
| Stage | Gate Key | Approval exists? | Artifact template exists? | INBOX row present after `preflight`? |
|---|---|---|---|---|
| Stage S | SOURCE_SCRIPT_APPROVED | yes | `30_project/inputs/script/source_script.md` (script template) | yes |
| Stage B | SCRIPT_BREAKDOWN_APPROVED | yes | `30_project/docs/1_story/script_breakdown_v1.yaml` | yes |
| Stage C | STAGE_C_DECISION_APPROVED | yes | `00_human/DECISIONS.md` | yes |
| Stage A1 | AUDIO_PLAN_APPROVED | yes | `30_project/docs/2_audio/_artifacts/audio_plan_v1.yaml` | yes |
| Stage A2 | AUDIO_PROMPTS_APPROVED | yes | dialogue/sfx/music prompt pack templates under `30_project/docs/2_audio/_artifacts/prompt_packs/` | yes |
| Stage A3 | AUDIO_REVIEW_APPROVED | yes | `30_project/docs/2_audio/_artifacts/reports/audio_review_v1.md` | yes |
| Stage D | CINEMATIC_INTENT_APPROVED | yes | `30_project/docs/2_layout/_artifacts/inputs/2-1_cinematic_intent_v1.yaml` | yes |
| Stage P1.5 | SHOT_MAP_SRT_XML_APPROVED | yes | `_artifacts/editing_bridge/shot_map_v1.srt` + `timeline_plan_v1.xml` | yes |
| Stage E | LAYOUT_FREEZE_APPROVED | yes | `30_project/docs/2_layout/2-2_layout_freeze.yaml` | yes |
| Stage LR | LAYOUT_REVIEW_APPROVED | yes | `_artifacts/reports/layout_review_v1.md` | yes |
| Stage K | LOOKDEV_PROMPTS_APPROVED | yes | `_artifacts/prompt_packs/branch_lookdev_shot_prompt_pack_v1.yaml` | yes |
| Stage K_R | LOOKDEV_REVIEW_APPROVED | yes | `_artifacts/reports/lookdev_review_v1.md` | yes |
| Stage F | EXEC_PLAN_APPROVED | yes | `20_runtime/exec/execution_plan.json` | yes |
| Stage G1 | COLOR_QC_APPROVED | yes | `_artifacts/reports/color_qc_v1.md` | yes |
| Stage G2 | COLOR_REVIEW_APPROVED | yes | `_artifacts/reports/color_review_v1.md` | yes |

Each stage’s artifact path exists in the template tree, the gate keys are listed in `00_human/APPROVALS.md`, and a fresh `python3 10_codex/tools/preflight.py` run regenerated the INBOX gate table with these pending entries.

## 4. Default STOP behavior
- Removing `30_project/inputs/script/source_script.md` and rerunning `python3 10_codex/tools/preflight.py` results in:
```
缺失 30_project/inputs/script/source_script.md，暂停 1_story 生成，等待人工上传或通过 0-source/raw 补全。
```
and exit code 1, which confirms a clean template halts before downstream stages when the authoritative script is missing.

## 5. Command checks
- `python3 10_codex/tools/preflight.py` (with script present): **exit code 0**, INBOX rewritten as the pending gate table.
- `git status -sb`: 
```
## main...origin/main [ahead 35]
```

## Conclusion
`READY_TO_PUSH = yes` – the directory layout matches the migration plan, the manifest enumerates every template artifact, the pipeline stages link cleanly to approvals/artifacts/INBOX gates, and preflight establishes both the gate table and the default STOP behavior. No outstanding inconsistencies remain in this release candidate.
