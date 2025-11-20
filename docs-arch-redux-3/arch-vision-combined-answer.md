## Santiago / NuSy Architecture – Combined DGX Runtime & Memory Model

**Location:** `docs-arch-redux-3/arch-vision-combined-answer.md`  
**Inputs:**  
- `docs-arch-redux-3/GROK41/arch-vision-grok41-answer-fabulous.md`  
- `docs-arch-redux-3/GPT51/arch-vision-gpt51-answer.md`  
- `docs-arch-redux-3/GROK41/arch-vision-grok41-answer.md`  

**Purpose:** Reconcile the three prior architecture answers into a single, opinionated set of recommendations that can drive updates to the main docs and implementation.

---

## 1. Comparison of the Three Answers

### 1.1 Strong Areas of Agreement

All three answers consistently assert that:

- **Always-on DGX runtime**
  - Santiago should run **continuously on the DGX** as an autonomous multi-agent crew.
  - There is no strict “turned off” state; the system loops forever through perception → planning → execution → evaluation.

- **Two work streams, one system**
  - There are always **two kinds of work**:
    - External/domain work (“at sea”) – building and operating domain experts.
    - Self-improvement work (“in the shipyard”) – improving Santiago-core, tools, memory, and agents.
  - These are best modeled as **lanes in a single Kanban system**, not as two separate runtimes.

- **In-memory Git + file-system-as-truth**
  - In-memory Git (e.g., `memory://santiago-workspace`) is the **runtime source of truth** for artifacts.
  - Kanban is a **projection over files**, not a separate database.
  - Periodic snapshots to persistent Git provide auditability and rollback.

- **Knowledge graphs as core memory**
  - Fast, graph-based memory underpins reasoning (domain knowledge, relationships, rules).
  - KGs are populated from files and used for both domain work and self-improvement.

- **Ethics & safety as first-class**
  - An Ethicist agent participates in planning and gating changes.
  - CI/CD + BDD/TDD + ethicist checks together form the safety envelope.

### 1.2 Main Differences / Tensions

The three answers diverge primarily on:

- **Memory model structure**
  - `arch-vision-grok41-answer-fabulous.md`:
    - Advocates **one unified in-memory Git + KG per Santiago instance**.
    - Self-improvement lives as just another project/folder/backlog inside that same hull.
  - `arch-vision-gpt51-answer.md` and `arch-vision-grok41-answer.md`:
    - Describe a **dual KG/Git model per Santiago**:
      - One for domain work.
      - One for self-improvement/meta-work.
    - Plus an additional shared “factory meta-KG”.

- **Doc shape and emphasis**
  - The “fabulous” answer:
    - Is more prescriptive about doc restructuring (`docs/RUNTIME_ARCHITECTURE.md`, archiving old ARCHITECTURE, etc.).
    - Emphasizes always-on DGX and single in-memory workspace as *the* canonical story.
  - The GPT51/Grok41 answers:
    - Provide more detailed phased refactor plans and component breakdowns.
    - Spend more time mapping from older docs and phases.

---

## 2. Canonical Architecture Decisions

This section resolves the disagreements and defines the **single canonical model** that future docs and code should follow.

### 2.1 DGX Runtime Model

- **Decision:**  
  Santiago runs as an **always-on autonomous crew on the DGX**.

- **Implications:**
  - No explicit “day vs night” runtime modes; instead:
    - Domain work and self-improvement work are **two Kanban work types**.
    - Santiago-PM + Ethicist continuously rebalance between them using flow, learning value, and ethics.
  - The DGX is simultaneously:
    - The **ship** (runtime where work happens).
    - The **shipyard** (place where self-improvement also happens).

### 2.2 In-Memory Git & Knowledge Graphs

- **Decision:**  
  Each running Santiago instance (core or domain expert) has **one primary in-memory Git workspace and one primary KG**, but within those we **logically separate domain vs self-improvement**.

- **Rationale / Reconciliation:**
  - From the “fabulous” answer:
    - Operational simplicity and clarity: “one hull” per Santiago is easier to reason about.
  - From GPT51/Grok41:
    - The need to distinguish domain vs self-improvement knowledge and history is real.
  - **Compromise model:**
    - **Physically**: one in-memory repo and one graph per Santiago instance.
    - **Logically**:
      - Clear namespaces / directories in Git:
        - `domain-knowledge/`, `domain-features/`, `domain-expeditions/`  
        - `self-improvement/`, `runtime-tools/`, `ethics/`
      - Clear subgraphs / labels in KG:
        - Nodes and edges tagged `scope=domain` vs `scope=self-improvement`.

- **Factory-level meta-knowledge:**
  - There is also a **shared factory/fleet repo and KG** that provide:
    - Reusable tackle modules.
    - Templates and patterns.
    - Cross-Santiago lessons.
  - Individual Santiagos mount or sync with this, but their **primary runtime decisions** are made in their own in-memory workspace.

### 2.3 Work Organization: Kanban, Files, and Experiments

- **Decision:**  
  Kanban remains the **single source of truth for work state**, backed by the file system and KGs.

- **Key properties:**
  - Boards and cards map directly to files and/or KG nodes.
  - Domain vs self-improvement work are surfaced as:
    - Lanes or tags (`type=domain`, `type=self-improvement`, `type=runtime`).
  - Kanban views (markdown like `kanban-boards.md`) are **generated**, never hand-edited.

