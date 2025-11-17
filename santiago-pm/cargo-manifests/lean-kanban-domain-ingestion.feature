---
artifact_type: cargo-manifest
title: Ingest Lean-Kanban Methodology Domain
status: ready
created: 2025-11-17
domain: lean_kanban
priority: high
estimated_effort: 2-3 weeks
triggered_by: santiago-pm/research-logs/2025-11-17-artifact-workflow-is-lean-kanban.md
related_artifacts:
  - santiago-pm/cargo-manifests/artifact-driven-workflow-orchestration.feature
  - knowledge/catches/external-pm-knowledge-extracted.md
tags: [domain-ingestion, lean, kanban, methodology, flow-management]
author: human-pm
---

# Cargo Manifest: Ingest Lean-Kanban Methodology Domain

## Feature Overview

Ingest Lean-Kanban methodology knowledge into Santiago's PM domain. Lean-Kanban is a **pull-based flow management system** that matches our artifact-driven workflow pattern. By extracting Kanban behaviors, Santiago can:
1. Understand and explain its own development process
2. Apply Kanban principles to optimize workflow
3. Measure and improve factory throughput

**Key Insight:** We're already USING Lean-Kanban (artifacts trigger work, status = kanban stages), but it's implicit. This makes it explicit.

## Business Value

**Why This Matters:**
- **Validates architecture:** Artifact-driven workflow = proven methodology (Lean-Kanban)
- **Improves factory:** Apply Kanban flow optimization to Santiago production
- **Enables measurement:** Track cycle time, throughput, identify bottlenecks
- **Completes PM knowledge:** Lean UX (discovery) + Lean Kanban (delivery) = full methodology

**ROI:**
- Faster domain ingestion (optimize flow → reduce cycle time)
- Higher quality catches (WIP limits → focused work)
- Better prioritization (explicit pull system → work on highest value)

## User Stories

### Story 1: Research Lean-Kanban Sources
```gherkin
Given Santiago needs to understand Lean-Kanban methodology
When we identify authoritative Lean-Kanban sources
Then we SHOULD fetch content from:
  | source                                        | key content                           |
  | David Anderson (LeanKanban.com)               | Core Kanban principles, classes       |
  | Mike Burrows (Kanban from the Inside)         | Inside-out perspective, patterns      |
  | Kanban University                             | Official practices, certification     |
  | Agile Alliance Kanban articles                | Community practices, case studies     |
  | Theory of Constraints (Eliyahu Goldratt)      | Flow optimization, bottlenecks        |
  | Toyota Production System                      | Lean manufacturing origins            |
And sources SHOULD be added to external PM knowledge ingestion pipeline
```

### Story 2: Extract Kanban Behaviors
```gherkin
Given Lean-Kanban source content has been fetched
When we run Catchfish extraction on Kanban knowledge
Then we SHOULD extract behaviors including:
  | behavior                    | description                                          |
  | visualize_workflow          | Create/maintain kanban board                         |
  | limit_wip                   | Set work-in-progress constraints per stage           |
  | manage_flow                 | Monitor cycle time, identify bottlenecks             |
  | make_policies_explicit      | Define stage transition criteria                     |
  | implement_feedback_loops    | Retrospectives, metrics reviews                      |
  | improve_collaboratively     | Team-driven process improvements                     |
  | measure_cycle_time          | Track artifact created → done duration              |
  | track_throughput            | Count artifacts completed per time period            |
  | identify_blockers           | Surface blocked artifacts, analyze causes            |
  | optimize_value_stream       | Map and improve end-to-end flow                      |
And each behavior SHOULD be mapped to PM domain ontology
And behaviors SHOULD have BDD scenarios for validation
```

