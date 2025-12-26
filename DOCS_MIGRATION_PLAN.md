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

## 2. Migration mappings (old -> archive/new)
- `30_project/docs/3_lookdev/` → `90_archive/docs/3_lookdev/` (legacy lookdev docs; update meta references from `00_docs/3_lookdev/...` to `90_archive/docs/3_lookdev/...`).
- `30_project/docs/3_prompt/` → `90_archive/docs/3_prompt/`.
- `30_project/docs/4_production/` → `90_archive/docs/4_production/`.
- `30_project/docs/4_render/` → `90_archive/docs/4_render/`.
- `30_project/docs/X_exec/` → `90_archive/docs/X_exec/` (shared exec inputs become archival reference; adjust meta if needed).
- `30_project/docs/2_layout/_exports/` → `90_archive/docs/2_layout/_exports/` (old export folder replaced by `_artifacts/exports/`).

## 3. Mandatory template files to preseed
- `30_project/inputs/script/source_script.md` (Stage S authority input; ensure listed in TEMPLATE_MANIFEST).
- `30_project/docs/2_layout/2-2_layout_freeze.yaml` (layout freeze product; add to manifest).
- `_artifacts` placeholders for each active workbench:
  - Layout prompt packs and exports/inputs/reports (already minimal but confirm).
  - Audio plan, prompt packs, reports, inputs/exports placeholders.
  - Color QC/Review reports + editing_bridge placeholders.
- `90_archive/docs_migration_log.md` (new log recording each moved directory/path).

## 4. Meta/reference updates
- Update `index.yaml`, `meta/project_config.yaml`, `meta/master_index.yaml`, `meta/state_machine.yaml`, and `meta/ingest_bridge.yaml` to point to the archived paths for legacy docs (or drop those entries) so there are no dangling references to missing directories.
