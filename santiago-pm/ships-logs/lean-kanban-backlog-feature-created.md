# Ships Log: Lean-Kanban Backlog Management Feature Created

**Date**: 2025-11-17
**Mission**: Build neurosymbolic backlog management with Three Amigos pattern
**Status**: Design Complete, Implementation Pending
**Crew**: Human PM + Santiago PM

---

## Mission Summary

Built comprehensive Lean-Kanban backlog management feature that uses **neurosymbolic reasoning** to prioritize work based on real-time KG queries. This is the "killer feature" that differentiates Santiago from traditional PM tools.

### Key Innovation: Neurosymbolic Prioritization

Instead of static formulas (WSJF, MoSCoW), Santiago **queries the knowledge graph** to understand:
- Who's available to work? (capacity + skills)
- What's blocked by what? (dependency chains)
- What do customers need? (hypothesis confidence)
- How can we maximize effectiveness? (not just efficiency)

Then uses **probabilistic evaluation** to calculate optimal priority scores with explanations.

---

## Artifacts Created

### 1. Cargo Manifest (Feature Specification)
**File**: `santiago-pm/cargo-manifests/neurosymbolic-backlog-management.feature`
**Size**: ~500 lines
**Content**:
- Feature overview & business value
- 4 user stories (prioritization, Three Amigos, pull-based assignment, flow metrics)
- BDD scenarios for each capability
- Neurosymbolic algorithm design (Python pseudocode)
- 5-phase implementation plan (3 weeks)
- Success metrics (effectiveness, efficiency, team health)

**Highlights**:
- Priority formula: `(customer_value * 0.4) + (unblock_impact * 0.3) + (worker_availability * 0.2) + (learning_value * 0.1)`
- Three Amigos automation: Santiago analyzes from PO/Dev/Test perspectives
- Pull system: Workers query "What should I work on next?"
- Flow metrics: Cycle time, throughput, WIP limits, bottleneck detection

### 2. Backlog Item Template
**File**: `santiago-pm/tackle/backlog-item-template.md`
**Size**: ~400 lines
**Content**:
- Complete YAML schema for backlog items
- Three Amigos sections (PO/Dev/Test perspectives)
- Flow metrics tracking (cycle time, cumulative flow)
- Example filled backlog item
- Field explanations (status flow, priority scoring, effort estimation)
- Tips for effective user stories, hypotheses, acceptance criteria

**Key Fields**:
```yaml
---
artifact_type: backlog-item
status: proposed | ready | in-progress | review | done
priority_score: 0.0-1.0  # Neurosymbolic calculation
estimated_effort: 1,2,3,5,8,13,21  # Fibonacci story points
customer_value: 0.0-1.0
unblock_impact: 0.0-1.0
worker_availability: 0.0-1.0
learning_value: 0.0-1.0
blocked_by: [list of IDs]
blocks: [list of IDs]
assigned_to: [workers]
required_skills: [PM, UXR, DevOps, etc.]
cumulative_flow: [stage history]
---
```

### 3. BDD Feature File (10 Scenarios)
**File**: `features/backlog-management.feature`
**Size**: ~850 lines
**Content**: 10 comprehensive BDD scenarios covering:

1. **Core Neurosymbolic Prioritization** (CRITICAL)
   - Query KG for workers, dependencies, value, capacity
   - Calculate weighted priority score
   - Generate explanations for each score
   - Blocked items automatically deprioritized

2. **Balance Team Workload**
   - Detect idle vs overloaded workers
   - Prevent worker burnout (no >100% capacity)
   - Maximize effectiveness (no idle workers when work available)
   - Surface workload imbalances to human PM

3. **Three Amigos Backlog Refinement**
   - Automated analysis from PO/Dev/Test perspectives
   - Human review loop (accept/reject/modify)
   - Work breakdown for large items (>8 story points)
   - Move refined items to "ready" status

4. **Pull-Based Work Assignment**
   - Workers query for next highest priority item
   - Skill matching (recommend work that fits skills)
   - Capacity tracking (update when work pulled)
   - Blocked worker detection (no suitable work available)

