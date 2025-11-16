# Assumptions and Risks — Combined Hybrid v3 Plan

---

## Assumptions

- Fake team can build the factory in 4–6 weeks
  - Rationale: Thin MCP proxies are fast to implement; most work is orchestrating Navigator, Catchfish, Fishnet.
  - Validation: Weekly demos of E2E runs; burn-down on Catchfish throughput and Fishnet coverage.

- Clinical prototype evidence generalizes (30–60m per source, 3 validation cycles)
  - Rationale: The 4-layer extraction model and validation loops are domain-agnostic.
  - Validation: Pilot across PM (SAFe + XP), Architecture (12-factor, C4 refs), and QA (Gherkin style guides) with the same loop.

- A/B testing threshold at ≥90% parity is sufficient for replacement
  - Rationale: Quality-cost tradeoff; shared DGX model reduces cost materially once proxies are replaced.
  - Validation: Define explicit scoring rubric; run 10–20 matched tasks; include inter-rater reliability checks.

- DGX can sustain target throughput via vLLM/TensorRT-LLM
  - Rationale: Observability and batching control allow tuning for latency/throughput envelopes.
  - Validation: Load test with representative traffic; publish SLIs and SLOs.

## Risks

- Catchfish extraction quality degrades without proper validation
  - Impact: KG corruption, brittle MCP services, test flakiness
  - Mitigation: Enforce ≥95% BDD pass before deploy; Navigator requires 3–5 cycles; provenance and trust registry entries mandatory

- Fake team API costs exceed budget before first replacement
  - Impact: Burn rate risks, schedule pressure
  - Mitigation: Apply budgets and rate limits per role; prioritize first catch with highest ROI (PM); move heavy workflows onto DGX earlier

- Real Santiagos fail to reach ≥90% parity
  - Impact: No replacement; value trapped behind proxies
  - Mitigation: Expand sources; refine extraction prompts; add specialized tools; increase validation cycles; consider role split (narrower scope)

- Concurrency issues cause KG race conditions
  - Impact: Inconsistent knowledge state; hard-to-debug failures
  - Mitigation: Queue-first writes with per-entity locks; schema validation and versioning

- Overfitting to initial sources reduces generalization
  - Impact: Poor performance on new tasks
  - Mitigation: Include diversity in sources; Fishnet generates broad coverage; periodic re-evaluation with fresh corpora

## Provenance & Queued Writes

- Unified KG Layer: All knowledge artifacts write through a single queue that enforces schema validation (Markdown + YAML frontmatter, graph edges) and versioned commits.
- Provenance Stamping: Every artifact includes `provenance.yaml` with sources, timestamps, hash, validation results, and authorship (proxy/real Santiago IDs).
- Trust Registry: `knowledge/catches/index.yaml` tracks catches, versions, hashes, validation status, and replacement decisions.
- Rehearsal Gate: ≥95% BDD pass required before deployment; runs on DGX to match production conditions.
- A/B Replacement Gate: Replacement requires ≥90% quality parity vs proxy measured on matched tasks; rollback paths defined and tested.

## Rollback Strategy

- Canary Routing: Start with 10% traffic to the real Santiago for 1–2 hours; if parity remains ≥90% and error ≤1%, ramp to 50%, then 100%.
- Switch-Back: Orchestrator keeps proxy service warm; a single feature-flag toggle returns routing to proxy within 1 minute.
- Data Safety: All KG writes from real Santiagos occur via the queue with idempotency keys; on rollback, pending events for the real service are drained and paused.
- Audit & Postmortem: On rollback, capture metrics snapshot, registry note (reason, timestamp), and open an RFC for remediation before retry.
