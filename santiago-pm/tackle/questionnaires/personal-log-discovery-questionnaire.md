# Personal Log Discovery Questionnaire

**Date**: 2025-11-17
**Type**: Discovery
**Subject**: Personal Log Feature for AI Agents & Humans
**Investigator**: Santiago-PM (Neurosymbolic Domain Expert)

---

## 1. Context & Story Prompt

### Problem Statement

We need a way for humans and AI agents to keep a log of what they did during work sessions. For humans, this is like a journal or diary capturing context, decisions, and progress. For AI agents, this is the chat history—a record of the conversation and work performed.

**Prior Art**:

- Old `chat-history/` folder (removed during refactor) - you used to periodically ask me to recreate this
- Current `ships-logs/` - tracks issues and bugs, but not daily work narratives
- Current `captains-journals/` - exists but undefined purpose
- Santiago-PM's own folder structure demonstrates the markdown-as-asset pattern

### Working Hypothesis

A **personal log** system that combines:

1. **Human journal pattern** - daily/session-based narrative entries
2. **AI chat history pattern** - conversation transcripts with provenance
3. **Ships-log metadata** - structured frontmatter (date, status, tags)
4. **Semantic linking** - connections to features, issues, experiments worked on

Would help both humans and agents:

- Preserve context across sessions (combat "lost context" problem)
- Track what was accomplished (progress visibility)
- Link work to artifacts (provenance)
- Enable retrospectives and learning (meta-cognition)

### Story Prompt

**Tell me about a specific time when you lost context between work sessions and had to spend significant time re-orienting yourself. What were you working on? What information did you lose? How much time did it cost you to get back up to speed? How did you feel about that experience?**

**Story Response**:

[USER: I wrote a lot of story in the chat window, so you can modify this feature in the future to have a convesational interface for this questionnaire. But, ill say the number one pain point at this time is that as I use copilot with different models and switch between them, I lose track of what context each model has. Sometimes I have to re-explain things or remind the model of prior decisions, which wastes time and breaks my flow. So for the agent side, having a full record of the chat, can help any new agent, or the agent that lost context, read the log and get back up to speed quickly. For me as a human, having a personal log that captures what I was working on, what decisions I made, and what questions I had, would help me re-orient myself quickly when I come back to a task after a break or switch to another task. It would also help me reflect on my work and learn from my experiences over time.] As a human working in an IDE with git, this is essentially our ships logs, but I think we need to separate it in terms of the team vs the individual. The ships logs are for the team to track issues, bugs, and technical debt. The personal logs are for the individual to track their own work sessions, decisions, and reflections. This way, both the team and the individual can benefit from having a clear record of what was done and why. Now it gets a little less clear as the chat log is a record of the conversaion with the agent, which is both individual and team in nature. So maybe we need to think about how to structure the personal log to include both the human's perspective and the agent's perspective, while still keeping them distinct from the ships logs. Or try something and refactor it as we gather information on how well it is working.]

---

## 2. Question Set

### Q1: What are you actually trying to accomplish with a personal log?

- **Type**: text
- **Rationale**: Need to understand the core job-to-be-done before designing the solution
- **Response**:

[USER: Initially, not have the AI loose context between sessions. For me as a human, to be able to quickly re-orient myself when I come back to a task after a break or switch to another task. Also, to have a record of my decisions and reflections for future reference and learning.]

---

### Q2: Who would use this feature?

- **Type**: choice (multiple selection)
- **Rationale**: Determines scope and interface design
- **Choices**:
  - [ ] Human developers (you)
  - [ ] AI agents (Santiago, proxies)
  - [x] Both humans and agents
  - [ ] Future team members (other humans)
  - [ ] Other: [specify]
- **Response**:

[USER: as this is the personal log, this can turn into the chat history of the agent, and human developers can use it as their personal journal]

---

### Q3: How often would you create personal log entries?

