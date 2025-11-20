## Expedition: VOY-001 BMJ DGX MVP – Two-Cycle Experiment

**ID:** EXP-VOY-001-BMJ-MVP-EXPERIMENT  
**Related Voyage:** VOY-001 BMJ Maiden Voyage  
**Owner:** Santiago-Architect + Santiago-PM (Hank as Captain)  

---

### 1. Purpose

Run a constrained but high-learning MVP experiment for VOY-001:

- Take a single BMJ topic.
- Run the BMJ and/or Santiago-Doctor-BMJ pipelines **locally on DGX**.
- Instrument everything, refactor iteratively, and measure:
  - cycle time,
  - framed-file/graph completeness,
  - logic/time/sequence coverage,
  - BDD pass rate.

After a small number of cycles (e.g. 5), we should know:

- How much DGX locality improves speed vs remote APIs.
- Where the biggest improvement opportunities lie.

---

### 2. Key Hypotheses

1. **DGX locality reduces cycle time and cost**  
   Running catchfish/fishnet and related pipelines against a local DGX LLM (with pre-loaded domain knowledge) will significantly reduce turnaround time vs remote API calls, without degrading quality.

2. **Iterative refactors can close quality gaps**  
   By instrumenting the pipeline and refactoring between cycles, we can systematically:
   - fill logic/time/sequence gaps,
   - improve framed-file coverage,
   - increase BDD pass %, for the chosen topic.

3. **We can stop after a small number of cycles with clear learnings**  
   After ~5 cycles (or when Hank decides), we will have enough data to decide:
   - how to generalize to more topics,
   - which refactors matter most,
   - and whether to lean more on BMJ pipeline or Santiago-native pipeline (Option 1 vs Option 2).

---

### 3. Plan (Two-Cycle Pattern, Repeated)

#### Cycle A – Instrument & Baseline Run

- [ ] Choose a BMJ topic and ensure inputs are ready.
- [ ] Wire metrics into:
  - DGX pipeline scripts (`run_bmj_pipeline.sh`, `run_santiago_bmj.sh`),
  - comparison script (`compare_engines.sh` if both engines are available).
- [ ] Run the topic through the current (slightly modified) machine on DGX:
  - BMJ pipeline,
  - and/or Santiago-Doctor-BMJ pipeline.
- [ ] Capture:
  - cycle time,
  - framed-file / graph coverage,
  - logic/time/sequence gaps,
  - BDD pass %,
  - logs and snapshots (`outputs/.../<topic_id>/`).

#### Cycle B – Refactor & Improve

- [ ] Analyze metrics and outputs from Cycle A:
  - Identify at least 10 candidate improvements (code, prompts, data, orchestration).
- [ ] With Hank (Captain) and PM input, **prioritize** improvements:
  - Use time-to-value estimates and impact on the BMJ $10M objective.
- [ ] Implement a small bundle of improvements (1–3 changes).
- [ ] Re-run the topic through the improved pipelines.
- [ ] Compare new metrics and outputs vs baseline.

Repeat **Cycle A+B** up to 5 times (or until Hank adjusts/ends the experiment).

---

### 4. Metrics & Time-to-Value

For each cycle, record:

- Cycle time per topic run.
- BDD pass % and number of failing scenarios.
- Coverage of:
  - sections,
  - logic,
  - time/sequence,
  - FHIR readiness (if applicable).
- Subjective engineering “sanity” (how hard it was to implement improvements).

Use these metrics to:

- Estimate time-to-value for each improvement.
- Decide where to invest further effort in VOY-001 and beyond.

---

### 5. Outputs

- Markdown report (e.g. `docs/architecture/expeditions/EXP-VOY-001-BMJ-MVP-EXPERIMENT-REPORT.md`) summarizing:
  - Cycles,
  - improvements attempted,
  - metrics before/after,
  - recommendations.
- Updated DGX scripts and configs checked into the repo.
- Candidate improvements promoted to:
  - future voyage plans,
  - or domain features.

---

### 6. Kanban Usage

Create cards such as:

- “VOY-001 MVP Cycle 1 – Instrumentation & Baseline Run”
- “VOY-001 MVP Cycle 2 – Refactor & Re-run”
- “VOY-001 MVP Summary & Recommendations”

Agents should:

- Work through each cycle using the Definition of Done from `CONTRIBUTING.md`.
- Record learnings and open questions in the expedition report and card comments.


