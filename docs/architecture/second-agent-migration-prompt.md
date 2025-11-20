# Prompt for Second Agent (EXP‑057 Migration Work)

You are joining an in‑progress architecture migration for the **NuSy / Santiago autonomous product-management system**.

## Repository & Branch

- **Repo**: `nusy-product-team`
- **Branch**: `exp-057-architecture-redux-3-migration`
- **Primary architecture doc**: `docs/architecture/arch-vision-merged-plan.md`
- **Migration review & work packages**: `MIGRATION_PLAN_ARCH_REVIEW.md`

## Runtime & Kanban Context

- The system uses:
  - **In-memory Git + Knowledge Graph** as the "brain".
  - A **Kanban system** (`self-improvement/santiago-pm/tackle/kanban`) as the unified workflow controller.
- There is a dedicated board for this work:
  - **Board ID**: `exp-057-migration`
  - Location: managed via `self-improvement/santiago-pm/tackle/kanban/kanban_cli.py` and rendered in `self-improvement/santiago-pm/kanban-boards.md`.

## Your Mission

1. **Read the spec**:
   - Skim `docs/architecture/arch-vision-merged-plan.md` to understand the target architecture.
   - Read `MIGRATION_PLAN_ARCH_REVIEW.md` carefully; it defines the approved decisions and six work packages (WP1–WP6).

2. **Use the Kanban board as your source of truth**:

   From `self-improvement/santiago-pm`:

   ```bash
   # Optional: activate venv
   # source ../../venv/bin/activate
   python -m tackle.kanban.kanban_cli show-board exp-057-migration
   ```

   - Choose **one** card (work package) that is still in **Backlog/Ready** and not clearly owned by another agent (e.g., `WP1: Self-Improvement Import Fixes` or `WP2: Missing Components Resolution`).
   - Move it to `in_progress` with your name:

   ```bash
   python -m tackle.kanban.kanban_cli move-card exp-057-migration <card_id> in_progress --moved-by "agent-name"
   ```

3. **Work style & constraints**

- **Follow**:
  - TDD/BDD and development workflow described in `CONTRIBUTING.md`.
  - The architecture decisions and scope in `MIGRATION_PLAN_ARCH_REVIEW.md`.
- **Do not**:
  - Make destructive changes to `santiago_core/` or legacy artifacts beyond what is explicitly allowed in your chosen work package.
  - Change production behavior without tests and clear justification.
- **Do**:
  - Keep changes **PR-sized** and cohesive around your chosen work package.
  - Use clear commits referencing the work package (e.g., `WP1: Fix self-improvement imports`).
  - Update the Kanban card state (`in_progress` → `review` → `done`) as you work.

1. **Deliverables per work package**

For whichever WP card you pick (from `MIGRATION_PLAN_ARCH_REVIEW.md`):

- Implement the code, tests, and docs needed to satisfy its description.
- Ensure **CI/test suite passes** locally for the areas you touch.
- Add any follow‑up notes (if needed) to a relevant log:
  - `self-improvement/santiago-pm/personal-logs/agents/` or
  - `self-improvement/santiago-pm/ships-logs/`
- When done:
  - Move the card to `done` via the Kanban CLI.
  - Leave a short summary in the card via a comment (or in the commit message) referencing what you changed.

Assume another agent is working in parallel on a **different** WP card from the same board; avoid overlapping scope unless explicitly coordinated via Kanban and comments.