- **Type**: choice
- **Rationale**: Frequency determines file organization and naming conventions
- **Choices**:
  - [x] Multiple times per day (per task)
  - [x] Once per work session (start/end of day)
  - [ ] Once per week (retrospective)
  - [ ] Only when significant events occur
  - [ ] Varies by context
- **Response**:

[USER: generally we would use this once per day, but copilot has lost context in the middle of a task, so having it more frequently would be helpful]

---

### Q4: What information should a personal log capture?

- **Type**: choice (multiple selection) + text
- **Rationale**: Defines the schema and frontmatter structure
- **Choices**:
  - [x] **Summary**: What was accomplished this session
  - [x] **Context**: What you were trying to solve
  - [x] **Decisions**: Key choices made and why
  - [x] **Blockers**: What's stuck or confusing
  - [x] **Questions**: Open questions or uncertainties
  - [x] **Mood/Energy**: How you felt (optional for humans)
  - [x] **Artifacts created**: Links to files/features/issues touched
  - [x] **Learning**: What you learned or realized
  - [x] **Next steps**: What to do next session
  - [x] Other: [specify]
- **Response**:

[USER: Look at how copilot captures history and use as much of that as possible as we want to make it easy for the agent/worker/human/santiago to reference prior context and decisions. As santiago evolves, we can use linked data to connect this log to the many assets that were worked on, modified, mentioned during the work. This will then be loaded into the graph and santiago pm can use it (for all types of decision making decisions to outcomes and improve over time. This is another key to how the pm domain knowledge loaded into a santiago, especially if if is operating in memory or with a vector db (or redis) will be important for very fast flow on the team. In fact, so slow that the rate limiter may become keeping human artifacts in files. hint: if you were scanning this file, you would also notice the idea for a new feature...]

---

### Q5: Should personal logs be structured or freeform?

- **Type**: choice
- **Rationale**: Balances flexibility vs. searchability
- **Choices**:
  - [x] Highly structured (YAML fields, checkboxes, required sections)
  - [x] Lightly structured (suggested sections, but flexible)
  - [ ] Mostly freeform (journal-style narrative with minimal structure)
  - [x] Hybrid (structured metadata + freeform content)
- **Response**:

[USER: Depends, if chat has a format for it's history, use it (see that is an example of building a domain model for this feature) and for a human, we would have structured metadata + freeform content so they can express themselves fully while still capturing key info in a consistent way. We may then later experiment with what works best for each type of entity on the team AND what works best for the whole team / santiago and system. hint: if you were scanning this file, you would also notice the idea for a new feature...]

---

### Q6: How do personal logs relate to ships-logs?

- **Type**: text
- **Rationale**: Understanding the distinction helps with ontology design
- **Question**: Ships-logs currently track issues (bugs, blockers, technical debt). How is a personal log different? When would you create each?
- **Response**:

[USER: In a sense, all of the assets in the PM folders and santiago-pm knowledge graph version of that, is a record of the "team conversaion", but it is helpful for us to have a daily log of what the team has accomplished. There are a bunch of XP, Safe and agile practices around daily standups, retrospectives, and sprint reviews that emphasize the importance of reflecting on what was done, what was learned, and what to do next. The ships logs are for the team to track issues, bugs, and technical debt. The personal logs are for the individual to track their own work sessions, decisions, and reflections.  BUT one of the key differences here is that all of this domain knowledge will be loaded into the Santiago-pm and be made available for planning and for other team members to reference (so we may want to warn humans that this is public to the team)...]

---

### Q7: Should AI agents automatically create personal logs?

- **Type**: boolean + text
- **Rationale**: Determines if this is manual or automated for agents
- **Question**: Should Santiago automatically generate a personal log entry at the end of each conversation, or should it be explicit (user asks "create personal log")?
- **Choices**:
  - [x] Automatic (always generate)
  - [ ] Explicit (only when requested)
  - [ ] Configurable (user can toggle)
- **Response**:

[USER: Automatic is best as we want to capture everything for context, but having a way to flag or highlight key entries would be helpful so we can quickly find important logs later. Santiago-pm can use NuSy methods to extract key points from the chat history and create a structured log entry automatically. Mainly, is there new work that informs any of the other work, and how can the team help this individaul be more effective?]

---

### Q8: What would you want to do with old personal logs?

- **Type**: text
- **Rationale**: Determines search, retrieval, and archival needs
- **Question**: Imagine you have 100 personal log entries from the past 3 months. What would you want to do with them?
- **Examples**:
  - Search for when you worked on Feature X
  - Review what blocked you last week
  - Generate a weekly summary report
  - Train an AI on your working patterns
  - Archive old logs to reduce clutter
- **Response**:

[USER: As an agent, I would want to be able to search for specific topics or decisions made in past logs to inform current work. As a human, I would want to review my past logs to reflect on my progress, identify patterns in my work habits, and learn from past challenges. I might also want to generate summaries of my work over a certain period to share with the team or for my own records. Archiving old logs would be useful to keep the workspace organized, but I would want to ensure that they are still accessible if needed in the future. Lastly, as a human, I can use this to summarize my work for billing or time tracking purposes.]

---

### Q9: How should personal logs integrate with existing santiago-pm artifacts?

- **Type**: text
- **Rationale**: Determines semantic relationships and linking strategy
- **Question**: Should personal logs link to cargo-manifests (features), ships-logs (issues), voyage-trials (experiments)? How would those links work?
- **Response**:

[USER: santiago-pm should be able to create semantic links between personal logs and other artifacts like cargo-manifests, ships-logs, and voyage-trials. For example, a personal log entry could link to the specific feature being worked on in a cargo-manifest, or to any issues encountered that are tracked in ships-logs. These links could be established through metadata in the personal log frontmatter, allowing for easy navigation between related artifacts. This would help provide context and provenance for the work being done, making it easier to understand the relationships between different pieces of work within the project.]

---

### Q10: What would make this feature successful for you?

- **Type**: text
- **Rationale**: Defines acceptance criteria and success metrics
- **Question**: In 3 months, if this personal log feature exists and you're using it, what would that look like? How would you know it's working?
- **Response**:

[USER: MVP - we save the chat history in a way that the new agent working with me (Hank) can read it and restore context. This is more of a feature of how we are working today. When santiago's are set up and working on a team together, this will be any team member being able to understand what the other team members are working on and how they are progressing on their tasks. This will help the team to coordinate better and avoid duplication of work. It will also help the team to learn from each other's experiences and improve their processes over time.]

---

## 3. Analysis & Action Mapping

### Synthesis

**Key Insights**:

1. **Context Loss is the Primary Pain Point** (MVP Focus)
   - Agents lose context when switching models or sessions
   - Humans lose context when switching tasks or returning after breaks
   - Current cost: Time wasted re-explaining, flow broken
   - **MVP Success Criteria**: New agent can read chat history and restore full context

2. **Two Distinct Log Types with Different Formats**
   - **Agent logs**: Chat history format (preserve existing structure), automatic generation
   - **Human logs**: Structured metadata + freeform narrative (journal-style)
   - Both need semantic linking to artifacts (cargo-manifests, ships-logs, voyage-trials)
   - Distinction: **Personal** (individual work) vs **Ships** (team issues/bugs)

3. **Semantic Linking is Key to Value**
   - Logs must link to: features worked on, issues encountered, decisions made, artifacts created
   - This enables: provenance tracking, context retrieval, learning from outcomes
   - Santiago-PM can query logs to understand: "What was worked on? What decisions were made? What blockers exist?"
   - **Future value**: Load into graph → fast flow decisions → learn from decisions-to-outcomes

4. **Automatic vs Manual Generation**
   - **Agents**: Automatic always (capture everything for context)
   - **Humans**: Automatic with manual override (suggest structure, allow freeform)
   - Flagging/highlighting key entries for quick retrieval
   - Santiago can extract key points using neurosymbolic methods

5. **Multiple Use Cases Beyond Context Restoration**
   - **Search**: Find when Feature X was worked on, what blocked us last week
   - **Reflection**: Review progress, identify patterns, learn from challenges
   - **Summaries**: Generate weekly reports for team or billing/time tracking
   - **Coordination**: Team understands what others are working on, avoid duplication
   - **Learning**: Improve processes over time from historical data

6. **New Feature Hints Detected** 🎯
   - **Conversational Questionnaire Interface**: "you can modify this feature in the future to have a conversational interface for this questionnaire"
   - **In-Memory/Vector DB Santiago**: "if santiago is operating in memory or with a vector db (or redis) will be important for very fast flow on the team"
   - **Rate Limiter**: "so slow that the rate limiter may become keeping human artifacts in files" (performance optimization opportunity)

### Recommended Behaviors (Existing Tackle)

**Already available in santiago-pm**:

- **create_note** (notes-domain-model)
  - **Why**: Could be used for journal-like entries
  - **Gap**: Not optimized for session-based logging, lacks temporal structure
  - **Verdict**: Not recommended - build dedicated personal log behavior

- **log_issue** (ships-logs)
  - **Why**: Has YAML frontmatter + markdown pattern (proven structure)
  - **Gap**: Issue-focused (bugs/blockers), not narrative/progress-focused
  - **Verdict**: Use as pattern inspiration, but keep separate (team vs individual)

- **link_related_notes** (notes-domain-model)
  - **Why**: Can create semantic links between log entries
  - **Gap**: Works, but need to define relationship types for logs
  - **Verdict**: ✅ Reuse for semantic linking (worked_on, mentioned, decided, blocked_by)

- **update_backlog** (from pm_proxy.py)
  - **Why**: Already exists in MCP tools
  - **Gap**: For backlog items, but shows Santiago can update artifacts
  - **Verdict**: Pattern to follow - personal logs can trigger backlog updates

### Proposed New Tools

**Phase 1: MVP - Chat History Preservation** (Priority: CRITICAL)

1. **save_chat_history** ⭐ MVP
   - **Purpose**: Save current chat conversation to personal log (for agents)
   - **Inputs**: conversation_id, participant (agent/human), format (preserve copilot format)
   - **Outputs**: log file path, semantic links to artifacts mentioned
   - **Why MVP**: Solves primary pain point (context loss when switching models)

2. **restore_context_from_log** ⭐ MVP
   - **Purpose**: Load previous chat history so new agent can restore context
   - **Inputs**: log_id or date_range
   - **Outputs**: conversation context, key decisions, artifacts worked on, current state
   - **Why MVP**: Enables "new agent reads log and gets up to speed"

3. **create_human_log_entry** ⭐ MVP
   - **Purpose**: Human creates personal journal entry (structured metadata + freeform)
   - **Inputs**: date, summary, decisions, blockers, artifacts_worked_on, next_steps, narrative (freeform)
   - **Outputs**: log file with semantic links
   - **Why MVP**: Allows humans to capture their work sessions

**Phase 2: Enhanced Functionality**

4. **query_personal_logs**
   - **Purpose**: Search across historical logs (semantic search)
   - **Inputs**: query (text), date_range (optional), tags (optional), entity_type (agent/human)
   - **Outputs**: matching log entries with excerpts, relevance scores

5. **link_log_to_artifact**
   - **Purpose**: Create semantic relationship between log and artifact
   - **Inputs**: log_id, artifact_id, relationship_type (worked_on, mentioned, decided, blocked_by)
   - **Outputs**: RDF triple in KG

6. **generate_log_summary**
   - **Purpose**: Auto-generate summary from chat history using neurosymbolic extraction
   - **Inputs**: chat_transcript, extract_decisions (bool), extract_artifacts (bool)
   - **Outputs**: structured summary with key points, decisions, artifacts

7. **flag_key_log_entry**
   - **Purpose**: Mark important logs for quick retrieval
   - **Inputs**: log_id, importance (high/medium/low), reason (text)
   - **Outputs**: updated log metadata

**Phase 3: Team Coordination**

8. **generate_team_summary**
   - **Purpose**: Aggregate individual logs into team standup report
   - **Inputs**: date_range, team_members (list)
   - **Outputs**: markdown report (who worked on what, blockers, decisions)

9. **detect_duplicate_work**
   - **Purpose**: Scan logs to identify when multiple people work on same thing
   - **Inputs**: date_range
   - **Outputs**: potential duplications, coordination suggestions

### Knowledge to Capture

**New ontology concepts** (pm-domain-ontology.ttl):

```turtle
nusy:PersonalLog a rdfs:Class ;
    rdfs:subClassOf nusy:Artifact ;
    rdfs:label "Personal Log" ;
    rdfs:comment "Session-based journal entry capturing work progress, context, and decisions" .

nusy:SessionLog a rdfs:Class ;
    rdfs:subClassOf nusy:PersonalLog ;
    rdfs:label "Session Log" ;
    rdfs:comment "Log entry for a single work session (human or AI)" .

nusy:DecisionLog a rdfs:Class ;
    rdfs:subClassOf nusy:PersonalLog ;
    rdfs:label "Decision Log" ;
    rdfs:comment "Record of a significant decision and its rationale" .

# Relationships
nusy:loggedInSession a rdf:Property ;
    rdfs:domain nusy:Artifact ;
    rdfs:range nusy:SessionLog ;
    rdfs:label "logged in session" ;
    rdfs:comment "Links an artifact (Feature, Issue) to the session where it was worked on" .

nusy:sessionWorkedOn a rdf:Property ;
    rdfs:domain nusy:SessionLog ;
    rdfs:range nusy:Artifact ;
    rdfs:label "session worked on" ;
    rdfs:comment "Links a session log to artifacts that were created or modified" .

nusy:followsSession a rdf:Property ;
    rdfs:domain nusy:SessionLog ;
    rdfs:range nusy:SessionLog ;
    rdfs:label "follows session" ;
    rdfs:comment "Temporal link to previous session (chronological ordering)" .
```

### Proposed Artifacts

**RECOMMENDED: Option C - Hybrid Structure** ✅

Rationale from user responses:
- Personal logs serve different purpose than ships-logs (individual vs team issues)
- Need both session-based logs (frequent) AND higher-level reflections (weekly)
- Chat history format is different from human journal format
- Separation enables privacy (personal) vs public (team)

**Structure**:

```
santiago-pm/
├── personal-logs/              # Session-based work logs (MVP focus)
│   ├── README.md              # Purpose, usage, difference from ships-logs
│   ├── personal-log-template.md  # Template for humans
│   ├── chat-history-template.md  # Template for agents (copilot format)
│   ├── agents/                # Agent chat histories
│   │   ├── 2025-11-17-santiago-pm-neurosymbolic-bdd.md
│   │   ├── 2025-11-17-copilot-claude-backlog-feature.md
│   │   └── 2025-11-18-copilot-gpt4-personal-log-design.md
│   ├── humans/                # Human journal entries
│   │   ├── 2025-11-17-hank-questionnaire-completion.md
│   │   └── 2025-11-18-hank-personal-log-reflection.md
│   └── archive/               # Old logs (monthly archival)
│       └── 2025-11/
│
├── captains-journals/          # Higher-level reflections (future)
│   ├── README.md              # Strategic insights, retrospectives
│   ├── weekly/                # Weekly retrospectives
│   │   └── 2025-W47-retrospective.md
│   ├── decisions/             # Architecture decision records (ADRs)
│   │   └── 2025-11-17-questionnaire-as-tackle.md
│   └── learning/              # Meta-learning, pattern discoveries
│       └── 2025-11-17-artifact-workflow-is-lean-kanban.md
│
└── ships-logs/                # EXISTING - Team issues/bugs (no change)
    ├── README.md
    └── [issues, blockers, technical debt]
```

**Key Design Decisions**:

1. **agents/ vs humans/ separation**: Different formats (chat history vs journal)
2. **personal-logs/ focus**: Daily/session-based (frequent), context preservation
3. **captains-journals/ focus**: Weekly/strategic (infrequent), meta-learning
4. **ships-logs/ unchanged**: Team issues, bugs, technical debt (existing pattern)
5. **Privacy note**: Personal logs are "public to team" (loaded into Santiago-PM KG)

**File Naming Conventions**:

- **Agent logs**: `YYYY-MM-DD-{agent-name}-{brief-topic}.md`
- **Human logs**: `YYYY-MM-DD-{human-name}-{brief-topic}.md`
- **Chat format**: Preserve whatever format Copilot uses (minimize transformation)

### FHIR Alignment

This questionnaire itself demonstrates the **FHIR Questionnaire → QuestionnaireResponse → Resource extraction** pattern:

1. **Questionnaire**: This file (defines questions)
2. **QuestionnaireResponse**: User's filled-in answers
3. **Extraction**: Responses → Feature file (cargo-manifest), Note file (captains-journal), or new tackle tool spec

---

## 4. Next Steps

**Phase 1: MVP - Chat History Preservation** (Priority: CRITICAL)

- [x] User completes questionnaire responses ✅
- [x] Santiago analyzes responses and fills in "Analysis & Action Mapping" section ✅
- [x] Create decision: Which artifact structure? → **Option C: Hybrid** ✅
- [ ] Create folder structure (personal-logs/agents/, personal-logs/humans/, captains-journals/)
- [ ] Create chat-history-template.md (preserve Copilot format)
- [ ] Create personal-log-template.md (humans: structured metadata + freeform)
- [ ] Create README.md for personal-logs/ (purpose, usage, privacy note)
- [ ] Save THIS chat as first agent log (proof-of-concept)
- [ ] Create cargo-manifest for personal-log-feature.md

**Phase 2: MCP Tools** (Week 2)

- [ ] Build `save_chat_history` MCP tool
- [ ] Build `restore_context_from_log` MCP tool
- [ ] Build `create_human_log_entry` MCP tool
- [ ] Build `link_log_to_artifact` MCP tool
- [ ] Test with real conversation context restoration

**Phase 3: Ontology & Integration** (Week 2-3)

- [ ] Update pm-domain-ontology.ttl with PersonalLog, SessionLog, DecisionLog classes
- [ ] Add semantic relationships (worked_on, mentioned, decided, blocked_by)
- [ ] Write BDD scenarios for personal log behaviors
- [ ] Integrate with backlog management (logs → backlog prioritization context)

**Phase 4: Advanced Features** (Week 3+)

- [ ] Build `query_personal_logs` (semantic search)
- [ ] Build `generate_log_summary` (neurosymbolic extraction)
- [ ] Build `generate_team_summary` (daily standup aggregation)
- [ ] Build `flag_key_log_entry` (importance tagging)
- [ ] Archival automation (monthly archive old logs)

**New Features Discovered** (Future Backlog):

- [ ] **Conversational Questionnaire Interface**: Chat-based questionnaire flow instead of markdown form
- [ ] **In-Memory/Vector DB Santiago**: Speed optimization for fast team flow (Redis/vector DB)
- [ ] **Performance Optimization**: Address "human artifacts in files" rate limiter

**Meta**:

- [ ] Document questionnaire pattern in knowledge/catches/
- [ ] Add questionnaire-as-tackle to santiago-pm MCP manifest
- [ ] Consider: santiago-ux/ mini-domain for UXR capability?

---

## Metadata

```yaml
id: personal-log-discovery-questionnaire
type: questionnaire
questionnaire_type: discovery
subject: personal-log-feature
status: draft
created_at: 2025-11-17
completed_at: null
investigator: Santiago-PM (Neurosymbolic Reasoner)
respondent: hankhead
extracted_artifacts: []
related_questionnaires: []
hypothesis: "Daily journal + chat history pattern with semantic linking will solve context loss problem"
success_criteria:
  - User completes all 10 questions with detailed responses
  - Santiago generates actionable recommendations (3+ tools or artifacts)
  - Decision made on artifact structure (personal-logs/ vs captains-journals/)
  - First personal log entry created within 1 session
```
