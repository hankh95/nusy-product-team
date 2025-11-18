"""
EXP-040: MCP Service Integration

Wraps EXP-036 foundational components as MCP services for integration
with EXP-039 entity architecture.
"""

import sys
import os
from pathlib import Path
from typing import Any, Dict, List, Optional
import asyncio
import uuid
from datetime import datetime

# Add EXP paths to sys.path for imports
exp_036_path = Path(__file__).parent.parent / "exp_036"
exp_038_path = Path(__file__).parent.parent / "exp_038"
exp_039_path = Path(__file__).parent.parent / "exp_039"
sys.path.insert(0, str(exp_036_path))
sys.path.insert(0, str(exp_038_path))
sys.path.insert(0, str(exp_039_path))

try:
    # Import EXP-036 components
    from workflow_orchestration_engine import WorkflowOrchestrationEngine
    from in_memory_llm_service import InMemoryLLMService
    from enhanced_shared_memory_git_service import EnhancedSharedMemoryGitService
    # Try to import Dulwich-based service as preferred option
    try:
        from dulwich_git_service import DulwichInMemoryGitService
        USE_DULWICH = True
        print("✅ Using Dulwich-based Git service (real Git operations)")
    except ImportError:
        USE_DULWICH = False
        print("ℹ️ Using enhanced shared memory Git service")
except ImportError as e:
    print(f"Warning: Could not import EXP-036 components: {e}")
    # Create mock implementations for development
    class WorkflowOrchestrationEngine:
        def prioritize_tasks(self, tasks): return sorted(tasks, key=lambda x: x.get('priority', 0), reverse=True)
        def execute_workflow(self, workflow): return {"status": "completed"}

    class InMemoryLLMService:
        def generate_response(self, prompt): return f"Mock response to: {prompt[:50]}..."

    class EnhancedSharedMemoryGitService:
        def commit_changes(self, message): return {"commit_id": str(uuid.uuid4())}
        def detect_conflicts(self, operations): return []

    USE_DULWICH = False

try:
    # Import EXP-038 Santiago Core - use simple core for now
    from simple_core import SantiagoCore, KnowledgeDomain
    print("✅ Using simple Santiago Core")
    
    # Define enums for compatibility
    class ReasoningMode:
        SYMBOLIC = "symbolic"
        NEURAL = "neural"
        NEUROSYMBOLIC = "neurosymbolic"
        HYBRID = "hybrid"
    
    class ReasoningContext:
        def __init__(self, query, domain, mode, confidence_threshold=0.7):
            self.query = query
            self.domain = domain
            self.mode = mode
            self.confidence_threshold = confidence_threshold
    
except ImportError as e:
    print(f"Warning: Could not import EXP-038 SantiagoCore: {e}")
    class SantiagoCore:
        def reason(self, query): return {"reasoning": f"Mock reasoning about: {query}"}
        async def initialize_core(self): return True
        def get_status(self): return {"health": "healthy"}

    # Define KnowledgeDomain as enum for compatibility
    from enum import Enum
    class KnowledgeDomain(Enum):
        PRODUCT_MANAGEMENT = "product_management"
        SOFTWARE_ENGINEERING = "software_engineering"
        SYSTEM_ARCHITECTURE = "system_architecture"
        TEAM_DYNAMICS = "team_dynamics"
        TECHNICAL_DEBT = "technical_debt"
        RISK_MANAGEMENT = "risk_management"
        KNOWLEDGE_MANAGEMENT = "knowledge_management"

try:
    # Import EXP-039 MCP components
    from mcp_service_layer import MCPService, MCPServiceRegistry, ServiceContract
    from entity_architecture import SantiagoEntity, EntityIdentity
    from capability_interfaces import CapabilityHub, KnowledgeQueryCapability, CapabilityDiscoveryCapability
