# Runtime Architecture Stub

The previous prototype runtime has been archived (tag: `prototype-archive-2025-11-16`). This stub marks the intentional absence of active runtime modules during the architecture redesign phase.

## Purpose

- Prevent reviewers conflating prototype scaffolding with forward architecture.
- Signal upcoming regeneration of services after migration validation.

## Planned Regeneration Components

1. Unified KG Interaction Layer (batched, schema-validated writes)
2. Event-sourced persistence (notes, issues, plans, experiments)
3. Neurosymbolic Reasoner v2 (rule + embedding hybrid)
4. Agent capability negotiation + orchestration bus
5. API surface aligned to bounded contexts (separate service modules)

See `ocean-arch-redux/arch-redux-gpt-5-v2-plan/MIGRATION_STEPS_v2.md` for sequencing.
