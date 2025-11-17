# Cargo Manifest: Workflow Test Data System

```yaml
---
artifact_type: cargo-manifest
feature_id: F-028
feature_name: workflow-test-data-system
priority: 0.92 (CRITICAL)
status: discovery
created: 2025-11-17
created_by: Hank (via personal log discovery)
source: santiago-pm/personal-logs/humans/2025-11-17-hank-workflow-test-data-feature.md
related_features:
  - F-027 (Personal Log Feature - needs executable tests)
  - F-026 (Lean-Kanban Backlog Management - needs workflow validation)
kerievsky_principles:
  - "Experiment & Learn Rapidly" (test to validate learning)
  - "Make Safety a Prerequisite" (test before deploy)
---
```

---

## Feature Overview

**Problem**: Testing Santiago's workflow capabilities (Lean-Kanban patterns, multi-agent coordination, state evolution) requires **realistic, evolving test data** that captures:
- Temporal patterns (state changing over time)
- Multi-agent interactions (PM, Architect, Dev, Ethicist, UX, humans)
- Git history (artifacts evolving)
- Knowledge graph evolution (knowledge accumulating)
- Workflow gates (safety, ethics, concurrency)
- Realistic project state (backlog, decisions, blockers)

**Current Gap**: 
- Unit tests use static fixtures (setup → execute → assert → teardown)
- BDD scenarios are documentation only (not executable)
- No way to test "what happens over 5 days of work" or "how do 3 agents coordinate?"
- Can't validate temporal reasoning ("why did we decide X on day 3?")

**Solution**: Build evolving test data system that:
1. **Accumulates state** across test scenarios (like real projects)
2. **Tracks time** (commit timestamps, KG timestamps, decision dates)
3. **Captures coordination** (agent message passing, human interactions)
4. **Enables temporal queries** ("what was KG state 3 commits ago?")
5. **Provides fixtures** for different maturity levels (Apprentice, Journeyman, Master)

**Key Insight**: Santiago's unique advantage is **temporal awareness** (git + KG + time). This feature enables us to **test that advantage** and **demonstrate it to users**.

---

## User Stories

### Story 1: Test Workflow State Evolution (MVP)

**As a Santiago developer**
**I want to test how work flows through Lean-Kanban states over multiple days**
**So that I can validate workflow patterns and gates work correctly**

**Given** a test project with initial state:
```yaml
backlog:
  - id: BI-001
    title: "Add user authentication"
    status: new
    priority: 0.85
    created: 2025-11-15
  
  - id: BI-002
    title: "Fix login bug"
    status: in-progress
    assigned_to: santiago-dev
    started: 2025-11-16
    blocked: false

knowledge_graph:
  - santiago_pm knows: "Modern Agile principles"
  - santiago_pm knows: "Lean-Kanban patterns"
  - decisions: []

git_state:
  - commit: abc123
  - files: ["README.md", "src/auth.py"]
  - timestamp: 2025-11-15T10:00
```

**When** I run workflow test scenarios over simulated time:

**Day 1** (2025-11-16):
```python
# Santiago-Dev completes BI-002
result = santiago_dev.complete_task("BI-002")
assert result.status == "done"
assert git.has_commit_by("santiago-dev", "Fix login bug")

# Santiago-PM moves BI-001 to in-progress
santiago_pm.prioritize_backlog()
assert backlog.item("BI-001").status == "in-progress"
```

**Day 2** (2025-11-17):
```python
# Santiago-Architect reviews BI-001 design
review = santiago_architect.review_design("BI-001")
assert review.approved == True  # Safety gate passes

# Santiago-Dev starts implementation
santiago_dev.start_task("BI-001")
assert backlog.item("BI-001").assigned_to == "santiago-dev"
```

**Day 3** (2025-11-18):
```python
# Human Hank adds requirement
hank.add_requirement("BI-001", "Must support OAuth")

# Santiago-PM detects scope change
alert = santiago_pm.detect_scope_change("BI-001")
assert alert.severity == "medium"
assert "OAuth" in alert.description
```

**Then** I can query temporal state:
```python
# What was backlog state on day 1?
state_day1 = backlog.at_date("2025-11-16")
assert len([x for x in state_day1 if x.status == "done"]) == 1

# When did BI-001 move to in-progress?
transition = backlog.item("BI-001").status_history()
assert transition["in-progress"]["date"] == "2025-11-16"

# What did Santiago-PM know on day 2?
knowledge_day2 = kg.at_date("2025-11-17").query("santiago_pm capabilities")
assert "Modern Agile" in knowledge_day2
```

