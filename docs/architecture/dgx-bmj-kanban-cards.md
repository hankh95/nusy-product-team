## DGX/BMJ Kanban Card Templates – Board `voy-001-bmj-maiden`

This file defines initial Kanban card templates for the DGX/BMJ readiness work.  
Cards use `board_id = "voy-001-bmj-maiden"` so they can be created via `SantiagoKanbanService` or other tools.

---

### Phase 0 – Voyage & Metrics

1. **Title:** Define VOY-001 BMJ voyage YAML  
   - **item_id:** `voy-001-bmj-voyage-yaml`  
   - **item_type:** `feature`  
   - **repository_path:** `docs-arch-redux-3/noesis_clipper_go_package/voyages/voyage-VOY-001-BMJ-Maiden.yaml`  
   - **Description:** Align the VOY-001 voyage YAML with `VOYAGE_MODEL_SPECIFICATION.md`: fill in main_objective, constraints, goals/measures, motivation_statement, team roles, and connections to expeditions.  
   - **Definition of Done:** YAML validates against spec; linked from `dgx-bmj-readiness-plan.md`; basic metrics and checkpoints (ALPHA/BETA/GAMMA) are defined.

2. **Title:** Define BMJ value & metrics model for VOY-001  
   - **item_id:** `voy-001-bmj-metrics-model`  
   - **item_type:** `research_log`  
   - **repository_path:** `docs/architecture/expeditions/EXP-VOY-001-BMJ-MVP-EXPERIMENT.md`  
   - **Description:** Specify which metrics (BDD %, coverage, cycle time, etc.) best approximate BMJ’s $10M objective and how they will be reported at voyage checkpoints.  
   - **Definition of Done:** Experiment expedition updated with explicit metrics and thresholds; summary paragraph added to `dgx-bmj-readiness-plan.md`.

---

### Phase 1 – DGX Infra & Scripts

3. **Title:** Align DGX readiness checklist with actual repo state  
   - **item_id:** `dgx-readiness-checklist-alignment`  
   - **item_type:** `task`  
   - **repository_path:** `docs/architecture/DGX_READINESS_CHECKLIST.md`  
   - **Description:** Cross-check each checklist item against the current repo (scripts, configs, docs) and ensure paths and expectations are accurate.  
   - **Definition of Done:** Checklist updated to reflect real script locations and configs; any missing items logged as follow-up cards.

4. **Title:** Verify DGX pipeline script stubs (local)  
   - **item_id:** `dgx-scripts-stub-verification`  
   - **item_type:** `task`  
   - **repository_path:** `docs-arch-redux-3/noesis_clipper_go_package/dgx`  
   - **Description:** Confirm `run_bmj_pipeline.sh`, `run_santiago_bmj.sh`, and `compare_engines.sh` exist, are executable, and match expectations described in the DGX readiness checklist.  
   - **Definition of Done:** Scripts run in stub mode locally; any gaps are captured as new cards or TODOs inside the scripts.

---

### Phase 2 – Models & Knowledge

5. **Title:** DGX LLM Selection – Cycle 1 Landscape & Shortlist  
   - **item_id:** `exp-dgx-llm-selection-cycle1`  
   - **item_type:** `expedition`  
   - **repository_path:** `docs/architecture/expeditions/EXP-DGX-LLM-SELECTION.md`  
   - **Description:** Execute Cycle 1 of the DGX LLM selection expedition: identify 3–5 candidate models and produce a shortlist with basic trade-offs.  
   - **Definition of Done:** Expedition doc updated with candidate list, basic properties, and a proposed shortlist.

6. **Title:** DGX Knowledge Loading – Map BMJ Project Surfaces  
   - **item_id:** `exp-dgx-knowledge-loading-map-surfaces`  
   - **item_type:** `expedition`  
   - **repository_path:** `docs/architecture/expeditions/EXP-DGX-KNOWLEDGE-LOADING-CADENCE.md`  
   - **Description:** Perform Cycle 1 of the knowledge loading cadence expedition: identify BMJ project artifacts (code, content, specs, graphs, logs) and decide what should live in NusY-Core vs LLM vs both.  
   - **Definition of Done:** Expedition doc updated with a clear artifact map; any needed ontology stubs are noted.

