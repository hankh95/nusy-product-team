## Santiago Architecture Redux 3 – Migration Plan

**Purpose:** Define how to evolve the current repository and runtime into the target architecture described in `arch-vision-merged-plan.md`, with clear folder moves, code refactors, Kanban changes, and glossary updates.

---

## 1. Repo Folder Migration Plan

### 1.1 Goals

- Align the on-disk folder structure with:
  - The **two-namespace model** (`domain/*` vs `self-improvement/*`) per Santiago-domain repo.
  - The **canonical self-improvement scaffold** based on `santiago-pm/`.
- Preserve history and provenance (archive, don’t delete, unless explicitly approved).

### 1.2 Top-Level Mapping (High-Level)

This table is intentionally high-level; detailed per-folder actions will be captured as Kanban tasks.

- **`santiago-pm/`** → Target: **canonical self-improvement scaffold** for the PM domain
  - Action: Keep as-is structurally, but:
    - Update `santiago-pm/tackle/folder-structure.md` to show how this structure appears under `self-improvement/` for future `santiago-<domain>` repos.
    - Use this as the template for self-improvement in other domains.

- **`santiago_core/`** → Target: core runtime services and agents
  - Action: Keep; clarify roles:
    - `agents/` – proxies + real agents.
    - `services/` – core services (Kanban, KG, etc.).
    - (Future) `knowledge/` – core KG location.

- **`expeditions/`** → Target: experimental / research-only
  - Action: Mark as experimental:
    - Do **not** treat as production code.
    - For pieces we want (e.g. Dulwich Git, in-memory LLM), create explicit migration tasks to bring them into `santiago_core/` or shared libraries with tests and CI.

- **`src/nusy_pm_core/`** → Target: legacy reference
  - Action: Treat as reference:
    - Do not expand; only pull patterns forward as needed.

Additional mappings (e.g. `knowledge/`, `nusy_orchestrator/`) will be fleshed out in later passes and tracked via Kanban.

### 1.3 Root Artifact Triage (Planned)

There are several **root-level artifacts** (files and folders directly under the repo root) that need to be assigned to either:

- `santiago_core/` (core, cross-domain).
- `santiago-pm/` or future `santiago-<domain>/` (domain-specific).
- `knowledge/` (factory/fleet-level knowledge).
- `_archive/` / `zarchive/` (historical only).

Examples (non-exhaustive):

- Root-level **features**: `features/*.feature` (currently global).
- Root-level **expeditions**: `expeditions/exp_0xx/*` (core/factory-level experiments).
- Root-level **research logs**: `research-logs/*.md` (cross-cutting architecture/memory work).
- Standalone root docs: `Epub-books-feature-memory.md`, `NuSy–Santiago-Architecture-Discussion-Grok-4-1.md`, `factory-activity-log.md`, etc.
- Root-level **knowledge**: `knowledge-graph/`, `knowledge/*` (factory/fleet-level).

Planned actions (to be implemented via Kanban tasks, not done automatically):

1. **Generate a triage report** listing each root-level artifact and a **proposed target home**:
   - `santiago_core/…`, `santiago-pm/…`, `knowledge/…`, or `_archive/…`.
2. **Review triage with Hank (Captain)**:
   - Confirm or adjust target locations.
   - Mark any ambiguous items for manual follow-up.
3. **Apply moves in small, reviewed PRs**:
   - Update references where necessary.
   - Preserve history and provenance (no destructive deletes without explicit approval).

### 1.4 PM Feature vs BDD File Cleanup (Planned)

There is currently a mix of **feature specifications** and **BDD `.feature` files** under `santiago-pm/cargo-manifests/`:

- Example **feature spec (doc)**: `santiago-pm/cargo-manifests/continuous-backlog-discovery.md`.
- Example **expedition spec (doc)**: `santiago-pm/expeditions/autonomous-multi-agent-swarm/autonomous-multi-agent-swarm.md`.
- Example **BDD test files**: various `*.feature` files living in `santiago-pm/cargo-manifests/`.

Planned actions:

1. Define a clear separation between:
   - **Feature/expedition specs** (markdown) that describe desired behavior.
   - **BDD test assets** (`*.feature`) that live alongside tests or in a dedicated test folder.
