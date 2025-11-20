## DGX & BMJ Readiness Migration Plan

**Purpose:** Coordinate all backlog work needed to:

- Bring Santiago / Noesis onto DGX in an always-on configuration; and  
- Deliver a credible BMJ Maiden Voyage (VOY-001) MVP, with measurable customer value and learning.

This plan focuses only on DGX + BMJ work and complements the broader `arch-migration-plan.md`.

---

## 1. Scope & Goals

- **In scope:**
  - DGX infrastructure, model serving, and environment readiness.
  - BMJ domain pipelines (BMJ pipeline and Santiago-Doctor-BMJ) running on DGX.
  - Knowledge loading (BMJ content, books, ontologies) into NusY-Core and/or DGX LLMs.
  - Experiments and expeditions that improve BMJ delivery and DGX utilization.
  - Kanban + wind patterns needed to keep this work flowing.
- **Out of scope:**
  - Non-BMJ domains (unless they are prerequisites for DGX infra).
  - General refactors not directly impacting DGX/BMJ.

**Target outcomes:**

1. A single BMJ topic can be run end-to-end on DGX with:
   - local LLM(s),
   - knowledge loading,
   - metrics and snapshots,
   - and at least a minimal BDD harness.
2. We have clear metrics and logs showing:
   - cycle time vs remote API approaches,
   - quality (coverage, logic, sequence, BDD pass %),
   - learning and improvement opportunities.
3. The Kanban system and wind patterns are sufficient for agents to keep working on DGX/BMJ without human permission for every step.

---

## 2. Current DGX/BMJ Backlog Assets

This section summarizes existing features and expeditions that are directly relevant.

### 2.1 Architecture & Checklists

- `docs/architecture/arch-vision-merged-plan.md` – target architecture and DGX runtime story.
- `docs/architecture/DGX_READINESS_CHECKLIST.md` – concrete DGX readiness steps.
- `docs-arch-redux-3/noesis_clipper_go_package/docs/ARCHITECTURE/DGX_Operations_Guide.md` – DGX operational vision.
- `docs-arch-redux-3/noesis_clipper_go_package/plans/VOY-001-BMJ-Maiden-Plan.md` – initial BMJ voyage plan.
- `docs-arch-redux-3/noesis_clipper_go_package/plans/Hybrid_Master_Plan_With_Checkpoints.md` – dual-path (Option 1/2) plan with ALPHA/BETA/GAMMA checkpoints.

### 2.2 Domain Features

- `domain/domain-features/specs/features/dgx-provisioning-automation.feature`
- `domain/domain-features/specs/features/dgx-storage-expansion-procurement.feature`
- `domain/domain-features/specs/features/dgx-monitoring-observability.feature`
- `domain/domain-features/specs/features/dgx-infrastructure-setup.feature` (via self-improvement workspace manifests)
- `domain/domain-features/specs/features/autonomous-execution-data-ingestion.feature`
- `domain/domain-features/specs/features/self-learning-autonomous-data.feature`
- `domain/domain-features/specs/features/multi-agent-framework.feature`
- `domain/domain-features/specs/features/ai-book-ingestion.feature` – legal book / textbook ingestion.

### 2.3 DGX/BMJ Expeditions

Under `docs/architecture/expeditions/`:

- `EXP-DGX-LLM-SELECTION.md` – choose DGX reasoning + worker/memory models.
- `EXP-VOY-001-BMJ-MVP-EXPERIMENT.md` – two-cycle BMJ DGX MVP experiment.
- `EXP-DGX-KNOWLEDGE-LOADING-CADENCE.md` – define reload cadence for project knowledge.
- `EXP-DGX-DIRECT-GRAPH-MAPPING.md` – test direct BMJ graph mapping (skip 4L tagging).

Under `self_improvement/santiago_dev/workspace/cargo-manifests/` (self-improvement DGX work):

- `dgx-infrastructure-setup.feature`
- `dgx-deployment-commissioning.feature`
- `dgx-readiness-preparation.feature`
- `nusypi-dgx-integration.feature`
- `software-stack-preparation.feature`
- `research-pipeline-development.feature`

### 2.4 Kanban & Wind

