.PHONY: precommit align dot ranks svg diagram

precommit: ## Run basic checks
	@scripts/verify_makefile_tabs.sh
	@scripts/check_python.sh


align: ## Fix task metadata in Fibery
	@python3 src/align.py

dot: tasks.dot ## Export tasks as Graphviz dot file

tasks.dot:
	@python3 src/workflow.py | unflatten -l 2 -f -c 5 > $@

ranks: ## Patch Fibery task ranks
	@python3 src/patch_ranks.py

svg: tasks.svg ## Render tasks.svg diagram

tasks.svg: tasks.dot
	@cp -f $< tasks_bck.dot
	@cat $< | dot -Tsvg -v > tasks_new.svg
	@mv tasks_new.svg $@

diagram: ranks svg ## Update ranks and render tasks.svg
