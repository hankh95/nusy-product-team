# Questionnaire System: Sub-Plan

**Date**: 2025-11-17
**Type**: Design Decision + Implementation Plan
**Context**: Building personal log feature revealed need for structured human data collection

---

## Executive Summary

We've created a **questionnaire system** (tackle tool) that enables Santiago to interview humans using story-based UX research patterns. This document outlines:

1. What we built (3 files, 800+ lines)
2. Why it matters (bootstrap capability for UX research)
3. Where it fits (santiago-pm/tackle/ now, santiago-ux/ later)
4. How to use it (workflow for both humans and agents)
5. Next steps (ontology updates, MCP tools, migration path)

---

## What We Built

### Files Created

```
santiago-pm/tackle/questionnaires/
├── README.md (208 lines)
│   └── Overview, principles, FHIR alignment, ontology mapping, meta-learning
├── questionnaire-template.md (174 lines)
│   └── Blank template: context → questions → analysis → next steps
└── personal-log-discovery-questionnaire.md (409 lines)
    └── Example questionnaire: 10 questions about personal log feature
```

### Key Features

**Story-Based Opening**:

- Problem statement (what pain we're investigating)
- Working hypothesis (what we think might help)
- Story prompt ("Tell me about a time when...")
- User writes 2-5 paragraph narrative before answering questions

**Structured Questions**:

- 5-10 numbered questions per questionnaire
- Types: text, boolean, choice, scale(1-5)
- Each question has: Q#, type, rationale, response field
- Conditional questions (manual skip logic)

**Action Mapping**:

- Synthesis of key insights
- Recommended behaviors (existing santiago-pm tools that apply)
- Proposed new tools (MCP tools we might need to build)
- Knowledge to capture (ontology concepts)
- Proposed artifacts (new files/folders)

**FHIR-Inspired Structure**:

- Borrowed: items, linkIds, types, enableWhen, subject-independent design, extraction to resources
- Simplified: Markdown instead of JSON, inline choices, manual conditions, narrative focus

---

## Why It Matters

### Bootstrap Capability

This system teaches Santiago to:

1. **Interview humans** - structured data collection with empathy (story-first)
2. **Map qualitative → quantitative** - extract structured knowledge from narratives
3. **Validate hypotheses** - test assumptions with real user feedback
4. **Design features** - translate user needs into tools/artifacts/knowledge

### Meta-Learning Pattern

By studying this questionnaire system, Santiago learns:

- How to design data collection instruments
- How to parse human responses into actionable insights
- How to bridge UXR → PM → Engineering (requirements pipeline)

This is **self-teaching**: santiago-pm builds a tool that teaches itself how to do user research.

### Alignment with NuSy Vision

**Catchfish 4-Layer Pattern**:

1. **L1 (Raw)**: User's story response (narrative text)
2. **L2 (Entities)**: Questions + answers (structured data)
3. **L3 (Structured)**: QuestionnaireResponse (completed form)
4. **L4 (KG)**: Extracted artifacts (Feature, Note, Tool) with provenance

**EARS-Inspired Scaffolding**:

- questionnaire-template.md = investigation template
- personal-log-discovery-questionnaire.md = specific investigation
- Pattern teaches Santiago how to build more questionnaires

**Tackle Philosophy**:

- Tool that Santiago can use (not hardcoded behavior)
- Markdown-based (no special UI needed)
- Composable with other tackle (status, notes, ships-logs)

---

## Where It Fits

### Current Location: santiago-pm/tackle/questionnaires/

**Rationale**:

- PM tool (gathering requirements is PM work)
- General-purpose (any domain can use it)
- Bootstrap-ready (santiago-pm can self-improve with it)

**Relationships**:

- **captains-journals/**: Journal entries may come from questionnaire responses
- **ships-logs/**: Issues may be discovered via questionnaires
- **research-logs/**: Research findings inform questionnaire design
- **notes-domain-model**: Semantic linking applies to questionnaire responses

### Future Migration: santiago-ux/ Mini-Domain?

**When** Santiago builds 3+ UX tools (questionnaires, personas, journey-maps), consider:

```
santiago-ux/
├── knowledge/catches/ux-research/      # UXR patterns from literature
├── cargo-manifests/                    # UX features (accessibility, usability)
├── tackle/
│   ├── questionnaires/                 # THIS FOLDER (moves here)
│   ├── personas/                       # User persona toolkit
│   ├── journey-maps/                   # User journey mapping
│   └── usability-tests/                # Test protocols
├── crew-manifests/
│   └── ux-researcher.role-spec.md      # Santiago-UX role
└── ships-logs/                         # UX-specific issues

```

**Migration Trigger**:

- 5+ questionnaires created (proves pattern works)
- UX persona tool built (shows broader UX scope)
- User asks for "santiago-ux" explicitly
- Need emerges for UX-specific behaviors (recruit participants, run A/B tests, etc.)

### Ontology Placement: Layer 3 (PM Domain Specifics)

**Add to pm-domain-ontology.ttl** (after Feature, Issue, Experiment):

```turtle
# Layer 3: PM Domain-Specific Artifact Types

nusy:Questionnaire a rdfs:Class ;
    rdfs:subClassOf nusy:Artifact ;
    rdfs:label "Questionnaire" ;
    rdfs:comment "Structured data collection tool for gathering requirements from humans" .

nusy:QuestionnaireResponse a rdfs:Class ;
    rdfs:subClassOf nusy:Artifact ;
    rdfs:label "Questionnaire Response" ;
    rdfs:comment "Completed questionnaire with user answers" .

# Relationships (Layer 4: PM Behaviors)

nusy:hasQuestionnaire a rdf:Property ;
    rdfs:domain nusy:QuestionnaireResponse ;
    rdfs:range nusy:Questionnaire ;
    rdfs:label "has questionnaire" .

nusy:extractsTo a rdf:Property ;
    rdfs:domain nusy:QuestionnaireResponse ;
    rdfs:range nusy:Artifact ;
    rdfs:label "extracts to" ;
    rdfs:comment "Indicates which artifacts (Feature, Issue, Note) were created from this response" .

nusy:investigates a rdf:Property ;
    rdfs:domain nusy:Questionnaire ;
    rdfs:range nusy:Concept ;
    rdfs:label "investigates" ;
    rdfs:comment "The concept or domain being researched by this questionnaire" .
```

---

## How to Use It

### For Humans (Developer/PM)

**Workflow**:

1. **Choose or create questionnaire**:
   - Browse `santiago-pm/tackle/questionnaires/`
   - Use existing questionnaire or copy template

2. **Read story prompt**:
   - Read problem statement and hypothesis
   - Write 2-5 paragraphs under "Story Response:"

3. **Answer questions**:
   - Fill in Response: field for each numbered question
   - Skip conditional questions if not applicable

4. **Review Santiago's analysis** (if auto-generated):
   - Read "Synthesis" section
   - Review "Recommended Behaviors" (existing tools)
   - Discuss "Proposed New Tools" (what we'd need to build)

5. **Collaborate on next steps**:
   - Decide which artifacts to create
   - Update ontology if needed
   - Create follow-up questionnaires

### For Santiago (AI Agent)

**Workflow**:

1. **Identify need for data collection**:
   - User asks to build feature → need requirements
   - Hypothesis needs validation → need user feedback
   - Domain unclear → need contextual inquiry

2. **Select or generate questionnaire**:
   - Check if questionnaire exists for this topic
   - If not, copy template and customize questions

3. **Present to user**:
   - Show problem statement and hypothesis
   - Ask user to write story response
   - Guide user through questions (answer 1-10)

4. **Analyze responses**:
   - Extract key insights (3-5 findings)
   - Map to existing behaviors (which tools apply?)
   - Propose new tools (what's missing?)
   - Identify knowledge gaps (what to add to KG?)

5. **Generate artifacts**:
   - Create Feature file (if new feature discovered)
   - Create Note file (if insights captured)
   - Create Tool spec (if new MCP tool needed)
   - Update ontology (if new concepts emerged)

6. **Link provenance**:
   - QuestionnaireResponse → Feature (extractsTo)
   - QuestionnaireResponse → Questionnaire (hasQuestionnaire)
   - Feature → QuestionnaireResponse (derivedFrom)

---

## Implementation Status

### ✅ Completed

- [x] README.md (system overview, principles, FHIR alignment)
- [x] questionnaire-template.md (blank template)
- [x] personal-log-discovery-questionnaire.md (example with 10 questions)
- [x] Story-based structure (problem → hypothesis → story → questions)
- [x] Action mapping (synthesis → behaviors → tools → knowledge → artifacts)
- [x] YAML metadata (status tracking, provenance, extraction)

### 🔄 In Progress

- [ ] User completes personal-log-discovery-questionnaire.md
- [ ] Santiago analyzes responses and fills "Analysis & Action Mapping"
- [ ] Decision on personal log structure (personal-logs/ vs captains-journals/)

### 📋 Not Started

**Ontology Updates**:

- [ ] Add nusy:Questionnaire class to pm-domain-ontology.ttl
- [ ] Add nusy:QuestionnaireResponse class
- [ ] Add nusy:hasQuestionnaire, nusy:extractsTo, nusy:investigates properties

**MCP Tools** (if needed based on responses):

- [ ] conduct_questionnaire (present questions to user, collect responses)
- [ ] analyze_questionnaire_responses (auto-generate synthesis section)
- [ ] extract_artifacts_from_questionnaire (QuestionnaireResponse → Feature/Note/Tool)

**BDD Tests**:

- [ ] Create `questionnaire-management.feature` in cargo-manifests/
- [ ] Test: Create questionnaire from template
- [ ] Test: Complete questionnaire (add responses)
- [ ] Test: Analyze questionnaire (generate synthesis)
- [ ] Test: Extract artifacts (QuestionnaireResponse → Feature)

**Documentation**:

- [ ] Update ARCHITECTURE.md with questionnaire system
- [ ] Update README.md with santiago-pm/tackle/questionnaires/ section
- [ ] Add questionnaire pattern to knowledge/catches/

**Migration Path** (if santiago-ux/ materializes):

- [ ] Create santiago-ux/ folder structure
- [ ] Move questionnaires/ to santiago-ux/tackle/
- [ ] Create ux-researcher.role-spec.md
- [ ] Update imports and references

---

## Design Decisions

### Decision 1: Markdown, Not JSON/XML

**Rationale**:

- Aligns with santiago-pm's markdown-as-asset pattern
- Human-readable and editable (no special tools needed)
- Git-friendly (diffs work well)
- Simple to parse (YAML frontmatter + markdown body)

**Trade-off**:

- Less structured than FHIR JSON (no schema validation)
- No complex enableWhen logic (manual skip instructions instead)
- Limited answer validation (no built-in valuesets)

**Mitigation**:

- Use YAML frontmatter for structured metadata
- Add "Type:" field to questions for response validation (future)
- Keep FHIR concepts (items, linkIds, types) in documentation for reference

### Decision 2: Story-First, Not Questions-First

**Rationale**:

- Jeff Patton's contextual inquiry: understand context before asking specific questions
- Janey Barnes' UXR: stories reveal pain points that direct questions miss
- Hypothesis-driven: start with working theory, validate through story + questions

**Trade-off**:

- Takes more time (user writes 2-5 paragraph story)
- Less structured (story is freeform narrative)

**Mitigation**:

- Story is optional (can skip if time-constrained)
- Story informs question interpretation (provides context)
- Santiago can ask clarifying questions based on story

### Decision 3: Action Mapping, Not Just Data Collection

**Rationale**:

- Santiago needs to act on insights, not just collect data
- Questionnaire → QuestionnaireResponse → Artifact is FHIR pattern
- Santiago's job is to map user needs → tools/knowledge/behaviors

**Trade-off**:

- More work for Santiago (analysis + synthesis + proposal)
- Subjective interpretation (Santiago might misread responses)

**Mitigation**:

- User reviews Santiago's analysis (collaborative)
- Multiple hypotheses proposed (not single "right answer")
- Next Steps section makes implementation explicit

### Decision 4: santiago-pm/tackle/, Not santiago-ux/ (Yet)

**Rationale**:

- PM tool first (gathering requirements is PM work)
- Proves pattern before creating new domain
- Bootstrap-ready (santiago-pm can use it immediately)

**Trade-off**:

- Might need to move later (if UX domain emerges)
- Unclear boundary (is this PM or UX?)

**Mitigation**:

- Document migration path (this file, section above)
- Define trigger conditions (5+ questionnaires → consider santiago-ux/)
- Keep relationships loose (easy to move files later)

---

## Success Criteria

**Short-term** (this feature):

- [x] Questionnaire system designed and documented
- [x] Template created and usable
- [ ] User completes personal-log-discovery-questionnaire.md (10 questions answered)
- [ ] Santiago analyzes responses and proposes artifacts
- [ ] Personal log feature implemented (structure decided, template created, first log entry written)

**Medium-term** (pattern validation):

- [ ] 3+ questionnaires created (proves pattern is reusable)
- [ ] 2+ features discovered via questionnaires (proves value)
- [ ] Ontology updated with Questionnaire/QuestionnaireResponse concepts
- [ ] BDD tests written for questionnaire lifecycle

**Long-term** (santiago-ux emergence):

- [ ] 5+ questionnaires in use (pattern is proven)
- [ ] 2+ non-questionnaire UX tools built (personas, journey-maps, etc.)
- [ ] User explicitly requests "santiago-ux" domain
- [ ] Migration to santiago-ux/ folder completed

---

## Risks & Mitigations

### Risk 1: Questionnaires are too heavyweight

**Symptom**: User finds it tedious to write story + answer 10 questions

**Mitigation**:

- Create short-form variant (3-5 questions, no story)
- Make story optional ("Skip to questions if time-constrained")
- Allow verbal responses (transcribe conversation to questionnaire)

### Risk 2: Santiago's analysis is inaccurate

**Symptom**: Proposed tools don't match user's actual need

**Mitigation**:

- Analysis section is collaborative (user reviews and corrects)
- Multiple hypotheses proposed (not single answer)
- Follow-up questions allowed ("Did I understand X correctly?")

### Risk 3: Pattern doesn't generalize beyond personal log

**Symptom**: No other features use questionnaires

**Mitigation**:

- Identify 2-3 more candidates (status-system usability, voyage-trial UX, tackle discoverability)
- Create questionnaires proactively (don't wait for user request)
- Document pattern in knowledge/catches/ (make it visible)

### Risk 4: Ontology pollution (too many artifact types)

**Symptom**: pm-domain-ontology.ttl becomes cluttered with niche concepts

**Mitigation**:

- Keep Questionnaire at Layer 3 (peer to Feature, Issue, Experiment)
- Limit to 2-3 classes (Questionnaire, QuestionnaireResponse, maybe QuestionnaireItem)
- Use relationships (extractsTo, investigates) instead of subclasses

---

## Next Actions

**Immediate** (this session):

- [ ] User reads this plan
- [ ] User completes personal-log-discovery-questionnaire.md
- [ ] Santiago analyzes responses
- [ ] Decide: personal-logs/ folder or captains-journals/ reuse?

**Next Session**:

- [ ] Create personal log template (based on questionnaire responses)
- [ ] Write first personal log entry (proof-of-concept)
- [ ] Update pm-domain-ontology.ttl with PersonalLog + Questionnaire concepts

**Next Sprint**:

- [ ] Create BDD feature: questionnaire-management.feature
- [ ] Build MCP tools (if needed): conduct_questionnaire, analyze_questionnaire_responses
- [ ] Create 2nd questionnaire (different topic, validate pattern)

**Next Phase** (if santiago-ux/ emerges):

- [ ] Create santiago-ux/ folder structure
- [ ] Move questionnaires/ to santiago-ux/tackle/
- [ ] Create ux-researcher.role-spec.md
- [ ] Build 2+ additional UX tools (personas, journey-maps)

---

## Meta-Observation

**This entire process is self-demonstrating**:

1. User said "I want personal log feature, but interview me first"
2. Santiago needed a way to interview humans → created questionnaire system
3. Questionnaire system itself is a meta-tool (teaches Santiago how to gather requirements)
4. This plan documents the questionnaire system design
5. **We're now using the questionnaire to design the questionnaire system** (recursive!)

This is the **bootstrap loop**:

- Santiago builds tool to gather requirements
- Tool is used to gather requirements for personal log feature
- Personal log feature captures what Santiago did (this conversation)
- Chat history becomes personal log entry (meta-level)

**Old Man and the Sea** pattern in action:

- Navigator: "We need a way to interview humans" (navigation step)
- Catchfish: Extract UXR patterns from FHIR + Patton + Barnes (4 layers)
- Fishnet: This questionnaire system (test + manifest)
- **Santiago learns**: How to do user research by studying its own process

---

## Appendix: FHIR Concepts We Borrowed

| FHIR Concept | Our Implementation | Notes |
|--------------|---------------------|-------|
| Questionnaire | questionnaire-template.md | Subject-independent definition |
| QuestionnaireResponse | Completed questionnaire file | User's answers filled in |
| item | Numbered questions (Q1-Q10) | Each question is an item |
| linkId | Question numbers (Q1, Q2, etc.) | Ties response to question |
| type | Response Type field | text, boolean, choice, scale |
| text | Question text | The actual question being asked |
| enableWhen | Conditional: field | Manual skip logic |
| initial | (not used) | Could add default values |
| answerOption | Choices: checkbox list | Inline options |
| answerValueSet | (not used) | Too complex for MVP |
| definition | (potential) | Could link to ontology elements |
| Extraction | Section 3: Analysis & Action Mapping | QuestionnaireResponse → Feature/Note/Tool |

**What we simplified**:

- No JSON/XML schema (plain markdown)
- No complex enableWhen operators (manual instructions)
- No external valuesets (inline choices)
- No rendering hints (assume markdown renderer)
- No score calculation (could add later with itemWeight extension)

**What we kept**:

- Subject-independent design (template vs. instance)
- Structured items (questions have types)
- Provenance (metadata tracks creation/completion)
- Extraction pattern (responses become other resources)
- Purpose alignment (gather data to inform decisions)

---

**End of Plan**

This questionnaire system is now ready to use. Next step: User completes personal-log-discovery-questionnaire.md!