### Story 3: Extend PM Domain Ontology with Kanban Concepts
```gherkin
Given Kanban behaviors have been extracted
When we extend the PM domain ontology
Then we SHOULD add Kanban-specific classes:
  | class           | description                                    |
  | KanbanBoard     | Visual workflow management system              |
  | WorkflowStage   | Stage in workflow (To Do, In Progress, Done)   |
  | WIPLimit        | Work-in-progress constraint for a stage        |
  | FlowMetric      | Cycle time, throughput, lead time measurements |
  | PullSignal      | Event that triggers work to be pulled          |
  | ValueStream     | End-to-end flow map                            |
And we SHOULD add Kanban-specific properties:
  | property        | domain            | range                  |
  | hasStage        | KanbanBoard       | WorkflowStage          |
  | hasWIPLimit     | WorkflowStage     | integer                |
  | currentWIP      | WorkflowStage     | integer                |
  | cycleTime       | Artifact          | duration               |
  | leadTime        | Artifact          | duration               |
  | pullsTrigger    | Artifact          | Agent/TeamMember       |
  | blockedBy       | Artifact          | Artifact (blocker)     |
And ontology version SHOULD be incremented to reflect Kanban layer
```

### Story 4: Map Santiago's Existing Workflow to Kanban
```gherkin
Given Santiago already uses artifact-driven workflow
When we analyze current process against Kanban principles
Then we SHOULD recognize:
  | santiago-pattern                    | kanban-equivalent                     |
  | Artifact created in domain folder   | Work item enters kanban board         |
  | Status transitions (open → done)    | Movement across kanban stages         |
  | Team member "pulls" artifact        | Pull-based work assignment            |
  | Multiple artifacts in progress      | Work-in-progress (WIP)                |
  | Artifacts wait for review           | Queue in Review stage                 |
And we SHOULD document mapping in knowledge base
And we SHOULD identify gaps (e.g., no explicit WIP limits)
```

## Acceptance Criteria

### AC1: Source Content Fetched
- [ ] David Anderson content fetched (LeanKanban.com articles, book summaries)
- [ ] Mike Burrows content fetched (Kanban from the Inside excerpts)
- [ ] Kanban University practices documented
- [ ] Agile Alliance Kanban articles collected
- [ ] Theory of Constraints (TOC) basics documented
- [ ] Toyota Production System context captured
- [ ] All sources stored in `knowledge/sources/lean-kanban/`

### AC2: Kanban Behaviors Extracted
- [ ] Minimum 10 Kanban-specific behaviors extracted
- [ ] Each behavior has: name, description, inputs, outputs, acceptance criteria
- [ ] Behaviors mapped to PM domain ontology classes
- [ ] BDD scenarios written for each behavior (3 scenarios x 10 behaviors = 30 scenarios)
- [ ] Behaviors integrated with existing PM behaviors (no conflicts)

### AC3: Ontology Extended
- [ ] Layer 10 created: "Flow Management" (Lean-Kanban concepts)
- [ ] 6+ new classes added (KanbanBoard, WorkflowStage, WIPLimit, etc.)
- [ ] 7+ new properties added (hasStage, cycleTime, pullsTrigger, etc.)
- [ ] Ontology validates without errors (RDF/OWL syntax check)
- [ ] Ontology version incremented to 1.3.0
- [ ] Namespace documented: `@prefix flow: <http://nusy.ai/ontology/flow#>`

### AC4: Santiago Workflow Mapped
- [ ] Document created: `santiago-pm/strategic-charts/santiago-kanban-mapping.md`
- [ ] Current artifact workflow diagrammed as Kanban board
- [ ] Status transitions mapped to Kanban stages
- [ ] WIP analysis performed (current WIP per domain)
- [ ] Flow metrics baseline established (cycle time for recent artifacts)
- [ ] Gaps identified (e.g., missing WIP limits, no cumulative flow diagram)

### AC5: Integration with Existing PM Knowledge
- [ ] Lean UX behaviors (from Task 18) linked to Kanban delivery flow
- [ ] User story mapping (Jeff Patton) integrated with Kanban prioritization
- [ ] ResearchOps (Nielsen Norman) connected to Kanban continuous improvement
- [ ] SAFe PO/PM practices aligned with Kanban at scale
- [ ] Consolidated PM methodology document created

## Technical Design

### Source Locations

