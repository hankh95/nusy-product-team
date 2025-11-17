# [Questionnaire Title]

**Date**: [YYYY-MM-DD]
**Type**: Discovery | Validation | Research
**Subject**: [What we're investigating]
**Investigator**: [Santiago-PM | Human Name]

---

## 1. Context & Story Prompt

### Problem Statement

[What pain point, inefficiency, or need are we investigating?]

### Working Hypothesis

[What do we currently believe might help solve this problem?]

### Story Prompt

Tell me about a specific time when you experienced this problem. What were you trying to accomplish? What happened? How did it feel?

**Story Response**:

[User writes their story here - 2-5 paragraphs describing a real situation]

---

## 2. Question Set

### Q1: [Question text]

- **Type**: text | boolean | choice | scale(1-5)
- **Rationale**: [Why we're asking this]
- **Choices** (if applicable):
  - [ ] Option A
  - [ ] Option B
  - [ ] Option C
- **Response**:

[User's answer]

---

### Q2: [Question text]

- **Type**: text | boolean | choice | scale(1-5)
- **Rationale**: [Why we're asking this]
- **Response**:

[User's answer]

---

### Q3: [Question text]

- **Type**: text | boolean | choice | scale(1-5)
- **Rationale**: [Why we're asking this]
- **Response**:

[User's answer]

---

### Q4: [Question text]

- **Type**: text | boolean | choice | scale(1-5)
- **Rationale**: [Why we're asking this]
- **Conditional**: Only answer if [condition from earlier response]
- **Response**:

[User's answer]

---

### Q5: [Question text]

- **Type**: text | boolean | choice | scale(1-5)
- **Rationale**: [Why we're asking this]
- **Response**:

[User's answer]

---

[Add more questions as needed - typically 5-10 total]

---

## 3. Analysis & Action Mapping

### Synthesis

[Santiago or human summarizes key findings from responses]

**Key Insights**:

1. [Insight 1 from responses]
2. [Insight 2 from responses]
3. [Insight 3 from responses]

### Recommended Behaviors (Existing Tackle)

[Which santiago-pm tools/behaviors already address parts of this need?]

- **Behavior**: [e.g., create_note, status_transition]
  - **Why**: [How it helps]
  - **Gap**: [What's missing]

### Proposed New Tools

[What new MCP tools might we need to build?]

- **Tool Name**: [e.g., log_daily_progress]
  - **Purpose**: [What it does]
  - **Inputs**: [What data it needs]
  - **Outputs**: [What it produces]

### Knowledge to Capture

[What domain knowledge should go into the KG?]

- **Concept**: [e.g., DailyLog artifact type]
  - **Relationships**: [Links to Feature, Issue, etc.]
  - **Properties**: [date, summary, context, mood, etc.]

### Proposed Artifacts

[What new files/folders should we create?]

- **Artifact Type**: [e.g., captains-journals/daily/]
  - **Template**: [Link to template if exists]
  - **Frequency**: [How often created]
  - **Integration**: [How it connects to other artifacts]

---

## 4. Next Steps

- [ ] [Action item 1]
- [ ] [Action item 2]
- [ ] [Action item 3]
- [ ] Create follow-up questionnaire if needed
- [ ] Update ontology with new concepts
- [ ] Build prototypes of proposed tools

---

## Metadata

```yaml
id: [questionnaire-slug]
type: questionnaire
questionnaire_type: [discovery|validation|research]
subject: [domain-area]
status: [draft|in-progress|completed|analyzed]
created_at: [YYYY-MM-DD]
completed_at: [YYYY-MM-DD or null]
investigator: [name]
respondent: [name or role]
extracted_artifacts:
  - type: [Feature|Issue|Note|etc.]
    path: [relative-path]
  - type: [...]
    path: [...]
related_questionnaires:
  - [link-to-related-questionnaire]
```
