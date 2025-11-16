# Migration Steps — GPT-5.1-Codex

## Milestone 1 — Stand Up Shared Memory & Knowledge Contracts

**Goals:**

- Establish repo-level `knowledge/` layout, ships logs, and roster schema required by Santiago-PM & Ethicist.
- Decouple KG persistence from `santiago_core/` so all agents/humans read the same artifacts.

**Scope / Affected Paths:** `knowledge/`, `santiago_core/services/knowledge_graph.py`, `notes/`, `santiago-pm/ships-logs/`, `DEVELOPMENT_PRACTICES.md`.

**Tasks:**

- [ ] Create `knowledge/shared/`, `knowledge/domains/pm/`, `knowledge/domains/ethics/`, `knowledge/shared/ships-log/`, `knowledge/shared/evolution-cycles/` with starter templates from `ocean-research/features-capabilities-for-shared-memory-and-evolution.md`.
- [ ] Move `santiago_core/knowledge/` TTL outputs to `knowledge/shared/kg/` and update `SantiagoKnowledgeGraph` path/constructor accordingly.
- [ ] Author initial `knowledge/shared/working-agreements.md`, `knowledge/shared/bdd-practices.md`, and `knowledge/shared/tools-and-mcp-capabilities.md` seeded from `DEVELOPMENT_PRACTICES.md`.
- [ ] Define `knowledge/shared/team-roster-and-capabilities.ttl` schema aligned with ponds→oceans + Apprentice→Master taxonomy.
- [ ] Wire NuSy PM documentation (plan + practices) to reference the new knowledge layout and ships log ritual.

## Milestone 2 — MCP Manifests for Santiago-PM & Santiago-Ethicist

**Goals:**

- Deliver two MCP services (PM = Master/Sea, Ethicist = Journeyman/Lake) that read/write the new knowledge store.
- Register both services in team roster + expose CLI stubs so fake-team mode can operate before DGX arrives.

**Scope / Affected Paths:** `santiago_core/agents/`, `santiago_core/core/`, `nusy_pm_core/`, `knowledge/shared/`, `knowledge/domains/ethics/`, `ocean-research/fake_team_pack/`.

**Tasks:**

- [ ] Create MCP manifest templates under `santiago_core/agents/<role>/mcp/manifest.json` capturing role, skill, knowledge scope, tool list.
- [ ] Implement Typer/FastAPI shims for Santiago-PM and Santiago-Ethicist that expose minimal tools:
  - PM: read/update working agreements, list roster, propose evolution cycles.
  - Ethicist: review evolution files, append guardrails to `knowledge/domains/ethics/evolution-reviews.md`.
- [ ] Update `knowledge/shared/team-roster-and-capabilities.ttl` with both agents’ URIs, MCP endpoints, and tool capabilities.
- [ ] Add scripts/docs so `fake_team_pack` instructions map to these new services (e.g., `python santiago_core/agents/pm/service.py`).

## Milestone 3 — NuSy Orchestrator as MCP Router

**Goals:**

- Transform `src/nusy_pm_core/api.py` into the canonical orchestrator that registers MCP agents, manages sessions, and proxies shared memory utilities.
- Provide APIs for VS Code agents to discover roster, request tasks, and append to ships logs.

**Scope / Affected Paths:** `src/nusy_pm_core/api.py`, `src/nusy_pm_core/services/`, `santiago_core/core/team_coordinator.py`, `santiago_core/run_team.py`, `templates/`.

**Tasks:**

- [ ] Introduce MCP registry module (e.g., `nusy_pm_core/services/mcp_registry.py`) storing manifest metadata + connection info sourced from roster TTL.
- [ ] Refactor `SantiagoTeamCoordinator` so task routing happens through orchestrator-provided interfaces rather than direct Python object references; keep backward-compatible shim for tests.
- [ ] Add orchestrator endpoints:
  - `POST /mcp/sessions` — start session with specified roles & knowledge scope.
  - `POST /team/ships-log` — append structured entries referencing evolution cycles.
  - `GET /team/roster` — return roster graph summary.
- [ ] Document how VS Code agents invoke these APIs (update `README.md` + `DEVELOPMENT_PLAN.md`).

## Milestone 4 — Concurrency Guardrails & Test Harness

**Goals:**

- Implement concurrency + isolation tests described in `nusy_manolin_multi_agent_test_plans.md` and ensure orchestrator enforces session isolation + tool locking.
- Provide BDD + pytest suites that can run locally and on DGX.

**Scope / Affected Paths:** `tests/`, `features/`, `santiago_core/core/`, `src/nusy_pm_core/`, `ocean-research/nusy_manolin_multi_agent_test_plans.md`.

**Tasks:**

- [ ] Convert cross-cutting scenarios (load baseline, session isolation, tool race) into `features/concurrency/*.feature` with accompanying step definitions.
- [ ] Build async pytest harness that spins up PM/Ethicist/Dev MCP services concurrently and validates isolation + latency SLOs.
- [ ] Add structured logging (session_id, role, tool) to orchestrator + agents to aid debugging.
- [ ] Wire CI job to run subset of concurrency tests with mocked inference, plus allow DGX mode via env flag to hit real vLLM runtime.

## Milestone 5 — Manolin Cluster Deployment & Evolution Cycles

**Goals:**

- Operationalize DGX Spark provisioning + storage expansion scripts in-repo and align them with NuSy deployment automation.
- Establish cadence for running evolutionary cycles with ethics reviews + ships log summaries.

**Scope / Affected Paths:** `ocean-research/building-on-DGX/`, new `infrastructure/manolin/` directory, `knowledge/shared/evolution-cycles/`, `santiago-pm/cargo-manifests/`, `chat-history/`.

**Tasks:**

- [ ] Promote provisioning scripts into `infrastructure/manolin/` with README instructions, parameter files, and optional Ansible/Terraform wrappers.
- [ ] Create `runbooks/manolin-cluster.md` referencing storage expansion, monitoring, and rollback procedures.
- [ ] Add CLI command (e.g., `python -m nusy_pm_core.cli evolution new`) that scaffolds an evolution-cycle markdown file and notifies Santiago-Ethicist for review.
- [ ] Require every merged feature to append outcome summaries to `knowledge/shared/ships-log/<date>.md` and update roster if skill/knowledge scope changes.
