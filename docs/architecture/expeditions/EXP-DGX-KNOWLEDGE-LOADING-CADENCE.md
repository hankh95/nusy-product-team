## Expedition: DGX Knowledge Loading Cadence for BMJ Projects

**ID:** EXP-DGX-KNOWLEDGE-LOADING-CADENCE  
**Related Voyage:** VOY-001 BMJ Maiden Voyage (and future voyages)  
**Owner:** Santiago-Architect + Santiago-UX/PM  

---

### 1. Purpose

Determine how often and in what way to **reload the entire project knowledge** (BMJ codebase, content, specs, and metrics) into:

- NusY-Core (graph + 4-layer model), and/or
- a local DGX LLM “project brain”,

so that:

- agents and humans have near-immediate answers to project questions,
- reloads don’t unduly disrupt flow or blow budgets.

---

### 2. Questions to Answer

1. How frequently do we need full reloads to keep project knowledge “fresh enough” for day-to-day work?
2. What parts of the project should be loaded where (NusY-Core vs LLM vs both)?
3. What are the trade-offs between:
   - Load time & GPU cost,
   - freshness of knowledge,
   - impact on developer/agent flow?
4. How can we automate reloads and make them visible on Kanban/voyage dashboards?

---

### 3. Hypothesis

> There exists a reload cadence (e.g. every N cycles, or at specific voyage checkpoints) that keeps answers fresh for BMJ voyages while keeping DGX load overhead acceptable.

---

### 4. Plan (High-Level Cycles)

#### Cycle 1 – Map Knowledge Surfaces

- [ ] Identify which artifacts make up “the project” for BMJ:
  - BMJ pipeline code and configs,
  - BMJ domain content (topics, guidelines),
  - relevant ontologies/graphs,
  - key logs/metrics.
- [ ] Define what should live in:
  - NusY-Core graphs,
  - LLM context or retrieval store,
  - both.

#### Cycle 2 – Prototype Load & Query

- [ ] Implement or script a **full project load** into:
  - NusY-Core,
  - and/or a local DGX LLM (project brain).
- [ ] Run a set of representative queries:
  - “What is the current DGX BMJ architecture?”
  - “Where is [X] pipeline implemented?”
  - “What are the current bottlenecks and metrics?”
- [ ] Measure:
  - load time,
  - memory usage,
  - approximate usefulness (did we get correct and helpful answers?).

#### Cycle 3 – Cadence Experiment

- [ ] Try at least two different cadences:
  - e.g. reload at:
    - ALPHA/BETA/GAMMA checkpoints,
    - or after every N Kanban cards completed,
    - or nightly.
- [ ] Observe:
  - how often the project brain feels “stale”,
  - impact on DGX utilization,
  - interruptions to flow.
- [ ] Recommend:
  - a default cadence for BMJ voyages,
  - signals to trigger ad-hoc reloads (e.g., major refactor, big BMJ content ingestion).

---

### 5. Outputs

- A markdown note (e.g. `docs/architecture/expeditions/EXP-DGX-KNOWLEDGE-LOADING-CADENCE-REPORT.md`) summarizing:
  - load strategies,
  - attempted cadences,
  - recommendations.
- Updates to:
  - `DGX_READINESS_CHECKLIST.md` (knowledge loading section),
  - any automation scripts or configs used for reloads.

---

### 6. Kanban Usage

Create cards such as:

- “DGX Knowledge Loading – Map BMJ Project Surfaces”
- “DGX Knowledge Loading – Prototype Full Project Load”
- “DGX Knowledge Loading – Cadence Experiment & Recommendation”

Agents should:

- Work as far as they can per cycle,
- Log learnings and open questions in the report and card comments,
- Propose follow-up cards if new opportunities or risks appear.


