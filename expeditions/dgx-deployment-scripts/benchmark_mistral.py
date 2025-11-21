#!/usr/bin/env python3
"""
Mistral-7B Performance Benchmark for DGX
Run this after deployment to validate performance
"""

import time
import requests
import json
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List
import argparse

class MistralBenchmark:
    def __init__(self, api_url: str = "http://localhost:8001", api_key: str = "nusy-dgx-2025"):
        self.api_url = f"{api_url}/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.1"

    def single_request(self, prompt: str, max_tokens: int = 100) -> Dict:
        """Make a single API request"""
        data = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }

        start_time = time.time()
        try:
            response = requests.post(self.api_url, headers=self.headers, json=data, timeout=60)
            end_time = time.time()

            if response.status_code == 200:
                result = response.json()
                content = result.get("choices", [{}])[0].get("message", {}).get("content", "")
                return {
                    "success": True,
                    "latency": end_time - start_time,
                    "status": response.status_code,
                    "response_length": len(content),
                    "tokens_generated": result.get("usage", {}).get("completion_tokens", 0)
                }
            else:
                return {
                    "success": False,
                    "latency": end_time - start_time,
                    "status": response.status_code,
                    "error": response.text
                }
        except Exception as e:
            end_time = time.time()
            return {
                "success": False,
                "latency": end_time - start_time,
                "error": str(e)
            }

    def benchmark_concurrent_requests(self, num_requests: int = 10, max_tokens: int = 100) -> Dict:
        """Benchmark concurrent requests simulating Santiago agents"""
        prompts = [
            f"Explain the concept of {topic} in the context of software development."
            for topic in [
                "machine learning", "neural networks", "software architecture",
                "agile development", "cloud computing", "data science",
                "artificial intelligence", "computer vision", "natural language processing",
                "distributed systems", "microservices", "API design", "testing strategies",
                "code review", "continuous integration", "database design"
            ]
        ]

        print(f"🚀 Starting benchmark with {num_requests} concurrent requests...")

        start_time = time.time()
        with ThreadPoolExecutor(max_workers=num_requests) as executor:
            results = list(executor.map(
                lambda p: self.single_request(p, max_tokens),
                prompts[:num_requests]
            ))
        end_time = time.time()

        # Analyze results
        successful_requests = [r for r in results if r["success"]]
        failed_requests = [r for r in results if not r["success"]]

        latencies = [r["latency"] for r in successful_requests]

        return {
            "total_requests": len(results),
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate": len(successful_requests) / len(results),
            "total_time": end_time - start_time,
            "requests_per_second": len(results) / (end_time - start_time),
            "avg_latency": sum(latencies) / len(latencies) if latencies else 0,
            "p50_latency": sorted(latencies)[int(len(latencies) * 0.5)] if latencies else 0,
            "p95_latency": sorted(latencies)[int(len(latencies) * 0.95)] if latencies else 0,
            "p99_latency": sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0,
            "min_latency": min(latencies) if latencies else 0,
            "max_latency": max(latencies) if latencies else 0,
            "failures": failed_requests
        }

    def benchmark_santiago_roles(self) -> Dict:
        """Test Santiago agent role simulation"""
        print("🎭 Testing Santiago Agent Role Simulation...")

        santiago_scenarios = {
            "Product Manager": {
                "task": "Design a product roadmap for implementing AI-powered code review in a development team",
                "expected_focus": ["strategy", "prioritization", "stakeholder"]
            },
            "Architect": {
                "task": "Design the system architecture for a multi-agent AI development platform",
                "expected_focus": ["technical design", "scalability", "integration"]
            },
            "Developer": {
                "task": "Implement a REST API endpoint for user authentication with JWT tokens",
                "expected_focus": ["code", "implementation", "best practices"]
            },
            "QA Specialist": {
                "task": "Create a comprehensive testing strategy for an AI-powered application",
                "expected_focus": ["testing", "quality", "validation"]
            },
            "UX Researcher": {
                "task": "Analyze user needs for an AI-assisted coding environment",
                "expected_focus": ["user experience", "usability", "needs analysis"]
            }
        }

        results = {}
        for role, scenario in santiago_scenarios.items():
            print(f"🤖 Testing {role}...")
            result = self.single_request(scenario["task"], max_tokens=300)
            results[role] = {
                "result": result,
                "scenario": scenario
            }

            if result["success"]:
                print(f"✅ {role}: {result['latency']:.2f}s, {result['response_length']} chars")
            else:
                print(f"❌ Failed: {result.get('error', 'Unknown error')}")

        return results

def main():
    parser = argparse.ArgumentParser(description="Mistral-7B DGX Performance Benchmark")
    parser.add_argument("--api-url", default="http://localhost:8001", help="vLLM API URL")
    parser.add_argument("--api-key", default="nusy-dgx-2025", help="API key")
    parser.add_argument("--concurrency", type=int, default=10, help="Number of concurrent requests")
    parser.add_argument("--max-tokens", type=int, default=100, help="Max tokens per request")
    parser.add_argument("--santiago-test", action="store_true", help="Run Santiago role simulation test")

    args = parser.parse_args()

    print("🧪 Mistral-7B DGX Performance Benchmark")
    print("=" * 50)
    print(f"API URL: {args.api_url}")
    print(f"Concurrency: {args.concurrency}")
    print(f"Max Tokens: {args.max_tokens}")
    print()

    benchmark = MistralBenchmark(args.api_url, args.api_key)

    # Test single request first
    print("📊 Single Request Test:")
    single_result = benchmark.single_request("What is the capital of France?")
    if single_result["success"]:
        print(f"✅ Latency: {single_result['latency']:.2f}s")
        print(f"Status: {single_result['status']}")
        print(f"Tokens: {single_result.get('tokens_generated', 'N/A')}")
    else:
        print(f"❌ Failed: {single_result.get('error', 'Unknown error')}")
        return

    print()

    # Concurrent benchmark
    print("📊 Concurrent Load Test:")
    concurrent_result = benchmark.benchmark_concurrent_requests(args.concurrency, args.max_tokens)

    print(f"Total Requests: {concurrent_result['total_requests']}")
    print(f"Successful: {concurrent_result['successful_requests']}")
    print(f"Failed: {concurrent_result['failed_requests']}")
    print(".1%")
    print(".2f")
    print(".1f")
    print(".2f")
    print(".2f")
    print(".2f")
    print(".2f")
    print(".2f")

    if concurrent_result['failed_requests'] > 0:
        print(f"\\n❌ Failures:")
        for failure in concurrent_result['failures'][:5]:  # Show first 5 failures
            print(f"  - {failure.get('error', 'Unknown error')}")

    print()

    # Santiago role test
    if args.santiago_test:
        print("🎭 Santiago Agent Role Test:")
        santiago_results = benchmark.benchmark_santiago_roles()

        successful_roles = sum(1 for r in santiago_results.values() if r["result"]["success"])
        print(f"\\nRole Tests: {successful_roles}/{len(santiago_results)} successful")

        for role, data in santiago_results.items():
            status = "✅" if data["result"]["success"] else "❌"
            latency = data["result"]["latency"]
            print(".2f")

    print("\\n✅ Benchmark complete!")

    # Save results
    results = {
        "timestamp": time.time(),
        "single_request": single_result,
        "concurrent_test": concurrent_result,
        "santiago_test": santiago_results if args.santiago_test else None
    }

    with open(f"benchmark_results_{int(time.time())}.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\\n📄 Results saved to benchmark_results_{int(time.time())}.json")

if __name__ == "__main__":
    main()</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/dgx-deployment-scripts/benchmark_mistral.py