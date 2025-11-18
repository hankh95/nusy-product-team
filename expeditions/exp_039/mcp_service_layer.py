"""
EXP-039: MCP Service Layer

Implements MCP (Model Context Protocol) wrapper for capabilities,
enabling tools and services to be exposed as hireable expert services.
This addresses the question: "Should Git and other tools be wrapped as
Santiago-PM MCP capabilities? Do we use MCP so experts can work both
on the team and as MCP services available for hire?"
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Protocol, Union
from datetime import datetime
import asyncio
import json
import uuid


@dataclass
class MCPRequest:
    """Standardized MCP request format."""
    id: str
    method: str
    params: Dict[str, Any]
    client_id: str
    timestamp: datetime
    priority: int = 1  # 1=normal, 2=high, 3=urgent


@dataclass
class MCPResponse:
    """Standardized MCP response format."""
    id: str
    timestamp: datetime
    execution_time_ms: float
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = None


@dataclass
class ServiceContract:
    """MCP service contract defining capabilities and interfaces."""
    service_name: str
    version: str
    capabilities: List[str]
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    cost_model: Dict[str, Any]  # pricing, rate limits, etc.
    metadata: Dict[str, Any] = None


class MCPCapability(Protocol):
    """Protocol for MCP-wrapped capabilities."""

    @property
    def name(self) -> str:
        """Capability name."""
        ...

    @property
    def contract(self) -> ServiceContract:
        """Service contract."""
        ...

    async def execute(self, request: MCPRequest) -> MCPResponse:
        """Execute the capability."""
        ...


class MCPService:
    """
    MCP wrapper for any capability, enabling it to be exposed as a hireable service.

    This addresses the architectural question: should tools like Git be wrapped
    as MCP services to enable expert marketplace functionality?
    """

    def __init__(self, capability: MCPCapability):
        self.capability = capability
        self.service_id = str(uuid.uuid4())
        self.active_requests: Dict[str, asyncio.Task] = {}
        self.request_history: List[MCPRequest] = []
        self.response_history: List[MCPResponse] = []
        self._performance_stats = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'average_execution_time': 0.0,
            'last_execution_time': 0.0
        }

    @property
    def name(self) -> str:
        return self.capability.name

    @property
    def contract(self) -> ServiceContract:
        return self.capability.contract

    async def invoke(self, request: MCPRequest) -> MCPResponse:
        """
        Standardized MCP invocation with monitoring and error handling.

        This implements the "hireable service" model where capabilities
        can be invoked by different clients (team members or external experts).
        """
        start_time = datetime.now()

        # Update stats
        self._performance_stats['total_requests'] += 1
        self.request_history.append(request)

        try:
            # Execute capability
            task = asyncio.create_task(self.capability.execute(request))
            self.active_requests[request.id] = task

            response = await task

            # Update success stats
            self._performance_stats['successful_requests'] += 1
            execution_time = (datetime.now() - start_time).total_seconds() * 1000
            self._performance_stats['last_execution_time'] = execution_time
            self._performance_stats['average_execution_time'] = (
                (self._performance_stats['average_execution_time'] *
                 (self._performance_stats['total_requests'] - 1) + execution_time) /
                self._performance_stats['total_requests']
            )

            response.execution_time_ms = execution_time
            self.response_history.append(response)

            return response

        except Exception as e:
            # Update failure stats
            self._performance_stats['failed_requests'] += 1
            execution_time = (datetime.now() - start_time).total_seconds() * 1000

            error_response = MCPResponse(
                id=request.id,
                error=str(e),
                timestamp=datetime.now(),
                execution_time_ms=execution_time,
                metadata={'exception_type': type(e).__name__}
            )

            self.response_history.append(error_response)
            return error_response

        finally:
            # Clean up active request
            if request.id in self.active_requests:
                del self.active_requests[request.id]

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for monitoring."""
        return self._performance_stats.copy()

    def get_active_requests(self) -> List[str]:
        """Get IDs of currently active requests."""
        return list(self.active_requests.keys())

    async def cancel_request(self, request_id: str) -> bool:
        """Cancel an active request."""
        if request_id in self.active_requests:
            task = self.active_requests[request_id]
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            del self.active_requests[request_id]
            return True
        return False


