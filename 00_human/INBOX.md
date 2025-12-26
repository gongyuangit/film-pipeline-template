# INBOX

| Order | Stage | Gate Key | Status | Action | Artifact | Prereq | Artifact Exists |
| -- | -- | -- | -- | -- | -- | -- | -- |
| 1 | Stage S | SOURCE_SCRIPT_APPROVED | approved | Source Synthesis / script confirmation | 30_project/inputs/script/source_script.md (exists) | yes | yes |
| 2 | Stage B | SCRIPT_BREAKDOWN_APPROVED | approved | Script breakdown (first draft) | 30_project/docs/1_story/script_breakdown_v1.yaml (exists) | yes | yes |
| 3 | Stage C | STAGE_C_DECISION_APPROVED | approved | Human creative/production decisions | 00_human/DECISIONS.md (exists) | yes | yes |
| 4 | Stage A1 | AUDIO_PLAN_APPROVED | pending | Audio plan | 30_project/docs/2_audio/_artifacts/audio_plan_v1.yaml (exists) | yes | yes |
| 5 | Stage A2 | AUDIO_PROMPTS_APPROVED | blocked | Audio prompt packs | 30_project/docs/2_audio/_artifacts/prompt_packs/dialogue_vo_prompt_pack_v1.yaml + 30_project/docs/2_audio/_artifacts/prompt_packs/sfx_prompt_pack_v1.yaml + 30_project/docs/2_audio/_artifacts/prompt_packs/music_prompt_pack_v1.yaml (exists) | missing: AUDIO_PLAN_APPROVED | yes |
| 6 | Stage A3 | AUDIO_REVIEW_APPROVED | blocked | Audio review | 30_project/docs/2_audio/_artifacts/reports/audio_review_v1.md (exists) | missing: AUDIO_PROMPTS_APPROVED | yes |
| 7 | Stage D | CINEMATIC_INTENT_APPROVED | pending | Cinematic intent / layout guidance | 30_project/docs/2_layout/_artifacts/inputs/2-1_cinematic_intent_v1.yaml (exists) | yes | yes |
| 8 | Stage P1.5 | SHOT_MAP_SRT_XML_APPROVED | blocked | Shot map SRT for downstream mapping | 30_project/docs/2_layout/_artifacts/editing_bridge/shot_map_v1.srt + 30_project/docs/2_layout/_artifacts/editing_bridge/timeline_plan_v1.xml (exists) | missing: CINEMATIC_INTENT_APPROVED | yes |
| 9 | Stage E | LAYOUT_FREEZE_APPROVED | blocked | Layout freeze | 30_project/docs/2_layout/2-2_layout_freeze.yaml (exists) | missing: SHOT_MAP_SRT_XML_APPROVED | yes |
| 10 | Stage LR | LAYOUT_REVIEW_APPROVED | blocked | Layout review and acceptance | 30_project/docs/2_layout/_artifacts/reports/layout_review_v1.md (exists) | missing: LAYOUT_FREEZE_APPROVED | yes |
| 11 | Stage K | LOOKDEV_PROMPTS_APPROVED | blocked | Lookdev shot prompts | 30_project/docs/2_layout/_artifacts/prompt_packs/branch_lookdev_shot_prompt_pack_v1.yaml (exists) | missing: LAYOUT_REVIEW_APPROVED, CINEMATIC_INTENT_APPROVED | yes |
| 12 | Stage K_R | LOOKDEV_REVIEW_APPROVED | blocked | Lookdev review (must cover STANDARDS_LOOKDEV.md pillars) | 30_project/docs/2_layout/_artifacts/reports/lookdev_review_v1.md (exists) | missing: LOOKDEV_PROMPTS_APPROVED | yes |
| 13 | Stage F | EXEC_PLAN_APPROVED | blocked | Execution planning | 20_runtime/exec/execution_plan.json (exists) | missing: LAYOUT_FREEZE_APPROVED, LOOKDEV_PROMPTS_APPROVED, LOOKDEV_REVIEW_APPROVED | yes |
| 14 | Stage G1 | COLOR_QC_APPROVED | blocked | Color QC (machine measurable checks) | 30_project/docs/5_color/_artifacts/reports/color_qc_v1.md (exists) | missing: EXEC_PLAN_APPROVED | yes |
| 15 | Stage G2 | COLOR_REVIEW_APPROVED | blocked | Color review (pass/fail gate before final deliver) | 30_project/docs/5_color/_artifacts/reports/color_review_v1.md (exists) | missing: COLOR_QC_APPROVED | yes |
