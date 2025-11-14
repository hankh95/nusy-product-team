# NuSy Product Team Core

This repo hosts the **NuSy Product Manager and Product Team** scaffolding:

- A **NuSy Product Manager agent** (Hank’s PM) that coordinates:
  - Architect – NuSy
  - Architect – Systems/Platform
  - Developer
  - QA Specialist
  - UX Researcher / Designer
  - Platform / Deployment Engineer
- A **FastAPI service** (`src/nusy_pm_core/api.py`) acting as the core PM / MCP surface.
- A **Typer CLI** (`src/nusy_pm_core/cli.py`) for commands like `scaffold_project`.
- Starter docs:
  - `DEVELOPMENT_PLAN.md` — phased plan for building this system.
  - `DEVELOPMENT_PRACTICES.md` — TDD/BDD/CI and AI–human collaboration rules.
  - `roles/` — role specs and instructions for all team roles.
  - `features/` — BDD feature files, starting with `scaffold_project.feature`.

## Quick Start

1. **Clone the repo**

```bash
git clone <your-url>/nusy-product-team.git
cd nusy-product-team
