# NuSy Product Team Core

> ARCHIVE NOTICE (2025-11-16): Prototype runtime code (`src/nusy_pm_core/` and `santiago-code/`) has been archived and removed to reduce cognitive load for architecture reviewers. An annotated snapshot is preserved via the git tag `prototype-archive-2025-11-16`. See `docs/PROTOTYPE_LEGACY.md` for lessons learned and migration rationale. The active focus of this repository is the v2 architecture planning artifacts under `ocean-arch-redux/arch-redux-gpt-5-v2-plan/`.

This repo now emphasizes planning, strategic reasoning, and architecture evolution. The former prototype implementation (FastAPI service, Typer CLI, multi-agent experiment runner, KG pipeline) has been retired and documented. Future runtime code will be regenerated following the migration steps outlined in `ocean-arch-redux/arch-redux-gpt-5-v2-plan/MIGRATION_STEPS_v2.md`.

## Reviewers Quick Start

For architecture reviewers (humans and AIs), start here:

- Prompt: `architecture-redux-prompt-v2.md` (at repo root)
- Strategic canonical: `santiago-pm/strategic-charts/Santiago-Trains-Manolin.md`
- Strategic index: `santiago-pm/strategic-charts/README.md`
- Calibration pointer: `calibration/README.md` (do not read until after initial deliverables)
- Latest v2 plan outputs: `ocean-arch-redux/arch-redux-gpt-5-v2-plan/`

## Quick Start (Planning Focus)

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

5. Review architecture & migration artifacts
  - `ARCHITECTURE_PLAN_v2.md`
  - `MIGRATION_STEPS_v2.md`
  - `FOLDER_LAYOUT_PROPOSAL_v2.md`
  - `RELEVANCE_MAP.md`

Runtime commands are intentionally absent until the migration phase begins.

## Prototype Legacy

The archived prototype exposed note ingestion, KG decoration, neurosymbolic querying stubs, and autonomous experiment orchestration. It served as a learning scaffold; details and lessons are captured in `docs/PROTOTYPE_LEGACY.md`.

## Usage Focus Shift

Active work now centers on refining architecture artifacts, validating migration sequencing, and preparing for a clean, modular rebuild (KG interaction layer, unified persistence, agent orchestration).

## Santiago Mini-Project Artifacts

Santiago-related knowledge and retrospectives remain in `notes/santiago/` and strategic vision in `santiago-pm/strategic-charts/`. Execution code has been archived; only conceptual and strategic materials are active.

AI reviewers should ignore runtime concerns until migration steps authorize regeneration.