7. **Title:** Design BMJ Project Brain Loader  
   - **item_id:** `bmj-project-brain-loader-design`  
   - **item_type:** `feature`  
   - **repository_path:** `docs/architecture/expeditions/EXP-DGX-KNOWLEDGE-LOADING-CADENCE.md`  
   - **Description:** Design a simple script/service that loads BMJ project artifacts into NusY-Core and/or a DGX LLM, using the surfaces identified in the previous card.  
   - **Definition of Done:** Design section added to expedition doc or a new design note; clear inputs/outputs and approximate implementation steps defined.

---

### Phase 3 – BMJ DGX MVP Experiment

8. **Title:** VOY-001 MVP – Cycle 1 Instrumentation & Baseline  
   - **item_id:** `voy-001-mvp-cycle1-baseline`  
   - **item_type:** `expedition`  
   - **repository_path:** `docs/architecture/expeditions/EXP-VOY-001-BMJ-MVP-EXPERIMENT.md`  
   - **Description:** Implement Cycle A of the MVP experiment: add metrics wiring to DGX scripts and run a baseline topic (locally, if DGX not yet reachable).  
   - **Definition of Done:** Expedition doc records metrics schema and baseline results; scripts contain TODOs or stubs for DGX-specific parts.

9. **Title:** VOY-001 MVP – Cycle 2 Refactor & Re-run (Design Only)  
   - **item_id:** `voy-001-mvp-cycle2-refactor-design`  
   - **item_type:** `expedition`  
   - **repository_path:** `docs/architecture/expeditions/EXP-VOY-001-BMJ-MVP-EXPERIMENT.md`  
   - **Description:** Based on imagined or stubbed baseline results, draft candidate improvements and a prioritization approach (time-to-value, risk, learning) for Cycle B.  
   - **Definition of Done:** Expedition doc lists at least 10 improvement ideas and how to prioritize them once real metrics are available.

---

### Phase 4 – Advanced Capabilities

10. **Title:** Direct Graph Mapping – Understand BMJ Spec & 4L Mapping  
    - **item_id:** `exp-dgx-direct-graph-mapping-understand`  
    - **item_type:** `expedition`  
    - **repository_path:** `docs/architecture/expeditions/EXP-DGX-DIRECT-GRAPH-MAPPING.md`  
    - **Description:** Execute Cycle 1 of the direct graph mapping expedition: collect BMJ graph schema/spec (or subset) and document how current 4L outputs map to it.  
    - **Definition of Done:** Expedition doc contains a clear mapping description, gaps, and data samples for later prototype work.

11. **Title:** AI Book Ingestion – Initial Design for BMJ Integration  
    - **item_id:** `ai-book-ingestion-bmj-design`  
    - **item_type:** `feature`  
    - **repository_path:** `domain/domain-features/specs/features/ai-book-ingestion.feature`  
    - **Description:** Extend the AI book ingestion feature with notes on how ingested clinical textbooks should be surfaced to BMJ graphs and DGX pipelines.  
    - **Definition of Done:** Feature file updated with at least one scenario connecting ingested books to BMJ graph/pipeline usage.

12. **Title:** DGX vLLM Service Config & Client Stub  
    - **item_id:** `dgx-vllm-service-setup`  
    - **item_type:** `feature`  
    - **repository_path:** `configs/dgx/vllm_mistral7b.json`  
    - **Description:** Define a DGX vLLM configuration (model name, base URL, concurrency hints) and a simple client wrapper (`santiago_core/services/vllm_client.py`) for multi-agent inference.  
    - **Definition of Done:** Config file exists and is documented; vLLMClient wrapper can be imported and called in a small test script, ready for future integration with LLMRouter and agents.


