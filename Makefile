.PHONY: smoke plan exec-plan
smoke:
	$(MAKE) -C 10_codex smoke

plan:
	$(MAKE) -C 10_codex plan

exec-plan:
	$(MAKE) -C 10_codex exec-plan
