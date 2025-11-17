---
id: hybrid-coordination-001
type: experiment
status: in_progress
state_reason: null
created_at: 2025-11-16T00:00:00Z
updated_at: 2025-11-16T00:00:00Z
assignees: ["copilot", "github-agents"]
labels: ["type:experiment", "methodology:hybrid-coordination", "phase:discovery"]
hypothesis: "Hybrid human-AI coordination (long-context Copilot + GitHub Agents) will be faster and higher quality than serial work"
success_criteria:
  - Time to complete architecture + implementation < 2 hours
  - BDD test pass rate ≥ 95%
  - GitHub Agent PR quality acceptable (minimal rework needed)
  - Context preservation across agent handoffs successful
metrics:
  - total_time_minutes: TBD
  - architecture_time_minutes: TBD
  - implementation_time_minutes: TBD
  - pr_count: TBD
  - pr_review_cycles: TBD
  - bdd_pass_rate: TBD
  - rework_percentage: TBD
signals:
  - coordination_overhead_low: "GitHub issue creation + PR review < 20% of total time"
  - quality_maintained: "PR changes align with architecture, no major refactors needed"
  - context_preserved: "Agents understand specs without back-and-forth clarification"
related_artifacts:
  - ../cargo-manifests/passage-system.feature
  - ../../knowledge/catches/santiago-pm-behaviors/passage-behaviors-extracted.md
  - ../../knowledge/ontologies/pm-domain-ontology.ttl
  - ../../knowledge/catches/santiago-pm-behaviors/santiago-pm-mcp-manifest.json
---

# Hybrid Coordination Mini Expedition

## Hypothesis

**Question**: Can we accelerate Santiago development by coordinating multiple AI agents (long-context Copilot + GitHub Agents) instead of serial work?

**Hypothesis**: Hybrid human-AI coordination will deliver faster time-to-value and maintain quality through:
1. Copilot (long context) handles architecture requiring deep understanding
2. GitHub Agents (parallel) handle well-specified implementation tasks
3. Copilot reviews PRs with full architectural context

## Experimental Design

### Phase 1: Architecture Foundation (Copilot) ⏱️ START: 2025-11-16T[TBD]

**Tasks**:
- [x] Extend pm-domain-ontology.ttl with Layer 7: Passage orchestration (4 classes, 13 properties, 8 behaviors)
- [x] Update santiago-pm-mcp-manifest.json from 20 → 28 tools (add 8 passage behaviors with full JSON schemas)
- [ ] Create Fishnet architecture specification (multi-strategy BDD generation design)
- [ ] Create Navigator architecture specification (10-step orchestration design)
- [ ] Write GitHub issues for agents with clear acceptance criteria

**Why Copilot**: Requires understanding of:
- Existing ontology structure (6 layers, 882 lines)
- MCP manifest patterns (20 existing tools)
- Bootstrap capability implications
- Integration with existing behaviors

**Deliverables**:
- Extended ontology (v1.1.0)
- Extended manifest (28 tools)
- Architecture specs for agents
- 3 GitHub issues (BDD generation, Fishnet impl, Navigator impl)

**Time Budget**: 30-45 minutes

---

### Phase 2: Parallel Implementation (GitHub Agents) ⏱️ START: [TBD]

**Agent 1: BDD Test Generation**
- Issue: "Generate 84 BDD .feature files for 28 PM behaviors"
- Input: pm-behaviors-extracted.md + passage-behaviors-extracted.md
- Output: 84 .feature files (3 scenarios per behavior)
- Acceptance: Valid Gherkin syntax, references KG nodes, covers happy/edge/error paths

**Agent 2: Fishnet Implementation**
- Issue: "Implement multi-strategy BDD generation in Fishnet"
- Input: Fishnet architecture spec + fishnet-bdd-generation-strategies.feature
- Output: Enhanced fishnet.py with 5 strategies
- Acceptance: All strategies implemented, unit tests pass, CLI works

**Agent 3: Navigator Implementation**
- Issue: "Implement Navigator 10-step orchestration engine"
- Input: Navigator architecture spec + navigator.py skeleton
- Output: Complete navigator.py with validation loops
- Acceptance: All 10 steps orchestrated, quality gates enforced, provenance logged

