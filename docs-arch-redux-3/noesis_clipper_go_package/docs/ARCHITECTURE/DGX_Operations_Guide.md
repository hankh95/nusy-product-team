# DGX Operations Guide – BMJ & Santiago-Doctor-BMJ

This guide defines how to run both the BMJ pipeline (Option 1) and the Santiago-Doctor-BMJ pipeline (Option 2) on the DGX, using separate commands (Option A).

## 1. Prerequisites

- DGX H100 (or equivalent) with:
  - Ubuntu 24.x
  - CUDA 12.x
  - vLLM or equivalent LLM serving runtime
- Local models installed (examples):
  - Reasoning model: Llama-3.1-70B-Instruct or Mistral-Large
  - Worker/memory model: Mistral 7B or Qwen2.5-7B
- BMJ repo checked out inside the project:
  - e.g. `clients/bmj/pipeline/`
- Santiago repo structure in place:
  - `santiago_core/`
  - `santiago/domain/santiago-doctor-bmj/`
  - `self-improvement/`
  - `dgx/`

## 2. Running the BMJ Pipeline (Option 1)

Use:

```bash
./dgx/run_bmj_pipeline.sh <topic_id>
```

Expected responsibilities of `run_bmj_pipeline.sh`:

1. Start or contact the DGX LLM service.
2. Configure environment variables for the BMJ pipeline (paths, models, config files).
3. Invoke the BMJ pipeline entrypoint for the specified `<topic_id>`.
4. Run extraction → graph → framed-file generation.
5. Run BDD tests (if available) for that topic.
6. Emit:
   - framed files
   - logs
   - metrics (time, BDD pass %, error counts)
   - a snapshot directory, e.g. `outputs/bmj/<topic_id>/`.

You will need to plug in the real BMJ pipeline entrypoint and parameters.

## 3. Running the Santiago-Doctor-BMJ Pipeline (Option 2)

Use:

```bash
./dgx/run_santiago_bmj.sh <topic_id>
```

Expected responsibilities of `run_santiago_bmj.sh`:

1. Start or contact the DGX LLM services required by Santiago-Doctor-BMJ.
2. Load NuSy-Core state for BMJ and any required embeddings/indexes.
3. Run the Santiago-Doctor-BMJ agent pipeline for the given `<topic_id>`:
   - domain loading
   - L0/L1/L2 extraction
   - logic and sequence modeling
   - FHIR-capable structure generation (or CR mapping)
4. Run BDD tests.
5. Emit:
   - semantic frames
   - logic structures
   - BDD results
   - metrics
   - a snapshot directory, e.g. `outputs/santiago-doctor-bmj/<topic_id>/`.

## 4. Comparing the Two Pipelines

Use:

```bash
./dgx/compare_engines.sh <topic_id>
```

Expected responsibilities of `compare_engines.sh`:

1. Ensure both:
   - `outputs/bmj/<topic_id>/`
   - `outputs/santiago-doctor-bmj/<topic_id>/`
   exist (running the pipelines if needed).
2. Compare:
   - framed file coverage
   - logic completeness
   - FHIR-readiness (if available)
   - BDD pass rates
   - cycle time metrics
3. Emit a human-readable and machine-readable report (e.g. JSON) summarising which engine performed better on which dimensions.

## 5. Extending to a Second DGX (Future)

If you acquire a second DGX, a natural split would be:

- **DGX-1:** Production runs for BMJ (Option 1 or 2 winner)
- **DGX-2:** Platform experiments and new domain expert development (like Santiago-Doctor-BMJ)

In that case, you would adjust the scripts to:
- point BMJ production runs to DGX-1
- and Santiago platform runs to DGX-2, or use a scheduler/orchestrator.

For now, the three scripts in `dgx/` are the “GO buttons” you can use locally and in automation.
