# Assumptions and Risks

## Assumptions

### Assumption 1: Fake team can build factory in 4-6 weeks

**Basis:** Phase 0 proxies are thin MCP wrappers (20-30 lines per role) calling GPT-4/Claude/Copilot. These powerful external models enable rapid development. Fake team immediately executes expeditions from `santiago-pm/` patterns.

**Validation Strategy:** Track weekly burn-up of Navigator/Catchfish/Fishnet capabilities in `ships-logs/expeditions/`. If any component slips more than one sprint, file expedition to adjust staffing or narrow scope.

### Assumption 2: Clinical prototype throughput generalizes to other domains

**Basis:** `nusy_prototype/` proved 30-60 minute extraction per guideline with 3 validation cycles. PM sources (SAFe, XP) are structurally similar to clinical guidelines—both are structured knowledge with entities, relationships, and workflows.

**Validation Strategy:** Instrument Catchfish to log per-source timings and cycle counts. Require <60 minutes and 3-5 cycles before accepting catch outside healthcare. Run pilot with PM sources to validate before scaling.

### Assumption 3: ≥90% A/B parity is safe replacement threshold

**Basis:** Fake team outputs are control; matching 90% quality while reducing cost/latency hits business goals. Remaining 10% gap allows for edge cases and continued learning.

**Validation Strategy:** Voyage-driven test harness compares fake vs real agents over 10 canonical tasks per role, scoring via Santiago-QA rubric. Document scoring methodology in `voyage-trials/`.

### Assumption 4: DGX Spark capacity sufficient for 10+ concurrent Santiagos

**Basis:** `building-on-DGX/dgx_spark_nusy_report.md` specifies 128GB RAM and 4TB NVMe. vLLM/TensorRT batching allows one shared Mistral-7B instance serving multiple agents with differentiation via prompt prefix and role instructions.

**Validation Strategy:** Load test concurrency milestone (P95 latency <6s) per `nusy_manolin_multi_agent_test_plans.md` before retiring proxy APIs. Monitor GPU/memory metrics with Prometheus.

### Assumption 5: santiago-pm/ folder structure adequate to train teams

**Basis:** Expeditions/tackle/voyage-trials encode hypothesis-driven workflows. They only need wiring into Navigator orchestration to teach both fake and real teams.

**Validation Strategy:** Every expedition log must cite at least one artifact from these folders. Audits ensure compliance. If citations drop below 80%, investigate gaps in pattern coverage.

## Risks

### Risk 1: Catchfish extraction quality regresses as domains diversify

**Impact:** Knowledge graph corruption, low BDD pass rates, failed A/B tests, inability to replace proxies.

**Mitigation:**

- Require queued writes with provenance for all KG mutations
- Enforce 3-5 validation cycles via Navigator before deployment
- Run Fishnet regression suites on historical catches before merging new ones
- Maintain schema validator in pipeline to catch malformed triples
- If BDD pass rate drops below 90%, halt fishing and retrospective

### Risk 2: Fake team API costs exceed budget before first replacement

**Impact:** Financial pressure may halt development prior to factory completion, leaving system in incomplete state.

**Mitigation:**

- Track per-role spend weekly, set budget alerts at 75% threshold
- Prioritize PM catch (highest volume) for first replacement to maximize cost savings
- Throttle non-critical expeditions until Phase 2 parity achieved
- Negotiate volume discounts with API providers (OpenAI, Anthropic)
- Keep lightweight local models (Mistral-7B) ready as fallback

### Risk 3: Real Santiagos fail to reach 90% parity

**Impact:** Replacement stalls, keeping expensive proxies in loop indefinitely. ROI case collapses.

**Mitigation:**

- Use Navigator retrospectives to pinpoint blockers (missing sources, weak validation, insufficient training data)
- Allow hybrid routing (partial traffic to real, partial to fake) until KPIs met
- Expand source corpus if knowledge gaps identified (e.g., add Kanban, Scrum for PM)
- If parity unachievable after 2 attempts, keep fake proxy and document decision
- Run ablation tests: which knowledge gaps cause failures?

### Risk 4: Ethics or concurrency guardrails lag behind capabilities

**Impact:** Tool collisions, policy violations, KG corruption, compliance failures, loss of trust.

**Mitigation:**

- Embed ethicist proxy in every tool queue from Milestone 0
- Run multi-agent test plans (`nusy_manolin_multi_agent_test_plans.md`) at each milestone: session isolation, tool locking, load SLOs
- Block deployments without passing concurrency tests (P95 <6s, no KG corruption)
- Implement circuit breakers: if ethics violations detected, halt all tool execution
- Log all decisions for audit trail in `ships-logs/`

### Risk 5: DGX deployment delays stall Phase 3 replacements

**Impact:** Real Santiagos cannot run on shared model infrastructure; proxies stay longer than planned, increasing costs.

**Mitigation:**

- Maintain temporary cloud inference path (AWS/Azure) as fallback, but limit to backup usage
- Tie DGX readiness to Milestone 5 acceptance criteria—don't proceed without it
- Order hardware early in Phase 1 to allow for shipping/setup time
- Run DGX validation tests in parallel with Phase 2 catch development
- If DGX unavailable, negotiate extended cloud credits rather than delaying replacements

## Provenance & Queued Writes

### Purpose

Prevent knowledge graph corruption during concurrent multi-agent operations while maintaining full audit trail.

### Implementation

**Catchfish Outputs:**

- All extracted knowledge lands in `knowledge/catches/<domain>/domain-knowledge/` with YAML frontmatter
- Frontmatter contains: source URL/hash, extraction timestamp, agent identifier, hypothesis reference
- No direct KG writes; Catchfish enqueues structured mutations

**Fishnet Provenance:**

- Writes BDD suites to `catches/<domain>/bdd-tests/` with generation metadata
- Creates `provenance.yaml` ledger capturing: validation cycles, testers (fake/real), pass/fail deltas, timestamps
- Links back to source documents and Catchfish extraction runs

**Navigator Queue Enforcement:**

- All KG mutations enter `nusy_orchestrator/santiago_builder/pipelines/provenance_queue.py`
- Queue assigns sequence numbers, validates against schema
- Ethics gating screens each mutation for policy compliance (licensing, usage constraints)
- Concurrency control: tool locking prevents simultaneous writes to same KG region
- Only after approval does `kg_writer.py` commit to graph

**Orchestrator Registry:**

- Every merged change updates `knowledge/catches/index.yaml`
- Registry records: Santiago name, trust score (A/B parity %), validation count, last updated
- Orchestrator routing uses registry to decide which Santiago handles which requests
- Allows hybrid deployments: route 80% to real, 20% to fake during transition

**Audit & Replay:**

- Queue runs on idempotent jobs with retry + dead-letter semantics
- Failed mutations logged separately for debugging
- If corruption detected, replay from provenance ledger to last known good state
- All queue events stream to observability stack (Loki) for forensics
