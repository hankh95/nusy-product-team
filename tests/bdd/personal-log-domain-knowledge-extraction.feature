# Feature: Personal Log Domain Knowledge Extraction
# Priority: 0.90 (HIGH)
# Related Feature: F-027 (Personal Log Feature)
# Kerievsky Principle: "Experiment & Learn Rapidly" - capture learning from conversations

As Santiago-PM
I want to detect domain knowledge mentions in personal logs
So that I can create tasks to research and integrate valuable knowledge into the system

## Background: Semantic Understanding

Personal logs contain unstructured mentions of domain experts, patterns, frameworks, and knowledge.
Santiago-PM should:
1. **Detect** domain knowledge mentions (semantic extraction)
2. **Assess** relevance to Santiago domain (contextual reasoning)
3. **Create tasks** to research and integrate knowledge (action mapping)
4. **Escalate** if uncertain (human interview or backlog item)

This pattern demonstrates:
- **Semantic linking**: personal log → domain knowledge → tasks
- **Action mapping**: mention → detection → research → integration
- **Progressive elaboration**: simple mention → research task → knowledge module → behavior changes

---

## Scenario 1: Simple Domain Knowledge Detection (MVP)

**User Story**: As Hank, when I mention a domain expert in my personal log, Santiago-PM should create a task to research that expert.

**Given** I am writing a personal log entry
**And** I mention "joshua kerievsky" in my notes
**And** I indicate it is "valuable domain knowledge"

**When** Santiago-PM analyzes my personal log entry

**Then** Santiago-PM should detect the domain knowledge mention
**And** create a task: "Research domain knowledge: Joshua Kerievsky"
**And** assign the task to appropriate Santiago role
**And** link the task back to my personal log entry (provenance)

**Acceptance Criteria**:
- [ ] Semantic extraction detects "joshua kerievsky" as a person entity
- [ ] Context "valuable domain knowledge" increases relevance score
- [ ] Task created with:
  - Title: "Research domain knowledge: Joshua Kerievsky"
  - Type: knowledge_extraction
  - Source: personal log entry (semantic link)
  - Priority: calculated from context urgency
- [ ] Task visible in backlog or task queue
- [ ] Original log entry has relationship: `mentioned_knowledge → joshua_kerievsky`

---

## Scenario 2: Contextual Relevance Assessment (Journeyman)

**User Story**: As Santiago-PM, I should assess whether domain knowledge is relevant to my domain before researching it.

**Given** I detect a domain knowledge mention: "joshua kerievsky"
**And** I have access to my domain context (Santiago-PM: product management, agile, workflows)

**When** I assess the relevance of "joshua kerievsky" to my domain

**Then** I should search for: "joshua kerievsky" + "agile" + "product management" + "software craftsmanship"
**And** I should find high relevance (Modern Agile creator, Refactoring to Patterns)
**And** I should create a task with priority: HIGH
**And** I should include preliminary context: "Modern Agile framework, evolutionary design"

**Acceptance Criteria**:
- [ ] AI search query includes domain context keywords
- [ ] Relevance score calculated: high (0.90), medium (0.60), low (0.30)
- [ ] High relevance → immediate task creation
- [ ] Medium relevance → add to backlog for review
- [ ] Low relevance → flag for user confirmation before research
- [ ] Preliminary context included in task description

---

## Scenario 3: Impact Analysis for Santiago-PM (Master)

**User Story**: As Santiago-PM, after researching domain knowledge, I should analyze how it affects my artifacts, behaviors, and capabilities.

**Given** I have completed AI search for "joshua kerievsky"
**And** I have synthesized a knowledge module about Kerievsky's work
**And** I know my current artifacts: backlog manager, questionnaire system, personal logs, cargo manifests

**When** I analyze the impact of Kerievsky's principles on my domain

**Then** I should identify:
- Modern Agile → affects expedition planning, workflow coordination
- Refactoring to Patterns → affects artifact evolution, incremental design
- Safety prerequisite → affects ethics gates, concurrency control
- Apprenticeship model → affects Santiago maturity levels (Apprentice → Journeyman → Master)

