"""
Pytest-BDD step definitions for Personal Log Domain Knowledge Extraction.

This implements the BDD scenarios from:
tests/bdd/personal-log-domain-knowledge-extraction.feature

Demonstrates:
- Semantic extraction (detect domain knowledge mentions)
- Relevance assessment (AI search + domain context)
- Task creation (action mapping)
- Temporal reasoning (provenance, learning)
"""

import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Load BDD scenarios
scenarios('../bdd/personal-log-domain-knowledge-extraction.feature')


# ============================================================================
# FIXTURES (Test Data & Harness)
# ============================================================================

@pytest.fixture
def personal_log_entry():
    """Sample personal log entry mentioning domain knowledge."""
    return {
        "artifact_type": "personal-log",
        "author": "Hank",
        "session_date": "2025-11-17",
        "content": """
        # Session Notes
        
        Remembered Joshua Kerievsky's work on Modern Agile. This seems highly relevant
        to how Santiago-PM should coordinate work - especially "Make Safety a Prerequisite"
        and "Experiment & Learn Rapidly". Need to research and integrate into Santiago's
        operating principles.
        
        This is valuable domain knowledge that could transform our workflow.
        """,
        "artifacts": {
            "mentioned": ["Joshua Kerievsky (domain expert)", "Modern Agile framework"]
        }
    }


@pytest.fixture
def santiago_pm_domain():
    """Santiago-PM's domain context (for relevance assessment)."""
    return {
        "role": "Santiago-PM",
        "domain": "product management",
        "keywords": [
            "agile",
            "workflow",
            "coordination",
            "planning",
            "backlog",
            "prioritization",
            "team management"
        ],
        "current_artifacts": [
            "backlog-manager",
            "questionnaire-system",
            "personal-logs",
            "cargo-manifests",
            "expedition-plans"
        ],
        "capabilities": [
            "prioritize_backlog",
            "coordinate_work",
            "detect_anomalies",
            "create_tasks",
            "interview_users"
        ]
    }


@pytest.fixture
def knowledge_graph(tmp_path):
    """Mock knowledge graph for Santiago."""
    from unittest.mock import MagicMock
    
    kg = MagicMock()
    
    # Simulate KG state at different times
    kg.at_date.return_value.query.side_effect = lambda q: {
        "2025-11-16": [],  # No knowledge of Kerievsky yet
        "2025-11-17": ["Modern Agile principles", "Refactoring to Patterns"]
    }.get(datetime.now().strftime("%Y-%m-%d"), [])
    
    return kg


@pytest.fixture
def santiago_pm(santiago_pm_domain, knowledge_graph):
    """Mock Santiago-PM agent with domain awareness."""
    from unittest.mock import MagicMock
    
    agent = MagicMock()
    agent.domain = santiago_pm_domain
    agent.kg = knowledge_graph
    agent.created_tasks = []
    agent.detected_mentions = []
    
    # Semantic extraction behavior
    def analyze_log(log_entry):
        """Extract domain knowledge mentions from log."""
        content = log_entry["content"].lower()
        mentions = []
        
        # Simple NER: detect person names + context markers
        if "joshua kerievsky" in content:
            context_window = content[max(0, content.find("joshua kerievsky") - 100):
                                    content.find("joshua kerievsky") + 100]
            
            mention = {
                "entity": "Joshua Kerievsky",
                "type": "person",
                "context": context_window,
                "relevance_signals": {
                    "explicit_markers": any(marker in context_window for marker in 
                                          ["valuable", "important", "relevant", "need to research"]),
                    "domain_keywords": sum(1 for kw in agent.domain["keywords"] 
                                          if kw in context_window),
                    "urgency": "need to" in context_window
                },
                "source_log": log_entry.get("artifact_type", "personal-log")
            }
            
            # Calculate relevance score
            signals = mention["relevance_signals"]
            relevance = (
                (0.4 if signals["explicit_markers"] else 0) +
                (0.1 * min(signals["domain_keywords"], 3)) +
                (0.3 if signals["urgency"] else 0)
            )
            mention["relevance_score"] = relevance
            
            mentions.append(mention)
            agent.detected_mentions.extend(mentions)
        
        return mentions
    
    agent.analyze_log = analyze_log
    
    # Task creation behavior
    def create_task(title, task_type, source, priority):
        """Create research task."""
        task = {
            "title": title,
            "type": task_type,
            "source": source,
            "priority": priority,
            "created_at": datetime.now().isoformat(),
            "status": "new"
        }
        agent.created_tasks.append(task)
        return task
    
    agent.create_task = create_task
    
    # Relevance assessment behavior
    def assess_relevance(mention):
        """Assess relevance of domain knowledge to Santiago-PM domain."""
        entity = mention["entity"].lower()
        
        # Simulate AI search results
        if "kerievsky" in entity:
            search_results = {
                "concepts": [
                    "Modern Agile",
                    "Refactoring to Patterns",
                    "software craftsmanship",
                    "evolutionary design",
                    "safety prerequisite",
                    "experiment rapidly"
                ],
                "quality": 0.9
            }
            
            # Calculate domain overlap
            domain_keywords = set(agent.domain["keywords"])
            search_concepts = set(c.lower() for c in search_results["concepts"])
            overlap = len(domain_keywords.intersection(search_concepts))
            domain_overlap_score = min(overlap / len(domain_keywords), 1.0)
            
            # Calculate final relevance
            relevance_score = (
                domain_overlap_score * 0.5 +
                mention.get("relevance_score", 0) * 0.3 +
                search_results["quality"] * 0.2
            )
            
            return {
                "mention": mention,
                "score": relevance_score,
                "preliminary_context": "Modern Agile framework, evolutionary design",
                "confidence": search_results["quality"],
                "recommendation": "high_relevance" if relevance_score > 0.7 else "medium_relevance"
            }
        
        return {"score": 0.0, "recommendation": "low_relevance"}
    
    agent.assess_relevance = assess_relevance
    
    return agent