**Why GitHub Agents**: Tasks are:
- Well-specified (clear inputs/outputs/acceptance)
- Parallelizable (no dependencies between agents)
- Repetitive (BDD file generation follows template)
- Implementation-focused (less architectural judgment needed)

**Time Budget**: Agents work in parallel, ~1-2 hours wall time

---

### Phase 3: Review & Integration (Copilot) ⏱️ START: [TBD]

**Tasks**:
- [ ] Review Agent 1 PR (BDD files) - check quality, coverage, Gherkin syntax
- [ ] Review Agent 2 PR (Fishnet) - verify architecture alignment, test coverage
- [ ] Review Agent 3 PR (Navigator) - verify orchestration logic, quality gates
- [ ] Merge PRs and resolve conflicts (if any)
- [ ] Run integration tests (Task 12: Navigator expedition)
- [ ] Measure expedition metrics

**Why Copilot**: Requires:
- Full context on architectural decisions
- Understanding of integration points
- Judgment on code quality vs speed tradeoffs
- Ability to identify subtle issues agents might miss

**Time Budget**: 15-30 minutes per PR = 45-90 minutes total

---

## Baseline Comparison

**Serial Work (Copilot only)**:
- Ontology extension: 15 min ✅ (DONE)
- Manifest update: 15 min ✅ (DONE)
- Fishnet architecture: 20 min (ESTIMATED)
- Fishnet implementation: 60 min (ESTIMATED)
- Navigator architecture: 20 min (ESTIMATED)
- Navigator implementation: 90 min (ESTIMATED)
- BDD file generation: 45 min (ESTIMATED)
- **Total: ~265 minutes (4.4 hours)**

**Hybrid Work (Copilot + 3 Agents)**:
- Phase 1 (Architecture): 30-45 min
- Phase 2 (Parallel Impl): 60-120 min wall time (agents work simultaneously)
- Phase 3 (Review): 45-90 min
- **Total: 135-255 minutes (2.3-4.3 hours)** + coordination overhead

**Hypothesis**: Hybrid saves 10-30% time through parallelization, even with coordination overhead.

---

## Metrics Collection

### Time Metrics
- `architecture_time_minutes`: Phase 1 duration ✅ START: [TBD]
- `agent_1_time_minutes`: BDD generation duration
- `agent_2_time_minutes`: Fishnet implementation duration
- `agent_3_time_minutes`: Navigator implementation duration
- `review_time_minutes`: Phase 3 duration
- `total_wall_time_minutes`: Start of Phase 1 → End of Phase 3
- `coordination_overhead_minutes`: Issue creation + PR review + conflict resolution

### Quality Metrics
- `ontology_valid`: Boolean (passes ttl validation)
- `manifest_valid`: Boolean (passes JSON schema validation)
- `bdd_files_generated`: Integer (expected 84)
- `bdd_syntax_errors`: Integer (should be 0)
- `fishnet_tests_pass`: Boolean
- `navigator_tests_pass`: Boolean
- `integration_tests_pass`: Boolean (Task 12 expedition)
- `pr_review_cycles`: Integer per PR (1 = accepted immediately, 2+ = changes requested)

### Coordination Metrics
- `github_issues_created`: Integer (expected 3)
- `pr_conflicts`: Integer (merge conflicts between agent PRs)
- `architecture_clarifications`: Integer (agents asking for spec clarification)
- `context_loss_incidents`: Integer (agents misunderstanding requirements)

---

## Success Criteria

**Time Efficiency**:
- ✅ Total time < 4 hours (serial baseline)
- ✅ Coordination overhead < 20% of total time
- ✅ Architecture phase complete in < 45 minutes

**Quality Maintained**:
- ✅ BDD pass rate ≥ 95% on first run
- ✅ All unit tests pass
- ✅ Integration test (Task 12) passes
- ✅ PR review cycles ≤ 2 per agent (minimal rework)

**Coordination Effectiveness**:
- ✅ Agents work in parallel (no blocking dependencies)
- ✅ Architecture specs clear enough (< 2 clarifications per agent)
- ✅ PR conflicts minimal (< 3 conflicts total)

