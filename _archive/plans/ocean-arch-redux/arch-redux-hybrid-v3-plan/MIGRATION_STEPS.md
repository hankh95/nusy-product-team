# Migration Steps

## Milestone 0: Bootstrap Fake Team

**Goal:** Deploy thin MCP proxy services for operational fake crew capable of coordinated expeditions

**Affected Paths:** `santiago_core/agents/_proxy/`, `knowledge/proxy-instructions/`, `config/experiment.json`

**Tasks:**

- [ ] Create role cards (PM, Architect, Developer, QA, UX, Platform, Ethicist) in `knowledge/proxy-instructions/`
- [ ] Implement MCP proxy services routing to GPT-4/Claude/Copilot with shared logging hooks
- [ ] Wire proxies into NuSy Orchestrator for expedition-style workflow execution
- [ ] Document MCP manifest contract for each proxy with versioned capabilities, TTL, budgets
- [ ] Test compound task: fake team completes backlog grooming + design session end-to-end

**Acceptance Criteria:**

- Fake team coordinates via MCP to complete compound tasks, outputs logged in `ships-logs/` with provenance
- MCP manifest contract documented for each proxy; mock contract tests pass
- Proxies respond to basic tools; budgets and rate limits enforced

---

## Milestone 1: Implement Factory Infrastructure

**Goal:** Fake team builds Navigator, Catchfish, Fishnet plus queued knowledge pipeline

**Affected Paths:** `nusy_orchestrator/santiago_builder/`, `santiago_core/agents/_proxy/`, `knowledge/templates/`

**Tasks:**

- [ ] Implement Navigator orchestration following "Old man and the sea" 10-step process with 3-5 validation loops
- [ ] Implement Catchfish 4-layer extraction (raw → entities → Markdown+YAML → KG queue) with timing instrumentation
- [ ] Implement Fishnet BDD + MCP manifest generator tied to queued KG inserts and provenance stamps
- [ ] Create reusable templates for catches, manifests, provenance ledgers in `knowledge/templates/`
- [ ] Build queued write pipeline with schema validation and conflict detection
- [ ] Define trust registry schema and add `knowledge/catches/index.yaml`
- [ ] Define KG write queue event schema with per-entity locking + idempotency
- [ ] Produce 2 exemplar BDD features linked to knowledge nodes

**Acceptance Criteria:**

- End-to-end rehearsal converts PDF into `knowledge/catches/demo/` with ≥95% BDD pass rate and auto-generated MCP manifest in <60m
- ≥2 feature files generated; CI validates knowledge, registry, and queue event schemas
- Provenance recorded; contract acceptance tests pass

---

## Milestone 2: First Santiago Catch

**Goal:** Use factory to catch santiago-pm-safe-xp, deploy, and replace fake PM if parity holds

**Affected Paths:** `knowledge/catches/santiago-pm-safe-xp/`, `santiago_core/agents/santiago-pm-safe-xp/`, `voyage-trials/`

**Tasks:**

- [ ] Run fishing expedition using SAFe + XP sources with Navigator enforcing 3 validation cycles
- [ ] Capture knowledge package, BDD suite, manifest with capability level + knowledge scope, provenance into `knowledge/catches/santiago-pm-safe-xp/`
- [ ] Deploy generated MCP service alongside fake PM proxy, register with orchestrator
- [ ] Execute 10-task A/B test (fake vs real), record quality, latency, cost metrics
- [ ] Define rollback plan (canary routing: 10% → 50% → 100%, switch-back, warm proxy) and validate it
- [ ] If real ≥90% quality, update orchestrator routing via canary progression to retire fake PM proxy

**Acceptance Criteria:**

- Real Santiago-PM matches ≥90% of fake PM quality, traffic routes to new MCP service via canary progression, catch stored with full provenance
- `knowledge/catches/santiago-pm-safe-xp/` populated (knowledge, tests, manifest, provenance); replacement decision executed per rule; rollback plan validated
- Trust registry entry created with version, hash, BDD pass rate, capability level, replacement decision

---

## Milestone 3: Progressive Replacement Wave 1

**Goal:** Repeat fishing workflow to replace Architect-NuSy and Developer roles

**Affected Paths:** `knowledge/catches/santiago-architect-nusy/`, `knowledge/catches/santiago-developer/`, `santiago_core/agents/`

**Tasks:**

