# Personal Logs

**Purpose**: Capture session-based work logs for both humans and AI agents to preserve context across sessions and enable effective collaboration.

---

## What Are Personal Logs?

**Personal logs** are session-based records of individual work—what you did, what you decided, what you learned, and what's next. They serve different purposes for different team members:

### For AI Agents
- **Chat history preservation**: Full conversation transcript with context
- **Context restoration**: New agent can read log and restore full understanding
- **Semantic linking**: Connects conversations to artifacts worked on
- **Automatic generation**: Saved automatically at end of session

### For Humans
- **Work journal**: Daily narrative of progress, decisions, and reflections
- **Context recovery**: Quick re-orientation when returning to task
- **Decision log**: Record of choices made and rationale
- **Learning tool**: Reflect on patterns, identify improvements

---

## How Personal Logs Differ from Ships Logs

| Aspect | Personal Logs | Ships Logs |
|--------|---------------|------------|
| **Focus** | Individual work sessions | Team issues & bugs |
| **Audience** | Individual + team (public) | Team |
| **Content** | Progress, decisions, reflections | Blockers, technical debt |
| **Frequency** | Multiple times per day | As issues arise |
| **Format** | Chat history (agents) or journal (humans) | Structured issue reports |

**Key Distinction**: Personal logs are about **"What did I work on?"** while ships logs are about **"What's broken or blocking us?"**

---

## Structure

```
personal-logs/
├── agents/              # AI agent chat histories
│   ├── 2025-11-17-santiago-pm-neurosymbolic-bdd.md
│   ├── 2025-11-17-copilot-claude-backlog-feature.md
│   └── 2025-11-18-copilot-gpt4-personal-log-design.md
├── humans/              # Human journal entries
│   ├── 2025-11-17-hank-questionnaire-completion.md
│   └── 2025-11-18-hank-personal-log-reflection.md
└── archive/             # Old logs (monthly archival)
    └── 2025-11/
```

### File Naming Conventions

- **Agent logs**: `YYYY-MM-DD-{agent-name}-{brief-topic}.md`
- **Human logs**: `YYYY-MM-DD-{human-name}-{brief-topic}.md`

Examples:
- `2025-11-17-santiago-pm-lean-kanban-research.md`
- `2025-11-17-copilot-claude-questionnaire-design.md`
- `2025-11-17-hank-personal-log-mvp.md`

---

## Templates

- **chat-history-template.md**: For AI agents (preserves Copilot format)
- **personal-log-template.md**: For humans (structured metadata + freeform narrative)

---

## Privacy & Team Access

⚠️ **Important**: Personal logs are **PUBLIC TO THE TEAM**.