**And** I should create a summary report:
```yaml
impact_analysis:
  knowledge_source: "Joshua Kerievsky"
  domain: "Santiago-PM"
  
  affected_artifacts:
    - artifact: expedition-plan-template
      impact: "Add safety gates (Modern Agile: Make Safety Prerequisite)"
      action: update_template
    
    - artifact: backlog-prioritization
      impact: "Add 'Experiment & Learn Rapidly' criterion"
      action: add_consideration
    
    - artifact: santiago-behaviors
      impact: "Map all behaviors to Kerievsky principles"
      action: document_alignment
  
  affected_capabilities:
    - capability: evolutionary_design
      change: "Adopt incremental refactoring over big rewrites"
      priority: high
    
    - capability: safety_first
      change: "Require safety gates before major changes"
      priority: critical
    
    - capability: apprenticeship
      change: "Formalize Santiago maturity model (Apprentice/Journeyman/Master)"
      priority: high
  
  new_behaviors_suggested:
    - behavior: apply_modern_agile_principles
      description: "Use Modern Agile 4 principles in all planning"
    
    - behavior: safety_gate_enforcement
      description: "Require Santiago-Ethicist review before major changes"
  
  next_steps:
    - "Update expedition-plan-template with safety checklist"
    - "Create apprenticeship curriculum"
    - "Map Modern Agile → Santiago behaviors (BDD scenarios)"
    - "Design safety gate automation"
```

**And** I should ask the user: "I've identified 4 high-impact changes from Kerievsky's work. Should I implement these now or create backlog items?"

**Acceptance Criteria**:
- [ ] Impact analysis covers: artifacts, capabilities, behaviors
- [ ] Each impact has: description, action, priority
- [ ] Changes linked to specific Kerievsky principles
- [ ] Summary includes actionable next steps
- [ ] User consulted before making changes (safety prerequisite!)

---

## Scenario 4: Escalation When Uncertain (Apprentice)

**User Story**: As Santiago-PM (Apprentice level), when I'm uncertain about domain knowledge relevance or impact, I should escalate to a human or create a research backlog item.

**Given** I detect domain knowledge mention: "ward cunningham"
**And** AI search returns: "inventor of wiki, extreme programming, technical debt"
**And** I'm uncertain if this affects Santiago-PM domain (medium relevance: 0.55)

**When** I assess my confidence in relevance analysis

**Then** I should recognize: confidence < threshold (0.70)
**And** I should create two options:
1. **Option A**: Interview the user who wrote the log
   - Create task: "Interview Hank: How does Ward Cunningham's work apply to Santiago-PM?"
   - Include context: "Mentioned in personal log 2025-11-17, preliminary research shows XP and technical debt concepts"
   
2. **Option B**: Create research backlog item for Santiago-UX
   - Create backlog item: "Research: Ward Cunningham's relevance to Santiago-PM"
   - Assign to: Santiago-UX (user research role)
   - Priority: medium
   - Context: Personal log mention, unclear immediate impact

**And** I should present both options to user: "I found domain knowledge about Ward Cunningham. Preliminary research suggests relevance to XP practices. Should I interview you for clarification, or should I create a backlog item for deeper research?"

**Acceptance Criteria**:
- [ ] Confidence threshold checked (< 0.70 → escalate)
- [ ] Two escalation paths presented:
  - Human interview (quick clarification)
  - Research backlog item (deeper investigation)
- [ ] Context from AI search included in escalation
- [ ] User chooses escalation path (not automatic)
- [ ] Apprentice-level behavior: ask for guidance when uncertain

---

## Scenario 5: End-to-End Knowledge Integration (Full Flow)

**User Story**: As a user and Santiago-PM working together, domain knowledge mentioned in personal logs should flow through the entire integration pipeline.

**Given** I write a personal log entry:
```yaml
---
date: 2025-11-17
author: Hank
artifacts:
  mentioned:
    - Joshua Kerievsky (domain expert)
    - Modern Agile framework
---

# Session Notes

Remembered Joshua Kerievsky's work on Modern Agile. This seems highly relevant
to how Santiago-PM should coordinate work - especially "Make Safety a Prerequisite"
and "Experiment & Learn Rapidly". Need to research and integrate into Santiago's
operating principles.

## Learning
- Modern Agile could be Santiago's operating system
- Safety gates align with ethics framework
- Apprenticeship model matches our maturity levels
```

**When** Santiago-PM processes this personal log entry

**Then** the following flow should execute:

### Step 1: Detection (Immediate)
- [x] Detect mention: "Joshua Kerievsky"
- [x] Extract context: "Modern Agile", "highly relevant", "need to research"
- [x] Create semantic link: `personal_log → mentioned_knowledge → joshua_kerievsky`

