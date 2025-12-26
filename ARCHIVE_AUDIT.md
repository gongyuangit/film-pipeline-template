# Archive Audit

## 1. `90_archive/` tree (≤3 levels)
- `90_archive/`
  - `docs/`
    - `2_layout/`
      - `_exports/`
    - `3_lookdev/`
    - `3_prompt/`
    - `4_production/`
    - `4_render/`
    - `X_exec/`

## 2. Questions

**a) Does any runtime script read/scan `90_archive/`?**  
`rg -n "90_archive" 10_codex/tools` shows only a documentation mention in `gen_template_index.py`; no script reads or ingests archive paths. `preflight.py`, `check_inputs.py`, and other tools work off `30_project/`, `00_human/`, and `10_codex/` directories, so nothing currently scans `90_archive/`.  

**b) Does `TEMPLATE_MANIFEST` / `TEMPLATE_INDEX` include archive paths?**  
Yes. `10_codex/TEMPLATE_MANIFEST.yaml` currently lists `90_archive/docs/` plus each legacy subdirectory, so `preflight` recreates/validates them. `TEMPLATE_INDEX.md` mentions compared-to-archive rules, but its generator already focuses on `00_human/`, `10_codex/`, and `30_project/docs` only.  

**c) Could `preflight.py` / `check_inputs` treat archive files as live artifacts?**  
Because the manifest lists every `90_archive` directory, `preflight` ensures those entries exist and may surface them if their presence fluctuates. `check_inputs.py` only reads `30_project/inputs/`, so it ignores archives. However, `preflight`'s structure enforcement currently bridges the archive into the runtime pipeline, so they are not fully isolated.

## 3. Conclusion
`90_archive/` is not fully isolated: manifest entries bring it into `preflight`'s scope, so archive directories are treated like required artifacts. We need to drop them from `TEMPLATE_MANIFEST.yaml` and ensure tools ignore `90_archive`, keeping it purely archival.
