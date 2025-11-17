# Cargo Manifest: Neurosymbolic Backlog Management

**Date**: 2025-11-17
**Type**: Feature
**Status**: in-progress
**Priority**: high
**Domain**: pm-workflow
**Triggered By**: User request for Lean-Kanban backlog + Three Amigos pattern

---

## Feature Overview

Build an **intelligent backlog management system** that uses neurosymbolic reasoning to prioritize work based on:
- **Available capacity** (who can work now?)
- **Work dependencies** (what's blocked by what?)
- **Customer value** (what serves our users best?)
- **Team health** (no one sits idle, no one is overwhelmed)

**Key Innovation**: Instead of static WSJF (Weighted Shortest Job First) or manual prioritization, Santiago uses its **knowledge graph** to dynamically calculate optimal work order. This maximizes **effectiveness** (doing the right things) over **efficiency** (doing things fast).

### The Three Amigos Pattern

**Classic Three Amigos** (Agile ceremony):
- **Product Owner**: Describes the feature ("what" and "why")
- **Developer**: Assesses technical approach ("how")
- **Tester**: Defines acceptance criteria ("done when...")

**Santiago's Neurosymbolic Three Amigos**:
- **Knowledge Graph**: All assets loaded (features, issues, workers, dependencies)
- **Probabilistic Reasoner**: Calculates optimal priority based on current state
- **Human Collaborator**: Validates AI's recommendations, provides context

**Meeting Flow**:
1. Review backlog items (santiago lists all proposed work)
2. Initial UX research (santiago extracts feature descriptions or hypotheses)
3. Break down work (santiago proposes tasks and estimates)
4. Prioritize (santiago calculates scores, human adjusts, consensus emerges)
5. Assign pull rights (workers "pull" from top of prioritized backlog)

---

## User Stories

### Story 1: Neurosymbolic Backlog Prioritization

```gherkin
Feature: Neurosymbolic Backlog Prioritization
  Santiago uses its knowledge graph to intelligently prioritize work
  based on available capacity, dependencies, value, and team health

  Background:
    Given Santiago PM KG contains:
      | entity_type     | count | status              |
      | backlog_items   | 25    | proposed            |
      | workers         | 5     | available/busy      |
      | dependencies    | 12    | blocking relations  |
      | customer_needs  | 8     | validated hypotheses|
    And Santiago can query KG for real-time state

  Scenario: Calculate optimal work priority (Neurosymbolic Power!)
    Given backlog contains 25 proposed work items
    And Santiago queries KG for:
      | query_type            | result                                    |
      | available_workers     | 2 workers idle, 3 workers at 80% capacity|
      | work_dependencies     | 5 items blocked, 12 items ready          |
      | customer_value_scores | 8 validated hypotheses with metrics      |
      | team_capacity         | 120 story points remaining this sprint   |
    When Santiago calculates priority scores
    Then Santiago uses probabilistic evaluation:
      """
      priority_score = 
        (customer_value * 0.4) +
        (unblock_impact * 0.3) +
        (worker_availability * 0.2) +
        (learning_value * 0.1)
      
      where:
      - customer_value: KG evidence of user need (hypothesis confidence)
      - unblock_impact: Number of downstream items this unblocks
      - worker_availability: Match skills to available capacity
      - learning_value: Does this reduce uncertainty?
      """
    And top 5 items SHOULD have priority_score > 0.7
    And blocked items SHOULD be deprioritized automatically
    And items requiring unavailable workers SHOULD be postponed
    And Santiago SHOULD explain reasoning for each score

  Scenario: Balance team workload (No idle workers!)
    Given worker A is idle (0% capacity used)
    And worker B is overloaded (120% capacity used)
    And worker C has medium load (60% capacity used)
    When Santiago prioritizes backlog
    Then Santiago SHOULD assign work to idle worker A first
    And Santiago SHOULD NOT assign new work to overloaded worker B
    And Santiago SHOULD optimize for "maximize effectiveness, not efficiency"
    And Santiago SHOULD surface overload issue to human PM
    And recommendation SHOULD be: "Worker B needs help or scope reduction"

  Scenario: Unblock dependencies (Flow optimization)
    Given feature X blocks features Y and Z
    And feature X is in backlog with medium priority
    When Santiago recalculates priorities
    Then feature X SHOULD get boosted priority (unblock_impact = 2)
    And explanation SHOULD say: "Unblocks 2 downstream features"
    And Santiago SHOULD recommend tackling X before Y or Z

  Scenario: Prioritize learning over delivery (Lean UX pattern)
    Given two features with equal customer value:
      | feature | customer_value | uncertainty | delivery_time |
      | A       | 0.8            | high (0.9)  | 2 weeks       |
      | B       | 0.8            | low (0.2)   | 1 week        |
    When Santiago calculates priority scores
    Then feature A SHOULD rank higher (learning_value = 0.9)
    And explanation SHOULD say: "Reduces more uncertainty"
    And this validates Lean UX principle: "Validate assumptions first"
```

### Story 2: Three Amigos Backlog Refinement

```gherkin
Feature: Three Amigos Backlog Refinement
  Santiago facilitates backlog grooming using Three Amigos pattern

  Scenario: Automated backlog review (Human + AI collaboration)
    Given backlog has 10 unrefined items (proposed status)
    When human initiates Three Amigos session
    Then Santiago SHOULD present each item:
      """
      Item: Personal Log Feature Discovery
      
      [Product Owner perspective - Santiago extracts from artifacts]
      - User Story: "As a human/AI agent, I want to log my work..."
      - Hypothesis: Daily journal + chat history = context preservation
      - Value: Reduces context loss between sessions
      
      [Developer perspective - Santiago queries technical feasibility]
      - Technical Approach: Markdown files with YAML frontmatter
      - Estimated Effort: 3 story points (small)
      - Dependencies: None (can start immediately)
      - Risks: Low (proven pattern in ships-logs)
      
      [Tester perspective - Santiago proposes acceptance criteria]
      - AC1: Personal log template created
      - AC2: First log entry written successfully
      - AC3: Log entries queryable by date/tags
      
      [Santiago's Recommendation]
      Priority Score: 0.85 (HIGH)
      Rationale: High value, low effort, no blockers, reduces known pain point
      Suggested Action: Move to "ready" status, assign to idle worker
      """
    And human can accept/reject/modify Santiago's analysis
    And refined items move to "ready" status

  Scenario: Break down large work items (Epic → Stories)
    Given backlog item "Lean-Kanban Domain Ingestion" is too large
    And estimated effort is 15 story points (large)
    When Santiago analyzes work breakdown
    Then Santiago SHOULD propose smaller items:
      | sub-item                        | effort | dependencies        |
      | Research Lean-Kanban sources    | 2 pts  | None                |
      | Extract Kanban behaviors        | 3 pts  | Research complete   |
      | Extend ontology with Kanban     | 3 pts  | Behaviors extracted |
      | Map Santiago workflow to Kanban | 2 pts  | Ontology extended   |
      | Implement WIP limits            | 2 pts  | Workflow mapped     |
      | Track flow metrics              | 3 pts  | WIP limits done     |
    And total effort SHOULD equal original estimate (15 pts)
    And dependencies SHOULD create logical sequence
    And each sub-item SHOULD be independently valuable
```

### Story 3: Dynamic Work Assignment (Pull-Based)

```gherkin
Feature: Dynamic Work Assignment
  Workers "pull" from prioritized backlog when ready

  Scenario: Worker pulls next highest priority item
    Given backlog is prioritized with scores:
      | item                  | priority_score | required_skills    |
      | Questionnaire system  | 0.95           | UXR, PM            |
      | Personal log feature  | 0.85           | PM, documentation  |
      | Kanban ingestion      | 0.75           | Knowledge engineer |
    And worker "Santiago-PM" has skills: [PM, UXR, documentation]
    And worker "Santiago-PM" is idle (0% capacity)
    When worker queries: "What should I work on next?"
    Then Santiago SHOULD recommend: "Questionnaire system"
    And rationale SHOULD be: "Highest priority match for your skills"
    And item status SHOULD change: proposed → in-progress
    And worker capacity SHOULD update: 0% → 50% (estimated)

  Scenario: No suitable work available (Worker blocked)
    Given all high-priority items require skill "DevOps"
    And worker "Santiago-PM" has skills: [PM, UXR]
    And worker "Santiago-PM" is idle
    When worker queries: "What should I work on next?"
    Then Santiago SHOULD respond: "No suitable work in your skill set"
    And Santiago SHOULD recommend: "Help with lower-priority PM items or learn DevOps"
    And Santiago SHOULD surface to human: "PM worker idle, DevOps backlog growing"
    And this triggers conversation about: skill development or hiring
```

### Story 4: Flow Metrics & Continuous Improvement

```gherkin
Feature: Flow Metrics Tracking
  Measure cycle time, throughput, blockers to improve workflow

  Scenario: Calculate cycle time per work item
    Given work item was:
      | event      | timestamp            |
      | created    | 2025-11-17 09:00     |
      | refined    | 2025-11-17 10:30     |
      | started    | 2025-11-17 11:00     |
      | completed  | 2025-11-19 15:00     |
    When Santiago calculates cycle time
    Then cycle_time SHOULD be: 2 days, 4 hours (started → completed)
    And lead_time SHOULD be: 2 days, 6 hours (created → completed)
    And refinement_time SHOULD be: 1.5 hours (created → refined)
    And Santiago SHOULD track these metrics in KG

  Scenario: Identify bottlenecks (WIP limits exceeded)
    Given WIP limit for "in-progress" stage is 3 items
    And current WIP is 4 items (limit exceeded!)
    When Santiago checks workflow health
    Then Santiago SHOULD flag: "WIP limit exceeded in 'in-progress' stage"
    And Santiago SHOULD recommend: "Complete existing work before starting new items"
    And Santiago SHOULD analyze: "Why did 4 items get started?"
    And this triggers retrospective: "How do we enforce WIP limits better?"

  Scenario: Measure throughput (Velocity)
    Given last 2 weeks, Santiago completed:
      | week | items_completed | story_points |
      | 1    | 8               | 21           |
      | 2    | 7               | 18           |
    When Santiago calculates throughput
    Then avg_throughput SHOULD be: 7.5 items/week or 19.5 story points/week
    And Santiago SHOULD use this for capacity planning
    And Santiago SHOULD forecast: "3 weeks to complete 15-item backlog"
```

---

## Acceptance Criteria

### AC1: Neurosymbolic Prioritization Algorithm

- [ ] **Algorithm implemented** that queries KG for:
  - [ ] Available workers (idle/busy, skills, capacity remaining)
  - [ ] Work dependencies (blocked_by, blocks, dependency graph)
  - [ ] Customer value (hypothesis confidence from research-logs)
  - [ ] Team capacity (story points remaining, WIP limits)
- [ ] **Priority score formula** uses weighted factors:
  - [ ] customer_value (40% weight)
  - [ ] unblock_impact (30% weight)
  - [ ] worker_availability (20% weight)
  - [ ] learning_value (10% weight)
- [ ] **Explanation generation** for each score (provenance, rationale)
- [ ] **Real-time recalculation** when KG state changes
- [ ] **BDD scenarios pass** for prioritization logic (3 scenarios minimum)

### AC2: Three Amigos Backlog Refinement

- [ ] **CLI command**: `santiago pm refine-backlog` triggers Three Amigos session
- [ ] **Automated analysis** presents:
  - [ ] Product Owner perspective (user story, hypothesis, value)
  - [ ] Developer perspective (technical approach, effort, dependencies)
  - [ ] Tester perspective (acceptance criteria, test scenarios)
- [ ] **Human review loop** allows accept/reject/modify
- [ ] **Work breakdown** suggests smaller items for large epics (>8 story points)
- [ ] **Refined items** move to "ready" status automatically

### AC3: Pull-Based Work Assignment

- [ ] **CLI command**: `santiago pm pull-work` returns highest priority item for worker
- [ ] **Skill matching** considers worker capabilities vs. required skills
- [ ] **Capacity tracking** updates when work is pulled/completed
- [ ] **Blocked worker detection** surfaces when no suitable work available
- [ ] **Status transitions** happen automatically (proposed → in-progress)

### AC4: Flow Metrics & Continuous Improvement

- [ ] **Cycle time tracking** for all work items (timestamps in YAML)
- [ ] **WIP limit enforcement** warns when limits exceeded
- [ ] **Throughput calculation** averages items/week and story points/week
- [ ] **Bottleneck detection** identifies stages with growing queues
- [ ] **Forecast generation** predicts completion dates based on velocity
- [ ] **Metrics dashboard**: `santiago pm metrics` shows all flow stats

### AC5: Integration with Existing Systems

- [ ] **Status tackle integration**: Backlog uses existing status system
- [ ] **Artifact metadata**: Backlog items stored as markdown with YAML
- [ ] **Ontology extension**: New classes for BacklogItem, Worker, Dependency
- [ ] **Questionnaire system**: Can create backlog items from responses
- [ ] **Research logs**: Can trigger backlog item creation

---

## Technical Design

### Backlog Item Schema

```yaml
---
artifact_type: backlog-item
id: BI-042
title: "Neurosymbolic Backlog Prioritization Algorithm"
status: proposed | ready | in-progress | review | done | cancelled
priority_score: 0.85  # Calculated by Santiago
priority_rank: 3      # Position in backlog (1 = highest)
estimated_effort: 5   # Story points
actual_effort: null   # Filled when done
created: 2025-11-17T09:00:00Z
refined: 2025-11-17T10:30:00Z  # When Three Amigos refined it
started: null
completed: null
cycle_time: null      # Calculated: started → completed
lead_time: null       # Calculated: created → completed

# Neurosymbolic prioritization factors
customer_value: 0.9   # From hypothesis confidence in research-logs
unblock_impact: 2     # Number of downstream items this unblocks
worker_availability: 0.8  # Skill match with available workers
learning_value: 0.7   # How much uncertainty this reduces

# Assignment & capacity
assigned_to: [santiago-pm]  # Who pulled this work
required_skills: [neurosymbolic-reasoning, probabilistic-evaluation, KG-queries]
blocked_by: []       # IDs of blocking items
blocks: [BI-043, BI-044]  # IDs of items this blocks

# Relationships
related_to: [research-logs/2025-11-17-artifact-workflow-is-lean-kanban.md]
triggered_by: cargo-manifests/lean-kanban-domain-ingestion.feature
extracts_to: []      # Artifacts created from this work

# Three Amigos refinement
product_owner_notes: |
  User story: As Santiago PM, I want intelligent prioritization
  so that I work on the most valuable items without manual analysis.
  
developer_notes: |
  Technical approach: Query KG for state, calculate weighted score,
  return sorted backlog with rationale. Use existing reasoner.
  
tester_notes: |
  Acceptance criteria:
  - Algorithm queries KG for 4 factors
  - Score uses correct weights (0.4/0.3/0.2/0.1)
  - Explanation generated for each score
  - BDD scenarios pass

# Flow metrics
wip_stage: backlog   # Which Kanban stage this is in
wip_limit: null      # Limit for current stage
cumulative_flow: []  # History of stage transitions

tags: [neurosymbolic, prioritization, lean-kanban, three-amigos]
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

[Filled in during development]

## Related Artifacts

- **Research Log**: artifact-workflow-is-lean-kanban.md (discovered we're already doing Kanban)
- **Feature**: lean-kanban-domain-ingestion.feature (extract Kanban behaviors)
- **Ontology**: pm-domain-ontology.ttl (needs BacklogItem, Worker, Dependency classes)
```

### Neurosymbolic Prioritization Algorithm

```python
# File: src/nusy_pm_core/backlog_manager.py

from dataclasses import dataclass
from typing import List, Dict, Tuple
from nusy_pm_core.adapters.kg_store import KGStore
from nusy_pm_core.santiago_core_bdd_executor import SantiagoCoreNeurosymbolicReasoner

@dataclass
class PriorityFactors:
    customer_value: float      # 0.0-1.0 (from hypothesis confidence)
    unblock_impact: float      # 0.0-1.0 (normalized blocked items count)
    worker_availability: float # 0.0-1.0 (skill match * capacity remaining)
    learning_value: float      # 0.0-1.0 (uncertainty reduction potential)

@dataclass
class BacklogItem:
    id: str
    title: str
    status: str
    estimated_effort: int
    required_skills: List[str]
    blocked_by: List[str]
    blocks: List[str]
    priority_score: float = 0.0
    priority_rank: int = 0
    factors: PriorityFactors = None
    rationale: str = ""

class NeurosymbolicBacklogManager:
    """
    Intelligent backlog management using neurosymbolic reasoning.
    
    Key Innovation: Query KG for real-time state, calculate optimal
    priority based on effectiveness (not just efficiency).
    """
    
    def __init__(self, kg_store: KGStore, reasoner: SantiagoCoreNeurosymbolicReasoner):
        self.kg = kg_store
        self.reasoner = reasoner
        
        # Priority score weights (from user story)
        self.weights = {
            'customer_value': 0.4,
            'unblock_impact': 0.3,
            'worker_availability': 0.2,
            'learning_value': 0.1
        }
    
    def prioritize_backlog(self) -> List[BacklogItem]:
        """
        Calculate optimal work priority using neurosymbolic reasoning.
        
        Returns:
            Sorted list of backlog items with priority scores and rationale
        """
        # Step 1: Query KG for current state
        backlog_items = self._get_backlog_items()
        available_workers = self._get_available_workers()
        dependency_graph = self._get_dependency_graph()
        customer_hypotheses = self._get_customer_hypotheses()
        team_capacity = self._get_team_capacity()
        
        # Step 2: Calculate priority score for each item
        for item in backlog_items:
            factors = self._calculate_priority_factors(
                item, 
                available_workers, 
                dependency_graph, 
                customer_hypotheses,
                team_capacity
            )
            
            score = self._weighted_score(factors)
            rationale = self._generate_rationale(item, factors)
            
            item.factors = factors
            item.priority_score = score
            item.rationale = rationale
        
        # Step 3: Sort by priority score (descending)
        sorted_backlog = sorted(
            backlog_items, 
            key=lambda x: x.priority_score, 
            reverse=True
        )
        
        # Step 4: Assign ranks
        for rank, item in enumerate(sorted_backlog, start=1):
            item.priority_rank = rank
        
        return sorted_backlog
    
    def _calculate_priority_factors(
        self, 
        item: BacklogItem, 
        workers: List[Dict],
        dependencies: Dict,
        hypotheses: Dict,
        capacity: Dict
    ) -> PriorityFactors:
        """
        Calculate the 4 priority factors for a backlog item.
        
        This is the neurosymbolic magic: query KG, reason about state,
        return probabilistic scores.
        """
        # Factor 1: Customer Value (from hypothesis confidence)
        customer_value = self._query_customer_value(item, hypotheses)
        
        # Factor 2: Unblock Impact (how many items this unblocks)
        unblock_impact = self._query_unblock_impact(item, dependencies)
        
        # Factor 3: Worker Availability (skill match * capacity)
        worker_availability = self._query_worker_availability(item, workers, capacity)
        
        # Factor 4: Learning Value (uncertainty reduction)
        learning_value = self._query_learning_value(item, hypotheses)
        
        return PriorityFactors(
            customer_value=customer_value,
            unblock_impact=unblock_impact,
            worker_availability=worker_availability,
            learning_value=learning_value
        )
    
    def _weighted_score(self, factors: PriorityFactors) -> float:
        """
        Calculate weighted priority score.
        
        Formula:
            score = (customer_value * 0.4) +
                    (unblock_impact * 0.3) +
                    (worker_availability * 0.2) +
                    (learning_value * 0.1)
        """
        score = (
            factors.customer_value * self.weights['customer_value'] +
            factors.unblock_impact * self.weights['unblock_impact'] +
            factors.worker_availability * self.weights['worker_availability'] +
            factors.learning_value * self.weights['learning_value']
        )
        return round(score, 3)
    
    def _generate_rationale(self, item: BacklogItem, factors: PriorityFactors) -> str:
        """
        Generate human-readable explanation for priority score.
        
        Example:
            "High priority (0.85) because:
            - Strong customer need (0.9 hypothesis confidence)
            - Unblocks 2 downstream items
            - Skills match available workers (PM, UXR)
            - Reduces significant uncertainty (0.7 learning value)"
        """
        score = self._weighted_score(factors)
        level = "HIGH" if score > 0.7 else "MEDIUM" if score > 0.4 else "LOW"
        
        rationale = f"{level} priority ({score:.2f}) because:\n"
        
        if factors.customer_value > 0.7:
            rationale += f"- Strong customer need ({factors.customer_value:.1f} hypothesis confidence)\n"
        
        if factors.unblock_impact > 0.5:
            num_blocked = int(factors.unblock_impact * 10)  # Denormalize
            rationale += f"- Unblocks {num_blocked} downstream items\n"
        
        if factors.worker_availability > 0.6:
            rationale += f"- Skills match available workers ({item.required_skills})\n"
        
        if factors.learning_value > 0.6:
            rationale += f"- Reduces significant uncertainty ({factors.learning_value:.1f} learning value)\n"
        
        if factors.worker_availability < 0.3:
            rationale += "- ⚠️ No workers with required skills available\n"
        
        if item.blocked_by:
            rationale += f"- ⚠️ Blocked by {len(item.blocked_by)} other items\n"
        
        return rationale.strip()
    
    # ... (KG query methods follow)
```

---

## Implementation Phases

### Phase 1: Core Algorithm (Week 1)
- [ ] Design priority calculation algorithm
- [ ] Implement neurosymbolic KG queries
- [ ] Write BDD scenarios for prioritization
- [ ] Test with sample backlog (10 items)

### Phase 2: Three Amigos Refinement (Week 1-2)
- [ ] Build automated analysis (PO/Dev/Test perspectives)
- [ ] Implement human review loop
- [ ] Create work breakdown suggestions
- [ ] Test with real cargo-manifests

### Phase 3: Pull-Based Assignment (Week 2)
- [ ] Build "pull-work" CLI command
- [ ] Implement skill matching
- [ ] Track capacity and WIP
- [ ] Test with simulated workers

### Phase 4: Flow Metrics (Week 2-3)
- [ ] Implement cycle time tracking
- [ ] Build WIP limit warnings
- [ ] Calculate throughput and velocity
- [ ] Create metrics dashboard

### Phase 5: Integration & Polish (Week 3)
- [ ] Integrate with status tackle
- [ ] Update ontology with backlog classes
- [ ] Write documentation
- [ ] Create demo video

---

## Success Metrics

**Effectiveness** (doing the right things):
- 90% of completed work was top 3 priority at start
- 0 instances of idle workers when work was available
- 20% reduction in "blocked" time (better dependency management)

**Efficiency** (doing things well):
- Cycle time reduces by 15% (better work selection)
- Throughput increases 10% (less context switching)
- WIP limits respected 95% of the time

**Team Health**:
- Worker satisfaction score > 4/5 ("I'm working on valuable things")
- No worker >100% capacity for >1 week
- Fair work distribution (no one gets all grunt work)

---

## Metadata

```yaml
feature_id: F-026
version: 1.0.0
author: human-pm + santiago-pm (collaboration!)
reviewers: [santiago-architect, santiago-developer]
estimated_effort: 3 weeks
dependencies: 
  - lean-kanban-domain-ingestion (F-025)
  - status-tackle (existing)
  - neurosymbolic-reasoner (existing)
blocked_by: []
blocks: [artifact-driven-workflow-orchestration]
priority_score: 0.95  # VERY HIGH (enables effective work)
triggered_by: user-request + lean-kanban-research
tags: [neurosymbolic, prioritization, three-amigos, lean-kanban, effectiveness]
```
