Here’s a prompt you can paste into any of your AI tools (Grok in VS Code, Copilot agents, etc.) when you’re in the root of nusy-product-team.

I’ll write it so the model knows:
	•	Repo root: nusy-product-team
	•	Research folder: ocean-research/
	•	Output folder: ocean-arch-redux/
	•	Per-model subfolder: ocean-arch-redux/arch-redux-<model_name>-plan/

You can tweak <model_name> if you want to hard-code it for a specific run.

⸻


You are acting as an **AI Software Architect & Refactoring Planner** for the `nusy-product-team` repository.

Your job is to:

1. Ingest the existing project under the current workspace root (`nusy-product-team`).
2. Ingest the **new research** and planning documents under `ocean-research/`.
3. Propose a **revised architecture and migration plan** for the project.
4. Save your results in `ocean-arch-redux/` in a structured way so future agents (and humans) can follow your plan.

---

## Context You MUST Use

1. **Project root:**  
   The current workspace root is the `nusy-product-team` repo.  
   You should scan at least:
   - `src/` (or equivalent code directories)
   - `knowledge/` (if present)
   - Any existing `README.md`, `DEVELOPMENT_PLAN.md`, `DEVELOPMENT_PRACTICES.md`

2. **New research folder: `ocean-research/`**  
   You MUST read and use the relevant files here, including (but not limited to):

   - `dgx_spark_nusy_report.md`  
   - `nusy_manolin_procurement_checklist.md`  
   - `nusy_manolin_architecture.md`  
   - `nusy_manolin_provisioning_automation.md`  
   - `nusy_manolin_multi_agent_test_plans.md`  
   - `fake_team_feature_plan.md` (or similarly named file)  
   - `fake_team_steps_for_hank_and_copilot.md`  
   - The feature/capability plan describing:
     - Santiago-PM
     - Santiago-Ethicist
     - Shared memory (`knowledge/` layout)
     - Apprentice/Journeyman/Master
     - Pond/Lake/Sea/Ocean knowledge scopes
     - MCP-based agents & team orchestration

   Treat these as the **authoritative vision** for where the architecture is trying to go:
   - DGX Spark / Manolin Cluster
   - Santiago-based multi-agent team
   - NuSy PM, Architect, Developers, Ethicist, and Hank (Captain / Vision Holder)
   - Use of MCP to expose each agent’s capabilities
   - Shared team memory across agents

---

## Your Output Location & Structure

All your outputs for this run must go into:

- `ocean-arch-redux/`

Inside that folder, create a subfolder specific to YOURSELF:

- `ocean-arch-redux/arch-redux-<model_name>-plan/`

Where `<model_name>` is some short identifier for you (for example, `grok-code-fast-1`, `gpt-5-architect`, `claude-arch`, etc.). Use a name that another agent or human can later recognize.

Inside your subfolder, produce at least:

1. `ARCHITECTURE_PLAN.md`  
   A detailed narrative describing:
   - Your understanding of the **current architecture** (as implemented in this repo).
   - Your understanding of the **target architecture** (as described in `ocean-research/`).
   - The key architectural changes you recommend to:
     - Support Santiago-PM, Santiago-Ethicist, and the Manolin team.
     - Make each agent an MCP-exposed service with explicit capabilities.
     - Implement shared long-term team memory (`knowledge/` structure).
     - Support evolutionary cycles, BDD/TDD, and DGX/Manolin deployment later.

2. `MIGRATION_STEPS.md`  
   A concrete, staged migration plan broken into **3–7 milestones**, for example:
   - Milestone 1: Introduce shared `knowledge/` layout and minimal Santiago-PM scaffold.
   - Milestone 2: Introduce Santiago-Ethicist scaffold and MCP manifests.
   - Milestone 3: Refactor coordinator/orchestrator around MCP-based agents.
   - Milestone 4+: Integration with DGX/Manolin-specific scripts, etc.

   Each milestone should include:
   - Goals
   - Affected directories/files
   - Specific tasks (can be expressed as checklists or BDD-style scenarios)

3. Optional but strongly encouraged:

   - `FOLDER_LAYOUT_PROPOSAL.md`  
     - Proposed directory structure for:
       - core NuSy / Santiago code
       - agents
       - MCP manifests
       - `knowledge/` (shared + per-domain)

   - Any **code scaffolding** that helps:
     - E.g., interface definitions, example MCP servers, role scaffolds, CLI stubs.
     - Place this under something like:
       - `ocean-arch-redux/arch-redux-<model_name>-plan/scaffolds/`

---

## Behavioral Requirements

- Do **NOT** modify or delete existing files outside of `ocean-arch-redux/` unless explicitly instructed later. This phase is **planning and scaffolding**, not wholesale rewriting.
- You may create **new** files and directories under:
  - `ocean-arch-redux/`
- Assume future agents and humans will read your plan, so clarity and structure matter.
- You should explicitly integrate the following concepts into your recommendations:
  - Santiago-PM as the central Product Manager agent with MCP-exposed capabilities.
  - Santiago-Ethicist as an early, always-on ethical reviewer.
  - Multi-agent structure (PM, Architect, 2–3 Developers, Ethicist, Hank as Captain).
  - Apprentice/Journeyman/Master skill levels.
  - Pond/Lake/Sea/Ocean knowledge scopes.
  - Shared memory in `knowledge/` plus ships logs.
  - DGX Spark / Manolin Cluster as eventual deployment target (even though we are “faking it” locally now).

---

## Task

1. **Read**:  
   - The current project structure and code in `nusy-product-team`.  
   - The research docs in `ocean-research/`.

2. **Analyze**:  
   - How the current implementation aligns or conflicts with the desired Santiago/NuSy/Manolin architecture.

3. **Produce** (in your own subfolder under `ocean-arch-redux/`):  
   - `ARCHITECTURE_PLAN.md`  
   - `MIGRATION_STEPS.md`  
   - Any optional supporting files you think will be helpful (folder layout proposals, code scaffolds, diagrams in Markdown/Mermaid, etc.).

Do not start modifying existing core code yet. Focus on **understanding, planning, and scaffolding**, so that future agents (including yourself in a later session) can safely execute the migration.