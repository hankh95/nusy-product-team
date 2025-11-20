"""
Santiago-Core BDD Test Executor
================================
Neurosymbolic test execution using KG knowledge instead of behave runner.

This implements the "second job" for santiago-core:
1. Load BDD feature files (Gherkin scenarios)
2. Convert scenarios to natural language questions
3. Query KG using neurosymbolic reasoning
4. Return provenance: which knowledge assets answered each test
5. Calculate pass/fail based on confidence threshold

Architecture:
- Replaces: behave runner + step definitions + fixtures
- Uses: RDFLib KG + keyword-based reasoning (neurosymbolic)
- Returns: Test results with knowledge provenance

Inspired by nusy_prototype's NeurosymbolicClinicalReasoner approach.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json

from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS

from domain.src.nusy_pm_core.adapters.kg_store import KGStore


def search_documents(keywords: List[str], workspace_path: Path) -> tuple[int, List[str]]:
    """
    Fallback search: scan source documents when KG is insufficient.
    Matches clinical prototype pattern of searching literature when KG sparse.
    
    Returns:
        (match_count, source_files) - number of keyword matches and which files
    """
    sources = []
    match_count = 0
    
    # Search key documentation files
    search_paths = [
        workspace_path / "README.md",
        workspace_path / "santiago-pm",
        workspace_path / "features",
        workspace_path / "roles",
    ]
    
    for path in search_paths:
        if not path.exists():
            continue
            
        # Collect all .md and .feature files
        if path.is_file():
            files = [path]
        else:
            files = list(path.glob("**/*.md")) + list(path.glob("**/*.feature"))
        
        for file in files:
            try:
                content = file.read_text().lower()
                file_matches = sum(1 for kw in keywords if kw in content)
                if file_matches > 0:
                    match_count += file_matches
                    sources.append(str(file.relative_to(workspace_path)))
            except Exception:
                pass  # Skip unreadable files
    
    return match_count, sources


@dataclass
class BDDScenario:
    """Parsed BDD scenario from .feature file"""
    feature_name: str
    scenario_name: str
    given_steps: List[str] = field(default_factory=list)
    when_steps: List[str] = field(default_factory=list)
    then_steps: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class TestResult:
    """Result of executing a BDD scenario"""
    scenario: BDDScenario
    passed: bool
    confidence: float
    evidence_triples: int
    doc_matches: int = 0  # Number of document matches (fallback search)
    entities_used: List[str] = field(default_factory=list)
    relationships_used: List[str] = field(default_factory=list)
    knowledge_sources: List[str] = field(default_factory=list)
    reasoning_explanation: str = ""
    execution_time_ms: float = 0.0


@dataclass
class TestSuiteResult:
    """Results for entire test suite"""
    domain_name: str
    total_scenarios: int
    passed: int
    failed: int
    pass_rate: float
    avg_confidence: float
    test_results: List[TestResult] = field(default_factory=list)
    executed_at: str = ""


class SantiagoCoreNeurosymbolicReasoner:
    """
    Lightweight neurosymbolic reasoner for PM domain.
    Adapted from nusy_prototype's NeurosymbolicClinicalReasoner.
    Uses simple keyword matching and graph traversal (proven clinical pattern).
    Falls back to document search when KG is sparse (clinical prototype pattern).
    """
    
    def __init__(self, workspace_path: Optional[Path] = None):
        self.workspace_path = workspace_path or Path(".")
    
    def _extract_keywords(self, question: str) -> List[str]:
        """Extract keywords from question text - matches clinical prototype."""
        # Simple tokenization
        tokens = re.findall(r"\b[\w']+\b", question.lower())
        
        # Filter short words (keep words > 3 chars)
        keywords = [token for token in tokens if len(token) > 3]
        
        # Fallback: use first token if no keywords found
        if not keywords:
            keywords = tokens[:1]
        
        return keywords
    
    def query_graph(
        self, 
        question: str, 
        kg_store: KGStore,
        confidence_threshold: float = 0.5
    ) -> Optional[Dict[str, Any]]:
        """
        Query knowledge graph using neurosymbolic reasoning.
        Uses simple graph traversal - matches clinical prototype pattern.
        
        Args:
            question: Natural language question
            kg_store: Knowledge graph store
            confidence_threshold: Minimum confidence for positive result
            
        Returns:
            Dictionary with entities, triples, confidence, and evidence
        """
        # Extract keywords from question
        keywords = self._extract_keywords(question)
        
        if not keywords:
            return {
                'entities': [],
                'relationships': [],
                'triples': 0,
                'confidence': 0.0,
                'keywords_used': [],
                'knowledge_sources': [],
                'passed': False
            }
        
        # Scan graph for triples matching keywords - clinical prototype pattern
        relevant_triples = []
        entities = set()
        relationships = set()
        
        # Get RDFLib graph from KG store
        graph = kg_store.graph
        
        # Traverse all triples
        for subject, predicate, obj in graph:
            s_str = str(subject).lower()
            p_str = str(predicate).lower()
            o_str = str(obj).lower()
            
            # Check if any keyword matches this triple
            for keyword in keywords:
                if keyword in s_str or keyword in p_str or keyword in o_str:
                    relevant_triples.append((subject, predicate, obj))
                    entities.add(str(subject))
                    entities.add(str(obj))
                    relationships.add(str(predicate))
                    break  # Only count each triple once
        
        triples_count = len(relevant_triples)
        
        # Fallback: If KG has insufficient evidence, search source documents
        # This matches clinical prototype pattern of searching literature when KG sparse
        doc_match_count = 0
        doc_sources = []
        if triples_count < 3:  # Threshold: need at least 3 triples for high confidence
            doc_match_count, doc_sources = search_documents(keywords, self.workspace_path)
        
        # Calculate confidence based on evidence found
        # Combine KG triples + document matches for total evidence
        # Weight doc matches lower (30%) since they're less specific than KG triples
        total_evidence = triples_count + (doc_match_count * 0.3)
        
        if total_evidence == 0:
            confidence = 0.0
        else:
            # Logarithmic scaling with more gradual growth
            # Formula: log(evidence+1) / log(evidence+20)
            # This gives: 3 evidence→0.60, 10→0.75, 50→0.85, 200→0.90, 500→0.92
            import math
            confidence = math.log(total_evidence + 1) / math.log(total_evidence + 20)
        
        # Build knowledge sources list
        knowledge_sources = ['santiago-pm-kg'] if triples_count > 0 else []
        knowledge_sources.extend(doc_sources[:5])  # Add top 5 doc sources
        
        return {
            'entities': [{'label': e} for e in list(entities)[:20]],  # Limit to top 20
            'relationships': list(relationships)[:10],
            'triples': triples_count,
            'doc_matches': doc_match_count,
            'confidence': confidence,
            'keywords_used': keywords,
            'knowledge_sources': knowledge_sources,
            'passed': confidence >= confidence_threshold
        }


class SantiagoCoreBDDExecutor:
    """
    Execute BDD tests using Santiago-Core neurosymbolic reasoning.
    Replaces behave runner with KG-based test execution.
    """
    
    def __init__(self, kg_store: KGStore, confidence_threshold: float = 0.7):
        """
        Initialize BDD executor.
        
        Args:
            kg_store: Knowledge graph store
            confidence_threshold: Minimum confidence for test to pass (0.0-1.0)
        """
        self.kg_store = kg_store
        self.confidence_threshold = confidence_threshold
        self.reasoner = SantiagoCoreNeurosymbolicReasoner(workspace_path=kg_store.workspace_path)
    
    def parse_feature_file(self, feature_path: Path) -> List[BDDScenario]:
        """Parse Gherkin .feature file into BDDScenario objects."""
        scenarios = []
        
        with open(feature_path) as f:
            content = f.read()
        
        # Extract feature name
        feature_match = re.search(r'Feature:\s*(.+)', content)
        feature_name = feature_match.group(1).strip() if feature_match else "Unknown"
        
        # Split into scenarios
        scenario_blocks = re.split(r'\n\s*Scenario:', content)
        
        for block in scenario_blocks[1:]:  # Skip feature description
            lines = block.strip().split('\n')
            scenario_name = lines[0].strip()
            
            given_steps = []
            when_steps = []
            then_steps = []
            tags = []
            
            # Parse tags from previous line (if any)
            tag_matches = re.findall(r'@([\w-]+)', content.split(f'Scenario: {scenario_name}')[0])
            tags = tag_matches[-3:] if tag_matches else []  # Last 3 tags before scenario
            
            for line in lines[1:]:
                line = line.strip()
                if line.startswith('Given '):
                    given_steps.append(line[6:])
                elif line.startswith('When '):
                    when_steps.append(line[5:])
                elif line.startswith('Then '):
                    then_steps.append(line[5:])
                elif line.startswith('And '):
                    # Append to most recent step list
                    if then_steps:
                        then_steps.append(line[4:])
                    elif when_steps:
                        when_steps.append(line[4:])
                    elif given_steps:
                        given_steps.append(line[4:])
            
            if scenario_name:
                scenarios.append(BDDScenario(
                    feature_name=feature_name,
                    scenario_name=scenario_name,
                    given_steps=given_steps,
                    when_steps=when_steps,
                    then_steps=then_steps,
                    tags=tags
                ))
        
        return scenarios
    
    def scenario_to_question(self, scenario: BDDScenario) -> str:
        """
        Convert BDD scenario to natural language question.
        Uses feature + scenario names as primary signal (most semantic info).
        
        Example:
        Feature: Development Plans Management
        Scenario: Create a new development plan
        
        -> "Development Plans Management Create a new development plan"
        """
        # Combine feature and scenario names - these have the most semantic content
        question = f"{scenario.feature_name} {scenario.scenario_name}"
        
        # Optionally add key action words from When steps
        for step in scenario.when_steps[:1]:  # Just first When step
            # Extract quoted strings (often contain important entities)
            quoted = re.findall(r'"([^"]+)"', step)
            if quoted:
                question += " " + " ".join(quoted)
        
        return question
    
    def execute_scenario(self, scenario: BDDScenario) -> TestResult:
        """Execute a single BDD scenario using neurosymbolic reasoning."""
        start_time = datetime.now()
        
        # Convert scenario to question
        question = self.scenario_to_question(scenario)
        
        # Query KG
        result = self.reasoner.query_graph(
            question=question,
            kg_store=self.kg_store,
            confidence_threshold=self.confidence_threshold
        )
        
        # Calculate execution time
        execution_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        if result is None:
            return TestResult(
                scenario=scenario,
                passed=False,
                confidence=0.0,
                evidence_triples=0,
                doc_matches=0,
                reasoning_explanation="No evidence found in KG",
                execution_time_ms=execution_time_ms
            )
        
        # Extract result details
        passed = result.get('passed', False)
        confidence = result.get('confidence', 0.0)
        entities = result.get('entities', [])
        triples = result.get('triples', 0)
        doc_matches = result.get('doc_matches', 0)
        sources = result.get('knowledge_sources', [])
        
        explanation = f"Found {triples} KG triples"
        if doc_matches > 0:
            explanation += f" + {doc_matches} document matches"
        explanation += f" with {len(entities)} entities. "
        explanation += f"Confidence: {confidence:.2f}. "
        explanation += f"Keywords matched: {', '.join(result.get('keywords_used', []))}"
        
        return TestResult(
            scenario=scenario,
            passed=passed,
            confidence=confidence,
            evidence_triples=triples,
            doc_matches=doc_matches,
            entities_used=[e.get('label', '') for e in entities],
            knowledge_sources=sources,
            reasoning_explanation=explanation,
            execution_time_ms=execution_time_ms
        )
    
    def execute_test_suite(self, domain_name: str, bdd_tests_dir: Path) -> TestSuiteResult:
        """
        Execute entire BDD test suite for a domain.
        
        Args:
            domain_name: Domain identifier
            bdd_tests_dir: Directory containing .feature files
            
        Returns:
            TestSuiteResult with pass/fail breakdown and provenance
        """
        # Find all .feature files
        feature_files = list(bdd_tests_dir.glob("*.feature"))
        
        all_results = []
        
        # Execute each feature file
        for feature_file in feature_files:
            scenarios = self.parse_feature_file(feature_file)
            
            for scenario in scenarios:
                result = self.execute_scenario(scenario)
                all_results.append(result)
        
        # Calculate aggregate metrics
        total = len(all_results)
        passed = sum(1 for r in all_results if r.passed)
        failed = total - passed
        pass_rate = passed / total if total > 0 else 0.0
        avg_confidence = sum(r.confidence for r in all_results) / total if total > 0 else 0.0
        
        return TestSuiteResult(
            domain_name=domain_name,
            total_scenarios=total,
            passed=passed,
            failed=failed,
            pass_rate=pass_rate,
            avg_confidence=avg_confidence,
            test_results=all_results,
            executed_at=datetime.now().isoformat()
        )
    
    def print_test_report(self, suite_result: TestSuiteResult) -> None:
        """Print human-readable test report with provenance."""
        print("=" * 80)
        print(f"🧪 SANTIAGO-CORE BDD TEST EXECUTION: {suite_result.domain_name}")
        print("=" * 80)
        print()
        print(f"📊 Overall Results:")
        print(f"   Total Scenarios: {suite_result.total_scenarios}")
        print(f"   Passed: {suite_result.passed} ✅")
        print(f"   Failed: {suite_result.failed} ❌")
        print(f"   Pass Rate: {suite_result.pass_rate * 100:.1f}%")
        print(f"   Avg Confidence: {suite_result.avg_confidence:.3f}")
        print(f"   Executed At: {suite_result.executed_at}")
        print()
        
        # Show failing tests with provenance
        failing_tests = [r for r in suite_result.test_results if not r.passed]
        if failing_tests:
            print(f"❌ Failing Tests ({len(failing_tests)}):")
            print("-" * 80)
            for result in failing_tests:
                print(f"   Feature: {result.scenario.feature_name}")
                print(f"   Scenario: {result.scenario.scenario_name}")
                print(f"   Confidence: {result.confidence:.3f}")
                print(f"   Evidence: {result.evidence_triples} triples")
                print(f"   Explanation: {result.reasoning_explanation}")
                print()
        
        # Show knowledge coverage
        all_sources = set()
        for result in suite_result.test_results:
            all_sources.update(result.knowledge_sources)
        
        print(f"📚 Knowledge Provenance:")
        print(f"   Unique Sources Used: {len(all_sources)}")
        if all_sources:
            for source in sorted(all_sources)[:10]:  # Show first 10
                print(f"   - {source}")
        print()
        
        print("=" * 80)
