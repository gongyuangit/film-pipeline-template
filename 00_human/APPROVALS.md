# APPROVALS
| Approval Key | Artifact | Status | Notes |
| -- | -- | -- | -- |
| SOURCE_SCRIPT_APPROVED | source_script.md | approved |  |
| SCRIPT_BREAKDOWN_APPROVED | script_breakdown_v1.yaml | approved |  |
| STAGE_C_DECISION_APPROVED | DECISIONS.md | approved |  |
| CINEMATIC_INTENT_APPROVED | _artifacts/inputs/2-1_cinematic_intent_v1.yaml | pending |  |
| SHOT_MAP_SRT_XML_APPROVED | _artifacts/editing_bridge/shot_map_v1.srt + _artifacts/editing_bridge/timeline_plan_v1.xml | pending |  |
| LAYOUT_FREEZE_APPROVED | 2-2_layout_freeze.yaml | pending |  |
| LAYOUT_REVIEW_APPROVED | _artifacts/reports/layout_review_v1.md | pending |  |
| LOOKDEV_PROMPTS_APPROVED | _artifacts/prompt_packs/branch_lookdev_shot_prompt_pack_v1.yaml | pending |  |
| LOOKDEV_REVIEW_APPROVED | _artifacts/reports/lookdev_review_v1.md | pending |  |
| AUDIO_PLAN_APPROVED | _artifacts/audio_plan_v1.yaml | pending |  |
| AUDIO_PROMPTS_APPROVED | _artifacts/prompt_packs/dialogue_vo_prompt_pack_v1.yaml + ... | pending |  |
| AUDIO_REVIEW_APPROVED | _artifacts/reports/audio_review_v1.md | pending |  |
| COLOR_QC_APPROVED | _artifacts/reports/color_qc_v1.md | pending |  |
| COLOR_REVIEW_APPROVED | _artifacts/reports/color_review_v1.md | pending |  |
| EXEC_PLAN_APPROVED | exec_plan.json | pending |  |

## Stage approvals
- SOURCE_SCRIPT_APPROVED: 人工确认剧本文本
- SCRIPT_BREAKDOWN_APPROVED: 人工确认 `script_breakdown_v1.yaml`
- STAGE_C_DECISION_APPROVED: 人工确认方向性/制片决策
- CINEMATIC_INTENT_APPROVED: 人工确认 `_artifacts/inputs/2-1_cinematic_intent_v1.yaml`
- SHOT_MAP_SRT_XML_APPROVED: 人工确认 `_artifacts/editing_bridge/shot_map_v1.srt` 与 `timeline_plan_v1.xml`
- LAYOUT_FREEZE_APPROVED: 人工确认 `2-2_layout_freeze.yaml`
- LAYOUT_REVIEW_APPROVED: 人工确认 `_artifacts/reports/layout_review_v1.md`
- LOOKDEV_PROMPTS_APPROVED: 人工确认 `_artifacts/prompt_packs/branch_lookdev_shot_prompt_pack_v1.yaml`
- LOOKDEV_REVIEW_APPROVED: 人工确认 `_artifacts/reports/lookdev_review_v1.md`
- AUDIO_PLAN_APPROVED: 人工确认 `_artifacts/audio_plan_v1.yaml`
- AUDIO_PROMPTS_APPROVED: 人工确认所有音频 prompt pack
- AUDIO_REVIEW_APPROVED: 人工确认 `_artifacts/reports/audio_review_v1.md`
- COLOR_QC_APPROVED: 人工确认 `_artifacts/reports/color_qc_v1.md`（机器量化 QC）
- COLOR_REVIEW_APPROVED: 人工确认 `_artifacts/reports/color_review_v1.md`，确认是否允许最终交付
- EXEC_PLAN_APPROVED: 人工确认执行计划输出

- 音频审批与视觉审批互不阻塞，均需按照 stop→go→stop 的节奏完成；而调色阶段则主要由机器做 QC 判断、人类负责盖章同意/拒绝最终交付。
