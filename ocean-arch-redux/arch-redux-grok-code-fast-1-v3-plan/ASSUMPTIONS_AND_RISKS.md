# Santiago Factory Assumptions and Risks

## Assumptions

- **Fake team builds factory in 4-6 weeks:** External APIs (GPT-4, Claude) provide sufficient capability for fake team to implement Navigator, Catchfish, Fishnet without manual coding.
- **Clinical prototype evidence generalizes:** 30-60m conversion time and 3 validation cycles apply to all domains, not just clinical guidelines.
- **A/B testing at ≥90% parity is sufficient replacement threshold:** Real Santiagos matching 90% of fake performance justifies proxy replacement.

## Risks

- **Catchfish extraction quality degrades without validation:** If validation loops fail, knowledge gaps lead to incomplete Santiagos.
- **Fake team API costs exceed budget before first replacement:** High costs from external APIs delay Phase 2, risking project viability.
- **Real Santiagos fail to match fake performance:** If real Santiagos underperform, no replacement occurs, system remains API-dependent.

## Provenance & Queued Writes

Unified KG layer with queued writes to avoid corruption:

- **Provenance tracking:** Each write includes prompt, context, tools, constraints, reviewers/approvals, artifact hashes, timestamps.
- **Queued writes:** KG updates enqueued, apply schema validation and provenance checks before merging.
- **Schema validation:** Ensures KG integrity, prevents conflicting updates.
- **Trust registry:** `knowledge/catches/index.yaml` summarizes approvals, versions, integration status.
