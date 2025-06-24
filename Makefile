.PHONY: precommit

precommit: ## Run basic checks
	@scripts/verify_makefile_tabs.sh
	@scripts/check_python.sh
