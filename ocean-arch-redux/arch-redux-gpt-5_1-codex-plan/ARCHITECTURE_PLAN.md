# Architecture Plan — GPT-5.1-Codex

Date: 2025-11-16

## 1. Executive Overview

NuSy currently contains two partially overlapping initiatives:

- **`src/nusy_pm_core/`** exposes a FastAPI + Typer service surface focused on notes, issues, and plan tracking but without a persistent multi-agent runtime.
- **`santiago_core/`** scaffolds an autonomous trio (PM/Architect/Developer) with an internal coordinator and RDF-based knowledge graph stored under `santiago_core/knowledge/`.

The target vision described across `ocean-research/` is a **Manolin Cluster** on DGX Spark where a Santiago-led team (PM, Ethicist, Architects, Developers, Hank as Captain) collaborate via MCP services, backed by shared memory (`knowledge/`), ponds-to-ocean knowledge scopes, and evolutionary development cycles.

This plan reconciles the current state with that target by defining the architectural lanes, data contracts, and service boundaries needed to evolve NuSy into a Santiago-first multi-agent platform.

## 2. Current Architecture Assessment

### 2.1 Application Surfaces

- `src/nusy_pm_core/api.py`: REST API focused on knowledge ingestion, plans, and issues. No MCP surface, no explicit multi-agent endpoints, little awareness of Santiago agents.
- `santiago_core/run_team.py`: launches three hard-coded agents via in-process asyncio; no external toolability, no MCP, no persistence beyond `knowledge_graph.py` TTL.

### 2.2 Knowledge & Memory

- Knowledge graph lives solely under `santiago_core/knowledge/` with TTL outputs; there is no repo-level `knowledge/` directory or shared ships-log described in research docs.
- `notes/` folder captures Santiago experiments but is disconnected from the RDF KG.

### 2.3 Agent & Tooling Gap

- Agents defined in `santiago_core/agents/*.py` use bespoke messaging and have no MCP manifests, no per-role tool declarations, and no notion of skill/knowledge tiers.
- `nusy_pm_core` services do not surface the Santiago team roster or register capabilities.

### 2.4 Operational Gap

- No DGX/Manolin deployment artifacts exist inside the repo (automation scripts live only in research docs).
- CI/CD and concurrency/load considerations from `nusy_manolin_multi_agent_test_plans.md` are absent from implementation.

## 3. Target Architecture (from Research)

Key requirements synthesized from `ocean-research/`:

1. **MCP-based Agent Mesh** — Each Santiago role (PM, Ethicist, Architect, Dev x2, QA, UX, Platform) is an MCP service exposing skills, knowledge scope (Pond→Ocean), and tooling.
2. **Shared Team Memory** — Repository-level `knowledge/` topology: `knowledge/shared/`, `knowledge/domains/<domain>/`, `knowledge/shared/ships-log/`, `knowledge/shared/team-roster-and-capabilities.ttl`.
3. **Evolution Cycles** — BDD-first evolution files, ethics reviews, and apprentices graduating to masters.
4. **Manolin Cluster Deployment** — DGX Spark host with Mistral-7B runtime (vLLM), fast NVMe tiers, automation scripts, and concurrency testing.
5. **Coordinator Over MCP** — NuSy orchestrator assigns work to MCP agents, manages sessions, enforces ethics, and logs to shared memory + KG.

## 4. Proposed Architecture

### 4.1 Layered View

1. **Interaction Layer (MCP/HTTP):**
   - `nusy_pm_core` becomes the **NuSy Orchestrator MCP gateway** exposing: session orchestration API, MCP registration, and shared memory utilities.
   - VS Code / CLI clients interact through MCP, not direct Python imports.
2. **Agent Layer:**
   - Each Santiago role implemented as a thin MCP server (initially local Typer/FastAPI apps) residing under `santiago_core/agents/<role>/service/`.
   - Agents declare manifests referencing skill level + knowledge scope and implement tool handlers bridging to shared memory, KG, and external adapters.
3. **Knowledge Layer:**
   - Repo-level `knowledge/` directory becomes the canonical shared memory; `santiago_core/services/knowledge_graph.py` writes to `knowledge/shared/kg/` to decouple from code tree.
   - Team roster TTL describes every agent, MCP endpoint, skill tier, and scope.
