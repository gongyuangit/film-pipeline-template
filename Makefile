SMOKE_DIR := 02_outputs/smoke
SMOKE_REPORT := $(SMOKE_DIR)/smoke_report.md

.PHONY: smoke
smoke:
	@mkdir -p $(SMOKE_DIR)
	@{ \
		printf "Time: %s\n" "$$(date -u +"%Y-%m-%dT%H:%M:%SZ")"; \
		printf "Git revision: %s\n" "$$(git rev-parse HEAD)"; \
		printf "Root entries:\n"; \
		ls -1; \
		printf "index.yaml present: %s\n" "$$( [ -f index.yaml ] && echo yes || echo no)"; \
	} > $(SMOKE_REPORT)
