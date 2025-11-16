# Assumptions and Risks

## Assumptions

1. **Fake team can build the factory within 4-6 weeks.**
   - *Basis:* Phase 0 proxies are thin MCP wrappers (20-30 lines per role) and can immediately execute expeditions from `santiago-pm/` patterns.
   - *Validation:* Track weekly burn-up of Navigator/Catchfish/Fishnet capabilities in `ships-logs/expeditions/`; if any component slips more than one sprint, file an expedition to adjust staffing or narrow scope.
2. **Clinical prototype throughput generalizes to other domains.**
   - *Basis:* `nusy_prototype/` proved 30-60 minute extraction per guideline with three validation cycles; PM sources (SAFe, XP) are structurally similar.
   - *Validation:* Instrument Catchfish to log per-source timings and cycle counts; require <60 minutes and 3-5 cycles before accepting a catch outside healthcare.
3. **≥90% A/B parity is a safe replacement threshold.**
   - *Basis:* Fake team outputs are the control; matching 90% quality while reducing cost/latency hits business goals.
   - *Validation:* Voyager-driven test harness compares fake vs real agents over 10 canonical tasks, scoring via Santiago-QA rubric.
4. **DGX Spark capacity (Mistral-7B-Instruct) is sufficient for 10+ concurrent Santiagos.**
   - *Basis:* `building-on-DGX/dgx_spark_nusy_report.md` specifies 128 GB RAM and 4 TB NVMe, with batching via vLLM/TensorRT.
   - *Validation:* Load test concurrency milestone (P95 latency < 6s) before retiring proxy APIs.
5. **santiago-pm/ folder structure is adequate to train fake and real teams.**
   - *Basis:* Expeditions/tackle/voyage-trials encode hypothesis-driven workflows; they only need wiring into Navigator.
   - *Validation:* Every expedition log must cite at least one artifact from these folders; audits ensure compliance.

## Risks

1. **Catchfish extraction quality regresses as domains diversify.**
   - *Impact:* Knowledge graph corruption, low BDD pass rates.
   - *Mitigation:* Require queued writes with provenance, enforce 3 validation cycles, and run Fishnet regression suites before merging new catches.
2. **Fake team API costs exceed budget before first replacement.**
   - *Impact:* Financial pressure may halt development prior to factory completion.
   - *Mitigation:* Track per-role spend, prioritize PM catch (highest volume) for replacement, and throttle non-critical expeditions until parity achieved.
3. **Real Santiagos fail to reach 90% parity.**
   - *Impact:* Replacement stalls, keeping expensive proxies in loop.
   - *Mitigation:* Use Navigator retrospectives to pinpoint blockers (missing sources, weak validation) and allow hybrid routing (partial traffic) until KPIs met.
4. **Ethics or concurrency guardrails lag behind new capabilities.**
   - *Impact:* Tool collisions, policy violations, or KG corruption.
   - *Mitigation:* Embed ethicist proxy in every tool queue, run multi-agent test plans (`nusy_manolin_multi_agent_test_plans.md`) at each milestone, and block deployments without passing scores.
5. **DGX deployment delays stall Phase 3 replacements.**
   - *Impact:* Real Santiagos cannot run on shared model; proxies stay longer.
   - *Mitigation:* Maintain temporary cloud inference path, but limit to fallback; tie DGX readiness to Milestone 5 acceptance criteria.

## Provenance & Queued Writes

- All Catchfish outputs land in `knowledge/catches/<domain>/domain-knowledge/` with YAML frontmatter containing source hashes, timestamps, and agent identifiers.
- Fishnet writes BDD suites plus a `provenance.yaml` ledger capturing validation cycles, testers, and pass/fail deltas.
- Navigator enforces a queued write pipeline: knowledge mutations enter `nusy_orchestrator/santiago_builder/pipelines/provenance_queue.py`, then merge into the KG only after Ethics and concurrency checks acknowledge the request.
- Every merged change updates `knowledge/catches/index.yaml`, recording trust scores (A/B parity %, validation count) so orchestrator routing remains auditable.
- Queues run on idempotent jobs with retry + dead-letter semantics, preventing half-applied KG updates and enabling post-incident replay if corruption is detected.
