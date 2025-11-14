# NuSy Product Team Core

This repo hosts the NuSy Product Manager and Product Team scaffolding:

- A NuSy Product Manager agent (Hank’s PM) that coordinates:
  - Architect – NuSy
  - Architect – Systems/Platform
  - Developer
  - QA Specialist
  - UX Researcher / Designer
  - Platform / Deployment Engineer
- A FastAPI service (`src/nusy_pm_core/api.py`) acting as the core PM / MCP surface.
- A Typer CLI (`src/nusy_pm_core/cli.py`) for commands like `scaffold_project`.
- Starter docs:
  - `DEVELOPMENT_PLAN.md` — phased plan for building this system.
  - `DEVELOPMENT_PRACTICES.md` — TDD/BDD/CI and AI–human collaboration rules.
  - `roles/` — role specs and instructions for all team roles.
  - `features/` — BDD feature files, starting with `scaffold_project.feature`.
- Human-friendly scaffolding:
  - `notes/` — Santiago-specific notes, plans, and retrospectives for this mini-project.
  - `santiago-code/` — any code, scripts, or connectors built specifically for the Santiago agent.

## Quick Start

1. **Clone the repo**

```bash
  git clone <your-url>/nusy-product-team.git
  cd nusy-product-team

2. Create and activate a virtual environment

  python -m venv .venv
  source .venv/bin/activate      # macOS/Linux
  # .venv\Scripts\activate       # Windows PowerShell

3. Install dependencies

  pip install -r requirements.txt

4. Configure environment

  cp .env.example .env
  # edit .env as needed

5. Run the API

  uvicorn src.nusy_pm_core.api:app --reload

  Then open:
  - http://localhost:8000/health
  - http://localhost:8000/version

6. Use the CLI

  python -m src.nusy_pm_core.cli version
  python -m src.nusy_pm_core.cli scaffold_project "Example MCP"

Next steps:

- Implement the “Scaffold the Project” feature according to features/scaffold_project.feature.
- Flesh out DEVELOPMENT_PLAN.md and DEVELOPMENT_PRACTICES.md to guide AI agents (Copilot, etc.).
- Gradually add:
  - Git forge integration (Gitea/GitLab).
  - PM tool integration (Taiga).
  - Chat integration (Matrix).
  - NuSy knowledge graph loading and reasoning.

## Santiago Mini-Project

- The Santiago mini-project stores every idea, experiment, and retrospective in `notes/santiago/`. Start by reading `notes/santiago-development-plan.md` to see what we plan to test and ship in the first iteration.
- All Santiago-specific code lives under `santiago-code/`; keep the README in that folder up to date as you add scripts, tests, or connectors.
- Agents should use the `/issues` directory to discover the next Copilot task (ISSUES list is mirrored there so we can stay offline before pushing to GitHub).

This repo is designed to be friendly to VS Code + Copilot (GPT-5 Codex) and other AI IDEs.
Start with the docs and CLI and let the AI help fill in the gaps iteratively.
