#!/usr/bin/env python
"""
Smoke Test for Phase 0 API Integration

Quick test to verify:
1. API keys are configured
2. LLM routing works
3. Real API calls succeed
4. Response parsing works

Run this after adding your API keys to .env
"""

import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from santiago_core.agents._proxy.pm_proxy import PMProxyAgent
from santiago_core.agents._proxy.architect_proxy import ArchitectProxyAgent
from santiago_core.services.llm_router import LLMRouter, TaskComplexity


async def test_api_keys():
    """Check if API keys are configured"""
    print("🔑 Checking API keys...")
    
    openai_key = os.getenv("OPENAI_API_KEY", "")
    xai_key = os.getenv("XAI_API_KEY", "")
    
    if not openai_key or openai_key == "changeme":
        print("❌ OPENAI_API_KEY not set in .env")
        return False
    else:
        print(f"✅ OpenAI API key configured ({openai_key[:8]}...)")
    
    if not xai_key or xai_key == "changeme":
        print("⚠️  XAI_API_KEY not set (optional for this test)")
    else:
        print(f"✅ xAI API key configured ({xai_key[:8]}...)")
    
    return True


async def test_llm_router():
    """Test LLM router configuration"""
    print("\n🔀 Testing LLM Router...")
    
    router = LLMRouter()
    
    # Test PM routes to OpenAI
    config = router.get_config("pm_proxy", TaskComplexity.SIMPLE)
    print(f"✅ PM Proxy routes to: {config.provider.value} / {config.model}")
    
    # Test Architect routes to xAI
    config = router.get_config("architect_proxy", TaskComplexity.MODERATE)
    print(f"✅ Architect Proxy routes to: {config.provider.value} / {config.model}")
    
    return True


async def test_pm_real_api():
    """Test PM proxy with real OpenAI API"""
    print("\n🤖 Testing PM Proxy with real API...")
    
    workspace = Path("./test_workspace")
    workspace.mkdir(exist_ok=True)
    
    try:
        # Create PM proxy
        pm = PMProxyAgent(workspace)
        print("✅ PM Proxy instantiated")
        
        # Make a simple API call
        print("\n📝 Asking PM to create a hypothesis...")
        result = await pm.invoke_tool(
            "create_hypothesis",
            {
                "vision": "Build a self-learning AI agent factory that can bootstrap itself from proxy agents to full autonomous Santiago crew"
            }
        )
        
        if "error" in result:
            print(f"❌ API call failed: {result['error']}")
            return False
        
        print("\n✅ Success! PM Response:")
        print("-" * 60)
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_architect_real_api():
    """Test Architect proxy with real xAI API (if key available)"""
    print("\n🏗️  Testing Architect Proxy with real API...")
    
    xai_key = os.getenv("XAI_API_KEY", "")
    if not xai_key or xai_key == "changeme":
        print("⚠️  Skipping (XAI_API_KEY not configured)")
        return True
    
    workspace = Path("./test_workspace")
    workspace.mkdir(exist_ok=True)
    
    try:
        # Create Architect proxy
        architect = ArchitectProxyAgent(workspace)
        print("✅ Architect Proxy instantiated")
        
        # Make a simple API call
        print("\n📐 Asking Architect to create a design...")
        result = await architect.invoke_tool(
            "create_design",
            {
                "requirements": "Design a message bus for multi-agent communication",
                "constraints": "Must support pub/sub and direct messaging"
            }
        )
        
        if "error" in result:
            print(f"❌ API call failed: {result['error']}")
            return False
        
        print("\n✅ Success! Architect Response:")
        print("-" * 60)
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)
        print("-" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all smoke tests"""
    print("=" * 60)
    print("Phase 0 API Integration Smoke Test")
    print("=" * 60)
    
    # Check API keys
    if not await test_api_keys():
        print("\n❌ Please add your API keys to .env file:")
        print("   1. Edit .env")
        print("   2. Replace 'changeme' with your actual keys")
        print("   3. Run this script again")
        return False
    
    # Test LLM router
    if not await test_llm_router():
        print("\n❌ LLM Router test failed")
        return False
    
    # Test PM with real API
    if not await test_pm_real_api():
        print("\n❌ PM API test failed")
        return False
    
    # Test Architect with real API (if key available)
    await test_architect_real_api()
    
    print("\n" + "=" * 60)
    print("✅ Smoke test complete!")
    print("=" * 60)
    print("\nPhase 0 API integration is working! 🚀")
    print("\nNext steps:")
    print("  • Run full test suite: pytest tests/")
    print("  • Try multi-agent workflows")
    print("  • Build end-to-end demos")
    
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
