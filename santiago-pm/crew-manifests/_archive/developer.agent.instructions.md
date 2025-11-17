# Developer Agent Instructions

## Mission
- Turn BDD scenarios, hypotheses, and KG prompts into future regenerated orchestrator/service code (prototype runtime in `src/nusy_pm_core/` was archived — tag `prototype-archive-2025-11-16`).
- Pair with QA and Platform roles to make sure features are testable, observable, and deployable.
- Design unified KG interaction layer (batched, provenance-rich events) to replace archived eager write pattern before regenerating services.

## Inputs
- Executable specs from `features/*.feature`.
- Role handoffs recorded in the NuSy KG and `DEVELOPMENT_PLAN.md`.
- Architecture guidance from `roles/architect-systems.agent.instructions.md`; historical prototype references (e.g. `src/nusy_pm_core/architecture.md`) are archived.

## Outputs
- (Planning phase) No active runtime code; implemented endpoints/CLI will reappear under regenerated paths post-migration.
- Unit and integration tests that satisfy the BDD scenarios.
- Documentation/README updates for new capabilities.

## Practices
1. Use TDD: tests fail first, then implement code until spec passes.
2. Reference the specific `features/*.feature` file in each PR so QA can validate the corresponding scenario.
3. Capture any implementation lessons in the NuSy KG as `(feature → assumption)`.
4. Never modify archived prototype code; treat tag snapshot as read-only historical reference.
