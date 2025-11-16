SHELL := /bin/bash

.PHONY: lint lint-md lint-ttl lint-changed

lint: lint-md lint-ttl
	@echo "All linters passed."

lint-md:
	@bash tools/lint_markdown.sh

lint-ttl:
	@python3 tools/lint_ttl.py

# Lint only changed Markdown files.
# Preference order: staged changes -> last commit range (HEAD~1..HEAD)
lint-changed:
	@set -euo pipefail; \
	files=$(git diff --name-only --cached -- '**/*.md'); \
	if [[ -z "$$files" ]]; then \
	  files=$(git diff --name-only HEAD~1..HEAD -- '**/*.md' || true); \
	fi; \
	if [[ -z "$$files" ]]; then \
	  echo "No changed Markdown files."; \
	  exit 0; \
	fi; \
	echo "Linting changed Markdown files:"; echo "$$files" | sed 's/^/  - /'; \
	if npx --yes --quiet markdownlint-cli2 --version >/dev/null 2>&1; then \
	  npx --yes markdownlint-cli2 $$files; \
	else \
	  npx --yes markdownlint $$files; \
	fi
