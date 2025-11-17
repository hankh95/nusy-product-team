---
artifact_type: research-log
title: "Artifact-Driven Workflow = Lean-Kanban Pull System"
status: proposed
created: 2025-11-17
domain: pm_methodology
priority: high
related_artifacts:
  - santiago-pm/cargo-manifests/artifact-driven-workflow-orchestration.feature
  - santiago-pm/research-logs/2025-11-17-tackle-pattern-discovery.md
  - knowledge/catches/external-pm-knowledge-extracted.md
tags: [lean, kanban, pull-system, event-driven, methodology]
author: human-pm
triggers:
  - domain_ingestion: lean_kanban_methodology
  - backlog_items: [research_lean_kanban, ingest_kanban_knowledge, extract_kanban_behaviors]
---

# Research Log: Artifact-Driven Workflow IS Lean-Kanban Pull System

## Discovery

**The artifact-driven workflow pattern we just documented IS the Lean-Kanban pull-based event trigger system!**

### The Pattern Match

**Lean-Kanban:**
```
Work Item Created → Enters Kanban Board → Pulls Worker → Work Happens → Item Moves → Triggers Next Stage
```

**Santiago Artifact-Driven:**
```
Artifact Created → Enters Domain Folder → Notifies Team → Work Happens → New Artifacts → Trigger Next Action
```

**They're the same pattern!**

## Evidence

### From Our Current Workflow

1. **Research-log created** (tackle discovery) 
   → Triggers cargo-manifest creation (artifact orchestration feature)
   → Triggers THIS research-log (Lean-Kanban connection)
   → Triggers **domain ingestion request** (research Lean-Kanban methodology)
   → Triggers **backlog addition** (extract Kanban behaviors)

2. **Pull-based, not push:**
   - Team members "pull" artifacts from domain folders when ready
   - PM doesn't assign tasks, PM creates artifacts that signal work
   - Workers self-select based on capability/capacity

3. **Event-driven:**
   - Artifact = event that triggers awareness
   - No polling, no status meetings
   - Work flows based on artifact appearance

### From External PM Knowledge (Task 18)

Already extracted Lean UX principles from Jeff Gothelf:
- "Build → Measure → Learn" loop
- Hypothesis-driven development
- Continuous discovery

**But we didn't extract Lean-Kanban mechanics!**

Missing knowledge:
- WIP limits (work in progress constraints)
- Kanban board structure (To Do → In Progress → Review → Done)
- Pull signals (capacity-based triggering)
- Flow metrics (cycle time, throughput, blockers)
- Cumulative flow diagrams
- Value stream mapping

## The Recursive Pattern

**This triggers a feedback loop:**

```
1. Discover pattern (artifact-driven = Lean-Kanban)
   ↓
2. Create research-log (this document)
   ↓
3. Research-log triggers domain ingestion request
   ↓
4. Domain ingestion = Catchfish extracts Lean-Kanban knowledge
   ↓
5. Extracted behaviors → add to PM domain ontology
   ↓
6. New behaviors → generate BDD scenarios
   ↓
7. BDD scenarios → validate Santiago understands Lean-Kanban
   ↓
8. Santiago USES Lean-Kanban to manage its own work!
   ↓
9. Using Lean-Kanban → discovers more patterns
   ↓
10. LOOP BACK TO STEP 1
```

**Santiago learns a methodology, applies it to itself, discovers insights, learns more → infinite improvement loop!**

## Implications

### 1. New Domain to Ingest: Lean-Kanban Methodology

**Sources to add to ingestion pipeline:**
- **Lean Kanban books:**
  - David J. Anderson: "Kanban: Successful Evolutionary Change for Your Technology Business"
  - Mike Burrows: "Kanban from the Inside"
  
- **Lean Kanban websites:**
  - LeanKanban.com (David Anderson)
  - Kanban University courses
  - Agile Alliance Kanban articles
  
