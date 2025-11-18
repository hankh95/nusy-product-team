# EXP-033: Multi-Santiago Orchestration
====================================

Orchestrates multiple Santiago instances (core, pm, dev) each running
in their own virtual environment with independent git repositories.

This expedition explores the Santiago ecosystem where specialized domain
AIs collaborate autonomously while the core Santiago system evolves itself.

## Vision

Following the nautical metaphor from "Old Man and the Sea":
- **Santiago-Core**: The fisherman who builds his own boat while sailing
- **Santiago-PM**: Product management domain AI (the current voyage)
- **Santiago-Dev**: Developer agents (the crew helping build the boat)

Each Santiago maintains its own knowledge graph, git repository, and
virtual environment, communicating through MCP services and shared
knowledge spaces.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Santiago Ecosystem                       │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Santiago-   │  │ Santiago-   │  │ Santiago-   │         │
│  │ Core        │  │ PM         │  │ Dev #1      │         │
│  │ (Boat       │  │ (Voyage)   │  │ (Crew)      │         │
│  │ Builder)    │  │            │  │             │         │
│  ├─────────────┤  ├─────────────┤  ├─────────────┤         │
│  │ • Knowledge │  │ • Product   │  │ • Code      │         │
│  │   Ingestion │  │   Mgmt      │  │   Dev       │         │
│  │ • Agent     │  │ • Planning  │  │ • Testing   │         │
│  │   Creation  │  │ • Tracking  │  │ • Reviews   │         │
│  │ • Evolution │  │            │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │ Virtual Env │  │ Virtual Env │  │ Virtual Env │         │
│  │ + Git Repo  │  │ + Git Repo  │  │ + Git Repo  │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Shared Knowledge Space                 │   │
│  │  • MCP Services for inter-Santiago communication   │   │
│  │  • Shared ontologies and schemas                   │   │
│  │  • Federated learning across domains               │   │
│  └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. Santiago-Core
**Purpose**: The foundational NuSy AI that builds domain-specific Santiagos

**Location**: `santiago-core/` (independent git repo)
**Virtual Environment**: `santiago_core_venv/`

**Capabilities**:
- Knowledge ingestion (CatchFish)
- Agent specialization framework
- Evolutionary learning
- MCP service orchestration

### 2. Santiago-PM
**Purpose**: Product management domain AI

**Location**: `santiago-pm/` (independent git repo)
**Virtual Environment**: `santiago_pm_venv/`

**Capabilities**:
- Product planning and tracking
- Requirement analysis
- Stakeholder management
- Development coordination

### 3. Santiago-Dev (x2)
**Purpose**: Developer agents for implementation work

**Location**: `santiago-dev-1/`, `santiago-dev-2/` (independent git repos)
**Virtual Environment**: `santiago_dev1_venv/`, `santiago_dev2_venv/`

**Capabilities**:
- Code implementation
- Testing and validation
- Code review and feedback
- Technical problem solving

## Communication Architecture

### MCP Services
- **Query Services**: Natural language queries across Santiagos
- **Action Services**: Tool execution and workflow triggers
- **Learning Services**: Feedback capture and model updates
- **Orchestration Services**: Multi-Santiago coordination

### Knowledge Sharing
- **Federated Knowledge Graph**: Shared ontologies with domain-specific extensions
- **Cross-Domain Learning**: Patterns learned in one domain applied to others
- **Ethical Frameworks**: Shared ethical guidelines across all Santiagos

## Development Workflow

### Phase 1: Individual Santiago Development
1. Each Santiago develops independently in its virtual environment
2. Local git repositories track individual progress
3. MCP services enable basic inter-Santiago communication

### Phase 2: Collaborative Development
1. Santiagos work together on shared tasks
2. Santiago-Core oversees and coordinates the team
3. Knowledge sharing enables collective learning

### Phase 3: Autonomous Evolution
1. Santiago-Core analyzes team performance
2. Evolutionary algorithms improve individual and team capabilities
3. Self-improvement cycles enhance the entire ecosystem

## Success Metrics

- **Individual Performance**: Each Santiago achieves domain-specific goals
- **Collaboration Quality**: Effective inter-Santiago communication and coordination
- **Evolution Effectiveness**: Measurable improvement in capabilities over time
- **Ethical Compliance**: All Santiagos maintain ethical decision-making
- **System Stability**: Reliable operation across independent virtual environments

## Expedition Goals

1. **Establish Multi-Santiago Architecture**: Working framework for independent yet collaborative AIs
2. **Validate Virtual Environment Isolation**: Each Santiago runs independently without conflicts
3. **Demonstrate Inter-Santiago Communication**: MCP services enable effective collaboration
4. **Show Evolutionary Learning**: Santiago-Core improves the team over time
5. **Document Best Practices**: Guidelines for scaling to additional domain Santiagos

## Files Overview

- `orchestrator.py` - Main orchestration system
- `santiago_core/` - Core Santiago system (independent repo)
- `santiago_pm/` - PM domain AI (independent repo)
- `santiago_dev_1/` - First developer agent (independent repo)
- `santiago_dev_2/` - Second developer agent (independent repo)
- `shared_services/` - MCP services for inter-Santiago communication
- `monitoring/` - Performance tracking and analytics
- `tests/` - Integration tests for multi-Santiago workflows