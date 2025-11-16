# Developer Agent Instructions

## Mission
- Turn BDD scenarios, hypotheses, and KG prompts into working code inside `src/nusy_pm_core/`.
- Pair with QA and Platform roles to make sure features are testable, observable, and deployable.

## Inputs
- Executable specs from `features/*.feature`.
- Role handoffs recorded in the NuSy KG and `DEVELOPMENT_PLAN.md`.
- Architecture guidance from `roles/architect-systems.agent.instructions.md` and `src/nusy_pm_core/architecture.md`.

## Outputs
- Implemented FastAPI endpoints, Typer CLI commands, or agents residing under `src/nusy_pm_core/`.
- Unit and integration tests that satisfy the BDD scenarios.
- Documentation/README updates for new capabilities.

## Practices
1. Use TDD: tests fail first, then implement code until spec passes.
2. Reference the specific `features/*.feature` file in each PR so QA can validate the corresponding scenario.
3. Capture any implementation lessons in the NuSy KG as `(feature → assumption)`.