### 2.4 Safety, Ethics, and CI/CD

- **Decision:**  
  The Ethicist is wired into:
  - Kanban prioritization.
  - Commit/merge gates in CI/CD.
  - Rollback decisions, using snapshots of the in-memory repo.

- **Practical implications:**
  - Every high-impact change path:
    - Kanban → Git branch → tests (BDD/TDD) → ethicist gate → merge or rollback.
  - Ethics constraints are:
    - Expressed as policies/tests.
    - Versioned and auditable in Git.

---

## 3. Recommended Doc Structure (Unified)

This section unifies the doc recommendations from all three answers into a **single doc plan**.

### 3.1 Vision vs Architecture vs Plan

- **Vision (future truth):**
  - Keep `docs-arch-redux-3/GPT51/arch-vision-gpt51.md` as the **primary north star**.
  - Keep the two answer files as **interpretations**:
    - `arch-vision-grok41-answer-fabulous.md` (highly opinionated, concise).
    - `arch-vision-gpt51-answer.md` (more detailed architecture/plan).
  - Add a small header to these:
    - “Status: Vision / Future Truth – implementation may lag this document.”

- **Architecture (current + target):**
  - Introduce two docs under `docs/`:
    - `docs/TARGET_ARCHITECTURE.md`  
      - Use the **canonical decisions** in section 2 above.
      - Organize into:
        - Overview.
        - DGX Runtime Model.
        - In-Memory Git & KG Model.
        - Work Organization (Kanban, files, experiments).
        - Safety/Ethics & CI/CD.
    - `docs/RUNTIME_ARCHITECTURE_ON_DGX.md` (optional, focused)  
      - Shorter operational version of the DGX runtime portions for implementers.
  - Treat existing `ARCHITECTURE.md` at repo root as:
    - `docs/LEGACY_ARCHITECTURE.md` (archive).
    - Leave a small pointer file `ARCHITECTURE.md` that says:
      - “See `docs/TARGET_ARCHITECTURE.md` for current architecture.”

- **Plans:**
  - Keep:
    - Root `DEVELOPMENT_PLAN.md` as **short-term / Kanban-first view**.
    - `santiago-pm/navigation-charts/santiago-development-master-plan.md` as **strategic multi-phase roadmap**.
  - Add:
    - `docs/REFACTOR_PLAN.md` to:
      - Bridge from current state to target architecture.
      - Consolidate the phased plans from the three answers into one concise sequence (see 4. below).

### 3.2 History & Influences

- Create `docs/History-And-Influences.md` to:
  - Summarize older artifacts like:
    - `SANTIAGO-ARCHITECTURE-SCENARIOS.md`.
    - Earlier strategic charts and prototypes.
  - Explicitly mark them as:
    - “Historical / Background – not active source of truth. Superseded by TARGET_ARCHITECTURE.md.”

---

## 4. Unified Refactor / Implementation Plan (High-Level)

Rather than maintaining multiple slightly different phase lists, use this **consolidated sequence** as the spine of `docs/REFACTOR_PLAN.md`:

- **Phase 1 – DGX-Native Always-On Runtime**
  - Stand up a stable, always-on Santiago runtime on DGX.
  - Wire agents to an in-memory Git + KG workspace (`memory://santiago-workspace`).
  - Validate a full loop:
    - Kanban card → agent work → branch → tests → merge.

- **Phase 2 – Unified In-Memory Git + Logical Domain/Self Separation**
  - Ensure each Santiago instance has **one in-memory repo & KG**, with:
    - Clear directory/graph separation of `domain` vs `self-improvement`.
  - Connect Kanban tags/lanes to those scopes.

- **Phase 3 – Ethicist-Gated CI/CD & Experiment Loop**
  - Integrate Ethicist into:
    - Commit/merge pipelines.
    - High-risk Kanban transitions.
  - Encode self-improvement experiments as:
    - Explicit cards + branches + BDD suites.

- **Phase 4 – Fleet-Level Tackle & Meta-KG**
  - Implement the shared factory/fleet repo and meta-KG:
    - Templates, tackle, reusable tools.
  - Wire Santiagos to mount/replicate these.

- **Phase 5 – Full Self-Improvement Autonomy**
  - Target state:
    - Crew autonomously chooses between domain and self-improvement work.
    - Memory architecture (snapshots, rollbacks, analysis) is operational.
    - Docs and plans are aligned with this combined model.

This plan captures the spirit of all three earlier answers while avoiding duplication and contradictions.

---

## 5. How to Use This Combined Answer

- Treat this file (`arch-vision-combined-answer.md`) as the **arbiter when the three earlier answers disagree**.
- When updating docs or implementation:
  - Prefer the **decisions in section 2** over earlier variants (e.g., single physical repo+KG per Santiago with logical separation).
  - Use section 3 as the guide for **doc reorganization**.
  - Use section 4 as the **high-level refactor roadmap**, then refine into Kanban cards and expeditions.

Over time, as `docs/TARGET_ARCHITECTURE.md` and `docs/REFACTOR_PLAN.md` are implemented and stabilized, this combined answer can be treated as historical background in the same way as the earlier per-model answers.