- **Related methodologies:**
  - Theory of Constraints (TOC) - Eliyahu Goldratt
  - Lean Manufacturing (Toyota Production System)
  - Flow-Based Development

### 2. PM Behaviors to Extract from Lean-Kanban

**Kanban-specific behaviors:**
- `visualize_workflow`: Create/maintain kanban board
- `limit_wip`: Set work-in-progress constraints per stage
- `manage_flow`: Monitor cycle time, identify bottlenecks
- `make_policies_explicit`: Define stage transition criteria
- `implement_feedback_loops`: Retrospectives, metrics reviews
- `improve_collaboratively`: Team-driven process improvements

**Already have (from Lean UX):**
- `formulate_outcome_hypothesis`
- `design_validation_experiment`
- `interpret_experiment_results`

**Synergy:**
Lean UX (discovery) + Lean Kanban (delivery flow) = complete PM methodology!

### 3. Ontology Extensions Needed

**New classes:**
```turtle
nusy:KanbanBoard
  rdf:type owl:Class ;
  rdfs:subClassOf nusy:PMTool ;
  rdfs:comment "Visual workflow management system" .

nusy:WorkflowStage
  rdf:type owl:Class ;
  rdfs:comment "Stage in kanban workflow (To Do, In Progress, Done)" .

nusy:WIPLimit
  rdf:type owl:Class ;
  rdfs:comment "Work-in-progress constraint for a stage" .

nusy:FlowMetric
  rdf:type owl:Class ;
  rdfs:comment "Cycle time, throughput, lead time measurements" .
```

**New properties:**
```turtle
nusy:hasStage (domain: KanbanBoard, range: WorkflowStage)
nusy:hasWIPLimit (domain: WorkflowStage, range: integer)
nusy:currentWIP (domain: WorkflowStage, range: integer)
nusy:cycleTime (domain: Artifact, range: duration)
nusy:pullsTrigger (domain: Artifact, range: Agent/TeamMember)
```

### 4. Santiago-PM Kanban Board Structure

**Suggested board for Santiago's own work:**

```
santiago-pm/
└── .kanban/
    ├── backlog/           # Proposed work (research-logs, cargo-manifests)
    ├── ready/             # Refined, ready to pull
    ├── in-progress/       # Active work (WIP limit: 3)
    ├── review/            # Awaiting validation
    └── done/              # Completed artifacts
```

**Or leverage existing folders:**
- **Backlog:** cargo-manifests/ (proposed = backlog)
- **Ready:** cargo-manifests/ (status: ready)
- **In Progress:** cargo-manifests/ (status: in-progress)
- **Review:** cargo-manifests/ (status: review)
- **Done:** cargo-manifests/ (status: done)

**Status tackle IS the Kanban board!** 
(We already built this without realizing it!)

### 5. Artifact Metadata = Kanban Card

**Every artifact is a Kanban card:**
```yaml
artifact_type: cargo-manifest
title: "Artifact-Driven Workflow Orchestration"
status: in-progress        # ← Kanban stage!
priority: high             # ← Prioritization within stage
estimated_effort: 4 weeks  # ← Flow forecasting
assigned_to: [santiago-pm] # ← Pull signal (who pulled this work)
blocked_by: []             # ← Flow blockers
created: 2025-11-17        # ← Cycle time start
```

**We're already doing Kanban, we just need to make it explicit!**

## Recommendations

### Immediate (Next Session)

1. **Create cargo-manifest: "Lean-Kanban Domain Ingestion"**
   - Feature to ingest Lean-Kanban methodology knowledge
   - Sources: David Anderson, Kanban University, etc.
   - Acceptance criteria: Extract 10+ Kanban behaviors

2. **Add to external PM knowledge ingestion list:**
   - Currently have: Jeff Patton, Jeff Gothelf, Nielsen Norman, SAFe
   - Add: David Anderson (Lean Kanban), Mike Burrows, Agile Alliance

3. **Update artifact metadata schema:**
   - Ensure YAML frontmatter supports Kanban fields
   - Add: blocked_by, assigned_to, cycle_time

