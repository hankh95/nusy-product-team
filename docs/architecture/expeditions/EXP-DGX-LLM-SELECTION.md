# Expedition: DGX LLM Selection for BMJ & Santiago-Doctor-BMJ

**ID:** EXP-DGX-LLM-SELECTION  
**Related Voyage:** VOY-001 BMJ Maiden Voyage  
**Owner:** Santiago-Architect (with Captain Hank)  

---

## 1. Purpose

Determine a recommended pair of LLMs to run on the DGX for BMJ work:

- A **reasoning model** (for complex clinical/graph reasoning).
- A **worker/memory model** (for bulk extraction, summarization, and knowledge loading).

The goal is to balance:

- reasoning quality,
- ability to load BMJ + semantic web knowledge,
- runtime characteristics on DGX,
- developer ergonomics.

---

## 2. Questions to Answer

1. Which candidate models are realistic for DGX (size, licensing, infra)?
2. How easy is it to load BMJ content and related ontologies into each?
3. Are there small but strong reasoning models that fit well into the workflow?
4. How do the models perform on a small set of BMJ‑like tasks (e.g. extracting logic, time, sequence)?

---

## 3. Hypothesis

> There exists a small set of open or DGX‑deployable models (e.g. Mistral, Qwen, Llama variants) that can provide strong reasoning and efficient knowledge loading for BMJ, allowing us to replace remote API calls without degrading quality.

---

## 4. Plan (High-Level Cycles)

### Cycle 1 – Landscape & Shortlist

- [ ] Identify 3–5 candidate LLMs available for DGX deployment.
- [ ] Capture:
  - [ ] model sizes, licenses, and hardware requirements,
  - [ ] support for long context windows,
  - [ ] tooling support (vLLM, Triton, etc.).
- [ ] Produce a **shortlist** (e.g. 2–3 top contenders).

### Cycle 2 – Knowledge Loading & Basic Tasks

- [ ] For each shortlisted model:
  - [ ] Load a small BMJ‑like knowledge slice and relevant ontologies.
  - [ ] Run a tiny set of representative tasks:
    - [ ] extract key facts,
    - [ ] reason about time and sequence,
    - [ ] interpret a small guideline‐like passage.
- [ ] Capture:
  - [ ] qualitative results,
  - [ ] rough latency and resource usage.

### Cycle 3 – Recommendation

- [ ] Compare models on:
  - [ ] reasoning quality,
  - [ ] ease of knowledge loading,
  - [ ] DGX runtime behavior,
  - [ ] fit with existing code & stack.
- [ ] Recommend:
  - [ ] a default **reasoner** model,
  - [ ] a default **worker/memory** model,
  - [ ] and any “do not use” candidates with rationale.

---

## 5. Outputs

- Short markdown report (e.g. `docs/architecture/dgx-llm-selection-report.md`) summarizing:
  - candidates, experiments, and the chosen model pair.
- Updates to:
  - `DGX_READINESS_CHECKLIST.md` (model section),
  - DGX voyage manifest if necessary.

---

## 6. Kanban Usage

- Create one or more cards (e.g. on the DGX voyage board) pointing to this expedition:
  - “DGX LLM Selection – Landscape & Shortlist”
  - “DGX LLM Selection – Knowledge Loading Experiment”
  - “DGX LLM Selection – Final Recommendation”
- Agents should:
  - work as far as they can per cycle,
  - record open questions/blocked points in the report and card comments.


