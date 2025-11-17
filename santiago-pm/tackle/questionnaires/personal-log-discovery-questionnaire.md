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

[USER: Please write your story here - 2-5 paragraphs describing a real situation where lost context hurt your productivity or caused frustration]

---

## 2. Question Set

### Q1: What are you actually trying to accomplish with a personal log?

- **Type**: text
- **Rationale**: Need to understand the core job-to-be-done before designing the solution
- **Response**:

[USER: Your answer here]

---

### Q2: Who would use this feature?

- **Type**: choice (multiple selection)
- **Rationale**: Determines scope and interface design
- **Choices**:
  - [ ] Human developers (you)
  - [ ] AI agents (Santiago, proxies)
  - [ ] Both humans and agents
  - [ ] Future team members (other humans)
  - [ ] Other: [specify]
- **Response**:

[USER: Select all that apply, add comments]

---

### Q3: How often would you create personal log entries?

- **Type**: choice
- **Rationale**: Frequency determines file organization and naming conventions
- **Choices**:
  - [ ] Multiple times per day (per task)
  - [ ] Once per work session (start/end of day)
  - [ ] Once per week (retrospective)
  - [ ] Only when significant events occur
  - [ ] Varies by context
- **Response**:

[USER: Your answer]

---

### Q4: What information should a personal log capture?

- **Type**: choice (multiple selection) + text
- **Rationale**: Defines the schema and frontmatter structure
- **Choices**:
  - [ ] **Summary**: What was accomplished this session
  - [ ] **Context**: What you were trying to solve
  - [ ] **Decisions**: Key choices made and why
  - [ ] **Blockers**: What's stuck or confusing
  - [ ] **Questions**: Open questions or uncertainties
  - [ ] **Mood/Energy**: How you felt (optional for humans)
  - [ ] **Artifacts created**: Links to files/features/issues touched
  - [ ] **Learning**: What you learned or realized
  - [ ] **Next steps**: What to do next session
  - [ ] Other: [specify]
- **Response**:

[USER: Select all that apply, note any additional fields you want]

---

### Q5: Should personal logs be structured or freeform?

- **Type**: choice
- **Rationale**: Balances flexibility vs. searchability
- **Choices**:
  - [ ] Highly structured (YAML fields, checkboxes, required sections)
  - [ ] Lightly structured (suggested sections, but flexible)
  - [ ] Mostly freeform (journal-style narrative with minimal structure)
  - [ ] Hybrid (structured metadata + freeform content)
- **Response**:

[USER: Your preference and why]

---

### Q6: How do personal logs relate to ships-logs?

- **Type**: text
- **Rationale**: Understanding the distinction helps with ontology design
- **Question**: Ships-logs currently track issues (bugs, blockers, technical debt). How is a personal log different? When would you create each?
- **Response**:

[USER: Describe the relationship]

---

### Q7: Should AI agents automatically create personal logs?

- **Type**: boolean + text
- **Rationale**: Determines if this is manual or automated for agents
- **Question**: Should Santiago automatically generate a personal log entry at the end of each conversation, or should it be explicit (user asks "create personal log")?
- **Choices**:
  - [ ] Automatic (always generate)
  - [ ] Explicit (only when requested)
  - [ ] Configurable (user can toggle)
- **Response**:

[USER: Your preference and reasoning]

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

[USER: Describe your use cases]

---

### Q9: How should personal logs integrate with existing santiago-pm artifacts?

- **Type**: text
- **Rationale**: Determines semantic relationships and linking strategy
- **Question**: Should personal logs link to cargo-manifests (features), ships-logs (issues), voyage-trials (experiments)? How would those links work?
- **Response**:

[USER: Describe integration points]

---

### Q10: What would make this feature successful for you?

- **Type**: text
- **Rationale**: Defines acceptance criteria and success metrics
- **Question**: In 3 months, if this personal log feature exists and you're using it, what would that look like? How would you know it's working?
- **Response**:

[USER: Describe your ideal outcome]

---

## 3. Analysis & Action Mapping

### Synthesis