5. **Flow Metrics & Continuous Improvement**
   - Cycle time calculation (started → completed)
   - Lead time calculation (created → completed)
   - Stage duration analysis
   - Bottleneck identification (stages with long wait times)
   - Flow efficiency (value-add time / total time)

6. **WIP Limit Enforcement**
   - Prevent pulling new work when at WIP limit
   - Encourage completion over starting
   - Improve flow (reduce context switching)
   - Maintain quality (focus > multitasking)

7. **Dependency Management**
   - Detect dependency chains (what blocks what)
   - Boost priority for items that unblock others
   - Deprioritize blocked items (50% penalty)
   - Auto-unblock when blocker completes
   - Notify workers when items unblock

8. **Throughput & Velocity Forecasting**
   - Calculate average throughput (items/week, story points/week)
   - Analyze velocity trends (increasing/decreasing?)
   - Forecast completion dates (optimistic/realistic/pessimistic)
   - Track forecast accuracy over time

9. **Integration with Existing Systems**
   - Map backlog stages to status tackle fields
   - Reuse existing YAML frontmatter
   - Leverage existing KG queries
   - Flow transitions update status automatically

10. **Neurosymbolic Learning Over Time**
    - Track predicted vs actual outcomes
    - Calculate prediction error metrics
    - Identify patterns (integration work underestimated, etc.)
    - Adjust weights based on learning
    - Apply learned patterns to new items

---

## The Neurosymbolic Advantage

### What Makes This Different?

**Traditional Tools** (Jira, Trello, Kanboard):
- Static prioritization (manual drag-and-drop or simple formulas)
- No context awareness (doesn't know who's available)
- No dependency reasoning (you manually track blockers)
- No learning (same formula forever)

**Santiago's Neurosymbolic Approach**:
- **Dynamic prioritization**: Recalculates when KG state changes
- **Context-aware**: Queries for workers, capacity, skills in real-time
- **Dependency reasoning**: Analyzes full dependency graph, boosts unblockers
- **Probabilistic evaluation**: Uses confidence scores, not binary yes/no
- **Self-improving**: Learns from outcomes, adjusts weights over time
- **Explainable**: Generates rationale for every priority score

### Example: How Santiago Prioritizes

```python
# Traditional WSJF (Weighted Shortest Job First)
priority = (user_value + time_criticality + risk_reduction) / effort

# Santiago's Neurosymbolic Prioritization
priority = calculate_priority(item, context={
    "available_workers": kg.query("SELECT ?worker WHERE {?worker nusy:idle true}"),
    "dependency_graph": kg.query("SELECT ?blocks WHERE {?item nusy:blocks ?blocks}"),
    "customer_value": kg.query("SELECT ?confidence WHERE {?hypothesis nusy:relatedTo ?item}"),
    "team_capacity": kg.query("SELECT ?capacity WHERE {?worker nusy:capacityRemaining ?capacity}")
})

# Result: Priority score + explanation
{
  "priority_score": 0.85,
  "rationale": """
    HIGH priority (0.85) because:
    - Strong customer need (0.9 hypothesis confidence)
    - Unblocks 2 downstream items
    - Skills match available workers (PM, UXR)
    - Reduces significant uncertainty (0.7 learning value)
  """
}
```

---

## Key Patterns & Insights

### 1. Three Amigos Pattern (Automated!)

**Traditional Three Amigos**: 3 humans meet to refine backlog items
- Product Owner: Describes feature (what/why)
- Developer: Assesses technical approach (how)
- Tester: Defines acceptance criteria (done when...)

**Santiago's Three Amigos**: AI + human collaboration
- Santiago analyzes from all 3 perspectives automatically
- Human reviews and validates/adjusts
- Faster refinement, consistent quality
- **Still collaborative** (human has final say)

### 2. Pull-Based Work Assignment

**Traditional Push**: PM assigns work to workers
- Risk: Overload workers, ignore skills/capacity
- Workers feel micromanaged

