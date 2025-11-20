## Migration Plan Architecture Review – EXP-057 `exp-057-architecture-redux-3-migration`

**Date:** 2025-11-20  
**Reviewer:** Architecture Agent (acting on behalf of Captain Hank)  

---

## 1. Overview & Scope

This document reviews the current state of the **Architecture Redux 3** migration on branch `exp-057-architecture-redux-3-migration` and provides **concrete decisions and next-step work packages**.

Inputs:

- `docs/architecture/architecture-review-guide.md`
- `docs/architecture/expedition-analysis-work-outline.md`
- Current repo structure (two-namespace model: `domain/` + `self-improvement/`)

Goals:

- Confirm/adjust the two-namespace model.
- Resolve key architecture questions (imports, tests, ownership, legacy code, kanban).
- Prioritize remaining migration work (Phase 2–4) with clear success criteria.

---

## 2. Current State Summary

### 2.1 Two-Namespace Architecture

Per `architecture-review-guide.md` and `expedition-analysis-work-outline.md`, the repository now follows a two-namespace pattern:

- **`domain/`** – Production code and demos:
  - `domain/src/nusy_pm_core/` – Core PM domain logic and expert CLI.
  - `domain/examples/` and `domain/scripts/` – Demos and utility scripts.
  - `domain/domain-features/`, `domain/domain-knowledge/` – Domain artifacts.
- **`self-improvement/`** – Autonomous improvement tools:
  - `self-improvement/santiago-pm/` – Canonical PM scaffold (tackle, cargo-manifests, voyages, etc.).
  - `self-improvement/santiago-dev/` – Autonomous workspace and continuous service.

Legacy and research:

- `santiago_core/` – Legacy core implementation (reference, not fully integrated).
- `expeditions/` – Historical expedition code and notes.
- `_archive/` – Archived legacy code/docs.

### 2.2 Validated Components

From `architecture-review-guide.md`:

- ✅ **KG Store** (`domain/src/nusy_pm_core/adapters/kg_store.py`)
  - Loads ~3,300 triples.
  - SPARQL-capable, provenance tracking.
- ✅ **Santiago Expert CLI** (`domain/src/nusy_pm_core/santiago_expert_cli.py`)
  - Neurosymbolic reasoning, ~82.5% confidence on PM tools.
- ✅ **Kanban System** (`self-improvement/santiago-pm/tackle/kanban/`)
  - Unified board model, CLI, markdown generation, regenerator polling at 10s.
- ✅ **Self-aware Demo** (`domain/scripts/demo_santiago_pm_self_aware.py`)
  - Demonstrates bootstrap + MCP manifest, KG integration.

### 2.3 Outstanding Issues

From both guides:

- **Self-improvement imports**:
  - Tools under `self-improvement/` sometimes fail with `No module named 'self_improvement'`.
  - sys.path/package structure not yet standardized.
- **Legacy `santiago_core/`**:
  - Contains substantial code not yet reconciled with the new structure.
- **Missing/partial components**:
  - Some tests reference `agent_adapter`, `experiment_runner` not yet implemented in the new layout.
- **Tests & expeditions**:
  - Tests are not yet fully co-located with their target code.
  - Expedition artifacts are not standardized.

---

## 3. Architecture Decisions

### 3.1 Import and Namespace Strategy

**Decision 1: Use absolute imports from the repository root for both `domain` and `self-improvement`.**

- **Rationale**:
  - Consistency across the codebase.
  - Easier mental model for agents and humans.
  - Aligns with patterns already validated in `domain/` (per `architecture-review-guide.md`).
- **Implications**:
  - All production imports should follow patterns like:
    - `from domain.src.nusy_pm_core.adapters.kg_store import KGStore`
    - `from self_improvement.santiago_pm.tackle.kanban.kanban_service import KanbanService`
  - Self-improvement scripts must set `PYTHONPATH` or package structure to support this.

**Decision 2: Introduce minimal `__init__.py` files to treat `domain` and `self_improvement` as packages.**

- This supports standard import resolution without heavy packaging.

### 3.2 Component Ownership

**Decision 3: Autonomous agent services are split by responsibility:**

- **Production-facing services** (APIs, CLIs, KG adapters):
  - Live in `domain/src/nusy_pm_core/` and subpackages.
- **Autonomous improvement/services** (experiment runners, Kanban regeneration, auto-refactors):
  - Live in `self-improvement/santiago-pm/` and `self-improvement/santiago-dev/`.

This keeps the **runtime “ship”** (Noesis executing production features) under `domain/`, and the **shipyard tools** under `self-improvement/`.

### 3.3 Legacy Code Disposition (`santiago_core/`)

**Decision 4: Treat `santiago_core/` as legacy reference and selectively migrate value.**

- Actions:
  - Mark `santiago_core/` as **legacy** in docs; move detailed legacy guides to `_archive/legacy-docs/`.
  - Identify valuable components (e.g., some agents/services) and:
    - Either migrate to `domain/src/` or `self-improvement/santiago-*/`.
    - Or leave as documented historical reference if superseded.
