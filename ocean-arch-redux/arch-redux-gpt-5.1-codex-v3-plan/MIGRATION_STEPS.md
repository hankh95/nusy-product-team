# Migration Steps

## Milestone 0: Bootstrap Fake Team (Week 1)

**Goal:** Stand up thin MCP proxy services so we have a working fake crew capable of coordinated expeditions.

**Affected Paths:** `santiago_core/agents/_proxy/`, `knowledge/proxy-instructions/`, `config/experiment.json`

**Tasks:**

- [ ] Add role cards for PM, Architect, Developer, QA, UX, Platform, Ethicist under `knowledge/proxy-instructions/`
- [ ] Implement MCP proxy services that route to GPT-4/Claude/Copilot with shared logging hooks
- [ ] Wire proxies into NuSy Orchestrator so fake team can run expedition-style workflows end-to-end

**Acceptance Criteria:** Fake team completes a compound backlog grooming + design session using only proxy roles, and outputs are logged in `ships-logs/` with provenance.

## Milestone 1: Implement Factory Infrastructure (Weeks 2-6)

**Goal:** Have fake team build Navigator, Catchfish, and Fishnet plus the queued knowledge pipeline they require.

**Affected Paths:** `nusy_orchestrator/santiago_builder/`, `santiago_core/agents/_proxy/`, `knowledge/templates/`

**Tasks:**

- [ ] Implement Navigator orchestration following the "Old man and the sea" 10-step process with 3-5 validation loops
- [ ] Implement Catchfish 4-layer extraction (raw → entities → Markdown+YAML → KG queue) with timing instrumentation
- [ ] Implement Fishnet BDD + MCP manifest generator tied to queued KG inserts and provenance stamps
- [ ] Create reusable templates for catches, manifests, and provenance ledgers in `knowledge/templates/`

**Acceptance Criteria:** End-to-end rehearsal converts a PDF into `knowledge/catches/demo/` with ≥95% BDD pass rate and auto-generated MCP manifest.

## Milestone 2: First Santiago Catch (Weeks 7-8)

**Goal:** Use the factory to catch `santiago-pm-safe-xp`, deploy it, and replace the fake PM if parity holds.

**Affected Paths:** `knowledge/catches/santiago-pm-safe-xp/`, `santiago_core/agents/santiago-pm-safe-xp/`, `voyage-trials/`

**Tasks:**

- [ ] Run fishing expedition using SAFe + XP sources with Navigator enforcing 3 validation cycles
- [ ] Capture knowledge package, BDD suite, manifest, and provenance into `knowledge/catches/santiago-pm-safe-xp/`
- [ ] Deploy the generated MCP service alongside the fake PM proxy and register it with the orchestrator
- [ ] Execute 10-task A/B test (fake vs real) and record quality, latency, and cost metrics

**Acceptance Criteria:** Real Santiago-PM matches ≥90% of fake PM quality in tests, leading to traffic being routed to the new MCP service.

## Milestone 3: Progressive Replacement Wave 1 (Weeks 9-14)

**Goal:** Repeat the fishing workflow to replace Architect-NuSy and Developer roles.

**Affected Paths:** `knowledge/catches/santiago-architect-nusy/`, `knowledge/catches/santiago-developer/`, `santiago_core/agents/`

**Tasks:**

- [ ] Prioritize Architect and Developer catches via Navigator hypothesis backlog
- [ ] Run Catchfish + Fishnet cycles for each role with dedicated validation voyage-trials
- [ ] Deploy generated MCP services, run A/B experiments, and retire proxies upon ≥90% parity

**Acceptance Criteria:** Both Architect-NuSy and Developer fake proxies are turned off, with provenance and test evidence stored in ships-logs and catches folders.

## Milestone 4: Progressive Replacement Wave 2 (Weeks 15-20)

**Goal:** Replace QA, UX, and Platform roles while introducing shared tooling for experiment orchestration.

**Affected Paths:** `knowledge/catches/`, `santiago_core/agents/`, `nusy_orchestrator/tests/`

**Tasks:**

- [ ] Extend Catchfish adapters for QA/UX research data and platform SRE runbooks
- [ ] Generate Fishnet suites emphasizing load, usability, and deployment guardrails
- [ ] Conduct A/B tests for each role; keep hybrid staffing when evidence is ambiguous

**Acceptance Criteria:** At least two of the three roles operate with real Santiagos, and hybrid metrics dashboards exist for any roles still partially fake.

## Milestone 5: DGX Production Hardening (Weeks 16-20)

**Goal:** Land the shared DGX Spark deployment (vLLM/TensorRT) plus concurrency and ethics enforcement in production.

**Affected Paths:** `building-on-DGX/`, `infrastructure/`, `nusy_orchestrator/concurrency/`, `knowledge/provenance/`

**Tasks:**

- [ ] Provision DGX Spark storage tiers (4 TB internal, 8-16 TB external NVMe) per deployment guide
- [ ] Host Mistral-7B-Instruct via vLLM with batching APIs exposed to MCP services
- [ ] Implement queued write pipeline with provenance ledger and ethics gating hooks per `nusy_manolin_multi_agent_test_plans.md`
- [ ] Run concurrency load tests (10-agent sessions) to validate P95 < 6s and no KG corruption

**Acceptance Criteria:** DGX stack serves ≥10 concurrent Santiagos with ethics/concurrency monitors green, and fake-team APIs are no longer needed for steady-state traffic.

## Milestone 6: Self-Sustaining Factory Improvements (Week 20+)

**Goal:** Empower real Santiagos to propose and deliver iterative factory enhancements using expeditions/tackle/voyage patterns.

**Affected Paths:** `santiago_core/backlog/`, `ocean-arch-redux/`, `knowledge/catches/index.yaml`, `ships-logs/`

**Tasks:**

- [ ] Establish backlog workflow where real Santiagos file expeditions to improve Catchfish cycle time (<15m target)
- [ ] Implement automated manifest regeneration and trust scoring (index of catches with parity metrics)
- [ ] Create feedback loop where voyage-trial regressions automatically trigger Navigator retrospectives

**Acceptance Criteria:** Factory improvements are authored and shipped solely by real Santiagos, with measurable reductions in Catchfish timing and updated manifests propagated without human intervention.
