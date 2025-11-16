# Prototype Legacy: Runtime Archive (2025-11-16)

The original prototype (`src/nusy_pm_core/` + `santiago-code/`) is archived (removed from main) to streamline architecture review and eliminate misleading scaffolding. A full snapshot is preserved via git tag: `prototype-archive-2025-11-16`.

## What The Prototype Demonstrated

- **Rapid JSON Persistence**: Notes, issues, plans, experiments stored in flat JSON files (`data/*.json`) for speed of iteration.
- **Immediate KG Decoration**: Each CRUD call eagerly wrote RDF triples (rdflib) causing implicit coupling between persistence and knowledge representation.
- **Neurosymbolic Stub**: A lightweight keyword extractor plus graph dump served as a placeholder for a richer neurosymbolic reasoning core.
- **Pipeline Modules**:
  - `SeawaterProcessor`: Parsed markdown note sections → L0 structures.
  - `CatchFishProcessor`: Converted L0 content into RDF triples with minimal provenance.
  - `FishNetGenerator`: Generated BDD scenario templates; highlighted intent to validate KG + behavior coverage.
- **Typer CLI & FastAPI Surface**: Exposed CRUD + pipeline triggers for interactive exploration.
- **Autonomous Experiment Scaffolds**: Experiment runner & agent adapter simulated multi-agent coordination (Quartermaster ethical oversight, Pilot PM expertise, Santiago orchestration).

## Key Lessons & Limitations

| Area | Lesson | Limitation / Change Rationale |
|------|--------|--------------------------------|
| Persistence | Simple JSON enabled velocity | Lacked transactional integrity, versioning, indexing |
| KG Writes | Eager decoration ensured visibility | Scattered writes → no batching, hard to enforce consistency |
| Reasoner | Stub helped shape query surface | No symbolic rule layer, no hybrid probabilistic integration |
| Pipeline | Clear stage boundaries useful | No incremental re-run / diff strategy; hash collisions possible |
| CLI/API | Fast iteration & demos | Inflated perceived maturity; not modular; mixed orchestration concerns |
| Experiment Runner | Highlighted agent roles & flows | Inter-agent logic embedded in async methods; no state machine |
| Agent Adapter | Fallback design resilient | Hardwired prompts; lacked capability negotiation or role evolution |

## Migration Principles (Forward)

1. **Separation of Concerns**: Split persistence, KG indexing, and reasoning into discrete layers with explicit contracts.
2. **Unified KG Interaction Layer**: Single module for queued, idempotent writes + schema validation.
3. **Event-Sourced Notes & Issues**: Replace flat JSON with append-only event log → materialized views.
4. **Composable Pipeline Steps**: Each stage pure + cacheable; support partial re-processing and provenance tracking.
5. **Reasoner Evolution Path**: Introduce declarative rule registry + embedding-backed semantic expansion.
6. **Agent Framework Abstraction**: Shift from hard-coded adapters to capability registry & negotiation protocol.
7. **Observability First**: Structured logs + metrics from inception; pipeline + KG instrumentation.

Reference the detailed steps in `ocean-arch-redux/arch-redux-gpt-5-v2-plan/MIGRATION_STEPS_v2.md` for sequencing.

## Retrieval Instructions

To inspect the removed code locally:

```bash
git checkout prototype-archive-2025-11-16 -- src/nusy_pm_core santiago-code
```

(Use a detached workspace or branch to avoid reintroducing legacy code.)

## Deferred Risks Documented

- Lack of schema evolution policy for KG predicates.
- Absence of concurrency controls around simultaneous note / issue writes.
- No provenance metadata for KG triples beyond minimal source linking.
- No authentication / authorization model for API endpoints.

## Next Architectural Focus

- Implement "Unified KG Layer" (see planned issue) consolidating all triple writes.
- Define `domain-model` package with versioned schemas + validation rules.
- Establish integration test harness using synthetic provenance scenarios.

## Tag Integrity Verification

To confirm tag content:

```bash
git show prototype-archive-2025-11-16 --name-only | grep src/nusy_pm_core | head
```

---
This document intentionally replaces scattered inline comments and README runtime instructions to keep the root surface minimal for reviewers.
