"""
EXP-039: Common Capability Interfaces

Defines common capability interfaces that domain experts can access.
This addresses the question: "How does the core's knowledge hub expose
a common set of capabilities that domain experts (use or are built with)?"
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, Union, Callable
from datetime import datetime
import asyncio
import inspect
import uuid


@dataclass
class CapabilityRequest:
    """Request to execute a capability."""
    id: str
    capability_name: str
    parameters: Dict[str, Any]
    requester_id: str
    priority: int = 1
    timeout_seconds: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CapabilityResponse:
    """Response from capability execution."""
    request_id: str
    success: bool
    result: Any
    execution_time: float
    cost: float
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class CapabilityInterface(Protocol):
    """Protocol for capability interfaces."""

    @property
    def name(self) -> str:
        """Capability name."""
        ...

    @property
    def description(self) -> str:
        """Capability description."""
        ...

    @property
    def input_schema(self) -> Dict[str, Any]:
        """Input parameter schema."""
        ...

    @property
    def output_schema(self) -> Dict[str, Any]:
        """Output result schema."""
        ...

    async def execute(self, request: CapabilityRequest) -> CapabilityResponse:
        """Execute the capability."""
        ...


class CommonCapability:
    """
    Base class for common capabilities that all domain experts can access.

    This implements the "common set of capabilities" that the knowledge hub exposes.
    """

    def __init__(self, name: str, description: str):
        self._name = name
        self._description = description
        self._usage_stats = {
            'total_calls': 0,
            'successful_calls': 0,
            'failed_calls': 0,
            'average_execution_time': 0.0,
            'total_cost': 0.0
        }

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def input_schema(self) -> Dict[str, Any]:
        """Default input schema - override in subclasses."""
        return {
            "type": "object",
            "properties": {
                "parameters": {"type": "object"}
            }
        }

    @property
    def output_schema(self) -> Dict[str, Any]:
        """Default output schema - override in subclasses."""
        return {
            "type": "object",
            "properties": {
                "success": {"type": "boolean"},
                "result": {"type": "any"},
                "execution_time": {"type": "number"},
                "cost": {"type": "number"}
            }
        }

    async def execute(self, request: CapabilityRequest) -> CapabilityResponse:
        """Execute capability with monitoring."""
        start_time = datetime.now()

        try:
            # Validate request
            self._validate_request(request)

            # Execute implementation
            result = await self._execute_impl(request)

            # Update stats
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_stats(success=True, execution_time=execution_time, cost=result.get('cost', 0.0))

            return CapabilityResponse(
                request_id=request.id,
                success=True,
                result=result,
                execution_time=execution_time,
                cost=result.get('cost', 0.0),
                metadata=result.get('metadata', {})
            )

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_stats(success=False, execution_time=execution_time, cost=0.0)

            return CapabilityResponse(
                request_id=request.id,
                success=False,
                result=None,
                execution_time=execution_time,
                cost=0.0,
                error_message=str(e),
                metadata={'exception_type': type(e).__name__}
            )

    @abstractmethod
    async def _execute_impl(self, request: CapabilityRequest) -> Dict[str, Any]:
        """Implementation of capability execution."""
        pass

    def _validate_request(self, request: CapabilityRequest):
        """Validate capability request."""
        if not request.capability_name:
            raise ValueError("Capability name is required")
        if request.capability_name != self.name:
            raise ValueError(f"Request capability '{request.capability_name}' does not match '{self.name}'")

    def _update_stats(self, success: bool, execution_time: float, cost: float):
        """Update usage statistics."""
        self._usage_stats['total_calls'] += 1
        if success:
            self._usage_stats['successful_calls'] += 1
        else:
            self._usage_stats['failed_calls'] += 1

        # Update average execution time
        total_calls = self._usage_stats['total_calls']
        current_avg = self._usage_stats['average_execution_time']
        self._usage_stats['average_execution_time'] = (
            (current_avg * (total_calls - 1) + execution_time) / total_calls
        )

        self._usage_stats['total_cost'] += cost

    def get_usage_stats(self) -> Dict[str, Any]:
        """Get capability usage statistics."""
        return self._usage_stats.copy()


# Core Common Capabilities

class KnowledgeQueryCapability(CommonCapability):
    """
    Capability for querying knowledge across domains.

    This enables domain experts to access shared knowledge.
    """

    def __init__(self, knowledge_base):
        super().__init__(
            name="knowledge_query",
            description="Query knowledge across domains with filtering and ranking"
        )
        self.knowledge_base = knowledge_base

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
                "domain": {"type": "string", "description": "Domain filter"},
                "tags": {"type": "array", "items": {"type": "string"}, "description": "Tag filters"},
                "min_confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.0},
                "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 10}
            },
            "required": ["query"]
        }

    async def _execute_impl(self, request: CapabilityRequest) -> Dict[str, Any]:
        params = request.parameters

        # Query knowledge
        results = self.knowledge_base.query_knowledge(
            domain=params.get('domain'),
            tags=params.get('tags'),
            min_confidence=params.get('min_confidence', 0.0)
        )

        # Apply limit
        limit = params.get('limit', 10)
        results = results[:limit]

        # Format results
        formatted_results = []
        for item in results:
            formatted_results.append({
                'id': item.id,
                'domain': item.domain,
                'content': item.content,
                'confidence': item.confidence,
                'source': item.source,
                'tags': item.tags,
                'timestamp': item.timestamp.isoformat()
            })

        return {
            'results': formatted_results,
            'total_found': len(results),
            'cost': 0.01 * len(results)  # Cost per result
        }


class CapabilityDiscoveryCapability(CommonCapability):
    """
    Capability for discovering available capabilities.

    This enables dynamic capability discovery and usage.
    """

    def __init__(self, capability_registry):
        super().__init__(
            name="capability_discovery",
            description="Discover available capabilities by category, tags, or keywords"
        )
        self.capability_registry = capability_registry

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "Capability category"},
                "keywords": {"type": "array", "items": {"type": "string"}, "description": "Search keywords"},
                "limit": {"type": "integer", "minimum": 1, "maximum": 50, "default": 20}
            }
        }

    async def _execute_impl(self, request: CapabilityRequest) -> Dict[str, Any]:
        params = request.parameters

        # Discover capabilities
        if params.get('category'):
            capabilities = self.capability_registry.discover_capabilities(params['category'])
        else:
            capabilities = list(self.capability_registry.capabilities.values())

        # Filter by keywords if provided
        keywords = params.get('keywords', [])
        if keywords:
            filtered = []
            for cap in capabilities:
                cap_text = f"{cap.name} {cap.description}".lower()
                if any(keyword.lower() in cap_text for keyword in keywords):
                    filtered.append(cap)
            capabilities = filtered

        # Apply limit
        limit = params.get('limit', 20)
        capabilities = capabilities[:limit]

        # Format results
        formatted_results = []
        for cap in capabilities:
            formatted_results.append({
                'name': cap.name,
                'description': cap.description,
                'execution_cost': cap.execution_cost,
                'success_rate': cap.success_rate,
                'usage_count': cap.usage_count,
                'last_used': cap.last_used.isoformat() if cap.last_used else None
            })

        return {
            'capabilities': formatted_results,
            'total_found': len(capabilities),
            'cost': 0.005 * len(capabilities)  # Cost per capability
        }


class CollaborationCapability(CommonCapability):
    """
    Capability for initiating and managing collaborations.

    This enables entities to work together on complex tasks.
    """

    def __init__(self, collaboration_network, entity_id: str):
        super().__init__(
            name="collaboration",
            description="Initiate and manage collaborations with other entities"
        )
        self.collaboration_network = collaboration_network
        self.entity_id = entity_id

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["find_partners", "initiate_collaboration", "update_trust"]},
                "goal_description": {"type": "string", "description": "Goal for collaboration"},
                "min_trust": {"type": "number", "minimum": 0.0, "maximum": 1.0, "default": 0.7},
                "partner_ids": {"type": "array", "items": {"type": "string"}, "description": "Specific partner IDs"},
                "trust_updates": {"type": "object", "description": "Trust score updates"}
            },
            "required": ["action"]
        }

    async def _execute_impl(self, request: CapabilityRequest) -> Dict[str, Any]:
        params = request.parameters
        action = params['action']

        if action == "find_partners":
            min_trust = params.get('min_trust', 0.7)
            partners = self.collaboration_network.get_collaboration_partners(
                self.entity_id, min_trust
            )

            return {
                'partners': partners,
                'min_trust': min_trust,
                'cost': 0.02 * len(partners)
            }

        elif action == "initiate_collaboration":
            goal_desc = params.get('goal_description', '')
            partner_ids = params.get('partner_ids', [])

            if not goal_desc or not partner_ids:
                raise ValueError("Goal description and partner IDs required for collaboration")

            goal_id = str(uuid.uuid4())
            participants = [self.entity_id] + partner_ids

            self.collaboration_network.record_collaboration(
                goal_id, participants, {'status': 'initiated', 'goal': goal_desc}
            )

            return {
                'collaboration_id': goal_id,
                'participants': participants,
                'goal': goal_desc,
                'status': 'initiated',
                'cost': 0.1
            }

        elif action == "update_trust":
            trust_updates = params.get('trust_updates', {})
            updates_made = 0

            for partner_id, trust_delta in trust_updates.items():
                if isinstance(trust_delta, (int, float)):
                    self.collaboration_network.update_trust(
                        self.entity_id, partner_id, float(trust_delta)
                    )
                    updates_made += 1

            return {
                'updates_made': updates_made,
                'cost': 0.01 * updates_made
            }

        else:
            raise ValueError(f"Unknown action: {action}")


class LearningCapability(CommonCapability):
    """
    Capability for learning and adapting from experience.

    This enables continuous improvement of entity capabilities.
    """

    def __init__(self, knowledge_base, capability_registry):
        super().__init__(
            name="learning",
            description="Learn from experience and adapt capabilities"
        )
        self.knowledge_base = knowledge_base
        self.capability_registry = capability_registry

    @property
    def input_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "action": {"type": "string", "enum": ["record_experience", "analyze_performance", "adapt_capability"]},
                "experience_data": {"type": "object", "description": "Experience data to record"},
                "capability_name": {"type": "string", "description": "Capability to analyze/adapt"},
                "analysis_period_days": {"type": "integer", "minimum": 1, "maximum": 365, "default": 30}
            },
            "required": ["action"]
        }

    async def _execute_impl(self, request: CapabilityRequest) -> Dict[str, Any]:
        params = request.parameters
        action = params['action']

        if action == "record_experience":
            experience = params.get('experience_data', {})

            # Create knowledge item from experience
            knowledge_item = KnowledgeItem(
                id=str(uuid.uuid4()),
                domain=experience.get('domain', 'general'),
                content=experience.get('content', {}),
                confidence=experience.get('confidence', 0.8),
                source='experience',
                timestamp=datetime.now(),
                tags=experience.get('tags', [])
            )

            self.knowledge_base.add_knowledge(knowledge_item)

            return {
                'knowledge_id': knowledge_item.id,
                'recorded': True,
                'cost': 0.05
            }

        elif action == "analyze_performance":
            cap_name = params.get('capability_name')
            if not cap_name:
                raise ValueError("Capability name required for analysis")

            capability = self.capability_registry.get_capability(cap_name)
            if not capability:
                raise ValueError(f"Capability not found: {cap_name}")

            # Analyze performance (simplified)
            analysis = {
                'capability': cap_name,
                'usage_count': capability.usage_count,
                'success_rate': capability.success_rate,
                'last_used': capability.last_used.isoformat() if capability.last_used else None,
                'recommendations': []
            }

            if capability.usage_count < 5:
                analysis['recommendations'].append("Low usage - consider more training")
            if capability.success_rate < 0.8:
                analysis['recommendations'].append("Low success rate - review implementation")

            return {
                'analysis': analysis,
                'cost': 0.03
            }

        elif action == "adapt_capability":
            cap_name = params.get('capability_name')
            if not cap_name:
                raise ValueError("Capability name required for adaptation")

            # Simplified adaptation - would implement actual ML/model updates
            capability = self.capability_registry.get_capability(cap_name)
            if capability:
                # Simulate improvement
                capability.success_rate = min(1.0, capability.success_rate + 0.05)

            return {
                'capability': cap_name,
                'adapted': True,
                'new_success_rate': capability.success_rate if capability else None,
                'cost': 0.2
            }

        else:
            raise ValueError(f"Unknown action: {action}")


class CapabilityHub:
    """
    Central hub that exposes common capabilities to domain experts.

    This implements the "knowledge hub" that exposes capabilities to all entities.
    """

    def __init__(self):
        self.capabilities: Dict[str, CommonCapability] = {}
        self.categories: Dict[str, List[str]] = {}  # category -> capability_names

    def register_capability(self, capability: CommonCapability, categories: List[str] = None):
        """Register a common capability."""
        self.capabilities[capability.name] = capability

        if categories:
            for category in categories:
                if category not in self.categories:
                    self.categories[category] = []
                self.categories[category].append(capability.name)

    async def execute_capability(self, request: CapabilityRequest) -> CapabilityResponse:
        """Execute a capability by name."""
        capability = self.capabilities.get(request.capability_name)
        if not capability:
            return CapabilityResponse(
                request_id=request.id,
                success=False,
                result=None,
                execution_time=0.0,
                cost=0.0,
                error_message=f"Capability not found: {request.capability_name}"
            )

        return await capability.execute(request)

    def list_capabilities(self, category: str = None) -> List[Dict[str, Any]]:
        """List available capabilities."""
        if category:
            cap_names = self.categories.get(category, [])
            capabilities = [self.capabilities[name] for name in cap_names if name in self.capabilities]
        else:
            capabilities = list(self.capabilities.values())

        return [{
            'name': cap.name,
            'description': cap.description,
            'usage_stats': cap.get_usage_stats()
        } for cap in capabilities]

    def get_capability_schema(self, capability_name: str) -> Optional[Dict[str, Any]]:
        """Get input/output schema for a capability."""
        capability = self.capabilities.get(capability_name)
        if not capability:
            return None

        return {
            'input_schema': capability.input_schema,
            'output_schema': capability.output_schema
        }


# Example usage and testing
async def demo_capability_interfaces():
    """Demonstrate common capability interfaces."""

    # Create hub
    hub = CapabilityHub()

    # Create mock knowledge base and registry for capabilities
    class MockKnowledgeBase:
        def query_knowledge(self, domain=None, tags=None, min_confidence=0.0):
            return [
                type('MockItem', (), {
                    'id': 'item1',
                    'domain': domain or 'test',
                    'content': 'Test knowledge',
                    'confidence': 0.9,
                    'source': 'test',
                    'tags': tags or [],
                    'timestamp': datetime.now()
                })()
            ]

    class MockCapabilityRegistry:
        def __init__(self):
            self.capabilities = {
                'test_cap': type('MockCap', (), {
                    'name': 'test_cap',
                    'description': 'Test capability',
                    'execution_cost': 0.1,
                    'success_rate': 0.95,
                    'usage_count': 10,
                    'last_used': datetime.now()
                })()
            }

        def discover_capabilities(self, category):
            return list(self.capabilities.values())

        def get_capability(self, name):
            return self.capabilities.get(name)

    knowledge_base = MockKnowledgeBase()
    capability_registry = MockCapabilityRegistry()

    # Register common capabilities
    hub.register_capability(
        KnowledgeQueryCapability(knowledge_base),
        categories=['knowledge', 'query']
    )

    hub.register_capability(
        CapabilityDiscoveryCapability(capability_registry),
        categories=['discovery', 'meta']
    )

    # Execute knowledge query
    request1 = CapabilityRequest(
        id=str(uuid.uuid4()),
        capability_name="knowledge_query",
        parameters={"query": "architecture patterns", "limit": 5},
        requester_id="entity_001"
    )

    response1 = await hub.execute_capability(request1)
    print(f"Knowledge query result: {response1.success}")
    print(f"Results found: {len(response1.result['results'])}")

    # Execute capability discovery
    request2 = CapabilityRequest(
        id=str(uuid.uuid4()),
        capability_name="capability_discovery",
        parameters={"category": "knowledge"},
        requester_id="entity_001"
    )

    response2 = await hub.execute_capability(request2)
    print(f"Capability discovery result: {response2.success}")
    print(f"Capabilities found: {len(response2.result['capabilities'])}")

    # List all capabilities
    all_caps = hub.list_capabilities()
    print(f"Total capabilities available: {len(all_caps)}")


if __name__ == "__main__":
    asyncio.run(demo_capability_interfaces())