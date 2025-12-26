.PHONY: plan exec-plan check-inputs

plan:
	$(MAKE) -C 10_codex plan

exec-plan:
	$(MAKE) -C 10_codex exec-plan

check-inputs:
	$(MAKE) -C 10_codex check-inputs
