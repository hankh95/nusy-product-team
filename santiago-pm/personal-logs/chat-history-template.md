# Chat History Template (AI Agents)

**Purpose**: Preserve conversation context so new agents can restore understanding.

---

## Metadata

```yaml
---
artifact_type: personal-log
log_type: agent-chat-history
agent_name: [copilot-claude | copilot-gpt4 | santiago-pm | etc.]
session_date: YYYY-MM-DD
session_start: YYYY-MM-DDTHH:MM:SSZ
session_end: YYYY-MM-DDTHH:MM:SSZ
session_duration: [minutes or hours]
conversation_id: [unique ID if available]
model: [e.g., claude-sonnet-4.5, gpt-4-turbo]

# Context
context_summary: |
  Brief summary of what this conversation was about.
  What problem were we solving? What were we building?

# Work Accomplished
summary: |
  What did we accomplish in this session?
  Key milestones, artifacts created, decisions made.

# Artifacts
worked_on: []      # IDs or paths of artifacts worked on
created: []        # New artifacts created this session
modified: []       # Existing artifacts modified
mentioned: []      # Artifacts referenced in conversation

# Decisions
key_decisions:
  - decision: ""
    rationale: ""
    alternatives_considered: []
    timestamp: ""

# State
blockers: []       # What's blocking progress
questions: []      # Open questions or uncertainties
next_steps: []     # What to do next session

# Semantic Links
related_to: []     # Related logs, features, issues
follows_session: null  # Previous session log (if continuation)
continued_by: null     # Next session log (filled retroactively)

# Flags
importance: [low | medium | high | critical]
flagged_for: []    # Tags for quick retrieval (e.g., "architecture-decision", "bug-fix")

tags: []
---
```

---

## Conversation Transcript

**Format**: Preserve whatever format Copilot/chat interface uses. Minimize transformation to avoid losing context.

### Turn 1: Human

[User message]

### Turn 2: Agent

[Agent response]

### Turn 3: Human

[User message]

### Turn 4: Agent

[Agent response]

[Continue for full conversation...]

---

## Session Notes (Optional)

**Extracted Key Points**:
- [Santiago can auto-extract key decisions, insights, patterns]
- [This section is for quick scanning without reading full transcript]

**Context for Next Session**:
- [What should the next agent know before continuing?]
- [Current state of work]
- [Outstanding questions or blockers]

---

## How to Use This Template

### For Automatic Logging (Agents)

```python
# MCP tool: save_chat_history
save_chat_history(
    conversation_id="conv_12345",
    agent_name="copilot-claude",
    format="preserve_copilot_format",  # Don't transform
    extract_metadata=True,              # Auto-fill YAML
    extract_semantic_links=True         # Auto-link to artifacts
)
```

### For Manual Logging (Debugging)

1. Copy this template
2. Name file: `YYYY-MM-DD-{agent-name}-{brief-topic}.md`
3. Fill in metadata (copy from Copilot interface)
4. Paste conversation transcript (preserve original format)
5. Optionally add session notes
6. Save to `personal-logs/agents/`

### For Context Restoration

```python
# MCP tool: restore_context_from_log
context = restore_context_from_log(
    log_id="2025-11-17-copilot-claude-backlog-feature",
    include_artifacts=True,     # Load mentioned artifacts
    include_decisions=True,     # Extract key decisions
    include_state=True          # Current state (blockers, next steps)
)

# New agent uses this context to continue conversation
new_agent.initialize_with_context(context)
```

---

## Example: Filled Log

See `2025-11-17-copilot-claude-personal-log-design.md` for complete example.

---

**Meta**: This template prioritizes **minimal transformation**. We want to preserve the original conversation format (Copilot's native structure) to avoid losing context during conversion. The metadata layer adds structure for querying without altering the core content.
