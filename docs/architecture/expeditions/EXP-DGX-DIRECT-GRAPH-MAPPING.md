## Expedition: Direct Graph Mapping to BMJ Spec (Skip 4L Tagging)

**ID:** EXP-DGX-DIRECT-GRAPH-MAPPING  
**Related Voyage:** VOY-001 BMJ Maiden Voyage (and successors)  
**Owner:** Santiago-Architect + Santiago-Dev/Research  

---

### 1. Purpose

Test the hypothesis that we can **map BMJ content directly to BMJ's graph specification** (or another partner's spec) without going through the full 4-layer tagging pipeline, by:

- loading the spec and content into the NuSy brain,
- learning or generating a new “Bigfish” model or mapping layer,
- and comparing results to the existing 4L → spec conversion.

---

### 2. Questions to Answer

1. Is it technically feasible to learn or specify a direct mapping from BMJ content → BMJ graph spec?
2. How does direct mapping quality compare to:
   - 4L tagging + downstream conversion?
3. What are the trade-offs in:
   - implementation effort,
   - explainability / maintainability,
   - performance on DGX?

---

### 3. Hypothesis

> By loading BMJ's graph spec and content into the NuSy brain, we can define a direct mapping (via “Bigfish” or equivalent) that yields equal or better graphs than our current 4-layer tagging pipeline, with lower complexity in some contexts.

---

### 4. Plan (High-Level Cycles)

#### Cycle 1 – Spec & Content Understanding

- [ ] Collect:
  - [ ] BMJ graph schema/spec (or representative subset).
  - [ ] Sample BMJ content and any current graph outputs.
- [ ] Document:
  - [ ] key entities, relationships, and constraints in the BMJ spec,
  - [ ] how current 4L outputs map to that spec.

#### Cycle 2 – Prototype Direct Mapping on a Tiny Slice

- [ ] Design an initial direct mapping approach:
  - explicit mapping rules,
  - small ML/LLM-based mapping using prompts,
  - or a hybrid.
- [ ] Implement a prototype that:
  - takes a small BMJ content slice,
  - produces BMJ-graph-spec-shaped output directly (no 4L intermediary).
- [ ] Compare:
  - coverage,
  - correctness,
  - effort required vs 4L → spec path.

#### Cycle 3 – Evaluate & Recommend

- [ ] Evaluate:
  - maintainability of direct mapping rules/models,
  - how easy it is to adapt to new BMJ topics,
  - where direct mapping fits vs 4L in the architecture.
- [ ] Produce a recommendation:
  - when to use direct mapping,
  - when 4L is still better,
  - any changes needed in Bigfish or mapping libraries.

---

### 5. Outputs

- A short report (e.g. `docs/architecture/expeditions/EXP-DGX-DIRECT-GRAPH-MAPPING-REPORT.md`) describing:
  - the mapping approach,
  - prototype results,
  - trade-offs and recommendations.
- Potential updates to:
  - domain features related to graph generation,
  - mapping libraries or Bigfish components.

---

### 6. Kanban Usage

Create cards such as:

- “Direct Graph Mapping – Understand BMJ Spec & 4L Mapping”
- “Direct Graph Mapping – Tiny Slice Prototype”
- “Direct Graph Mapping – Evaluation & Recommendations”

Agents should:

- Work iteratively through cycles,
- Use Definition of Done from `CONTRIBUTING.md`,
- Log discoveries and open questions in the report and card comments.


