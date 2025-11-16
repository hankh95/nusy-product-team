# Migration Steps — Combined Hybrid v3 Plan

This roadmap follows the factory pattern: Phase 0 proxies, Phase 1 factory, Phase 2 first catch and replacement, then progressive replacement and self-improvement. Max 7 milestones.

---

## Milestone 0: Bootstrap Fake Team (Week 1)

- Goal: Deploy thin MCP proxies to external APIs and verify role coordination.
- Affected Paths: `santiago_core/agents/_proxy/`, `knowledge/proxy-instructions/`, `ocean-research/fake_team_pack/`
- Tasks:
  - [ ] Create `santiago_core/agents/_proxy/` with PM, Architect, Dev, QA, UX, Platform, Ethicist proxies
  - [ ] Add `knowledge/proxy-instructions/<role>.md` baseline instructions
  - [ ] Implement unified API adapter (OpenAI/Claude/Copilot) with rate limits and budgets
  - [ ] Smoke test compound tasks across proxies via MCP
- Acceptance Criteria:
  - Proxies respond to basic tools; compound task succeeds end-to-end; budgets and rate limits enforced
  - MCP manifest contract documented for each proxy; mock contract tests pass

## Milestone 1: Implement Factory Infrastructure (Weeks 2–6)

- Goal: Fake team builds Navigator, Catchfish, Fishnet with validation loops and provenance.
- Affected Paths: `nusy_orchestrator/santiago_builder/`, `knowledge/templates/`, `santiago-pm/voyage-trials/`
- Tasks:
  - [ ] Implement `navigator.py` (10-step process, 3–5 validation cycles)
  - [ ] Implement `catchfish.py` (4-layer extraction; Markdown+YAML; KG edges)
  - [ ] Implement `fishnet.py` (BDD generation; MCP manifest inference)
  - [ ] Define trust registry schema and add `knowledge/catches/index.yaml`
  - [ ] Define KG write queue event schema with per-entity locking + idempotency
  - [ ] E2E test: PDF → knowledge → BDD → deployed MCP stub
  - [ ] Produce 2 exemplar BDD features linked to knowledge nodes
- Acceptance Criteria:
  - E2E run completes; provenance recorded; ≥2 feature files generated; CI validates knowledge, registry, and queue event schemas

## Milestone 2: First Santiago Catch (Weeks 7–8)

- Goal: Catch and deploy `santiago-pm-safe-xp`; A/B test and replace if ≥90% parity.
- Affected Paths: `knowledge/catches/santiago-pm-safe-xp/`, `santiago_core/agents/santiago-pm-safe-xp/`, `santiago_core/agents/_proxy/pm_proxy.py`
- Tasks:
  - [ ] Run expedition with Navigator on SAFe 6.0 + XP sources
  - [ ] Iterate 3–5 validation cycles to ≥95% BDD pass
  - [ ] Generate `mcp-manifest.json` and deploy MCP service
  - [ ] A/B test Fake PM vs Real PM on 10+ matched tasks
  - [ ] Define rollback plan (switch-back + canary %) and validate it
  - [ ] Switch routing to Real if ≥90% quality parity; otherwise record deltas and retry
- Acceptance Criteria:
  - `knowledge/catches/santiago-pm-safe-xp/` populated (knowledge, tests, manifest, provenance); replacement decision executed per rule; rollback plan validated

## Milestone 3: Progressive Replacement — Architect & Developer (Weeks 9–12)

- Goal: Repeat expedition for Architect and Developer roles; replace proxies upon parity.
- Affected Paths: `knowledge/catches/santiago-architect-*`, `knowledge/catches/santiago-developer-*`, corresponding MCP services and proxies
- Tasks:
  - [ ] Define authoritative sources per role; run expeditions
  - [ ] Achieve ≥95% BDD pass; generate manifests; deploy services
  - [ ] Run A/B tests and replace proxies on ≥90% parity
- Acceptance Criteria:
  - At least Architect or Developer proxy replaced; routing updated; cost/latency improvements recorded

## Milestone 4: DGX Deployment & Observability (Weeks 9–12, parallel)

- Goal: Stabilize shared 7–8B model serving, observability, and budgets.
- Affected Paths: `ocean-research/building-on-DGX/`, infra-as-code, ops configs
- Tasks:
  - [ ] Deploy vLLM/TensorRT-LLM with continuous batching on DGX
  - [ ] Instrument Prometheus metrics and Loki/Grafana dashboards
  - [ ] Implement per-role budgets and backpressure in orchestrator
- Acceptance Criteria:
  - SLIs/SLOs published: p95 latency ≤ 2500 ms (real), error ≤ 1%, ≥20 RPS sustained; dashboards live; alerting configured; successful load test at target QPS

## Milestone 5: Ethics & Concurrency Gating (Weeks 12–14)

- Goal: Enforce queued KG writes, schema validation, provenance, and ethical review.
- Affected Paths: KG write pipeline, `knowledge/` schema, `santiago_core/` orchestrator
- Tasks:
  - [ ] Add queue-first writes with per-entity locks and schema validation
  - [ ] Stamp provenance on all writes; extend trust registry with versions/hashes
  - [ ] Introduce Ethicist service checks before risky actions; human-in-the-loop escalation
  - [ ] Enforce idempotency keys and rejection on schema violations with diagnostics
- Acceptance Criteria:
  - No direct writes bypass queue; audit trail complete; gated actions require explicit approvals; idempotency and schema validation verified in CI

## Milestone 6: Self-Improvement Loop (Weeks 14–20)

- Goal: Real Santiagos propose and implement factory improvements via guarded RFCs.
- Affected Paths: `nusy_orchestrator/santiago_builder/`, RFC process, CI
- Tasks:
  - [ ] Establish RFC template and review gate for factory changes
  - [ ] Run A/B or rehearsal tests for proposed changes
  - [ ] Roll out improvements with provenance and rollback plans
- Acceptance Criteria:
  - At least one factory improvement shipped by a real Santiago; test coverage and performance improve without KG corruption