**Acceptance Criteria**:
- [ ] Test fixtures define initial project state (backlog, KG, git)
- [ ] Test scenarios can "advance time" (day 1, day 2, day 3)
- [ ] State accumulates across scenarios (commit history grows)
- [ ] Temporal queries work: `at_date()`, `status_history()`, `kg.at_date()`
- [ ] Multiple agents can interact in same test (PM, Dev, Architect)
- [ ] Human interactions captured (add requirement, review, approve)

---

### Story 2: Test Multi-Agent Coordination (Journeyman)

**As a Santiago developer**
**I want to test how multiple Santiago agents coordinate work**
**So that I can validate message passing, concurrency control, and gates**

**Given** a test scenario with 4 agents working concurrently:
```yaml
agents:
  - santiago-pm: "Prioritizes backlog, coordinates work"
  - santiago-architect: "Reviews designs, approves changes"
  - santiago-dev: "Implements features, writes tests"
  - santiago-ethicist: "Safety gates, ethics reviews"

test_project:
  backlog:
    - BI-003: "Implement payment processing" (HIGH risk, needs ethics review)
    - BI-004: "Add logging" (LOW risk, no review needed)
```

**When** agents work on tasks with coordination:

**Scenario A**: High-risk task requires gates
```python
# Santiago-PM assigns BI-003 to Dev
santiago_pm.assign_task("BI-003", "santiago-dev")

# Santiago-Dev starts work, triggers safety gate
result = santiago_dev.start_task("BI-003")
assert result.status == "waiting_for_review"
assert result.gate == "ethics_review_required"

# Santiago-Ethicist reviews (auto-triggered)
review = santiago_ethicist.review_task("BI-003")
assert review.risk_level == "high"
assert review.concerns == ["PCI compliance", "data security"]

# If approved, work continues
if review.approved:
    santiago_dev.continue_task("BI-003")
    assert backlog.item("BI-003").status == "in-progress"
```

**Scenario B**: Low-risk task bypasses gates
```python
# Santiago-PM assigns BI-004 to Dev
santiago_pm.assign_task("BI-004", "santiago-dev")

# Santiago-Dev starts work, no gate triggered
result = santiago_dev.start_task("BI-004")
assert result.status == "in-progress"  # No waiting!
assert result.gate is None
```

**Scenario C**: Concurrent work with locking
```python
# Two agents try to work on same artifact
task1 = santiago_dev.start_task("BI-003")  # Touches auth.py
task2 = santiago_architect.review_file("auth.py")  # Also touches auth.py

# Concurrency control prevents conflict
assert task1.has_lock("auth.py") == True
assert task2.status == "waiting_for_lock"
```

**Then** I can validate coordination:
```python
# Message bus captured all interactions
messages = test_harness.get_messages()
assert any(m.type == "task_assigned" for m in messages)
assert any(m.type == "ethics_review_requested" for m in messages)
assert any(m.type == "safety_gate_passed" for m in messages)

# Timeline shows coordination
timeline = test_harness.get_timeline()
assert timeline[0] == ("10:00", "santiago-pm", "assign_task", "BI-003")
assert timeline[1] == ("10:01", "santiago-dev", "start_task", "BI-003")
assert timeline[2] == ("10:01", "santiago-ethicist", "review_triggered", "BI-003")
assert timeline[3] == ("10:05", "santiago-ethicist", "review_complete", "approved")
assert timeline[4] == ("10:06", "santiago-dev", "continue_task", "BI-003")
```

**Acceptance Criteria**:
- [ ] Multiple agents can work in same test scenario
- [ ] Safety gates trigger automatically based on risk level
- [ ] Concurrency control prevents conflicts (file locking)
- [ ] Message bus captures all agent interactions
- [ ] Timeline shows coordination sequence
- [ ] High-risk tasks require ethics review, low-risk bypass
- [ ] Human escalation works (if agent uncertain, ask human)

---

### Story 3: Test Temporal Reasoning (Master)

**As a Santiago developer**
**I want to test Santiago's ability to reason about past state and decisions**
**So that I can validate learning, provenance, and anomaly detection**

