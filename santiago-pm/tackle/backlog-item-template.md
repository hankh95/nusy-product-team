# Backlog Item Template

**Usage**: Copy this template when creating new backlog items.

```yaml
---
artifact_type: backlog-item
id: BI-XXX  # Auto-generated or manual
title: "Short descriptive title"
status: proposed  # proposed | ready | in-progress | review | done | cancelled
priority_score: 0.0  # Calculated by Santiago (0.0-1.0)
priority_rank: 0     # Position in backlog (1 = highest)
estimated_effort: 0  # Story points (Fibonacci: 1,2,3,5,8,13,21)
actual_effort: null  # Filled when done
created: YYYY-MM-DDTHH:MM:SSZ
refined: null  # When Three Amigos refined it
started: null
completed: null
cycle_time: null      # Calculated: started → completed
lead_time: null       # Calculated: created → completed

# Neurosymbolic prioritization factors (calculated by Santiago)
customer_value: 0.0   # From hypothesis confidence in research-logs
unblock_impact: 0.0   # Number of downstream items this unblocks (normalized)
worker_availability: 0.0  # Skill match with available workers
learning_value: 0.0   # How much uncertainty this reduces

# Assignment & capacity
assigned_to: []  # Who pulled this work
required_skills: []  # Skills needed (e.g., UXR, PM, DevOps, ML)
blocked_by: []       # IDs of blocking items (e.g., [BI-012])
blocks: []           # IDs of items this blocks (e.g., [BI-043, BI-044])

# Relationships
related_to: []       # Related artifacts (research-logs, cargo-manifests, etc.)
triggered_by: null   # What caused this to be created
extracts_to: []      # Artifacts created from this work (filled during work)

# Three Amigos refinement
product_owner_notes: |
  User story: As [role], I want [capability] so that [benefit].
  
  Hypothesis: If [we build this], then [outcome will happen].
  
  Value: [Why this matters to customers/team]
  
  Success Metrics:
  - [Measurable outcome 1]
  - [Measurable outcome 2]

developer_notes: |
  Technical approach: [How we'll build this]
  
  Estimated effort: [Why this story point estimate]
  
  Dependencies: [What needs to happen first]
  
  Risks: [Technical risks or unknowns]

tester_notes: |
  Acceptance criteria:
  - [ ] AC1: [Specific testable criterion]
  - [ ] AC2: [Specific testable criterion]
  - [ ] AC3: [Specific testable criterion]
  
  Test scenarios: [What scenarios to test]

# Flow metrics
wip_stage: backlog   # Which Kanban stage: backlog | ready | in-progress | review | done
wip_limit: null      # Limit for current stage (if enforced)
cumulative_flow: []  # History of stage transitions (auto-populated)

tags: []  # Keywords for filtering/searching
---

# [Backlog Item Title]

## User Story

As **[role]**, I want **[capability]** so that **[benefit]**.

## Hypothesis

If [we build this], then [outcome will happen], measured by [metric].

## Product Owner Perspective

**Value**: [Why this matters]

**Success Metrics**:
- [Measurable outcome 1]
- [Measurable outcome 2]
- [Measurable outcome 3]

## Developer Perspective

**Technical Approach**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Estimated Effort**: [X story points] ([size label]: small/medium/large)

**Dependencies**: [What needs to happen first, or "None"]

**Risks**: [Technical risks, or "Low"]

## Tester Perspective

**Acceptance Criteria**:
- [ ] AC1: [Specific testable criterion]
- [ ] AC2: [Specific testable criterion]
- [ ] AC3: [Specific testable criterion]

**Test Scenarios**: [What scenarios to test]

## Implementation Notes

[Fill this in during development - decisions made, challenges encountered, learnings]

## Related Artifacts

- **Research Log**: [Link if exists]
- **Feature Spec**: [Link if exists]
- **Ontology**: [Link if extended]
- **Dependencies**: [Links to blocking items]
```

---

## Example: Filled Backlog Item

