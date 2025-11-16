# Architecture Plan — Copilot GPT-5 v2 (2025-11-16)

```text
**Metadata**
Model Name: copilot-gpt-5
Model Version: unknown
Date: 2025-11-16
Repo Commit SHA: 53a9fc4
Run ID: arch-plan-copilot-gpt-5-2025-11-16-1
```text

## 1. Current Architecture Summary
- Prototype runtime (`src/nusy_pm_core/`) ARCHIVED (tag `prototype-archive-2025-11-16`).
- No root `knowledge/` hierarchy exists (GAP) — scattered TTL (`notes/kg.ttl`, any historical knowledge subpaths).
- `santiago_core/` directory absent (GAP) though strategic docs reference it as core engine; existing domain artifacts under `santiago-pm/` and planning docs under `ocean-arch-redux/`.
- Multi-agent and neurosymbolic pipeline concepts (Seawater, CatchFish, FishNet, Navigator) present only in legacy summaries in `nusy_prototype/`.
- Research cluster expectations (DGX / Manolin) detailed in `ocean-research/` docs but not codified into infra or provisioning scripts.
- Ethics gating and concurrency patterns not yet implemented in code; only described textually.

## 2. Target Architecture Overview
"Ethics & Concurrency Gating" enforced across orchestrator and MCP services.
- Orchestrator Service (`orchestrator/`): Coordinates tasks, evolution cycles, policy & audit events.
- MCP Role Services (`services/mcp-<role>/`): PM, Ethicist, Architect, Developer, QA, UX, Platform. Each exposes manifest.json, tool schemas, knowledge mounts, audit hooks.
- Unified Knowledge Tree (`knowledge/`):
  - `knowledge/shared/` (roster.ttl, working-agreements.md, ships-log.md, evolution-cycles/, policy.ttl).
  - `knowledge/domains/core/` (graph.ttl, glossary.md, ontology.ttl, provenance-log.ttl).
  - Additional domain folders introduced via migration milestones.
- Unified KG Interaction Layer: Batched queued writes, provenance capture, schema validation, idempotent operations (replacing prior eager writes).
- Ethics & Concurrency Gate Middleware: Rate limiting, approval workflows, disallowed-action policy, multi-step escalation referencing `ocean-research/nusy_manolin_multi_agent_test_plans.md`.
- Deployment Modes:
  - Local Dev: single-process orchestrator + stub MCP services, file-based KG.
  - DGX/Manolin: containerized services, Spark integration for data, vector store (e.g. Milvus / pgvector), vLLM for model hosting.
- Observability: Structured logs (JSON), request tracing with correlation IDs, audit ledger capturing tool invocations + decisions.

## 3. Key Architectural Deltas
| Area | Current | Target | Delta Actions |
| --- | --- | --- | --- |
| Runtime Core | Archived prototype | Regenerated orchestrator + MCP services | Scaffold orchestrator + manifests, retire legacy patterns |
| Knowledge | Scattered TTL & docs | Hierarchical `knowledge/` with domains/shared | Consolidate, add provenance & ontology |
| KG Writes | Eager individual writes | Queued, batched, provenance-rich events | Implement interaction layer abstraction |
| Concurrency | Unspecified | Policy + rate limit + gating middleware | Define gating interfaces + test harness |
| Ethics | Text only | Programmatic policies + audit + escalation | Encode ethics rules in TTL/policy file + middleware checks |
| Deployment | Local scripts only | Dual-mode (local & DGX cluster) | Provisioning runbooks + config separation |
| Role Services | Conceptual | MCP manifests per role | Generate manifest templates & capability contracts |
| Evolution Cycles | Ad-hoc docs | Formal cycle artifacts in shared knowledge | Define cycle template + orchestrator endpoints |

## 4. Interfaces & Contracts (Plan-Level)
- Orchestrator API (OpenAPI draft):
  - POST /tasks, GET /tasks/{id}
  - POST /evolution-cycles, GET /evolution-cycles/{id}
  - GET /knowledge/search?q=...
  - GET /audit/{id}
- MCP Manifest (JSON): role, capabilities[], tools[], knowledge_mounts[], policies[], version.
- KG Interaction Layer Python Interface (pseudo):
  - `queue_write(triple, provenance)`
  - `flush(batch_size)`
  - `validate(triple)`
  - `get_history(entity_id)`
- Ethics & Concurrency Gate Middleware Hooks:
  - `before_tool_call(context)`
  - `check_policy(action, actor)`
  - `record_decision(result)`

## 5. Knowledge Graph Unification Principles
- Single authoritative core graph: `knowledge/domains/core/graph.ttl`.
- Provenance: Named graphs or reified triples linking source doc filename + timestamp.
- Batch Commit: Flush queue on size/time triggers; produce aggregate provenance record.
- Schema Evolution: Track ontology versions in `ontology.ttl`; migration scripts update dependent manifests.

## 6. Ethics & Concurrency Gating Strategy
Derived from `ocean-research/nusy_manolin_multi_agent_test_plans.md`:
- Pre-execution classification: safety level + risk tag.
- For high-risk operations: escalate to Ethicist MCP service for approval.
- Quota windows per role (e.g., max concurrent dev tasks) with dynamic reduction during high system load.
- Audit ledger: immutable append-only file + structured events for reproducibility.

## 7. DGX / Manolin Deployment Considerations
- Container sets: orchestrator, each MCP role service, vector store, Spark gateway.
- Shared volume / object store for `knowledge/` snapshots.
- CI pipeline builds local dev image + DGX variant (feature flag for cluster connectors).
- Provisioning automation referencing `ocean-research/nusy_manolin_provisioning_automation.md` (infra steps, secrets management).

## 8. Observability & Metrics
- Metrics: task latency, queue depth (KG writes), approval turnaround time, policy violation counts.
- Knowledge Coverage: ratio of backlog concepts mapped to graph entities.
- Evolution Metrics: cycle outcome improvement vs previous cycles.

## 9. Risks (High-Level)
- Delay in knowledge consolidation causing schema drift.
- Over-complex gating increasing friction.
- Insufficient provenance leading to weak audit trails.
- DGX integration complexity delaying role service rollout.

## 10. Success Criteria (Phase v2)
- Root `knowledge/` tree created with shared + core domain populated.
- MCP manifests (PM & Ethicist) defined and linted.
- Orchestrator interface + ethics/concurrency gate specifications documented.
- Migration milestones accepted (see MIGRATION_STEPS.md).
- References cited across all deliverables; independence maintained pre-calibration.

### References Cited
- ocean-research/dgx_spark_nusy_report.md
- ocean-research/nusy_manolin_architecture.md
- ocean-research/nusy_manolin_provisioning_automation.md
- ocean-research/nusy_manolin_multi_agent_test_plans.md
- ocean-research/fake_team_feature_plan.md
- ocean-research/fake_team_steps_for_hank_and_copilot.md
- ocean-research/features-capabilities-for-shared-memory-and-evolution.md
