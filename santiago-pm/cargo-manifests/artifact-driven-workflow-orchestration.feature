---
artifact_type: cargo-manifest
title: Artifact-Driven Workflow Orchestration
status: proposed
created: 2025-11-17
domain: pm_workflow
priority: high
related_behaviors:
  - evaluate_artifacts_for_next_action
  - consult_specialists_on_decisions
  - orchestrate_team_based_on_discoveries
tags: [workflow, orchestration, event-driven, pm-core]
---

# Cargo Manifest: Artifact-Driven Workflow Orchestration

## Feature Overview

As a PM working in Santiago, discoveries during work generate artifacts (features, issues, research, tackle ideas). These artifacts are placed in domain folders (cargo-manifests/, ships-logs/, research-logs/, tackle/, etc.), which triggers awareness for relevant team members. The PM then evaluates the accumulated artifacts, consults with specialists, and decides the next action.

This is **event-driven product management** - artifacts are signals that drive workflow decisions.

## Business Value

**Why This Matters:**
- Captures organic discovery process (not just planned work)
- Makes implicit knowledge explicit (artifacts vs. lost context)
- Enables asynchronous collaboration (team members see artifacts when ready)
- PM has visibility into all work streams (centralized decision-making)
- Scales better than meetings (artifacts persist, can be reviewed anytime)

**Current Gap:**
- Santiago discovers patterns (like tackle = tools insight) but doesn't systematically:
  - Create corresponding artifacts
  - Notify relevant team members
  - Aggregate artifacts for PM review
  - Provide decision framework for "what next?"

## User Stories

### Story 1: Discovery Creates Artifacts
```gherkin
Given I am working on Task 15 (scaffold recognition)
When I discover that "tackle" represents reusable tools/implementations
Then I SHOULD create a research-log artifact documenting this insight
And the research-log SHOULD be tagged with relevant domains (tackle, meta-learning)
And team members interested in "tackle" SHOULD be notified
```

### Story 2: Artifacts Trigger Team Awareness
```gherkin
Given a new artifact is created in a domain folder
When the artifact is saved with appropriate tags/metadata
Then team members with roles matching those tags SHOULD be notified
And the artifact SHOULD appear in their work queue
And they MAY add comments, create related artifacts, or take action
```

### Story 3: PM Evaluates Artifacts for Next Action
```gherkin
Given multiple artifacts have been created across domain folders
When the PM runs an evaluation process
Then the system SHOULD:
  | capability                                          |
  | Aggregate all artifacts created since last review   |
  | Group artifacts by domain/theme                     |
  | Identify relationships between artifacts            |
  | Surface high-priority items (blocker issues, etc.)  |
  | Suggest consultation targets (specialists to ask)   |
And the PM SHOULD review the aggregated view
And the PM SHOULD consult with suggested specialists
And the PM SHOULD decide next action (new task, escalate, defer, etc.)
```

### Story 4: PM Decides and Communicates Next Action
```gherkin
Given the PM has evaluated artifacts and consulted specialists
When the PM decides on next action
Then the PM SHOULD create a navigation-chart (plan) artifact
And the navigation-chart SHOULD reference relevant artifacts as context
And the navigation-chart SHOULD specify:
  | field                   |
  | objective               |
  | assigned_team_members   |
  | dependencies            |
  | success_criteria        |
And team members SHOULD be notified of the new plan
```

## Acceptance Criteria

### AC1: Artifact Creation During Work
- [ ] Santiago creates artifacts during task execution (not just after)
- [ ] Artifacts include: research-logs (insights), ships-logs (blockers), cargo-manifests (feature ideas)
- [ ] Artifacts are tagged with domain, priority, related work
- [ ] Artifacts have YAML frontmatter for machine-readability

### AC2: Team Notification System
- [ ] System detects new artifacts in domain folders
- [ ] System identifies team members with relevant roles/interests
- [ ] System notifies via appropriate channel (could be file-based queue for now)
- [ ] Team members can subscribe to domains/tags

### AC3: PM Artifact Aggregation
- [ ] PM can run `nusy pm review-artifacts` command
- [ ] Command aggregates artifacts since last review (date-based)
- [ ] Artifacts grouped by: domain, priority, related themes
- [ ] Relationships visualized (e.g., research-log → suggests cargo-manifest)
- [ ] High-priority items surfaced (issues blocking work, etc.)

### AC4: Consultation Suggestion
- [ ] System suggests specialists to consult based on artifact domains
- [ ] Suggestions include: crew-manifest role holders, previous artifact authors
- [ ] PM can mark consultations as "done" and capture outcomes

### AC5: Decision Capture
- [ ] PM creates navigation-chart after evaluation
- [ ] Navigation-chart references source artifacts (traceability)
- [ ] Navigation-chart specifies team assignments
- [ ] System notifies assigned team members

## Technical Design

### Artifact Metadata Schema

Every artifact YAML frontmatter includes:
```yaml
artifact_type: [cargo-manifest|ships-log|research-log|navigation-chart|etc.]
title: "Descriptive title"
status: [proposed|in-progress|blocked|done|archived]
created: YYYY-MM-DD
domain: [pm_workflow|tackle|status|experiments|etc.]
priority: [low|medium|high|critical]
related_artifacts: [list of artifact IDs or paths]
tags: [list of searchable tags]
author: [team member or agent]
```

### Notification Mechanism (Phase 1: File-Based)

