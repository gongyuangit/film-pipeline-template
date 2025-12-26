# Runtime Cache Skeleton

`20_runtime/` is a cache area for runtime artifacts such as `plan/shot_list.json` and `exec/execution_plan.json`. These files are generated at runtime and should never be committed. Treat this directory as writable cache: it may be cleared at any time and is rehydrated automatically.

Today the template only ships the empty skeleton (`plan/`, `exec/`, `tests/`, `final/`) with `.gitkeep` placeholders; real artifacts are produced during execution and must stay out of source control.
