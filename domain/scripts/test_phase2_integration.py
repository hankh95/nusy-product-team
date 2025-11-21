#!/usr/bin/env python3
"""
Test Phase 2 Integration: Navigator + Catchfish + Fishnet

Tests end-to-end fishing expedition on a small test domain.
Validates all components work together before running full santiago-pm expedition.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from domain.nusy_orchestrator.santiago_builder.navigator import Navigator
from domain.nusy_orchestrator.santiago_builder.catchfish import Catchfish
from domain.nusy_orchestrator.santiago_builder.fishnet import Fishnet


async def test_catchfish_basic():
    """Test Catchfish extraction on a single file"""
    print("\n" + "=" * 80)
    print("TEST 1: Catchfish Basic Extraction")
    print("=" * 80)
    
    catchfish = Catchfish(workspace_path=project_root)
    
    # Test with a small known file
    test_file = project_root / "README.md"
    if not test_file.exists():
        print(f"❌ Test file not found: {test_file}")
        return False
    
    try:
        results = await catchfish.extract_from_source(test_file)
        print(f"✅ Catchfish extracted {len(results)} layers from {test_file.name}")
        return True
    except Exception as e:
        print(f"❌ Catchfish failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_fishnet_basic():
    """Test Fishnet BDD generation"""
    print("\n" + "=" * 80)
    print("TEST 2: Fishnet BDD Generation")
    print("=" * 80)
    
    fishnet = Fishnet(workspace_path=project_root)
    
    # Test with sample behaviors and mock entities/relationships
    test_behaviors = ["create_test_feature", "update_test_feature"]
    test_entities = []  # Mock entities from Catchfish
    test_relationships = []  # Mock relationships from Catchfish
    
    try:
        features = await fishnet.generate_bdd_features(
            domain_name="test-domain",
            behaviors=test_behaviors,
            entities=test_entities,
            relationships=test_relationships
        )
        print(f"✅ Fishnet generated {len(features)} BDD features")
        return True
    except Exception as e:
        print(f"❌ Fishnet failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_navigator_mini_expedition():
    """Test Navigator with minimal expedition"""
    print("\n" + "=" * 80)
    print("TEST 3: Navigator Mini Expedition")
    print("=" * 80)
    
    navigator = Navigator(workspace_path=project_root)
    
    # Create test sources
    test_sources = [
        project_root / "README.md"
    ]
    
    test_behaviors = ["test_behavior_1", "test_behavior_2"]
    
    try:
        expedition = await navigator.run_expedition(
            domain_name="test-mini",
            sources=test_sources,
            target_behaviors=test_behaviors
        )
        
        print(f"✅ Navigator completed expedition: {expedition.expedition_id}")
        print(f"   Status: {expedition.status}")
        print(f"   Cycles: {len(expedition.cycles)}")
        print(f"   Final metrics: {expedition.final_metrics}")
        return True
    except Exception as e:
        print(f"❌ Navigator failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all integration tests"""
    print("\n" + "=" * 80)
    print("PHASE 2 INTEGRATION TEST SUITE")
    print("=" * 80)
    print(f"Project Root: {project_root}")
    
    results = []
    
    # Test 1: Catchfish
    test1_pass = await test_catchfish_basic()
    results.append(("Catchfish Basic", test1_pass))
    
    # Test 2: Fishnet
    test2_pass = await test_fishnet_basic()
    results.append(("Fishnet BDD Generation", test2_pass))
    
    # Test 3: Navigator (only if 1 & 2 pass)
    if test1_pass and test2_pass:
        test3_pass = await test_navigator_mini_expedition()
        results.append(("Navigator Mini Expedition", test3_pass))
    else:
        print("\n⚠️  Skipping Navigator test (dependencies failed)")
        results.append(("Navigator Mini Expedition", False))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(passed for _, passed in results)
    
    if all_passed:
        print("\n🎉 All tests passed! Phase 2 integration ready.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Review errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