2. Inventory all `*.feature` files in `santiago-pm/cargo-manifests/` and propose target homes:
   - E.g. move under a `tests/` or `bdd-tests/` subtree referenced from the specs.
3. Update `santiago-pm/tackle/folder-structure.md` and relevant docs to:
   - Document where feature specs live vs where BDD tests live.
4. Apply moves via small PRs, ensuring:
   - CI still finds and runs the BDD tests.
   - Links from specs to tests remain valid.

---

## 2. Code Migration & Refactor Plan

### 2.1 Production vs Experimental Code

- **Production code (keep, integrate, harden):**
  - `santiago_core/` – agent & service implementations.
  - `santiago-pm/tackle/` – Kanban + PM tools.
  - `src/nusy_pm_core/` – core adapters and libraries (selectively).

- **Experimental code (expeditions, research):**
  - `expeditions/exp_036/` – enhanced shared memory Git & in-memory LLM.
  - `expeditions/exp_040/` – Dulwich in-memory Git service.
  - Other `expeditions/exp_*` – research trials.

### 2.2 Migration Principles

- Do not move/delete code directly from expeditions into production folders.
- Instead:
  - Create **new production modules** under `santiago_core/` or shared libs.
  - Port patterns from expeditions, with:
    - Tests.
    - Docs.
    - CI integration.
  - Mark expeditions as historical/experimental.

---

## 3. Kanban Reprioritization Plan

### 3.1 New Epic: Architecture Redux 3

Create a new epic/expedition in `santiago-pm/cargo-manifests/`:

- `EXP-056: Architecture Redux 3 – Target Runtime & Repo Alignment`

Sub-areas under this epic:

1. **Docs Alignment**
   - Align `ARCHITECTURE.md` and related docs with `arch-vision-merged-plan.md`.
2. **Folder & Code Migration**
   - Implement the two-namespace (`domain/*` and `self-improvement/*`) model per Santiago-domain repo.
3. **Runtime/CI/CD Hardening**
   - Ensure DGX runtime and CI/CD reflect the merged architecture.
4. **Glossary & Semantics**
   - Update glossary and semantic definitions to match the new model.

### 3.2 Example Kanban Tasks (to be created)

- “Update `santiago-pm/tackle/folder-structure.md` to show `self-improvement/` nesting pattern.”
- “Mark `expeditions/exp_036/*` and `expeditions/exp_040/*` as experimental in docs and Kanban.”
- “Draft `docs/ARCHITECTURE/arch-vision-merged-plan.md` pointer and archive old bootstrap docs.”

---

## 4. Glossary Upgrade Plan

### 4.1 Goals

- Make sure `GLOSSARY.md` and `arch-vision-merged-plan.md` use:
  - Consistent names for **Noesis**, **Santiago**, **workspace**, **DGX runtime**, **in-memory Git**, **KG**, and **memory types**.
  - Clear definitions of **domain work**, **self-improvement work**, and **Hank’s captain role**.

### 4.2 Actions

- Extend `GLOSSARY.md` with:
  - Runtime & Memory section:
    - DGX runtime, Noesis, Santiago-core, in-memory Git, KG, working/episodic/semantic memory.
  - Work types:
    - Domain vs self-improvement.
  - Human roles:
    - Hank as Captain / Vision Holder (global weights and constraints).

- Add a short “Glossary of Core Runtime Terms” section near the top of `arch-vision-merged-plan.md` that references `GLOSSARY.md` as canonical.

---

## 5. Next Steps (High-Level)

1. **Review & refine this migration plan** (you + AI, section by section).
2. **Create the Architecture Redux 3 epic and initial Kanban cards** under `santiago-pm/cargo-manifests/`.
3. **Align docs**:
   - Add pointer from `docs/ARCHITECTURE.md` (or new `docs/ARCHITECTURE/arch-vision-merged-plan.md`) to `arch-vision-merged-plan.md`.
   - Mark older docs as historical.
4. **Implement low-risk migrations first**:
   - Folder-structure docs.
   - Glossary updates.
   - Non-destructive code organization.
5. **Only then** move to structural code moves and DGX runtime changes, with CI/CD and ethical gates in place.