```
knowledge/
└── sources/
    └── lean-kanban/
        ├── david-anderson/
        │   ├── kanban-principles.md
        │   ├── evolutionary-change.md
        │   └── classes-of-service.md
        ├── mike-burrows/
        │   ├── kanban-from-inside.md
        │   └── need-purpose-approach.md
        ├── kanban-university/
        │   ├── kanban-practices.md
        │   └── certification-levels.md
        ├── agile-alliance/
        │   └── kanban-articles.md
        └── related-methodologies/
            ├── theory-of-constraints.md
            └── toyota-production-system.md
```

### Ontology Layer 10: Flow Management

```turtle
@prefix flow: <http://nusy.ai/ontology/flow#> .
@prefix nusy: <http://nusy.ai/ontology#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

# Classes
flow:KanbanBoard
  rdf:type owl:Class ;
  rdfs:subClassOf nusy:PMTool ;
  rdfs:label "Kanban Board" ;
  rdfs:comment "Visual workflow management system showing work items across stages" .

flow:WorkflowStage
  rdf:type owl:Class ;
  rdfs:label "Workflow Stage" ;
  rdfs:comment "Stage in workflow (e.g., To Do, In Progress, Review, Done)" .

flow:WIPLimit
  rdf:type owl:Class ;
  rdfs:label "WIP Limit" ;
  rdfs:comment "Work-in-progress constraint for a workflow stage" .

flow:FlowMetric
  rdf:type owl:Class ;
  rdfs:label "Flow Metric" ;
  rdfs:comment "Measurement of flow efficiency (cycle time, throughput, lead time)" .

flow:PullSignal
  rdf:type owl:Class ;
  rdfs:label "Pull Signal" ;
  rdfs:comment "Event that triggers work to be pulled into a stage" .

flow:ValueStream
  rdf:type owl:Class ;
  rdfs:label "Value Stream" ;
  rdfs:comment "End-to-end flow map from discovery to delivery" .

# Properties
flow:hasStage
  rdf:type owl:ObjectProperty ;
  rdfs:domain flow:KanbanBoard ;
  rdfs:range flow:WorkflowStage .

flow:hasWIPLimit
  rdf:type owl:DatatypeProperty ;
  rdfs:domain flow:WorkflowStage ;
  rdfs:range xsd:integer .

flow:currentWIP
  rdf:type owl:DatatypeProperty ;
  rdfs:domain flow:WorkflowStage ;
  rdfs:range xsd:integer .

flow:cycleTime
  rdf:type owl:DatatypeProperty ;
  rdfs:domain nusy:Artifact ;
  rdfs:range xsd:duration .

flow:leadTime
  rdf:type owl:DatatypeProperty ;
  rdfs:domain nusy:Artifact ;
  rdfs:range xsd:duration .

flow:pullsTrigger
  rdf:type owl:ObjectProperty ;
  rdfs:domain nusy:Artifact ;
  rdfs:range nusy:Agent .

flow:blockedBy
  rdf:type owl:ObjectProperty ;
  rdfs:domain nusy:Artifact ;
  rdfs:range nusy:Artifact .
```

### Santiago Kanban Board Mapping

**Current Implicit Board:**
```
santiago-pm/
├── cargo-manifests/     # Features (All stages via status field)
│   ├── *.feature       # status: proposed → Backlog
│   ├── *.feature       # status: ready → Ready to Pull
│   ├── *.feature       # status: in-progress → In Progress
│   └── *.feature       # status: review → Review
├── ships-logs/          # Issues (same status progression)
├── research-logs/       # Research (same status progression)
└── navigation-charts/   # Plans (same status progression)
```

**Explicit Board (via CLI):**
```bash
nusy pm board

=== Santiago PM Kanban Board ===

📋 BACKLOG (WIP: 8, Limit: ∞)
  - cargo-manifests/artifact-driven-workflow.feature [proposed]
  - cargo-manifests/lean-kanban-ingestion.feature [proposed]
  - research-logs/tackle-pattern-discovery.md [proposed]
  ...

🎯 READY (WIP: 3, Limit: 5)
  - cargo-manifests/multi-strategy-bdd.feature [ready]
  - Task 16: Self-aware demo [ready]
  ...

🚧 IN PROGRESS (WIP: 2, Limit: 3) ⚠️ NEAR LIMIT
  - Task 15: Scaffold recognition [in-progress]
  - Task 18: External PM knowledge [in-progress]

🔍 REVIEW (WIP: 1, Limit: 2)
  - PRs #8-11 (GitHub agents) [review]

✅ DONE (Last 7 days: 5 artifacts)
  - Task 17: Vision knowledge extraction [done]
  - Task 18: External PM knowledge extraction [done]
  - Task 15: Scaffold recognition [done]
  ...

📊 FLOW METRICS
  - Avg Cycle Time: 2.5 days
  - Throughput: 5 artifacts/week
  - Blocked Items: 0
```

