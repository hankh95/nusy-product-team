# Santiago Questionnaires (Tackle)

**Type**: Data Collection Tool (FHIR-inspired)  
**Pattern**: Story-Based Requirements Gathering  
**Usage**: UXR interviews, feature discovery, hypothesis validation  
**Level**: Journeyman (Lake scope)

---

## Overview

Questionnaires are a **tackle** (tool) that Santiago uses to gather structured information from humans. Inspired by:
- **FHIR Questionnaire**: Clinical data collection standard
- **Jeff Patton's contextual inquiry**: Field interviews with hypothesis testing
- **Janey Barnes' story-based UXR**: Ask users to tell real stories highlighting pain points

### Key Principles

1. **Story First**: Ask for a real-life scenario before diving into questions
2. **Hypothesis-Driven**: Start with a working theory about what might help
3. **Iterative Refinement**: Use answers to formulate next hypotheses
4. **Actionable Output**: Map responses to behaviors/tools/knowledge that solve the problem

---

## Structure

Each questionnaire is a markdown file with three sections:

### 1. Context & Story Prompt
- **Problem statement**: What pain/need are we investigating?
- **Story prompt**: "Tell me about a time when..." 
- **Working hypothesis**: What we think might help

### 2. Question Set
- Numbered questions (1-10 typically)
- Mix of types: open-ended, multiple choice, yes/no
- Conditional questions (show if earlier answer matches pattern)
- Each question has:
  - **Q#**: The question text
  - **Response Type**: text | boolean | choice | scale
  - **Rationale**: Why we're asking this
  - **Response**: (filled in by user)

### 3. Analysis & Action Mapping
- **Synthesis**: What we learned from responses
- **Behaviors**: What santiago-pm actions would help (existing tackle)
- **Tools**: What new MCP tools might be needed
- **Knowledge**: What domain knowledge needs to be captured

---

## Usage Pattern

### For Santiago (AI Agent)

```markdown
1. Review problem context
2. Present story prompt to user
3. Read user's story response
4. Ask questions 1-N, adapting based on responses
5. Synthesize findings into action mapping
6. Propose: new tackle, updates to existing artifacts, or new knowledge to capture
```

### For Humans (Developer/PM)

```markdown
1. Open questionnaire file
2. Read story prompt, write your story under "Story Response:"
3. Answer each numbered question in the Response: field
4. Review Santiago's analysis (if auto-generated)
5. Collaborate on action items
```

---

## Example: Personal Log Feature Questionnaire

See: `personal-log-discovery-questionnaire.md`

This demonstrates:
- Story-based opening ("Tell me about a time you lost context...")
- Hypothesis formation (daily journal + chat history = context preservation)
- Mixed question types (open, boolean, choice, scale)
- Action mapping to santiago-pm artifacts (captains-journals, ships-logs, tackle)

---

## Questionnaire Types

### Discovery Questionnaires
**Purpose**: Learn about a new feature need  
**Example**: personal-log-discovery-questionnaire.md  
**Output**: New artifact type or tackle tool

### Validation Questionnaires  
**Purpose**: Test hypothesis about existing feature  
**Example**: (future) status-system-usability.questionnaire.md  
**Output**: Refinements to existing tools

### Research Questionnaires
**Purpose**: Understand domain/user patterns  
**Example**: (future) pm-workflow-patterns.questionnaire.md  
**Output**: Knowledge graph updates, research-logs entries

---

## Relationship to Other Tackle

| This Tackle | Related Tackle | Relationship |
|-------------|----------------|--------------|
| questionnaires/ | captains-journals/ | Journal entries may come from questionnaire responses |
| questionnaires/ | research-logs/ | Research findings feed questionnaire design |
| questionnaires/ | status/ | Status transitions may trigger questionnaires (e.g., "Why blocked?") |
| questionnaires/ | notes-domain-model | Semantic linking applies to questionnaire responses |

---

## FHIR Questionnaire Alignment

We borrowed these concepts from FHIR:

- **Structured items**: Questions have linkIds, types, enableWhen conditions
- **QuestionnaireResponse**: User's completed form (stored as filled questionnaire)
- **item.definition**: Questions can link to ElementDefinitions (our ontology)
- **Subject-independent**: Template defines questions, response is instance
- **Extraction**: Responses convert to other resources (Feature, Issue, Note, etc.)

We simplified:
- Markdown instead of JSON/XML
- No complex enableWhen logic (use manual skip instructions)
- No answer valuesets (use inline choices)
- Focus on narrative + structured data, not pure structured data

---

## Files in This Folder

```
questionnaires/
├── README.md                                    # This file
├── questionnaire-template.md                    # Blank template
├── personal-log-discovery-questionnaire.md      # Example: Feature discovery
└── [future-questionnaires].md                   # More questionnaires as needed
```

---

## Ontology Mapping

**Potential additions** to `pm-domain-ontology.ttl`:

```turtle
nusy:Questionnaire a rdfs:Class ;
    rdfs:subClassOf nusy:Artifact ;
    rdfs:label "Questionnaire" ;
    rdfs:comment "Structured data collection tool for gathering requirements from humans" .

nusy:QuestionnaireResponse a rdfs:Class ;
    rdfs:subClassOf nusy:Artifact ;
    rdfs:label "Questionnaire Response" ;
    rdfs:comment "Completed questionnaire with user answers" .

nusy:hasQuestionnaire a rdf:Property ;
    rdfs:domain nusy:QuestionnaireResponse ;
    rdfs:range nusy:Questionnaire ;
    rdfs:label "has questionnaire" ;
    rdfs:comment "Links a response to its source questionnaire" .

nusy:extractsTo a rdf:Property ;
    rdfs:domain nusy:QuestionnaireResponse ;
    rdfs:range nusy:Artifact ;
    rdfs:label "extracts to" ;
    rdfs:comment "Indicates which artifacts were created from questionnaire responses" .
```

---

## Future: Santiago-UX Mini-Domain?

This questionnaire tackle could bootstrap a **santiago-ux** domain:

```
santiago-ux/
├── knowledge/catches/ux-research/      # UXR patterns
├── cargo-manifests/                    # UX features
├── tackle/questionnaires/              # THIS FOLDER (moves here)
├── tackle/personas/                    # User persona toolkit
├── tackle/journey-maps/                # User journey mapping
└── crew-manifests/ux-researcher.role-spec.md
```

But for now, it lives in **santiago-pm/tackle/** as a general-purpose PM tool.

---

## Meta-Learning Note

By creating this questionnaire system, Santiago learns:
1. **How to interview humans** (UXR capability)
2. **How to map qualitative data → structured artifacts** (extraction pattern)
3. **How to validate hypotheses** (research methodology)

This is a **bootstrap pattern**: santiago-pm builds UX research capability that can later become its own Santiago-UX domain.
