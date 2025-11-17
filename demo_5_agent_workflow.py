#!/usr/bin/env python
"""
5-Agent Workflow Demo

Full software development lifecycle with 5 agents:
1. PM: Creates hypothesis and feature spec
2. Architect: Designs system architecture  
3. Developer: Implements the feature
4. QA: Tests and validates
5. UX: Provides user experience feedback

This demonstrates:
- Complete feature workflow
- Multi-agent coordination
- Real LLM API calls (GPT-5 + Grok)
- Different complexity levels
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
from santiago_core.agents._proxy.developer_proxy import DeveloperProxyAgent
from santiago_core.agents._proxy.qa_proxy import QAProxyAgent
from santiago_core.agents._proxy.ux_proxy import UXProxyAgent


async def step1_pm_creates_hypothesis():
    """Step 1: PM analyzes user needs and creates hypothesis"""
    print("\n" + "="*70)
    print("STEP 1: PM Creates Product Hypothesis")
    print("="*70)
    
    workspace = Path("test_workspace")
    pm = PMProxyAgent(workspace_path=workspace)
    
    print(f"🤖 Agent: {pm.name}")
    print(f"📊 Model: {pm.llm_router.get_config('pm_proxy').model}")
    
    result = await pm.invoke_tool(
        tool_name="create_hypothesis",
        params={
            "vision": """
User Need: Development teams struggle with agent coordination
Problem: Manual orchestration is error-prone and slow
Opportunity: Automated multi-agent workflows with Redis pub/sub
            """,
            "context": "Building on successful Passage System demo"
        }
    )
    
    hypothesis = result.get('hypothesis', {})
    print(f"\n✅ Hypothesis Created:")
    print(f"   Title: {hypothesis.get('title', 'N/A')}")
    print(f"   Experiments: {len(hypothesis.get('experiments', []))}")
    
    return result


async def step2_architect_designs_system(hypothesis: dict):
    """Step 2: Architect designs the technical solution"""
    print("\n" + "="*70)
    print("STEP 2: Architect Designs System Architecture")
    print("="*70)
    
    workspace = Path("test_workspace")
    architect = ArchitectProxyAgent(workspace_path=workspace)
    
    print(f"🏗️  Agent: {architect.name}")
    print(f"📊 Model: {architect.llm_router.get_config('architect_proxy').model}")
    
    requirements = f"""
Feature: Multi-Agent Workflow Orchestration

Hypothesis:
{json.dumps(hypothesis.get('hypothesis', {}), indent=2)[:500]}

Requirements:
- Async coordination between 5+ agents
- Redis pub/sub for messaging
- Tool-based MCP interface
- Provenance logging
- Budget tracking
"""
    
    result = await architect.invoke_tool(
        tool_name="create_design",
        params={
            "requirements": requirements,
            "constraints": "Must integrate with existing proxy framework and LLM router"
        }
    )
    
    design = result.get('design', {})
    print(f"\n✅ Architecture Design Created:")
    print(f"   Title: {design.get('title', 'N/A')}")
    print(f"   Components: {len(design.get('components', []))}")
    
    return result


async def step3_developer_implements(hypothesis: dict, design: dict):
    """Step 3: Developer implements the feature"""
    print("\n" + "="*70)
    print("STEP 3: Developer Implements Feature")
    print("="*70)
    
    workspace = Path("test_workspace")
    developer = DeveloperProxyAgent(workspace_path=workspace)
    
    print(f"💻 Agent: {developer.name}")
    print(f"📊 Model: {developer.llm_router.get_config('developer_proxy').model}")
    
    spec = f"""
Implementation Request

Hypothesis: {json.dumps(hypothesis.get('hypothesis', {}), indent=2)[:300]}

Architecture: {json.dumps(design.get('design', {}), indent=2)[:300]}

