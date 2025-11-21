## Expedition EXP-042 – Santiago Fleet Memory Architecture (Three-Tier Memory)

**ID:** EXP-042  
**Title:** Three-Tier Fleet Memory Architecture  
**Owner:** Santiago-Architect (with Captain Hank)  
**Status:** In progress  

---

### 1. Purpose

Implement and validate the **three-tier memory architecture** for Santiago-core and the Santiago fleet, so that agents:

- have persistent **personal memory** (working/episodic/semantic);
- share **voyage/project knowledge** via structured graphs; and
- maintain **live conversation context** and multimodal inputs,

in a way that measurably improves team performance and aligns with the naval metaphor and ethical principles.

This expedition realizes the vision outlined in:

- `_archive/legacy-docs/research-logs/memory-architecture-analysis.md` (EXP-042 definition), and  
- `_archive/legacy-docs/research-logs/memory-architecture-comprehensive-stream.md`.

---

### 2. Target Memory Layers (Concept → Code)

From the three-tier memory analysis, we map:

- **Crew Member Brain / Officer’s Private Logbook** → `santiago_core/services/personal_memory.py`
  - Working/episodic/semantic personal knowledge per agent.
  - Private reflections and patterns not immediately shared.

- **Bridge Talk (Live Conversation Memory)** → `santiago_core/services/conversation_memory.py`
  - Live conversation context for multi-agent and human–agent sessions.
  - Archival of conversations with summaries for later reuse.

- **Voyage Shared Memory (Boat / Fleet Knowledge Graph)** → `santiago_core/services/knowledge_graph.py`
  - Project/voyage knowledge (decisions, artifacts, metrics) as RDF/graph.
  - Links to experiments, expeditions, Kanban items, and DGX runs.

- **Multimodal Ingest Officer** → `santiago_core/services/multimodal_ingest.py`
  - Normalizes and routes inputs (text, logs, possibly files) into the right layers (personal, conversation, KG).

- **Memory Coordinator (Fleet Memory Orchestrator)** → `santiago_core/services/memory_coordinator.py`
  - Orchestrates calls across memory layers.
  - Provides a single API to agents and the team coordinator.

Agents and team coordination:

- `santiago_core/core/team_coordinator.py` wired to `SantiagoMemoryCoordinator`.  
- `santiago_core/agents/santiago_pm.py`, `santiago_architect.py`, `santiago_developer.py` take `memory_coordinator` and call into it for learning and recall.

---

### 3. Questions & Hypotheses

**Q1. Does fleet memory reduce “lost context” and repeated work?**  
Hypothesis: With personal + conversation + shared memory wired in, agents will:
- refer back to prior decisions instead of re-deriving them; and  
- complete similar cards faster over time.

**Q2. Does conversation memory improve multi-agent coordination?**  
Hypothesis: Bridge Talk + archival summaries will reduce coordination overhead between PM/Architect/Developer, especially across long voyages or DGX runs.

**Q3. Is the architecture maintainable and aligned with the 4-layer model?**  
Hypothesis: The implementation can be cleanly described as:
- L1: narrative logs and conversations;
- L2: structured triples/graphs and indexed memories;
- L3: policies and logic in `memory_coordinator` and agents;
- L4: concrete services and tools (ingest, search, archival).

---

### 4. Plan (High-Level Cycles)

#### Cycle 1 – Document & Align Architecture

- [ ] Write a concise **Fleet Memory Architecture** section under `docs/architecture/`:
  - Map the naval metaphor + three-tier model to the new services.
  - Show how this interacts with KG and DGX/BMJ voyages.
- [ ] Cross-reference:
  - legacy memory research logs,
  - new services in `santiago_core/services/`,
  - and the motivation sections in `arch-vision-merged-plan.md`.

#### Cycle 2 – Baseline Behavior & Metrics

- [ ] Design small, focused experiments:
  - A few autonomous runs with and without memory enabled (ablation).
  - Measure:
    - time to complete a set of Kanban cards,
    - number of repeated questions/decisions,
    - how often prior logs/decisions are reused.
- [ ] Capture metrics and qualitative observations in an expedition report.

#### Cycle 3 – Integration with Voyages & DGX

- [ ] Show how EXP-042 supports:
  - VOY-001 BMJ Maiden Voyage (DGX/BMJ plan),
  - Kanban wind patterns (e.g. Ask-AI, 5 Whys, stop-card).
- [ ] Propose any adjustments needed to:
  - voyage YAML structure,
  - DGX experiment designs,
  - or Kanban rules to maximize learning from memory.

---

### 5. Outputs

- `docs/architecture/EXP-042-fleet-memory-architecture.md` or similar section summarizing:
  - memory layers,
  - code locations,
  - and 4-layer mapping.
- A short **expedition report** (can be appended to this file or a sibling) with:
  - experiment designs,
  - metrics before/after,
  - recommendations.
- Kanban cards marked `done` for EXP-042 implementation and added cards for evaluation & evolution.

---

### 6. Kanban Usage

Suggested cards (on the master board or a memory-focused board):

- “EXP-042 – Document Fleet Memory Architecture in docs/architecture”
- “EXP-042 – Design and run memory ablation experiment”
- “EXP-042 – Integrate Fleet Memory with VOY-001 BMJ voyage & DGX plans”

Agents should:

- Treat this expedition as **done at code level but in-progress at system/validation level**.
- Use the Definition of Done from `CONTRIBUTING.md` (tests, docs, logs, Kanban state) for each card.