**Given** a test project with accumulated history:
```yaml
git_history:
  - commit: abc123 (2025-11-15)
    - Added: README.md, auth.py
    - Author: hank
  
  - commit: def456 (2025-11-16)
    - Modified: auth.py (add OAuth support)
    - Author: santiago-dev
    - Decision: "Use OAuth instead of basic auth for security"
  
  - commit: ghi789 (2025-11-17)
    - Added: test_auth.py
    - Author: santiago-dev
    - Tests: OAuth flow

knowledge_graph_evolution:
  - 2025-11-15T10:00: santiago_pm learns "Lean-Kanban workflow"
  - 2025-11-16T14:00: Decision: "Use OAuth for auth" (confidence: high)
  - 2025-11-17T09:00: santiago_pm learns "OAuth security best practices"

backlog_history:
  - BI-001:
      - 2025-11-15: created (priority: 0.85)
      - 2025-11-16: in-progress (assigned: santiago-dev)
      - 2025-11-17: done (completed in 2 days)
```

**When** I ask temporal reasoning questions:

**Query 1**: "Why did we choose OAuth?"
```python
explanation = santiago_pm.explain_decision("Use OAuth for auth")
assert explanation.decision_date == "2025-11-16"
assert "security" in explanation.rationale
assert explanation.alternatives == ["basic auth", "API keys"]
assert explanation.confidence == "high"
assert explanation.decided_by == "santiago-dev"
assert explanation.context == "During implementation of BI-001 auth feature"
```

**Query 2**: "What did we know about OAuth on Nov 15 vs Nov 17?"
```python
knowledge_nov15 = kg.at_date("2025-11-15").query("OAuth")
assert knowledge_nov15 == []  # Didn't know about OAuth yet

knowledge_nov17 = kg.at_date("2025-11-17").query("OAuth")
assert "security best practices" in knowledge_nov17
assert "OAuth flow" in knowledge_nov17
```

**Query 3**: "When did auth.py change and why?"
```python
history = git.file_history("auth.py")
assert len(history) == 2

assert history[0].date == "2025-11-15"
assert history[0].change == "created"
assert history[0].reason == "Initial auth implementation"

assert history[1].date == "2025-11-16"
assert history[1].change == "modified (OAuth support)"
assert history[1].reason == "Decision: Use OAuth instead of basic auth for security"
```

**Query 4**: "Detect anomaly - why is BI-002 taking longer than usual?"
```python
# BI-001 completed in 2 days
# BI-002 has been in-progress for 5 days (anomaly!)

anomaly = santiago_pm.detect_anomaly("BI-002")
assert anomaly.detected == True
assert anomaly.expected_duration == "2-3 days"  # Based on BI-001 pattern
assert anomaly.actual_duration == "5 days"
assert anomaly.possible_causes == ["blocked", "scope creep", "complexity underestimated"]

# Santiago-PM suggests action
suggestion = santiago_pm.suggest_action(anomaly)
assert "interview Hank" in suggestion or "review requirements" in suggestion
```

**Query 5**: "What's the provenance of safety gates in expeditions?"
```python
provenance = santiago_pm.trace_provenance("safety gates in expeditions")

assert provenance.origin == "Kerievsky's 'Make Safety a Prerequisite' principle"
assert provenance.discovered_via == "Personal log mention (2025-11-17)"
assert provenance.researched_by == "santiago-pm"
assert provenance.integrated_date == "2025-11-17"
assert "kerievsky-foundation.md" in provenance.knowledge_artifacts
assert "expedition-plan-template.md" in provenance.affected_artifacts
```

**Acceptance Criteria**:
- [ ] Explain decisions with rationale, alternatives, confidence, context
- [ ] Query KG state at any past date: `kg.at_date("YYYY-MM-DD")`
- [ ] Query git history with semantic understanding (why file changed)
- [ ] Detect anomalies by comparing current patterns to historical patterns
- [ ] Trace provenance from knowledge source → research → integration → usage
- [ ] Timeline queries: "when did X happen?", "what happened between T1 and T2?"
- [ ] Causality reasoning: "X caused Y because Z"

---

## Technical Design

### Test Data Structure

