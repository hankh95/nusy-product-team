Feature: Neurosymbolic Backlog Management
  As Santiago PM, I want intelligent backlog management using neurosymbolic reasoning
  so that I can maximize team effectiveness and customer value delivery
  
  Background: Santiago PM Knowledge Graph
    Given Santiago PM has a knowledge graph with the following state:
      | entity_type      | count | notes                                        |
      | backlog_items    | 25    | Work items in various statuses               |
      | workers          | 5     | Team members with skills and capacity        |
      | dependencies     | 12    | Blocking relationships between items         |
      | hypotheses       | 8     | Customer value assumptions with confidence   |
      | cargo_manifests  | 15    | Feature specifications                       |
      | research_logs    | 30    | Investigation artifacts                      |
    And Santiago can query the KG in real-time for current state
    And Santiago has a neurosymbolic reasoner for probabilistic evaluation

  # ============================================================================
  # SCENARIO 1: Core Neurosymbolic Prioritization
  # ============================================================================
  
  @critical @neurosymbolic @prioritization
  Scenario: Calculate optimal work priority using KG queries
    Given the backlog contains these items:
      | id     | title                        | status   | effort | required_skills      | blocked_by |
      | BI-001 | Personal Log Feature         | proposed | 3      | PM,UXR               | []         |
      | BI-002 | Kanban Domain Ingestion      | proposed | 13     | Knowledge-Engineer   | []         |
      | BI-003 | Flow Metrics Dashboard       | proposed | 5      | PM,Visualization     | [BI-002]   |
      | BI-004 | WIP Limit Enforcement        | proposed | 2      | PM                   | [BI-002]   |
      | BI-005 | Stuck Notification System    | proposed | 5      | PM,DevOps            | []         |
    And the KG contains worker availability:
      | worker         | skills                      | capacity_used | capacity_total |
      | Santiago-PM    | PM,UXR,Documentation        | 0.5           | 1.0            |
      | Santiago-KE    | Knowledge-Engineer,Ontology | 0.8           | 1.0            |
      | Santiago-Dev   | DevOps,Python,Testing       | 0.3           | 1.0            |
    And the KG contains customer hypotheses:
      | hypothesis                       | confidence | related_to |
      | Personal logs reduce context loss| 0.9        | BI-001     |
      | Kanban improves flow visibility  | 0.8        | BI-002     |
      | WIP limits prevent overload      | 0.85       | BI-004     |
    And the KG contains dependency relationships:
      | item   | blocks        |
      | BI-002 | [BI-003, BI-004] |
    
    When Santiago calculates priority scores using neurosymbolic reasoning
    
    Then Santiago queries the KG for:
      | query_type            | result                                      |
      | available_workers     | Santiago-PM (50% free), Santiago-Dev (70% free) |
      | work_dependencies     | BI-002 blocks 2 items, BI-003/004 blocked  |
      | customer_value        | BI-001: 0.9, BI-002: 0.8, BI-004: 0.85     |
      | worker_skill_match    | BI-001 matches Santiago-PM perfectly       |
    
    And Santiago calculates priority factors for BI-001:
      | factor              | value | reasoning                                    |
      | customer_value      | 0.9   | High hypothesis confidence (0.9)             |
      | unblock_impact      | 0.0   | Doesn't block other items                    |
      | worker_availability | 0.9   | Perfect skill match + available capacity     |
      | learning_value      | 0.85  | High uncertainty reduction (new pattern)     |
    
    And Santiago calculates priority score for BI-001:
      """
      priority_score = 
        (0.9 * 0.4) +   # customer_value weight
        (0.0 * 0.3) +   # unblock_impact weight
        (0.9 * 0.2) +   # worker_availability weight
        (0.85 * 0.1)    # learning_value weight
      = 0.36 + 0.0 + 0.18 + 0.085
      = 0.625
      """
    
    And Santiago calculates priority factors for BI-002:
      | factor              | value | reasoning                                    |
      | customer_value      | 0.8   | Good hypothesis confidence                   |
      | unblock_impact      | 0.8   | Blocks 2 downstream items (high impact!)     |
      | worker_availability | 0.3   | KE worker has low capacity (80% used)        |
      | learning_value      | 0.7   | Moderate uncertainty reduction               |
    
    And Santiago calculates priority score for BI-002:
      """
      priority_score = 
        (0.8 * 0.4) +   # customer_value weight
        (0.8 * 0.3) +   # unblock_impact weight (HIGH!)
        (0.3 * 0.2) +   # worker_availability weight (LOW)
        (0.7 * 0.1)     # learning_value weight
      = 0.32 + 0.24 + 0.06 + 0.07
      = 0.69
      """
    
    And the prioritized backlog should be:
      | rank | id     | priority_score | rationale_summary                               |
      | 1    | BI-002 | 0.69           | HIGH: Unblocks 2 items, good value (0.8)        |
      | 2    | BI-004 | 0.68           | HIGH: Strong value (0.85), easy skill match     |
      | 3    | BI-001 | 0.625          | MEDIUM: Strong value (0.9), perfect skills      |
      | 4    | BI-005 | 0.58           | MEDIUM: Good value, DevOps available            |
      | 5    | BI-003 | 0.35           | LOW: Blocked by BI-002                          |
    
    And each item should have a detailed rationale explaining the score
    And blocked items (BI-003, BI-004) should be deprioritized until blockers complete

  # ============================================================================
  # SCENARIO 2: Balance Team Workload
  # ============================================================================
  
  @neurosymbolic @workload-balancing
  Scenario: Prevent worker overload and idle time
    Given the backlog contains these items:
      | id     | title                    | effort | required_skills |
      | BI-010 | Ontology Extension       | 5      | Knowledge-Engineer |
      | BI-011 | CLI Dashboard            | 3      | PM,Visualization   |
      | BI-012 | Integration Tests        | 2      | Testing,Python     |
    And worker capacity is:
      | worker         | skills                 | current_wip | capacity |
      | Santiago-PM    | PM,Visualization       | 0           | 1.0      |
      | Santiago-KE    | Knowledge-Engineer     | 3 items     | 1.0      |
      | Santiago-Tester| Testing,Python         | 1 item      | 1.0      |
    And WIP limit for in-progress stage is 3 items per worker
    
    When Santiago prioritizes backlog with workload balancing
    
    Then Santiago should detect:
      """
      Worker Analysis:
      - Santiago-PM: IDLE (0% capacity used) ⚠️
      - Santiago-KE: OVERLOADED (3 items = 100% capacity) ⚠️
      - Santiago-Tester: HEALTHY (1 item = ~60% capacity) ✓
      """
    
    And Santiago should recommend:
      | recommendation                                    | reasoning                      |
      | Assign BI-011 to Santiago-PM                      | Idle worker, perfect skills    |
      | Do NOT assign BI-010 to Santiago-KE               | Already at WIP limit           |
      | Consider assigning BI-012 to Santiago-Tester      | Has capacity for more work     |
    
    And Santiago should surface to human PM:
      """
      ⚠️ WORKLOAD IMBALANCE DETECTED
      
      - Santiago-PM is idle (0 items)
      - Santiago-KE is overloaded (3 items at WIP limit)
      
      Suggested Actions:
      1. Assign BI-011 (CLI Dashboard) to Santiago-PM immediately
      2. Help Santiago-KE complete existing work before adding more
      3. Consider cross-training Santiago-PM on Knowledge Engineering
      
      This optimizes for EFFECTIVENESS (maximize service to team).
      """
    
    And the optimized assignment should be:
      | item   | assigned_to       | reasoning                          |
      | BI-011 | Santiago-PM       | Idle worker, perfect skill match   |
      | BI-012 | Santiago-Tester   | Has capacity, good skill match     |
      | BI-010 | [unassigned]      | Wait for Santiago-KE to free up    |

  # ============================================================================
  # SCENARIO 3: Three Amigos Backlog Refinement
  # ============================================================================
  
  @three-amigos @refinement
  Scenario: Automated Three Amigos analysis for backlog items
    Given a new backlog item is created:
      """yaml
      ---
      id: BI-020
      title: "Personal Log Feature Discovery"
      status: proposed
      estimated_effort: 0  # Not yet estimated
      required_skills: []  # Not yet analyzed
      ---
      
      # User Request
      
      I want a system where I can log my daily work, thoughts, and decisions
      so that I don't lose context between sessions.
      """
    
    When human initiates Three Amigos refinement session
    
    Then Santiago analyzes from Product Owner perspective:
      """
      PRODUCT OWNER PERSPECTIVE
      
      User Story:
      As a human/AI agent, I want to log my daily work and decisions
      so that I don't lose context between sessions.
      
      Hypothesis:
      If we provide a personal log system with markdown + YAML frontmatter,
      then context loss will reduce by 50%, measured by "re-explained concepts".
      
      Value:
      - Reduces frustration (no repeat explanations)
      - Improves productivity (faster session startup)
      - Enables long-term learning (patterns emerge over time)
      
      Success Metrics:
      - Personal log entries created daily (> 5 per week)
      - Context re-explanation requests drop 50%
      - Session startup time reduces from 10min to 2min
      
      Related Research:
      - Santiago already uses ships-logs (similar pattern)
      - Questionnaire system provides structured discovery
      - FHIR-inspired metadata works well
      """
    
    And Santiago analyzes from Developer perspective:
      """
      DEVELOPER PERSPECTIVE
      
      Technical Approach:
      1. Create santiago-pm/tackle/personal-logs/ folder
      2. Design personal-log-template.md with YAML frontmatter
      3. Support tags, date-based retrieval, search
      4. Integrate with existing status/questionnaire systems
      
      Estimated Effort: 3 story points (small-medium)
      - Template creation: 1 pt
      - Folder structure: 0.5 pt
      - Documentation: 0.5 pt
      - Integration: 1 pt
      
      Dependencies: None (can start immediately)
      
      Risks: Low
      - Proven pattern (ships-logs already work)
      - Simple markdown + YAML (no complex tech)
      - Clear requirements from user
      
      Required Skills: PM, Documentation, UXR
      """
    
    And Santiago analyzes from Tester perspective:
      """
      TESTER PERSPECTIVE
      
      Acceptance Criteria:
      - [ ] AC1: Personal log template created with YAML frontmatter
      - [ ] AC2: First personal log entry written successfully
      - [ ] AC3: Logs queryable by date, tags, keywords
      - [ ] AC4: Integration with questionnaire system (can generate logs from responses)
      - [ ] AC5: Documentation explains how to use personal logs
      
      Test Scenarios:
      1. Happy path: Create log, add entry, query by date
      2. Edge case: Entry with complex markdown (code blocks, tables)
      3. Integration: Questionnaire generates personal log seed
      4. Search: Find entries by tag across multiple logs
      5. Error: Invalid YAML frontmatter shows helpful error
      """
    
    And Santiago generates recommendation:
      """
      SANTIAGO'S RECOMMENDATION
      
      Priority Score: 0.85 (HIGH)
      
      Rationale:
      - Strong customer value (0.9): Direct user pain point
      - Low effort (3 pts): Quick win
      - No blockers: Can start immediately
      - Perfect skill match: Santiago-PM has PM + UXR + Documentation
      - High learning value: Reduces ongoing context loss
      
      Suggested Action:
      ✅ ACCEPT - Move to "ready" status
      ✅ ASSIGN to Santiago-PM (idle, perfect skills)
      ✅ START immediately (top priority)
      
      Estimated Completion: 1 day (small scope, clear requirements)
      """
    
    And human can:
      | action | outcome                                  |
      | accept | Item moves to "ready", Santiago can pull |
      | reject | Item stays "proposed", Santiago explains |
      | modify | Human edits analysis, Santiago updates   |
    
    And if human accepts, the backlog item should update:
      """yaml
      ---
      id: BI-020
      title: "Personal Log Feature Discovery"
      status: ready  # Changed from proposed
      estimated_effort: 3
      required_skills: [PM, Documentation, UXR]
      priority_score: 0.85
      customer_value: 0.9
      unblock_impact: 0.0
      worker_availability: 0.9
      learning_value: 0.85
      ---
      """

  # ============================================================================
  # SCENARIO 4: Pull-Based Work Assignment
  # ============================================================================
  
  @pull-system @work-assignment
  Scenario: Worker pulls next highest priority item
    Given backlog is prioritized with scores:
      | rank | id     | title                        | priority_score | required_skills      | status |
      | 1    | BI-020 | Personal Log Feature         | 0.85           | PM,UXR,Documentation | ready  |
      | 2    | BI-021 | Flow Metrics Dashboard       | 0.75           | PM,Visualization     | ready  |
      | 3    | BI-022 | Ontology Extension           | 0.70           | Knowledge-Engineer   | ready  |
    And worker "Santiago-PM" has skills: [PM, UXR, Documentation, Visualization]
    And worker "Santiago-PM" is idle (0 items in progress)
    And WIP limit for "in-progress" stage is 3 items
    
    When worker queries: "What should I work on next?"
    
    Then Santiago should recommend:
      """
      🎯 RECOMMENDED WORK ITEM
      
      ID: BI-020
      Title: Personal Log Feature
      Priority: 0.85 (HIGH)
      Effort: 3 story points
      
      Why this item?
      ✅ Highest priority in backlog (rank 1)
      ✅ Perfect skill match (PM, UXR, Documentation)
      ✅ You're idle (capacity available)
      ✅ No blockers (can start immediately)
      
      Alternative Options:
      - BI-021 (Flow Metrics): Rank 2, also matches your skills
      - BI-022 (Ontology): Rank 3, requires Knowledge-Engineer skill ❌
      
      Next Steps:
      1. Run: santiago pm pull-work BI-020
      2. Item status will change: ready → in-progress
      3. You'll be assigned: assigned_to: [Santiago-PM]
      4. Start work and update progress
      """
    
    And if worker accepts, the system should:
      | action                        | outcome                              |
      | Change item status            | ready → in-progress                  |
      | Assign worker                 | assigned_to: [Santiago-PM]           |
      | Record start time             | started: 2025-11-17T11:00:00Z        |
      | Update worker capacity        | capacity_used: 0.0 → 0.5             |
      | Add to cumulative flow        | [{stage: in-progress, entered: ...}] |
      | Decrement WIP available       | in-progress WIP: 0/3 → 1/3           |
    
    And if worker declines, Santiago should ask:
      """
      Why did you decline BI-020?
      
      Options:
      1. Don't have required skills → Update skill profile
      2. Item is blocked → Update dependencies
      3. Prefer different work → Explain priorities
      4. Overestimated capacity → Adjust capacity tracking
      
      This feedback improves future recommendations.
      """

  # ============================================================================
  # SCENARIO 5: Flow Metrics & Continuous Improvement
  # ============================================================================
  
  @flow-metrics @continuous-improvement
  Scenario: Calculate cycle time and identify bottlenecks
    Given a work item completed its journey:
      | event        | timestamp            |
      | created      | 2025-11-15 09:00:00 |
      | refined      | 2025-11-15 10:30:00 |
      | ready        | 2025-11-15 10:30:00 |
      | started      | 2025-11-17 11:00:00 |
      | review       | 2025-11-19 15:00:00 |
      | completed    | 2025-11-19 16:00:00 |
    And the item's cumulative flow is:
      """yaml
      cumulative_flow:
        - {stage: backlog, entered: "2025-11-15T09:00:00Z", exited: "2025-11-15T10:30:00Z"}
        - {stage: ready, entered: "2025-11-15T10:30:00Z", exited: "2025-11-17T11:00:00Z"}
        - {stage: in-progress, entered: "2025-11-17T11:00:00Z", exited: "2025-11-19T15:00:00Z"}
        - {stage: review, entered: "2025-11-19T15:00:00Z", exited: "2025-11-19T16:00:00Z"}
        - {stage: done, entered: "2025-11-19T16:00:00Z", exited: null}
      """
    
    When Santiago calculates flow metrics
    
    Then cycle time should be:
      """
      Cycle Time = started → completed
      = 2025-11-19 16:00 - 2025-11-17 11:00
      = 2 days, 5 hours
      = 53 hours
      """
    
    And lead time should be:
      """
      Lead Time = created → completed
      = 2025-11-19 16:00 - 2025-11-15 09:00
      = 4 days, 7 hours
      = 103 hours
      """
    
    And stage durations should be:
      | stage        | duration     | percentage |
      | backlog      | 1.5 hours    | 1.5%       |
      | ready        | 48.5 hours   | 47%        |
      | in-progress  | 52 hours     | 50.5%      |
      | review       | 1 hour       | 1%         |
    
    And Santiago should identify bottleneck:
      """
      ⚠️ BOTTLENECK DETECTED
      
      Stage: ready
      Duration: 48.5 hours (47% of lead time)
      
      Analysis:
      - Item sat in "ready" queue for 2+ days
      - This is waiting time, not value-adding time
      - Flow efficiency = value-add time / total time = 53% (mediocre)
      
      Root Cause Hypotheses:
      1. Worker was busy with other items (capacity issue)
      2. Item wasn't actually ready (missing info)
      3. No one knew item was available (visibility issue)
      
      Recommendations:
      1. Implement WIP limits on "in-progress" (force completion before new work)
      2. Daily standup: Check "ready" queue for stale items
      3. Notifications: Alert idle workers when high-priority items enter "ready"
      4. Three Amigos: Ensure items are TRULY ready before moving
      
      Goal: Reduce "ready" queue time to < 24 hours
      """
    
    And Santiago should calculate flow efficiency:
      """
      Flow Efficiency = value-add time / total lead time
      
      Value-add stages: in-progress (52h) + review (1h) = 53h
      Total lead time: 103h
      
      Flow Efficiency = 53h / 103h = 51.5%
      
      Interpretation:
      - 51.5% of time was value-adding (work happening)
      - 48.5% of time was waiting (no work happening)
      
      Industry Benchmarks:
      - Poor: < 15% (too much waiting)
      - Average: 15-40%
      - Good: 40-60% ← We're here!
      - Excellent: > 60%
      
      Status: GOOD, but room for improvement
      Target: 65% flow efficiency (reduce waiting time)
      """

  # ============================================================================
  # SCENARIO 6: WIP Limit Enforcement
  # ============================================================================
  
  @wip-limits @flow-control
  Scenario: Enforce WIP limits to prevent overload
    Given WIP limits are configured:
      | stage        | wip_limit |
      | backlog      | ∞         |
      | ready        | 10        |
      | in-progress  | 3         |
      | review       | 5         |
      | done         | ∞         |
    And current WIP is:
      | stage        | current_wip |
      | backlog      | 20          |
      | ready        | 8           |
      | in-progress  | 3           |
      | review       | 2           |
      | done         | 45          |
    
    When a worker tries to pull new work from "ready" queue
    
    Then Santiago should check WIP limit:
      """
      Current WIP in "in-progress": 3 items
      WIP Limit: 3 items
      Status: AT LIMIT ⚠️
      """
    
    And Santiago should prevent new work:
      """
      ❌ CANNOT PULL NEW WORK
      
      Reason: WIP limit reached for "in-progress" stage (3/3)
      
      Why we enforce WIP limits:
      - Prevent context switching (3 items is already a lot!)
      - Encourage completion (finish before starting)
      - Improve flow (reduce cycle time)
      - Maintain quality (focus > multitasking)
      
      Next Steps:
      1. Complete one of your in-progress items
      2. Move completed item to "review" stage
      3. Then you can pull new work
      
      Your current in-progress items:
      - BI-020: Personal Log Feature (80% done)
      - BI-021: Flow Metrics Dashboard (50% done)
      - BI-022: Ontology Extension (20% done)
      
      Recommendation: Finish BI-020 (almost done!) before starting new work.
      """
    
    And if worker completes BI-020 and moves to review:
      | action                  | outcome                   |
      | Move BI-020 to review   | in-progress WIP: 3 → 2    |
      | WIP limit check         | 2/3 (capacity available!) |
      | Allow new work          | Yes ✅                     |
    
    And Santiago should congratulate:
      """
      ✅ ITEM COMPLETED: BI-020
      
      Great work! You finished "Personal Log Feature".
      
      Flow Impact:
      - in-progress WIP: 3 → 2 (capacity freed!)
      - You can now pull new work
      
      Next highest priority item:
      - BI-023: Stuck Notification System (priority: 0.82)
      
      Want to pull BI-023?
      """

  # ============================================================================
  # SCENARIO 7: Dependency Management
  # ============================================================================
  
  @dependencies @blocking
  Scenario: Automatically deprioritize blocked items
    Given backlog contains items with dependencies:
      | id     | title                    | blocks    | blocked_by | priority_score |
      | BI-030 | Kanban Ontology          | [BI-031]  | []         | 0.75           |
      | BI-031 | WIP Limit Tracking       | []        | [BI-030]   | 0.80           |
      | BI-032 | Personal Log Template    | []        | []         | 0.70           |
    
    When Santiago prioritizes backlog
    
    Then Santiago should analyze dependency chain:
      """
      Dependency Graph:
      
      BI-030 (Kanban Ontology)
        ↓ blocks
      BI-031 (WIP Limit Tracking)
      
      BI-032 (Personal Log Template) [independent]
      """
    
    And Santiago should adjust priorities:
      | original_rank | id     | original_score | adjusted_score | reasoning                       |
      | 1             | BI-031 | 0.80           | 0.40           | Blocked by BI-030 (50% penalty) |
      | 2             | BI-030 | 0.75           | 0.83           | Unblocks BI-031 (+10% bonus)    |
      | 3             | BI-032 | 0.70           | 0.70           | No dependencies (no change)     |
    
    And the re-ranked backlog should be:
      | rank | id     | adjusted_score | status      | reasoning                          |
      | 1    | BI-030 | 0.83           | ready       | Boosted: unblocks downstream work  |
      | 2    | BI-032 | 0.70           | ready       | Independent: can start immediately |
      | 3    | BI-031 | 0.40           | blocked     | Deprioritized: waiting for BI-030  |
    
    And BI-031 should be marked as blocked:
      """yaml
      ---
      id: BI-031
      title: "WIP Limit Tracking"
      status: blocked  # Changed from "ready"
      blocked_by: [BI-030]
      priority_score: 0.40  # Reduced from 0.80
      ---
      
      ⚠️ BLOCKED
      This item cannot be started until BI-030 (Kanban Ontology) is complete.
      
      Rationale:
      WIP limit tracking requires ontology classes from BI-030.
      Starting this work now would create technical debt.
      
      Watch: BI-030 (will auto-unblock when complete)
      """
    
    And when BI-030 completes:
      | action                      | outcome                             |
      | BI-030 status → done        | Completed successfully              |
      | BI-031 unblocked            | blocked_by: [BI-030] → []           |
      | BI-031 status → ready       | Now available for work              |
      | BI-031 score restored       | 0.40 → 0.80 (original score)        |
      | BI-031 rank updated         | Re-prioritized to rank 1 (highest!) |
    
    And Santiago should notify workers:
      """
      🔓 ITEM UNBLOCKED: BI-031
      
      "WIP Limit Tracking" is now ready for work!
      
      Blocker Resolved:
      - BI-030 (Kanban Ontology) completed
      - All dependencies satisfied
      
      Priority: 0.80 (HIGH)
      Rank: 1 (top of backlog)
      
      Recommendation: Pull this item next
      """

  # ============================================================================
  # SCENARIO 8: Throughput & Velocity Forecasting
  # ============================================================================
  
  @forecasting @velocity
  Scenario: Forecast completion dates based on historical throughput
    Given Santiago has completed work over the last 4 weeks:
      | week | items_completed | story_points |
      | 1    | 8               | 21           |
      | 2    | 7               | 18           |
      | 3    | 9               | 23           |
      | 4    | 6               | 16           |
    And current backlog has:
      | status   | item_count | total_story_points |
      | proposed | 12         | 48                 |
      | ready    | 8          | 24                 |
      | in-progress | 3       | 9                  |
    
    When Santiago calculates throughput and forecasts completion
    
    Then average throughput should be:
      """
      Average Throughput (Items):
      = (8 + 7 + 9 + 6) / 4
      = 30 / 4
      = 7.5 items per week
      
      Average Throughput (Story Points):
      = (21 + 18 + 23 + 16) / 4
      = 78 / 4
      = 19.5 story points per week
      """
    
    And velocity trend should be:
      """
      Velocity Trend Analysis:
      Week 1: 21 pts
      Week 2: 18 pts (-14% ↓)
      Week 3: 23 pts (+28% ↑)
      Week 4: 16 pts (-30% ↓)
      
      Observations:
      - High variability (16-23 pts range)
      - Slight downward trend in recent weeks
      - Average: 19.5 pts/week
      
      Possible Causes:
      - Week 3 spike: Easy items or extra capacity?
      - Week 4 dip: Complex items or interruptions?
      - Need more data for reliable trend
      """
    
    And completion forecast should be:
      """
      Backlog Completion Forecast:
      
      Total Remaining Work:
      - proposed: 48 story points
      - ready: 24 story points
      - in-progress: 9 story points
      - TOTAL: 81 story points
      
      Average Throughput: 19.5 story points/week
      
      Optimistic Forecast (Week 3 pace: 23 pts/week):
      = 81 pts / 23 pts/week
      = 3.5 weeks
      = Completion by: 2025-12-15
      
      Realistic Forecast (Average pace: 19.5 pts/week):
      = 81 pts / 19.5 pts/week
      = 4.15 weeks
      = Completion by: 2025-12-22
      
      Pessimistic Forecast (Week 4 pace: 16 pts/week):
      = 81 pts / 16 pts/week
      = 5.06 weeks
      = Completion by: 2025-12-29
      
      Recommended Communication:
      "Current backlog will take 4-5 weeks to complete at our current pace.
      We can improve this by:
      1. Reducing WIP (focus on fewer items)
      2. Removing low-priority items (trim backlog)
      3. Adding capacity (more workers or hours)
      
      Which approach do you prefer?"
      """
    
    And Santiago should track forecast accuracy:
      """
      Forecast Accuracy Tracking:
      
      Previous Forecast (4 weeks ago):
      - Predicted: 60 story points in 3 weeks
      - Actual: 57 story points in 3 weeks
      - Accuracy: 95% ✅
      
      This validates our forecasting model!
      Continue using average throughput for estimates.
      """

  # ============================================================================
  # SCENARIO 9: Integration with Existing Systems
  # ============================================================================
  
  @integration @status-tackle
  Scenario: Backlog integrates with status tackle system
    Given Santiago PM uses status tackle for workflow tracking
    And status tackle recognizes these states:
      | status        | meaning                |
      | proposed      | Not yet refined        |
      | ready         | Refined, ready to pull |
      | in-progress   | Worker actively working|
      | review        | Awaiting approval      |
      | done          | Completed and shipped  |
      | cancelled     | No longer needed       |
    And backlog management needs Kanban stages:
      | stage         | description            |
      | backlog       | Unrefined proposals    |
      | ready         | Ready to pull          |
      | in-progress   | Active work            |
      | review        | Under review           |
      | done          | Completed              |
    
    When Santiago maps backlog to status tackle
    
    Then the mapping should be:
      | backlog_stage | status_field | notes                              |
      | backlog       | proposed     | Items awaiting refinement          |
      | ready         | ready        | Three Amigos complete              |
      | in-progress   | in-progress  | Worker assigned and working        |
      | review        | review       | Work complete, awaiting approval   |
      | done          | done         | Accepted and shipped               |
    
    And backlog items should use existing YAML frontmatter:
      """yaml
      ---
      artifact_type: backlog-item
      status: ready  # Uses status tackle field!
      priority_score: 0.85
      assigned_to: [Santiago-PM]
      ---
      """
    
    And Santiago should leverage existing status queries:
      ```python
      # Query backlog using existing status system
      ready_items = kg_store.query("""
        SELECT ?item WHERE {
          ?item nusy:artifactType "backlog-item" .
          ?item nusy:status "ready" .
        }
        ORDER BY ?priority_score DESC
      """)
      ```
    
    And flow transitions should update status automatically:
      | action                | status_change       | triggers                     |
      | Create backlog item   | → proposed          | Three Amigos session queued  |
      | Refine item           | proposed → ready    | Available for pull           |
      | Pull work             | ready → in-progress | Worker assigned, timer starts|
      | Complete work         | in-progress → review| Reviewer notified            |
      | Accept work           | review → done       | Cycle time calculated        |

  # ============================================================================
  # SCENARIO 10: Neurosymbolic Learning Over Time
  # ============================================================================
  
  @neurosymbolic @learning
  Scenario: Santiago learns better prioritization from outcomes
    Given Santiago has prioritized 50 backlog items over 2 months
    And Santiago tracks actual vs predicted outcomes:
      | item_id | predicted_value | actual_value | predicted_effort | actual_effort |
      | BI-001  | 0.9             | 0.95         | 3                | 2             |
      | BI-002  | 0.8             | 0.6          | 5                | 8             |
      | BI-003  | 0.7             | 0.85         | 2                | 2             |
    
    When Santiago analyzes prediction accuracy
    
    Then Santiago should calculate error metrics:
      """
      Value Prediction Error:
      - BI-001: |0.9 - 0.95| = 0.05 (5% error)
      - BI-002: |0.8 - 0.6| = 0.2 (20% error) ⚠️
      - BI-003: |0.7 - 0.85| = 0.15 (15% error)
      
      Average Error: (0.05 + 0.2 + 0.15) / 3 = 13.3%
      
      Effort Prediction Error:
      - BI-001: |3 - 2| / 3 = 33% overestimate
      - BI-002: |5 - 8| / 5 = 60% underestimate ⚠️
      - BI-003: |2 - 2| / 2 = 0% (perfect!)
      
      Average Error: (33% + 60% + 0%) / 3 = 31%
      """
    
    And Santiago should identify patterns:
      """
      LEARNING INSIGHTS
      
      Pattern 1: Integration items often underestimated
      - BI-002 was integration work (8 pts vs 5 predicted)
      - Hypothesis: Dependencies add hidden complexity
      - Adjustment: Multiply integration effort estimates by 1.5x
      
      Pattern 2: Template/documentation items overestimated
      - BI-001 was template work (2 pts vs 3 predicted)
      - Hypothesis: We're getting faster at these
      - Adjustment: Multiply template effort estimates by 0.7x
      
      Pattern 3: Value predictions generally accurate
      - Average error: 13.3% (good!)
      - Hypothesis: User feedback is reliable
      - Adjustment: Continue using hypothesis confidence as proxy
      """
    
    And Santiago should update prioritization weights:
      """
      Weight Adjustment Based on Learning:
      
      BEFORE (initial weights):
      - customer_value: 0.4
      - unblock_impact: 0.3
      - worker_availability: 0.2
      - learning_value: 0.1
      
      AFTER (learned weights):
      - customer_value: 0.35 (reduce slightly, not perfect predictor)
      - unblock_impact: 0.35 (increase, high-impact in practice)
      - worker_availability: 0.20 (keep same, good predictor)
      - learning_value: 0.10 (keep same, good predictor)
      
      Rationale:
      Items that unblock others had higher actual value than predicted.
      Boost unblock_impact weight to 0.35 (equal to customer_value).
      """
    
    And Santiago should apply learned patterns to new items:
      """
      NEW ITEM: BI-050 (Integration with External API)
      
      Initial Estimate: 5 story points
      
      Learned Adjustment:
      - Item type: Integration
      - Adjustment factor: 1.5x (from Pattern 1)
      - Adjusted estimate: 5 * 1.5 = 7.5 ≈ 8 story points
      
      Explanation to team:
      "I've adjusted this estimate up based on past integration work.
      We tend to underestimate integration complexity by 50%.
      Let's start with 8 points and adjust if needed."
      """
