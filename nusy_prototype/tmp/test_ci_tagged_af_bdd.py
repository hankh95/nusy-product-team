#!/usr/bin/env python3
"""
Test CI-Tagged Atrial Fibrillation Knowledge Graph with BDD Questions

This script tests our neurosymbolic framework by loading the actual CI-tagged
atrial fibrillation knowledge graph and evaluating it against BDD-style questions.
"""

import torch
import torch_geometric as pyg
from torch_geometric.data import Data
import rdflib
import json
from typing import Dict, List, Tuple, Optional
import numpy as np
from pathlib import Path

# Import our neurosymbolic components
from ai_knowledge_review.docs.neurosymbolic_prototype import (
    NeurosymbolicClinicalReasoner,
    load_ci_tagged_graph
)


def load_atrial_fibrillation_graph() -> rdflib.Graph:
    """Load the atrial fibrillation CI-tagged knowledge graph."""
    file_path = "/workspaces/clinical-intelligence-starter-v10-simplified/ci-tagged-source/1_Established atrial fibrillation_treatment_algorithm_batch_12_CQA_approved_2025-08-13T17-15-43_knowledge_graph_framed.jsonld"

    print(f"Loading CI-tagged atrial fibrillation knowledge graph: {file_path}")
    return load_ci_tagged_graph(file_path)


def create_bdd_style_questions() -> List[str]:
    """
    Create BDD-style questions about atrial fibrillation treatment.

    These questions are designed to test clinical decision-making capabilities
    that would be expected from a comprehensive knowledge graph.
    """
    return [
        # Basic diagnostic questions
        "What are the symptoms of atrial fibrillation?",
        "How is atrial fibrillation diagnosed?",

        # Treatment strategy questions
        "When should rate control be preferred over rhythm control in atrial fibrillation?",
        "What is the first-line treatment for hemodynamically unstable atrial fibrillation?",

        # Risk stratification questions
        "Which patients with atrial fibrillation need anticoagulation?",
        "What is the CHA2DS2-VASc score used for in atrial fibrillation?",

        # Emergency management questions
        "When is DC cardioversion indicated in atrial fibrillation?",
        "What are the contraindications for DC cardioversion?",

        # Complication questions
        "What are the complications of atrial fibrillation?",
        "How does atrial fibrillation increase stroke risk?",

        # Special population questions
        "How should atrial fibrillation be managed in patients with cancer?",
        "What are the considerations for atrial fibrillation in elderly patients?"
    ]


def analyze_graph_statistics(graph: rdflib.Graph) -> Dict:
    """Analyze basic statistics of the knowledge graph."""
    stats = {
        'total_triples': len(graph),
        'unique_subjects': len(set(s for s, p, o in graph)),
        'unique_predicates': len(set(p for s, p, o in graph)),
        'unique_objects': len(set(o for s, p, o in graph))
    }

    # Count different types of relationships
    relationship_counts = {}
    for s, p, o in graph:
        pred = str(p).split('#')[-1] if '#' in str(p) else str(p).split('/')[-1]
        relationship_counts[pred] = relationship_counts.get(pred, 0) + 1

    stats['relationship_types'] = dict(sorted(relationship_counts.items(),
                                            key=lambda x: x[1], reverse=True)[:10])

    return stats


def test_question_answering(reasoner: NeurosymbolicClinicalReasoner,
                          graph_data: Data,
                          questions: List[str]) -> List[Dict]:
    """
    Test the neurosymbolic reasoner against BDD questions.

    Returns a list of question-answer pairs with confidence scores.
    """
    results = []

    print(f"\n🧠 Testing {len(questions)} BDD-style questions:")
    print("=" * 60)

    for i, question in enumerate(questions, 1):
        print(f"\n{i}. {question}")

        try:
            # Process question through neurosymbolic pipeline
            result = reasoner.forward(graph_data, question)

            confidence = result['reasoning_result']['confidence'].item()
            question_type = result['reasoning_result']['logical_result']['question_type']

            print(f"   Confidence: {confidence:.3f}")
            print(f"   Type: {question_type}")

            results.append({
                'question': question,
                'question_type': question_type,
                'confidence': confidence,
                'graph_nodes': graph_data.num_nodes,
                'graph_edges': graph_data.num_edges,
                'success': True
            })

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append({
                'question': question,
                'error': str(e),
                'success': False
            })

    return results