```
tests/
  fixtures/
    workflow/
      projects/
        simple/          # Apprentice-level: 1 agent, 3 backlog items, 1 week
          initial_state.yaml
          day1_scenario.yaml
          day2_scenario.yaml
          expected_outcomes.yaml
        
        medium/          # Journeyman-level: 2 agents, 10 items, 2 weeks
          initial_state.yaml
          coordination_scenarios.yaml
          expected_outcomes.yaml
        
        complex/         # Master-level: 4 agents, 30 items, 1 month
          initial_state.yaml
          multi_agent_scenarios.yaml
          temporal_reasoning_scenarios.yaml
          expected_outcomes.yaml
      
      snapshots/         # KG state at different times
        2025-11-15_kg_snapshot.ttl
        2025-11-17_kg_snapshot.ttl
      
      git_repos/         # Fixture git repositories
        simple_project/  # Git history for simple project
        complex_project/ # Git history for complex project
      
      schemas/
        backlog_item.yaml
        knowledge_graph_state.yaml
        agent_message.yaml
        decision_record.yaml
  
  bdd/
    workflow_evolution.feature
    multi_agent_coordination.feature
    temporal_reasoning.feature
  
  integration/
    test_workflow_state_evolution.py
    test_multi_agent_coordination.py
    test_temporal_reasoning.py
```

### Fixture Schema: Initial State

```yaml
# tests/fixtures/workflow/projects/simple/initial_state.yaml
---
project_name: "simple_test_project"
maturity_level: apprentice
agents:
  - name: santiago-pm
    capabilities: [prioritize, coordinate, assign]
    maturity: journeyman

humans:
  - name: hank
    role: product_owner

backlog:
  - id: BI-001
    title: "Add user authentication"
    description: "Implement OAuth-based authentication"
    status: new
    priority: 0.85
    created: 2025-11-15T10:00:00Z
    created_by: hank
    estimated_effort: 2 days
    tags: [security, authentication]
  
  - id: BI-002
    title: "Fix login bug"
    description: "Users can't login with special characters in password"
    status: in-progress
    priority: 0.95
    created: 2025-11-14T09:00:00Z
    assigned_to: santiago-dev
    started: 2025-11-16T10:00:00Z
    estimated_effort: 1 day
    tags: [bug, authentication]

knowledge_graph:
  agents:
    santiago-pm:
      knows:
        - "Lean-Kanban workflow patterns"
        - "Modern Agile principles"
      capabilities:
        - prioritize_backlog
        - assign_tasks
        - detect_anomalies
      maturity: journeyman
  
  decisions: []  # No decisions yet
  
  relationships:
    - subject: BI-001
      predicate: related_to
      object: BI-002
      reason: "Both touch authentication module"

git_state:
  repo_path: tests/fixtures/workflow/git_repos/simple_project
  initial_commit: abc123
  commits:
    - id: abc123
      date: 2025-11-15T10:00:00Z
      author: hank
      message: "Initial commit: Add README and auth stub"
      files:
        - path: README.md
          status: added
        - path: src/auth.py
          status: added
          content: "# Auth module stub"

workflow_gates:
  - name: ethics_review
    triggers:
      - condition: "risk_level > 0.7"
        action: "require_ethics_review"
    approvers: [santiago-ethicist, hank]
  
  - name: architecture_review
    triggers:
      - condition: "affects_core_architecture == true"
        action: "require_architect_review"
    approvers: [santiago-architect]

current_date: 2025-11-15T10:00:00Z
```

### Fixture Schema: Day Scenario

```yaml
# tests/fixtures/workflow/projects/simple/day1_scenario.yaml
---
scenario_name: "Day 1: Dev completes bug fix, PM starts new feature"
date: 2025-11-16T10:00:00Z

events:
  - time: "10:00"
    agent: santiago-dev
    action: complete_task
    params:
      task_id: BI-002
      result:
        status: done
        git_commit: def456
        commit_message: "Fix: Handle special chars in password validation"
        tests_passed: true
    expected_outcomes:
      - backlog.item("BI-002").status == "done"
      - git.has_commit("def456")
      - BI-002 moved to done column (Kanban)
  
  - time: "10:15"
    agent: santiago-pm
    action: prioritize_backlog
    params:
      criteria: [urgency, value, dependencies]
    expected_outcomes:
      - BI-001 moves to top of backlog
      - BI-001.priority recalculated
  
  - time: "10:30"
    agent: santiago-pm
    action: assign_task
    params:
      task_id: BI-001
      assignee: santiago-dev
    expected_outcomes:
      - BI-001.status == "in-progress"
      - BI-001.assigned_to == "santiago-dev"
      - BI-001.started timestamp set
  
  - time: "11:00"
    agent: santiago-dev
    action: start_task
    params:
      task_id: BI-001
    triggers:
      - gate: architecture_review
        reason: "Adding new auth module (affects core architecture)"
    expected_outcomes:
      - BI-001.status == "waiting_for_review"
      - message sent to santiago-architect
      - gate.architecture_review.triggered == true

assertions:
  backlog_state:
    - id: BI-001
      status: waiting_for_review
      assigned_to: santiago-dev
    - id: BI-002
      status: done
  
  git_state:
    commits: 2  # abc123 + def456
    latest_commit: def456
  
  knowledge_graph:
    decisions:
      - decision: "BI-001 requires architecture review"
        reason: "Affects core auth module"
        decided_by: santiago-dev
        timestamp: "2025-11-16T11:00:00Z"
  
  messages:
    - from: santiago-dev
      to: santiago-architect
      type: review_requested
      payload:
        task_id: BI-001
        reason: "New auth module affects architecture"
```

