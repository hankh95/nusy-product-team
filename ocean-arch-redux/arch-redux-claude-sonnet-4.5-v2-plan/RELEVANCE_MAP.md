# Relevance Map — 2025-11-16

**Metadata**
Model Name: Claude Sonnet 4.5
Model Version: claude-sonnet-4.5-20250514
Date: 2025-11-16
Repo Commit SHA: 5bfcc00
Run ID: arch-redux-claude-sonnet-4.5-2025-11-16

## Relevant

- `santiago_core/` — Active agent framework implementation with PM, Architect, Developer roles; requires migration to MCP services but represents core runtime logic
- `santiago_core/agents/` — Current agent implementations that will be refactored into MCP services
- `santiago_core/services/knowledge_graph.py` — Active KG service requiring refactoring to add queuing, provenance, and validation layers
- `santiago_core/core/agent_framework.py` — Base agent class with ethical oversight; will remain as foundation for MCP services
- `DEVELOPMENT_PLAN.md` — Strategic roadmap defining phased milestones, hypotheses, and KG commitments; directly informs migration priorities
- `DEVELOPMENT_PRACTICES.md` — Core principles (TDD/BDD, KG as source of truth) that must be encoded in `knowledge/shared/working-agreements.md`
- `ocean-research/` — Target-state truth defining DGX architecture, Manolin cluster design, fake-team patterns, and concurrency test plans
- `ocean-research/nusy_manolin_architecture.md` — Canonical architecture specification for MCP-based Santiago team on DGX Spark
- `ocean-research/building-on-DGX/dgx_spark_nusy_report.md` — Hardware and storage requirements for 10-Santiago team deployment
- `ocean-research/nusy_manolin_multi_agent_test_plans.md` — Concurrency test scenarios and SLO definitions essential for orchestrator design
- `ocean-research/features-capabilities-for-shared-memory-and-evolution.md` — Detailed feature specifications for Santiago-PM, Santiago-Ethicist, and shared memory architecture
- `ocean-research/fake_team_pack/` — Interim deployment strategy using external LLM APIs before DGX availability
- `pyproject.toml` — Project metadata and dependency management; will require updates for new orchestrator and MCP service dependencies
- `requirements.txt` — Python dependencies; will be expanded with FastAPI, MCP libraries, concurrency testing tools
- `.github/` — CI/CD infrastructure; will need workflow updates for concurrency tests and multi-service deployment validation

## Peripheral

- `notes/` — Historical development notes; useful context but transitioning to `knowledge/shared/ships-log/` for active decision tracking
- `notes/santiago/` — Santiago-specific session notes; pattern will continue in new ships log structure
- `backlog/` — Feature and issue tracking; relevant for understanding work queue but not directly migrated into new architecture
- `experiments/` — Experimental designs and autonomous multi-agent experiments; provides learning but not part of core migration
- `config/experiment.json` — Experiment configuration; useful reference for understanding prior autonomous agent testing
- `experiment_runner.py` — Autonomous experiment execution script; demonstrates multi-agent patterns but will be superseded by MCP orchestrator
- `templates/` — Code scaffolding templates (api.py, cli.py); useful patterns but not directly integrated into migration
- `docs/` — Additional documentation; supportive but not migration-critical
- `tools/` — Development utilities; may contain helpful scripts for migration tasks
- `calibration/` — Evaluation and calibration artifacts; useful for comparing migration outcomes
- `chat-history/` — Conversational logs; historical context only

## Legacy-Duplicate

- `src/nusy_pm_core/` — ARCHIVED prototype runtime (tag `prototype-archive-2025-11-16`); superseded by new `nusy_orchestrator/` design; do not migrate
- `santiago-code/` — ARCHIVED per `DEVELOPMENT_PRACTICES.md`; historical reference only; do not modify
- `nusy_prototype/` — Early neurosymbolic prototype code and setup guides; superseded by current `santiago_core/` and future MCP architecture
- `architecture-redux-prompt.md` — Prior version of architecture prompt; superseded by `architecture-redux-prompt-v2.md`
- `santiago/` — Appears to duplicate content in `santiago_core/` or be legacy structure; verify and consolidate into `santiago_core/` or archive

## Irrelevant

- `.venv/` — Virtual environment directory; local development artifact, not tracked in version control
- `.pytest_cache/` — Test cache; temporary artifact
- `__pycache__/` — Python bytecode cache; temporary artifact
- `.vscode/` — Editor configuration; local preferences, not migration-relevant
- `.env.example` — Environment variable template; useful for setup but not architectural
- `.gitignore` — Repository configuration; standard tooling
- `.markdownlint.jsonc` — Linting configuration; standard tooling
- `Makefile` — Build automation; may need minor updates but not architecturally significant
- `neurosymbolic_prototype.py` — Single-file prototype; superseded by structured `santiago_core/`
- `nusy_query_interface.html` — UI prototype; not part of core migration
- `setup_experiment.sh` — Setup script for experiments; superseded by orchestrator-based execution
- `copilot-auto-approve-settings-guide.md` — Development workflow guide; not architectural

## GAP Analysis

**Missing `knowledge/` Directory at Repository Root**

The most critical gap is the absence of the `knowledge/` folder structure specified in `ocean-research/features-capabilities-for-shared-memory-and-evolution.md`. This folder is essential for:

- Shared team memory across agent sessions
- Working agreements and BDD practices
- Team roster and capability discovery (RDF graph)
- Ships logs for evolutionary decision tracking
- Domain-specific knowledge for each Santiago role

**Recommendation:** Milestone 1 of the migration must create this structure as the foundation for all subsequent work.

**Missing MCP Infrastructure**

No current implementation of:
- MCP service manifests (`mcp/manifests/`)
- MCP registry and discovery (`mcp/registry/`)
- MCP adapter layer (`santiago_core/services/mcp_adapter.py`)

**Recommendation:** Milestone 2 addresses this by implementing Santiago-PM and Santiago-Ethicist as the first MCP services, establishing the pattern.

**Missing Orchestrator**

The archived `src/nusy_pm_core/` was a prototype; no production-ready orchestrator exists for:
- Session management
- Ethics & Concurrency Gating
- MCP service routing
- Policy enforcement

**Recommendation:** Milestone 4 implements the new `nusy_orchestrator/` with all required capabilities.

**Missing DGX Infrastructure**

No deployment automation, runbooks, or infrastructure-as-code for DGX Spark deployment:
- Provisioning scripts
- Docker Compose orchestration
- Storage layout documentation
- Operational runbooks

**Recommendation:** Milestone 6 provides complete DGX deployment automation per `ocean-research/building-on-DGX/dgx_spark_nusy_report.md`.

**Missing Concurrency Test Harness**

While `experiment_runner.py` demonstrates autonomous agents, there is no formal test suite for:
- Session isolation validation
- Tool invocation race conditions
- Load profiles and SLO measurement

**Recommendation:** Milestone 5 implements comprehensive concurrency testing per `ocean-research/nusy_manolin_multi_agent_test_plans.md`.

## Calibration Appendix

*(This section intentionally left for post-submission calibration against other model outputs if desired)*

### References Cited

- ocean-research/nusy_manolin_architecture.md
- ocean-research/building-on-DGX/dgx_spark_nusy_report.md
- ocean-research/nusy_manolin_multi_agent_test_plans.md
- ocean-research/features-capabilities-for-shared-memory-and-evolution.md
- ocean-research/fake_team_pack/fake_team_feature_plan.md
