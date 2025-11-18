"""
EXP-039: Santiago Entity Architecture

Implements "people-ish" entities that combine knowledge and capabilities.
This addresses the question: "Should Santiagos be modeled as entities with
both knowledge and tools/capabilities? What are the fastest interfaces
in an in-memory system of systems?"
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, Set, Union
from datetime import datetime
import asyncio
import uuid
import threading
import time
from concurrent.futures import ThreadPoolExecutor


@dataclass
class EntityIdentity:
    """Identity and persona of a Santiago entity."""
    entity_id: str
    name: str
    role: str  # e.g., "architect", "developer", "reviewer"
    expertise_domains: List[str]
    personality_traits: Dict[str, float]  # e.g., {"autonomy": 0.8, "collaboration": 0.9}
    created_at: datetime
    trust_score: float = 1.0
    reputation: Dict[str, float] = field(default_factory=dict)  # domain -> score


@dataclass
class KnowledgeItem:
    """A piece of knowledge in the entity's knowledge base."""
    id: str
    domain: str
    content: Any
    confidence: float
    source: str
    timestamp: datetime
    tags: List[str] = field(default_factory=list)
    relationships: Dict[str, List[str]] = field(default_factory=dict)  # type -> related_ids


@dataclass
class Capability:
    """A tool or capability that an entity can execute."""
    name: str
    description: str
    interface: Any  # Could be function, class, or MCP service
    execution_cost: float  # Resource cost to execute
    success_rate: float = 1.0
    last_used: Optional[datetime] = None
    usage_count: int = 0


@dataclass
class Goal:
    """A goal that an entity is working toward."""
    id: str
    description: str
    priority: int
    deadline: Optional[datetime] = None
    dependencies: List[str] = field(default_factory=list)  # goal_ids
    status: str = "pending"  # pending, active, completed, failed
    progress: float = 0.0


@dataclass
class ActionResult:
    """Result of an entity action."""
    success: bool
    result: Any
    execution_time: float
    cost: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class KnowledgeBase:
    """
    In-memory knowledge base for entities.

    This implements the knowledge component of "people-ish" entities.
    """

    def __init__(self):
        self.knowledge: Dict[str, KnowledgeItem] = {}
        self.domain_index: Dict[str, Set[str]] = {}  # domain -> knowledge_ids
        self.tag_index: Dict[str, Set[str]] = {}  # tag -> knowledge_ids
        self.relationship_graph: Dict[str, Dict[str, List[str]]] = {}  # id -> type -> related_ids

    def add_knowledge(self, item: KnowledgeItem):
        """Add knowledge item to the base."""
        self.knowledge[item.id] = item

        # Update domain index
        if item.domain not in self.domain_index:
            self.domain_index[item.domain] = set()
        self.domain_index[item.domain].add(item.id)

        # Update tag index
        for tag in item.tags:
            if tag not in self.tag_index:
                self.tag_index[tag] = set()
            self.tag_index[tag].add(item.id)

        # Update relationship graph
        self.relationship_graph[item.id] = item.relationships

    def query_knowledge(self,
                       domain: str = None,
                       tags: List[str] = None,
                       min_confidence: float = 0.0) -> List[KnowledgeItem]:
        """Query knowledge by domain, tags, and confidence."""
        candidates = set(self.knowledge.keys())

        if domain:
            candidates &= self.domain_index.get(domain, set())

        if tags:
            for tag in tags:
                candidates &= self.tag_index.get(tag, set())

        results = []
        for item_id in candidates:
            item = self.knowledge[item_id]
            if item.confidence >= min_confidence:
                results.append(item)

        return sorted(results, key=lambda x: x.confidence, reverse=True)

    def get_related_knowledge(self, item_id: str, relationship_type: str = None) -> List[KnowledgeItem]:
        """Get knowledge related to a specific item."""
        if item_id not in self.relationship_graph:
            return []

        relationships = self.relationship_graph[item_id]
        related_ids = set()

        if relationship_type:
            related_ids.update(relationships.get(relationship_type, []))
        else:
            for rel_type, ids in relationships.items():
                related_ids.update(ids)

        return [self.knowledge[kid] for kid in related_ids if kid in self.knowledge]

    def update_confidence(self, item_id: str, new_confidence: float):
        """Update confidence score for a knowledge item."""
        if item_id in self.knowledge:
            self.knowledge[item_id].confidence = new_confidence


