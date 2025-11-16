# Assumptions and Risks (v3)

## Assumptions

1. **Fake team can build the factory core within 4–6 weeks.**
   - Basis: MCP proxies are thin wrappers; expedition/tackle patterns accelerate delivery.
   - Validation: Weekly burn-up of Navigator/Catchfish/Fishnet capabilities; slip >1 sprint triggers scope/ownership adjustment.

2. **Clinical 4-layer extraction generalizes to PM and adjacent domains.**
   - Basis: Structure (entities/relations/workflows) appears across guidelines and methods.
   - Validation: Instrument Catchfish; require ≤60 minutes/source and 3–5 validation cycles before adopting in production.

3. **≥90% parity is a safe replacement threshold.**
   - Basis: Real must match fake on quality while improving cost/latency.
   - Validation: 10-task A/B harness with transparent rubric and logs.

4. **DGX Spark can support ≥10 concurrent Santiagos via batched inference.**
   - Basis: vLLM/TensorRT allow efficient shared serving.
   - Validation: Concurrency tests meet P95 < 6s with no KG corruption.

5. **`santiago-pm/` patterns are sufficient to train fake and real teams.**
   - Basis: Expedition/tackle/voyage provide an operational backbone.
   - Validation: Every expedition cites at least one artifact; audits when citation rate <80%.

---

## Risks

1. **Extraction quality drifts across domains.**
   - Impact: KG corruption, failing BDD suites, stalled replacements.
   - Mitigation: Queued writes with schema validation; require validation loops; run regression tests on historical catches.

2. **Proxy API costs rise before first replacement.**
   - Impact: Budget pressure delays factory completion.
   - Mitigation: Track per-role spend; prioritize PM for early ROI; throttle non-critical expeditions; maintain small local models as fallback.

3. **Parity threshold not achieved.**
   - Impact: Proxies remain; ROI weakens.
   - Mitigation: Navigator retrospectives; hybrid routing; broaden source corpus; explicit stop/continue criteria after repeated attempts.

4. **Ethics/concurrency guardrails lag capability.**
   - Impact: Policy breaches or data corruption.
   - Mitigation: Ethics in every tool queue; load/lock/isolation tests at milestones; circuit breakers on violations; comprehensive logging.

5. **DGX deployment delays.**
   - Impact: Prolonged dependence on costly external APIs.
   - Mitigation: Cloud fallback with caps; align DGX readiness with gating criteria; stage hardware and tests early.

---

## Provenance & Queued Writes (Implementation Notes)

- Catchfish writes Layer-3 artifacts with YAML frontmatter (source hash, timestamp, agent ID, hypothesis reference).
- Fishnet writes `.feature` tests and a `provenance.yaml` ledger of validation cycles and outcomes.
- Navigator routes KG mutations through `pipelines/provenance_queue.py` → `kg_writer.py` only after ethics and concurrency checks pass.
- `knowledge/catches/index.yaml` records trust scores (parity %, validations) for Orchestrator routing and gradual rollouts.
- Queues are idempotent with retry/dead-letter; replay from provenance is supported for recovery.
