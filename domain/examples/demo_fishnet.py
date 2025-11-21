"""
Fishnet Demo - BDD Test + MCP Manifest Generation

Demonstrates Fishnet generating behavior-driven tests and service manifests:
1. BDD .feature files with Gherkin scenarios
2. MCP manifest.json with service contract
3. Coverage analysis with gap detection

Shows:
- 3 scenarios per behavior (happy path, edge case, error)
- Capability levels (Apprentice/Journeyman/Master/Expert)
- Knowledge scope (Pond/Lake/Sea/Ocean)
- Concurrency risk detection
- Contract test generation
"""

import asyncio
from pathlib import Path

from domain.nusy_orchestrator.santiago_builder.fishnet import (
    Fishnet,
    CapabilityLevel,
    KnowledgeScope,
)


async def main():
    """Run Fishnet demonstration"""
    
    print("="*80)
    print("      Fishnet BDD Test + MCP Manifest Generation Demo")
    print("="*80)
    
    # Initialize Fishnet
    workspace_path = Path(__file__).parent
    fishnet = Fishnet(workspace_path=workspace_path)
    
    # Define domain and behaviors
    domain_name = "santiago-pm-safe-xp"
    behaviors = [
        "create_backlog",
        "prioritize_stories",
        "define_acceptance_criteria",
        "plan_iteration",
        "track_velocity",
    ]
    
    # Mock entities and relationships (from Catchfish)
    entities = [
        {"name": "Backlog", "type": "concept"},
        {"name": "User Story", "type": "concept"},
        {"name": "Acceptance Criteria", "type": "concept"},
        {"name": "Iteration", "type": "concept"},
        {"name": "Velocity", "type": "metric"},
    ]
    
    relationships = [
        {"subject": "Backlog", "predicate": "contains", "object": "User Story"},
        {"subject": "User Story", "predicate": "has", "object": "Acceptance Criteria"},
        {"subject": "Iteration", "predicate": "tracks", "object": "Velocity"},
    ]
    
    print(f"\n📚 Generating Tests and Manifests For:")
    print(f"   Domain: {domain_name}")
    print(f"   Behaviors: {len(behaviors)}")
    print(f"   Entities: {len(entities)}")
    print(f"   Relationships: {len(relationships)}\n")
    
    try:
        # Step 1: Generate BDD features
        print("Step 1: Generating BDD Features")
        features = await fishnet.generate_bdd_features(
            domain_name=domain_name,
            behaviors=behaviors,
            entities=entities,
            relationships=relationships,
        )
        
        # Step 2: Generate MCP manifest
        print("\nStep 2: Generating MCP Manifest")
        manifest = await fishnet.generate_mcp_manifest(
            domain_name=domain_name,
            behaviors=behaviors,
            capability_level=CapabilityLevel.JOURNEYMAN,
            knowledge_scope=KnowledgeScope.LAKE,
            entities=entities,
        )
        
        # Step 3: Analyze coverage
        print("\nStep 3: Analyzing Coverage")
        coverage = await fishnet.analyze_coverage(
            domain_name=domain_name,
            behaviors=behaviors,
            features=features,
        )
        
        # Print results
        print("\n" + "="*80)
        print("                        Results")
        print("="*80)
        
        # BDD Features
        print(f"\n📝 BDD Features Generated: {len(features)}")
        for feature in features:
            print(f"\n   Feature: {feature.name}")
            print(f"   Scenarios: {len(feature.scenarios)}")
            for scenario in feature.scenarios:
                print(f"      • {scenario.name}")
                print(f"        Given: {len(scenario.given_steps)} steps")
                print(f"        When: {len(scenario.when_steps)} steps")
                print(f"        Then: {len(scenario.then_steps)} steps")
        
        # Feature files
        catch_dir = workspace_path / "knowledge" / "catches" / domain_name / "bdd-tests"
        if catch_dir.exists():
            feature_files = list(catch_dir.glob("*.feature"))
            print(f"\n   ✅ Feature Files Created: {len(feature_files)}")
            for f in feature_files[:3]:  # Show first 3
                print(f"      📄 {f.name}")
        
        # MCP Manifest
        print(f"\n📦 MCP Manifest:")
        print(f"   Service: {manifest.service_name} v{manifest.version}")
        print(f"   Capability: {manifest.capability_level.value}")
        print(f"   Knowledge Scope: {manifest.knowledge_scope.value}")
        print(f"   Tools: {len(manifest.tools)}")
        
        for tool in manifest.tools:
            concurrency = "⚠️" if tool.concurrency_risk else "✅"
            print(f"      {concurrency} {tool.name} ({tool.tool_type})")
            if tool.mutates_kg:
                print(f"         • Mutates KG")
        
        manifest_file = workspace_path / "knowledge" / "catches" / domain_name / "mcp-manifest.json"
        if manifest_file.exists():
            print(f"\n   ✅ Manifest Saved: {manifest_file}")
        
        # Coverage Report
        print(f"\n📊 Coverage Analysis:")
        print(f"   Total Behaviors: {coverage.total_behaviors}")
        print(f"   Behaviors with Tests: {coverage.behaviors_with_tests}")
        print(f"   Total Scenarios: {coverage.total_scenarios}")
        print(f"   Coverage Ratio: {coverage.coverage_ratio * 100:.1f}%")
        
        if coverage.gaps:
            print(f"\n   ⚠️  Gaps Found: {len(coverage.gaps)}")
            for gap in coverage.gaps:
                print(f"      • {gap}")
        
        if coverage.recommendations:
            print(f"\n   💡 Recommendations:")
            for rec in coverage.recommendations:
                print(f"      • {rec}")
        
        # Sample feature file content
        if feature_files:
            sample_file = feature_files[0]
            print(f"\n📄 Sample Feature File: {sample_file.name}")
            print("   " + "-"*76)
            with open(sample_file, 'r') as f:
                content = f.read()
            lines = content.split('\n')[:20]  # First 20 lines
            for line in lines:
                print(f"   {line}")
            if len(content.split('\n')) > 20:
                print("   ...")
        
        print("\n" + "="*80)
        print("                🎉 Generation Complete! 🎉")
        print("="*80)
        
    except Exception as e:
        print(f"\n❌ Generation failed: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(main())