class CapabilityRegistry:
    """
    Registry of capabilities available to an entity.

    This implements the tool/capability component of "people-ish" entities.
    """

    def __init__(self):
        self.capabilities: Dict[str, Capability] = {}
        self.category_index: Dict[str, Set[str]] = {}  # category -> capability_names

    def register_capability(self, capability: Capability, categories: List[str] = None):
        """Register a capability."""
        self.capabilities[capability.name] = capability

        if categories:
            for category in categories:
                if category not in self.category_index:
                    self.category_index[category] = set()
                self.category_index[category].add(capability.name)

    def get_capability(self, name: str) -> Optional[Capability]:
        """Get a capability by name."""
        return self.capabilities.get(name)

    def discover_capabilities(self, category: str = None) -> List[Capability]:
        """Discover capabilities by category."""
        if not category:
            return list(self.capabilities.values())

        capability_names = self.category_index.get(category, set())
        return [self.capabilities[name] for name in capability_names if name in self.capabilities]

    def update_usage_stats(self, capability_name: str):
        """Update usage statistics for a capability."""
        if capability_name in self.capabilities:
            cap = self.capabilities[capability_name]
            cap.last_used = datetime.now()
            cap.usage_count += 1


class CollaborationNetwork:
    """
    Network of relationships and collaboration patterns for entities.

    This enables the social aspect of "people-ish" entities.
    """

    def __init__(self):
        self.relationships: Dict[str, Dict[str, float]] = {}  # entity_id -> {other_id: trust_score}
        self.collaboration_history: Dict[str, List[Dict]] = {}  # entity_id -> collaboration_records
        self.active_collaborations: Dict[str, Set[str]] = {}  # goal_id -> participating_entity_ids

    def add_relationship(self, entity_a: str, entity_b: str, initial_trust: float = 0.5):
        """Add or update relationship between entities."""
        if entity_a not in self.relationships:
            self.relationships[entity_a] = {}
        if entity_b not in self.relationships:
            self.relationships[entity_b] = {}

        self.relationships[entity_a][entity_b] = initial_trust
        self.relationships[entity_b][entity_a] = initial_trust

    def update_trust(self, entity_a: str, entity_b: str, trust_delta: float):
        """Update trust score between entities."""
        if entity_a in self.relationships and entity_b in self.relationships[entity_a]:
            current_trust = self.relationships[entity_a][entity_b]
            new_trust = max(0.0, min(1.0, current_trust + trust_delta))
            self.relationships[entity_a][entity_b] = new_trust
            self.relationships[entity_b][entity_a] = new_trust

    def get_collaboration_partners(self, entity_id: str, min_trust: float = 0.7) -> List[str]:
        """Get potential collaboration partners for an entity."""
        if entity_id not in self.relationships:
            return []

        partners = []
        for other_id, trust in self.relationships[entity_id].items():
            if trust >= min_trust:
                partners.append(other_id)

        return sorted(partners, key=lambda x: self.relationships[entity_id][x], reverse=True)

    def record_collaboration(self, goal_id: str, participants: List[str], outcome: Dict):
        """Record a collaboration event."""
        for participant in participants:
            if participant not in self.collaboration_history:
                self.collaboration_history[participant] = []
            self.collaboration_history[participant].append({
                'goal_id': goal_id,
                'participants': participants,
                'outcome': outcome,
                'timestamp': datetime.now()
            })

        self.active_collaborations[goal_id] = set(participants)


