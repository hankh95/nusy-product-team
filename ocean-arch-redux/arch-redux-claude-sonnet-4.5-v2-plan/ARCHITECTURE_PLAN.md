# Architecture Plan — 2025-11-16

**Metadata**
Model Name: Claude Sonnet 4.5
Model Version: claude-sonnet-4.5-20250514
Date: 2025-11-16
Repo Commit SHA: 5bfcc00
Run ID: arch-redux-claude-sonnet-4.5-2025-11-16

## Current Architecture

The `nusy-product-team` repository contains a **transitional architecture** with multiple architectural phases represented:

**Core Runtime (ARCHIVED)**
- `src/nusy_pm_core/` contains a prototype FastAPI orchestrator (archived via tag `prototype-archive-2025-11-16`)
- This service attempted to provide NuSy knowledge graph endpoints but is no longer active code

**Santiago Agent Framework (ACTIVE)**
- `santiago_core/` implements an autonomous agent framework with:
  - Base `SantiagoAgent` class with ethical oversight
  - Three role implementations: PM, Architect, Developer
  - `SantiagoTeamCoordinator` for message-based communication
  - Local async/await agent execution patterns
  - Knowledge graph service (`santiago_core/services/knowledge_graph.py`)

**Limitations of Current State**
- Agents run as local Python classes, not as MCP services
- No standardized MCP manifests declaring capabilities, skill levels, or knowledge scopes
- **Missing `knowledge/` folder at repository root** (GAP) — no shared team memory structure
- Agents lack formal contracts for:
  - Shared working agreements
  - Team roster and capability discovery
  - Ships logs for tracking evolutionary decisions
- No DGX deployment runbooks or infrastructure automation
- Concurrency patterns exist but lack formal ethics gating and policy enforcement
- Knowledge graph interaction is service-based but lacks:
  - Queued/batched write patterns
  - Provenance tracking
  - Schema validation layers

## Target Architecture

The target "Manolin Cluster" architecture transforms the current local-agent system into a **production-grade, MCP-based multi-agent platform** designed for DGX Spark deployment:

**1. MCP-Based Role Services**

Each Santiago role becomes an independent MCP service with:
- Formal MCP manifest declaring:
  - Role identity (PM, Ethicist, Architect-NuSy, Architect-Systems, Developer, QA, UX, Platform)
  - Skill level: Apprentice / Journeyman / Master
  - Knowledge scope: Pond / Lake / Sea / Ocean
  - Tool permissions and capabilities
- Service endpoints exposing:
  - `status`, `capabilities`, `request_help`
  - Role-specific tools (e.g., PM: `read_working_agreements`, `propose_evolution_cycle`)
- Session isolation for concurrent operation

**2. Shared Team Memory (knowledge/ Tree)**

A structured knowledge repository at the repository root:
```
knowledge/
  shared/
    working-agreements.md
    bdd-practices.md
    tools-and-mcp-capabilities.md
    team-roster-and-capabilities.ttl
    ships-log/
      YYYY-MM-DD-<slug>.md
  domains/
    pm/
    ethics/
    architecture/
    development/
```

This provides:
- Persistent, version-controlled team memory
- Cross-session continuity for all agents
- Clear separation of shared vs domain-specific knowledge
- Discoverable contracts and working agreements

**3. NuSy Orchestrator Evolution**

The orchestrator (successor to archived `src/nusy_pm_core/`) becomes:
- FastAPI MCP gateway coordinating all role services
- Request router with:
  - Session management
  - **Ethics & Concurrency Gating** enforcement
  - Tool invocation coordination
  - Logging and observability per role/session
- Integration points:
  - Shared LLM runtime (vLLM/Transformers serving Mistral-7B-Instruct)
  - Unified KG interaction layer
  - Vector DB (Qdrant/pgvector)
  - Git forge, PM tools, CI/CD

**4. Unified Knowledge Graph Interaction Layer**