All personal logs are loaded into Santiago-PM's knowledge graph and accessible to team members. This enables:
- Context sharing (understand what others are working on)
- Coordination (avoid duplicate work)
- Learning (learn from each other's experiences)
- Provenance (trace decisions to outcomes)

If you need truly private notes, use a separate system outside the project.

---

## Use Cases

### 1. Context Restoration (MVP Focus)
**Problem**: AI agent loses context when switching models or sessions.

**Solution**: New agent reads previous chat history log and restores full context.

**Example**:
```
User: "Continue working on the backlog feature"
New Agent: *reads 2025-11-17-copilot-claude-backlog-feature.md*
New Agent: "I see we've designed neurosymbolic prioritization with 4 factors 
(customer_value, unblock_impact, worker_availability, learning_value). 
You wanted to start implementing Phase 1. Ready to proceed?"
```

### 2. Quick Re-Orientation (Human)
**Problem**: Human returns to task after break and forgets context.

**Solution**: Read yesterday's personal log to remember what you were doing.

**Example**:
```
*Reads 2025-11-17-hank-questionnaire-completion.md*
"Oh right, I was answering the personal log questionnaire and had insights 
about chat history preservation. Next step: review Santiago's analysis."
```

### 3. Team Coordination
**Problem**: Team members don't know what others are working on.

**Solution**: Santiago generates daily standup report from personal logs.

**Example**:
```
Daily Standup Summary (2025-11-18):

Hank:
- Completed personal log questionnaire ✅
- Discovered 3 new feature ideas (conversational UI, vector DB, performance)
- Next: Review Santiago's analysis and approve MVP plan

Santiago-PM:
- Analyzed questionnaire responses ✅
- Designed hybrid personal log structure (agents/ vs humans/)
- Created 9 MCP tools for personal log management
- Next: Build MVP (save_chat_history, restore_context_from_log)
```

### 4. Decision Provenance
**Problem**: "Why did we decide to use hybrid structure?"

**Solution**: Search personal logs for decision context.

**Example**:
```
Query: "personal log structure decision"
Result: 2025-11-17-santiago-pm-questionnaire-analysis.md
  "User responses indicated two distinct log types (agents vs humans) 
   with different formats. Hybrid structure (Option C) chosen to 
   accommodate both use cases while maintaining separation."
```

### 5. Learning & Improvement
**Problem**: Want to identify patterns in work habits.

**Solution**: Analyze personal logs over time.

**Example**:
```
Pattern Analysis (3 months):
- Integration work consistently underestimated by 50%
- Morning sessions 30% more productive than afternoon
- Context loss costs average 15 minutes per session
- Decision to adopt personal logs reduced context loss by 60%
```

### 6. Billing & Time Tracking (Human)
**Problem**: Need to summarize work for billing or reports.

**Solution**: Generate summary from personal logs.

**Example**:
```
Weekly Summary (2025-11-11 to 2025-11-17):
- 5 work sessions, 20 total hours
- Completed: Santiago Questionnaire System (4 files)
- Completed: Lean-Kanban Backlog Management (3 files)
- In Progress: Personal Log Feature (MVP design)
- Artifacts: 7 new files, 2,500+ lines of code/docs
```

---

## Semantic Linking

Personal logs create semantic relationships to other artifacts:

### Relationship Types

- **worked_on**: Log mentions feature/issue being worked on
  - Example: `2025-11-17-hank-questionnaire.md` → `personal-log-discovery-questionnaire.md`

- **mentioned**: Log references artifact in conversation
  - Example: `2025-11-17-copilot-backlog.md` → `lean-kanban-domain-ingestion.feature`

- **decided**: Log records decision about artifact
  - Example: `2025-11-17-santiago-analysis.md` → decision to use hybrid structure

- **blocked_by**: Log identifies blocker
  - Example: `2025-11-17-hank-work.md` → blocked by context loss issue

- **created**: Log documents artifact creation
  - Example: `2025-11-17-copilot-backlog.md` → created `neurosymbolic-backlog-management.feature`

### How Links Are Created

1. **Automatic extraction** (agents): Santiago scans chat history for artifact mentions
2. **Manual tagging** (humans): User adds `worked_on: [list]` in frontmatter
3. **Semantic search** (both): NLP identifies implicit references

### Benefits of Linking

- **Provenance**: Trace feature back to conversation that created it
- **Context**: Understand why decisions were made
- **Discovery**: Find related work across logs
- **Learning**: Analyze patterns (e.g., which features took longest?)

---

## MCP Tools

Personal logs are managed through MCP tools in `pm_proxy.py`:

### Phase 1: MVP (Critical)
- `save_chat_history`: Save conversation to agent log
- `restore_context_from_log`: Load previous log for context restoration
- `create_human_log_entry`: Create journal entry for humans

### Phase 2: Enhanced
- `query_personal_logs`: Search across logs
- `link_log_to_artifact`: Create semantic relationship
- `generate_log_summary`: Auto-extract key points
- `flag_key_log_entry`: Mark important logs

### Phase 3: Team Coordination
- `generate_team_summary`: Daily standup aggregation
- `detect_duplicate_work`: Identify coordination issues

---

## Archival

To keep workspace organized, old logs are archived monthly:

### Automatic Archival (Planned)
- Logs older than 30 days move to `archive/YYYY-MM/`
- Semantic links preserved in knowledge graph
- Still searchable via `query_personal_logs`

### Manual Archival
```bash
# Move old logs to archive
mv personal-logs/agents/2025-10-*.md personal-logs/archive/2025-10/
mv personal-logs/humans/2025-10-*.md personal-logs/archive/2025-10/
```

---

## Comparison to Other Santiago Artifacts

| Artifact | Purpose | Frequency | Audience |
|----------|---------|-----------|----------|
| **personal-logs/** | Session work logs | Multiple/day | Individual + team |
| **ships-logs/** | Team issues/bugs | As needed | Team |
| **captains-journals/** | Strategic reflections | Weekly | Team |
| **cargo-manifests/** | Feature specs | Per feature | Team |
| **research-logs/** | Investigation findings | Per research | Team |
| **voyage-trials/** | Experiment results | Per experiment | Team |

**Personal logs** are most frequent (daily/session) and most personal (individual work), but still shared with team.

---

## Getting Started

### For AI Agents
1. At end of conversation, Santiago automatically saves chat history
2. File created: `personal-logs/agents/YYYY-MM-DD-{agent}-{topic}.md`
3. Semantic links extracted from conversation
4. Next agent can restore context by reading this log

### For Humans
1. Use template: `personal-log-template.md`
2. Fill in metadata (date, summary, decisions, artifacts)
3. Write freeform narrative in main body
4. Save as: `personal-logs/humans/YYYY-MM-DD-{name}-{topic}.md`
5. Santiago extracts semantic links automatically

### Quick Commands (Planned)
```bash
# Create new human log entry
nusy pm log start "Working on personal log feature"

# Add decision to current log
nusy pm log decision "Use hybrid structure" --rationale "Accommodates agents and humans"

# Complete and save log
nusy pm log end --summary "Designed personal log MVP"

# Search logs
nusy pm logs search "context restoration"

# Generate team summary
nusy pm logs team-summary --today
```

---

## Success Metrics

Personal logs are successful if:

### MVP Success
- ✅ New agent can read chat history and restore full context (no re-explanation needed)
- ✅ Humans can re-orient in <2 minutes when returning to task
- ✅ Chat history preserved across model switches

### Long-Term Success
- 90% of sessions have personal log entry
- Context restoration time reduces by 60%
- Team coordination improves (fewer duplicate work instances)
- Learning patterns emerge (identify process improvements)
- Billing/time tracking becomes effortless (auto-generated from logs)

---

## Future Enhancements

### Conversational Questionnaire Interface
User insight: "you can modify this feature in the future to have a conversational interface for this questionnaire"

**Vision**: Instead of filling out markdown forms, have natural conversation with Santiago where responses are automatically structured into questionnaire format.

### In-Memory/Vector DB Santiago
User insight: "if santiago is operating in memory or with a vector db (or redis) will be important for very fast flow"

**Vision**: Load personal logs into fast in-memory storage (Redis, vector DB) for real-time context restoration without file I/O latency.

### Performance Optimization
User insight: "so slow that the rate limiter may become keeping human artifacts in files"

**Vision**: Optimize artifact storage/retrieval to prevent file I/O from becoming bottleneck in high-velocity teams.

---

## Questions?

- **"What if I want truly private notes?"** Use external system. Personal logs are team-visible.
- **"How often should I create logs?"** Daily minimum, more if context loss is frequent.
- **"Can I edit old logs?"** Yes, but preserve original for provenance (use git to track changes).
- **"What if I forget to log?"** Santiago can prompt: "Want to create a personal log for today's session?"
- **"How are logs different from git commits?"** Git = code changes. Personal logs = narrative + context + decisions.

---

**Meta**: This README itself demonstrates the markdown-as-asset pattern. It's both documentation and a knowledge artifact that Santiago can query.