### Step 2: Research Task Creation (< 1 minute)
- [x] Create task: "Research domain knowledge: Joshua Kerievsky"
- [x] Priority: HIGH (user indicated "highly relevant")
- [x] Assigned to: Santiago-PM (self)
- [x] Context: "Modern Agile, safety gates, apprenticeship model"

### Step 3: AI Search Execution (< 2 minutes)
- [x] Execute AI search: "Joshua Kerievsky Modern Agile software craftsmanship"
- [x] Synthesize findings into knowledge module
- [x] Save to: `knowledge/shared/kerievsky/kerievsky-foundation.md`

### Step 4: Impact Analysis (< 5 minutes)
- [x] Analyze impact on Santiago-PM artifacts
- [x] Identify affected capabilities
- [x] Generate suggested behavior changes
- [x] Create summary report

### Step 5: User Consultation (Human gate)
- [ ] Present findings to user
- [ ] Ask: "Should I integrate these principles now or create backlog items?"
- [ ] Wait for user decision

### Step 6: Integration (If approved)
- [ ] Update expedition-plan-template (add safety checklist)
- [ ] Create apprenticeship curriculum
- [ ] Map Modern Agile → Santiago behaviors
- [ ] Add Kerievsky principles to ontology

### Step 7: Provenance & Learning (Always)
- [x] Link knowledge module back to original personal log
- [x] Update personal log with semantic relationships
- [x] Add to Santiago-PM's learned knowledge
- [x] Create ADR (Architecture Decision Record) documenting integration

**Acceptance Criteria**:
- [ ] Complete flow: detection → research → analysis → consultation → integration
- [ ] Total time (detection → consultation): < 10 minutes
- [ ] Human gate before making changes (Kerievsky: safety prerequisite!)
- [ ] Full provenance chain: personal log → task → knowledge module → behaviors
- [ ] All artifacts updated with semantic links
- [ ] Learning captured in Santiago-PM's knowledge graph