- `docs/kanban-work-poller.md` – Kanban work poller service.
- `docs/architecture/KANBAN_WIND_PLAYBOOK.md` – wind patterns for unblocking flow.
- `self_improvement/santiago-pm/cargo-manifests/kanban-wind-creation-board-unblocking.md` – wind creation feature spec.

---

## 3. Phased Plan to DGX & BMJ MVP

### Phase 0 – Clarify Voyage & Metrics (L1 → L2)

**Goal:** Turn the BMJ journey mind-dumps into a concrete VOY-001 voyage and measurement framework.

- [ ] Finalize `voyage-VOY-001-BMJ-Maiden.yaml` per `VOYAGE_MODEL_SPECIFICATION.md`, including:
  - main_objective,
  - constraints (duration, compute, budget),
  - goals and measures (BDD %, coverage, cycle time, BMJ value proxies),
  - motivation_statement,
  - team roles and motivation_vector.
- [ ] Define a **BMJ value measurement model**:
  - Which metrics correspond to BMJ’s $10M problem?
  - How will we report progress (ALPHA/BETA/GAMMA checkpoints)?
- [ ] Add or refine any missing **knowledge/ontology stubs** for:
  - journeys/voyages,
  - motivation,
  - BMJ domain entities (if needed).

**Time-to-value:** ~2–4 hours.  
**Dependencies:** None; unblocks all downstream DGX/BMJ work by clarifying “what good looks like.”

---

### Phase 1 – DGX Infrastructure & Model Readiness (L4 base)

**Goal:** Make DGX a safe, reliable host for Santiago/Noesis BMJ work.

- **Infra features / manifests:**
  - `dgx-infrastructure-setup.feature`
  - `dgx-deployment-commissioning.feature`
  - `dgx-readiness-preparation.feature`
  - `software-stack-preparation.feature`
- **Checklist alignment:**
  - `DGX_READINESS_CHECKLIST.md` – hardware, OS, GPU, storage, scripts.

**Work items:**

- [ ] Stand up or confirm:
  - OS, CUDA, drivers, NCCL.
  - Storage layout for `outputs/bmj/<topic_id>/` and `outputs/santiago-doctor-bmj/<topic_id>/`.
- [ ] Make sure:
  - `run_bmj_pipeline.sh`, `run_santiago_bmj.sh`, `compare_engines.sh` exist, are executable, and run at least stub flows.
- [ ] Implement & test a **minimal Kanban → DGX integration path**:
  - card → script invocation → logs/snapshots → status update.

**Time-to-value:**  
- 1–2 days of focused infra+tooling work, but **partial value** as soon as stub scripts run and logs/snapshots appear.

---

### Phase 2 – Model & Knowledge Readiness (L2 / L3)

**Goal:** Ensure DGX has the right models and knowledge surfaces for BMJ.

**LLM selection & configuration:**

- `EXP-DGX-LLM-SELECTION.md` – pick:
  - reasoning model (e.g., Llama/Mistral),
  - worker/memory model (for extraction + summarization).

**Knowledge loading & books:**

- `EXP-DGX-KNOWLEDGE-LOADING-CADENCE.md` – set reload cadence and process.
- `ai-book-ingestion.feature` – ingest legal textbooks/books into L0–L3 and KG, with licensing and provenance.

**Work items:**

- [ ] Shortlist and test DGX-capable models for:
  - BMJ reasoning,
  - bulk extraction / summarization.
- [ ] Implement a **project brain loader**:
  - loads BMJ code, content, specs, and relevant ontologies into:
    - NusY-Core graphs,
    - and/or a local LLM memory store.
- [ ] Run initial QA on:
  - key Q&A patterns (“What is X?”, “Where is Y pipeline implemented?”, “What are current bottlenecks?”).

**Time-to-value:**  
- 1–2 days for a first pass, but meaningful value as soon as the project brain can answer basic questions and remove “where is X?” delays.

---

### Phase 3 – BMJ DGX MVP Experiment (L3 → L4)

**Goal:** Run the VOY-001 MVP experiment (two-cycle pattern) and show concrete improvements vs baseline.

**Key expedition:**

- `EXP-VOY-001-BMJ-MVP-EXPERIMENT.md`

