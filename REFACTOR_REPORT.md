# Template Refactor Report

## 1. Directory Tree Summary
- Top-level: `00_human/`, `10_codex/`, `20_runtime/`, `30_project/` plus hidden git metadata.
- `20_runtime/` contains parallel submodules (`layout/`, `exec/`, `post/`, `lookdev/`, `shots/`, `tests/`, `plan/`) but only `exec/` is tied to a named pipeline stage; the rest are unused placeholders today.
- `30_project/` splits into `inputs/`, `work/`, `docs/`, `archive/`. Within `docs/` we now host `0-source`, `1_story`, `2_layout`, `2_audio`, `5_color` with bespoke workbench structures.

## 2. Issues to Address
- **Duplicate/Orphan directories:** `20_runtime/post`, `20_runtime/shots`, `20_runtime/tests` and `30_project/work` are not referenced by any pipeline stage, docs, or manifest entry. They look like leftovers from earlier iterations.
- **Old paths / manifest drift:** `20_runtime/exec/execution_plan.json` is the Stage F product but it is *not declared* in `10_codex/TEMPLATE_MANIFEST.yaml`, so preflight cannot pre-create it; no other manifest entry points to `20_runtime/exec/execution_plan.json` either. Conversely, every manifest entry presently exists on disk (no missing entries), but there are several essential artifacts (e.g., `20_runtime/exec/execution_plan.json`, `2_audio/_artifacts/prompt_packs/dialogue_vo_prompt_pack_v1.yaml`, `5_color/_artifacts/reports/color_qc_v1.md`) that should be explicitly noted as required templates.
- **Approval/inbox mismatch:** `00_human/INBOX.md` is currently a generic to-do list that includes stage rows but also manual notes; it does not reflect the formal gate table implied by `00_human/APPROVALS.md`, and there is no clear mapping from pending rows to `Approval Key`s.

## 3. Stage Consistency Check
| Stage | `PIPELINE_STAGES.yaml` product | Preflight gate row (approx) | Human docs reference | Actual file exists? |
|---|---|---|---|---|
| Stage D | `_artifacts/2-1_cinematic_intent_v1.yaml` | yes (`STAGE_D_ROW`) | README + APPROVALS | yes
| Stage P1.5 | `_artifacts/editing_bridge/shot_map_v1.srt + timeline_plan_v1.xml` | yes (`STAGE_P1_5_ROW`) | APPROVALS | yes
| Stage E | `2-2_layout_freeze.yaml` | *no dedicated row* | README/APPROVALS mention freeze | yes (file exists) but not referenced in gate table
| Stage LR | `_artifacts/reports/layout_review_v1.md` | yes | README + APPROVALS | yes
| Stage K/K_R | lookdev artifacts & review | yes | README + APPROVALS | yes
| Stage F | `20_runtime/exec/execution_plan.json` | *missing in view table* | APPROVALS lists key | exists only as placeholder under runtime (no template) 
| Stages A1-A3 | audio plan/prompt/review | yes | README + APPROVALS | yes
| Stages G1-G2 | color QC/review | yes | README + APPROVALS | yes

**Observations:** Stage E and Stage F lack explicit INBOX gate rows despite being non-trivial gates, and `execution_plan.json` is not treated as a template artifact. The INBOX/APPROVALS split is therefore inconsistent with the stop→go→stop philosophy and will be tightened in the refactor.