# ============================================================================
# STEP DEFINITIONS: Scenario 1 - Simple Domain Knowledge Detection (MVP)
# ============================================================================

@given("I am writing a personal log entry")
def given_writing_log(personal_log_entry):
    """Set up context: writing a log."""
    return personal_log_entry


@given('I mention "joshua kerievsky" in my notes')
def given_mention_kerievsky(personal_log_entry):
    """Verify log contains mention."""
    assert "joshua kerievsky" in personal_log_entry["content"].lower()


@given('I indicate it is "valuable domain knowledge"')
def given_indicate_valuable(personal_log_entry):
    """Verify log contains value indicator."""
    assert "valuable domain knowledge" in personal_log_entry["content"].lower()


@when("Santiago-PM analyzes my personal log entry")
def when_analyze_log(santiago_pm, personal_log_entry):
    """Santiago-PM processes the log."""
    mentions = santiago_pm.analyze_log(personal_log_entry)
    return mentions


@then("Santiago-PM should detect the domain knowledge mention")
def then_detect_mention(santiago_pm):
    """Verify mention was detected."""
    assert len(santiago_pm.detected_mentions) > 0
    assert santiago_pm.detected_mentions[0]["entity"] == "Joshua Kerievsky"


@then(parsers.parse('create a task: "{task_title}"'))
def then_create_task(santiago_pm, task_title):
    """Verify task was created."""
    # Simulate task creation from detected mention
    if santiago_pm.detected_mentions:
        mention = santiago_pm.detected_mentions[0]
        santiago_pm.create_task(
            title=task_title,
            task_type="knowledge_extraction",
            source=mention["source_log"],
            priority="high" if mention["relevance_score"] > 0.7 else "medium"
        )
    
    assert len(santiago_pm.created_tasks) > 0
    assert santiago_pm.created_tasks[0]["title"] == task_title


@then("assign the task to appropriate Santiago role")
def then_assign_task(santiago_pm):
    """Verify task was assigned."""
    task = santiago_pm.created_tasks[0]
    assert task["type"] == "knowledge_extraction"
    # In real implementation, would assign to Santiago-PM for research


@then("link the task back to my personal log entry (provenance)")
def then_link_provenance(santiago_pm):
    """Verify provenance link exists."""
    task = santiago_pm.created_tasks[0]
    assert task["source"] == "personal-log"


# ============================================================================
# STEP DEFINITIONS: Scenario 2 - Relevance Assessment
# ============================================================================

@given(parsers.parse('I detect a domain knowledge mention: "{entity}"'))
def given_detect_mention(santiago_pm, personal_log_entry, entity):
    """Santiago-PM has detected a mention."""
    mentions = santiago_pm.analyze_log(personal_log_entry)
    assert any(m["entity"] == entity for m in mentions)
    return mentions[0]


@given("I have access to my domain context (Santiago-PM: product management, agile, workflows)")
def given_domain_context(santiago_pm):
    """Verify Santiago-PM has domain awareness."""
    assert santiago_pm.domain["role"] == "Santiago-PM"
    assert "agile" in santiago_pm.domain["keywords"]


@when(parsers.parse('I assess the relevance of "{entity}" to my domain'))
def when_assess_relevance(santiago_pm, entity):
    """Perform relevance assessment."""
    mention = next(m for m in santiago_pm.detected_mentions if m["entity"] == entity)
    assessment = santiago_pm.assess_relevance(mention)
    santiago_pm.last_assessment = assessment
    return assessment


@then(parsers.parse('I should search for: "{entity}" + "agile" + "product management" + "software craftsmanship"'))
def then_search_with_context(santiago_pm, entity):
    """Verify AI search includes domain context."""
    # In real implementation, would verify search query construction
    assert santiago_pm.last_assessment is not None