**Work items (for one topic):**

- [ ] **Cycle A – Instrument & Baseline:**
  - Wire metrics into DGX scripts.
  - Run BMJ and/or Santiago-Doctor-BMJ pipeline on DGX.
  - Capture cycle time, coverage, BDD results, and snapshots.
- [ ] **Cycle B – Refactor & Improve:**
  - Generate 10+ improvement candidates.
  - Use prioritizer (time-to-value, risk, learning) to pick a subset.
  - Implement and re-run.
- [ ] Repeat up to 5 cycles (or until Captain re-directs).
- [ ] Summarize learnings and recommendations in an expedition report.

**Time-to-value:**  
- First baseline run: ~0.5–1 day.  
- Each refactor cycle: ~0.5–1 day.  
- Value increases with each cycle as metrics and outputs improve and we discover which levers matter.

---

### Phase 4 – Direct Graph Mapping & Advanced Capabilities (L3 enhancements)

**Goal:** Explore advanced paths that may simplify or strengthen BMJ knowledge representation.

**Key expedition:**

- `EXP-DGX-DIRECT-GRAPH-MAPPING.md` – direct BMJ graph mapping without full 4L tagging.

**Other candidates:**

- Extending `ai-book-ingestion.feature` into:
  - specialized medical book pipelines,
  - integration with BMJ graphs.
- Additional domain features for:
  - multi-agent reasoning over BMJ content,
  - FHIR-aware mappings.

**Time-to-value:**  
- Highly exploratory; treat as optional experiments that proceed in parallel once Phases 1–3 are underway.

---

## 4. Kanban & Wind Integration

To keep both human and agent crews busy without constant permission:

- **Boards:**
  - Use a dedicated DGX/BMJ board (e.g. `voy-001-bmj-maiden`) with:
    - columns per `KanbanBoard` model,
    - `Ready` always seeded with at least 3–5 small cards.
- **Card templates:**
  - For each feature/expedition above, define:
    - a short title,
    - `repository_path`,
    - a one-paragraph Definition of Done (tests, docs, metrics, learning logged).
- **Wind patterns:**
  - When the board stalls, use `KANBAN_WIND_PLAYBOOK.md`:
    - journey re-framing,
    - hypothesis-driven experiments,
    - ask-AI research,
    - 5 Whys + stop-card,
    - prioritizer wind.
  - Encode these as explicit cards so agents can claim them.

---

## 5. Roles & Motivation (4-Layer Learning)

- **L1 (Narrative):** BMJ journey descriptions, motivation statements (“be of maximum service to BMJ by…”).
- **L2 (Structured):** Voyage YAML, motivation_vector, DGX & BMJ ontologies.
- **L3 (Logic):** Features and expeditions here, plus wind patterns and decision rules (when to reload, when to stop, when to escalate).
- **L4 (Execution):** DGX scripts, Kanban poller, autonomous services, CI/CD, plus in-memory Git + KG runtime.

Key roles for this plan:

- **Santiago-PM:** Owns VOY-001 voyage definition, backlog clarity, and BMJ value measurement.
- **Santiago-Architect:** Owns DGX runtime, experiments, and system-level learning.
- **Santiago-Dev/Research:** Implement features and expeditions, instrument pipelines.
- **Santiago-UX:** Ensure humans/agents can see progress, understand state, and know how to interact.
- **Santiago-Ethicist:** Guardrails for BMJ content, licensing, and any clinical implications.

---

## 6. Next Actions (Immediate, 0–4 Hours)

1. Confirm this plan is saved and visible: `docs/architecture/dgx-bmj-readiness-plan.md`.  
2. Create initial DGX/BMJ Kanban cards (manually or via poller integration) for:
   - VOY-001 voyage YAML finalization,
   - DGX readiness checklist steps,
   - DGX LLM selection cycle 1,
   - DGX MVP Cycle 1 instrumentation & baseline.
3. Ensure the Kanban poller and autonomous service can:
   - see the DGX/BMJ board,
   - claim `Ready` cards,
   - update status and logs without human permission for each step.
4. Begin executing Phase 0 and Phase 1 tasks while logging learnings per expedition/feature.