**Santiago's Pull**: Workers pull from prioritized backlog
- Worker queries: "What should I work on next?"
- Santiago recommends based on skills + capacity + priority
- Worker chooses (autonomy + ownership)
- **Maximizes effectiveness** (right work, right person, right time)

### 3. Effectiveness > Efficiency

**User's Key Insight**: "Maximize effectiveness, not efficiency"

**Effectiveness** = Doing the right things
- High-value work completed
- No idle workers (when work available)
- No overloaded workers (burnout prevention)
- Fair work distribution

**Efficiency** = Doing things fast
- Low cycle time
- High throughput
- Fast velocity

Santiago optimizes for **effectiveness FIRST**, efficiency second. Better to do the right work slowly than the wrong work quickly.

### 4. Bootstrap Loop (Santiago Using Santiago!)

This feature enables Santiago to manage its own backlog:
1. Santiago prioritizes its own work items
2. Santiago refines them with Three Amigos
3. Santiago pulls work based on capacity
4. Santiago tracks flow metrics
5. Santiago learns from outcomes
6. **Loop**: Better prioritization → better work selection → better outcomes → better learning!

**Meta-insight**: Santiago learns project management by doing project management (recursive improvement).

---

## Next Steps (Implementation)

### Phase 1: Core Algorithm (Week 1) - READY TO START
- [ ] Implement priority calculation algorithm
- [ ] Build KG query functions (workers, dependencies, value, capacity)
- [ ] Write BDD test scenarios
- [ ] Test with sample backlog (10 items)

**Blocked by**: Nothing! Can start immediately.

**Required skills**: Neurosymbolic reasoning, KG queries, probabilistic evaluation

**Estimated effort**: 5 story points (1 week)

### Phase 2: Three Amigos Automation (Week 1-2)
- [ ] Build automated analysis (PO/Dev/Test perspectives)
- [ ] Implement human review loop
- [ ] Create work breakdown suggestions
- [ ] Test with real cargo-manifests

### Phase 3: Pull-Based Assignment (Week 2)
- [ ] Build CLI command: `santiago pm pull-work`
- [ ] Implement skill matching
- [ ] Track capacity and WIP
- [ ] Test with simulated workers

### Phase 4: Flow Metrics (Week 2-3)
- [ ] Implement cycle time tracking
- [ ] Build WIP limit warnings
- [ ] Calculate throughput and velocity
- [ ] Create metrics dashboard: `santiago pm metrics`

### Phase 5: Integration & Polish (Week 3)
- [ ] Integrate with status tackle
- [ ] Update ontology (BacklogItem, Worker, Dependency classes)
- [ ] Write documentation
- [ ] Create demo video

---

## Success Metrics

### Effectiveness (Doing the right things)
- **Target**: 90% of completed work was top 3 priority at start
- **Target**: 0 instances of idle workers when work was available
- **Target**: 20% reduction in "blocked" time (better dependency management)

### Efficiency (Doing things well)
- **Target**: Cycle time reduces by 15% (better work selection)
- **Target**: Throughput increases 10% (less context switching)
- **Target**: WIP limits respected 95% of the time

### Team Health
- **Target**: Worker satisfaction > 4/5 ("I'm working on valuable things")
- **Target**: No worker >100% capacity for >1 week
- **Target**: Fair work distribution (no one gets all grunt work)

### Learning (Continuous improvement)
- **Target**: Priority prediction error < 15% after 2 months
- **Target**: Effort estimation error < 30% after 2 months
- **Target**: Weights adjusted based on outcomes (self-improving!)

---

## Integration Points

### Existing Santiago Systems
- **Status Tackle**: Backlog uses existing status field (proposed/ready/in-progress/review/done)
- **Ontology**: Extends with BacklogItem, Worker, Dependency classes (Layer 10: Flow Management)
- **Neurosymbolic Reasoner**: Uses existing reasoner for probabilistic evaluation
- **Questionnaire System**: Can create backlog items from questionnaire responses
- **Research Logs**: Can trigger backlog item creation

### External PM Tools (Future)
- **Jira/Linear/Asana**: Export backlog to external tools (if user wants)
- **GitHub Issues**: Sync backlog with GitHub issues
- **Slack/Discord**: Post backlog updates to team chat

