#!/usr/bin/env python3
"""
Test Santiago Agent Integration with Mistral-7B
Run this to validate agent role simulation
"""

import asyncio
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

API_URL = "http://localhost:8001/v1/chat/completions"
API_KEY = "nusy-dgx-2025"

SANTIAGO_ROLES = {
    "Product Manager": "You are a Product Manager in an autonomous AI development team. Focus on strategy, prioritization, and stakeholder management.",
    "Architect": "You are a Systems Architect designing scalable AI infrastructure. Focus on technical design, patterns, and system integration.",
    "Developer": "You are a Software Developer implementing features and fixing bugs. Focus on code quality, testing, and best practices.",
    "QA Specialist": "You are a QA Specialist ensuring software quality. Focus on testing, validation, and defect prevention.",
    "UX Researcher": "You are a UX Researcher studying user needs and interface design. Focus on user experience and usability."
}

def create_agent_prompt(role: str, task: str) -> str:
    """Create a role-specific prompt for Santiago agent"""
    system_prompt = SANTIAGO_ROLES[role]
    return f"{system_prompt}\\n\\nTask: {task}\\n\\nProvide a detailed response as a {role.lower()} would."

def test_single_agent(role: str, task: str) -> dict:
    """Test a single Santiago agent interaction"""
    prompt = create_agent_prompt(role, task)

    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.7
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    start_time = time.time()
    try:
        response = requests.post(API_URL, headers=headers, json=data, timeout=60)
        end_time = time.time()

        if response.status_code == 200:
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            return {
                "role": role,
                "success": True,
                "latency": end_time - start_time,
                "response_length": len(content),
                "content_preview": content[:200] + "..." if len(content) > 200 else content,
                "tokens_used": result.get("usage", {}).get("total_tokens", 0)
            }
        else:
            return {
                "role": role,
                "success": False,
                "error": f"HTTP {response.status_code}: {response.text}",
                "latency": end_time - start_time
            }
    except Exception as e:
        end_time = time.time()
        return {
            "role": role,
            "success": False,
            "error": str(e),
            "latency": end_time - start_time
        }

async def test_multi_agent_simulation():
    """Test multiple Santiago agents working concurrently"""
    print("🎭 Testing Santiago Multi-Agent Simulation")
    print("=" * 50)

    # Define test scenarios for each role
    test_scenarios = {
        "Product Manager": "Design a product roadmap for implementing AI-powered code review in a development team",
        "Architect": "Design the system architecture for a multi-agent AI development platform",
        "Developer": "Implement a REST API endpoint for user authentication with JWT tokens",
        "QA Specialist": "Create a comprehensive testing strategy for an AI-powered application",
        "UX Researcher": "Analyze user needs for an AI-assisted coding environment"
    }

    print("\\n🚀 Testing individual agents...")
    results = []
    for role, task in test_scenarios.items():
        print(f"🤖 Testing {role}...")
        result = test_single_agent(role, task)
        results.append(result)

        if result["success"]:
            print(f"✅ {role}: {result['latency']:.2f}s, {result['response_length']} chars")
        else:
            print(f"❌ Failed: {result['error']}")

    print("\\n\\n🔄 Testing concurrent multi-agent execution...")
    start_time = time.time()

    # Test concurrent execution
    with ThreadPoolExecutor(max_workers=5) as executor:
        concurrent_results = list(executor.map(
            lambda item: test_single_agent(item[0], item[1]),
            test_scenarios.items()
        ))

    end_time = time.time()

    successful = sum(1 for r in concurrent_results if r["success"])
    total_time = end_time - start_time

    print("\\n📊 Concurrent Test Results:")
    print(f"Total agents: {len(concurrent_results)}")
    print(f"Successful: {successful}")
    print(f"Success rate: {successful/len(concurrent_results)*100:.1f}%")
    print(f"Total time: {total_time:.2f}s")
    print(f"Time per agent: {total_time/len(concurrent_results):.2f}s")

    # Detailed results
    print("\\n📋 Detailed Results:")
    for result in concurrent_results:
        status = "✅" if result["success"] else "❌"
        latency = f"{result['latency']:.2f}s" if result["success"] else "N/A"
        tokens = result.get("tokens_used", "N/A")
        print(f"  {status} {result['role']}: {latency}, {tokens} tokens")

    # Save results
    test_results = {
        "timestamp": time.time(),
        "individual_tests": results,
        "concurrent_test": {
            "results": concurrent_results,
            "total_time": total_time,
            "success_rate": successful/len(concurrent_results)
        }
    }

    with open(f"santiago_agent_test_{int(time.time())}.json", "w") as f:
        json.dump(test_results, f, indent=2)

    print(f"\\n📄 Results saved to santiago_agent_test_{int(time.time())}.json")

    if successful == len(concurrent_results):
        print("\\n🎉 All Santiago agent tests passed! Ready for production integration.")
    else:
        print(f"\\n⚠️  {len(concurrent_results) - successful} agent tests failed. Check configuration.")

    return test_results

if __name__ == "__main__":
    asyncio.run(test_multi_agent_simulation())