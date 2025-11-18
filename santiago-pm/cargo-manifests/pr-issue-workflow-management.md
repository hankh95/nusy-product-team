# Feature: PR/Issue Workflow Management System

```yaml
---
artifact_type: cargo-manifest
feature_id: F-030
feature_name: pr-issue-workflow-management
priority: 0.85 (HIGH)
status: implemented
created: 2025-11-17
created_by: Hank
started: 2025-11-17
completed: 2025-11-17
branch: feature/f-030-pr-workflow-management
implementation_commit: b1ba04e
source: Discussion about agent work completion and PM/architect review workflow
related_features:
  - F-027 (Personal Log Feature - tracks agent work sessions)
  - F-029 (Continuous Backlog Discovery - discovers new work items)
  - F-026 (Lean-Kanban Backlog Management - prioritizes work)
kerievsky_principles:
  - "Deliver Value Continuously" (smooth flow from code to production)
  - "Experiment & Learn Rapidly" (quick feedback loops)
  - "Make Work Visible" (clear status throughout workflow)
---
```

---

## Feature Overview

**Problem**: When AI coding agents complete work, there's no standardized workflow for:
- Agent signaling work completion
- PM/Architect reviewing pull requests
- Approving and merging PRs
- Automatically updating linked issues with review outcomes
- Closing issues when work is validated and merged

**Human Pattern** (Traditional):
- Agent creates PR manually
- PM gets notification (email/Slack)
- PM reviews when available (delays)
- Manual approval and merge
- Manual issue update/closure
- Status scattered across tools

**Santiago-PM Pattern** (Automated):
- Agent completes work → auto-creates PR with provenance
- Santiago-PM detects new PR → notifies PM
- PM reviews → approves/requests changes
- On approval → Santiago-PM auto-merges
- On merge → Santiago-PM updates issue with review summary
- On merge → Santiago-PM auto-closes issue with completion notes

**Key Insight**: The workflow from code completion to issue closure should be automated with human approval gates at critical points (review, merge decision).

**Lean Hypothesis**:
We believe that **Santiago-PM should expose workflow management as a native MCP capability** because:
1. **Lower Latency**: When multiple Santiago agents collaborate at high velocity, external system latency (GitHub API calls, webhooks) becomes a bottleneck
2. **Better Reliability**: External dependencies (GitHub downtime, rate limits) create brittle failure modes
3. **Richer Context**: Native MCP tools can access full Santiago context (KG, personal logs, cargo manifests) without round-trips
4. **Team Effectiveness**: A unified workflow surface is more effective than context-switching between Santiago tools and GitHub

**We will know this is true when**:
- Multi-agent workflows complete 10x faster with native tools vs GitHub-dependent flows
- Workflow reliability reaches 99.9% vs <95% with external dependencies
- Agent coordination overhead drops by 80% (measured in API calls, wait times)
- Team reports higher satisfaction with unified vs fragmented tooling

**Test Plan**:
Build parallel implementations:
- **Path A (External)**: Use GitHub API for all workflow operations (baseline)
- **Path B (Native)**: Use Santiago-PM MCP tools for workflow operations
- **Metrics**: Measure latency, reliability, API calls, agent coordination time
- **Success Criteria**: Path B shows ≥5x improvement in latency and ≥2x improvement in reliability

**Value Proposition**:
- **Faster feedback loops**: Agents know immediately when work is approved
- **Better traceability**: Every issue has full PR review history
- **Reduced manual overhead**: No manual issue updates or closures
- **Clear work states**: Always know status of in-flight work
- **Learning data**: Track review patterns, approval times, rejection reasons
- **High-velocity collaboration**: Native tools support rapid multi-agent coordination
- **Resilience**: No external dependencies in critical workflow paths

---

## User Stories

### Story 1: Agent Work Completion Workflow (MVP)

**As an AI Coding Agent (Copilot)**
**I want to signal work completion and create a PR automatically**
**So that my work can be reviewed without manual intervention**