```
santiago-pm/
└── .notifications/
    ├── queue/
    │   ├── santiago-architect-001.yaml
    │   ├── santiago-developer-001.yaml
    │   └── human-pm-001.yaml
    └── subscriptions/
        ├── santiago-architect.yaml  # Subscribes to: tackle, architecture
        ├── santiago-developer.yaml  # Subscribes to: cargo-manifests, ships-logs
        └── human-pm.yaml            # Subscribes to: all
```

### PM Review Command

```bash
nusy pm review-artifacts [--since DATE] [--domain DOMAIN] [--priority PRIORITY]

# Examples:
nusy pm review-artifacts --since 2025-11-15
nusy pm review-artifacts --domain tackle --priority high
nusy pm review-artifacts  # All new since last review
```

Output:
```
=== PM Artifact Review ===
Since: 2025-11-15
Total artifacts: 12

📁 By Domain:
  tackle (5 artifacts)
    - research-log: "Tackle represents reusable tools" (high priority)
    - cargo-manifest: "Scaffold recognition system" (high priority)
    ...
  
  status (3 artifacts)
    - ships-log: "Status transitions need validation" (medium)
    ...

🔗 Relationships Detected:
  - research-log (tackle insight) → suggests → cargo-manifest (scaffold feature)
  - ships-log (status validation) → blocks → cargo-manifest (status MCP tool)

🚨 High Priority Items (2):
  1. Research-log: "Tackle represents reusable tools" (tackle domain)
  2. Cargo-manifest: "Scaffold recognition system" (meta-learning domain)

💬 Suggested Consultations:
  - Santiago-Architect: Review tackle/meta-learning design
  - Santiago-Developer: Estimate scaffold implementation effort
  
📋 Recommended Next Action:
  - Create navigation-chart for Task 15 (scaffold system implementation)
  - Consult Santiago-Architect on tackle abstraction patterns
```

### Artifact Graph

Build knowledge graph relationships:
```turtle
:ResearchLog_TackleInsight
  rdf:type nusy:ResearchLog ;
  nusy:suggests :CargoManifest_ScaffoldFeature ;
  nusy:hasDomain :TackleDomain ;
  nusy:hasPriority "high" .

:CargoManifest_ScaffoldFeature
  rdf:type nusy:CargoManifest ;
  nusy:basedOn :ResearchLog_TackleInsight ;
  nusy:requiresConsultation :SantiagoArchitect ;
  nusy:status "proposed" .
```

## Implementation Phases

### Phase 1: Artifact Creation & Metadata (Week 1)
- [ ] Define YAML frontmatter schema for all artifact types
- [ ] Update artifact templates with metadata fields
- [ ] Create utility to validate artifact metadata
- [ ] Document metadata conventions

### Phase 2: File-Based Notification System (Week 2)
- [ ] Create `.notifications/` folder structure
- [ ] Implement artifact watcher (detects new files)
- [ ] Generate notification files in queues
- [ ] Create subscription configuration

### Phase 3: PM Review Command (Week 3)
- [ ] Implement `nusy pm review-artifacts` CLI
- [ ] Artifact aggregation logic
- [ ] Relationship detection (via tags, explicit references)
- [ ] Priority surfacing
- [ ] Consultation suggestions

### Phase 4: Decision Capture (Week 4)
- [ ] Navigation-chart template with artifact references
- [ ] `nusy pm decide` command to create plans
- [ ] Team member assignment logic
- [ ] Notification on plan creation

### Phase 5: Knowledge Graph Integration (Future)
- [ ] Import artifacts into KG with relationships
- [ ] Query KG for artifact patterns
- [ ] Visualize artifact flow over time
- [ ] Measure: artifact→decision time, consultation effectiveness

## Success Metrics

**Process Efficiency:**
- Time from discovery → artifact creation: < 5 minutes
- Time from artifact → PM review: < 24 hours
- Time from review → decision: < 1 hour (with consultations)

**Visibility:**
- % of discoveries that become artifacts: > 80%
- % of artifacts referenced in decisions: > 60%
- % of consultations captured: > 90%

**Collaboration:**
- Avg # of team members notified per artifact: 1-3
- Avg # of consultations per decision: 2-4
- Artifact comment/response rate: > 50%

## Related Work

**Similar Patterns:**
- Event-driven architecture (artifacts = events)
- Kanban pull systems (artifacts pulled into work queues)
- GitHub Issues/PRs (artifacts trigger reviews, discussions)
- JIRA workflow (issue states trigger team actions)

**Santiago Context:**
- This extends Navigation-charts (plans) with artifact-driven triggers
- Complements Status system (artifacts have statuses)
- Integrates with Knowledge Graph (artifacts are KG nodes)

## Questions & Risks

**Questions:**
- How frequently should PM run review-artifacts? (daily? per task? on-demand?)
- Should artifacts auto-escalate if not reviewed within SLA?
- What's the balance between artifact creation overhead vs. lost context?

**Risks:**
- **Artifact overload:** Too many artifacts = PM can't process (mitigation: priority filtering, auto-archiving)
- **Notification fatigue:** Team members ignore notifications (mitigation: smart filtering, digest mode)
- **Context loss:** Artifacts lack sufficient detail (mitigation: templates enforce detail, review checklist)

## Next Steps

1. **Immediate:** Capture Task 15 discovery (tackle = tools) as research-log artifact
2. **This Sprint:** Implement Phase 1 (metadata schema) for all artifact types
3. **Next Sprint:** Build PM review command (Phase 3) for manual review process
4. **Future:** Automate with KG queries and agent-based consultation

---

## Metadata
```yaml
feature_id: F-024
version: 1.0.0
author: human-pm
reviewers: [santiago-architect, santiago-pm]
estimated_effort: 4 weeks
dependencies: [status-system, knowledge-graph]
```
