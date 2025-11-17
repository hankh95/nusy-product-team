# Personal Log Template (Humans)

**Purpose**: Capture your work session, decisions, and reflections in a structured journal format.

---

## Metadata

```yaml
---
artifact_type: personal-log
log_type: human-journal
author: hank
session_date: 2025-11-17
session_start: HH:MM  # When you started working
session_end: HH:MM    # When you stopped
session_duration: [hours]
energy_level: [low | medium | high]  # Optional: how you felt
focus_quality: [distracted | ok | focused]  # Optional

# Context
context_summary: |
  What were you trying to accomplish this session?
  What task or feature were you working on?

# Work Accomplished
summary: |
  What did you accomplish this session?
  Key milestones, progress made, problems solved.

# Artifacts
worked_on: []      # Files, features, issues you touched
created: []        # New artifacts you created
modified: []       # Existing artifacts you changed
reviewed: []       # Code/docs you reviewed

# Decisions
key_decisions:
  - decision: ""
    rationale: ""
    alternatives_considered: []
    confidence: [low | medium | high]

# State
blockers: []       # What's blocking you
questions: []      # Open questions or uncertainties
learning: []       # What you learned or realized
mood: ""           # Optional: How you felt about the work

# Next Steps
next_session: |
  What to do next time you work on this.
  Where to pick up, what to focus on.

# Semantic Links
related_to: []     # Related logs, features, issues
follows_session: null  # Previous session (if continuation)

# Metadata
importance: [routine | notable | significant | critical]
tags: []
---
```

---

## Session Narrative

[Freeform journal-style writing. Capture your thoughts, process, insights.]

### What I Did

[Describe what you worked on this session]

### Challenges Encountered

[What was difficult? What took longer than expected?]

### Insights & Learning

[What did you realize? What patterns emerged?]

### Mood & Reflection

[Optional: How did you feel about the work? What was satisfying/frustrating?]

### For Next Time

[Advice to your future self when you return to this task]

---

## How to Use This Template

### Daily Work Session

1. **Start of session**: Copy template, fill in start time and context
2. **During session**: Add notes as you work (decisions, blockers)
3. **End of session**: Fill in summary, next steps, save file
4. **File naming**: `YYYY-MM-DD-{your-name}-{brief-topic}.md`
5. **Save location**: `personal-logs/humans/`

### Quick Template Fill

```bash
# Copy template
cp personal-log-template.md humans/2025-11-17-hank-backlog-work.md

# Edit file
# ... fill in metadata and narrative ...

# Santiago can auto-extract semantic links from content
```

### Lightweight Alternative (If Short Session)

If you don't have time for full template, minimal version:

```markdown
# Quick Log: [Brief Topic]

**Date**: YYYY-MM-DD
**Duration**: [X hours]

**Did**: [1-2 sentence summary]
**Next**: [What to do next time]
```

---

## Tips for Effective Personal Logs

### What to Include

✅ **Good**:
- Specific decisions made ("Chose hybrid structure over Option A/B")
- Problems solved ("Fixed context loss by saving chat history")
- Blockers encountered ("Stuck on how to preserve Copilot format")
- Learning insights ("Realized semantic linking is key value prop")
- Next steps ("Start implementing save_chat_history tool")

❌ **Not Necessary**:
- Exact code snippets (git has that)
- Detailed step-by-step (git commits show that)
- Perfect prose (this is your journal, not a report)

### When to Create Logs

- **Daily minimum**: One log per work day
- **Task switch**: When switching focus to different feature
- **After breakthrough**: When you solve hard problem or have insight
- **Before long break**: Capture context before vacation/time off
- **Context loss recovery**: When you struggle to remember what you were doing

### How Much to Write

- **Minimum**: 2-3 sentences (summary + next steps)
- **Ideal**: 1-2 paragraphs (context + what happened + learning)
- **Maximum**: Whatever helps you (some people like detailed journals)

**Rule of thumb**: If future-you can read this and remember what you were doing in <2 minutes, it's enough.