def generate_coverage_report(results: List[Dict]) -> Dict:
    """Generate a coverage report based on question answering results."""
    successful_answers = [r for r in results if r.get('success', False)]
    failed_answers = [r for r in results if not r.get('success', False)]

    # Calculate confidence statistics
    if successful_answers:
        confidences = [r['confidence'] for r in successful_answers]
        avg_confidence = np.mean(confidences)
        min_confidence = np.min(confidences)
        max_confidence = np.max(confidences)
    else:
        avg_confidence = min_confidence = max_confidence = 0.0

    # Analyze question types
    question_types = {}
    for result in successful_answers:
        qtype = result.get('question_type', 'unknown')
        question_types[qtype] = question_types.get(qtype, 0) + 1

    report = {
        'total_questions': len(results),
        'successful_answers': len(successful_answers),
        'failed_answers': len(failed_answers),
        'success_rate': len(successful_answers) / len(results) if results else 0,
        'confidence_stats': {
            'average': avg_confidence,
            'minimum': min_confidence,
            'maximum': max_confidence
        },
        'question_type_coverage': question_types,
        'recommendations': []
    }

    # Generate recommendations
    if report['success_rate'] < 0.8:
        report['recommendations'].append("Low success rate indicates knowledge gaps")

    if avg_confidence < 0.7:
        report['recommendations'].append("Low average confidence suggests weak reasoning")

    if len(question_types) < 3:
        report['recommendations'].append("Limited question type coverage")

    return report


