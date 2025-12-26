# Template Migration Plan

## 1. Target Directory Structure (per workbench)
- **Layout (`30_project/docs/2_layout/`)**
  - `_artifacts/`
    - `inputs/` (shot-map metadata, cinematic intent samples)
    - `prompt_packs/` (segment/shot/blender/lookdev prompt packs)
    - `reports/` (layout review, lookdev review, QC reminders)
    - `editing_bridge/` (shot_map SRT/XML, rename/manifest/notes)
    - `exports/` (layout deliverable markers and metadata)
  - `CURRENT.yaml` (approved artifact pointer)
- **Audio (`30_project/docs/2_audio/`)** mirrors layout with `prompt_packs/`, `reports/`, `editing_bridge/`, `exports/`, `inputs/`, plus placeholders for dialog/sfx/music prompts.
- **Color (`30_project/docs/5_color/`)** retains `inputs/`, `reports/`, `exports/`, `editing_bridge/` and adds a `docs/` level README describing QC-only work.

Each `_artifacts/` directory must expose `inputs/`, `reports/`, and `exports/` (even if empty or containing placeholders) so preflight can enforce consistency.

## 2. Migration Mapping (old -> new)
- `30_project/docs/2_layout/_artifacts/branch1_segment_prompt_pack_v1.yaml`  → `_artifacts/prompt_packs/branch1_segment_prompt_pack_v1.yaml` (and analogous moves for branch2/branch3/branch_lookdev).
- `_artifacts/2-1_cinematic_intent_v1.yaml` → `_artifacts/inputs/2-1_cinematic_intent_v1.yaml` so cinematic intent sleeps among input metadata, not root-level artifacts.
- `_artifacts/reports/layout_review_v1.md` & `reports/lookdev_review_v1.md` stay in `reports/` but we must ensure README references new path.
- `_artifacts/editing_bridge/*` remain but will now be referenced via new `inputs`/`editing_bridge` combos in docs and pipeline.
- Introduce `_artifacts/exports/layout_markers_v1.yaml` to capture layout deliverable markers (new file).
- `00_human/INBOX.md` will shift from descriptive table to strict gate table that mirrors `APPROVALS.md` keys (`Stage, Gate Key, Status, Action, Artifact`). Preflight will now refresh this table automatically.

## 3. Required Sample Files (minimal content)
Each sample is ~5-20 lines to stay light.
1. `30_project/docs/2_layout/_artifacts/inputs/2-1_cinematic_intent_v1.yaml` with `meta` & `segments` list to show structure (used as template for future variants).
2. `30_project/docs/2_layout/_artifacts/prompt_packs/branch1_segment_prompt_pack_v1.yaml` showing `globals` + `shots[]` + `segments[]` sections, plus `notes` referencing `negative_effective = globals.negative + shots[].negative`.
3. `30_project/docs/3_lookdev/_artifacts/prompt_packs/branch_lookdev_shot_prompt_pack_v1.yaml` with lookdev-specific guidance.
4. `30_project/docs/2_audio/_artifacts/prompt_packs/dialogue_vo_prompt_pack_v1.yaml` as already existing template (will stay and get referenced in manifest/README).
5. `30_project/docs/5_color/_artifacts/reports/color_qc_v1.md` and `color_review_v1.md` with the metrics/checklist stub already present; ensure references mention final deliverable gating.
6. `30_project/docs/2_layout/_artifacts/exports/layout_markers_v1.yaml` as new placeholder enumerating shot markers for final exports.
7. `00_human/INBOX.md` gate table template with headers: `| Stage | Gate Key | Status | Action | Artifact |` plus pending rows; preflight will rewrite it on each run.

## 4. INBOX Gate Table Overhaul Plan
1. Replace `00_human/INBOX.md` with a generated table listing only pending approvals present in `APPROVALS.md`. Columns: Stage, Gate Key, Status, Action, Artifact. Actions describe what humans must do (e.g., "Review shot map SRT + timeline markups").
2. Preflight will parse `APPROVALS.md` to update `INBOX.md` before each run; once an approval is marked `approved`, its row disappears, ensuring the file shows only active gates.
3. Each gate row/approval key in the pipeline (SOURCE_SCRIPT_APPROVED, ..., COLOR_REVIEW_APPROVED) will have a corresponding `Action` description tied to the artifact paths defined in `PIPELINE_STAGES.yaml`.
4. This table will be the *sole* source of truth for pending work; human notes must go elsewhere (INBOX becomes gate tracker, while human-specific commentary stays in `00_human/PRODUCTION.md`, `DECISIONS.md`, or other docs).

Once the migration mapping is executed, the pipeline, manifest, preflight, and human docs will consistently reference the new artifact locations and gating table, fully aligning with the stop→go→stop philosophy.
