# Root Artifact Triage Report

## Overview

This report analyzes root-level artifacts in the repository and proposes target homes based on the migration plan principles:

- **Two-namespace model**: `domain/*` vs `self-improvement/*`
- **Canonical scaffold**: `santiago-pm/` as the self-improvement scaffold
- **Production vs experimental**: Clear separation of concerns

## Triage Categories

### Keep in Root (Infrastructure)

These files should remain at root level as they are repository infrastructure:

- `.DS_Store` - macOS system file (ignore)
- `.continue/` - Continue.dev configuration
- `.env` - Environment variables (production)
- `.env.example` - Environment template
- `.git/` - Git repository
- `.github/` - GitHub configuration
- `.gitignore` - Git ignore rules
- `.markdownlint.jsonc` - Markdown linting config
- `.pytest_cache/` - Test cache (temporary)
- `.venv/` - Virtual environment (temporary)
- `.vscode/` - VS Code workspace settings
- `Dockerfile` - Container definition
- `Makefile` - Build automation
- `README.md` - Repository documentation
- `docker-compose.yml` - Container orchestration
- `nginx.conf` - Web server config
- `pyproject.toml` - Python project config
- `requirements.txt` - Python dependencies

### Move to `domain/` (Production Domain Code)

Production code that implements the domain functionality:

- `API_CLIENT_IMPLEMENTATION.md` - API documentation
- `config/` - Configuration files
- `examples/` - Usage examples
- `features/` - Feature definitions
- `knowledge/` - Domain knowledge
- `knowledge-graph/` - Knowledge graph implementation
- `models/` - Domain models
- `nusy_orchestrator/` - Main orchestrator
- `roles/` - Role definitions
- `santiago_core/` - Core domain logic
- `scripts/` - Utility scripts
- `src/` - Source code
- `templates/` - Code templates
- `tools/` - Development tools

### Move to `self-improvement/` (Self-Improvement System)

Code that implements the self-improvement capabilities:

- `santiago-dev/` - Development self-improvement tools
- `santiago-pm/` - Product management scaffold (canonical)
- `kanban-boards.md` - Kanban documentation
- `kanban_regenerator.py` - Kanban regeneration logic
- `load_pm_knowledge.py` - PM knowledge loading

### Archive to `_archive/` (Historical/Deprecated)

Files that should be archived for historical reference:

- `ARCHITECTURE.md` - Superseded by docs-arch-redux-3/
- `ASSUMPTIONS_AND_RISKS.md` - Historical assumptions
- `COMMIT_MESSAGE.txt` - Temporary commit message
- `CONTRIBUTING.md` - May be superseded
- `DEVELOPMENT_PLAN.md` - Historical plan
- `Epub-books-feature-memory.md` - Feature memory
- `NuSy–Santiago-Architecture-Discussion-Grok-4-1.md` - Historical discussion
- `SANTIAGO-ARCHITECTURE-SCENARIOS.md` - Historical scenarios
- `analyze_features.py` - Analysis script
- `ci_cd_test.py` - Test script
- `demo_*.py` - Demo scripts (move to examples/ or archive)
- `dgx-readiness-priorities.json` - Historical priorities
- `dgx_readiness_prioritization.py` - Prioritization script
- `exp032_venv/` - Experimental environment
- `factory-activity-log.md` - Activity log
- `notebooks/` - Jupyter notebooks (move to examples/ or archive)
- `research-logs/` - Research logs
- `save-chat-log.py` - Chat logging script
- `smoke_test.py` - Smoke test
- `test_workspace/` - Test workspace
- `tests/` - Test files (should be in appropriate domain/self-improvement locations)
- `venv/` - Virtual environment
- `zarchive/` - Already archived

### Move to `docs/` (Documentation)

Documentation files that should be organized:

- `docs/` - Existing docs
- `docs-arch-redux-3/` - Current architecture docs
- `GLOSSARY.md` - Should be in docs/

## Implementation Plan

### Phase 1: Non-destructive Moves

1. Create `domain/` and `self-improvement/` directories
2. Move production code to `domain/`
3. Move self-improvement code to `self-improvement/`
4. Update imports and references

### Phase 2: Documentation Consolidation

1. Move `GLOSSARY.md` to `docs/`
2. Consolidate architecture docs in `docs/architecture/`
3. Update all references

### Phase 3: Archive Cleanup

1. Move historical files to `_archive/`
2. Update any remaining references
3. Clean up temporary files

## Questions for Captain Review

1. Should `santiago-pm/` remain as the canonical scaffold, or should it be moved under `self-improvement/`?
2. How should demo scripts be handled - examples/ or archive?
3. Should `tests/` be distributed to appropriate domain/self-improvement locations?
4. What should be the final structure for documentation?
