REPO_ROOT := ..
RUNTIME_DIR := $(REPO_ROOT)/20_runtime
PLAN_DIR := $(RUNTIME_DIR)/plan
PLAN_REPORT := $(PLAN_DIR)/shot_list.json
EXEC_DIR := $(RUNTIME_DIR)/exec
EXEC_REPORT := $(EXEC_DIR)/execution_plan.json

.PHONY: preflight plan exec-plan check-inputs FORCE

preflight:
	@python3 tools/preflight.py

check-inputs: preflight
	@python3 tools/check_inputs.py

plan: preflight $(PLAN_REPORT)

INDEX_FILE := $(REPO_ROOT)/index.yaml

$(PLAN_REPORT): tools/generate_plan.py $(INDEX_FILE) FORCE
	@mkdir -p $(PLAN_DIR)
	@python3 tools/generate_plan.py

exec-plan: preflight $(EXEC_REPORT)

$(EXEC_REPORT): tools/generate_exec_plan.py $(PLAN_REPORT) FORCE
	@mkdir -p $(EXEC_DIR)
	@python3 tools/generate_exec_plan.py

FORCE:
