SHELL := /bin/bash

.PHONY: lint lint-md lint-ttl

lint: lint-md lint-ttl
	@echo "All linters passed."

lint-md:
	@bash tools/lint_markdown.sh

lint-ttl:
	@python3 tools/lint_ttl.py