[Santiago will fill this in after user completes questions]

**Key Insights**:

1. [Insight from responses]
2. [Insight from responses]
3. [Insight from responses]

### Recommended Behaviors (Existing Tackle)

**Already available in santiago-pm**:

- **create_note** (notes-domain-model)
  - **Why**: Could be used for journal-like entries
  - **Gap**: Not optimized for session-based logging, lacks temporal structure

- **log_issue** (ships-logs)
  - **Why**: Has YAML frontmatter + markdown pattern
  - **Gap**: Issue-focused, not narrative/progress-focused

- **link_related_notes** (notes-domain-model)
  - **Why**: Can create semantic links between log entries
  - **Gap**: Works, but need to define relationship types for logs

### Proposed New Tools

[Santiago will propose tools based on responses]

**Potential MCP tools**:

1. **log_session_start**
   - **Purpose**: Begin a work session, create log entry stub
   - **Inputs**: session_goal (text), context (text)
   - **Outputs**: log file path, session_id

2. **log_session_end**
   - **Purpose**: Complete session log with summary
   - **Inputs**: session_id, summary (text), artifacts_created (list)
   - **Outputs**: updated log file, links to artifacts

3. **log_decision**
   - **Purpose**: Capture a significant decision mid-session
   - **Inputs**: decision (text), rationale (text), alternatives_considered (list)
   - **Outputs**: decision entry in current log

4. **query_personal_logs**
   - **Purpose**: Search across historical logs
   - **Inputs**: query (text), date_range (optional), tags (optional)
   - **Outputs**: matching log entries with excerpts

5. **generate_session_summary**
   - **Purpose**: Auto-generate summary from chat history (for AI agents)
   - **Inputs**: chat_transcript (text), session_duration (time)
   - **Outputs**: structured summary with key points

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

**Option A: Dedicated personal-logs/ folder** (mirrors ships-logs)

```
santiago-pm/personal-logs/
├── README.md
├── personal-log-template.md
├── 2025-11-17-neurosymbolic-bdd-session.md
├── 2025-11-18-personal-log-design-session.md
└── archive/
    └── 2025-11/
```

**Option B: Use captains-journals/** (repurpose existing folder)

```
santiago-pm/captains-journals/
├── README.md  (update purpose)
├── daily/
│   ├── 2025-11-17.md
│   └── 2025-11-18.md
├── weekly/
│   └── 2025-W47-retrospective.md
└── decisions/
    └── 2025-11-17-questionnaire-as-tackle.md
```

**Option C: Hybrid** (both exist, different purposes)

- **personal-logs/**: Session-based work logs (daily narrative)
- **captains-journals/**: Higher-level reflections (weekly retrospectives, strategic insights)

**Recommendation**: [Santiago will recommend after seeing user responses]

### FHIR Alignment

This questionnaire itself demonstrates the **FHIR Questionnaire → QuestionnaireResponse → Resource extraction** pattern:

1. **Questionnaire**: This file (defines questions)
2. **QuestionnaireResponse**: User's filled-in answers
3. **Extraction**: Responses → Feature file (cargo-manifest), Note file (captains-journal), or new tackle tool spec

---

## 4. Next Steps

**Immediate**:

- [ ] User completes questionnaire responses
- [ ] Santiago analyzes responses and fills in "Analysis & Action Mapping" section
- [ ] Create decision: Which artifact structure (A, B, or C)?
- [ ] Create template file for chosen structure

**Follow-up**:

- [ ] Build MCP tool prototypes (if new tools are needed)
- [ ] Update pm-domain-ontology.ttl with PersonalLog concepts
- [ ] Add personal log behavior to santiago-pm BDD tests
- [ ] Create first personal log entry as proof-of-concept
- [ ] Update README.md and ARCHITECTURE.md with personal log pattern

**Meta**:

- [ ] Consider: Should questionnaires/ become a formal santiago-ux mini-domain?
- [ ] Document this questionnaire pattern in knowledge/catches/
- [ ] Add questionnaire-as-tackle to santiago-pm MCP manifest

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
