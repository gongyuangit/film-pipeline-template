SMOKE_DIR := 02_outputs/smoke
SMOKE_REPORT := $(SMOKE_DIR)/smoke_report.md
PLAN_DIR := 02_outputs/plan
PLAN_REPORT := $(PLAN_DIR)/shot_list.json
EXEC_DIR := 02_outputs/exec
EXEC_REPORT := $(EXEC_DIR)/execution_plan.json

.PHONY: smoke plan FORCE
smoke:
	@mkdir -p $(SMOKE_DIR)
	@{ \
		printf "Time: %s\n" "$$(date -u +"%Y-%m-%dT%H:%M:%SZ")"; \
		printf "Git revision: %s\n" "$$(git rev-parse HEAD)"; \
		printf "Root entries:\n"; \
		ls -1; \
		printf "index.yaml present: %s\n" "$$( [ -f index.yaml ] && echo yes || echo no)"; \
	} > $(SMOKE_REPORT)

plan: $(PLAN_REPORT)

$(PLAN_REPORT): tools/generate_plan.py index.yaml FORCE
	@mkdir -p $(PLAN_DIR)
	@python3 tools/generate_plan.py

exec-plan: $(EXEC_REPORT)

$(EXEC_REPORT): tools/generate_exec_plan.py $(PLAN_REPORT) FORCE
	@mkdir -p $(EXEC_DIR)
	@python3 tools/generate_exec_plan.py

FORCE:
