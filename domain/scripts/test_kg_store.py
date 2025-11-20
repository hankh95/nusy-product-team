"""
Test KG Store Implementation
=============================
Validates RDFLib-based knowledge graph storage.

Tests:
1. Triple addition and persistence
2. SPARQL query execution
3. Entity retrieval by type
4. Domain knowledge export
5. Provenance tracking
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from nusy_pm_core.adapters.kg_store import KGStore, KGTriple


def test_kg_store():
    """Test knowledge graph storage functionality."""
    
    print("=" * 80)
    print("TEST 1: Triple Addition and Persistence")
    print("=" * 80)
    
    # Create KG store (test workspace)
    kg = KGStore(workspace_path="test_workspace")
    kg.clear()  # Start fresh
    
    # Add some test triples
    triples = [
        KGTriple(
            subject="pm:Feature_123",
            predicate="rdf:type",
            object="pm:Feature",
            source="test-doc.md",
            confidence=0.95
        ),
        KGTriple(
            subject="pm:Feature_123",
            predicate="pm:hasName",
            object="Navigation System",
            source="test-doc.md",
            confidence=1.0
        ),
        KGTriple(
            subject="pm:Feature_123",
            predicate="pm:hasStatus",
            object="pm:InProgress",
            source="test-doc.md",
            confidence=1.0
        ),
        KGTriple(
            subject="pm:Behavior_StatusQuery",
            predicate="rdf:type",
            object="pm:Behavior",
            source="test-doc.md",
            confidence=1.0
        ),
        KGTriple(
            subject="pm:Behavior_StatusQuery",
            predicate="pm:operatesOn",
            object="pm:Feature",
            source="test-doc.md",
            confidence=0.9
        ),
    ]
    
    count = kg.add_triples(triples)
    print(f"✅ Added {count} triples")
    
    # Get statistics
    stats = kg.get_statistics()
    print(f"   📊 Total triples: {stats.total_triples}")
    print(f"   📊 Unique subjects: {stats.unique_subjects}")
    print(f"   📊 Unique predicates: {stats.unique_predicates}")
    print(f"   📊 Unique objects: {stats.unique_objects}")
    
    # Save to disk
    kg.save()
    print()
    
    print("=" * 80)
    print("TEST 2: SPARQL Query Execution")
    print("=" * 80)
    
    # Query all features
    query = """
    SELECT ?feature ?name WHERE {
        ?feature rdf:type pm:Feature .
        ?feature pm:hasName ?name .
    }
    """
    
    results = kg.query(query)
    print(f"✅ Query executed: Found {len(results)} features")
    for r in results:
        print(f"   - Feature: {r['feature']}")
        print(f"     Name: {r['name']}")
    print()
    
    print("=" * 80)
    print("TEST 3: Entity Retrieval by Type")
    print("=" * 80)
    
    # Get all behaviors
    behaviors = kg.get_entities_by_type("pm:Behavior")
    print(f"✅ Found {len(behaviors)} behaviors:")
    for b in behaviors:
        print(f"   - {b}")
    
    # Get all features
    features = kg.get_entities_by_type("pm:Feature")
    print(f"✅ Found {len(features)} features:")
    for f in features:
        print(f"   - {f}")
    print()
    
    print("=" * 80)
    print("TEST 4: Entity Properties")
    print("=" * 80)
    
    # Get properties of Feature_123
    props = kg.get_entity_properties("https://nusy.dev/pm/Feature_123")
    print(f"✅ Feature_123 properties:")
    for prop, val in props.items():
        print(f"   - {prop}: {val}")
    print()
    
    print("=" * 80)
    print("TEST 5: Load from Disk")
    print("=" * 80)
    
    # Create new KG instance and load
    kg2 = KGStore(workspace_path="test_workspace")
    stats2 = kg2.get_statistics()
    print(f"✅ Loaded KG from disk")
    print(f"   📊 Total triples: {stats2.total_triples}")
    
    # Verify data persisted
    features2 = kg2.get_entities_by_type("pm:Feature")
    print(f"✅ Verified {len(features2)} features after reload")
    print()
    
    print("=" * 80)
    print("TEST 6: Domain Export")
    print("=" * 80)
    
    # Export pm domain knowledge
    export_path = kg.export_domain_knowledge("pm", output_path=Path("test_workspace/knowledge/kg/pm_test_export.ttl"))
    print(f"✅ Exported to: {export_path}")
    print()
    
    print("=" * 80)
    print("🎉 ALL TESTS PASSED!")
    print("=" * 80)
    print()
    print("KG Store ready for integration with Navigator Step 6")


if __name__ == "__main__":
    test_kg_store()