```yaml
---
artifact_type: backlog-item
id: BI-042
title: "Neurosymbolic Backlog Prioritization Algorithm"
status: in-progress
priority_score: 0.85
priority_rank: 1
estimated_effort: 5
actual_effort: null
created: 2025-11-17T09:00:00Z
refined: 2025-11-17T10:30:00Z
started: 2025-11-17T11:00:00Z
completed: null
cycle_time: null
lead_time: null

customer_value: 0.9
unblock_impact: 0.6
worker_availability: 0.8
learning_value: 0.7

assigned_to: [santiago-pm]
required_skills: [neurosymbolic-reasoning, probabilistic-evaluation, KG-queries]
blocked_by: []
blocks: [BI-043, BI-044]

related_to: 
  - santiago-pm/research-logs/2025-11-17-artifact-workflow-is-lean-kanban.md
  - santiago-pm/cargo-manifests/lean-kanban-domain-ingestion.feature
triggered_by: user-request
extracts_to: []

product_owner_notes: |
  User story: As Santiago PM, I want intelligent prioritization
  so that I work on the most valuable items without manual analysis.
  
  Hypothesis: If Santiago uses neurosymbolic reasoning to prioritize,
  then Santiago will maximize effectiveness and team health.
  
  Value: Eliminates manual prioritization (saves 2-4 hours/week),
  reduces context switching, improves team morale.
  
  Success Metrics:
  - Cycle time reduces by 20%
  - Worker idle time < 5%
  - 90% of completed work was top 3 priority

developer_notes: |
  Technical approach: Query KG for state, calculate weighted score,
  return sorted backlog with rationale. Use existing reasoner.
  
  Estimated effort: 5 story points (medium complexity, well-scoped)
  
  Dependencies: None (KG and reasoner already exist)
  
  Risks: Low (algorithm is straightforward, BDD scenarios will validate)

tester_notes: |
  Acceptance criteria:
  - [ ] Algorithm queries KG for 4 factors
  - [ ] Score uses correct weights (0.4/0.3/0.2/0.1)
  - [ ] Explanation generated for each score
  - [ ] BDD scenarios pass
  
  Test scenarios: Happy path, edge cases, error handling

wip_stage: in-progress
wip_limit: 3
cumulative_flow:
  - {stage: backlog, entered: "2025-11-17T09:00:00Z", exited: "2025-11-17T10:30:00Z"}
  - {stage: ready, entered: "2025-11-17T10:30:00Z", exited: "2025-11-17T11:00:00Z"}
  - {stage: in-progress, entered: "2025-11-17T11:00:00Z", exited: null}

tags: [neurosymbolic, prioritization, lean-kanban, three-amigos, high-value]
---

# Neurosymbolic Backlog Prioritization Algorithm

## User Story

As **Santiago PM**, I want **intelligent backlog prioritization** so that **I work on the most valuable items without manual analysis**.

## Hypothesis

If Santiago uses neurosymbolic reasoning to prioritize work based on KG state (available workers, dependencies, customer value), then Santiago will maximize effectiveness (doing the right things) and team health (no idle/overloaded workers).

## Product Owner Perspective

**Value**: Eliminates manual prioritization (saves 2-4 hours/week), reduces context switching (work on most impactful items), improves team morale (fair work distribution).

**Success Metrics**:
- Cycle time reduces by 20% (better work selection)
- Worker idle time < 5% (always has suitable work)
- Backlog items completed in priority order 90% of the time

## Developer Perspective

**Technical Approach**:
1. Query KG for current state (workers, dependencies, hypotheses, capacity)
2. Calculate priority score using weighted formula
3. Sort backlog by score
4. Generate explanation for each item
5. Return prioritized list with rationale

**Estimated Effort**: 5 story points (medium)

**Dependencies**: None (KG and reasoner already exist)

**Risks**: Low (algorithm is straightforward, BDD scenarios will validate)

## Tester Perspective

**Acceptance Criteria**:
- [ ] Algorithm queries KG for 4 factors (workers, dependencies, value, capacity)
- [ ] Priority score uses correct weights (0.4, 0.3, 0.2, 0.1)
- [ ] Explanation generated for each score (provenance + rationale)
- [ ] BDD scenarios pass (happy path, edge cases, error handling)
- [ ] Integration test: Full backlog prioritization end-to-end

## Implementation Notes

2025-11-17 11:00 - Started work. Created cargo manifest first to scope the full feature. Algorithm design is straightforward - the magic is in the KG queries. Will use existing neurosymbolic reasoner for probabilistic evaluation.

## Related Artifacts

- **Research Log**: artifact-workflow-is-lean-kanban.md (discovered we're already doing Kanban)
- **Feature**: lean-kanban-domain-ingestion.feature (extract Kanban behaviors)
- **Cargo Manifest**: neurosymbolic-backlog-management.feature (this feature's parent)
```

