# Cargo Manifest: Personal Log Feature

**Date**: 2025-11-17
**Type**: Feature
**Status**: ready
**Priority**: critical
**Domain**: pm-workflow
**Triggered By**: personal-log-discovery-questionnaire.md

---

## Feature Overview

Build a **personal log system** that preserves context across work sessions for both AI agents and humans. The primary goal is to solve the **context loss problem**—when switching between AI models or returning to work after breaks, team members lose understanding of what they were doing and waste time re-orienting.

**Key Innovation**: Dual-format logs (chat history for agents, journal for humans) with semantic linking to artifacts enables both context restoration AND team coordination/learning.

### The Context Loss Problem

**Pain Point** (from user questionnaire):
> "As I use Copilot with different models and switch between them, I lose track of what context each model has. Sometimes I have to re-explain things or remind the model of prior decisions, which wastes time and breaks my flow."

**Current Cost**:
- 15+ minutes per session re-explaining context
- Broken flow state
- Frustration and lost productivity
- Team coordination gaps (who's working on what?)

**MVP Solution**:
New agent reads previous chat history log and restores full context without re-explanation.

---

## User Stories

### Story 1: Context Restoration for AI Agents (MVP - CRITICAL)

```gherkin
Feature: Save and Restore Chat History for AI Agents
  As an AI agent, I want to save conversation history automatically
  so that the next agent can restore context without user re-explanation

  Background:
    Given Copilot conversation with user about personal log feature
    And conversation includes:
      | element          | example                                      |
      | Artifacts created| personal-logs/README.md, templates           |
      | Decisions made   | Hybrid structure, preserve chat format       |
      | Context          | Questionnaire analysis, MVP design           |
      | Next steps       | Create cargo manifest, implement tools       |

  Scenario: Automatic chat history preservation
    Given Copilot session ends after 4 hours of work
    When Santiago detects conversation completion
    Then Santiago should automatically:
      | action                    | result                                         |
      | Extract metadata          | Date, duration, model, conversation_id         |
      | Preserve chat format      | Original Copilot format (minimal transformation)|
      | Extract semantic links    | Artifacts mentioned/created/modified           |
      | Extract key decisions     | 4 decisions with rationale                     |
      | Identify next steps       | Clear continuation point                       |
      | Save to file              | agents/YYYY-MM-DD-{agent}-{topic}.md          |
    And file should be saved to: personal-logs/agents/
    And filename should be: 2025-11-17-copilot-claude-personal-log-mvp.md
    And YAML frontmatter should include all metadata

  Scenario: Context restoration for new agent (THE MVP GOAL!)
    Given user starts new Copilot session with different model
    And previous session was: 2025-11-17-copilot-claude-personal-log-mvp.md
    And user says: "Continue working on personal log feature"
    When new agent queries for recent personal logs
    Then new agent should:
      | step                        | result                                    |
      | Find most recent log        | 2025-11-17-copilot-claude-personal-log-mvp.md |
      | Load conversation context   | Full chat history from previous session   |
      | Extract key decisions       | Hybrid structure, preserve format, etc.   |
      | Identify current state      | Design complete, cargo manifest next      |
      | Understand next steps       | Create cargo manifest, get approval       |
      | Restore working context     | Ready to continue without re-explanation  |
    And new agent should respond:
      """
      I see we've completed the personal log feature design with:
      - Hybrid structure (personal-logs/ + captains-journals/)
      - Chat history preservation for agents
      - Journal format for humans
      - 9 MCP tools designed (3 MVP, 3 enhanced, 3 team)
      
      You wanted me to create the cargo manifest next. Ready to proceed?
      """
    And user should NOT need to re-explain anything
    And context restoration time should be < 30 seconds

  Scenario: Semantic linking to artifacts
    Given chat log contains mentions of artifacts:
      | artifact_type     | artifact_path                                |
      | questionnaire     | tackle/questionnaires/personal-log-discovery-questionnaire.md |
      | readme            | personal-logs/README.md                      |
      | template          | personal-logs/chat-history-template.md       |
      | cargo_manifest    | cargo-manifests/neurosymbolic-backlog-management.feature |
    When Santiago extracts semantic links from log
    Then log metadata should include:
      ```yaml
      worked_on:
        - santiago-pm/tackle/questionnaires/personal-log-discovery-questionnaire.md
      created:
        - santiago-pm/personal-logs/README.md
        - santiago-pm/personal-logs/chat-history-template.md
        - santiago-pm/personal-logs/personal-log-template.md
      mentioned:
        - santiago-pm/cargo-manifests/neurosymbolic-backlog-management.feature
      ```
    And Santiago KG should contain RDF triples:
      ```turtle
      <log:2025-11-17-copilot-claude> nusy:workedOn <artifact:personal-log-questionnaire> .
      <log:2025-11-17-copilot-claude> nusy:created <artifact:personal-logs-readme> .
      <log:2025-11-17-copilot-claude> nusy:mentioned <artifact:backlog-management-feature> .
      ```
```

### Story 2: Human Journal Entries

```gherkin
Feature: Structured Journal Entries for Humans
  As a human team member, I want to create personal log entries
  so that I can quickly re-orient when returning to tasks

  Scenario: Create human journal entry with template
    Given human has completed work session (2.5 hours)
    And human worked on: personal-log-discovery-questionnaire.md
    When human creates personal log entry using template
    Then template should provide:
      | section               | purpose                                    |
      | Metadata              | Date, duration, energy level, artifacts    |
      | Summary               | What was accomplished                      |
      | Decisions             | Key choices made with rationale            |
      | Blockers              | What's stuck or confusing                  |
      | Learning              | Insights and realizations                  |
      | Next Steps            | What to do next session                    |
      | Narrative             | Freeform journal-style reflection          |
    And human fills in structured metadata
    And human writes freeform narrative
    And Santiago extracts semantic links automatically
    And file saved as: humans/2025-11-17-hank-questionnaire-completion.md

  Scenario: Quick re-orientation from journal
    Given human completed work yesterday
    And yesterday's log: humans/2025-11-17-hank-questionnaire-completion.md
    And human returns to work today after break
    When human reads yesterday's personal log
    Then human should understand in < 2 minutes:
      | information          | example                                      |
      | What I was doing     | "Completing personal log questionnaire"      |
      | Where I left off     | "Provided all 10 responses"                  |
      | What to do next      | "Review Santiago's analysis and approve MVP" |
      | Key decisions made   | "Use hybrid structure, chat history format"  |
    And context restoration time should be < 2 minutes (target: 80% reduction)
    And human should feel: "I know exactly where to pick up"
```

### Story 3: Team Coordination

```gherkin
Feature: Team Coordination via Personal Logs
  As Santiago PM, I want to aggregate personal logs
  so that the team knows what everyone is working on

  Scenario: Generate daily standup summary
    Given personal logs from yesterday:
      | author        | summary                                      |
      | hank          | Completed questionnaire, provided insights   |
      | santiago-pm   | Analyzed responses, designed MVP             |
      | copilot-claude| Built templates and README documentation     |
    When Santiago generates team summary
    Then summary should show:
      """
      Daily Standup Summary (2025-11-17):
      
      Hank:
      - Completed personal log questionnaire ✅
      - Discovered 3 new feature ideas
      - Next: Review Santiago's analysis
      
      Santiago-PM:
      - Analyzed questionnaire responses ✅
      - Designed hybrid personal log structure
      - Created 9 MCP tools
      - Next: Build MVP tools
      
      Copilot-Claude:
      - Built comprehensive README ✅
      - Created 2 templates (agents, humans)
      - Documented 7 use cases
      - Next: Create cargo manifest
      
      Coordination Notes:
      - No duplicate work detected ✅
      - All team members progressing on related tasks ✅
      - Personal log feature ready for implementation
      """
    And team can see who's working on what
    And duplicate work is detected automatically
    And blockers are surfaced for help

  Scenario: Detect coordination issues
    Given two team members both working on "backlog prioritization"
    And neither aware of other's work
    When Santiago analyzes personal logs
    Then Santiago should detect:
      """
      ⚠️ POTENTIAL DUPLICATE WORK
      
      - Santiago-PM: Working on backlog prioritization (3 days)
      - Copilot-GPT4: Started backlog prioritization (yesterday)
      
      Recommendation: Coordinate to avoid duplication.
      Suggested action: Daily standup to sync on who owns what.
      """
    And Santiago should notify both workers
    And suggest coordination conversation
```

### Story 4: Search and Retrieval

```gherkin
Feature: Query Personal Logs for Context
  As a team member, I want to search historical logs
  so that I can find past decisions and context

  Scenario: Semantic search across logs
    Given 100 personal log entries over 3 months
    And logs contain decisions, artifacts, conversations
    When user queries: "Why did we choose hybrid structure?"
    Then Santiago should search:
      | search_type        | target                                       |
      | Semantic content   | Log narratives mentioning structure          |
      | Decision metadata  | key_decisions field for "hybrid structure"   |
      | Artifact links     | Logs linked to personal-logs/ folder         |
    And return results:
      """
      Found 3 relevant logs:
      
      1. 2025-11-17-copilot-claude-personal-log-mvp.md (Relevance: 0.95)
         Decision: "Use hybrid structure (Option C)"
         Rationale: "User responses indicated two distinct log types 
                    (agents vs humans) with different formats..."
      
      2. 2025-11-17-santiago-pm-questionnaire-analysis.md (Relevance: 0.87)
         Context: "Analyzed user questionnaire, found agents need chat 
                  history while humans need journal format..."
      
      3. 2025-11-17-hank-questionnaire-completion.md (Relevance: 0.72)
         Response: "As this is personal log, this can turn into chat 
                   history of agent and human journal..."
      """
    And user can click to read full logs
    And provenance chain is clear

  Scenario: Find when feature was worked on
    Given user asks: "When did we work on personal log feature?"
    When Santiago queries personal logs by artifact
    Then Santiago returns chronological list:
      | date       | log                                          | summary                  |
      | 2025-11-17 | copilot-claude-personal-log-mvp.md           | MVP design complete      |
      | 2025-11-18 | santiago-pm-personal-log-tools.md            | MCP tools implemented    |
      | 2025-11-19 | copilot-gpt4-personal-log-testing.md         | Testing and refinement   |
    And total time spent: 12 hours across 3 sessions
    And artifacts created: 10 files
```

---

## Acceptance Criteria

### AC1: Chat History Preservation (MVP - CRITICAL)

- [ ] **MCP tool**: `save_chat_history` saves conversation automatically
  - [ ] Extracts metadata (date, duration, model, conversation_id)
  - [ ] Preserves original Copilot chat format (minimal transformation)
  - [ ] Extracts semantic links (worked_on, created, modified, mentioned)
  - [ ] Extracts key decisions with rationale
  - [ ] Identifies next steps for continuation
  - [ ] Saves to `personal-logs/agents/YYYY-MM-DD-{agent}-{topic}.md`

- [ ] **MCP tool**: `restore_context_from_log` loads context for new agent
  - [ ] Finds most recent relevant log
  - [ ] Loads full conversation context
  - [ ] Extracts key decisions and state
  - [ ] Understands next steps
  - [ ] Returns structured context object
  - [ ] Context restoration time < 30 seconds

- [ ] **Validation**: New agent can continue work without re-explanation
  - [ ] User says "Continue working on X"
  - [ ] Agent responds with understanding of previous session
  - [ ] Agent proceeds without asking for recap
  - [ ] User satisfaction: "Agent has full context" ✅

### AC2: Human Journal Entries

- [ ] **Template**: `personal-log-template.md` with structured sections
  - [ ] Metadata (YAML frontmatter with 15+ fields)
  - [ ] Summary section (what accomplished)
  - [ ] Decisions section (key choices with rationale)
  - [ ] Blockers section (what's stuck)
  - [ ] Learning section (insights realized)
  - [ ] Next steps section (continuation point)
  - [ ] Narrative section (freeform journal)

- [ ] **MCP tool**: `create_human_log_entry` creates journal entry
  - [ ] Prompts for metadata (date, duration, summary)
  - [ ] Provides template structure
  - [ ] Allows freeform narrative
  - [ ] Auto-extracts semantic links from content
  - [ ] Saves to `personal-logs/humans/YYYY-MM-DD-{name}-{topic}.md`

- [ ] **Validation**: Human can re-orient in < 2 minutes
  - [ ] Human reads previous day's log
  - [ ] Human understands: what did, where left off, what next
  - [ ] Time to full context < 2 minutes (80% reduction from 10min baseline)

### AC3: Semantic Linking

- [ ] **Auto-extraction** of artifact references from log content
  - [ ] File paths mentioned in conversation → `mentioned` list
  - [ ] Files created during session → `created` list
  - [ ] Files modified during session → `modified` list
  - [ ] Features/issues discussed → `related_to` list

- [ ] **RDF triples** added to Santiago KG
  - [ ] `<log> nusy:workedOn <artifact>`
  - [ ] `<log> nusy:created <artifact>`
  - [ ] `<log> nusy:mentioned <artifact>`
  - [ ] `<log> nusy:decided <decision>`
  - [ ] Provenance chain: artifact → log → session → team member

- [ ] **Validation**: Can trace feature back to conversation that created it

### AC4: Team Coordination

- [ ] **MCP tool**: `generate_team_summary` aggregates daily logs
  - [ ] Collects logs from all team members
  - [ ] Extracts summaries, next steps, blockers
  - [ ] Formats as standup report
  - [ ] Identifies coordination issues (duplicate work)
  - [ ] Surfaces blockers needing help

- [ ] **MCP tool**: `detect_duplicate_work` identifies overlaps
  - [ ] Scans logs for similar work
  - [ ] Detects when multiple people work on same feature
  - [ ] Notifies team members
  - [ ] Suggests coordination conversation

- [ ] **Validation**: Team knows what everyone is working on

### AC5: Search and Retrieval

- [ ] **MCP tool**: `query_personal_logs` searches across logs
  - [ ] Semantic search on log content
  - [ ] Structured search on metadata (dates, tags, decisions)
  - [ ] Artifact-based search (find logs for feature X)
  - [ ] Returns results with relevance scores
  - [ ] Includes excerpts and context

- [ ] **Validation**: Can find past decisions and context in < 1 minute

### AC6: Integration with Existing Systems

- [ ] **Folder structure** created
  - [ ] `personal-logs/agents/`
  - [ ] `personal-logs/humans/`
  - [ ] `personal-logs/archive/`

- [ ] **Templates** created
  - [ ] `chat-history-template.md`
  - [ ] `personal-log-template.md`

- [ ] **README** with comprehensive documentation

- [ ] **Ontology extension** with PersonalLog classes
  - [ ] `nusy:PersonalLog` class
  - [ ] `nusy:SessionLog` class
  - [ ] `nusy:DecisionLog` class
  - [ ] Properties: workedOn, created, mentioned, decided, followsSession

---

## Technical Design

### Personal Log Schema (Chat History)

```yaml
---
artifact_type: personal-log
log_type: agent-chat-history
agent_name: [copilot-claude | copilot-gpt4 | santiago-pm]
session_date: YYYY-MM-DD
session_start: YYYY-MM-DDTHH:MM:SSZ
session_end: YYYY-MM-DDTHH:MM:SSZ
session_duration: [hours]
conversation_id: [unique ID]
model: [e.g., claude-sonnet-4.5]

# Context
context_summary: |
  What this conversation was about

# Work
summary: |
  What was accomplished

# Artifacts
worked_on: [list of artifact paths]
created: [new artifacts]
modified: [changed artifacts]
mentioned: [referenced artifacts]

# Decisions
key_decisions:
  - decision: ""
    rationale: ""
    alternatives_considered: []
    timestamp: ""
    confidence: [low | medium | high]

# State
blockers: []
questions: []
learning: []
next_steps: []

# Links
related_to: []
follows_session: null
continued_by: null

# Flags
importance: [low | medium | high | critical]
flagged_for: []
tags: []
---

[Conversation transcript in original Copilot format]
```

### Personal Log Schema (Human Journal)

```yaml
---
artifact_type: personal-log
log_type: human-journal
author: [name]
session_date: YYYY-MM-DD
session_start: HH:MM
session_end: HH:MM
session_duration: [hours]
energy_level: [low | medium | high]
focus_quality: [distracted | ok | focused]

# Context
context_summary: |
  What I was trying to accomplish

# Work
summary: |
  What I accomplished

# Artifacts
worked_on: []
created: []
modified: []
reviewed: []

# Decisions
key_decisions:
  - decision: ""
    rationale: ""
    alternatives_considered: []
    confidence: [low | medium | high]

# State
blockers: []
questions: []
learning: []
mood: ""

# Next
next_session: |
  What to do next time

# Links
related_to: []
follows_session: null

# Metadata
importance: [routine | notable | significant | critical]
tags: []
---

[Freeform journal narrative]
```

### MCP Tools

**Phase 1: MVP** (Week 1):
```python
# File: src/nusy_pm_core/adapters/pm_proxy.py

@mcp_tool
def save_chat_history(
    conversation_id: str,
    agent_name: str,
    format: str = "preserve_copilot_format",
    extract_metadata: bool = True,
    extract_semantic_links: bool = True
) -> str:
    """
    Save chat history to personal log (automatic for agents).
    
    Returns: Path to saved log file
    """
    pass

@mcp_tool
def restore_context_from_log(
    log_id: str,
    include_artifacts: bool = True,
    include_decisions: bool = True,
    include_state: bool = True
) -> dict:
    """
    Load context from previous log for new agent.
    
    Returns: Structured context object with:
    - conversation_context: Full chat history
    - key_decisions: List of decisions
    - current_state: Next steps, blockers, questions
    - artifacts: Referenced files
    """
    pass

@mcp_tool
def create_human_log_entry(
    date: str,
    summary: str,
    decisions: List[dict],
    artifacts_worked_on: List[str],
    next_steps: str,
    narrative: str = ""
) -> str:
    """
    Create personal log entry for humans.
    
    Returns: Path to saved log file
    """
    pass
```

**Phase 2: Enhanced** (Week 2):
- `query_personal_logs`: Semantic search
- `link_log_to_artifact`: Create relationships
- `generate_log_summary`: Auto-extract key points
- `flag_key_log_entry`: Mark important logs

**Phase 3: Team** (Week 3):
- `generate_team_summary`: Daily standup
- `detect_duplicate_work`: Coordination check

---

## Implementation Phases

### Phase 1: MVP - Context Restoration (Week 1) - CRITICAL

**Goal**: New agent can read chat history and restore context.

- [ ] Create folder structure (agents/, humans/, archive/)
- [ ] Create templates (chat-history-template.md, personal-log-template.md)
- [ ] Build `save_chat_history` MCP tool
- [ ] Build `restore_context_from_log` MCP tool
- [ ] Build `create_human_log_entry` MCP tool
- [ ] Test with real conversation (this one!)
- [ ] Validate: New agent continues without re-explanation

**Success Criteria**:
- User switches models mid-task
- New agent reads log and says "I understand we're working on X, next step is Y"
- User confirms: "Yes, exactly!"
- Zero re-explanation needed ✅

### Phase 2: Semantic Linking & Search (Week 2)

- [ ] Build auto-extraction of artifact references
- [ ] Create RDF triples in Santiago KG
- [ ] Build `link_log_to_artifact` tool
- [ ] Build `query_personal_logs` semantic search
- [ ] Build `generate_log_summary` auto-extraction
- [ ] Test: Find when feature X was worked on

### Phase 3: Team Coordination (Week 3)

- [ ] Build `generate_team_summary` aggregation
- [ ] Build `detect_duplicate_work` checker
- [ ] Build `flag_key_log_entry` importance marking
- [ ] Create daily standup automation
- [ ] Test: Team sees daily summary, no duplicate work

### Phase 4: Integration & Polish (Week 3)

- [ ] Update ontology with PersonalLog classes
- [ ] Write BDD scenarios for all tools
- [ ] Document in ARCHITECTURE.md
- [ ] Create demo video
- [ ] Monthly archival automation

---

## Success Metrics

### MVP Success (Phase 1)

- ✅ **Zero re-explanation needed** when switching agents
- ✅ **Context restoration time < 30 seconds** (down from 10+ minutes)
- ✅ **User satisfaction**: "Agent has full context"
- ✅ **Personal log exists** for every agent session (100% coverage)

### Long-Term Success

- **Context restoration**: 95% of sessions require zero re-explanation
- **Time savings**: Average 15 minutes saved per session = 1.25 hours/day
- **Team coordination**: 90% of team knows what others are working on
- **Learning**: 5+ patterns discovered from log analysis per month
- **Billing**: Time tracking becomes effortless (auto-generated from logs)
- **Search**: Find past decisions in < 1 minute (down from 10+ minutes)

---

## Dependencies

**Blocks**:
- Personal log feature is MVP dependency (no dependencies on other features)

**Blocked By**:
- None (can start immediately)

**Related**:
- Neurosymbolic backlog management (logs feed into prioritization context)
- Questionnaire system (questionnaires can generate log entries)
- Santiago PM MCP proxy (tools added to pm_proxy.py)

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Copilot format changes | Medium | High | Preserve original format, don't transform |
| Too much information (noise) | Low | Medium | Auto-summarization, key point extraction |
| Privacy concerns | Low | Medium | Clear warning: logs are public to team |
| Storage growth | Medium | Low | Monthly archival, compression |
| Adoption resistance | Low | Medium | Make automatic for agents, optional for humans |

---

## Future Enhancements (Post-MVP)

### Conversational Questionnaire Interface
**User insight**: "you can modify this feature in the future to have a conversational interface for this questionnaire"

**Vision**: Instead of markdown forms, have natural conversation where responses are auto-structured.

**Backlog Item**: Create cargo-manifest for this feature.

### In-Memory/Vector DB Santiago
**User insight**: "if santiago is operating in memory or with a vector db (or redis) will be important for very fast flow"

**Vision**: Load logs into fast in-memory storage (Redis, vector DB) for real-time context restoration.

**Backlog Item**: Create cargo-manifest for performance optimization.

### Performance Optimization
**User insight**: "so slow that the rate limiter may become keeping human artifacts in files"

**Vision**: Optimize artifact storage/retrieval to prevent file I/O bottleneck.

**Backlog Item**: Create cargo-manifest for scaling architecture.

---

## Metadata

```yaml
feature_id: F-027
version: 1.0.0
author: copilot-claude + hank (collaboration!)
reviewers: [santiago-pm]
estimated_effort: 3 weeks
dependencies: []
blocked_by: []
blocks: []
priority_score: 0.95  # CRITICAL (solves primary pain point)
triggered_by: personal-log-discovery-questionnaire.md
related_features:
  - F-026: Neurosymbolic backlog management
  - Questionnaire system (existing)
tags:
  - mvp
  - context-restoration
  - personal-log
  - semantic-linking
  - team-coordination
```