class MCPServiceRegistry:
    """
    Registry for MCP services, enabling service discovery and marketplace functionality.

    This implements the "expert marketplace" concept where services can be
    discovered and hired by different clients.
    """

    def __init__(self):
        self.services: Dict[str, MCPService] = {}
        self.service_categories: Dict[str, List[str]] = {}  # category -> service_ids
        self.client_usage: Dict[str, List[str]] = {}  # client_id -> service_ids used

    def register_service(self, service: MCPService, categories: List[str] = None) -> str:
        """Register an MCP service."""
        service_id = service.service_id
        self.services[service_id] = service

        if categories:
            for category in categories:
                if category not in self.service_categories:
                    self.service_categories[category] = []
                self.service_categories[category].append(service_id)

        return service_id

    def unregister_service(self, service_id: str) -> bool:
        """Unregister an MCP service."""
        if service_id in self.services:
            del self.services[service_id]

            # Remove from categories
            for category, service_ids in self.service_categories.items():
                if service_id in service_ids:
                    service_ids.remove(service_id)

            return True
        return False

    def discover_services(self,
                         category: str = None,
                         capability: str = None,
                         client_id: str = None) -> List[MCPService]:
        """Discover services by category, capability, or client usage history."""
        candidates = list(self.services.values())

        if category:
            category_services = self.service_categories.get(category, [])
            candidates = [s for s in candidates if s.service_id in category_services]

        if capability:
            candidates = [s for s in candidates if capability in s.contract.capabilities]

        if client_id and client_id in self.client_usage:
            # Prioritize services the client has used before
            used_services = self.client_usage[client_id]
            candidates.sort(key=lambda s: s.service_id in used_services, reverse=True)

        return candidates

    def get_service(self, service_id: str) -> Optional[MCPService]:
        """Get a specific service by ID."""
        return self.services.get(service_id)

    def record_client_usage(self, client_id: str, service_id: str):
        """Record that a client used a service."""
        if client_id not in self.client_usage:
            self.client_usage[client_id] = []
        if service_id not in self.client_usage[client_id]:
            self.client_usage[client_id].append(service_id)

    def get_service_stats(self) -> Dict[str, Any]:
        """Get registry-wide statistics."""
        total_services = len(self.services)
        total_categories = len(self.service_categories)
        total_clients = len(self.client_usage)

        return {
            'total_services': total_services,
            'total_categories': total_categories,
            'total_clients': total_clients,
            'services_per_category': {
                cat: len(services) for cat, services in self.service_categories.items()
            }
        }


class MCPClient:
    """
    Client for invoking MCP services, representing either team members or external experts.

    This enables the "experts working both on team and as hireable services" model.
    """

    def __init__(self, client_id: str, registry: MCPServiceRegistry):
        self.client_id = client_id
        self.registry = registry
        self.session_requests: List[MCPRequest] = []

    async def invoke_service(self,
                           service_id: str,
                           method: str,
                           params: Dict[str, Any],
                           priority: int = 1) -> MCPResponse:
        """Invoke an MCP service."""
        service = self.registry.get_service(service_id)
        if not service:
            return MCPResponse(
                id=str(uuid.uuid4()),
                error=f"Service {service_id} not found",
                timestamp=datetime.now(),
                execution_time_ms=0.0
            )

        request = MCPRequest(
            id=str(uuid.uuid4()),
            method=method,
            params=params,
            timestamp=datetime.now(),
            client_id=self.client_id,
            priority=priority
        )

        self.session_requests.append(request)
        response = await service.invoke(request)

        # Record usage for future discovery prioritization
        self.registry.record_client_usage(self.client_id, service_id)

        return response

    async def discover_and_invoke(self,
                                category: str = None,
                                capability: str = None,
                                method: str = None,
                                params: Dict[str, Any] = None,
                                priority: int = 1) -> MCPResponse:
        """Discover a service and invoke it."""
        services = self.registry.discover_services(
            category=category,
            capability=capability,
            client_id=self.client_id
        )

        if not services:
            return MCPResponse(
                id=str(uuid.uuid4()),
                error=f"No services found for category={category}, capability={capability}",
                timestamp=datetime.now(),
                execution_time_ms=0.0
            )

        # Use first available service (could implement load balancing, etc.)
        service = services[0]
        return await self.invoke_service(
            service.service_id,
            method or "execute",
            params or {},
            priority
        )


# Example usage and testing
async def demo_mcp_service_layer():
    """Demonstrate MCP service layer functionality."""

    # Create registry
    registry = MCPServiceRegistry()

    # Create a mock Git capability (would wrap actual Git service)
    class MockGitCapability:
        @property
        def name(self) -> str:
            return "git_operations"

        @property
        def contract(self) -> ServiceContract:
            return ServiceContract(
                service_name="Git Operations",
                version="1.0.0",
                capabilities=["commit", "push", "pull", "merge"],
                input_schema={
                    "type": "object",
                    "properties": {
                        "operation": {"type": "string", "enum": ["commit", "push", "pull", "merge"]},
                        "params": {"type": "object"}
                    }
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean"},
                        "result": {"type": "object"}
                    }
                },
                cost_model={
                    "pricing": "per_operation",
                    "rate_limit": "100/hour",
                    "cost_per_operation": 0.01
                }
            )

        async def execute(self, request: MCPRequest) -> MCPResponse:
            # Mock implementation
            await asyncio.sleep(0.1)  # Simulate work
            return MCPResponse(
                id=request.id,
                result={"success": True, "operation": request.params.get("operation")},
                timestamp=datetime.now(),
                execution_time_ms=100.0
            )

    # Wrap capability as MCP service
    git_capability = MockGitCapability()
    git_service = MCPService(git_capability)
    registry.register_service(git_service, categories=["version_control", "collaboration"])

    # Create client (representing a team member or external expert)
    client = MCPClient("team_member_1", registry)

    # Invoke service directly
    response1 = await client.invoke_service(
        git_service.service_id,
        "execute",
        {"operation": "commit", "message": "Initial commit"}
    )
    print(f"Direct invocation: {response1.result}")

    # Discover and invoke
    response2 = await client.discover_and_invoke(
        category="version_control",
        method="execute",
        params={"operation": "push"}
    )
    print(f"Discovery invocation: {response2.result}")

    # Check stats
    service_stats = git_service.get_performance_stats()
    registry_stats = registry.get_service_stats()
    print(f"Service stats: {service_stats}")
    print(f"Registry stats: {registry_stats}")


if __name__ == "__main__":
    asyncio.run(demo_mcp_service_layer())