**Given** I have completed implementation of an assigned issue:
```yaml
work_completed:
  issue_id: "#6"
  issue_title: "Implement Fishnet v2.0.0 multi-strategy BDD generation"
  branch: "copilot/implement-fishnet-v2"
  commits:
    - "666595b: Implement Fishnet v2.0.0 multi-strategy BDD generation"
    - "9970339: Add BottomUpStrategy and CLI interface"
  tests_passing: true
  session_log_saved: true  # F-027 integration
  acceptance_criteria_met:
    - "base_strategy.py with abstract base class + data classes": true
    - "bottom_up_strategy.py fully implemented": true
    - "fishnet.py orchestrator generates 84 files": true
    - "CLI works with all arguments": true
    - "Unit tests pass": true
```

**When** I complete my work session

**Then** the system should:
1. Save session context (F-027):
   ```bash
   python save-chat-log.py --paste --with-summary --topic "fishnet-implementation"
   ```
   - Raw transcript saved to `santiago-pm/personal-logs/agents/raw-transcripts/`
   - Summary log created with metadata extraction
   - Both linked for full provenance

2. Create a PR automatically with:
   - Title: "Closes #6: Implement Fishnet v2.0.0 multi-strategy BDD generation"
   - Body: Generated from work session log (includes link to session context)
   - Labels: `autonomous`, `santiago`, `enhancement`
   - Reviewers: Assigned PM (hankh95)
   - Linked issue: #6
   - Session log reference for reviewer context

3. Add PR link to issue #6 as comment
4. Update issue status to "in-review"
5. Notify PM via GitHub notification

**Acceptance Criteria**:
- [ ] Agent can trigger PR creation via CLI command or API
- [ ] Session context saved before PR creation (F-027 integration)
- [ ] PR body includes: work summary, session log link, acceptance criteria checklist, test results, commits
- [ ] PR automatically links to issue using "Closes #N" keyword
- [ ] Issue gets comment with PR link
- [ ] PM receives notification with full context

---

### Story 2: PM/Architect Review Workflow

**As a Product Manager or Architect**
**I want a structured review process for agent-created PRs**
**So that I can efficiently validate work quality and provide feedback**

**Given** an agent has created PR #17 for issue #6:
```yaml
pr_details:
  number: 17
  title: "Closes #6: Implement Fishnet v2.0.0 multi-strategy BDD generation"
  author: "copilot-swe-agent"
  status: "open"
  reviewers: ["hankh95"]
  linked_issue: 6
  files_changed: 12
  tests_status: "passing"
```

**When** I open the PR for review

**Then** I should see:
1. **PR Summary Section**:
   - Linked issue with original requirements
   - Work completion summary from agent session
   - Acceptance criteria checklist (all marked as complete)
   - Test results (unit tests, integration tests, BDD scenarios)
   
2. **Review Checklist** (auto-generated):
   ```markdown
   ## Review Checklist
   - [ ] Code quality meets project standards
   - [ ] All acceptance criteria are met
   - [ ] Tests are comprehensive and passing
   - [ ] Documentation is updated
   - [ ] No breaking changes without migration plan
   - [ ] Architecture follows project patterns
   - [ ] Security concerns addressed
   ```

3. **Review Actions**:
   - **Approve**: Mark all checklist items as passed, approve PR
   - **Request Changes**: Add comments, mark specific checklist items as failed
   - **Reject**: Close PR with reason, update issue with rejection notes

**Acceptance Criteria**:
- [ ] PR template includes all review sections
- [ ] Review checklist is auto-generated from project standards
- [ ] PM can approve/request changes via GitHub UI
- [ ] Comments are linked to specific code sections when possible

---

### Story 3: Auto-Merge and Issue Update on Approval

**As Santiago-PM**
**I want to automatically merge approved PRs and update linked issues**
**So that work flows smoothly from approval to deployment**