- No blind deletion; all removals must be gated via:
  - CI/CD.
  - Ethicist + Hank approval for destructive actions (as per cleanup features).

### 3.4 Kanban Integration

**Decision 5: Kanban core lives in self-improvement (`self-improvement/santiago-pm`), with domain code importing it.**

- Rationale:
  - Kanban is primarily a **self-improvement and coordination tool**, but domain need to read/write board state.
- Implementation:
  - Keep `santiago-pm/tackle/kanban/` under self-improvement.
  - Domain scripts import services via absolute imports from `self_improvement.santiago_pm...`.
  - Do **not** duplicate Kanban code under `domain/`; maintain a single implementation.

---

## 4. Test & Expedition Strategy

### 4.1 Test Distribution

**Decision 6: Co-locate tests with code, using namespaced test roots:**

- `domain/tests/` for production code tests.
- `self-improvement/santiago-pm/tests/`, `self-improvement/santiago-dev/tests/` for self-improvement tests.
- Cross-namespace integration tests can live under a dedicated `tests/integration/` or `domain/tests/integration/` with clear naming.

### 4.2 Expedition Artifacts

**Decision 7: Standardize expedition artifact layout under `expeditions/exp_XXX/`.**

- Adopt the template proposed in `architecture-review-guide.md`:

```text
expeditions/exp_057/
├── README.md                 # overview
├── captain-decisions-log.md  # Hank's decisions
├── phase2-progress-log.md    # progress snapshots
├── triage-report.md          # root artifact & risk triage
├── code/                     # scripts
├── results/                  # outputs, logs
└── analysis/                 # lessons learned
```

- Future expeditions should follow this pattern to ease review and provenance tracking.

---

## 5. Prioritized Work Packages (Next Steps)

Based on `architecture-review-guide.md` and `expedition-analysis-work-outline.md`, as well as the decisions above, here is the prioritized work:

### 5.1 High Priority (Before Any Broad Refactor)

1. **Self-Improvement Import Fixes**
   - Standardize imports to absolute from repo root.
   - Ensure `self_improvement` package is importable (add `__init__.py`, adjust `PYTHONPATH` for scripts).
   - Validate:
     - Kanban workflow demos.
     - Experiment runners and quality assessments.

2. **Missing Components Resolution**
   - For references like `agent_adapter` and `experiment_runner`:
     - Implement minimal versions in `domain/src/` or `self-improvement/` as appropriate; or
     - Mark tests as legacy and move them to `_archive/tests/` if not part of target arch.
   - CI must be green after changes.

### 5.2 Medium Priority (Architecture Cleanup)

3. **Legacy `santiago_core/` Audit & Disposition**
   - Inventory modules in `santiago_core/`.
   - Classify: migrate vs archive vs leave as reference.
   - Update docs to clearly mark legacy status and new home for any migrated pieces.

4. **Expedition Artifact Standardization**
   - Apply the new expedition folder template to:
     - `expeditions/exp_032`–`exp_041`, and `exp_057`.
   - Create at least:
     - `README.md`, `captain-decisions-log.md`, and `results/` for each.

### 5.3 Lower Priority (Polish & Validation)

5. **Test Co-location & Discovery**
   - Move tests into the appropriate `domain/tests/` or `self-improvement/.../tests/` directories.
   - Update any test runner configuration to match new locations.

6. **End-to-End Validation Scripts**
   - Implement scripts that:
     - Run core flows across `domain` & `self-improvement`.
     - Validate DGX runtime behavior (always-on loop, Kanban, KG interaction).

---

## 6. Timeline & Effort Estimates

Using the outlines in the existing docs as a baseline:

- **High Priority**:
  - Self-improvement import fixes: **2–4 hours**
  - Missing components resolution: **4–6 hours**
- **Medium Priority**:
  - `santiago_core/` audit & disposition: **2–3 hours**
  - Expedition artifact standardization: **1–2 hours**
- **Lower Priority**:
  - Test co-location: **4–6 hours**
  - End-to-end validation scripts: **3–4 hours**

**Total estimate**: ~16–25 hours, depending on how many legacy edges are uncovered.

---

## 7. Success Criteria

**Architecture Redux 3 & EXP-057 are considered successful when:**

1. **Imports & Namespaces**
   - All modules under `domain/` and `self-improvement/` import cleanly using absolute imports.
   - No `No module named 'self_improvement'` or equivalent import errors in CI.

2. **Legacy Code**
   - `santiago_core/` is clearly marked as legacy or selectively migrated.
   - No active code paths depend on ambiguous or undocumented legacy modules.

3. **Kanban & Self-Improvement**
   - Kanban system works from its canonical home in `self-improvement/santiago-pm/`.
   - Domain scripts can interact with Kanban via well-defined imports.

4. **Tests**
   - All critical tests pass (unit, integration, key BDD).
   - Tests are co-located or clearly mapped to code.

5. **Expeditions & Docs**
   - Expedition records are standardized and discoverable.
   - `docs/architecture/` and related docs point unambiguously to the target architecture.

When these conditions are met, the repository will be ready for Phase 4 work (runtime validation, scaling up multi-domain, and deeper KnowledgeOps integration).  


