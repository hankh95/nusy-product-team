# Noesis Clipper Voyage / Journey Model Specification

A **Voyage** is a structured journey where Santiago and its crew work on a specific domain with a clear customer, objective, and set of constraints. Each voyage is designed to both serve the customer and improve Santiago-core itself.

## 1. Concept

- Every voyage has a **domain**, **customer**, **main objective**, **constraints**, **goals**, **team**, **cycles**, **outputs**, and **evaluation**.
- Voyages are the primary unit of value delivery and learning in the Noesis Clipper architecture.
- Expeditions (micro-iterations) sit inside voyages; voyages roll up to a long-term program.

## 2. YAML Specification

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

## 3. Usage

- Each new clinical or product domain expedition defines a voyage YAML using this schema.
- The voyage definition feeds Santiago-core’s orchestration layer, motivation engine, and evaluation harness.
- Retrospectives and metrics update the global backlog and influence future voyages.