**Success Metrics**:
- Detection accuracy: 95% (correctly identify domain knowledge mentions)
- Relevance assessment: 85% precision (high relevance = actually useful)
- Integration time: < 10 minutes (detection → user consultation)
- User satisfaction: Zero false alarms (don't create tasks for irrelevant mentions)

---

## Technical Implementation Notes

### Semantic Extraction

```python
@santiago_behavior
def extract_domain_knowledge_from_log(log_entry: PersonalLog) -> List[KnowledgeMention]:
    """
    Extract domain knowledge mentions from personal log.
    
    Pattern: NER (Named Entity Recognition) + context analysis
    """
    mentions = []
    
    # Extract entities (people, frameworks, concepts)
    entities = extract_named_entities(log_entry.content)
    
    for entity in entities:
        # Analyze context around mention
        context = get_context_window(log_entry.content, entity, window_size=100)
        
        # Calculate relevance signals
        signals = {
            'explicit_markers': has_markers(context, ['valuable', 'important', 'relevant', 'need to research']),
            'domain_keywords': count_domain_keywords(context, SANTIAGO_PM_DOMAIN),
            'user_intent': classify_intent(context),  # research, integrate, learn
            'urgency': detect_urgency(context)  # now, later, someday
        }
        
        # Calculate relevance score
        relevance = calculate_relevance(entity, signals, SANTIAGO_PM_DOMAIN)
        
        if relevance > THRESHOLD:
            mentions.append(KnowledgeMention(
                entity=entity,
                context=context,
                relevance=relevance,
                signals=signals,
                source_log=log_entry.id
            ))
    
    return mentions
```

### Relevance Assessment

```python
@santiago_behavior
def assess_knowledge_relevance(mention: KnowledgeMention) -> RelevanceAssessment:
    """
    Assess whether domain knowledge is relevant to Santiago-PM.
    
    Uses AI search + domain context matching.
    """
    # Execute AI search with domain context
    search_query = f"{mention.entity} {' '.join(SANTIAGO_PM_KEYWORDS)}"
    search_results = ai_search(search_query, max_results=5)
    
    # Extract key concepts from search results
    concepts = extract_concepts(search_results)
    
    # Match concepts to Santiago-PM domain
    domain_overlap = calculate_overlap(concepts, SANTIAGO_PM_DOMAIN)
    
    # Calculate relevance score
    relevance_score = (
        domain_overlap * 0.5 +
        mention.relevance * 0.3 +
        search_result_quality(search_results) * 0.2
    )
    
    return RelevanceAssessment(
        mention=mention,
        score=relevance_score,
        preliminary_context=summarize(search_results),
        confidence=calculate_confidence(search_results),
        recommendation=get_recommendation(relevance_score)
    )
```

### Action Mapping

```python
@santiago_behavior
def map_knowledge_to_actions(knowledge: KnowledgeModule, domain: str) -> ImpactAnalysis:
    """
    Analyze how domain knowledge affects Santiago-PM artifacts and behaviors.
    
    Kerievsky principle: "Experiment & Learn Rapidly" → test impact, learn, adapt
    """
    # Get current Santiago-PM artifacts
    artifacts = get_domain_artifacts(domain)
    
    # Get current capabilities
    capabilities = get_domain_capabilities(domain)
    
    # Get current behaviors
    behaviors = get_domain_behaviors(domain)
    
    # Analyze impact on each
    affected_artifacts = []
    for artifact in artifacts:
        impact = analyze_artifact_impact(knowledge, artifact)
        if impact.score > 0.5:
            affected_artifacts.append(impact)
    
    affected_capabilities = []
    for capability in capabilities:
        impact = analyze_capability_impact(knowledge, capability)
        if impact.score > 0.5:
            affected_capabilities.append(impact)
    
    new_behaviors = suggest_new_behaviors(knowledge, domain)
    
    return ImpactAnalysis(
        knowledge_source=knowledge,
        affected_artifacts=affected_artifacts,
        affected_capabilities=affected_capabilities,
        new_behaviors=new_behaviors,
        next_steps=generate_next_steps(affected_artifacts, affected_capabilities),
        confidence=calculate_confidence([affected_artifacts, affected_capabilities])
    )
```

### Escalation Decision

```python
@santiago_behavior
def decide_escalation(assessment: RelevanceAssessment, maturity_level: str) -> EscalationDecision:
    """
    Decide whether to escalate to human or create backlog item.
    
    Kerievsky apprenticeship: Apprentices ask for guidance when uncertain.
    """
    confidence_threshold = {
        'apprentice': 0.70,  # Low confidence → escalate
        'journeyman': 0.50,  # Medium confidence → proceed with caution
        'master': 0.30       # High confidence → proceed autonomously
    }
    
    threshold = confidence_threshold[maturity_level]
    
    if assessment.confidence < threshold:
        # Uncertain → offer escalation options
        return EscalationDecision(
            should_escalate=True,
            options=[
                EscalationOption(
                    type='human_interview',
                    description=f"Interview user about: {assessment.mention.entity}",
                    estimated_time="5-10 minutes",
                    priority='high' if assessment.score > 0.7 else 'medium'
                ),
                EscalationOption(
                    type='research_backlog',
                    description=f"Create research backlog item: {assessment.mention.entity}",
                    assign_to='Santiago-UX',
                    priority=calculate_priority(assessment)
                )
            ],
            reason=f"Confidence {assessment.confidence:.2f} below threshold {threshold}",
            preliminary_context=assessment.preliminary_context
        )
    else:
        # Confident → proceed autonomously
        return EscalationDecision(
            should_escalate=False,
            action='proceed_with_research',
            confidence=assessment.confidence
        )
```

---

## Ontology Extensions

### New Classes

```turtle
# Domain Knowledge
nusy:DomainKnowledge a rdfs:Class ;
    rdfs:label "Domain Knowledge" ;
    rdfs:comment "Expert knowledge, frameworks, patterns, principles" .

nusy:KnowledgeMention a rdfs:Class ;
    rdfs:label "Knowledge Mention" ;
    rdfs:comment "Reference to domain knowledge in personal log or artifact" .

nusy:ImpactAnalysis a rdfs:Class ;
    rdfs:label "Impact Analysis" ;
    rdfs:comment "Analysis of how knowledge affects domain artifacts/behaviors" .

# Tasks
nusy:KnowledgeExtractionTask a rdfs:Class ;
    rdfs:subClassOf nusy:Task ;
    rdfs:label "Knowledge Extraction Task" ;
    rdfs:comment "Task to research and integrate domain knowledge" .
```

### New Properties

```turtle
# Knowledge relationships
nusy:mentionedKnowledge a rdf:Property ;
    rdfs:domain nusy:PersonalLog ;
    rdfs:range nusy:DomainKnowledge ;
    rdfs:label "mentioned knowledge" .

nusy:extractedFrom a rdf:Property ;
    rdfs:domain nusy:KnowledgeModule ;
    rdfs:range nusy:PersonalLog ;
    rdfs:label "extracted from" .

nusy:affectsArtifact a rdf:Property ;
    rdfs:domain nusy:DomainKnowledge ;
    rdfs:range nusy:Artifact ;
    rdfs:label "affects artifact" .

nusy:affectsCapability a rdf:Property ;
    rdfs:domain nusy:DomainKnowledge ;
    rdfs:range nusy:Capability ;
    rdfs:label "affects capability" .

nusy:createdTask a rdf:Property ;
    rdfs:domain nusy:KnowledgeMention ;
    rdfs:range nusy:Task ;
    rdfs:label "created task" .
```

### Example RDF Triples

```turtle
# Personal log mentions Kerievsky
<personal-log:2025-11-17-copilot-claude-personal-log-mvp> 
    nusy:mentionedKnowledge <knowledge:joshua-kerievsky> ;
    nusy:author <user:hank> ;
    nusy:created "2025-11-17T12:00:00Z" .

# Knowledge mention detected
<mention:kerievsky-2025-11-17> a nusy:KnowledgeMention ;
    nusy:entity <knowledge:joshua-kerievsky> ;
    nusy:sourceLog <personal-log:2025-11-17-copilot-claude-personal-log-mvp> ;
    nusy:relevanceScore 0.95 ;
    nusy:context "Modern Agile, safety gates, apprenticeship model" ;
    nusy:createdTask <task:research-kerievsky> .

# Task created
<task:research-kerievsky> a nusy:KnowledgeExtractionTask ;
    nusy:title "Research domain knowledge: Joshua Kerievsky" ;
    nusy:priority "high" ;
    nusy:assignedTo <agent:santiago-pm> ;
    nusy:status "completed" ;
    nusy:resultedInArtifact <knowledge:kerievsky-foundation> .

# Knowledge module created
<knowledge:kerievsky-foundation> a nusy:KnowledgeModule ;
    nusy:extractedFrom <personal-log:2025-11-17-copilot-claude-personal-log-mvp> ;
    nusy:createdBy <agent:santiago-pm> ;
    nusy:filePath "knowledge/shared/kerievsky/kerievsky-foundation.md" ;
    nusy:affectsArtifact <artifact:expedition-plan-template> ;
    nusy:affectsCapability <capability:safety-first> ;
    nusy:affectsCapability <capability:evolutionary-design> .

# Impact on artifacts
<knowledge:kerievsky-foundation> nusy:affectsArtifact <artifact:expedition-plan-template> ;
    nusy:impactDescription "Add safety gates (Modern Agile: Make Safety Prerequisite)" ;
    nusy:impactPriority "critical" .
```

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Detection accuracy | 95% | Correctly identify domain knowledge mentions |
| False positive rate | < 5% | Avoid creating tasks for irrelevant mentions |
| Relevance precision | 85% | High relevance = actually useful |
| Time to consultation | < 10 min | Detection → user consultation |
| Integration quality | 90% | Integrated knowledge improves Santiago effectiveness |
| User satisfaction | > 4.5/5 | "Santiago catches what I need without noise" |

---

## Related Features

- **F-027**: Personal Log Feature (parent feature)
- **F-026**: Lean-Kanban Backlog Management (task creation integration)
- **Future**: Santiago-UX research coordinator (escalation path)
- **Future**: Conversational questionnaire (human interview automation)

---

## Meta

This BDD scenario itself demonstrates:
- **Kerievsky's "Experiment & Learn Rapidly"**: Personal log → detection → research → learning
- **Modern Agile "Make Safety Prerequisite"**: Human gate before making changes
- **Apprenticeship model**: Different behaviors for Apprentice/Journeyman/Master maturity levels
- **Semantic linking**: Full provenance chain from log mention → knowledge module → behavior changes

**Status**: ready-for-implementation
**Priority**: 0.90 (HIGH) - Key differentiator for Santiago's learning capability
**Estimated effort**: 2 weeks (Phase 1: detection + task creation, Phase 2: impact analysis + integration)
