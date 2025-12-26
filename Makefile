.PHONY: preflight plan exec-plan check-inputs

preflight:
	$(MAKE) -C 10_codex preflight

plan:
	$(MAKE) -C 10_codex plan

exec-plan:
	$(MAKE) -C 10_codex exec-plan

check-inputs:
	$(MAKE) -C 10_codex check-inputs
