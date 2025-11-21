## Fleet Memory (EXP-042) Kanban Card Templates

These templates define work items for the EXP-042 Fleet Memory Architecture.
They should typically live on the `master_board` or a dedicated memory-focused board.

---

### 1. Document Fleet Memory Architecture

- **Title:** EXP-042 – Document Fleet Memory Architecture  
- **item_id:** `exp-042-fleet-memory-docs`  
- **item_type:** `expedition`  
- **repository_path:** `docs/architecture/expeditions/EXP-042-FLEET-MEMORY-ARCHITECTURE.md`  
- **Description:** Write a concise architecture description for the Fleet Memory system, mapping the three-tier memory model and naval metaphor to concrete services (`personal_memory`, `conversation_memory`, `knowledge_graph`, `multimodal_ingest`, `memory_coordinator`) and the 4-layer model.  
- **Definition of Done:** Expedition doc updated with clear diagrams/sections listing memory layers, code locations, and how they interact.

---

### 2. Design Memory Ablation Experiment

- **Title:** EXP-042 – Design memory ablation experiment  
- **item_id:** `exp-042-memory-ablation-design`  
- **item_type:** `expedition`  
- **repository_path:** `docs/architecture/expeditions/EXP-042-FLEET-MEMORY-ARCHITECTURE.md`  
- **Description:** Define one or more small experiments comparing autonomous runs with and without Fleet Memory enabled (or with certain layers disabled), including metrics and evaluation criteria.  
- **Definition of Done:** Expedition doc includes a concrete experiment design: steps, metrics (e.g., task completion time, repeated questions, reuse of prior decisions), and logging locations.

---

### 3. Run Memory Experiment & Capture Results

- **Title:** EXP-042 – Run memory experiment & capture results  
- **item_id:** `exp-042-memory-experiment-run`  
- **item_type:** `expedition`  
- **repository_path:** `docs/architecture/expeditions/EXP-042-FLEET-MEMORY-ARCHITECTURE.md`  
- **Description:** Execute the designed experiment(s), collect metrics/logs, and summarize findings (does Fleet Memory improve team performance and coordination?).  
- **Definition of Done:** Expedition doc updated with before/after metrics, qualitative observations, and explicit recommendations (e.g., keep/change memory design, tuning suggestions).

---

### 4. Integrate Fleet Memory with DGX/BMJ Voyages

- **Title:** EXP-042 – Integrate Fleet Memory with VOY-001 BMJ voyage  
- **item_id:** `exp-042-memory-voy-001-integration`  
- **item_type:** `feature`  
- **repository_path:** `docs/architecture/dgx-bmj-readiness-plan.md`  
- **Description:** Update DGX/BMJ readiness and VOY-001 voyage docs to show how Fleet Memory is used during BMJ voyages (e.g., conversation logs, decision memory, experiment artifacts).  
- **Definition of Done:** `dgx-bmj-readiness-plan.md` and/or voyage YAML include explicit references to Fleet Memory roles and usage; any new experiments or metrics are linked to EXP-042.