### Test Implementation Pattern

```python
# tests/integration/test_workflow_state_evolution.py

import pytest
from pathlib import Path
from datetime import datetime
from santiago_test_harness import WorkflowTestHarness

@pytest.fixture
def workflow_harness():
    """Create test harness with evolving state."""
    return WorkflowTestHarness(
        fixture_path="tests/fixtures/workflow/projects/simple/",
        enable_temporal_queries=True,
        enable_git_tracking=True,
        enable_kg_snapshots=True
    )

def test_workflow_state_evolution_over_3_days(workflow_harness):
    """
    Test that work flows correctly through Lean-Kanban states over 3 days.
    
    This tests:
    - State accumulation (commit history grows)
    - Temporal queries (what was state on day 2?)
    - Multi-agent coordination (PM assigns, Dev implements, Architect reviews)
    - Workflow gates (architecture review triggered)
    """
    # Load initial state
    harness = workflow_harness
    harness.load_initial_state("initial_state.yaml")
    
    # Verify initial state
    assert len(harness.backlog.items) == 2
    assert harness.backlog.item("BI-001").status == "new"
    assert harness.backlog.item("BI-002").status == "in-progress"
    assert harness.git.commit_count() == 1
    assert harness.kg.query("santiago-pm capabilities") is not None
    
    # === Day 1: Dev completes bug fix, PM starts new feature ===
    harness.advance_to_date("2025-11-16T10:00:00Z")
    harness.run_scenario("day1_scenario.yaml")
    
    # Verify day 1 outcomes
    assert harness.backlog.item("BI-002").status == "done"
    assert harness.backlog.item("BI-001").status == "waiting_for_review"
    assert harness.git.commit_count() == 2
    
    # Verify gates triggered
    assert harness.gates.is_active("architecture_review", "BI-001") == True
    
    # Verify messages sent
    messages = harness.message_bus.get_messages(date="2025-11-16")
    assert any(m.type == "review_requested" for m in messages)
    
    # === Day 2: Architect approves, Dev implements ===
    harness.advance_to_date("2025-11-17T09:00:00Z")
    
    # Architect reviews and approves
    review = harness.agents.santiago_architect.review_task("BI-001")
    assert review.approved == True
    assert harness.backlog.item("BI-001").status == "in-progress"
    
    # Dev implements feature
    result = harness.agents.santiago_dev.work_on_task("BI-001", duration_hours=4)
    assert result.progress == 0.5  # 50% done after 4 hours
    assert harness.git.commit_count() == 3  # New commit
    
    # === Day 3: Dev completes, PM closes ===
    harness.advance_to_date("2025-11-18T10:00:00Z")
    
    # Dev completes implementation
    result = harness.agents.santiago_dev.complete_task("BI-001")
    assert result.status == "done"
    assert result.tests_passed == True
    
    # PM reviews and closes
    harness.agents.santiago_pm.close_task("BI-001")
    assert harness.backlog.item("BI-001").status == "done"
    
    # === Temporal Reasoning Assertions ===
    
    # Query: What was backlog state on day 1?
    backlog_day1 = harness.backlog.at_date("2025-11-16")
    assert len([x for x in backlog_day1 if x.status == "done"]) == 1  # BI-002
    assert len([x for x in backlog_day1 if x.status == "waiting_for_review"]) == 1  # BI-001
    
    # Query: When did BI-001 move to in-progress?
    history = harness.backlog.item("BI-001").status_history()
    assert history["in-progress"]["date"] == "2025-11-17T09:30:00Z"
    assert history["in-progress"]["triggered_by"] == "architecture_review_approved"
    
    # Query: What did Santiago-PM know on day 2 vs day 3?
    kg_day2 = harness.kg.at_date("2025-11-17")
    kg_day3 = harness.kg.at_date("2025-11-18")
    
    assert kg_day2.query("BI-001 status") == "in-progress"
    assert kg_day3.query("BI-001 status") == "done"
    
    # Query: Timeline of BI-001
    timeline = harness.timeline.for_item("BI-001")
    assert timeline[0] == ("2025-11-15T10:00", "created", "by hank")
    assert timeline[1] == ("2025-11-16T10:30", "assigned", "to santiago-dev")
    assert timeline[2] == ("2025-11-16T11:00", "gate_triggered", "architecture_review")
    assert timeline[3] == ("2025-11-17T09:30", "gate_approved", "by santiago-architect")
    assert timeline[4] == ("2025-11-17T09:30", "status_changed", "to in-progress")
    assert timeline[5] == ("2025-11-18T10:00", "completed", "by santiago-dev")
    assert timeline[6] == ("2025-11-18T10:15", "closed", "by santiago-pm")
    
    # Query: Git evolution
    git_history = harness.git.file_history("src/auth.py")
    assert len(git_history) == 3  # Initial + bug fix + OAuth feature
    assert git_history[2].commit_message == "feat: Add OAuth authentication"
    assert git_history[2].related_to == "BI-001"
    
    # Query: Provenance - why OAuth?
    decision = harness.kg.decisions.find("Use OAuth for authentication")
    assert decision.decided_by == "santiago-dev"
    assert decision.date == "2025-11-17"
    assert decision.context == "Implementing BI-001 auth feature"
    assert "security" in decision.rationale


def test_multi_agent_coordination_with_gates(workflow_harness):
    """
    Test that multiple agents coordinate correctly with safety gates.
    
    This tests:
    - Concurrent work (multiple agents active)
    - Safety gates (ethics review for high-risk)
    - Concurrency control (file locking)
    - Message passing (agents communicate)
    """
    harness = workflow_harness
    harness.load_initial_state("initial_state.yaml")
    
    # Add high-risk task
    harness.backlog.add_item({
        "id": "BI-003",
        "title": "Implement payment processing",
        "risk_level": 0.85,  # HIGH risk
        "requires_ethics_review": True
    })
    
    # Santiago-PM assigns high-risk task
    harness.agents.santiago_pm.assign_task("BI-003", "santiago-dev")
    
    # Santiago-Dev starts task → SHOULD TRIGGER ETHICS GATE
    result = harness.agents.santiago_dev.start_task("BI-003")
    
    assert result.status == "waiting_for_review"
    assert result.gate == "ethics_review_required"
    
    # Verify message sent to Santiago-Ethicist
    messages = harness.message_bus.get_messages()
    assert any(
        m.type == "ethics_review_requested" and
        m.payload["task_id"] == "BI-003"
        for m in messages
    )
    
    # Santiago-Ethicist reviews (auto-triggered)
    review = harness.agents.santiago_ethicist.review_task("BI-003")
    assert review.risk_level == "high"
    assert "PCI compliance" in review.concerns
    
    # If approved, work continues
    assert review.approved == True
    assert harness.backlog.item("BI-003").status == "in-progress"
    
    # Test concurrency control
    # Two agents try to modify same file
    task1 = harness.agents.santiago_dev.start_task("BI-003")  # Locks payment.py
    task2 = harness.agents.santiago_architect.review_file("payment.py")
    
    assert task1.has_lock("payment.py") == True
    assert task2.status == "waiting_for_lock"
    assert task2.blocked_by == "santiago-dev"


def test_temporal_reasoning_and_provenance(workflow_harness):
    """
    Test Santiago's ability to reason about past state and decisions.
    
    This tests:
    - Decision provenance (why did we decide X?)
    - Temporal queries (what did we know at time T?)
    - Anomaly detection (why is this taking longer?)
    - Causality reasoning (X caused Y)
    """
    harness = workflow_harness
    harness.load_initial_state("initial_state.yaml")
    
    # Accumulate history over several days
    harness.run_scenario("day1_scenario.yaml")
    harness.run_scenario("day2_scenario.yaml")
    harness.run_scenario("day3_scenario.yaml")
    
    # Query: Why did we choose OAuth?
    decision = harness.agents.santiago_pm.explain_decision("Use OAuth for auth")
    assert decision.rationale contains "security"
    assert decision.alternatives == ["basic auth", "API keys"]
    assert decision.confidence == "high"
    assert decision.decided_by == "santiago-dev"
    
    # Query: What did we know about OAuth on day 1 vs day 3?
    kg_day1 = harness.kg.at_date("2025-11-16")
    kg_day3 = harness.kg.at_date("2025-11-18")
    
    assert kg_day1.query("OAuth") == []  # Didn't know yet
    assert "OAuth security best practices" in kg_day3.query("OAuth")
    
    # Query: Detect anomaly
    # BI-001 completed in 2 days, BI-004 taking 5 days
    anomaly = harness.agents.santiago_pm.detect_anomaly("BI-004")
    assert anomaly.detected == True
    assert anomaly.expected_duration == "2-3 days"
    assert anomaly.actual_duration == "5 days"
    
    # Query: Trace provenance of safety gates
    provenance = harness.agents.santiago_pm.trace_provenance("safety gates")
    assert provenance.origin == "Kerievsky's 'Make Safety a Prerequisite'"
    assert provenance.discovered_via == "Personal log mention"
    assert provenance.knowledge_artifact == "kerievsky-foundation.md"
```