**Given** PM has approved PR #17:
```yaml
pr_approval:
  pr_number: 17
  reviewer: "hankh95"
  approved_at: "2025-11-17T10:30:00Z"
  review_comment: "Excellent implementation. All acceptance criteria met. Code quality is high."
  checklist_status:
    - "Code quality meets project standards": true
    - "All acceptance criteria are met": true
    - "Tests are comprehensive and passing": true
    - "Documentation is updated": true
    - "No breaking changes": true
    - "Architecture follows patterns": true
    - "Security concerns addressed": true
```

**When** the approval is submitted

**Then** Santiago-PM should automatically:
1. **Merge PR**:
   - Merge strategy: Squash and merge (configurable)
   - Commit message: Preserve PR title and body
   - Delete branch after merge
   
2. **Update Linked Issue #6**:
   - Add comment with review summary:
     ```markdown
     ✅ **Work Approved and Merged**
     
     **PR**: #17
     **Reviewer**: @hankh95
     **Approved**: 2025-11-17 10:30 AM
     **Merged**: 2025-11-17 10:31 AM
     
     **Review Summary**:
     Excellent implementation. All acceptance criteria met. Code quality is high.
     
     **Checklist Results**:
     - ✅ Code quality meets project standards
     - ✅ All acceptance criteria are met
     - ✅ Tests are comprehensive and passing
     - ✅ Documentation is updated
     - ✅ No breaking changes
     - ✅ Architecture follows patterns
     - ✅ Security concerns addressed
     
     **Next Steps**:
     Issue closed automatically. Agent can proceed to next assigned work.
     ```
   - Close issue with label `approved-merged`
   
3. **Notify Agent**:
   - Add note to agent's personal log
   - Update agent's work queue (remove completed item)

**Acceptance Criteria**:
- [ ] Auto-merge triggers on PM approval
- [ ] Issue gets comprehensive update comment
- [ ] Issue closes automatically with appropriate label
- [ ] Agent receives completion notification
- [ ] Merge preserves full provenance chain

---

### Story 4: Request Changes Workflow

**As a Product Manager**
**I want to request changes when work doesn't meet standards**
**So that agents can iterate and improve their implementation**

**Given** PM reviews PR #18 for issue #7 and finds issues:
```yaml
review_findings:
  pr_number: 18
  linked_issue: 7
  reviewer: "hankh95"
  status: "changes_requested"
  review_comments:
    - file: "navigator.py"
      line: 125
      comment: "Validation loop should check quality gates after each cycle, not just at the end"
      severity: "blocker"
    - file: "navigator.py"
      line: 245
      comment: "Add error handling for failed Catchfish extraction"
      severity: "important"
    - general: "Documentation needs more detail on the 10-step process"
      severity: "minor"
```

**When** PM submits "Request Changes" review

**Then** Santiago-PM should:
1. **Update PR Status**:
   - Label: `changes-requested`
   - Status: Block merge until resolved
   
2. **Update Linked Issue #7**:
   - Add comment:
     ```markdown
     ⚠️ **Changes Requested on PR #18**
     
     **Reviewer**: @hankh95
     **Reviewed**: 2025-11-17 11:00 AM
     
     **Issues Found**:
     - 🔴 **Blocker**: Validation loop should check quality gates after each cycle, not just at the end (navigator.py:125)
     - 🟡 **Important**: Add error handling for failed Catchfish extraction (navigator.py:245)
     - 🟢 **Minor**: Documentation needs more detail on the 10-step process
     
     **Next Steps**:
     Agent will address comments and update PR. Issue remains open pending resolution.
     ```
   - Keep issue open with label `in-revision`
   
3. **Notify Agent**:
   - Create task list from review comments
   - Add to agent's work queue for next session
   - Include context: original issue, PR, review comments

**Acceptance Criteria**:
- [ ] "Request Changes" updates issue with clear action items
- [ ] Issue remains open with `in-revision` label
- [ ] Agent receives structured task list
- [ ] PR blocks merge until changes addressed
- [ ] Subsequent reviews follow same update pattern