## Implementation Phases

### Phase 1: Source Research (Week 1)
- [ ] Identify authoritative Lean-Kanban sources
- [ ] Fetch web content or book summaries
- [ ] Create `knowledge/sources/lean-kanban/` structure
- [ ] Document key concepts, principles, practices

### Phase 2: Knowledge Extraction (Week 2)
- [ ] Run Catchfish on Lean-Kanban sources
- [ ] Extract 10+ Kanban behaviors
- [ ] Write behavior specifications (inputs, outputs, criteria)
- [ ] Create BDD scenarios for each behavior

### Phase 3: Ontology Extension (Week 2)
- [ ] Design Layer 10: Flow Management
- [ ] Add 6+ classes, 7+ properties
- [ ] Validate ontology syntax
- [ ] Update ontology version to 1.3.0
- [ ] Document namespace and usage

### Phase 4: Santiago Workflow Mapping (Week 3)
- [ ] Analyze current artifact workflow
- [ ] Map to Kanban board structure
- [ ] Measure current WIP per domain
- [ ] Calculate cycle time baselines
- [ ] Identify gaps and improvement opportunities

### Phase 5: Integration (Week 3)
- [ ] Link Lean UX + Lean Kanban behaviors
- [ ] Create unified PM methodology document
- [ ] Update MCP manifest with Kanban tools
- [ ] Implement `nusy pm board` CLI command (bonus)

## Success Metrics

**Coverage:**
- 10+ Kanban behaviors extracted
- 30+ BDD scenarios written
- 6+ ontology classes added
- 7+ ontology properties added

**Quality:**
- BDD pass rate ≥95% after validation
- Ontology validation passes
- All sources documented with provenance

**Impact:**
- Santiago workflow mapped to Kanban (100% coverage)
- WIP limits proposed for each domain
- Cycle time baseline established
- 3+ flow improvement opportunities identified

## Dependencies

**Builds on:**
- Task 18: External PM knowledge extraction (Lean UX foundation)
- Status tackle: Already provides status tracking (Kanban stages)
- Artifact metadata schema: YAML frontmatter for Kanban fields

**Blocks:**
- Artifact-driven workflow orchestration (needs Kanban foundation)
- Flow optimization initiatives (needs metrics baseline)
- Factory throughput measurement (needs Kanban concepts)

## Risks & Mitigation

**Risk 1: Source accessibility**
- Many Kanban books are copyrighted
- **Mitigation:** Focus on publicly available articles, summaries, official practices

**Risk 2: Over-complication**
- Kanban at scale (Kanban for multiple teams) may be too complex initially
- **Mitigation:** Start with core Kanban for single team (Santiago PM), scale later

**Risk 3: Integration conflicts**
- Kanban concepts may conflict with existing PM behaviors
- **Mitigation:** Careful ontology design, map relationships explicitly

## Next Steps

1. **Immediate:** Research David Anderson, Mike Burrows sources (public content)
2. **This week:** Create `knowledge/sources/lean-kanban/` and fetch initial content
3. **Next week:** Run Catchfish extraction, write BDD scenarios
4. **Following week:** Extend ontology, map Santiago workflow

---

## Metadata
```yaml
feature_id: F-025
version: 1.0.0
author: human-pm
reviewers: [santiago-architect, santiago-pm]
estimated_effort: 2-3 weeks
dependencies: [task-18-external-pm-knowledge, status-tackle]
triggered_by: research-logs/2025-11-17-artifact-workflow-is-lean-kanban.md
priority_score: 9.5/10 (critical for methodology validation)
```
