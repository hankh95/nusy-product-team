"""
MCP Service wrapper for the Question Answering Service.

Integrates the question answering capabilities with the Santiago-PM MCP service layer.
"""

import sys
import uuid
from pathlib import Path
from typing import Any, Dict, Optional
from datetime import datetime

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "expeditions" / "exp_040"))
sys.path.insert(0, str(Path(__file__).parent))

try:
    from mcp_service_layer import MCPService, ServiceContract
    from question_answering_service import QuestionAnsweringService
except ImportError as e:
    print(f"Warning: Could not import required modules: {e}")
    # Mock implementations for development
    class MCPService:
        def __init__(self, capability): self.capability = capability

    class ServiceContract:
        def __init__(self, **kwargs): pass

    class QuestionAnsweringService:
        async def answer_question(self, question, context=None): return {"answer": "Mock answer"}


class QuestionAnsweringMCPService:
    """MCP wrapper for Question Answering Service capabilities."""

    def __init__(self, question_service: QuestionAnsweringService):
        self.question_service = question_service
        self.name = "question_answering"

    @property
    def contract(self) -> ServiceContract:
        return ServiceContract(
            service_name="Question Answering Service",
            version="1.0.0",
            capabilities=[
                "answer_question",
                "generate_questionnaire",
                "analyze_questionnaire_response",
                "prioritization_analysis"
            ],
            input_schema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["answer", "generate_questionnaire", "analyze_response", "prioritize"]
                    },
                    "params": {"type": "object"}
                },
                "required": ["operation"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "result": {"type": "object"},
                    "answer": {"type": "string"},
                    "confidence": {"type": "number"},
                    "questionnaire": {"type": "object"},
                    "analysis": {"type": "object"}
                }
            },
            cost_model={
                "pricing": "per_operation",
                "base_cost": 0.03,
                "complexity_multiplier": 1.5,
                "questionnaire_generation_multiplier": 2.0
            }
        )

    async def execute(self, request):
        """Execute question answering operations through MCP interface."""
        from mcp_service_layer import MCPRequest, MCPResponse

        operation = request.params.get("operation")
        params = request.params.get("params", {})

        try:
            if operation == "answer":
                question = params.get("question", "")
                context = params.get("context", {})

                result = await self.question_service.answer_question(question, context)

                return MCPResponse(
                    id=request.id,
                    result={
                        "success": True,
                        "result": result,
                        "answer": result.get("answer"),
                        "confidence": result.get("confidence", 0),
                        "reasoning": result.get("reasoning"),
                        "method": result.get("method"),
                        "questionnaire": result.get("questionnaire"),
                        "artifacts_generated": result.get("artifacts_generated", [])
                    },
                    timestamp=datetime.now(),
                    execution_time_ms=500.0  # Estimated
                )

            elif operation == "generate_questionnaire":
                topic = params.get("topic", "")
                context = params.get("context", {})

                result = await self.question_service.generate_questionnaire_for_topic(topic, context)

                return MCPResponse(
                    id=request.id,
                    result={
                        "success": True,
                        "questionnaire": result,
                        "title": result.get("title"),
                        "content": result.get("content"),
                        "template_used": result.get("template_used")
                    },
                    timestamp=datetime.now(),
                    execution_time_ms=300.0
                )

            elif operation == "analyze_response":
                response_content = params.get("response_content", "")

                result = await self.question_service.analyze_questionnaire_response(response_content)

                return MCPResponse(
                    id=request.id,
                    result={
                        "success": True,
                        "analysis": result,
                        "insights": result.get("insights", []),
                        "recommended_actions": result.get("recommended_actions", []),
                        "potential_artifacts": result.get("potential_artifacts", [])
                    },
                    timestamp=datetime.now(),
                    execution_time_ms=400.0
                )

            elif operation == "prioritize":
                question = params.get("question", "What should we prioritize?")
                context = params.get("context", {})

                result = await self.question_service.answer_question(question, context)

                return MCPResponse(
                    id=request.id,
                    result={
                        "success": True,
                        "prioritization": result,
                        "answer": result.get("answer"),
                        "prioritized_items": result.get("prioritized_items", [])
                    },
                    timestamp=datetime.now(),
                    execution_time_ms=600.0
                )

            else:
                return MCPResponse(
                    id=request.id,
                    result={"success": False, "error": f"Unsupported operation: {operation}"},
                    timestamp=datetime.now(),
                    execution_time_ms=10.0
                )

        except Exception as e:
            return MCPResponse(
                id=request.id,
                error=str(e),
                timestamp=datetime.now(),
                execution_time_ms=10.0
            )


def create_question_answering_mcp_service(registry=None) -> MCPService:
    """
    Factory function to create the Question Answering MCP service.

    Args:
        registry: Optional MCP service registry for integration

    Returns:
        MCPService instance for question answering
    """
    question_service = QuestionAnsweringService(registry)
    mcp_wrapper = QuestionAnsweringMCPService(question_service)
    return MCPService(mcp_wrapper)


# Integration function for EXP-040
def integrate_question_answering_service(registry):
    """
    Integrate the Question Answering service into an existing MCP service registry.

    Args:
        registry: The MCP service registry to integrate into
    """
    question_service = QuestionAnsweringService(registry)
    mcp_wrapper = QuestionAnsweringMCPService(question_service)
    mcp_service = MCPService(mcp_wrapper)

    # Register with appropriate categories
    registry.register_service(mcp_service, categories=["question_answering", "reasoning", "team_support"])

    print("✅ Question Answering Service integrated into MCP registry")
    return mcp_service


if __name__ == "__main__":
    # Test the MCP service
    import asyncio

    async def test_mcp_service():
        print("Testing Question Answering MCP Service...")

        service = create_question_answering_mcp_service()

        # Test question answering
        from mcp_service_layer import MCPRequest

        request = MCPRequest(
            id=str(uuid.uuid4()),
            method="execute",
            params={
                "operation": "answer",
                "params": {
                    "question": "How should we prioritize our product features?",
                    "context": {"domain": "product_management"}
                }
            },
            timestamp=datetime.now(),
            client_id="test_client"
        )

        response = await service.invoke(request)
        print(f"Question answering test result: {response.result}")

        # Test questionnaire generation
        request2 = MCPRequest(
            id=str(uuid.uuid4()),
            method="execute",
            params={
                "operation": "generate_questionnaire",
                "params": {"topic": "feature prioritization"}
            },
            timestamp=datetime.now(),
            client_id="test_client"
        )

        response2 = await service.invoke(request2)
        print(f"Questionnaire generation test result: {response2.result}")

        print("Question Answering MCP Service test completed!")

    asyncio.run(test_mcp_service())