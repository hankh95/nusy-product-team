# DGX Readiness Checklist – Noesis / BMJ / Santiago-Doctor-BMJ

This checklist breaks down DGX readiness into concrete, testable steps so Santiago‑Architect, Santiago‑PM, and autonomous agents can prepare and validate DGX usage for the **BMJ Maiden Voyage (VOY‑001)** and later voyages.

It is derived from:

- `docs-arch-redux-3/noesis_clipper_go_package/docs/ARCHITECTURE/DGX_Operations_Guide.md`
- `docs-arch-redux-3/noesis_clipper_go_package/plans/VOY-001-BMJ-Maiden-Plan.md`
- `docs-arch-redux-3/noesis_clipper_go_package/plans/Hybrid_Master_Plan_With_Checkpoints.md`

---

## 1. Hardware & Base System

- [ ] **DGX hardware available**
  - [ ] DGX H100 (or equivalent) online and reachable.
  - [ ] OS: Ubuntu 24.x or equivalent supported version.
- [ ] **GPU & driver stack**
  - [ ] CUDA 12.x installed and working (`nvidia-smi`, `nvcc --version`).
  - [ ] NCCL / driver versions meet vendor recommendations.
- [ ] **Storage & directories**
  - [ ] Sufficient disk space allocated for:
    - [ ] `outputs/bmj/<topic_id>/`
    - [ ] `outputs/santiago-doctor-bmj/<topic_id>/`
    - [ ] logs, metrics, and snapshots.

---

## 2. Model Serving & LLM Runtime

- [ ] **LLM runtime installed**
  - [ ] vLLM or equivalent serving runtime installed on DGX.
  - [ ] Basic health check endpoint reachable.
- [ ] **Models available locally**
  - [ ] Reasoning model (e.g. Llama‑3.1‑70B‑Instruct or Mistral‑Large) downloaded and configured.
  - [ ] Worker/memory model (e.g. Mistral‑7B or Qwen2.5‑7B) downloaded and configured.
- [ ] **Configuration**
  - [ ] Environment variables or config files specify:
    - [ ] model names / paths,
    - [ ] max context / batch settings,
    - [ ] ports and auth (if any).

---

## 3. Repository Layout & Code Readiness

- [ ] **Noesis / BMJ repo layout present**
  - [ ] `docs-arch-redux-3/noesis_clipper_go_package/` present with:
    - [ ] `dgx/run_bmj_pipeline.sh`
    - [ ] `dgx/run_santiago_bmj.sh`
    - [ ] `dgx/compare_engines.sh`
    - [ ] `plans/` and `docs/ARCHITECTURE/` as reference.
- [ ] **Santiago / BMJ domain layout (future)**
  - [ ] BMJ domain modules defined or planned (e.g. `santiago/domain/santiago-doctor-bmj/` per Option 2 plan).
- [ ] **Entry points compile / lint**
  - [ ] Any Python/Go wrappers referenced by the DGX scripts pass basic lint/compile checks.

---

## 4. DGX Scripts – Execution & Outputs

For each script, the goal is to have at least a **smoke test** path that runs end‑to‑end for a test `<topic_id>` and produces outputs under `outputs/`.

### 4.1 `run_bmj_pipeline.sh` (Option 1 – BMJ pipeline)

- [ ] Script present and executable.
- [ ] When run as:

  ```bash
  ./dgx/run_bmj_pipeline.sh <topic_id>
  ```

  it should:

  - [ ] Start or contact the DGX LLM service.
  - [ ] Configure BMJ pipeline environment (paths, models, configs).
  - [ ] Invoke the BMJ pipeline entrypoint for `<topic_id>`.
  - [ ] Run extraction → graph → framed‑file generation.
  - [ ] Optionally run BDD tests, if available.
  - [ ] Emit:
    - [ ] framed files,
    - [ ] logs,
    - [ ] metrics (time, error counts),
    - [ ] a snapshot directory `outputs/bmj/<topic_id>/`.