---

## Fields Explained

### Status Flow

```
proposed → ready → in-progress → review → done
                              ↓
                          cancelled
```

- **proposed**: New backlog item, not yet refined
- **ready**: Three Amigos complete, ready to pull
- **in-progress**: Worker actively working on this
- **review**: Work complete, awaiting approval
- **done**: Accepted and shipped
- **cancelled**: No longer needed

### Priority Score (0.0-1.0)

Calculated by Santiago's neurosymbolic algorithm:
- **0.9-1.0**: CRITICAL (drop everything)
- **0.7-0.9**: HIGH (top 3 priority)
- **0.4-0.7**: MEDIUM (important but not urgent)
- **0.0-0.4**: LOW (nice to have)

Formula:
```
priority_score = 
  (customer_value * 0.4) +
  (unblock_impact * 0.3) +
  (worker_availability * 0.2) +
  (learning_value * 0.1)
```

### Effort Estimation (Fibonacci)

- **1 pt**: Trivial (< 1 hour)
- **2 pts**: Small (2-4 hours)
- **3 pts**: Medium (1 day)
- **5 pts**: Large (2-3 days)
- **8 pts**: Very large (1 week) - consider breaking down
- **13 pts**: Epic (2 weeks) - MUST break down
- **21 pts**: Too large - break into smaller items

### Required Skills

Common skills in Santiago ecosystem:
- **UXR**: User experience research
- **PM**: Product management
- **Architecture**: System design
- **Knowledge Engineer**: Ontology, KG, domain modeling
- **DevOps**: CI/CD, deployment, infrastructure
- **ML**: Machine learning, neurosymbolic AI
- **Documentation**: Writing, technical docs
- **Testing**: BDD scenarios, test design

### Cycle Time vs Lead Time

- **Lead Time**: created → completed (total time in system)
- **Cycle Time**: started → completed (actual work time)
- **Refinement Time**: created → refined (grooming duration)

### WIP Limits

Recommended limits for Santiago PM workflow:
- **backlog**: ∞ (unlimited proposals)
- **ready**: 10 (groomed and ready to pull)
- **in-progress**: 3 (limit context switching)
- **review**: 5 (don't overwhelm reviewers)
- **done**: ∞ (archive of completed work)

### Cumulative Flow

Tracks item's journey through Kanban stages:
```yaml
cumulative_flow:
  - {stage: backlog, entered: "2025-11-17T09:00:00Z", exited: "2025-11-17T10:30:00Z"}
  - {stage: ready, entered: "2025-11-17T10:30:00Z", exited: "2025-11-17T11:00:00Z"}
  - {stage: in-progress, entered: "2025-11-17T11:00:00Z", exited: null}
```

This enables:
- Cycle time calculation per stage
- Bottleneck identification (long stage duration)
- Cumulative flow diagrams (CFD)
- Flow efficiency analysis

---

## Tips for Effective Backlog Items

### Good User Stories

✅ **Good**: "As a PM agent, I want automated prioritization so that I can focus on high-value work"

❌ **Bad**: "Build prioritization algorithm" (no role, benefit, or context)

### Good Hypotheses

✅ **Good**: "If we add neurosymbolic prioritization, then cycle time will reduce by 20%, measured by avg(completed - started)"

❌ **Bad**: "Prioritization will be better" (not measurable, vague outcome)

### Good Acceptance Criteria

✅ **Good**: "Algorithm queries KG for 4 factors and returns priority_score between 0.0-1.0"

❌ **Bad**: "Prioritization works correctly" (not testable, subjective)

### Effective Tags

Use tags for:
- **Themes**: neurosymbolic, lean-kanban, automation
- **Domains**: pm-workflow, knowledge-engineering, UXR
- **Types**: bug-fix, feature, improvement, research
- **Urgency**: critical, high-value, technical-debt
- **Skills**: requires-ml, requires-devops, beginner-friendly

---

## Related Templates

- **cargo-manifest-template.md**: For larger features (epics)
- **research-log-template.md**: For investigations
- **questionnaire-template.md**: For discovery interviews
- **ships-log-template.md**: For task completion reports

---

**Meta**: This template itself is an artifact (artifact_type: template) that enables backlog management. It's neurosymbolic-friendly (structured YAML + human narrative) and Lean-Kanban-aligned (Three Amigos sections, flow metrics).