---

## Connections to Existing Research

### 1. Artifact-Driven Workflow IS Lean-Kanban
**File**: `research-logs/2025-11-17-artifact-workflow-is-lean-kanban.md`

**Discovery**: Santiago's artifact-driven workflow = Lean-Kanban pull system!
- Artifact created → Domain folder → Worker notified → Work happens
- Research-log creates cargo-manifest (pull trigger!)
- **We're already doing Kanban implicitly**

**Implication**: This backlog feature makes the implicit pattern **explicit** and **measurable**.

### 2. Lean-Kanban Domain Ingestion (Planned)
**File**: `cargo-manifests/lean-kanban-domain-ingestion.feature`

**Status**: ready (designed, awaiting implementation)

**Content**: Ingest Lean-Kanban methodology knowledge
- Sources: David Anderson, Mike Burrows, Kanban University
- Behaviors: visualize_workflow, limit_wip, manage_flow, etc. (10+)
- Ontology: Layer 10 "Flow Management" classes

**Connection**: This backlog feature is a **test case** for Lean-Kanban patterns. Once we build this, we'll have empirical evidence to inform the domain ingestion.

### 3. Prioritize Backlog Behavior (Extracted)
**File**: `knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md`

**Behavior**: 2.2 prioritize_backlog (Master capability, Sea scope)

**Input Schema**: features, criteria (value/risk/alignment/effort), constraints (dependencies/deadlines)

**Output Schema**: prioritized_backlog (ranked with scores), conflicts, recommendations

**Connection**: This BDD feature **implements** the extracted behavior. We're turning the specification into working code.

---

## Technical Architecture

### Data Flow

```
1. Backlog Item Created
   ↓
2. Santiago Queries KG
   - available_workers: Who can work on this?
   - work_dependencies: What blocks this?
   - customer_hypotheses: How valuable is this?
   - team_capacity: Do we have bandwidth?
   ↓
3. Santiago Calculates Priority Factors
   - customer_value: 0.0-1.0
   - unblock_impact: 0.0-1.0
   - worker_availability: 0.0-1.0
   - learning_value: 0.0-1.0
   ↓
4. Santiago Calculates Weighted Score
   priority_score = weighted_sum(factors)
   ↓
5. Santiago Generates Rationale
   "HIGH priority (0.85) because..."
   ↓
6. Santiago Sorts Backlog by Score
   Rank 1 = highest priority
   ↓
7. Worker Queries for Next Work
   "What should I work on next?"
   ↓
8. Santiago Recommends Top Match
   Considers: priority + skills + capacity
   ↓
9. Worker Pulls Work
   status: ready → in-progress
   assigned_to: [worker]
   started: timestamp
   ↓
10. Worker Completes Work
    status: in-progress → done
    completed: timestamp
    cycle_time: completed - started
    ↓
11. Santiago Updates Metrics
    throughput += 1
    velocity += story_points
    flow_efficiency = calculate()
    ↓
12. Santiago Learns from Outcome
    predicted_value vs actual_value
    predicted_effort vs actual_effort
    adjust_weights_if_needed()
```

### Code Structure (Planned)

```
src/nusy_pm_core/
├── backlog_manager.py          # Main backlog management class
│   ├── NeurosymbolicBacklogManager
│   ├── prioritize_backlog()
│   ├── refine_backlog()
│   ├── pull_work()
│   └── calculate_metrics()
├── priority_calculator.py      # Priority scoring algorithm
│   ├── PriorityFactors (dataclass)
│   ├── calculate_priority_factors()
│   ├── weighted_score()
│   └── generate_rationale()
├── three_amigos_analyzer.py    # Automated refinement
│   ├── analyze_product_owner_perspective()
│   ├── analyze_developer_perspective()
│   ├── analyze_tester_perspective()
│   └── generate_recommendation()
├── flow_metrics_tracker.py     # Cycle time, throughput, etc.
│   ├── calculate_cycle_time()
│   ├── calculate_lead_time()
│   ├── identify_bottlenecks()
│   └── forecast_completion()
└── models/
    ├── backlog_item.py         # BacklogItem dataclass
    ├── worker.py               # Worker dataclass
    └── dependency.py           # Dependency graph structures
```

