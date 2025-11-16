# Santiago Factory Migration Steps

## Milestone 0: Bootstrap Fake Team

**Goal:** Deploy fake team MCP proxies to external APIs, enabling factory construction.

**Affected Paths:** `santiago_core/agents/_proxy/`, `knowledge/proxy-instructions/`

**Tasks:**

- [ ] Create MCP proxy classes for each role (PM, Architect, Developer, QA, Ethicist, UX, Platform)
- [ ] Implement API routing to OpenAI/Claude/Copilot with role instructions
- [ ] Load instructions from `knowledge/proxy-instructions/`
- [ ] Validate fake team coordination on compound tasks

**Acceptance Criteria:** Fake team operational in <1 week, coordinates via MCP, completes hypothesis writing.

## Milestone 1: Implement Factory Infrastructure

**Goal:** Fake team builds Navigator, Catchfish, Fishnet components.

**Affected Paths:** `nusy_orchestrator/santiago_builder/`, `santiago_core/agents/_proxy/`

**Tasks:**

- [ ] Fake team implements Navigator (10-step orchestration)
- [ ] Fake team implements Catchfish (4-layer extraction, 30-60m → <15m)
- [ ] Fake team implements Fishnet (BDD generation from KG)
- [ ] Fake team writes BDD tests for factory behavior
- [ ] End-to-end test: PDF → deployed MCP service

**Acceptance Criteria:** Factory operational in <6 weeks, end-to-end fishing expedition succeeds.

## Milestone 2: First Santiago Catch

**Goal:** Factory catches santiago-pm-safe-xp, A/B test vs. fake, replace if ≥90% parity.

**Affected Paths:** `knowledge/catches/santiago-pm-safe-xp/`, `santiago_core/agents/`

**Tasks:**

- [ ] Run fishing expedition for PM domain (SAFe/XP sources)
- [ ] Catchfish extracts knowledge (30-60m)
- [ ] Fishnet generates BDD tests
- [ ] Navigator validates with 3-5 cycles (≥95% pass rate)
- [ ] Deploy as MCP service
- [ ] A/B test fake vs. real on 10 tasks
- [ ] Replace proxy if ≥90% parity

**Acceptance Criteria:** Real Santiago-PM deployed, A/B shows ≥90% parity, API costs reduced by 1/7th.

## Milestone 3: Progressive Replacement

**Goal:** Repeat catch/replacement for each role, achieving hybrid then full real team.

**Affected Paths:** `knowledge/catches/`, `santiago_core/agents/`

**Tasks:**

- [ ] Catch Santiago-Architect-NuSy from ontology sources
- [ ] A/B test and replace if ≥90% parity
- [ ] Repeat for Developer, QA, Ethicist, UX, Platform
- [ ] Manage hybrid team during transitions
- [ ] Hypothesis-driven experiments per replacement

**Acceptance Criteria:** All roles replaced or kept based on A/B results, system runs on DGX without external API dependency.

## Milestone 4: Self-Sustaining Factory

**Goal:** Real Santiagos improve factory, enable on-demand Santiago generation.

**Affected Paths:** `nusy_orchestrator/santiago_builder/`, `knowledge/catches/`

**Tasks:**

- [ ] Real Santiagos propose improvements (e.g., Catchfish parallelization)
- [ ] Implement enhancements via self-directed experiments
- [ ] Optimize Catchfish to <15m per source
- [ ] Generate new domain Santiagos autonomously

**Acceptance Criteria:** Factory self-improves, generates Santiagos for new domains, zero external API dependency.
