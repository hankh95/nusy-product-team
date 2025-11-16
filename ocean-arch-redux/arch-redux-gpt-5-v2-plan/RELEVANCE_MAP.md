# Repository Relevance Map — GPT-5 v2 (2025-11-16)

This map classifies folders/files by their relevance to the Architecture Redux task. Categories: Relevant (core to planning/execution), Peripheral (helpful context, not central), Legacy/Duplicate (to be consolidated), Irrelevant (infrastructure/noise).

## Top-Level Directories

| Path | Category | Notes |
| --- | --- | --- |
| `src/nusy_pm_core/` | Relevant | Current FastAPI/CLI PM core; candidate to evolve into NuSy Orchestrator. |
| `santiago_core/` | Relevant | Multi-agent prototype (agents, framework, knowledge); source for MCP service extraction. |
| `ocean-research/` | Relevant | Target-state references (DGX/Manolin, fake-team, concurrency plans, capabilities). |
| `ocean-arch-redux/` | Relevant | Prior plan runs; do not read for bias, but keep our outputs here (`arch-redux-gpt-5-v2-plan`). |
| `notes/` | Relevant | Human-readable logs and KG TTL (`notes/kg.ttl`), used for migration to root `knowledge/`. |
| `santiago-pm/` | Relevant | PM-specific artifacts (ships-logs, cargo-manifests, passages, quality-assessments); important inputs to consolidation. |
| `templates/` | Peripheral | Simple API/CLI scaffolds; useful_examples. |
| `experiments/` | Peripheral | Planning docs; keep for context only. |
| `nusy_prototype/` | Peripheral | Separate clinical prototype; not in scope for Manolin unless explicitly integrated later. |
| `santiago/` | Peripheral | Older Santiago docs; keep until consolidated. |
| `chat-history/` | Peripheral | Meta logs of AI sessions; not needed for architecture plan. |
| `.github/` | Peripheral | Agent instruction docs; informative but not execution code. |
| `config/` | Peripheral | Experiment config; limited impact. |
| `.git/`, `.venv/`, `.pytest_cache/`, `.vscode/` | Irrelevant | Tooling/build caches and SCM internals. |

## Key Files (Selected)

| File | Category | Notes |
| --- | --- | --- |
| `architecture-redux-prompt.md` | Relevant | The planning prompt we follow. |
| `DEVELOPMENT_PLAN.md` | Relevant | Phased goals; align with migration. |
| `DEVELOPMENT_PRACTICES.md` | Relevant | Working agreements to seed shared memory. |
| `src/nusy_pm_core/api.py` | Relevant | Current service surface; informs orchestrator extraction. |
| `src/nusy_pm_core/cli.py` | Relevant | CLI entry points; extend for evolution cycles. |
| `src/nusy_pm_core/knowledge/graph.py` | Relevant | KG access pattern; migrate to root `knowledge/`. |
| `santiago_core/core/agent_framework.py` | Relevant | Agent base + ethics stub; guide MCP boundary. |
| `santiago_core/agents/santiago_pm.py` | Relevant | PM behavior; basis for a PM MCP service. |
| `ocean-research/building-on-DGX/dgx_spark_nusy_report.md` | Relevant | DGX target. |
| `ocean-research/building-on-DGX/nusy_manolin_provisioning_automation.md` | Relevant | Provisioning automation. |
| `ocean-research/nusy_manolin_architecture.md` | Relevant | Overall target architecture. |
| `ocean-research/nusy_manolin_multi_agent_test_plans.md` | Relevant | Concurrency and ethics gating. |
| `ocean-research/features-capabilities-for-shared-memory-and-evolution.md` | Relevant | Shared memory, role taxonomy, evolution cycles. |
| `requirements.txt`, `pyproject.toml` | Peripheral | Env setup; unchanged in plan-only phase. |

## Legacy / Duplicate Areas

| Path | Why Legacy/Duplicate | Planned Action |
| --- | --- | --- |
| `santiago-code/` | Older Santiago-specific code, superseded by `santiago_core/`. | Freeze; migrate any still-useful bits into agents or orchestrator; deprecate afterward. |
| `notes/kg.ttl` and `santiago_core/knowledge/santiago_kg.ttl` | Multiple graphs across trees. | Consolidate into `knowledge/domains/core/graph.ttl`. |
| `santiago/` vs `santiago_core/` | Naming drift; documentation split. | Keep `santiago_core/` as canonical; link docs; retire `santiago/` after merge. |

## Out of Scope / Irrelevant for Planning

- `.git/**`, caches under `.pytest_cache/**`, editor configs under `.vscode/**`.
- Binary/object files under `.git/objects/**`.
- Temporary research scratchpads in `nusy_prototype/tmp/**` (unless explicitly adopted).

## Summary

- Core execution focus: `src/nusy_pm_core`, `santiago_core`, `ocean-research`, `notes`, `santiago-pm`.
- Immediate gaps: no root `knowledge/` tree; no MCP service boundaries; missing roster TTL and ships-log at root; DGX automation not integrated into repo scripts.