---

## Example: Filled Log

```yaml
---
artifact_type: personal-log
log_type: human-journal
author: hank
session_date: 2025-11-17
session_start: 09:00
session_end: 11:30
session_duration: 2.5 hours
energy_level: high
focus_quality: focused

context_summary: |
  Completing personal log discovery questionnaire that Santiago created.
  Goal: Provide detailed responses so Santiago can design the feature.

summary: |
  Completed all 10 questions in the personal log questionnaire.
  Provided rich insights about context loss pain points, chat history
  preservation needs, and semantic linking requirements. Also dropped
  hints about 3 future features (conversational UI, vector DB, performance).

worked_on:
  - santiago-pm/tackle/questionnaires/personal-log-discovery-questionnaire.md

key_decisions:
  - decision: "Use hybrid structure (personal-logs/ for daily, captains-journals/ for strategic)"
    rationale: "Agents and humans have different needs. Chat history vs journal format."
    confidence: high

blockers: []
questions: []

learning:
  - "Personal logs are about individual work sessions, ships-logs are about team issues"
  - "Context loss is the primary pain point (MVP should focus on this)"
  - "Semantic linking to artifacts is key for future value"

next_session: |
  Review Santiago's analysis of my questionnaire responses.
  Approve or adjust the personal log MVP plan.
  Test the first personal log entry (this conversation should become one!).

related_to:
  - santiago-pm/tackle/questionnaires/personal-log-discovery-questionnaire.md

importance: significant
tags: [questionnaire, personal-log, mvp, discovery]
---

## Session Narrative

### What I Did

Spent 2.5 hours completing the personal log discovery questionnaire. Santiago asked 10 really good questions that made me think deeply about:

1. What problem are we actually solving? (Context loss!)
2. Who uses this? (Both agents and humans, but differently)
3. How is this different from ships-logs? (Individual vs team focus)

I provided detailed responses with multiple insights per question. Santiago designed this questionnaire to extract not just answers but also feature hints—I dropped 3 hints about future features (conversational questionnaire UI, vector DB Santiago, performance optimization).

### Key Insight

The real MVP is simple: **Save chat history so new agent can restore context**. That's it. Everything else (semantic linking, summaries, team coordination) is valuable but not critical for first version.

This is like the "personal log inception"—I'm filling out a questionnaire about personal logs, which will help design personal logs, which will capture this conversation about designing personal logs. Very meta!

### Mood & Reflection

This felt productive. The questionnaire format worked really well—Santiago's questions were sharp and helped me articulate fuzzy ideas. I'm excited to see Santiago's analysis and the resulting MVP design.

One surprise: I realized that personal logs could help with billing/time tracking (didn't think of that use case initially).

### For Next Time

When I come back to this:
1. Read Santiago's completed analysis in the questionnaire file
2. Review the personal log MVP plan
3. Approve and let Santiago start building
4. Test by having this conversation saved as our first agent personal log

**Meta note**: This log entry itself is an example of what I want—it captures context, decisions, and next steps. If I read this tomorrow, I'll know exactly where we are.
```

---

## Comparison to Other Logs

| Log Type | Purpose | Format | Example |
|----------|---------|--------|---------|
| **Personal Log** | Individual work session | Structured + freeform | "Worked on backlog feature, decided X, learned Y" |
| **Ships Log** | Team issue/bug | Structured issue report | "Database query slow, root cause: missing index" |
| **Captain's Journal** | Strategic reflection | Freeform essay | "Why we chose Lean-Kanban methodology" |
| **Research Log** | Investigation findings | Structured analysis | "Discovered artifact workflow = Lean-Kanban" |
| **Git Commit** | Code change | Brief description | "feat: Add save_chat_history MCP tool" |

Personal logs are the **daily work narrative**—they connect the dots between all the other artifacts.

---

**Meta**: This template itself is a knowledge artifact. Santiago can query it to understand the personal log structure and guide humans in creating effective logs.
