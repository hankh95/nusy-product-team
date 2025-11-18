"""
Test script for the integrated Santiago-PM Question Answering system.

Tests the question answering capabilities with Santiago Core reasoning and prioritization.
"""

import asyncio
import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "expeditions" / "exp_040"))
sys.path.insert(0, str(Path(__file__).parent))

async def test_question_answering_integration():
    """Test the question answering service integration."""

    print("🧪 Testing Santiago-PM Question Answering Integration")
    print("=" * 60)

    try:
        # Import the integrated registry
        from mcp_service_integration import IntegratedServiceRegistry
        print("✅ Imported integrated service registry")

        # Create registry
        registry = IntegratedServiceRegistry()
        print(f"📋 Available services: {registry.list_services()}")

        # Test question answering service
        qa_service = registry.get_service("question_answering")
        if qa_service:
            print("✅ Question Answering service available")

            # Test different types of questions
            test_questions = [
                "How should we prioritize our product features?",
                "What is the best way to handle technical debt?",
                "How do we improve team collaboration?",
                "Should we focus on user experience or performance first?"
            ]

            from mcp_service_layer import MCPRequest
            import uuid
            from datetime import datetime

            for i, question in enumerate(test_questions, 1):
                print(f"\n❓ Test Question {i}: {question}")

                request = MCPRequest(
                    id=str(uuid.uuid4()),
                    method="execute",
                    params={
                        "operation": "answer",
                        "params": {
                            "question": question,
                            "context": {"domain": "product_management"}
                        }
                    },
                    timestamp=datetime.now(),
                    client_id="test_client"
                )

                response = await qa_service.invoke(request)

                if hasattr(response, 'result') and response.result.get('success'):
                    result = response.result.get('result', {})
                    print(f"   📝 Answer: {result.get('answer', 'No answer')[:100]}...")
                    print(f"   🎯 Confidence: {result.get('confidence', 0):.2f}")
                    print(f"   🧠 Method: {result.get('method', 'unknown')}")
                else:
                    print(f"   ❌ Failed to get answer: {getattr(response, 'error', 'Unknown error')}")

        else:
            print("❌ Question Answering service not available")

        # Test Santiago Core integration
        core_service = registry.get_service("santiago_core")
        if core_service:
            print("\n🧠 Testing Santiago Core integration")

            from mcp_service_layer import MCPRequest

            request = MCPRequest(
                id=str(uuid.uuid4()),
                method="execute",
                params={
                    "operation": "reason",
                    "params": {
                        "query": "What are the key factors for successful product prioritization?",
                        "domain": "product_management"
                    }
                },
                timestamp=datetime.now(),
                client_id="test_client"
            )

            response = await core_service.invoke(request)

            if hasattr(response, 'result') and response.result.get('success'):
                reasoning = response.result.get('reasoning', {})
                print(f"   📝 Santiago Core answer: {reasoning.get('answer', 'No answer')[:150]}...")
                print(f"   🎯 Confidence: {reasoning.get('confidence', 0):.2f}")
            else:
                print(f"   ❌ Santiago Core reasoning failed: {getattr(response, 'error', 'Unknown error')}")

        print("\n🎉 Question Answering Integration Test Complete!")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_question_answering_integration())