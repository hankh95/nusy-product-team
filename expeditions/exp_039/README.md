# EXP-039: Santiago Entity Architecture

## Overview
Explore the fundamental architecture of Santiago entities - whether they should be "people-ish" constructs with both knowledge and capabilities, how to implement fast in-memory interfaces between system components, and the role of MCP (Model Context Protocol) in enabling expert collaboration.

## Core Questions to Answer

### 1. MCP as Santiago-PM Capability
**Question**: Should Git and other tools be wrapped as Santiago-PM MCP capabilities?
- How does MCP enable experts to work both on the team and as hireable services?
- What architectural patterns emerge from treating tools as MCP services?
- How does this affect the boundary between core reasoning and tool execution?

### 2. Knowledge Flow & Common Capabilities
**Question**: How does the core's knowledge hub expose common capabilities to domain experts?
- What shared capabilities should all domain experts have access to?
- How are capabilities discovered and invoked across the system?
- What interfaces enable seamless capability sharing?

### 3. Santiago as People-ish Entities
**Question**: Should Santiagos be modeled as entities with both knowledge and tools/capabilities?
- What does a "people-ish" entity architecture look like?
- How do knowledge and capabilities integrate within a single entity?
- What are the fastest interfaces in an in-memory system of systems?

## Success Metrics
- ✅ Clear architectural decision on MCP vs direct service integration
- ✅ Defined common capability interfaces for domain experts
- ✅ Entity model that balances knowledge and tool integration
- ✅ Performance benchmarks for different interface approaches
- ✅ Prototype implementation demonstrating chosen architecture

## Architectural Exploration Areas

### MCP Service Model
**Current Thinking**: Git as direct service vs MCP-wrapped capability
- **Direct Service**: Tight coupling, high performance, complex integration
- **MCP Service**: Loose coupling, discoverable, expert-hireable, standardized interface

**Questions**:
- Does MCP enable the "expert marketplace" vision?
- How does MCP affect system performance vs direct calls?
- What capabilities should be MCP-wrapped vs directly integrated?

### Common Capability Interfaces
**Core Capabilities** that all entities should expose:
- Knowledge Query Interface
- Tool Execution Interface
- Learning/Adaptation Interface
- Collaboration Interface
- Health/Monitoring Interface

**Discovery Mechanisms**:
- Capability registries
- Dynamic interface negotiation
- Version compatibility checking

### Entity Architecture Patterns
**People-ish Entity Characteristics**:
- **Identity**: Unique persona, expertise profile, relationship network
- **Knowledge**: Domain expertise, learning history, confidence models
- **Capabilities**: Tool access, execution permissions, resource limits
- **Social**: Communication patterns, collaboration preferences, trust models

**Interface Speed Considerations**:
- Memory-mapped communication
- Shared object spaces
- Message passing vs direct calls
- Async vs sync interfaces

## Implementation Phases

### Phase 1: MCP Service Architecture (Week 1)
- Design MCP wrapper for Git service
- Implement service discovery and invocation
- Compare performance vs direct integration
- Prototype expert marketplace concept

### Phase 2: Common Capability Interfaces (Week 2)
- Define core capability interfaces
- Implement capability registries
- Test cross-entity capability sharing
- Validate interface performance

### Phase 3: Entity Model Design (Week 3)
- Design people-ish entity architecture
- Implement knowledge-capability integration
- Test entity collaboration patterns
- Benchmark interface speeds

### Phase 4: Integration & Validation (Week 4)
- Integrate with EXP-038 Santiago Core
- Test full entity ecosystem
- Performance optimization
- Architecture documentation

## Expected Learnings

### MCP Architectural Insights
- **Service Boundaries**: When to use MCP vs direct integration
- **Expert Marketplace**: How MCP enables flexible expert collaboration
- **Performance Trade-offs**: MCP overhead vs development velocity
- **Standardization Benefits**: Common interfaces across different tools

### Capability Interface Patterns
- **Common Capabilities**: What all entities need vs domain-specific needs
- **Interface Design**: Fast, reliable, discoverable capability access
- **Resource Management**: Capability limits and fair sharing
- **Evolution**: How capabilities upgrade without breaking interfaces

### Entity Design Principles
- **People-ish Balance**: Right mix of autonomy, collaboration, and oversight
- **Knowledge-Tool Integration**: Seamless flow between reasoning and execution
- **Interface Performance**: Fastest communication patterns for in-memory systems
- **Scalability**: How entity architecture scales with system complexity

## Technical Implementation

### MCP Service Layer
```python
class MCPService:
    """MCP wrapper for any capability."""
    def __init__(self, capability_name: str, implementation: Any):
        self.name = capability_name
        self.implementation = implementation
        self.interface_contract = self._generate_contract()
    
    async def invoke(self, request: MCPRequest) -> MCPResponse:
        """Standardized MCP invocation."""
        # Contract validation, execution, response formatting
        pass
```

### Entity Architecture
```python
class SantiagoEntity:
    """People-ish entity with knowledge and capabilities."""
    def __init__(self, identity: EntityIdentity):
        self.identity = identity
        self.knowledge_base = KnowledgeBase()
        self.capability_registry = CapabilityRegistry()
        self.collaboration_network = CollaborationNetwork()
    
    async def reason_and_act(self, goal: Goal) -> ActionResult:
        """Unified reasoning and action execution."""
        # Knowledge-driven planning + capability execution
        pass
```

### Fast Interface Patterns
- **Shared Memory Spaces**: Direct object sharing between entities
- **Memory-Mapped Communication**: Zero-copy data transfer
- **Async Message Buses**: High-throughput event-driven communication
- **Capability Proxies**: Lazy-loaded, cached capability access

## Risk Mitigation
- **Performance Regression**: Careful benchmarking of MCP vs direct calls
- **Interface Complexity**: Start with minimal interfaces, expand gradually
- **Entity Coupling**: Design for loose coupling between entities
- **Capability Conflicts**: Clear ownership and conflict resolution

## Success Criteria
- Clear architectural direction on MCP integration
- Defined common capability interfaces
- Entity model that enables flexible collaboration
- Performance data on interface approaches
- Prototype demonstrating expert marketplace concept

## Files Created
- `expeditions/exp_039/mcp_service_layer.py` - MCP wrapper implementations
- `expeditions/exp_039/entity_architecture.py` - People-ish entity design
- `expeditions/exp_039/capability_interfaces.py` - Common capability interfaces
- `expeditions/exp_039/interface_benchmarks.py` - Performance testing
- `expeditions/exp_039/README.md` - This documentation

## Dependencies
- EXP-038 Santiago Core (for integration testing)
- EXP-036 components (Git, workflow, LLM services)
- Python async frameworks
- Performance benchmarking tools

## Connection to Overall Vision
This expedition addresses fundamental architectural questions that will shape how Santiago entities collaborate, how capabilities are shared, and how the system scales. The answers here will guide the integration of EXP-036 components and the evolution toward a full autonomous development ecosystem.</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/exp_039/README.md