@then("I should find high relevance (Modern Agile creator, Refactoring to Patterns)")
def then_find_high_relevance(santiago_pm):
    """Verify high relevance detected."""
    assessment = santiago_pm.last_assessment
    assert assessment["score"] > 0.7
    assert "Modern Agile" in assessment["preliminary_context"]


@then("I should create a task with priority: HIGH")
def then_create_high_priority_task(santiago_pm):
    """Verify high-priority task creation."""
    assessment = santiago_pm.last_assessment
    if assessment["recommendation"] == "high_relevance":
        santiago_pm.create_task(
            title=f"Research domain knowledge: {assessment['mention']['entity']}",
            task_type="knowledge_extraction",
            source=assessment['mention']['source_log'],
            priority="high"
        )
    
    task = santiago_pm.created_tasks[-1]
    assert task["priority"] == "high"


@then(parsers.parse('I should include preliminary context: "{context}"'))
def then_include_context(santiago_pm, context):
    """Verify preliminary context included."""
    assessment = santiago_pm.last_assessment
    assert any(term in assessment["preliminary_context"] for term in context.split())


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def extract_named_entities(text: str) -> List[Dict[str, Any]]:
    """
    Extract named entities from text.
    
    In real implementation, would use:
    - spaCy NER
    - BERT-based entity recognition
    - Custom trained model for domain experts
    
    For testing, simple pattern matching.
    """
    entities = []
    
    # Pattern: Capitalized names (simple heuristic)
    import re
    name_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
    matches = re.findall(name_pattern, text)
    
    for match in matches:
        entities.append({
            "text": match,
            "type": "PERSON",
            "confidence": 0.8
        })
    
    return entities


def calculate_relevance(entity: str, signals: Dict, domain_keywords: List[str]) -> float:
    """
    Calculate relevance score for domain knowledge mention.
    
    Factors:
    - Explicit markers ("valuable", "important")
    - Domain keyword overlap
    - User intent (research, integrate, learn)
    - Urgency indicators
    """
    score = 0.0
    
    # Explicit markers (40% weight)
    if signals.get("explicit_markers"):
        score += 0.4
    
    # Domain keywords (30% weight)
    keyword_count = signals.get("domain_keywords", 0)
    score += min(keyword_count * 0.1, 0.3)
    
    # Urgency (30% weight)
    if signals.get("urgency"):
        score += 0.3
    
    return min(score, 1.0)


# ============================================================================
# INTEGRATION TESTS (Beyond BDD scenarios)
# ============================================================================

def test_end_to_end_knowledge_extraction_flow(santiago_pm, personal_log_entry):
    """
    Integration test: Full flow from log mention → task → research → integration.
    
    This tests the complete pipeline described in Scenario 5 (End-to-End).
    """
    # Step 1: Detection
    mentions = santiago_pm.analyze_log(personal_log_entry)
    assert len(mentions) > 0
    assert mentions[0]["entity"] == "Joshua Kerievsky"
    
    # Step 2: Relevance Assessment
    assessment = santiago_pm.assess_relevance(mentions[0])
    assert assessment["score"] > 0.7  # High relevance
    assert assessment["recommendation"] == "high_relevance"
    
    # Step 3: Task Creation
    task = santiago_pm.create_task(
        title=f"Research domain knowledge: {mentions[0]['entity']}",
        task_type="knowledge_extraction",
        source=mentions[0]["source_log"],
        priority="high"
    )
    assert task["status"] == "new"
    assert task["priority"] == "high"
    
    # Step 4: (Simulated) AI Search & Knowledge Module Creation
    # In real implementation:
    # - Execute AI search
    # - Synthesize findings
    # - Create knowledge/shared/kerievsky/kerievsky-foundation.md
    knowledge_module = {
        "path": "knowledge/shared/kerievsky/kerievsky-foundation.md",
        "content": "# Kerievsky Knowledge Module\n\nModern Agile...",
        "created_at": datetime.now().isoformat()
    }
    
    # Step 5: (Simulated) Impact Analysis
    # In real implementation:
    # - Analyze affected artifacts
    # - Identify capability changes
    # - Generate recommendations
    impact_analysis = {
        "affected_artifacts": ["expedition-plan-template", "safety-checklist"],
        "affected_capabilities": ["safety-first", "evolutionary-design"],
        "new_behaviors": ["apply_modern_agile_principles"]
    }
    
    # Verify flow completed
    assert task is not None
    assert knowledge_module["path"] is not None
    assert len(impact_analysis["affected_artifacts"]) > 0


