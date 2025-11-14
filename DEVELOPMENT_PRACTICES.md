# Development Practices for NuSy Product Team

## Core Principles

1. **TDD / BDD First** – Every new capability starts with an executable specification (Gherkin, test spec, or notebook). Tests must fail before code is implemented.
2. **Small Batch, Fast Feedback** – Ship incremental slices that touch vision -> hypothesis -> experiment → metric in one cycle.
3. **Knowledge Graph as Source of Truth** – Capture decisions, hypotheses, and role expectations into the NuSy KG so future features can query reuse patterns.
4. **Transparent Team Coordination** – Document handoffs, outputs, and CI status in chat and Git so every role stays aligned.

## Tooling Rules

- The `features/` directory holds BDD scenarios (Gherkin).
- The `roles/` directory hosts `*.agent.instructions.md` files describing expectations per role.
- The `nusy_pm_core/` service exposes MCP endpoints; all changes must ship with documentation or API contracts.

## Quality Gates

| Gate | Description | Enforcement |
| --- | --- | --- |
| Tests | All features must add or update BDD/TDD specs before merging | CI runs `pytest` and `behave` (or equivalent) per feature |
| Code Review | Each PR must list impacted artifacts (plan, features, KG entries) | Reviewers verify artifacts and tests |
| Knowledge Capture | Feature learning summary and experiment result must be added to KG | Update `knowledge/` folder or KG import agents |

## Collaboration Rituals

- **Daily Vision Sync** – Share what hypothesis you’re testing today and what KG entities got updated.
- **Knowledge Debrief** – Once an experiment finishes, summarize the outcome and update the KG with the new relationship triangles.
- **Practices Backlog** – When a gap is spotted (missing role instructions, inconsistent testing), add a card and refine practice docs.
