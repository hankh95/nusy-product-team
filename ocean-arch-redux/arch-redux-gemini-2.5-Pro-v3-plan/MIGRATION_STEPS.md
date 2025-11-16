# Migration Steps

## Milestone 0: Bootstrap Fake Team

**Goal:** Deploy thin MCP proxy services for operational fake crew capable of coordinated expeditions

**Affected Paths:** `santiago_core/agents/_proxy/`, `knowledge/proxy-instructions/`, `config/experiment.json`

**Tasks:**

- [ ] Create role cards (PM, Architect, Developer, QA, UX, Platform, Ethicist) in `knowledge/proxy-instructions/`
- [ ] Implement MCP proxy services routing to GPT-4/Claude/Copilot with shared logging hooks
- [ ] Wire proxies into NuSy Orchestrator for expedition-style workflow execution
- [ ] Test compound task: fake team completes backlog grooming + design session end-to-end

**Acceptance Criteria:** Fake team coordinates via MCP to complete compound tasks, outputs logged in `ships-logs/` with provenance

## Milestone 1: Implement Factory Infrastructure

**Goal:** Fake team builds Navigator, Catchfish, Fishnet plus queued knowledge pipeline

**Affected Paths:** `nusy_orchestrator/santiago_builder/`, `santiago_core/agents/_proxy/`, `knowledge/templates/`

**Tasks:**

- [ ] Implement Navigator orchestration following "Old man and the sea" 10-step process with 3-5 validation loops
- [ ] Implement Catchfish 4-layer extraction (raw → entities → Markdown+YAML → KG queue) with timing instrumentation
- [ ] Implement Fishnet BDD + MCP manifest generator tied to queued KG inserts and provenance stamps
- [ ] Create reusable templates for catches, manifests, provenance ledgers in `knowledge/templates/`
- [ ] Build queued write pipeline with schema validation and conflict detection

**Acceptance Criteria:** End-to-end rehearsal converts PDF into `knowledge/catches/demo/` with ≥95% BDD pass rate and auto-generated MCP manifest in <60m

## Milestone 2: First Santiago Catch

**Goal:** Use factory to catch santiago-pm-safe-xp, deploy, and replace fake PM if parity holds

**Affected Paths:** `knowledge/catches/santiago-pm-safe-xp/`, `santiago_core/agents/santiago-pm-safe-xp/`, `voyage-trials/`

**Tasks:**

- [ ] Run fishing expedition using SAFe + XP sources with Navigator enforcing 3 validation cycles
- [ ] Capture knowledge package, BDD suite, manifest, provenance into `knowledge/catches/santiago-pm-safe-xp/`
- [ ] Deploy generated MCP service alongside fake PM proxy, register with orchestrator
- [ ] Execute 10-task A/B test (fake vs real), record quality, latency, cost metrics
- [ ] If real ≥90% quality, update orchestrator routing to retire fake PM proxy

**Acceptance Criteria:** Real Santiago-PM matches ≥90% of fake PM quality, traffic routes to new MCP service, catch stored with full provenance

## Milestone 3: Progressive Replacement Wave 1

**Goal:** Repeat fishing workflow to replace Architect-NuSy and Developer roles

**Affected Paths:** `knowledge/catches/santiago-architect-nusy/`, `knowledge/catches/santiago-developer/`, `santiago_core/agents/`

**Tasks:**

- [ ] Prioritize Architect and Developer catches via Navigator hypothesis backlog
- [ ] Run Catchfish + Fishnet cycles for each role with dedicated validation voyage-trials
- [ ] Deploy generated MCP services, run A/B experiments
- [ ] Retire proxies upon ≥90% parity, maintain metrics dashboard for hybrid periods

**Acceptance Criteria:** Both Architect-NuSy and Developer fake proxies turned off, provenance and test evidence in ships-logs and catches

## Milestone 4: Progressive Replacement Wave 2

**Goal:** Replace QA, UX, Platform roles with shared experiment orchestration tooling

**Affected Paths:** `knowledge/catches/`, `santiago_core/agents/`, `nusy_orchestrator/tests/`

**Tasks:**

- [ ] Extend Catchfish adapters for QA/UX research data and platform SRE runbooks
- [ ] Generate Fishnet suites emphasizing load, usability, deployment guardrails
- [ ] Conduct A/B tests for each role, keep hybrid staffing when evidence ambiguous
- [ ] Build experiment orchestration dashboard tracking parity metrics across all roles

**Acceptance Criteria:** At least two of three roles operate with real Santiagos, hybrid metrics dashboards exist for partial-fake roles

## Milestone 5: DGX Production Hardening

**Goal:** Land shared DGX Spark deployment (vLLM/TensorRT) plus concurrency and ethics enforcement

**Affected Paths:** `building-on-DGX/`, `infrastructure/`, `nusy_orchestrator/concurrency/`, `knowledge/provenance/`

**Tasks:**

- [ ] Provision DGX Spark storage tiers (4TB internal, 8-16TB external NVMe) per deployment guide
- [ ] Host Mistral-7B-Instruct via vLLM with batching APIs exposed to MCP services
- [ ] Implement queued write pipeline with provenance ledger and ethics gating hooks per `nusy_manolin_multi_agent_test_plans.md`
- [ ] Run concurrency load tests (10-agent sessions) validating P95 <6s and no KG corruption
- [ ] Deploy observability stack (Prometheus + Loki) for GPU/memory metrics

**Acceptance Criteria:** DGX stack serves ≥10 concurrent Santiagos with ethics/concurrency monitors green, fake-team APIs no longer needed for steady-state

## Milestone 6: Self-Sustaining Factory Improvements

**Goal:** Empower real Santiagos to propose and deliver iterative factory enhancements

**Affected Paths:** `santiago_core/backlog/`, `ocean-arch-redux/`, `knowledge/catches/index.yaml`, `ships-logs/`

**Tasks:**

- [ ] Establish backlog workflow where real Santiagos file expeditions to improve Catchfish cycle time (<15m target)
- [ ] Implement automated manifest regeneration and trust scoring (index of catches with parity metrics)
- [ ] Create feedback loop where voyage-trial regressions automatically trigger Navigator retrospectives
- [ ] Run pilot: real Santiago-PM proposes parallelization, real Architect/Developer implement, measure improvement

**Acceptance Criteria:** Factory improvements authored and shipped solely by real Santiagos, with measurable Catchfish timing reductions and updated manifests propagated without human intervention
