# Docs Migration Plan (align 30_project/docs with pipeline)

## 1. Target 30_project/docs structure (final)
- `0-source/` – raw structured fragments + parsed outputs; already aligned with Source Synthesis.
- `1_story/` – contains `script_breakdown_v1.yaml` (authority for Stage B).
- `2_layout/` – the layout workbench comprises:
  - `_artifacts/inputs/2-1_cinematic_intent_v1.yaml` (cinematic intent template)
  - `_artifacts/prompt_packs/` (segment, shot, blender, lookdev prompt pack templates + README)
  - `_artifacts/reports/` (layout and lookdev reviews)
  - `_artifacts/editing_bridge/` (shot map SRT/XML, rename/asset manifests)
  - `_artifacts/exports/` (layout marker plan)
  - `2-2_layout_freeze.yaml` (layout freeze product)
  - `CURRENT.yaml` points to approved cinematic intent.
- `2_audio/` – audio workbench with `_artifacts/inputs/`, `_artifacts/prompt_packs/`, `_artifacts/reports/`, `_artifacts/exports/`, `_artifacts/editing_bridge/`.
- `5_color/` – color workbench with `_artifacts/inputs/`, `_artifacts/reports/`, `_artifacts/exports/`, `_artifacts/editing_bridge/`.

## 2. Migration mappings (legacy)
- Legacy `3_lookdev/`, `3_prompt/`, `4_production/`, `4_render/`, `X_exec/`, and `_exports/` directories no longer exist; those archives were hard-deleted as part of this cleanup and are no longer referenced anywhere.

## 3. Mandatory template files to preseed
- `30_project/inputs/script/source_script.md` (Stage S authority input; ensure listed in TEMPLATE_MANIFEST).
- `30_project/docs/2_layout/2-2_layout_freeze.yaml` (layout freeze product; add to manifest).
- `_artifacts` placeholders for each active workbench:
  - Layout prompt packs and exports/inputs/reports (already minimal but confirm).
  - Audio plan, prompt packs, reports, inputs/exports placeholders.
  - Color QC/Review reports + editing_bridge placeholders.
- The migration log documents every moved directory/path.

## 4. Meta/reference updates
- Update `index.yaml`, `meta/project_config.yaml`, `meta/master_index.yaml`, `meta/state_machine.yaml`, and `meta/ingest_bridge.yaml` to point to the archived paths for legacy docs (or drop those entries) so there are no dangling references to missing directories.
