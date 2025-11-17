#!/usr/bin/env python
"""
Multi-Agent Demo: Passage System Feature Implementation

This demo runs a complete multi-agent workflow to design and plan
the Passage System feature from santiago-pm/cargo-manifests/.

Workflow:
1. PM reads feature specification
2. PM creates hypothesis for approach
3. Architect designs the system architecture
4. PM creates development plan
5. All artifacts logged to test_workspace/

This demonstrates:
- Real LLM API calls (GPT-5 and Grok)
- Multi-agent coordination
- MCP tool invocations
- Provenance logging
"""

import asyncio
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

from santiago_core.agents._proxy.pm_proxy import PMProxyAgent
from santiago_core.agents._proxy.architect_proxy import ArchitectProxyAgent


async def read_feature_spec():
    """Read the Passage System feature specification"""
    feature_path = Path("santiago-pm/cargo-manifests/passage-system.feature")
    
    if not feature_path.exists():
        print(f"❌ Feature file not found: {feature_path}")
        return None
    
    with open(feature_path) as f:
        content = f.read()
    
    print(f"📄 Loaded feature: {feature_path}")
    print(f"   Size: {len(content)} chars")
    return content


async def step1_pm_hypothesis(feature_spec: str):
    """Step 1: PM creates hypothesis for implementation approach"""
    print("\n" + "="*70)
    print("STEP 1: PM Creates Implementation Hypothesis")
    print("="*70)
    
    # Initialize PM with workspace
    workspace = Path("test_workspace")
    pm = PMProxyAgent(workspace_path=workspace)
    
    print(f"🤖 PM Agent: {pm.name}")
    print(f"📊 Using model: {pm.llm_router.get_config('pm_proxy').model}")
    print(f"📝 Creating hypothesis for Passage System...")
    
    # Create hypothesis using MCP tool
    result = await pm.invoke_tool(
        tool_name="create_hypothesis",
        params={
            "vision": f"Implement the Passage System for NuSy PM.\n\nFeature Specification:\n{feature_spec[:2000]}...",
            "context": "This is a core system for coordinating multi-step nautical workflows with human and AI agents."
        }
    )
    
    print("\n✅ Hypothesis Created!")
    print(f"   Title: {result.get('hypothesis', {}).get('title', 'N/A')}")
    print(f"   Experiments: {len(result.get('hypothesis', {}).get('experiments', []))}")
    
    return result


async def step2_architect_design(feature_spec: str, hypothesis: dict):
    """Step 2: Architect designs system architecture"""
    print("\n" + "="*70)
    print("STEP 2: Architect Creates System Design")
    print("="*70)
    
    # Initialize Architect with workspace
    workspace = Path("test_workspace")
    architect = ArchitectProxyAgent(workspace_path=workspace)
    
    print(f"🏗️  Architect Agent: {architect.name}")
    print(f"📊 Using model: {architect.llm_router.get_config('architect_proxy').model}")
    print(f"🎨 Designing architecture for Passage System...")
    
    # Create design using MCP tool
    requirements = f"""
Feature: Passage System Implementation

{feature_spec[:1500]}

PM Hypothesis:
{json.dumps(hypothesis.get('hypothesis', {}), indent=2)[:500]}
"""
    
    result = await architect.invoke_tool(
        tool_name="create_design",
        params={
            "requirements": requirements,
            "constraints": "Must integrate with MCP endpoints, knowledge graph, and support YAML passage definitions"
        }
    )
    
    print("\n✅ Architecture Design Created!")
    design = result.get('design', {})
    print(f"   Title: {design.get('title', 'N/A')}")
    print(f"   Components: {len(design.get('components', []))}")
    print(f"   Diagrams: {len(design.get('diagrams', []))}")
    
    # Show first diagram if available
    diagrams = design.get('diagrams', [])
    if diagrams and isinstance(diagrams, list):
        first_diagram = diagrams[0]
        if isinstance(first_diagram, dict):
            print(f"\n   First Diagram: {first_diagram.get('type', 'Unknown')}")
            content = first_diagram.get('content', '')
            if content:
                print(f"   Preview: {content[:200]}...")
    
    return result


async def step3_pm_development_plan(hypothesis: dict, design: dict):
    """Step 3: PM creates user story map based on design"""
    print("\n" + "="*70)
    print("STEP 3: PM Creates User Story Map")
    print("="*70)
    
    # Initialize PM
    workspace = Path("test_workspace")
    pm = PMProxyAgent(workspace_path=workspace)
    
    print(f"🤖 PM Agent: {pm.name}")
    print(f"📋 Creating user story map...")
    
    # Create story map
    feature_summary = f"""
Passage System Implementation

Hypothesis: {json.dumps(hypothesis.get('hypothesis', {}), indent=2)[:300]}...

Architecture: {json.dumps(design.get('design', {}), indent=2)[:300]}...
"""
    
    result = await pm.invoke_tool(
        tool_name="create_story_map",
        params={
            "feature": feature_summary
        }
    )
    
    print("\n✅ User Story Map Created!")
    story_map = result.get('story_map', {})
    print(f"   Feature: Passage System")
    print(f"   User Journeys: {len(story_map.get('user_journeys', []))}")
    
    # Show journeys
    journeys = story_map.get('user_journeys', [])
    if journeys:
        print(f"\n   User Journeys:")
        for i, journey in enumerate(journeys[:3], 1):
            if isinstance(journey, dict):
                print(f"     {i}. {journey.get('name', 'Unknown')}: {len(journey.get('stories', []))} stories")
    
    return result


async def main():
    """Run the complete multi-agent workflow"""
    print("\n" + "🚢"*35)
    print("NuSy Proxy Team Demo: Passage System Implementation")
    print("🚢"*35)
    
    # Read feature specification
    feature_spec = await read_feature_spec()
    if not feature_spec:
        return
    
    try:
        # Step 1: PM creates hypothesis
        hypothesis_result = await step1_pm_hypothesis(feature_spec)
        
        # Step 2: Architect designs system
        design_result = await step2_architect_design(feature_spec, hypothesis_result)
        
        # Step 3: PM creates user story map
        plan_result = await step3_pm_development_plan(hypothesis_result, design_result)
        
        # Summary
        print("\n" + "="*70)
        print("🎉 DEMO COMPLETE!")
        print("="*70)
        print("\nArtifacts Created:")
        print("  ✅ PM Hypothesis (using gpt-5.1)")
        print("  ✅ System Architecture (using grok-4-fast)")
        print("  ✅ User Story Map (using gpt-5.1)")
        
        workspace = Path("test_workspace/ships-logs")
        if workspace.exists():
            pm_logs = list(workspace.glob("pm_proxy/*.md"))
            arch_logs = list(workspace.glob("architect_proxy/*.md"))
            print(f"\nProvenance Logs:")
            print(f"  📝 PM logs: {len(pm_logs)} entries")
            print(f"  🏗️  Architect logs: {len(arch_logs)} entries")
            print(f"  📂 Location: {workspace}")
        
        print("\nModels Used:")
        print("  • PM (moderate): gpt-5.1 ($1.25/$10 per 1M tokens)")
        print("  • Architect (complex): grok-4-fast ($0.20/$0.50 per 1M tokens)")
        print("  • Total API calls: 3")
        
        print("\nNext Steps:")
        print("  • Review logs in test_workspace/ships-logs/")
        print("  • Examine architecture diagrams in architect logs")
        print("  • Use story map to implement feature")
        print("  • Try with other features from cargo-manifests/")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