A new abstraction replacing direct KG service calls:
- **Queued/batched writes** to prevent conflicts during concurrent agent operations
- **Provenance tracking** recording which agent made which KG modifications
- **Schema validation** ensuring all KG updates conform to NuSy ontology
- Read-optimized paths for fast agent queries
- Write coordination with conflict detection

**5. DGX Spark / Manolin Deployment**

Infrastructure for production deployment:
- DGX Spark with 128 GB unified memory, 4 TB internal NVMe
- External NVMe RAID (8-16 TB) for:
  - Model checkpoints (Mistral-7B-Instruct variants)
  - KG snapshots and vector indexes
  - Experiment artifacts and logs
- Single shared model instance serving 10+ concurrent Santiago agents
- Deployment automation scripts:
  - Model provisioning
  - Service orchestration (Docker Compose or Kubernetes)
  - Backup and recovery procedures

**6. Ethics & Concurrency Infrastructure**

Formal enforcement layer for multi-agent safety:
- **Santiago-Ethicist** as first-class MCP service monitoring:
  - Proposed evolutionary changes
  - New role/tool additions
  - Data sensitivity patterns
- **Ethics & Concurrency Gating** in orchestrator:
  - Pre-execution review of high-risk operations
  - Concurrent write coordination
  - Audit logging of all autonomous decisions
- Test harness covering:
  - Session isolation (no context leakage)
  - Tool invocation race conditions
  - Load profiles and SLO validation

## Key Deltas

**1. MCP Service Migration**
- **From:** Local Python agent classes with message passing
- **To:** Independent MCP services with formal manifests and capability declarations
- **Rationale:** Enables standardized discovery, composition, and evolution of agent capabilities per `ocean-research/features-capabilities-for-shared-memory-and-evolution.md`

**2. Shared Knowledge Architecture**
- **From:** No centralized team memory; knowledge scattered across notes/ and santiago_core/
- **To:** Structured `knowledge/` tree with shared working agreements, team roster (RDF), and ships logs
- **Rationale:** Provides cross-session persistence, enables agents to discover "how we work" without relying on context windows

**3. Ethics & Concurrency Gating**
- **From:** Built-in ethical oversight in individual agents but no orchestrator-level policy enforcement
- **To:** Santiago-Ethicist MCP service + orchestrator gating layer with formal review workflows
- **Rationale:** Satisfies concurrency safety requirements from `ocean-research/nusy_manolin_multi_agent_test_plans.md`; prevents conflicts during parallel agent operations

**4. Unified KG Interaction Layer**
- **From:** Direct service calls to `santiago_core/services/knowledge_graph.py`
- **To:** Queued write layer with provenance tracking and schema validation
- **Rationale:** Reduces risk of KG corruption during concurrent updates; enables audit trails for autonomous decisions

**5. DGX Deployment Readiness**
- **From:** Local development environment assumptions; no production infrastructure automation
- **To:** DGX Spark provisioning scripts, storage layout specifications, model serving patterns
- **Rationale:** Aligns with `ocean-research/building-on-DGX/dgx_spark_nusy_report.md` recommendations for 10-agent Santiago team on shared Mistral-7B-Instruct

**6. Orchestrator Refactoring**
- **From:** Archived prototype runtime without MCP integration
- **To:** Production FastAPI orchestrator coordinating MCP services with session management and policy enforcement
- **Rationale:** Provides scalable foundation per `ocean-research/nusy_manolin_architecture.md` execution layer design

**7. Skill Level & Knowledge Scope Formalization**
- **From:** Implicit agent capabilities
- **To:** Explicit metadata in MCP manifests (Apprentice/Journeyman/Master, Pond/Lake/Sea/Ocean)
- **Rationale:** Enables composition of smaller Santiago packages and evolutionary capability growth

### References Cited

- ocean-research/nusy_manolin_architecture.md
- ocean-research/building-on-DGX/dgx_spark_nusy_report.md
- ocean-research/nusy_manolin_multi_agent_test_plans.md
- ocean-research/features-capabilities-for-shared-memory-and-evolution.md
- ocean-research/fake_team_pack/fake_team_feature_plan.md