- [ ] Prioritize Architect and Developer catches via Navigator hypothesis backlog
- [ ] Run Catchfish + Fishnet cycles for each role with dedicated validation voyage-trials
- [ ] Deploy generated MCP services, run A/B experiments with hybrid routing (80/20 splits during transition)
- [ ] Track parity metrics dashboards (quality, latency, cost) per role
- [ ] Retire proxies upon ≥90% parity, maintain metrics dashboard for hybrid periods

**Acceptance Criteria:**

- Both Architect-NuSy and Developer fake proxies turned off or hybrid routing active with ≥80% traffic to real, provenance and test evidence in ships-logs and catches
- Trust registry updated; routing config reflects hybrid or full replacement decisions
- Cost/latency improvements recorded

---

## Milestone 4: Progressive Replacement Wave 2

**Goal:** Replace QA, UX, Platform roles with shared experiment orchestration tooling

**Affected Paths:** `knowledge/catches/`, `santiago_core/agents/`, `nusy_orchestrator/tests/`

**Tasks:**

- [ ] Extend Catchfish adapters for QA/UX research data and platform SRE runbooks
- [ ] Generate Fishnet suites emphasizing load, usability, deployment guardrails
- [ ] Conduct A/B tests for each role, keep hybrid staffing when evidence ambiguous
- [ ] Build experiment orchestration dashboard tracking parity metrics across all roles
- [ ] Run ablation tests if parity fails to identify which knowledge gaps cause failures

**Acceptance Criteria:**

- At least two of three roles operate with real Santiagos, hybrid metrics dashboards exist for partial-fake roles
- Ablation test results documented for any failed replacements
- Trust registry reflects all replacement decisions with rationale

---

## Milestone 5: DGX Production Hardening & Ethics Gating

**Goal:** Land shared DGX Spark deployment (vLLM/TensorRT) plus concurrency and ethics enforcement

**Affected Paths:** `building-on-DGX/`, `infrastructure/`, `nusy_orchestrator/concurrency/`, `knowledge/provenance/`

**Tasks:**

- [ ] Provision DGX Spark storage tiers (4TB internal hot, 8-16TB external warm, NAS cold) per deployment guide
- [ ] Host Mistral-7B-Instruct via vLLM with batching APIs exposed to MCP services
- [ ] Implement queued write pipeline with provenance ledger and ethics gating hooks per `nusy_manolin_multi_agent_test_plans.md`
- [ ] Add queue-first writes with per-entity locks and schema validation
- [ ] Stamp provenance on all writes; extend trust registry with versions/hashes
- [ ] Introduce Ethicist service checks before risky actions; human-in-the-loop escalation
- [ ] Enforce idempotency keys and rejection on schema violations with diagnostics
- [ ] Run concurrency load tests (10-agent sessions) validating P95 <6s and no KG corruption
- [ ] Deploy observability stack (Prometheus + Loki) for GPU/memory metrics

**Acceptance Criteria:**

- DGX stack serves ≥10 concurrent Santiagos with ethics/concurrency monitors green, fake-team APIs no longer needed for steady-state
- SLIs/SLOs published: p95 latency ≤ 2500 ms (real), error ≤ 1%, ≥20 RPS sustained; dashboards live; alerting configured; successful load test at target QPS
- No direct writes bypass queue; audit trail complete; gated actions require explicit approvals; idempotency and schema validation verified in CI

---

## Milestone 6: Self-Sustaining Factory Improvements

**Goal:** Empower real Santiagos to propose and deliver iterative factory enhancements

**Affected Paths:** `santiago_core/backlog/`, `ocean-arch-redux/`, `knowledge/catches/index.yaml`, `ships-logs/`

**Tasks:**

- [ ] Establish backlog workflow where real Santiagos file expeditions to improve Catchfish cycle time (<15m target)
- [ ] Implement automated manifest regeneration and trust scoring (index of catches with parity metrics)
- [ ] Create feedback loop where voyage-trial regressions automatically trigger Navigator retrospectives
- [ ] Establish RFC template and review gate for factory changes
- [ ] Run A/B or rehearsal tests for proposed changes
- [ ] Roll out improvements with provenance and rollback plans
- [ ] Run pilot: real Santiago-PM proposes parallelization, real Architect/Developer implement, measure improvement

**Acceptance Criteria:**

- Factory improvements authored and shipped solely by real Santiagos, with measurable Catchfish timing reductions and updated manifests propagated without human intervention
- At least one factory improvement shipped by a real Santiago; test coverage and performance improve without KG corruption