---

## Implementation Phases

### Phase 1: Foundation (Week 1) - CRITICAL

**Goal**: Basic test data structure + temporal queries

**Tasks**:
- [ ] Create test harness framework (`WorkflowTestHarness` class)
- [ ] Define fixture schemas (YAML format for initial state, scenarios)
- [ ] Implement `at_date()` temporal queries for backlog, KG, git
- [ ] Create 1 simple fixture (apprentice-level, 3 items, 1 week)
- [ ] Write 1 executable test using pytest
- [ ] Document fixture creation patterns

**Deliverables**:
- `santiago_test_harness.py` (core test framework)
- `tests/fixtures/workflow/schemas/` (YAML schemas)
- `tests/fixtures/workflow/projects/simple/` (1 fixture)
- `tests/integration/test_workflow_basics.py` (1 test)
- `WORKFLOW-TESTING.md` (documentation)

**Success Criteria**:
- Test can load fixture, advance time, query past state
- `backlog.at_date("2025-11-16")` returns correct historical state
- Git history tracked with commit timestamps
- KG snapshots saved at each scenario step

---

### Phase 2: Multi-Agent Coordination (Week 2)

**Goal**: Test agent interactions, gates, concurrency

**Tasks**:
- [ ] Implement message bus capture in test harness
- [ ] Add workflow gates (safety, ethics, architecture review)
- [ ] Add concurrency control (file locking)
- [ ] Create medium fixture (journeyman-level, 10 items, 2 agents, 2 weeks)
- [ ] Write multi-agent coordination tests
- [ ] Add timeline visualization (agent actions over time)