---

### Story 5: Workflow State Tracking and Metrics

**As Santiago-PM**
**I want to track workflow states and measure cycle times**
**So that we can optimize the development process**

**Given** multiple issues and PRs in various workflow states:
```yaml
workflow_states:
  - issue: 6
    state: "closed"
    pr: 17
    created_at: "2025-11-17T05:10:26Z"
    pr_created_at: "2025-11-17T08:30:00Z"
    review_started_at: "2025-11-17T10:00:00Z"
    approved_at: "2025-11-17T10:30:00Z"
    merged_at: "2025-11-17T10:31:00Z"
    closed_at: "2025-11-17T10:31:00Z"
    
  - issue: 7
    state: "in-revision"
    pr: 18
    created_at: "2025-11-17T05:10:59Z"
    pr_created_at: "2025-11-17T09:00:00Z"
    review_started_at: "2025-11-17T11:00:00Z"
    changes_requested_at: "2025-11-17T11:15:00Z"
```

**When** analyzing workflow performance

**Then** Santiago-PM should calculate:
1. **Cycle Time Metrics**:
   - Issue creation → PR creation: 3.3 hours (issue #6)
   - PR creation → Review started: 1.5 hours (issue #6)
   - Review started → Approval: 0.5 hours (issue #6)
   - Approval → Merge/Close: 1 minute (issue #6)
   - **Total cycle time**: 5.3 hours (issue #6)

2. **Quality Metrics**:
   - First-time approval rate: 50% (1 of 2 PRs)
   - Average review iterations: 1.5
   - Blocker rate: 50% (1 of 2 PRs had blockers)

3. **Workflow Bottlenecks**:
   - Slowest stage: Issue → PR (3.3 hours average)
   - Review turnaround: 0.5 hours (excellent)
   - Changes resolution time: TBD (issue #7 still open)

**Acceptance Criteria**:
- [ ] Track workflow state transitions with timestamps
- [ ] Calculate cycle time metrics per issue
- [ ] Identify bottlenecks and optimization opportunities
- [ ] Export metrics to ships-logs for analysis
- [ ] Generate weekly workflow performance reports

---

## Technical Architecture

### Workflow State Machine

```
┌─────────────┐
│   Issue     │
│   Created   │
└─────────────┘
      │
      │ Agent assigns self
      ▼
┌─────────────┐
│   Issue     │
│ In Progress │
└─────────────┘
      │
      │ Agent completes work
      ▼
┌─────────────┐      ┌─────────────┐
│  PR Created │─────▶│   Issue     │
│             │      │  In Review  │
└─────────────┘      └─────────────┘
      │                     │
      │                     │ PM reviews
      ▼                     ▼
┌─────────────┐      ┌─────────────┐
│   Tests     │      │   Review    │
│  Running    │      │  Complete   │
└─────────────┘      └─────────────┘
      │                     │
      ├─────────┬───────────┤
      │         │           │
      ▼         ▼           ▼
┌─────────┐ ┌──────────┐ ┌──────────┐
│Approved │ │ Changes  │ │Rejected  │
│         │ │Requested │ │          │
└─────────┘ └──────────┘ └──────────┘
      │         │           │
      │         │           │ Update issue
      │         │           ▼
      │         │      ┌──────────┐
      │         │      │  Issue   │
      │         │      │ Closed   │
      │         │      │(Rejected)│
      │         │      └──────────┘
      │         │
      │         │ Agent addresses comments
      │         ▼
      │    ┌─────────────┐
      │    │   Issue     │
      │    │ In Revision │
      │    └─────────────┘
      │         │
      │         │ Updated PR
      │         ▼
      │    (back to "PR Created")
      │
      │ Auto-merge
      ▼
┌─────────────┐
│  PR Merged  │
└─────────────┘
      │
      │ Update issue + close
      ▼
┌─────────────┐
│   Issue     │
│   Closed    │
│ (Approved)  │
└─────────────┘
```

### Data Model

```python
@dataclass
class WorkflowState:
    """Tracks state of issue/PR workflow"""
    issue_id: str
    issue_title: str
    current_state: WorkflowStateEnum
    pr_number: Optional[int]
    assigned_agent: str
    assigned_reviewer: str
    
    # Timestamps
    created_at: datetime
    pr_created_at: Optional[datetime]
    review_started_at: Optional[datetime]
    review_completed_at: Optional[datetime]
    merged_at: Optional[datetime]
    closed_at: Optional[datetime]
    
    # Review data
    review_comments: List[ReviewComment]
    approval_status: Optional[bool]
    checklist_results: Dict[str, bool]
    
    # Metrics
    cycle_time_seconds: Optional[float]
    review_iterations: int
    
class WorkflowStateEnum(Enum):
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    CHANGES_REQUESTED = "changes_requested"
    IN_REVISION = "in_revision"
    APPROVED = "approved"
    MERGED = "merged"
    CLOSED_APPROVED = "closed_approved"
    CLOSED_REJECTED = "closed_rejected"
```

### GitHub Integration

```python
class GitHubWorkflowManager:
    """Manages PR/Issue workflow via GitHub API"""
    
    def create_pr_from_agent_work(
        self,
        issue_id: str,
        branch: str,
        work_summary: str,
        commits: List[str],
        tests_passing: bool
    ) -> int:
        """Create PR with agent work completion"""
        pass
    
    def add_pr_review_checklist(self, pr_number: int) -> None:
        """Add review checklist to PR body"""
        pass
    
    def on_pr_approved(self, pr_number: int) -> None:
        """Handle PR approval event"""
        # 1. Auto-merge PR
        # 2. Update linked issue
        # 3. Close issue
        # 4. Notify agent
        pass
    
    def on_changes_requested(self, pr_number: int, comments: List[ReviewComment]) -> None:
        """Handle changes requested event"""
        # 1. Update issue with comment list
        # 2. Create agent task list
        # 3. Notify agent
        pass
    
    def calculate_workflow_metrics(self, issue_id: str) -> WorkflowMetrics:
        """Calculate cycle time and quality metrics"""
        pass
```

---

## Implementation Phases

### Phase 1: Basic PR Creation and Issue Linking (MVP)
**Time Estimate**: 3-4 hours

**Deliverables**:
- [ ] CLI command for agent to create PR
- [ ] PR template with work summary and acceptance criteria
- [ ] Auto-link PR to issue using "Closes #N"
- [ ] Add PR comment to issue

**Success Criteria**:
- Agent can create PR with single command
- PR correctly links to issue
- Issue shows PR link in comments

### Phase 2: Review Workflow Automation
**Time Estimate**: 4-5 hours

**Deliverables**:
- [ ] GitHub webhook handler for PR events
- [ ] Auto-merge on approval
- [ ] Issue update with review summary
- [ ] Auto-close issue on merge

**Success Criteria**:
- Approval triggers auto-merge
- Issue updated with comprehensive review summary
- Issue closes automatically with correct label

### Phase 3: Changes Request Workflow
**Time Estimate**: 3-4 hours

**Deliverables**:
- [ ] Parse review comments into task list
- [ ] Update issue with structured change requests
- [ ] Notify agent with action items
- [ ] Track revision iterations

**Success Criteria**:
- "Request Changes" creates clear action items
- Issue remains open with correct state
- Agent receives structured task list

### Phase 4: Metrics and Reporting
**Time Estimate**: 3-4 hours

**Deliverables**:
- [ ] Workflow state tracking
- [ ] Cycle time calculation
- [ ] Quality metrics (approval rate, iterations)
- [ ] Weekly performance reports

**Success Criteria**:
- All workflow states tracked with timestamps
- Cycle time metrics calculated per issue
- Reports show bottlenecks and trends

---

## Integration Points

### With F-027 (Personal Log Feature)
- Agent work sessions logged to personal logs
- PR creation includes link to session log
- Review outcomes captured in agent's learning log

### With F-029 (Continuous Discovery)
- Closed issues analyzed for learning patterns
- Review feedback used to improve future work
- Rejection reasons feed into discovery process

### With F-026 (Prioritization)
- Cycle time metrics influence priority scores
- High-approval-rate agents get higher confidence
- Review patterns inform work allocation

### With GitHub
- GitHub API for PR/issue operations
- GitHub webhooks for event handling
- GitHub Actions for automation (optional)

---

## Success Metrics

### Workflow Efficiency
- **Target**: Average cycle time < 6 hours (issue → closed)
- **Baseline**: Unknown (needs measurement)
- **Measurement**: Track all workflow transitions

### Review Quality
- **Target**: First-time approval rate > 70%
- **Baseline**: Unknown (needs measurement)
- **Measurement**: Track approval vs changes requested

### Automation Rate
- **Target**: 90% of PRs auto-merged on approval
- **Baseline**: 0% (all manual)
- **Measurement**: Count auto vs manual merges

### Agent Learning
- **Target**: Decreasing revision iterations over time
- **Baseline**: Unknown (needs measurement)
- **Measurement**: Track review iterations per agent

---

## Risks and Mitigations

### Risk 1: Auto-merge breaks production
**Likelihood**: Medium
**Impact**: High
**Mitigation**: 
- Require passing tests before auto-merge
- Add manual override option
- Implement rollback mechanism
- Start with non-critical branches

### Risk 2: Review comments not actionable
**Likelihood**: Medium
**Impact**: Medium
**Mitigation**:
- Provide comment templates for reviewers
- Parse comments into structured tasks
- Request clarification if comments unclear

### Risk 3: GitHub API rate limits
**Likelihood**: Low
**Impact**: Medium
**Mitigation**:
- Cache API responses
- Batch operations when possible
- Monitor rate limit headers

---

## Questions for User Consultation

### Q1 (HIGH PRIORITY): Auto-merge strategy?
**Options**:
- A) Squash and merge (clean history, lose commit details)
- B) Merge commit (preserves full history, more commits)
- C) Rebase and merge (linear history, rewrites commits)

**Recommendation**: A (Squash and merge) - cleaner history, easier rollbacks

### Q2 (MEDIUM): Review approval threshold?
**Options**:
- A) Single approval required (PM or architect)
- B) Two approvals required (PM and architect)
- C) Configurable per issue/PR