def main():
    """Main function to test CI-tagged atrial fibrillation knowledge graph."""
    print("🫀 CI-Tagged Atrial Fibrillation Knowledge Graph BDD Testing")
    print("=" * 65)

    try:
        # Load the CI-tagged knowledge graph
        print("\n📚 Loading knowledge graph...")
        rdf_graph = load_atrial_fibrillation_graph()

        # Analyze graph statistics
        stats = analyze_graph_statistics(rdf_graph)
        print("✓ Graph loaded successfully")
        print(f"  - {stats['total_triples']} triples")
        print(f"  - {stats['unique_subjects']} unique subjects")
        print(f"  - {stats['unique_predicates']} unique predicates")
        print(f"  - {stats['unique_objects']} unique objects")
        print(f"  - Top relationships: {list(stats['relationship_types'].keys())[:5]}")

        # Initialize neurosymbolic reasoner
        print("\n🧠 Initializing neurosymbolic reasoner...")
        reasoner = NeurosymbolicClinicalReasoner()
        print("✓ Neurosymbolic reasoner initialized")

        # Convert to PyTorch Geometric format
        print("\n🔄 Converting to graph neural network format...")
        graph_data = reasoner.process_knowledge_graph(rdf_graph)
        print(f"✓ Converted to PyG Data: {graph_data.num_nodes} nodes, {graph_data.num_edges} edges")

        # Create BDD questions
        questions = create_bdd_style_questions()
        print(f"\n❓ Created {len(questions)} BDD-style test questions")

        # Test question answering
        results = test_question_answering(reasoner, graph_data, questions)

        # Generate coverage report
        report = generate_coverage_report(results)

        print("\n📊 COVERAGE REPORT")
        print("=" * 30)
        print(f"Questions Tested: {report['total_questions']}")
        print(f"Successful Answers: {report['successful_answers']}")
        print(f"Success Rate: {report['success_rate']:.1%}")
        print(f"Average Confidence: {report['confidence_stats']['average']:.3f}")
        print(f"Question Types Covered: {len(report['question_type_coverage'])}")

        if report['recommendations']:
            print("\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"  - {rec}")

        # Business readiness assessment
        print("\n🏢 BUSINESS READINESS ASSESSMENT")
        print("=" * 40)

        success_rate = report['success_rate']
        avg_confidence = report['confidence_stats']['average']

        if success_rate >= 0.8 and avg_confidence >= 0.7:
            readiness = "🟢 MARKET READY"
            message = "Knowledge graph demonstrates strong clinical question answering capability"
        elif success_rate >= 0.6 and avg_confidence >= 0.5:
            readiness = "🟡 NEEDS IMPROVEMENT"
            message = "Knowledge graph shows promise but requires enhancement for production use"
        else:
            readiness = "🔴 NOT MARKET READY"
            message = "Significant gaps in clinical knowledge coverage identified"

        print(f"Status: {readiness}")
        print(f"Assessment: {message}")

        print("\n✅ Testing completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)


def load_atrial_fibrillation_graph() -> rdflib.Graph:
    """Load the atrial fibrillation CI-tagged knowledge graph."""
    file_path = "/workspaces/clinical-intelligence-starter-v10-simplified/ci-tagged-source/1_Established atrial fibrillation_treatment_algorithm_batch_12_CQA_approved_2025-08-13T17-15-43_knowledge_graph_framed.jsonld"

    print(f"Loading CI-tagged atrial fibrillation knowledge graph: {file_path}")
    return load_ci_tagged_graph(file_path)


def create_bdd_style_questions() -> List[str]:
    """
    Create BDD-style questions about atrial fibrillation treatment.

    These questions are designed to test clinical decision-making capabilities
    that would be expected from a comprehensive knowledge graph.
    """
    return [
        # Basic diagnostic questions
        "What are the symptoms of atrial fibrillation?",
        "How is atrial fibrillation diagnosed?",

        # Treatment strategy questions
        "When should rate control be preferred over rhythm control in atrial fibrillation?",
        "What is the first-line treatment for hemodynamically unstable atrial fibrillation?",

        # Risk stratification questions
        "Which patients with atrial fibrillation need anticoagulation?",
        "What is the CHA2DS2-VASc score used for in atrial fibrillation?",

        # Emergency management questions
        "When is DC cardioversion indicated in atrial fibrillation?",
        "What are the contraindications for DC cardioversion?",

        # Complication questions
        "What are the complications of atrial fibrillation?",
        "How does atrial fibrillation increase stroke risk?",

        # Special population questions
        "How should atrial fibrillation be managed in patients with cancer?",
        "What are the considerations for atrial fibrillation in elderly patients?"
    ]


def analyze_graph_statistics(graph: rdflib.Graph) -> Dict:
    """Analyze basic statistics of the knowledge graph."""
    stats = {
        'total_triples': len(graph),
        'unique_subjects': len(set(s for s, p, o in graph)),
        'unique_predicates': len(set(p for s, p, o in graph)),
        'unique_objects': len(set(o for s, p, o in graph))
    }

    # Count different types of relationships
    relationship_counts = {}
    for s, p, o in graph:
        pred = str(p).split('#')[-1] if '#' in str(p) else str(p).split('/')[-1]
        relationship_counts[pred] = relationship_counts.get(pred, 0) + 1

    stats['relationship_types'] = dict(sorted(relationship_counts.items(),
                                            key=lambda x: x[1], reverse=True)[:10])

    return stats


def test_question_answering(reasoner: NeurosymbolicClinicalReasoner,
                          graph_data: Data,
                          questions: List[str]) -> List[Dict]:
    """
    Test the neurosymbolic reasoner against BDD questions.

    Returns a list of question-answer pairs with confidence scores.
    """
    results = []

    print(f"\n🧠 Testing {len(questions)} BDD-style questions:")
    print("=" * 60)

    for i, question in enumerate(questions, 1):
        print(f"\n{i}. {question}")

        try:
            # Process question through neurosymbolic pipeline
            result = reasoner.forward(graph_data, question)

            confidence = result['reasoning_result']['confidence'].item()
            question_type = result['reasoning_result']['logical_result']['question_type']

            print(f"   Confidence: {confidence:.3f}")
            print(f"   Type: {question_type}")

            results.append({
                'question': question,
                'question_type': question_type,
                'confidence': confidence,
                'graph_nodes': graph_data.num_nodes,
                'graph_edges': graph_data.num_edges,
                'success': True
            })

        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            results.append({
                'question': question,
                'error': str(e),
                'success': False
            })

    return results


def generate_coverage_report(results: List[Dict]) -> Dict:
    """Generate a coverage report based on question answering results."""
    successful_answers = [r for r in results if r.get('success', False)]
    failed_answers = [r for r in results if not r.get('success', False)]

    # Calculate confidence statistics
    if successful_answers:
        confidences = [r['confidence'] for r in successful_answers]
        avg_confidence = np.mean(confidences)
        min_confidence = np.min(confidences)
        max_confidence = np.max(confidences)
    else:
        avg_confidence = min_confidence = max_confidence = 0.0

    # Analyze question types
    question_types = {}
    for result in successful_answers:
        qtype = result.get('question_type', 'unknown')
        question_types[qtype] = question_types.get(qtype, 0) + 1

    report = {
        'total_questions': len(results),
        'successful_answers': len(successful_answers),
        'failed_answers': len(failed_answers),
        'success_rate': len(successful_answers) / len(results) if results else 0,
        'confidence_stats': {
            'average': avg_confidence,
            'minimum': min_confidence,
            'maximum': max_confidence
        },
        'question_type_coverage': question_types,
        'recommendations': []
    }

    # Generate recommendations
    if report['success_rate'] < 0.8:
        report['recommendations'].append("Low success rate indicates knowledge gaps")

    if avg_confidence < 0.7:
        report['recommendations'].append("Low average confidence suggests weak reasoning")

    if len(question_types) < 3:
        report['recommendations'].append("Limited question type coverage")

    return report


def main():
    """Main function to test CI-tagged atrial fibrillation knowledge graph."""
    print("🫀 CI-Tagged Atrial Fibrillation Knowledge Graph BDD Testing")
    print("=" * 65)

    try:
        # Load the CI-tagged knowledge graph
        print("\n📚 Loading knowledge graph...")
        rdf_graph = load_atrial_fibrillation_graph()

        # Analyze graph statistics
        stats = analyze_graph_statistics(rdf_graph)
        print("✓ Graph loaded successfully"        print(f"  - {stats['total_triples']} triples")
        print(f"  - {stats['unique_subjects']} unique subjects")
        print(f"  - {stats['unique_predicates']} unique predicates")
        print(f"  - {stats['unique_objects']} unique objects")
        print(f"  - Top relationships: {list(stats['relationship_types'].keys())[:5]}")

        # Initialize neurosymbolic reasoner
        print("\n🧠 Initializing neurosymbolic reasoner...")
        reasoner = NeurosymbolicClinicalReasoner()
        print("✓ Neurosymbolic reasoner initialized")

        # Convert to PyTorch Geometric format
        print("\n🔄 Converting to graph neural network format...")
        graph_data = reasoner.process_knowledge_graph(rdf_graph)
        print(f"✓ Converted to PyG Data: {graph_data.num_nodes} nodes, {graph_data.num_edges} edges")

        # Create BDD questions
        questions = create_bdd_style_questions()
        print(f"\n❓ Created {len(questions)} BDD-style test questions")

        # Test question answering
        results = test_question_answering(reasoner, graph_data, questions)

        # Generate coverage report
        report = generate_coverage_report(results)

        print("\n📊 COVERAGE REPORT")        print("=" * 30)
        print(f"Questions Tested: {report['total_questions']}")
        print(f"Successful Answers: {report['successful_answers']}")
        print(f"Success Rate: {report['success_rate']:.1%}")
        print(f"Average Confidence: {report['confidence_stats']['average']:.3f}")
        print(f"Question Types Covered: {len(report['question_type_coverage'])}")

        if report['recommendations']:
            print("\n💡 Recommendations:")
            for rec in report['recommendations']:
                print(f"  - {rec}")

        # Business readiness assessment
        print("\n🏢 BUSINESS READINESS ASSESSMENT")
        print("=" * 40)

        success_rate = report['success_rate']
        avg_confidence = report['confidence_stats']['average']

        if success_rate >= 0.8 and avg_confidence >= 0.7:
            readiness = "🟢 MARKET READY"
            message = "Knowledge graph demonstrates strong clinical question answering capability"
        elif success_rate >= 0.6 and avg_confidence >= 0.5:
            readiness = "🟡 NEEDS IMPROVEMENT"
            message = "Knowledge graph shows promise but requires enhancement for production use"
        else:
            readiness = "🔴 NOT MARKET READY"
            message = "Significant gaps in clinical knowledge coverage identified"

        print(f"Status: {readiness}")
        print(f"Assessment: {message}")

        print("\n✅ Testing completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)