# 30_project/docs Structure Audit

## 1. Current docs tree (depth 3)

- `30_project/docs`
  - `0-source`
    - `parsed`
    - `raw`
      - `structured`
  - `1_story`
  - `2_audio`
    - `_artifacts`
      - `editing_bridge`
      - `exports`
      - `inputs`
      - `prompt_packs`
      - `reports`
  - `2_layout`
    - `_artifacts`
      - `editing_bridge`
      - `exports`
      - `inputs`
      - `prompt_packs`
      - `reports`
    - `_exports`
  - `3_lookdev`
  - `3_prompt`
  - `4_production`
  - `4_render`
  - `5_color`
    - `_artifacts`
      - `editing_bridge`
      - `exports`
      - `inputs`
      - `reports`
  - `meta`
  - `X_exec`

## 2. Pipeline stage products

| Stage | Product(s) | Exists | In manifest? |
| --- | --- | --- | --- |
| Stage S | `30_project/inputs/script/source_script.md` | ✅ | ❌ |
| Stage B | `30_project/docs/1_story/script_breakdown_v1.yaml` | ✅ | ✅ |
| Stage C | `00_human/DECISIONS.md` | ✅ | ✅ |
| Stage A1 | `30_project/docs/2_audio/_artifacts/audio_plan_v1.yaml` | ✅ | ✅ |
| Stage A2 | Throw of three prompt packs | ✅ | ✅ |
| Stage A3 | `30_project/docs/2_audio/_artifacts/reports/audio_review_v1.md` | ✅ | ✅ |
| Stage D | `30_project/docs/2_layout/_artifacts/inputs/2-1_cinematic_intent_v1.yaml` | ✅ | ✅ |
| Stage P1.5 | `30_project/docs/2_layout/_artifacts/editing_bridge/shot_map_v1.srt` and `timeline_plan_v1.xml` | ✅ | ✅ |
| Stage E | `30_project/docs/2_layout/2-2_layout_freeze.yaml` | ✅ | ❌ |
| Stage LR | `30_project/docs/2_layout/_artifacts/reports/layout_review_v1.md` | ✅ | ✅ |
| Stage K | `_artifacts/prompt_packs/branch_lookdev_shot_prompt_pack_v1.yaml` | ✅ | ✅ |
| Stage K_R | `_artifacts/reports/lookdev_review_v1.md` | ✅ | ✅ |
| Stage F | `20_runtime/exec/execution_plan.json` | ✅ | ✅ |
| Stage G1 | `_artifacts/reports/color_qc_v1.md` | ✅ | ✅ |
| Stage G2 | `_artifacts/reports/color_review_v1.md` | ✅ | ✅ |

**Notes:** Stage S (source script) and Stage E (layout freeze) artifacts are not currently listed in `10_codex/TEMPLATE_MANIFEST.yaml`, meaning preflight cannot auto-create them. All other product paths exist and are tracked.

## 3. Docs vs pipeline alignment

- **Missing pipeline directories/files in docs:** None beyond those stage products above (all exist).  
- **Docs directories not referenced by pipeline:** `3_lookdev`, `3_prompt`, `4_production`, `4_render`, `X_exec` appear only in meta/index references; they do not serve any current stage products and look like legacy workbenches.  
- **Duplicate or migration leftovers:** `30_project/docs/2_layout/_exports` is redundant now that `_artifacts/exports` exists; it should be archived. `30_project/docs/meta` still references `00_docs/3_lookdev`/`X_exec`, so those paths will break when the directories are moved unless metadata is updated.
- **Manifest coverage gaps:** Stage S and Stage E artifacts are missing from the manifest; need to add them so preflight can enforce pre-creation.

## 4. Actionable summary

- Add `30_project/inputs/script/source_script.md` and `30_project/docs/2_layout/2-2_layout_freeze.yaml` to `TEMPLATE_MANIFEST.yaml`.
- Archive unused directories (`3_lookdev`, `3_prompt`, `4_production`, `4_render`, `_exports`, `X_exec`) under `90_archive/` and update meta/index references to point at the archived copies.
- Ensure `_artifacts/` for each active stage contains the required `inputs`, `prompt_packs`, `reports`, `exports` subfolders with placeholder content so the manifest/preflight can rely on them.