class SantiagoEntity:
    """
    A "people-ish" entity that combines knowledge, capabilities, and social intelligence.

    This addresses the core question: should Santiagos be modeled as entities with
    both knowledge and tools/capabilities?
    """

    def __init__(self, identity: EntityIdentity):
        self.identity = identity
        self.knowledge_base = KnowledgeBase()
        self.capability_registry = CapabilityRegistry()
        self.collaboration_network = CollaborationNetwork()

        # Goal management
        self.active_goals: Dict[str, Goal] = {}
        self.completed_goals: List[Goal] = []

        # Performance tracking
        self.performance_stats = {
            'total_actions': 0,
            'successful_actions': 0,
            'failed_actions': 0,
            'average_execution_time': 0.0,
            'total_cost': 0.0
        }

        # Communication interfaces
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.response_handlers: Dict[str, asyncio.Future] = {}

    async def reason_and_act(self, goal: Goal) -> ActionResult:
        """
        Core method: unified reasoning and action execution.

        This implements the integration of knowledge and capabilities
        in a "people-ish" entity.
        """
        start_time = datetime.now()
        self.active_goals[goal.id] = goal

        try:
            # Phase 1: Knowledge-driven planning
            relevant_knowledge = self.knowledge_base.query_knowledge(
                domain=goal.description.split()[0].lower(),  # Simple domain extraction
                min_confidence=0.6
            )

            # Phase 2: Capability selection
            required_capabilities = self._identify_required_capabilities(goal, relevant_knowledge)

            # Phase 3: Collaboration assessment
            collaborators = self.collaboration_network.get_collaboration_partners(
                self.identity.entity_id,
                min_trust=0.8
            )

            # Phase 4: Execute plan
            result = await self._execute_plan(goal, required_capabilities, collaborators)

            # Phase 5: Learn from outcome
            self._learn_from_outcome(goal, result)

            # Update performance stats
            execution_time = (datetime.now() - start_time).total_seconds()
            self._update_performance_stats(result.success, execution_time, result.cost)

            goal.status = "completed" if result.success else "failed"
            goal.progress = 1.0
            self.completed_goals.append(goal)
            del self.active_goals[goal.id]

            result.execution_time = execution_time
            return result

        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            goal.status = "failed"
            self.completed_goals.append(goal)
            if goal.id in self.active_goals:
                del self.active_goals[goal.id]

            return ActionResult(
                success=False,
                result=str(e),
                execution_time=execution_time,
                cost=0.0,
                metadata={'exception': type(e).__name__}
            )

    def _identify_required_capabilities(self, goal: Goal, knowledge: List[KnowledgeItem]) -> List[str]:
        """Identify capabilities needed to achieve the goal."""
        # Simple heuristic: extract keywords from goal and match to capabilities
        goal_words = set(goal.description.lower().split())
        required_caps = []

        for cap_name, capability in self.capability_registry.capabilities.items():
            cap_words = set(capability.description.lower().split())
            if goal_words & cap_words:  # Intersection of words
                required_caps.append(cap_name)

        return required_caps

    async def _execute_plan(self,
                          goal: Goal,
                          capabilities: List[str],
                          collaborators: List[str]) -> ActionResult:
        """Execute the planned actions."""
        total_cost = 0.0
        results = []

        for cap_name in capabilities:
            capability = self.capability_registry.get_capability(cap_name)
            if not capability:
                continue

            # Check if we need collaboration
            if collaborators and capability.execution_cost > 0.5:  # Arbitrary threshold
                # Use collaborator (simplified - would need actual communication)
                collaborator = collaborators[0]
                result = await self._collaborate_on_capability(capability, goal, collaborator)
            else:
                # Execute directly
                result = await self._execute_capability(capability, goal)

            results.append(result)
            total_cost += result.cost
            self.capability_registry.update_usage_stats(cap_name)

            if not result.success:
                return ActionResult(
                    success=False,
                    result=f"Failed to execute {cap_name}: {result.result}",
                    execution_time=0.0,
                    cost=total_cost,
                    metadata={'failed_capability': cap_name}
                )

        return ActionResult(
            success=True,
            result={'executed_capabilities': capabilities, 'results': results},
            execution_time=0.0,
            cost=total_cost
        )

    async def _execute_capability(self, capability: Capability, goal: Goal) -> ActionResult:
        """Execute a single capability."""
        try:
            # Simplified execution - in reality would call the capability interface
            if asyncio.iscoroutinefunction(capability.interface):
                result = await capability.interface(goal)
            else:
                result = capability.interface(goal)

            return ActionResult(
                success=True,
                result=result,
                execution_time=0.1,  # Mock
                cost=capability.execution_cost
            )
        except Exception as e:
            return ActionResult(
                success=False,
                result=str(e),
                execution_time=0.1,
                cost=capability.execution_cost
            )

    async def _collaborate_on_capability(self,
                                       capability: Capability,
                                       goal: Goal,
                                       collaborator_id: str) -> ActionResult:
        """Collaborate with another entity on a capability."""
        # Simplified collaboration - would need actual inter-entity communication
        # For now, just execute locally but mark as collaborative
        result = await self._execute_capability(capability, goal)
        result.metadata = result.metadata or {}
        result.metadata['collaborator'] = collaborator_id
        return result

    def _learn_from_outcome(self, goal: Goal, result: ActionResult):
        """Learn from the outcome to improve future performance."""
        # Update knowledge confidence based on success
        related_knowledge = self.knowledge_base.query_knowledge(
            domain=goal.description.split()[0].lower()
        )

        confidence_adjustment = 0.1 if result.success else -0.1
        for item in related_knowledge:
            new_confidence = max(0.0, min(1.0, item.confidence + confidence_adjustment))
            self.knowledge_base.update_confidence(item.id, new_confidence)

    def _update_performance_stats(self, success: bool, execution_time: float, cost: float):
        """Update performance statistics."""
        self.performance_stats['total_actions'] += 1
        if success:
            self.performance_stats['successful_actions'] += 1
        else:
            self.performance_stats['failed_actions'] += 1

        # Update average execution time
        total_actions = self.performance_stats['total_actions']
        current_avg = self.performance_stats['average_execution_time']
        self.performance_stats['average_execution_time'] = (
            (current_avg * (total_actions - 1) + execution_time) / total_actions
        )

        self.performance_stats['total_cost'] += cost

    # Communication interfaces for fast inter-entity communication
    async def send_message(self, target_entity_id: str, message: Dict[str, Any]) -> str:
        """Send message to another entity (fast in-memory interface)."""
        message_id = str(uuid.uuid4())
        full_message = {
            'id': message_id,
            'from': self.identity.entity_id,
            'to': target_entity_id,
            'content': message,
            'timestamp': datetime.now()
        }

        # In a real system, this would use shared memory or fast IPC
        # For demo, we'll use a global message bus (simplified)
        await self._send_to_entity(target_entity_id, full_message)
        return message_id

    async def receive_message(self) -> Dict[str, Any]:
        """Receive message from another entity."""
        return await self.message_queue.get()

    async def _send_to_entity(self, target_id: str, message: Dict[str, Any]):
        """Internal method to send message (would use fast interface)."""
        # Placeholder for fast interface implementation
        # In real system: shared memory, memory-mapped files, or direct memory access
        pass

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get entity performance statistics."""
        return {
            **self.performance_stats,
            'active_goals': len(self.active_goals),
            'completed_goals': len(self.completed_goals),
            'knowledge_items': len(self.knowledge_base.knowledge),
            'capabilities': len(self.capability_registry.capabilities),
            'relationships': len(self.collaboration_network.relationships.get(self.identity.entity_id, {}))
        }


# Fast Interface Implementations for System of Systems

class SharedMemorySpace:
    """
    Fast shared memory space for inter-entity communication.

    This addresses: "What are the fastest interfaces in an in-memory system of systems?"
    """

    def __init__(self):
        self._lock = threading.Lock()
        self._spaces: Dict[str, Any] = {}
        self._subscribers: Dict[str, Set[str]] = {}  # space_name -> entity_ids

    def create_space(self, name: str, initial_data: Any = None) -> bool:
        """Create a new shared memory space."""
        with self._lock:
            if name in self._spaces:
                return False
            self._spaces[name] = initial_data or {}
            self._subscribers[name] = set()
            return True

    def write_to_space(self, space_name: str, key: str, value: Any, entity_id: str):
        """Write to shared memory space (very fast)."""
        with self._lock:
            if space_name not in self._spaces:
                return False
            if not isinstance(self._spaces[space_name], dict):
                return False

            self._spaces[space_name][key] = value
            # Notify subscribers (async in real implementation)
            return True

    def read_from_space(self, space_name: str, key: str = None) -> Any:
        """Read from shared memory space (very fast)."""
        with self._lock:
            if space_name not in self._spaces:
                return None
            space = self._spaces[space_name]
            return space.get(key) if key else space

    def subscribe_to_space(self, space_name: str, entity_id: str):
        """Subscribe to changes in a memory space."""
        with self._lock:
            if space_name in self._subscribers:
                self._subscribers[space_name].add(entity_id)


class MemoryMappedInterface:
    """
    Memory-mapped interface for zero-copy data transfer between entities.
    """

    def __init__(self):
        self._mappings: Dict[str, memoryview] = {}
        self._executor = ThreadPoolExecutor(max_workers=4)

    def create_mapping(self, name: str, size: int) -> bool:
        """Create a memory mapping."""
        # Simplified - real implementation would use mmap
        try:
            # Simulate memory mapping
            self._mappings[name] = memoryview(bytearray(size))
            return True
        except Exception:
            return False

    def write_to_mapping(self, mapping_name: str, offset: int, data: bytes) -> bool:
        """Write data to memory mapping (zero-copy)."""
        if mapping_name not in self._mappings:
            return False

        mapping = self._mappings[mapping_name]
        if offset + len(data) > len(mapping):
            return False

        mapping[offset:offset + len(data)] = data
        return True

    def read_from_mapping(self, mapping_name: str, offset: int, size: int) -> bytes:
        """Read data from memory mapping (zero-copy)."""
        if mapping_name not in self._mappings:
            return b''

        mapping = self._mappings[mapping_name]
        if offset + size > len(mapping):
            size = len(mapping) - offset

        return bytes(mapping[offset:offset + size])


# Example usage and testing
async def demo_entity_architecture():
    """Demonstrate Santiago entity architecture."""

    # Create entity identity
    identity = EntityIdentity(
        entity_id="entity_001",
        name="Alex",
        role="architect",
        expertise_domains=["software_architecture", "system_design"],
        personality_traits={"autonomy": 0.8, "collaboration": 0.9, "creativity": 0.7},
        created_at=datetime.now()
    )

    # Create entity
    entity = SantiagoEntity(identity)

    # Add some knowledge
    knowledge = KnowledgeItem(
        id="arch_001",
        domain="software_architecture",
        content="Microservices enable independent scaling and deployment",
        confidence=0.9,
        source="experience",
        timestamp=datetime.now(),
        tags=["microservices", "scalability"]
    )
    entity.knowledge_base.add_knowledge(knowledge)

    # Add capabilities
    async def design_system(goal: Goal):
        return {"design": f"Designed system for: {goal.description}"}

    design_capability = Capability(
        name="system_design",
        description="Design software systems and architectures",
        interface=design_system,
        execution_cost=0.3
    )
    entity.capability_registry.register_capability(design_capability, ["design", "architecture"])

    # Create and execute a goal
    goal = Goal(
        id="goal_001",
        description="Design a scalable microservices architecture",
        priority=2,
        deadline=datetime.now().replace(hour=datetime.now().hour + 1)
    )

    result = await entity.reason_and_act(goal)
    print(f"Goal execution result: {result.success}")
    print(f"Result details: {result.result}")

    # Check performance stats
    stats = entity.get_performance_stats()
    print(f"Entity stats: {stats}")

    # Demonstrate fast interfaces
    shared_space = SharedMemorySpace()
    shared_space.create_space("collaboration_space")
    shared_space.write_to_space("collaboration_space", "current_goal", goal.id, entity.identity.entity_id)

    data = shared_space.read_from_space("collaboration_space")
    print(f"Shared memory data: {data}")


if __name__ == "__main__":
    asyncio.run(demo_entity_architecture())