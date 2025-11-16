#!/usr/bin/env python3
"""
NuSy Prototype Verification Script
Tests installation and basic functionality of the Neurosymbolic Clinical Reasoner
"""

import sys
import os
import json
from pathlib import Path

def test_imports():
    """Test core and optional imports"""
    print("Testing imports...")

    # Core imports (required)
    try:
        import rdflib
        print(f"✓ rdflib {rdflib.__version__} - Core RDF processing")
    except ImportError as e:
        print(f"✗ rdflib import failed: {e}")
        return False

    # Optional imports
    optional_modules = [
        ('SPARQLWrapper', 'Advanced SPARQL queries'),
        ('networkx', 'Graph algorithms'),
        ('sklearn', 'Machine learning'),
        ('transformers', 'Neural language models'),
        ('torch', 'PyTorch neural networks'),
        ('fastapi', 'Web API framework'),
        ('pytest', 'Testing framework'),
    ]

    for module, description in optional_modules:
        try:
            __import__(module)
            print(f"✓ {module} - {description}")
        except ImportError:
            print(f"⚠ {module} not available - {description}")

    return True

def test_basic_functionality():
    """Test basic RDFLib functionality"""
    print("\nTesting basic functionality...")

    try:
        import rdflib

        # Test graph creation
        g = rdflib.Graph()
        print("✓ RDFLib graph creation")

        # Test namespace handling
        from rdflib import Namespace
        ex = Namespace("http://example.org/")
        print("✓ Namespace handling")

        # Test triple addition
        g.add((ex.subject, ex.predicate, ex.object))
        assert len(g) == 1
        print("✓ Triple operations")

        # Test JSON-LD parsing capability
        test_jsonld = {
            "@context": {"@vocab": "http://example.org/"},
            "@id": "test",
            "label": "Test Resource"
        }

        # Convert to JSON string and parse
        import json
        json_str = json.dumps(test_jsonld)
        g2 = rdflib.Graph()
        g2.parse(data=json_str, format='json-ld')
        print("✓ JSON-LD parsing")

        return True

    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def test_nusy_prototype():
    """Test NuSy prototype functionality"""
    print("\nTesting NuSy prototype...")

    try:
        # Import prototype modules
        sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

        from neurosymbolic_prototype import NeurosymbolicClinicalReasoner, load_ci_tagged_graph
        print("✓ NuSy prototype imports")

        # Test reasoner initialization
        reasoner = NeurosymbolicClinicalReasoner()
        print("✓ NeurosymbolicClinicalReasoner initialization")

        # Test keyword extraction
        question = "What are the symptoms of ischemic stroke?"
        keywords = reasoner._extract_keywords(question)
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        print(f"✓ Keyword extraction: {keywords}")

        # Test with sample data
        sample_graph_data = {
            "@context": {
                "@vocab": "http://example.org/",
                "rdfs": "http://www.w3.org/2000/01/rdf-schema#"
            },
            "@graph": [
                {
                    "@id": "stroke",
                    "@type": "MedicalCondition",
                    "rdfs:label": "Ischemic Stroke",
                    "hasSymptom": {"@id": "headache"}
                },
                {
                    "@id": "headache",
                    "@type": "Symptom",
                    "rdfs:label": "Headache"
                }
            ]
        }

        import rdflib
        g = rdflib.Graph()
        g.parse(data=json.dumps(sample_graph_data), format='json-ld')
        print("✓ Sample knowledge graph creation")

        # Test querying
        result = reasoner.query_graph(question, g)
        assert result is not None
        assert 'entities' in result
        assert 'triples' in result
        print(f"✓ Query execution: {result['triples']} triples found")

        return True

    except ImportError as e:
        print(f"✗ NuSy prototype import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ NuSy prototype test failed: {e}")
        return False

def main():
    """Main verification function"""
    print("NuSy Prototype Verification")
    print("=" * 50)
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print()

    # Run tests
    tests = [
        ("Import Tests", test_imports),
        ("Basic Functionality", test_basic_functionality),
        ("NuSy Prototype", test_nusy_prototype),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}")
        print("-" * len(test_name))
        success = test_func()
        results.append((test_name, success))

    # Summary
    print("\n" + "=" * 50)
    print("VERIFICATION SUMMARY")
    print("=" * 50)

    all_passed = True
    for test_name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name}")
        if not success:
            all_passed = False

    print()
    if all_passed:
        print("🎉 All tests passed! NuSy prototype is ready to use.")
        print("\nNext steps:")
        print("1. Review the technical summary: research/neurosymbolic-clinical-reasoner-technical-summary.md")
        print("2. Check the setup guide: research/nusy-setup-guide.md")
        print("3. Run example queries with your knowledge graphs")
        return 0
    else:
        print("❌ Some tests failed. Please check the installation.")
        print("\nTroubleshooting:")
        print("1. Ensure all requirements are installed: pip install -r research/requirements-nusy.txt")
        print("2. Check Python version (3.7+ required)")
        print("3. Verify neurosymbolic_prototype.py is in the correct location")
        return 1

if __name__ == "__main__":
    sys.exit(main())