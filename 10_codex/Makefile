REPO_ROOT := ..
RUNTIME_DIR := $(REPO_ROOT)/20_runtime
SMOKE_DIR := $(RUNTIME_DIR)/smoke
SMOKE_REPORT := $(SMOKE_DIR)/smoke_report.md
PLAN_DIR := $(RUNTIME_DIR)/plan
PLAN_REPORT := $(PLAN_DIR)/shot_list.json
EXEC_DIR := $(RUNTIME_DIR)/exec
EXEC_REPORT := $(EXEC_DIR)/execution_plan.json

.PHONY: smoke plan exec-plan FORCE
smoke:
	@mkdir -p $(SMOKE_DIR)
	@{ \
		printf "Time: %s\n" "$$(date -u +"%Y-%m-%dT%H:%M:%SZ")"; \
		printf "Git revision: %s\n" "$$(git rev-parse HEAD)"; \
		printf "Root entries:\n"; \
		ls -1 $(REPO_ROOT); \
		printf "index.yaml present: %s\n" "$$( [ -f $(INDEX_FILE) ] && echo yes || echo no)"; \
	} > $(SMOKE_REPORT)

plan: $(PLAN_REPORT)

INDEX_FILE := $(REPO_ROOT)/index.yaml

$(PLAN_REPORT): tools/generate_plan.py $(INDEX_FILE) FORCE
	@mkdir -p $(PLAN_DIR)
	@python3 tools/generate_plan.py

exec-plan: $(EXEC_REPORT)

$(EXEC_REPORT): tools/generate_exec_plan.py $(PLAN_REPORT) FORCE
	@mkdir -p $(EXEC_DIR)
	@python3 tools/generate_exec_plan.py

FORCE:
