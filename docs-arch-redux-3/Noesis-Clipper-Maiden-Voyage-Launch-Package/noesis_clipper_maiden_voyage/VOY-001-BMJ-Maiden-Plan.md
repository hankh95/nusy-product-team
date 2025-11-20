# Noesis Clipper – Maiden Voyage Launch Plan (Improved)
**Date:** 2025-11-20  
**Voyage ID:** VOY-001-BMJ-Maiden  
**Status:** Ready for Launch  

This document describes the improved execution plan for the BMJ → Machine-Executable Knowledge Maiden Voyage on the DGX, integrating the earlier MVP plan and the later “Launch Package” plan into a single, realistic, and extensible design.

---

## 1. DGX Maiden Voyage Execution Plan – BMJ → Machine-Executable Knowledge

### 1.1 DGX Configuration

**Hardware**
- DGX H100 ×8  
- 1.5 TB RAM  
- 30 TB NVMe RAID0  
- Shared in-memory workspace: `memory://voy-001-bmj-maiden`

**Software**
- Ubuntu 24.04  
- CUDA 12.4  
- vLLM 0.6.x (role-based routing)  
- Optional: ExllamaV2 / TensorRT-LLM for quantized models  
- Santiago-core v1.0 (post-migration)  
- Noesis Clipper runtime services (agents, KG engine, metrics engine)

---

### 1.2 LLM Strategy – Hybrid Dual-Model Setup

A realistic but powerful dual-model setup for the Maiden Voyage:

| Layer                    | Model (example)                 | Quant | Context | Purpose                                      |
|--------------------------|---------------------------------|-------|---------|----------------------------------------------|
| Reasoning Layer          | Llama-3.1-70B-Instruct or Mistral-Large-2411 | 4-bit | 128k    | Heavy cognitive work, extraction, KG mapping |
| Memory/Worker Layer      | Mistral 7B or Qwen2.5 7B        | 4-bit | 32k     | Fast project Q&A, micro-tasks, RAG helper    |

Optional third specialist model (for later voyages, not required for MVP):
- Med42 or OpenBioLLM-70B as a medical specialist reasoning tool.

---

### 1.3 Domain Knowledge Loading

**Into NuSy-Core**
- BMJ topic HTML, lists, and tables  
- Clinical vocabularies and semantic-web schemas (RDF/OWL/TTL)  
- CI-Knowledge Graph and 4-layer model definitions  
- BMJ-specific KG spec (for direct mapping experiment)

**Into Embedding Store**
- All BMJ topic sections as text chunks  
- BMJ glossary and decision tables  
- BDD scenario templates

**Into Memory/Worker LLM**
- Frequently accessed project context  
- Summaries of NuSy-Core state for fast Q&A

---

### 1.4 Crew Composition (Roles, Not Fixed Headcount)

| Role                | Description                                 | Primary Tools                              | Motivation Focus       |
|---------------------|---------------------------------------------|--------------------------------------------|------------------------|
| PM / Navigator      | Defines journey and prioritises work        | Prioritiser, Kanban, metrics dashboards    | Service, clarity       |
| Architect           | Maintains Noesis Clipper structure          | KG engine, L3/L4 mappers, schemas          | Craft excellence       |
| Extractor           | L0→L1→L2 semantic extraction                | Catchfish, Seawater L0                     | Learning, clarity      |
| Developer(s)        | Code refactor, tackle modules               | Code runner, DGX tools, CI/CD              | Craft, urgency         |
| Researcher          | Hypotheses, spec adaptation, model choice   | Clinical corpora, experiment harness       | Curiosity              |
| QA                  | BDD scenarios, correctness checks           | Fishnet BDD engine                         | Excellence             |
| Ethicist            | Safety and integrity gate                   | Harm scanner, non-aggression rules         | Integrity              |

Crew size can flex (4–12 agents) per voyage phase.

---

### 1.5 Voyage Structure – 10-Day Hybrid Cycle Design

#### Day 0 – Baseline

- Load selected BMJ topic into NuSy-Core and embedding store.  
- Run existing pipeline (as-is) once entirely on DGX.  
- Capture extraction metrics, BDD results, and performance.  
- Snapshot code + outputs as **Baseline**.

---

#### Cycle 1 (Days 1–4) – Knowledge Catch & Alignment

**Goal**  
Build a robust BMJ → L0→L1→L2→L3 extraction pipeline fully local on DGX.

**Targets**  
- ≥95% extraction completeness for the topic(s)  
- ≥90% BDD pass rate across core scenarios  
- Zero external API calls

**Activities**  
- Tune extraction prompts and tools.  
- Improve semantic framing and graph generation.  
- Track topic-per-hour throughput and error categories.  
- Generate at least 10 concrete improvement proposals.

---

#### Cycle 2 (Days 5–9) – Machine-Executable Conversion

**Goal**  
Convert BMJ knowledge into deployable, machine-executable modules (e.g., FHIR Clinical Reasoning + MCP services).

**Targets**  
- ≥98% BDD pass rate on core scenarios.  
- Direct BMJ → BMJ-KG mapping working for at least one topic.  
- ≥15 reusable tackle modules created.

**Activities**  
- Implement Hypothesis 2: direct mapping to BMJ’s KG spec.  
- Refactor pipeline to reduce reliance on intermediate manual tagging.  
- Harden BDD suites; expand coverage on edge cases.  
- Prioritise improvements by Time-to-Value (TTV).  

---

#### Day 10 – Final Evaluation & Retrospective

- Compare Baseline, Cycle 1, and Cycle 2 snapshots.  
- Review metrics (BDD, cycle time, hallucination rate, tackle count).  
- Capture a voyage retrospective and learning summary.  
- Update Santiago-core motivation vector and fleet backlog.

---

### 1.6 Success Criteria

| Metric                          | Target                                    |
|---------------------------------|-------------------------------------------|
| BDD pass rate (core scenarios)  | ≥98%                                      |
| Topic cycle time                | ≤18 minutes per topic                     |
| External API usage              | 0 after Day 0                             |
| Reusable tackle modules         | ≥15                                       |
| Domain correctness              | ≥96% alignment with BMJ ground truth      |

---

### 1.7 Reproducibility

From the repo root:

```bash
./voyages/launch_voyage.sh VOY-001-BMJ-Maiden
```

This script is responsible for configuring models, starting services, loading BMJ topics, and kicking off the voyage.

---

## 2. Canonical Voyage / Journey Model – Noesis Clipper

A **Journey** is a structured mission taken by Santiago and its crew to transform domain knowledge into executable intelligence in service to a customer.

### 2.1 Voyage Specification (YAML)

```yaml
voyage:
  id: string
  name: string
  domain: string
  customer: string | org | "Global Community"
  main_objective: string
  motivation_statement: "Be of maximum service to [customer] by achieving [objective]"
  constraints:
    max_duration_days: int
    budget_usd: int | 0
    compute_limit: "DGX-only | allowed-cloud"
    quality_gates:
      bdd_pass: ">=98%"
      provenance: ">=100%"
  goals:
    - description: string
      measure: string
      target: number
  team:
    roles:
      - PM
      - Architect
      - Researcher
      - Extractor
      - Developer
      - QA
      - Ethicist
    motivation_vector:
      service_to_customer: float
      craft: float
      curiosity: float
      urgency: float
      ethics: float
  cycles:
    design: "Baseline + Two-Cycle (Catch→Execute) + 24h micro-iterations"
  outputs:
    - semantic_graph
    - executable_modules
    - tackle
    - retrospective
    - improvement_proposals
  evaluation:
    retrospective_required: true
    metrics_to_capture:
      - bdd_pass
      - extraction_completeness
      - cycle_time
      - hallucination_rate
      - customer_satisfaction
  connections:
    expeditions: "daily micro-iterations"
    update_global_kg: true
```

---

## 3. Santiago-core Motivation Model – Version 1

### 3.1 Motivation Vector

```yaml
motivation_vector:
  service_to_customer: 0.85-1.0
  craft_excellence:    0.90-1.0
  curiosity:           0.60-0.95
  urgency:             0.50-0.95
  empathy:             0.70-1.0
  mission_integrity:   1.0
  learning_velocity:   tracked
```

### 3.2 Additional Santiago-core Properties

```yaml
santiago_core:
  motivation_engine:           active
  customer_empathy_module:     active
  reflection_loop:             mandatory
  learning_velocity_tracker:   active
  service_urgency_detector:    active
  mission_monitor:             active
```