**Deliverables**:
- Message bus integration in test harness
- Gate triggering logic
- Concurrency control (locking)
- `tests/fixtures/workflow/projects/medium/` (1 fixture)
- `tests/integration/test_multi_agent_coordination.py`
- Timeline visualization utility

**Success Criteria**:
- Gates trigger automatically based on rules
- Concurrency control prevents conflicts
- Message bus captures all agent communications
- Timeline shows coordination sequence

---

### Phase 3: Temporal Reasoning (Week 3)

**Goal**: Test learning, provenance, anomaly detection

**Tasks**:
- [ ] Implement decision provenance tracking
- [ ] Add `explain_decision()` capability
- [ ] Add `detect_anomaly()` (compare to historical patterns)
- [ ] Add `trace_provenance()` (knowledge source → integration)
- [ ] Create complex fixture (master-level, 30 items, 4 agents, 1 month)
- [ ] Write temporal reasoning tests
- [ ] Create BDD scenarios for temporal queries

**Deliverables**:
- Decision provenance system
- Anomaly detection algorithm
- `tests/fixtures/workflow/projects/complex/` (1 fixture)
- `tests/integration/test_temporal_reasoning.py`
- `tests/bdd/temporal_reasoning.feature` (executable BDD)

**Success Criteria**:
- Can explain any decision with rationale, alternatives, confidence
- Anomaly detection finds tasks taking longer than historical average
- Provenance traces knowledge from source to usage
- Complex fixture tests 1 month of work with 4 agents

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Fixture Coverage | 3 levels | Apprentice, Journeyman, Master fixtures |
| Temporal Query Speed | < 100ms | `backlog.at_date()`, `kg.at_date()` |
| Test Execution Time | < 30s | Full integration test suite |
| State Accuracy | 100% | Historical state matches expected |
| Coordination Validation | 95% | Gates, locks, messages work correctly |
| Provenance Completeness | 90% | Can trace 90% of decisions to source |
| Developer Satisfaction | > 4.5/5 | "Easy to write workflow tests" |

