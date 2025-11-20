You are an expert software and systems architect with full repo-wide reasoning.

## Task
Analyze architecture-related files across the repo, especially:

- `docs-arch-redux-3/GPT51/arch-vision-gpt51-answer.md`  (use as the base)
- `docs-arch-redux-3/GROK41/arch-vision-grok41-answer-fabulous.md`
- `docs-arch-redux-3/arch-vision-combined-answer.md`
- `docs/vision/00-ARCHITECTURE-PATTERN.md`
- `docs/FOLDER_LAYOUT.md`
- `docs/RELEVANCE_MAP.md`
- `SANTIAGO-ARCHITECTURE-SCENARIOS.md` (historical background)
- any other architecture, agent, KG, or workflow files in the repo that materially affect the design

Treat the three arch-vision answer files as **primary** sources and the others as supporting/background unless they clearly resolve conflicts.

Then create a **new unified architecture file**:

`docs/ARCHITECTURE/arch-vision-merged-plan.md`

(If `docs/ARCHITECTURE/` does not exist yet, conceptually target that path in your structure and refer to it consistently.)

## Constraints and Assumptions

- **Always-on DGX runtime model**
  - Santiago runs 24/7 on DGX.
  - Domain work and self-improvement work are two Kanban work types/lanes executed within the same runtime, not separate runtimes.

- **One physical in-memory Git + KG per Santiago**
  - Each Santiago instance (core or domain expert) has **one primary in-memory Git workspace and one primary KG**.
  - Within that workspace/graph, domain vs self-improvement are separated **logically**:
    - By directories/namespaces in Git (e.g., `domain-*` vs `self-*`).
    - By labels/namespaces in the KG (e.g., `scope=domain` vs `scope=self-improvement`).
  - There is also a shared factory/fleet repo + meta-KG providing reusable tackle and patterns, but your job is to **document and sharpen this model, not to change it.**

- Your job is to **clarify and document** these choices and integrate them consistently across the architecture; do not re-open them as design options.

## Requirements
1. Use the GPT‑5.1 plan (`docs-arch-redux-3/GPT51/arch-vision-gpt51-answer.md`) as the structural and narrative base.
2. Pull improvements from:
   - the Grok 4.1 plan (`docs-arch-redux-3/GROK41/arch-vision-grok41-answer-fabulous.md`)
   - the combined plan (`docs-arch-redux-3/arch-vision-combined-answer.md`)
   - any additional architecture-relevant files discovered via repo search
3. Integrate repo patterns, folder structures, agent roles, and KGs as defined in code/docs (especially `docs/FOLDER_LAYOUT.md`, `docs/RELEVANCE_MAP.md`, and `santiago-pm/tackle/folder-structure.md` if present).
4. Resolve unclear roles and relationships using information found across the repo.
5. Clarify and make explicit:
   - KG multiplicity (shared vs per-agent, and how domain vs self-improvement namespaces are modeled).
   - Self-improvement pipelines and experiment loops.
   - DGX execution model (always-on loop, Kanban work types).
   - Agent lifecycle (how “at sea” vs “shipyard” are expressed in Kanban/runtime, not as separate runtimes).
   - Operational architecture (CI/CD, eval harness, rollback, and ethical gating).
6. Produce a single, clean markdown file with sections in **this exact order**:
   1. Vision & Conceptual Architecture
   2. Runtime Architecture on DGX
   3. Knowledge Graph & Memory Model
   4. Agents & Roles
   5. Reference Implementation Architecture (folders, services, flows)
   6. Operational Architecture (CI/CD, eval, rollback, ethics)
   7. Change Log (Sources of Ideas)
7. Include at least one Mermaid diagram for:
   - the DGX runtime / in-memory Git + KG + Kanban loop, and
   - the agent / KG / memory interactions.
8. Add a final section:
   `## Change Log (Sources of Ideas)`
   listing where each major addition came from (by file and, where useful, by line range or concept).

## Style
- Clear, consistent voice.
- No duplicated or conflicting passages.
- Visionary but implementable.
- Based on full-repo reasoning.
- Target a concise but substantial document (roughly 6–10 major sections as above, not an unstructured stream).

Now search the repo and begin synthesis when ready.