# Sanity Check After Refactor

- Running `python3 10_codex/tools/preflight.py` on the refactored template completes successfully and regenerates `00_human/INBOX.md` as the pending-gate table shown in the instructions. The gate table now mirrors `00_human/APPROVALS.md` and includes only keys whose status is `pending`.
- If the core driver (`30_project/inputs/script/source_script.md`) is missing, running `python3 10_codex/tools/preflight.py` exits with the message `缺失 30_project/inputs/script/source_script.md...` and returns exit code 1, so a fresh template copy stops before creating downstream artifacts when no script is provided.
- With the inputs populated again, running preflight restores the INBOX gate table, confirming that a clean project defaults to STOP at the first pending gate and clearly reports which approval is next.
