# Option 2 – Santiago-Doctor-BMJ Domain Expert Voyage

**Objective:**  
Build **santiago-doctor-bmj**, the first Santiago domain expert focused on BMJ Best Practice:

> A domain expert that converts guidelines → semantic graph → logic → FHIR-capable knowledge, and can answer scenario-based clinical questions.

This stream focuses on **platform improvement** and **reusable patterns** while using BMJ as the pilot domain.

## 1. Goals

1. Create a clean domain module:
   - `santiago/domain/santiago-doctor-bmj/`
2. Load BMJ content into NuSy-Core and embeddings.
3. Define specialist agents:
   - Santiago-Architect-BMJ
   - Santiago-Extractor-BMJ
   - Santiago-Reasoner-BMJ
   - Santiago-QA-BMJ
   - Santiago-Ethicist
   - Santiago-PM
4. Implement a Santiago-native pipeline that:
   - runs fully on DGX
   - generates semantic frames and logic
   - produces FHIR-friendly output
   - passes BDD tests for selected topics
5. Run autonomous DGX experiments to:
   - tune prompts
   - refine orchestration
   - design tackle modules
6. Directly compare Santiago-native results with the BMJ pipeline from Option 1.

## 2. Weekly Cadence (~96 hours / 4 days, largely autonomous)

Typically: **Thu–Sun**.

### Human Tasks (you)

- Design/check:
  - new prompts and agent configs
  - experiment setups
  - evaluation metrics
- Review DGX logs and experiment results.
- Guide the next set of experiments.

### DGX Tasks (autonomous)

Driven via:

```bash
./dgx/run_santiago_bmj.sh <topic_id>
```

This should:
1. Start or connect to DGX LLM services.
2. Load NuSy-Core and BMJ domain knowledge.
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

Experiments will iterate over:
- topic selection
- extraction strategies
- mapping to BMJ KG spec vs 4-layer vs FHIR CR
- pipeline structure and orchestration.

## 3. Platform Deliverables

From this voyage, the platform should gain:

- Reusable tackle modules for:
  - DGX orchestration
  - semantic frame extraction
  - direct KG mapping
  - FHIR CR emission
- Improved NuSy-Core patterns for guideline domains.
- A reusable blueprint for “Doctor-X” domain experts for other guideline sets.