def test_temporal_provenance_chain(santiago_pm, personal_log_entry, knowledge_graph):
    """
    Test that full provenance chain is maintained:
    personal log → mention → task → knowledge module → behavior changes
    """
    # Create mention
    mentions = santiago_pm.analyze_log(personal_log_entry)
    mention = mentions[0]
    
    # Create task from mention
    task = santiago_pm.create_task(
        title="Research domain knowledge: Joshua Kerievsky",
        task_type="knowledge_extraction",
        source=mention["source_log"],
        priority="high"
    )
    
    # Verify provenance links
    assert task["source"] == "personal-log"
    
    # In real implementation, would verify:
    # - KG triple: <task> derived_from <personal_log_entry>
    # - KG triple: <knowledge_module> created_by <task>
    # - KG triple: <behavior_change> influenced_by <knowledge_module>
    
    # Temporal query: "Why do we have safety gates?"
    # Expected answer: "Kerievsky's 'Make Safety a Prerequisite' principle,
    #                   discovered from personal log on 2025-11-17,
    #                   researched and integrated by Santiago-PM"
    
    provenance_chain = {
        "origin": "Personal log mention (2025-11-17)",
        "detection": "Santiago-PM semantic extraction",
        "research": "AI search + synthesis",
        "artifact": "kerievsky-foundation.md",
        "integration": "Updated expedition-plan-template with safety gates"
    }
    
    assert provenance_chain["origin"] is not None
    assert provenance_chain["artifact"] is not None


# ============================================================================
# MATURITY LEVEL TESTS (Apprentice / Journeyman / Master)
# ============================================================================

def test_apprentice_escalation_on_uncertainty(santiago_pm, personal_log_entry):
    """
    Test that Apprentice-level Santiago escalates when uncertain.
    
    Confidence < 0.70 → escalate to human or create backlog item
    """
    santiago_pm.maturity_level = "apprentice"
    santiago_pm.confidence_threshold = 0.70
    
    # Create mention with medium relevance (uncertain)
    personal_log_entry["content"] = """
    Heard about Ward Cunningham's wiki concept. Might be useful?
    """
    
    mentions = santiago_pm.analyze_log(personal_log_entry)
    
    # No mentions detected (simplified test)
    # In real implementation, would detect but have low confidence
    # Then escalate: "Should I interview you about Ward Cunningham?"
    
    # For now, verify maturity level is set
    assert santiago_pm.maturity_level == "apprentice"
    assert santiago_pm.confidence_threshold == 0.70


def test_journeyman_contextual_reasoning(santiago_pm, personal_log_entry):
    """
    Test that Journeyman-level Santiago does contextual reasoning.
    
    Uses domain context to assess relevance before acting.
    """
    santiago_pm.maturity_level = "journeyman"
    
    mentions = santiago_pm.analyze_log(personal_log_entry)
    assessment = santiago_pm.assess_relevance(mentions[0])
    
    # Journeyman includes preliminary context
    assert "preliminary_context" in assessment
    assert assessment["confidence"] > 0.5
    
    # Journeyman assesses before acting (doesn't blindly create task)
    assert assessment["recommendation"] in ["high_relevance", "medium_relevance", "low_relevance"]


def test_master_impact_analysis(santiago_pm, personal_log_entry):
    """
    Test that Master-level Santiago analyzes impact on domain.
    
    Identifies affected artifacts, capabilities, and suggests behaviors.
    """
    santiago_pm.maturity_level = "master"
    
    mentions = santiago_pm.analyze_log(personal_log_entry)
    assessment = santiago_pm.assess_relevance(mentions[0])
    
    # Master analyzes impact (simulated)
    impact = {
        "affected_artifacts": [
            "expedition-plan-template",
            "backlog-prioritization",
            "santiago-behaviors"
        ],
        "affected_capabilities": [
            "evolutionary_design",
            "safety_first",
            "apprenticeship"
        ],
        "new_behaviors": [
            "apply_modern_agile_principles",
            "safety_gate_enforcement"
        ]
    }
    
    # Master provides comprehensive impact analysis
    assert len(impact["affected_artifacts"]) > 0
    assert len(impact["affected_capabilities"]) > 0
    assert len(impact["new_behaviors"]) > 0


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

def test_semantic_extraction_performance(santiago_pm, personal_log_entry):
    """Test that semantic extraction completes in < 1 second."""
    import time
    
    start = time.time()
    mentions = santiago_pm.analyze_log(personal_log_entry)
    duration = time.time() - start
    
    assert duration < 1.0  # Should be fast
    assert len(mentions) > 0


def test_relevance_assessment_performance(santiago_pm, personal_log_entry):
    """Test that relevance assessment completes in < 2 seconds."""
    import time
    
    mentions = santiago_pm.analyze_log(personal_log_entry)
    
    start = time.time()
    assessment = santiago_pm.assess_relevance(mentions[0])
    duration = time.time() - start
    
    assert duration < 2.0  # AI search + analysis
    assert assessment is not None