4. **Runtime Layer:**
   - DGX Spark hosts a single shared LLM (Mistral-7B-Instruct via vLLM) accessible through an inference gateway consumed by all agents.
   - Containerized deployment (Docker + NVIDIA runtime) managed via provisioning scripts from `ocean-research/building-on-DGX/`.

### 4.2 Key Architectural Changes

| Area | Current | Target |
| --- | --- | --- |
| Agent contracts | In-process Python classes | MCP services + manifests with declared tools, skill tiers, knowledge scope |
| Shared memory | `santiago_core/knowledge/` only | `knowledge/shared/`, `knowledge/domains/*/`, KG TTL + ships logs + roster |
| Coordinator | `SantiagoTeamCoordinator` synchronous | NuSy Orchestrator bridging FastAPI ↔ MCP, supporting multi-agent concurrency & DGX deployment |
| Ethics | Embedded `EthicalOversight` class | Dedicated Santiago-Ethicist MCP service gating plan milestones and capability changes |
| Evolution tracking | Ad-hoc notes in `notes/santiago/` | `knowledge/shared/evolution-cycles/*` + BDD features + ships logs |

### 4.3 Data Contracts & Tooling

- **Team Roster Graph:** Extend `SantiagoKnowledgeGraph` schema to include `skill_level`, `knowledge_scope`, `mcp_endpoint`, `tools` and sync with `knowledge/shared/team-roster-and-capabilities.ttl`.
- **Shared Memory APIs:** Implement simple Python/CLI utilities (`nusy_pm_core/knowledge_tools.py`) that MCP agents call for reading/writing working agreements, ships logs, and evolution cycles.
- **Ethics Hooks:** All plan or capability changes trigger `Santiago-Ethicist` review; orchestrator enforces approval bit before execution.

### 4.4 Role & Capability Model

- **Santiago-PM (Master, Sea):** Maintains backlog, working agreements, evolution cycles, roster completeness.
- **Santiago-Ethicist (Journeyman, Lake):** Reviews every evolution, produces guardrails in `knowledge/domains/ethics/evolution-reviews.md`.
- **Architect Roles (Journeyman/Master, Sea):** Manage NuSy ontology, system infra (DGX + storage) and update `ocean-research` derived plans.
- **Developers (Apprentice→Journeyman, Pond→Lake):** Implement features via BDD + CLI scaffolds; escalate to Masters based on test history.
- **Hank (Captain):** Remains human-in-the-loop with override ability, captured in ships logs.

### 4.5 Deployment & Operations

- **Environment Patterns:**
   - Local dev: Run orchestrator + MCP agents via `uv`/`poetry` and mock inference (OpenAI/Azure) per `fake_team_pack` guidance.
   - DGX deployment: Use automation scripts (`provision_dgx_spark_base.sh`, etc.) to bootstrap host, then deploy orchestrator + agents as services (systemd or containers) with GPU-accessible inference runtime.
- **Observability:** Add session-level logging, metrics per agent (latency, concurrency) to satisfy `nusy_manolin_multi_agent_test_plans.md`.

## 5. Gaps & Considerations

1. **Shared knowledge folder missing** — need to create real `knowledge/` tree to support target state.
2. **Tooling debt** — typical developer tooling (CI, tests, MCP discovery) is absent; migration plan must stage these capabilities.
3. **Security & secrets** — provisioning scripts mention secrets mgmt but repo lacks implementation; ensure `.env` + vault pattern before DGX deployment.
4. **Scalable concurrency** — `SantiagoTeamCoordinator` currently blocks on `await asyncio.gather`; multi-agent load tests must move to orchestrator-level concurrency with proper cancellation semantics.
5. **Manolin hardware timeline** — architecture must support "fake team" mode (external LLM APIs) until DGX arrives; MCP manifests should note runtime mode (remote vs local inference).

## 6. Success Criteria

- MCP agents registered with manifests exposing role, skill, knowledge scope, and tool surfaces.
- Repository-level shared memory & knowledge graph accessible to both human and AI contributors.
- Evolution cycles recorded with ethics review + ships log entries.
- NuSy Orchestrator coordinates concurrent tasks per `nusy_manolin_multi_agent_test_plans.md` and can deploy to DGX Spark following provisioning scripts.
- Documentation in `ocean-arch-redux/arch-redux-gpt-5_1-codex-plan/` provides clear next steps for future agents/humans.
