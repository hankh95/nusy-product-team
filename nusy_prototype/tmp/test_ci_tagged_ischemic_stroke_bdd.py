#!/usr/bin/env python3
"""
Test CI-Tagged Ischemic Stroke Knowledge Graph with BDD Questions

This script tests our neurosymbolic framework by loading the available CI-tagged
ischemic stroke knowledge graph and evaluating it against the 100 BDD test scenarios.
"""

import torch
import torch_geometric as pyg
from torch_geometric.data import Data
import rdflib
import json
from typing import Dict, List, Tuple, Optional
import numpy as np
from pathlib import Path
import pandas as pd

# Import our neurosymbolic components
import sys
sys.path.append('/workspaces/clinical-intelligence-starter-v10-simplified')
from neurosymbolic_prototype import (
    NeurosymbolicClinicalReasoner,
    load_ci_tagged_graph
)


def load_ischemic_stroke_graph() -> rdflib.Graph:
    """Load the ischemic stroke CI-tagged knowledge graph."""
    file_path = "/workspaces/clinical-intelligence-starter-v10-simplified/ci-tagged-source/1078_Ischemic stroke_risk_batch_12_CQA_approved_2025-09-05T15-46-50_knowledge_graph_framed.jsonld"

    print(f"Loading CI-tagged ischemic stroke knowledge graph: {file_path}")
    return load_ci_tagged_graph(file_path)


def load_ischemic_stroke_bdd_scenarios() -> List[Dict]:
    """Load the 100 ischemic stroke BDD scenarios."""
    scenario_file = "/workspaces/clinical-intelligence-starter-v10-simplified/generated/BMJ_1078_ischemic_stroke/bdd-fishnet/runs/2025-11-12T05-31-31Z/artifacts/scenario_inventory.json"

    print(f"Loading ischemic stroke BDD scenarios: {scenario_file}")

    with open(scenario_file, 'r') as f:
        data = json.load(f)

    # Extract scenarios from the "scenarios" key
    scenarios = data.get('scenarios', [])

    return scenarios


def extract_questions_from_scenarios(scenarios: List[Dict]) -> List[str]:
    """Extract decision questions from BDD scenarios."""
    questions = []

    for scenario in scenarios:
        if 'decisionQuestion' in scenario and scenario['decisionQuestion']:
            questions.append(scenario['decisionQuestion'])

    # Remove duplicates while preserving order
    seen = set()
    unique_questions = []
    for q in questions:
        if q not in seen:
            seen.add(q)
            unique_questions.append(q)

    return unique_questions


def evaluate_question_coverage(reasoner: NeurosymbolicClinicalReasoner,
                              question: str,
                              graph: rdflib.Graph) -> Dict:
    """
    Evaluate how well the knowledge graph covers a specific question.

    Returns coverage assessment with confidence score and explanation.
    """
    try:
        # Convert question to graph query
        query_result = reasoner.query_graph(question, graph)

        # Calculate confidence based on result completeness
        confidence = 0.0
        explanation = "No relevant knowledge found in graph"

        if query_result:
            # Analyze result quality
            if isinstance(query_result, dict):
                if 'entities' in query_result and query_result['entities']:
                    confidence = min(0.8, len(query_result['entities']) * 0.1)
                    explanation = f"Found {len(query_result['entities'])} relevant entities"

                if 'relationships' in query_result and query_result['relationships']:
                    confidence = min(1.0, confidence + len(query_result['relationships']) * 0.05)
                    explanation += f", {len(query_result['relationships'])} relationships"

                if 'evidence' in query_result and query_result['evidence']:
                    confidence = min(1.0, confidence + 0.2)
                    explanation += ", evidence-based"

            else:
                confidence = 0.3
                explanation = "Partial match found"

        return {
            'question': question,
            'covered': confidence > 0.0,
            'confidence': confidence,
            'explanation': explanation,
            'raw_result': str(query_result)[:200] + "..." if len(str(query_result)) > 200 else str(query_result)
        }

    except Exception as e:
        return {
            'question': question,
            'covered': False,
            'confidence': 0.0,
            'explanation': f"Error processing question: {str(e)}",
            'raw_result': ""
        }


def main():
    """Main evaluation function."""
    print("=== Ischemic Stroke BDD Coverage Analysis ===\n")

    # Load knowledge graph
    try:
        graph = load_ischemic_stroke_graph()
        print(f"✓ Loaded knowledge graph with {len(graph)} triples\n")
    except Exception as e:
        print(f"✗ Failed to load knowledge graph: {e}")
        return

    # Load BDD scenarios
    try:
        scenarios = load_ischemic_stroke_bdd_scenarios()
        questions = extract_questions_from_scenarios(scenarios)
        print(f"✓ Loaded {len(scenarios)} BDD scenarios, extracted {len(questions)} unique questions\n")
    except Exception as e:
        print(f"✗ Failed to load BDD scenarios: {e}")
        return

    # Initialize neurosymbolic reasoner
    try:
        reasoner = NeurosymbolicClinicalReasoner()
        print("✓ Initialized neurosymbolic reasoner\n")
    except Exception as e:
        print(f"✗ Failed to initialize reasoner: {e}")
        return

    # Evaluate coverage
    print("Evaluating question coverage...\n")

    results = []
    covered_count = 0
    total_confidence = 0.0

    for i, question in enumerate(questions, 1):
        print(f"[{i}/{len(questions)}] Evaluating: {question[:80]}{'...' if len(question) > 80 else ''}")

        result = evaluate_question_coverage(reasoner, question, graph)
        results.append(result)

        if result['covered']:
            covered_count += 1
        total_confidence += result['confidence']

        print(f"  → {'✓' if result['covered'] else '✗'} Confidence: {result['confidence']:.2f}")

    # Summary statistics
    coverage_rate = covered_count / len(questions) if questions else 0
    avg_confidence = total_confidence / len(questions) if questions else 0

    print("\n=== Coverage Summary ===")
    print(f"Total Questions: {len(questions)}")
    print(f"Questions Covered: {covered_count}")
    print(f"Coverage Rate: {coverage_rate:.1%}")
    print(f"Average Confidence: {avg_confidence:.2f}")
    print(f"Knowledge Graph Scope: Risk factors only (incomplete)")

    # Save detailed results
    output_file = "/workspaces/clinical-intelligence-starter-v10-simplified/ai-knowledge-review/docs/ischemic_stroke_bdd_coverage_analysis.json"

    with open(output_file, 'w') as f:
        json.dump({
            'summary': {
                'total_questions': len(questions),
                'covered_questions': covered_count,
                'coverage_rate': coverage_rate,
                'average_confidence': avg_confidence,
                'knowledge_graph': 'ischemic_stroke_risk_batch_only'
            },
            'results': results
        }, f, indent=2)

    print(f"\n✓ Detailed results saved to: {output_file}")

    # Print top gaps
    print("\n=== Top Knowledge Gaps ===")
    uncovered = [r for r in results if not r['covered']]
    for result in uncovered[:10]:  # Show top 10 gaps
        print(f"• {result['question']}")
        print(f"  Reason: {result['explanation']}")

    if len(uncovered) > 10:
        print(f"... and {len(uncovered) - 10} more gaps")


if __name__ == "__main__":
    main()