except ImportError as e:
    print(f"Warning: Could not import EXP-039 components: {e}")
    # Create minimal mock implementations
    class MCPService:
        def __init__(self, capability): self.capability = capability
        async def invoke(self, request): return {"result": "mock"}

    class MCPServiceRegistry:
        def __init__(self): self.services = {}
        def register_service(self, service, categories=None): return str(uuid.uuid4())

    class SantiagoEntity:
        def __init__(self, identity): self.identity = identity

    class CapabilityHub:
        def __init__(self): self.capabilities = {}


class GitMCPService:
    """MCP wrapper for Git service capabilities - supports both Dulwich and custom implementations."""

    def __init__(self, git_service):
        self.git_service = git_service
        self.name = "git_operations"
        self.is_dulwich = hasattr(git_service, 'commit_changes') and hasattr(git_service, 'create_branch')

    @property
    def contract(self) -> ServiceContract:
        return ServiceContract(
            service_name="Git Operations Service",
            version="1.0.0",
            capabilities=["commit", "push", "pull", "merge", "conflict_resolution", "branch_management"],
            input_schema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["commit", "push", "pull", "merge", "resolve_conflicts", "create_branch"]
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
                    "commit_id": {"type": "string"},
                    "conflicts": {"type": "array"}
                }
            },
            cost_model={
                "pricing": "per_operation",
                "base_cost": 0.01,
                "conflict_resolution_multiplier": 2.0
            }
        )

    async def execute(self, request):
        """Execute Git operations through MCP interface."""
        from mcp_service_layer import MCPRequest, MCPResponse

        operation = request.params.get("operation")
        params = request.params.get("params", {})

        try:
            if operation == "commit":
                if self.is_dulwich:
                    # Dulwich service
                    message = params.get("message", "Auto-commit")
                    files = params.get("files")
                    result = await self.git_service.commit_changes(message, files=files)
                    return MCPResponse(
                        id=request.id,
                        result={"success": result.success, "commit_id": result.commit_id, "result": result.result},
                        timestamp=datetime.now(),
                        execution_time_ms=50.0
                    )
                else:
                    # Enhanced shared memory service
                    result = self.git_service.commit_changes(params.get("message", "Auto-commit"))
                    return MCPResponse(
                        id=request.id,
                        result={"success": True, "commit_id": result.get("commit_id")},
                        timestamp=datetime.now(),
                        execution_time_ms=50.0
                    )

            elif operation == "create_branch":
                if self.is_dulwich:
                    branch_name = params.get("branch_name", f"branch_{uuid.uuid4().hex[:8]}")
                    result = await self.git_service.create_branch(branch_name)
                    return MCPResponse(
                        id=request.id,
                        result={"success": result.success, "branch_name": result.branch},
                        timestamp=datetime.now(),
                        execution_time_ms=30.0
                    )
                else:
                    # Fallback for shared memory service
                    return MCPResponse(
                        id=request.id,
                        result={"success": False, "error": "Branch operations not supported in shared memory mode"},
                        timestamp=datetime.now(),
                        execution_time_ms=10.0
                    )

            elif operation == "resolve_conflicts":
                if self.is_dulwich:
                    operations = params.get("operations", [])
                    conflicts = await self.git_service.detect_conflicts(operations)
                    resolved = len(conflicts) == 0
                    return MCPResponse(
                        id=request.id,
                        result={
                            "success": resolved,
                            "conflicts_detected": len(conflicts),
                            "conflicts": conflicts
                        },
                        timestamp=datetime.now(),
                        execution_time_ms=100.0
                    )
                else:
                    operations = params.get("operations", [])
                    conflicts = self.git_service.detect_conflicts(operations)
                    return MCPResponse(
                        id=request.id,
                        result={
                            "success": len(conflicts) == 0,
                            "conflicts_detected": len(conflicts),
                            "conflicts": conflicts
                        },
                        timestamp=datetime.now(),
                        execution_time_ms=100.0
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


class WorkflowMCPService:
    """MCP wrapper for Workflow orchestration capabilities."""

    def __init__(self, workflow_engine: WorkflowOrchestrationEngine):
        self.workflow_engine = workflow_engine
        self.name = "workflow_orchestration"

    @property
    def contract(self) -> ServiceContract:
        return ServiceContract(
            service_name="Workflow Orchestration Service",
            version="1.0.0",
            capabilities=["prioritize_tasks", "execute_workflow", "create_workflow", "monitor_progress"],
            input_schema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["prioritize", "execute", "create", "monitor"]
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
                    "prioritized_tasks": {"type": "array"},
                    "workflow_status": {"type": "string"}
                }
            },
            cost_model={
                "pricing": "per_operation",
                "base_cost": 0.02,
                "complexity_multiplier": 1.5
            }
        )

    async def execute(self, request):
        """Execute workflow operations through MCP interface."""
        from mcp_service_layer import MCPRequest, MCPResponse

        operation = request.params.get("operation")
        params = request.params.get("params", {})

        try:
            if operation == "prioritize":
                tasks = params.get("tasks", [])
                prioritized = self.workflow_engine.prioritize_tasks(tasks)
                return MCPResponse(
                    id=request.id,
                    result={"success": True, "prioritized_tasks": prioritized},
                    timestamp=datetime.now(),
                    execution_time_ms=75.0
                )

            elif operation == "execute":
                workflow = params.get("workflow", {})
                result = self.workflow_engine.execute_workflow(workflow)
                return MCPResponse(
                    id=request.id,
                    result={"success": True, "workflow_result": result},
                    timestamp=datetime.now(),
                    execution_time_ms=200.0
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


class LLMMCPService:
    """MCP wrapper for LLM service capabilities."""

    def __init__(self, llm_service: InMemoryLLMService):
        self.llm_service = llm_service
        self.name = "llm_reasoning"

    @property
    def contract(self) -> ServiceContract:
        return ServiceContract(
            service_name="LLM Reasoning Service",
            version="1.0.0",
            capabilities=["generate_response", "analyze_code", "design_solution", "review_implementation"],
            input_schema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["generate", "analyze", "design", "review"]
                    },
                    "params": {"type": "object"}
                },
                "required": ["operation"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "response": {"type": "string"},
                    "analysis": {"type": "object"},
                    "confidence": {"type": "number"}
                }
            },
            cost_model={
                "pricing": "per_token",
                "base_cost": 0.001,
                "reasoning_multiplier": 1.2
            }
        )

    async def execute(self, request):
        """Execute LLM operations through MCP interface."""
        from mcp_service_layer import MCPRequest, MCPResponse

        operation = request.params.get("operation")
        params = request.params.get("params", {})

        try:
            if operation == "generate":
                prompt = params.get("prompt", "")
                response = self.llm_service.generate_response(prompt)
                return MCPResponse(
                    id=request.id,
                    result={"success": True, "response": response, "confidence": 0.8},
                    timestamp=datetime.now(),
                    execution_time_ms=300.0
                )

            elif operation == "analyze":
                code = params.get("code", "")
                prompt = f"Analyze this code: {code}"
                analysis = self.llm_service.generate_response(prompt)
                return MCPResponse(
                    id=request.id,
                    result={"success": True, "analysis": analysis, "confidence": 0.7},
                    timestamp=datetime.now(),
                    execution_time_ms=250.0
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


class SantiagoCoreMCPService:
    """MCP wrapper for Santiago Core reasoning capabilities."""

    def __init__(self, santiago_core: SantiagoCore):
        self.santiago_core = santiago_core
        self.name = "santiago_reasoning"

    @property
    def contract(self) -> ServiceContract:
        return ServiceContract(
            service_name="Santiago Core Reasoning Service",
            version="1.0.0",
            capabilities=["reason", "analyze_problem", "synthesize_solution", "evaluate_options"],
            input_schema={
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["reason", "analyze", "synthesize", "evaluate"]
                    },
                    "params": {"type": "object"}
                },
                "required": ["operation"]
            },
            output_schema={
                "type": "object",
                "properties": {
                    "success": {"type": "boolean"},
                    "reasoning": {"type": "object"},
                    "analysis": {"type": "object"},
                    "recommendation": {"type": "string"}
                }
            },
            cost_model={
                "pricing": "per_reasoning",
                "base_cost": 0.05,
                "complexity_multiplier": 2.0
            }
        )

    async def execute(self, request):
        """Execute Santiago Core reasoning through MCP interface."""
        from mcp_service_layer import MCPRequest, MCPResponse

        operation = request.params.get("operation")
        params = request.params.get("params", {})

        try:
            if operation == "reason":
                query = params.get("query", "")
                domain_name = params.get("domain", "product_management")
                
                # Simple core interface
                domain_map = {
                    "product_management": KnowledgeDomain.PRODUCT_MANAGEMENT,
                    "software_engineering": KnowledgeDomain.SOFTWARE_ENGINEERING,
                    "system_architecture": KnowledgeDomain.SYSTEM_ARCHITECTURE,
                    "team_dynamics": KnowledgeDomain.TEAM_DYNAMICS,
                    "technical_debt": KnowledgeDomain.TECHNICAL_DEBT,
                    "risk_management": KnowledgeDomain.RISK_MANAGEMENT,
                    "knowledge_management": KnowledgeDomain.KNOWLEDGE_MANAGEMENT
                }
                domain = domain_map.get(domain_name, KnowledgeDomain.PRODUCT_MANAGEMENT)
                
                result = await self.santiago_core.reason(query, domain)
                
                return MCPResponse(
                    id=request.id,
                    result={
                        "success": True, 
                        "reasoning": {
                            "answer": result["answer"],
                            "confidence": result["confidence"],
                            "execution_time": result["execution_time"],
                            "knowledge_used": result.get("knowledge_used", 0)
                        }
                    },
                    timestamp=datetime.now(),
                    execution_time_ms=result["execution_time"] * 1000
                )

            elif operation == "load_knowledge":
                domain_name = params.get("domain", "product_management")
                knowledge_data = params.get("knowledge_data", {})
                
                domain_map = {
                    "product_management": KnowledgeDomain.PRODUCT_MANAGEMENT,
                    "software_engineering": KnowledgeDomain.SOFTWARE_ENGINEERING,
                    "system_architecture": KnowledgeDomain.SYSTEM_ARCHITECTURE,
                    "team_dynamics": KnowledgeDomain.TEAM_DYNAMICS,
                    "technical_debt": KnowledgeDomain.TECHNICAL_DEBT,
                    "risk_management": KnowledgeDomain.RISK_MANAGEMENT,
                    "knowledge_management": KnowledgeDomain.KNOWLEDGE_MANAGEMENT
                }
                
                domain = domain_map.get(domain_name, KnowledgeDomain.PRODUCT_MANAGEMENT)
                
                if hasattr(self.santiago_core, 'load_domain_knowledge'):
                    nodes_loaded = await self.santiago_core.load_domain_knowledge(domain, knowledge_data)
                else:
                    nodes_loaded = 0  # Simple core doesn't support loading
                
                return MCPResponse(
                    id=request.id,
                    result={"success": True, "result": {"nodes_loaded": nodes_loaded, "domain": domain_name}},
                    timestamp=datetime.now(),
                    execution_time_ms=50.0
                )

            elif operation == "get_status":
                if hasattr(self.santiago_core, 'get_status'):
                    status = self.santiago_core.get_status()
                else:
                    status = {"health": "unknown"}
                    
                return MCPResponse(
                    id=request.id,
                    result={"success": True, "status": status},
                    timestamp=datetime.now(),
                    execution_time_ms=10.0
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


class IntegratedServiceRegistry:
    """
    Registry that integrates all EXP-036 components as MCP services.
    """

    def __init__(self, santiago_core: Optional[SantiagoCore] = None, workspace_path: Optional[str] = None):
        self.registry = MCPServiceRegistry()
        self.services = {}

        # Initialize EXP-036 components
        # Use provided workspace path or default
        if workspace_path is None:
            workspace_path = str(Path(__file__).parent.parent.parent / "workspace")
        
        self.workspace_path = workspace_path
        
        if USE_DULWICH:
            self.git_service = DulwichInMemoryGitService(workspace_path=workspace_path)
        else:
            self.git_service = EnhancedSharedMemoryGitService(workspace_path=workspace_path)
            
        self.workflow_engine = WorkflowOrchestrationEngine()
        self.llm_service = InMemoryLLMService()
        
        # Use provided Santiago Core or create new one
        self.santiago_core = santiago_core or SantiagoCore()
        # Don't call asyncio.run here - let caller handle async initialization

        # Wrap as MCP services
        self._wrap_services()

    def _wrap_services(self):
        """Wrap all EXP-036 components as MCP services."""

        # Git service
        git_mcp = GitMCPService(self.git_service)
        git_service = MCPService(git_mcp)
        self.registry.register_service(git_service, categories=["version_control", "collaboration"])
        self.services["git"] = git_service

        # Workflow service
        workflow_mcp = WorkflowMCPService(self.workflow_engine)
        workflow_service = MCPService(workflow_mcp)
        self.registry.register_service(workflow_service, categories=["workflow", "orchestration"])
        self.services["workflow"] = workflow_service

        # LLM service
        llm_mcp = LLMMCPService(self.llm_service)
        llm_service = MCPService(llm_mcp)
        self.registry.register_service(llm_service, categories=["ai", "reasoning"])
        self.services["llm"] = llm_service

        # Santiago Core service
        core_mcp = SantiagoCoreMCPService(self.santiago_core)
        core_service = MCPService(core_mcp)
        self.registry.register_service(core_service, categories=["reasoning", "core"])
        self.services["santiago_core"] = core_service

        # Question Answering service (optional integration)
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent.parent / "santiago-pm" / "tackle" / "question_answering"))
            from question_answering_mcp import create_question_answering_mcp_service
            qa_service = create_question_answering_mcp_service(self)
            self.registry.register_service(qa_service, categories=["question_answering", "reasoning", "team_support"])
            self.services["question_answering"] = qa_service
            print("✅ Question Answering Service integrated")
        except ImportError as e:
            print(f"ℹ️ Question Answering Service not available: {e}")

    def get_service(self, service_name: str) -> Optional[MCPService]:
        """Get an MCP service by name."""
        return self.services.get(service_name)

    def list_services(self) -> List[str]:
        """List available service names."""
        return list(self.services.keys())

    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics."""
        return self.registry.get_service_stats()


# Test the integration
async def test_mcp_integration():
    """Test MCP service integration."""

    print("Testing MCP Service Integration...")

    # Create integrated registry
    registry = IntegratedServiceRegistry()

    print(f"Available services: {registry.list_services()}")
    print(f"Registry stats: {registry.get_registry_stats()}")

    # Test Git service
    git_service = registry.get_service("git")
    if git_service:
        from mcp_service_layer import MCPRequest
        request = MCPRequest(
            id=str(uuid.uuid4()),
            method="execute",
            params={"operation": "commit", "params": {"message": "Test commit"}},
            timestamp=datetime.now(),
            client_id="test_client"
        )

        response = await git_service.invoke(request)
        print(f"Git service test: {response.result}")

    # Test workflow service
    workflow_service = registry.get_service("workflow")
    if workflow_service:
        from mcp_service_layer import MCPRequest
        request = MCPRequest(
            id=str(uuid.uuid4()),
            method="execute",
            params={"operation": "prioritize", "params": {"tasks": [{"id": "task1", "priority": 1}]}},
            timestamp=datetime.now(),
            client_id="test_client"
        )

        response = await workflow_service.invoke(request)
        print(f"Workflow service test: {response.result}")

    print("MCP Integration test completed!")


if __name__ == "__main__":
    asyncio.run(test_mcp_integration())