---

## Lessons Learned

### 1. Semantic Search Prevented Duplicate Work
Before building, we searched and found:
- Research log on Lean-Kanban (already written!)
- Cargo manifest on domain ingestion (already designed!)
- Prioritize backlog behavior (already extracted!)

**Without semantic search**, we would have recreated all of this. **With semantic search**, we built on the existing foundation.

### 2. User's Neurosymbolic Insight Was Key
User said: "A neurosymbolic AI will be very good at this because it can look at all the assets, know who is available to work, and use probabilistic evaluation."

This insight unlocked the **differentiating feature**:
- Not just static formulas (WSJF, MoSCoW)
- **Query the KG** for real-time state
- **Reason probabilistically** about optimal priority
- **Explain the reasoning** (provenance + rationale)

### 3. Three Amigos Pattern Is Powerful
Automated analysis from 3 perspectives:
- Product Owner: Value, hypothesis, metrics
- Developer: Technical approach, effort, risks
- Tester: Acceptance criteria, test scenarios

This ensures **comprehensive refinement** without requiring 3 humans to meet every time. Human still validates, but AI does the heavy lifting.

### 4. Pull > Push for Autonomy
Workers **pulling work** (vs being **pushed work**) creates:
- **Ownership**: "I chose this"
- **Autonomy**: "I control my workload"
- **Alignment**: "I'm working on what I'm good at"

Santiago recommends, but worker chooses. This respects human agency while providing intelligent guidance.

---

## Open Questions (For Implementation)

### 1. How to handle priority conflicts?
What if two items have equal priority scores?
- Tiebreaker: Effort (smaller first)?
- Tiebreaker: Created date (older first)?
- Tiebreaker: Customer importance (ask human)?

### 2. How to track worker satisfaction?
Success metric: "Worker satisfaction > 4/5"
- Survey after each sprint?
- Sentiment analysis of commit messages?
- Ask directly: "Are you working on valuable things?"

### 3. How to enforce WIP limits technically?
When WIP limit reached, should we:
- Hard block: CLI command fails
- Soft warning: "You're at limit, are you sure?"
- Notification: "WIP limit reached, complete work first"

### 4. How often to recalculate priorities?
Real-time on every KG change? Or periodic (daily/weekly)?
- Real-time: More accurate, higher compute cost
- Periodic: Less accurate, lower compute cost
- Hybrid: Real-time for critical items, periodic for backlog

### 5. How to handle external dependencies?
What if item is blocked by external team (not in our KG)?
- Mark as blocked, but no auto-unblock
- Track external blockers separately
- Surface to human: "Check with external team"

---

## Conclusion

We've designed a **comprehensive neurosymbolic backlog management system** that:
- Prioritizes work intelligently (KG queries + probabilistic reasoning)
- Automates Three Amigos refinement (PO/Dev/Test perspectives)
- Enables pull-based work assignment (worker autonomy + smart recommendations)
- Tracks flow metrics (cycle time, throughput, bottlenecks)
- Learns from outcomes (self-improving over time)

**Key differentiator**: Neurosymbolic reasoning makes Santiago **context-aware** and **adaptive** in ways traditional PM tools are not.

**Next step**: Implement Phase 1 (core algorithm) and validate with real backlog items.

**Status**: Design complete, ready for implementation! 🚀

---

## Metadata

```yaml
artifact_type: ships-log
mission_id: lean-kanban-backlog-feature
status: design-complete
crew: [human-pm, santiago-pm]
date: 2025-11-17
estimated_implementation: 3 weeks (5 phases)
priority: high
dependencies: [neurosymbolic-reasoner, kg-store, status-tackle]
blocks: [artifact-driven-workflow-orchestration, factory-throughput-measurement]
tags: [neurosymbolic, lean-kanban, three-amigos, backlog, prioritization, effectiveness]
```