**Learning Outcomes**:
- Document what worked / didn't work
- Identify optimal task types for each agent type
- Refine architecture spec templates
- Improve GitHub issue templates

---

## Risk Assessment

### Risk 1: Agent Context Loss
**Probability**: Medium  
**Impact**: High (requires rework)  
**Mitigation**: Write extremely detailed GitHub issues with examples, input/output schemas, acceptance criteria

### Risk 2: Integration Conflicts
**Probability**: Medium  
**Impact**: Medium (time spent resolving)  
**Mitigation**: Clear module boundaries in architecture specs, agents work on different files

### Risk 3: Quality Degradation
**Probability**: Low  
**Impact**: High (defeats purpose of expedition)  
**Mitigation**: Strict PR review, BDD tests validate correctness, roll back if quality issues found

### Risk 4: Coordination Overhead
**Probability**: High  
**Impact**: Medium (negates time savings)  
**Mitigation**: Template GitHub issues, automate PR checks, batch review instead of real-time

---

## Results

### Phase 1: Architecture Foundation (Copilot)

**Started**: 2025-11-16T[TBD]  
**Completed**: 2025-11-16T[TBD]  
**Duration**: [TBD] minutes

**Deliverables**:
- [x] pm-domain-ontology.ttl v1.1.0 (Layer 7: Orchestration added)
  - 4 new classes: Passage, PassageExecution, PassageStep, PassageActor
  - 13 new properties: hasCategory, hasTrigger, hasStep, executionState, etc.
  - 8 new PMBehavior classes
- [x] santiago-pm-mcp-manifest.json v1.1.0 (28 tools)
  - Added passage_orchestration category
  - 8 passage tools with full JSON schemas
  - Updated metadata (completeness 0.90, recursive self-improvement note)
- [ ] Fishnet architecture spec (IN PROGRESS)
- [ ] Navigator architecture spec (IN PROGRESS)
- [ ] 3 GitHub issues created (PENDING)

**Quality**:
- Ontology valid: [TBD]
- Manifest valid: [TBD]
- Architecture specs clear: [TBD]

**Observations**:
- [TBD - Copilot will fill this in after Phase 1]

---

### Phase 2: Parallel Implementation (GitHub Agents)

**Agent 1 (BDD Generation)**:
- Started: [TBD]
- Completed: [TBD]
- PR: #[TBD]
- Files generated: [TBD] / 84
- Syntax errors: [TBD]
- Review cycles: [TBD]

**Agent 2 (Fishnet)**:
- Started: [TBD]
- Completed: [TBD]
- PR: #[TBD]
- Tests passing: [TBD]
- Review cycles: [TBD]

**Agent 3 (Navigator)**:
- Started: [TBD]
- Completed: [TBD]
- PR: #[TBD]
- Tests passing: [TBD]
- Review cycles: [TBD]

**Coordination Issues**:
- Context loss incidents: [TBD]
- Clarifications needed: [TBD]
- PR conflicts: [TBD]

---

### Phase 3: Review & Integration (Copilot)

**Started**: [TBD]  
**Completed**: [TBD]  
**Duration**: [TBD] minutes

**PR Reviews**:
- Agent 1 review: [TBD] minutes, [TBD] changes requested
- Agent 2 review: [TBD] minutes, [TBD] changes requested
- Agent 3 review: [TBD] minutes, [TBD] changes requested

**Integration**:
- Merge conflicts: [TBD]
- Integration tests: [TBD] pass / [TBD] fail
- Task 12 (Navigator expedition): [TBD]

**Final Metrics**:
- Total wall time: [TBD] minutes
- Coordination overhead: [TBD] minutes ([TBD]%)
- BDD pass rate: [TBD]
- Quality maintained: [TBD]

---

## Analysis

### What Worked
- [TBD - Fill in after completion]

### What Didn't Work
- [TBD - Fill in after completion]

### Lessons Learned
- [TBD - Fill in after completion]

### Recommendations for Future Expeditions
- [TBD - Fill in after completion]

---

## Conclusion

**Hypothesis Validated**: [YES / NO / PARTIAL]

**Key Findings**:
- [TBD]

**Next Steps**:
- [TBD]

**Expedition Status**: 🚧 IN PROGRESS
