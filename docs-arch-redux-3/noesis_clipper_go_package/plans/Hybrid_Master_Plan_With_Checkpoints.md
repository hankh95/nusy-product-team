# Hybrid Master Plan – BMJ Delivery + Santiago-Doctor-BMJ

This document coordinates:

- **Option 1:** BMJ Delivery Accelerator (21 hours / 3 days per week)
- **Option 2:** Santiago-Doctor-BMJ Domain Expert (≈96 hours / 4 days per week, largely autonomous)

and defines decision checkpoints where you may shift BMJ-focused time to the clearly superior approach.

## 1. Weekly Rhythm

- **Thu–Sun:** Option 2
  - Santiago-Doctor-BMJ experiments
  - platform improvement
  - DGX orchestration tuning

- **Sun night + Mon–Wed:** Option 1
  - BMJ pipeline improvements and deliveries
  - focus on framed files, graph completeness, and FHIR-capable logic
  - always informed by Option 2 learnings

## 2. Checkpoints

### 2.1 Checkpoint ALPHA – End of Week 1

Questions:

- Is the BMJ repo running stably on DGX via `run_bmj_pipeline.sh`?
- Is the first Santiago-Doctor-BMJ pipeline able to complete at least one topic end-to-end, even if rough?
- Did Option 2 uncover obvious improvements that Option 1 can apply immediately (e.g., better extraction prompts)?

Decision:

- Proceed with Option 1 work next Mon–Wed as planned.
- If BMJ pipeline is unstable, spend part of Option 1 time stabilising wrappers and LLM integration first.

---

### 2.2 Checkpoint BETA – End of Weeks 2–3

Compare, for one or more topics:

- Framed file completeness
- Coverage of logic, time, and sequence
- FHIR-capable structure readiness
- Cycle time per topic
- DGX resource usage
- Engineering sanity (how hard is each pipeline to improve?)

Decision:

- Continue both streams as is.
- OR shift a bit more of your personal time to Option 2 if it is clearly the scalable path.
- Keep BMJ days focused on the approach (Option 1 or 2) that best serves BMJ’s near-term needs.

---

### 2.3 Checkpoint GAMMA – End of 4 Weeks

Evaluate:

- Which engine (BMJ pipeline vs Santiago-Doctor-BMJ) is:
  - producing better graphs and logic
  - easier to extend to FHIR CR
  - faster to run on DGX
  - more maintainable for the next 8 months and 1,050 topics

Decision:

- For your **BMJ-focused 21 hours per week**, choose to:
  - primarily use the improved BMJ pipeline (Option 1), OR
  - primarily use the Santiago-Doctor-BMJ pipeline (Option 2), OR
  - use a merged pipeline that combines the best of both.

Option 2 (Santiago-native) may become the primary path if it clearly outperforms Option 1.

## 3. Switching Rule

At each checkpoint, the guiding principle is:

> “For BMJ’s 21 hours/week of work, always choose the approach that maximally speeds up delivery of a high-quality, logic-complete, FHIR-capable graph for 1,050 topics.”

Platform work (Option 2) continues to evolve irrespective of which engine is used on BMJ days, but BMJ days should be aligned with the clear winner.