**Recommendation**: A (Single approval) for MVP, C (Configurable) for Phase 2

### Q3 (MEDIUM): Failed test handling?
**Options**:
- A) Block PR creation if tests fail
- B) Create PR but block merge until tests pass
- C) Allow override with manual approval

**Recommendation**: B - create PR for visibility, block merge for safety

### Q4 (LOW): Issue closure timing?
**Options**:
- A) Close immediately on PR merge
- B) Wait 24 hours for smoke tests
- C) Manual verification before closure

**Recommendation**: A (Immediate closure) for MVP, agent learns from any issues

---

## Learning Opportunities

### For Agents
- What review comments are most common?
- Which acceptance criteria are hardest to meet?
- How does code quality correlate with approval rate?

### For Santiago-PM
- What are typical workflow bottlenecks?
- Which review patterns indicate quality work?
- How can we predict approval likelihood?

### For Team
- How effective is the TDD/BDD process?
- What documentation gaps cause confusion?
- Which standards need clarification?

---

## References

- **GitHub Docs**: [Linking PRs to Issues](https://docs.github.com/en/issues/tracking-your-work-with-issues/linking-a-pull-request-to-an-issue)
- **GitHub Docs**: [PR Reviews](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests)
- **CONTRIBUTING.md**: Section on "Closing Issues" and "Pull Request Process"
- **F-027**: Personal Log Feature for session tracking
- **F-029**: Continuous Discovery for learning from closed work
