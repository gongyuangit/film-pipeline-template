.PHONY: preflight plan exec-plan check-inputs

.PHONY: docs-index docs-index-check

preflight:
	$(MAKE) -C 10_codex preflight

plan:
	$(MAKE) -C 10_codex plan

exec-plan:
	$(MAKE) -C 10_codex exec-plan

check-inputs:
	$(MAKE) -C 10_codex check-inputs

docs-index:
	python3 10_codex/tools/gen_template_index.py

docs-index-check:
	python3 10_codex/tools/gen_template_index.py --check