Tasks:
1. Implement message routing
2. Add agent coordination layer
3. Create test suite
4. Document API
"""
    
    result = await developer.invoke_tool(
        tool_name="write_code",
        params={
            "feature": "multi-agent-orchestration",
            "code": spec,
            "tests": "Full BDD test coverage required"
        }
    )
    
    implementation = result.get('implementation', {})
    print(f"\n✅ Implementation Complete:")
    print(f"   Test Coverage: {implementation.get('coverage', 'N/A')}%")
    print(f"   Files: {len(implementation.get('files_modified', []))}")
    
    return result


async def step4_qa_validates(implementation: dict):
    """Step 4: QA validates the implementation"""
    print("\n" + "="*70)
    print("STEP 4: QA Validates Implementation")
    print("="*70)
    
    workspace = Path("test_workspace")
    qa = QAProxyAgent(workspace_path=workspace)
    
    print(f"🔍 Agent: {qa.name}")
    print(f"📊 Model: {qa.llm_router.get_config('qa_proxy').model}")
    
    result = await qa.invoke_tool(
        tool_name="run_tests",
        params={
            "test_path": "tests/integration/multi_agent_workflow_test.py",
            "coverage": True
        }
    )
    
    test_results = result.get('test_results', {})
    print(f"\n✅ Test Results:")
    print(f"   Passed: {test_results.get('passed', 0)}")
    print(f"   Failed: {test_results.get('failed', 0)}")
    print(f"   Coverage: {test_results.get('coverage', 0)}%")
    
    return result


async def step5_ux_evaluates(hypothesis: dict, implementation: dict):
    """Step 5: UX evaluates user experience"""
    print("\n" + "="*70)
    print("STEP 5: UX Evaluates User Experience")
    print("="*70)
    
    workspace = Path("test_workspace")
    ux = UXProxyAgent(workspace_path=workspace)
    
    print(f"🎨 Agent: {ux.name}")
    print(f"📊 Model: {ux.llm_router.get_config('ux_proxy').model}")
    
    eval_context = f"""
Feature: Multi-Agent Workflow Orchestration

Original Hypothesis:
{json.dumps(hypothesis.get('hypothesis', {}), indent=2)[:200]}

Implementation Status:
{json.dumps(implementation.get('implementation', {}), indent=2)[:200]}

Evaluate developer experience, coordination clarity, error handling, and documentation.
"""
    
    result = await ux.invoke_tool(
        tool_name="test_usability",
        params={
            "prototype": "multi-agent-orchestration",
            "participants": 5
        }
    )
    
    evaluation = result.get('usability', {})
    print(f"\n✅ Usability Test Complete:")
    print(f"   Success Rate: {evaluation.get('success_rate', 'N/A')}")
    print(f"   Issues Found: {len(evaluation.get('issues', []))}")
    
    return result


async def main():
    """Run complete 5-agent workflow"""
    print("\n" + "🚀"*35)
    print("5-Agent Software Development Workflow")
    print("🚀"*35)
    
    try:
        # Execute workflow
        hypothesis_result = await step1_pm_creates_hypothesis()
        design_result = await step2_architect_designs_system(hypothesis_result)
        impl_result = await step3_developer_implements(hypothesis_result, design_result)
        test_result = await step4_qa_validates(impl_result)
        ux_result = await step5_ux_evaluates(hypothesis_result, impl_result)
        
        # Summary
        print("\n" + "="*70)
        print("🎉 5-AGENT WORKFLOW COMPLETE!")
        print("="*70)
        
        print("\nAgent Contributions:")
        print("  1. ✅ PM: Product hypothesis and vision")
        print("  2. ✅ Architect: System design with components")
        print("  3. ✅ Developer: Implementation with tests")
        print("  4. ✅ QA: Test validation and coverage")
        print("  5. ✅ UX: User experience evaluation")
        
        print("\nModels Used:")
        print("  • PM (moderate): gpt-5.1")
        print("  • Architect (complex): grok-4-fast")
        print("  • Developer (moderate): gpt-5.1")
        print("  • QA (moderate): gpt-5.1")
        print("  • UX (moderate): gpt-5.1")
        
        print("\nProvenance Logs:")
        workspace = Path("test_workspace/ships-logs")
        if workspace.exists():
            for role in ["pm", "architect", "developer", "qa", "ux"]:
                role_dir = workspace / role
                if role_dir.exists():
                    logs = list(role_dir.glob("*.jsonl"))
                    print(f"  📝 {role}: {len(logs)} log files")
        
        print("\nNext Steps:")
        print("  • Review detailed logs in test_workspace/ships-logs/")
        print("  • Examine architecture diagrams")
        print("  • Run actual tests on implementation")
        print("  • Iterate based on UX feedback")
        print("  • Add Redis message bus for real-time coordination")
        
    except Exception as e:
        print(f"\n❌ Workflow failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
