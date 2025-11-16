# Migration Steps — GPT-5 v2 (Plan-Only)

This plan refines milestones based on a full-repo read. It assumes no production code edits in this phase; deliverables are planning artifacts and scaffolds.

## Milestone 1 — Relevance + Knowledge Canonicalization

- Create `knowledge/` at repo root with:
  - `knowledge/shared/`: `roster.ttl`, `working-agreements.md`, `ships-log.md`, `evolution-cycles/`.
  - `knowledge/domains/core/`: `graph.ttl`, `glossary.md`.
- Consolidate graphs from `notes/` and `santiago_core/knowledge/` into `domains/core/graph.ttl` with provenance.
- Add CI lint for Markdown (MD022/31/32/55/58) and Turtle syntax.

## Milestone 2 — Orchestrator Skeleton

- Define orchestrator API surface: task submit/status, audit log, evolution CRUD, knowledge search/query.
- Add ethics/concurrency middleware stubs (rate limiting, policy checks, approvals) — plan-only interface.
- Draft OpenAPI and minimal request/response contracts (plan-level).

## Milestone 3 — MCP Service Boundaries

- Define MCP manifests for PM and Developer services; include tool schemas, knowledge mounts, and audit hooks.
- Map `santiago_core/agents` behaviors to MCP tools; list gaps and adapter needs.
- Plan for UX/QA/Architect/Platform services similarly, tracking dependencies.

## Milestone 4 — DGX/Manolin Mode

- Specify environment flags and adapter boundaries for DGX vs local.
- Outline provisioning automation steps referencing `ocean-research/building-on-DGX/*` docs.
- Identify model backends and data connectors (Spark, vector store, vLLM) and their config surfaces.

## Milestone 5 — Consolidation and Cleanup

- Choose `santiago_core/` as canonical over `santiago/` and `santiago-code/`; mark duplicates for retirement.
- Normalize documentation locations; link ships-logs and development practices into `knowledge/shared/`.
- Update templates to align with MCP service scaffolds.

## Milestone 6 — Pilot Flows and Tests (Plan Level)

- Gherkin feature stubs for orchestrated flows across two services (PM→Developer) with ethics gates.
- Concurrency tests per `ocean-research/nusy_manolin_multi_agent_test_plans.md` as plan scenarios.
- Acceptance: manifests pass lint; knowledge tree populated; plan contracts stable.
