# Migration Steps (v3)

## Milestone 0 — Fake Team Online

**Goal:** Ship a functioning crew of MCP proxies that can execute expedition workflows and produce logs/provenance.

**Affected Paths:** `santiago_core/agents/_proxy/`, `knowledge/proxy-instructions/`, `config/experiment.json`

**Tasks:**

- [ ] Author role cards for PM, Architect, Developer, QA, UX, Platform, Ethicist in `knowledge/proxy-instructions/`
- [ ] Implement thin MCP proxy services (route to external models; add unified logging)
- [ ] Wire proxies into Orchestrator so multi-step expeditions run end-to-end
- [ ] Validate with a compound task (backlog grooming → design session → acceptance review)

**Acceptance Criteria:** End-to-end run succeeds with artifacts in `ships-logs/` and basic parity metrics recorded.

---

## Milestone 1 — Factory Core Delivered

**Goal:** Build Navigator, Catchfish, Fishnet and a queued KG write pipeline with schema/provenance enforcement.

**Affected Paths:** `nusy_orchestrator/santiago_builder/`, `knowledge/templates/`, `knowledge/catches/`

**Tasks:**

- [ ] Implement Navigator orchestration of the 10-step fishing workflow with 3–5 validation loops
- [ ] Implement Catchfish 4-layer extraction with timing instrumentation and provenance
- [ ] Implement Fishnet to generate BDD scenarios and MCP manifests from the KG
- [ ] Provide templates for catches (domain-knowledge, bdd-tests, manifest, provenance)
- [ ] Add KG write queue with schema validation and ethics/concurrency hooks

**Acceptance Criteria:** Dress rehearsal converts a sample PDF → `knowledge/catches/demo/` with ≥95% BDD pass rate in ≤60 minutes.

---

## Milestone 2 — First Real Santiago (PM)

**Goal:** Catch and deploy `santiago-pm` from SAFe/XP sources; replace fake PM if parity holds.

**Affected Paths:** `knowledge/catches/santiago-pm/`, `santiago_core/agents/santiago-pm/`, `voyage-trials/`

**Tasks:**

- [ ] Run expedition with Navigator enforcing ≥3 validation cycles
- [ ] Package knowledge, BDD, manifest, provenance in `knowledge/catches/santiago-pm/`
- [ ] Deploy MCP service and register with Orchestrator alongside the proxy
- [ ] Run a 10-task A/B test (quality, latency, cost) against fake PM
- [ ] Switch routing when real PM reaches ≥90% parity

**Acceptance Criteria:** Real PM handles production traffic; proxy retired; parity evidence logged.

---

## Milestone 3 — Replacement Wave 1 (Architect, Developer)

**Goal:** Repeat the catch/validate/deploy pattern for Architect and Developer roles.

**Affected Paths:** `knowledge/catches/santiago-architect/`, `knowledge/catches/santiago-developer/`, `santiago_core/agents/`

**Tasks:**

- [ ] Prioritize roles via PM backlog; define hypotheses for each catch
- [ ] Run Catchfish + Fishnet cycles and targeted voyage-trials
- [ ] Deploy new MCP services and A/B test
- [ ] Retire proxies after sustained ≥90% parity

**Acceptance Criteria:** Architect and Developer proxies disabled; evidence stored in catches and logs.

---

## Milestone 4 — Replacement Wave 2 (QA, UX, Platform)

**Goal:** Replace additional roles while improving experiment orchestration and dashboards.

**Affected Paths:** `knowledge/catches/`, `nusy_orchestrator/tests/`, `ships-logs/`

**Tasks:**

- [ ] Extend Catchfish adapters for QA/UX/Platform sources
- [ ] Generate Fishnet suites for load/usability/deployment guardrails
- [ ] Maintain hybrid routing when evidence is ambiguous; continue experiments

**Acceptance Criteria:** At least two of three roles fully real; experiments traceable and repeatable.

---

## Milestone 5 — DGX Production Readiness

**Goal:** Land shared inference and concurrency/ethics enforcement with SLOs.

**Affected Paths:** `building-on-DGX/`, `nusy_orchestrator/concurrency/`, `knowledge/provenance/`

**Tasks:**

- [ ] Provision storage tiers (hot NVMe, warm RAID) per guide
- [ ] Host a shared instruction model (vLLM/TensorRT) with batching
- [ ] Enforce queued writes with provenance + ethics checks
- [ ] Run concurrency tests (≥10 agents) and meet P95 < 6s
- [ ] Stand up observability (Prometheus + Loki) and alerts

**Acceptance Criteria:** DGX environment green; steady-state no longer depends on proxy APIs.

---

## Milestone 6 — Self-Sustaining Improvements

**Goal:** Real Santiagos drive factory optimization via measurable expeditions.

**Affected Paths:** `santiago_core/backlog/`, `knowledge/catches/index.yaml`, `ships-logs/`

**Tasks:**

- [ ] Establish a backlog of factory hypotheses (e.g., sub-15-minute Catchfish)
- [ ] Automate manifest regeneration and trust score updates
- [ ] Trigger Navigator retrospectives on regression

**Acceptance Criteria:** Improvements authored and shipped by real Santiagos with measurable wins.