### 4.2 `run_santiago_bmj.sh` (Option 2 – Santiago‑Doctor‑BMJ)

- [ ] Script present and executable.
- [ ] When run as:

  ```bash
  ./dgx/run_santiago_bmj.sh <topic_id>
  ```

  it should:

  - [ ] Start or contact DGX LLM services.
  - [ ] Load NuSy‑Core state and BMJ domain knowledge.
  - [ ] Run the Santiago‑Doctor‑BMJ agent pipeline for `<topic_id>`:
    - [ ] domain loading,
    - [ ] L0/L1/L2 extraction,
    - [ ] logic and sequence modeling,
    - [ ] FHIR‑capable structure generation (or CR mapping).
  - [ ] Run BDD tests (once defined).
  - [ ] Emit:
    - [ ] semantic frames,
    - [ ] logic structures,
    - [ ] BDD results,
    - [ ] metrics,
    - [ ] a snapshot directory `outputs/santiago-doctor-bmj/<topic_id>/`.

### 4.3 `compare_engines.sh` (Engine comparison)

- [ ] Script present and executable.
- [ ] When run as:

  ```bash
  ./dgx/compare_engines.sh <topic_id>
  ```

  it should:

  - [ ] Ensure `outputs/bmj/<topic_id>/` and `outputs/santiago-doctor-bmj/<topic_id>/` exist (running the pipelines if needed).
  - [ ] Compare:
    - [ ] framed file coverage,
    - [ ] logic completeness,
    - [ ] FHIR‑readiness,
    - [ ] BDD pass rates,
    - [ ] cycle time.
  - [ ] Emit:
    - [ ] a human‑readable report (markdown or text),
    - [ ] a JSON summary suitable for dashboards or logs.

---

## 5. Voyage Orchestration & Checkpoints

- [ ] **Voyage YAML present**
  - [ ] A `voyage-VOY-001-BMJ-Maiden.yaml` (or equivalent) exists and matches the schema in `VOYAGE_MODEL_SPECIFICATION.md`.
- [ ] **Orchestrator entrypoint**
  - [ ] A script or service can:
    - [ ] read the voyage YAML,
    - [ ] run DGX scripts for the configured topics,
    - [ ] record metrics per topic and per checkpoint (ALPHA, BETA, GAMMA).
- [ ] **Checkpoint integration**
  - [ ] The orchestrator (or a simple notebook/script) can generate ALPHA/BETA/GAMMA comparison reports that match the Hybrid plan questions.

---

## 6. Kanban & Workflow Readiness (Architect / PM)

- [ ] **DGX voyage manifest linked**
  - [ ] `self_improvement/santiago-pm/cargo-manifests/dgx-bmj-maiden-voyage.md` is the canonical spec for DGX BMJ work.
- [ ] **DGX Kanban board defined**
  - [ ] A board (e.g. `voy-001-bmj-maiden`) exists with cards for:
    - [ ] `run_bmj_pipeline.sh`
    - [ ] `run_santiago_bmj.sh`
    - [ ] `compare_engines.sh`
    - [ ] voyage YAML + orchestrator
    - [ ] DGX readiness checklist integration
  - [ ] 3–5 cards are in **Ready** for agents to claim.
- [ ] **WIP threshold rule documented**
  - [ ] Policy in DGX manifest and/or this checklist:
    - When DGX voyage board has **< 5 Ready cards**, Architect must:
      - review Backlog items and voyage plans,
      - break down more work,
      - promote 3–5 executable cards into Ready.

---

## 7. Validation & Sign‑off

- [ ] DGX hardware and model stack verified.
- [ ] All three DGX scripts execute a smoke test for at least one `<topic_id>`.
- [ ] Voyage YAML + orchestrator can run a small set of topics and capture metrics.
- [ ] Kanban board set up with DGX work ready to pull.
- [ ] Hank (Captain) has reviewed and approved the readiness checklist for VOY‑001.