---

## Dependencies

- **pytest** (test runner)
- **pytest-bdd** (BDD scenario execution)
- **PyYAML** (fixture loading)
- **gitpython** (git history tracking)
- **rdflib** (KG snapshots)
- **freezegun** (time manipulation in tests)

---

## Risk Assessment

### High Risks

1. **Performance**: Temporal queries may be slow (loading full KG history)
   - **Mitigation**: Snapshot KG at key points, cache queries, use indexing
   - **Backup**: This is where vector DB / Redis feature helps (from earlier hint)

2. **Complexity**: Evolving state harder to debug than static fixtures
   - **Mitigation**: Timeline visualization, clear error messages, snapshot diffs
   - **Backup**: Start simple (phase 1), add complexity incrementally

3. **Maintenance**: Fixtures need updating as Santiago evolves
   - **Mitigation**: Schema versioning, migration scripts, clear documentation
   - **Backup**: Automated fixture validation on CI

### Medium Risks

4. **Test Interdependence**: If state accumulates, tests may depend on each other
   - **Mitigation**: Each test starts from clean snapshot, explicit dependencies
   - **Backup**: Isolated test mode (fresh state each test)

5. **Git Conflicts**: Multiple tests creating git repos may conflict
   - **Mitigation**: Each test gets own temp git repo, cleanup after test
   - **Backup**: Use test-specific namespaces

---

## Related Work & Research

Need to research how other systems handle workflow testing:

1. **Temporal.io**: Workflow testing framework
   - How do they test workflows that run for days/weeks?
   - Do they use time acceleration?
   - How handle state snapshots?

2. **Cadence** (Uber): Workflow engine testing
   - Testing patterns for distributed workflows
   - Replay testing (run workflow against history)

3. **Airflow**: DAG testing patterns
   - How test task dependencies and orchestration?
   - How validate execution order?

4. **Time-series databases**: Testing temporal data
   - How query historical state efficiently?
   - Indexing strategies for time-based queries?

5. **Event Sourcing**: Testing event-driven systems
   - How replay events to recreate state?
   - How validate event sequences?

---

## Future Enhancements

(Not in scope for MVP, but identified for later)

1. **Fixture Generator**: Auto-generate realistic fixtures from real projects
2. **Visual Test Debugger**: See timeline, state transitions, agent messages in UI
3. **Performance Benchmarking**: Track test execution time, identify bottlenecks
4. **Chaos Testing**: Introduce random failures, test recovery
5. **Replay Mode**: Re-run actual project history in tests (ultimate validation!)
6. **Test Data Marketplace**: Share fixtures across teams (like Kaggle datasets)

---

## Metadata

```yaml
cargo_manifest:
  feature_id: F-028
  feature_name: workflow-test-data-system
  priority: 0.92 (CRITICAL)
  estimated_effort: 3 weeks
  complexity: high
  risk_level: medium
  
  value_proposition: |
    - Test Santiago's unique differentiator (temporal awareness)
    - Validate Lean-Kanban patterns with real workflows
    - Enable BDD scenarios to be executable tests
    - Foundation for all future workflow features
  
  key_insight: |
    Santiago's temporal awareness (git + KG + time) requires
    temporal test data. This is a hard problem but Santiago
    is uniquely positioned to solve it. No other PM tool does this.
  
  phases:
    - phase: 1
      name: foundation
      duration: 1 week
      deliverables: test harness, temporal queries, 1 simple fixture
      critical: true
    
    - phase: 2
      name: coordination
      duration: 1 week
      deliverables: multi-agent tests, gates, 1 medium fixture
      critical: false
    
    - phase: 3
      name: reasoning
      duration: 1 week
      deliverables: temporal reasoning tests, 1 complex fixture
      critical: false
  
  dependencies: []  # Can start immediately
  
  related_features:
    - F-027: Personal Log (needs executable tests)
    - F-026: Lean-Kanban Backlog (needs workflow validation)
    - Future: Vector DB / Redis (performance optimization)
  
  discovered_via:
    artifact: santiago-pm/personal-logs/humans/2025-11-17-hank-workflow-test-data-feature.md
    date: 2025-11-17
    context: "Reviewing BDD scenarios, realized need executable tests + evolving state"
```

---

**Meta**: This cargo manifest was created from a personal log entry, demonstrating the feature extraction pattern we're building. If Santiago-PM reads the personal log that spawned this manifest, it should recognize the provenance chain and create semantic links. Full circle. 🚢
