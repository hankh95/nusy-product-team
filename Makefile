SHELL := /bin/bash

.PHONY: lint lint-md lint-ttl lint-changed test test-cov test-smoke build deploy deploy-dev deploy-staging deploy-prod clean docker-build docker-run docker-stop help

# Development
help: ## Show this help message
	@echo "Santiago Development Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

lint: lint-md lint-ttl ## Run all linters
	@echo "All linters passed."

lint-md: ## Lint markdown files
	@bash tools/lint_markdown.sh

lint-ttl: ## Lint turtle files
	@python3 tools/lint_ttl.py

lint-changed: ## Lint only changed markdown files
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

test: ## Run all tests
	pytest tests/ -v

test-cov: ## Run tests with coverage
	pytest --cov=santiago_core --cov=nusy_pm_core --cov=nusy_orchestrator \
		   --cov-report=term-missing --cov-report=html --cov-fail-under=80 \
		   -v tests/

test-smoke: ## Run smoke tests
	python smoke_test.py

build: ## Build the application
	@echo "Building Santiago..."
	pip install -e .
	@echo "Build complete."

# Deployment
deploy-dev: ## Deploy to development environment
	./scripts/deploy.sh development

deploy-staging: ## Deploy to staging environment
	./scripts/deploy.sh staging

deploy-prod: ## Deploy to production environment
	./scripts/deploy.sh production

# Docker
docker-build: ## Build Docker image
	docker build -t santiago:latest .

docker-run: ## Run with Docker Compose
	docker-compose up -d

docker-stop: ## Stop Docker containers
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

# Cleanup
clean: ## Clean up build artifacts and caches
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name ".coverage" -delete
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/

# CI/CD simulation
ci: lint test-cov test-smoke ## Run full CI pipeline locally
	@echo "CI pipeline completed successfully!"

# Development server
serve: ## Start development server
	python -m santiago_core.api

serve-reload: ## Start development server with auto-reload
	NUSY_ENV=development python -m santiago_core.api