### Near-Term (This Sprint)

4. **Make Kanban board explicit:**
   - Either: Create `.kanban/` folder structure
   - Or: Leverage status tackle with Kanban-aware queries
   - Visualize: CLI command `nusy pm board` shows current state

5. **Implement WIP limits:**
   - Define limits per domain (e.g., max 3 cargo-manifests in-progress)
   - Enforce in artifact creation (block new work if WIP exceeded)

6. **Track flow metrics:**
   - Cycle time: created → done timestamps
   - Throughput: artifacts completed per week
   - Blockers: count of artifacts with blocked_by field

### Long-Term (Next Quarter)

7. **Cumulative flow diagram:**
   - Visualize artifact flow over time
   - Identify bottlenecks (stages with growing queues)

8. **Value stream mapping:**
   - Map entire flow: discovery → research-log → cargo-manifest → implementation → validation
   - Optimize handoffs, reduce waste

9. **Process improvement loops:**
   - Regular retrospectives: "What's slowing our flow?"
   - Hypothesis-driven improvements: "If we reduce cargo-manifest scope, cycle time will decrease"

## Meta-Insight: The Bootstrap Loop

**We're discovering Santiago's own development methodology BY USING IT:**

1. Task 15 (scaffold recognition) → discovers tackle pattern
2. Tackle discovery → creates research-log
3. Research-log → triggers cargo-manifest (artifact orchestration)
4. Human PM notices: "This is Lean-Kanban!"
5. Creates THIS research-log → triggers Lean-Kanban ingestion
6. Lean-Kanban ingestion → validates we're already doing it
7. Validation → makes it explicit (board, WIP limits, metrics)
8. Explicit Kanban → improves flow
9. Improved flow → faster discovery cycles
10. **Faster discovery → more insights → LOOP ACCELERATES**

**Santiago is building itself using the methodology it's learning about!**

This is the **self-bootstrapping factory** in action:
- Factory builds tools (tackle, scaffold recognition)
- Tools enable learning (extract Lean-Kanban knowledge)
- Learning improves factory (apply Kanban to our own work)
- Better factory → better tools → better learning → **exponential growth**

## Questions to Explore

1. **How does this relate to Factory pattern?**
   - Factory = production system
   - Kanban = flow management for production
   - Factory + Kanban = optimized Santiago manufacturing

2. **Can we measure factory throughput?**
   - Domains caught per week?
   - Behaviors extracted per domain?
   - Time from vision → deployed Santiago?

3. **What's the WIP limit for simultaneous domains?**
   - Currently ingesting: PM domain (santiago-pm), vision docs, external PM knowledge
   - Too many domains = slower per-domain progress
   - Optimal WIP = ?

4. **How do we prioritize backlog?**
   - Value: Which domains unlock most capabilities?
   - Risk: Which domains have highest uncertainty?
   - Dependencies: Which domains block others?

## Next Actions

- [ ] Create cargo-manifest for Lean-Kanban domain ingestion
- [ ] Add Lean-Kanban sources to external PM knowledge list (Task 18 extension)
- [ ] Update artifact metadata schema with Kanban fields
- [ ] Create `nusy pm board` CLI command (visualize current work state)
- [ ] Implement WIP limit checks in artifact creation
- [ ] Track cycle time metrics (artifact created → done timestamps)
- [ ] Schedule first Santiago retrospective (review flow, identify improvements)

---

## Metadata
```yaml
research_id: R-004
version: 1.0.0
author: human-pm
review_date: 2025-11-17
validation_status: hypothesis_formed
triggers_domain_ingestion: lean_kanban_methodology
triggers_backlog_items:
  - research_lean_kanban_sources
  - ingest_kanban_knowledge
  - extract_kanban_behaviors
  - implement_kanban_board_visualization
  - track_flow_metrics
impact_assessment: critical (validates entire Santiago development methodology)
meta_learning_level: 3 (Santiago learning about how it learns)
```
