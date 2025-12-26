# INBOX

| Order | Stage | Gate Key | Status | Prereq | Artifact | Notes |
| -- | -- | -- | -- | -- | -- | -- |
| 1 | Stage S | SOURCE_SCRIPT_APPROVED | approved | yes | 30_project/inputs/script/source_script.md (exists) | Source Synthesis / script confirmation |
| 2 | Stage B | SCRIPT_BREAKDOWN_APPROVED | approved | yes | 30_project/docs/1_story/script_breakdown_v1.yaml (exists) | Script breakdown (first draft) |
| 3 | Stage C | STAGE_C_DECISION_APPROVED | approved | yes | 00_human/DECISIONS.md (exists) | Human creative/production decisions |
| 4 | Stage A1 | AUDIO_PLAN_APPROVED | pending | yes | 30_project/docs/2_audio/_artifacts/audio_plan_v1.yaml (exists) | Audio plan |
| 5 | Stage A2 | AUDIO_PROMPTS_APPROVED | blocked | missing: AUDIO_PLAN_APPROVED | 30_project/docs/2_audio/_artifacts/prompt_packs/dialogue_vo_prompt_pack_v1.yaml + 30_project/docs/2_audio/_artifacts/prompt_packs/sfx_prompt_pack_v1.yaml + 30_project/docs/2_audio/_artifacts/prompt_packs/music_prompt_pack_v1.yaml (exists) | Audio prompt packs |
| 6 | Stage A3 | AUDIO_REVIEW_APPROVED | blocked | missing: AUDIO_PROMPTS_APPROVED | 30_project/docs/2_audio/_artifacts/reports/audio_review_v1.md (exists) | Audio review |
| 7 | Stage D | CINEMATIC_INTENT_APPROVED | pending | yes | 30_project/docs/2_layout/_artifacts/inputs/2-1_cinematic_intent_v1.yaml (exists) | Cinematic intent / layout guidance |
| 8 | Stage P1.5 | SHOT_MAP_SRT_XML_APPROVED | blocked | missing: CINEMATIC_INTENT_APPROVED | 30_project/docs/2_layout/_artifacts/editing_bridge/shot_map_v1.srt + 30_project/docs/2_layout/_artifacts/editing_bridge/timeline_plan_v1.xml (exists) | Shot map SRT for downstream mapping |
| 9 | Stage E | LAYOUT_FREEZE_APPROVED | blocked | missing: SHOT_MAP_SRT_XML_APPROVED | 30_project/docs/2_layout/2-2_layout_freeze.yaml (exists) | Layout freeze |
| 10 | Stage LR | LAYOUT_REVIEW_APPROVED | blocked | missing: LAYOUT_FREEZE_APPROVED | 30_project/docs/2_layout/_artifacts/reports/layout_review_v1.md (exists) | Layout review and acceptance |
| 11 | Stage K | LOOKDEV_PROMPTS_APPROVED | blocked | missing: LAYOUT_REVIEW_APPROVED, CINEMATIC_INTENT_APPROVED | 30_project/docs/2_layout/_artifacts/prompt_packs/branch_lookdev_shot_prompt_pack_v1.yaml (exists) | Lookdev shot prompts |
| 12 | Stage K_R | LOOKDEV_REVIEW_APPROVED | blocked | missing: LOOKDEV_PROMPTS_APPROVED | 30_project/docs/2_layout/_artifacts/reports/lookdev_review_v1.md (exists) | Lookdev review (must cover STANDARDS_LOOKDEV.md pillars) |
| 13 | Stage F | EXEC_PLAN_APPROVED | blocked | missing: LAYOUT_FREEZE_APPROVED, LOOKDEV_PROMPTS_APPROVED, LOOKDEV_REVIEW_APPROVED | 20_runtime/exec/execution_plan.json (exists) | Execution planning |
| 14 | Stage G1 | COLOR_QC_APPROVED | blocked | missing: EXEC_PLAN_APPROVED | 30_project/docs/5_color/_artifacts/reports/color_qc_v1.md (exists) | Color QC (machine measurable checks) |
| 15 | Stage G2 | COLOR_REVIEW_APPROVED | blocked | missing: COLOR_QC_APPROVED | 30_project/docs/5_color/_artifacts/reports/color_review_v1.md (exists) | Color review (pass/fail gate before final deliver) |
