# Folder Layout Proposal — 2025-11-16

**Metadata**
Model Name: Claude Sonnet 4.5
Model Version: claude-sonnet-4.5-20250514
Date: 2025-11-16
Repo Commit SHA: 5bfcc00
Run ID: arch-redux-claude-sonnet-4.5-2025-11-16

## Proposed Tree

```
knowledge/
  shared/
    working-agreements.md
    bdd-practices.md
    tools-and-mcp-capabilities.md
    team-roster-and-capabilities.ttl
    ships-log/
      2025-11-16-migration-launch.md
      YYYY-MM-DD-<slug>.md
  domains/
    pm/
      strategy-patterns.md
      hypothesis-templates.md
    ethics/
      evolution-reviews.md
      risk-assessment-rubric.md
    architecture/
      nusy-ontology/
      system-patterns/
    development/
      code-standards.md
      test-patterns.md
    qa/
      coverage-metrics.md
    ux/
      journey-maps/
    platform/
      deployment-runbooks/

santiago_core/
  agents/
    pm/
      service/
        main.py
        mcp_endpoints.py
      __init__.py
    ethicist/
      service/
        main.py
        review_engine.py
    architect_nusy/
      service/
    architect_systems/
      service/
    developer/
      service/
    qa/
      service/
    ux/
      service/
    platform/
      service/
  core/
    agent_framework.py
    team_coordinator.py
  services/
    knowledge_graph.py
    kg_queue.py
    kg_provenance.py
    kg_validator.py
    mcp_adapter.py
  interfaces/

mcp/
  registry/
    manifest-schema.json
  manifests/
    pm.json
    ethicist.json
    architect-nusy.json
    architect-systems.json
    developer.json
    qa.json
    ux.json
    platform.json

nusy_orchestrator/
  main.py
  session_manager.py
  ethics_gate.py
  mcp_router.py
  config/
    policies.yaml
    slo-targets.yaml

infra/
  dgx/
    provision.sh
    docker-compose.yml
    storage-layout.md
    runbooks/
      deployment.md
      scaling.md
      backup-restore.md
      monitoring.md
  local-dev/
    docker-compose.dev.yml

tests/
  concurrency/
    test_session_isolation.py
    test_tool_races.py
    load_profiles.py
  integration/
  unit/

scaffolds/
  mcp-manifest-template.json
  roster-entry-template.ttl
  evolution-cycle-template.md
```

## Mapping Table

| Current Path | Target Path | Action |
|--------------|-------------|--------|
| `santiago_core/agents/santiago_pm.py` | `santiago_core/agents/pm/service/main.py` | Refactor: Convert to MCP service architecture with manifest in `mcp/manifests/pm.json` |
| `santiago_core/agents/santiago_architect.py` | `santiago_core/agents/architect_nusy/service/` AND `santiago_core/agents/architect_systems/service/` | Split: Separate NuSy-focused and Systems-focused architect concerns |
| `santiago_core/agents/santiago_developer.py` | `santiago_core/agents/developer/service/main.py` | Refactor: Convert to MCP service with manifest |
| `santiago_core/services/knowledge_graph.py` | `santiago_core/services/knowledge_graph.py` (refactored) | Extract: Move queuing, provenance, and validation logic to separate modules (`kg_queue.py`, `kg_provenance.py`, `kg_validator.py`) |
| `santiago_core/core/agent_framework.py` | `santiago_core/core/agent_framework.py` (retain) | Retain: Keep as base class for MCP services |
| `santiago_core/core/team_coordinator.py` | `santiago_core/core/team_coordinator.py` (deprecate orchestration, retain utilities) | Consolidate: Orchestration moves to `nusy_orchestrator/`; retain shared utilities |
| `src/nusy_pm_core/` | N/A (archived) | Deprecate: Already archived with tag `prototype-archive-2025-11-16`; do not migrate |
| `notes/` | `notes/` (retain for historical context) | Retain: Keep as reference but transition active decision tracking to `knowledge/shared/ships-log/` |
| `DEVELOPMENT_PRACTICES.md` | `DEVELOPMENT_PRACTICES.md` (retain) AND extract key sections to `knowledge/shared/working-agreements.md` | Extract: Formalize practices into `knowledge/shared/` for agent consumption while keeping human-readable doc |
| `santiago-code/` | N/A (archived) | Deprecate: Historical reference only per `DEVELOPMENT_PRACTICES.md` |
| N/A | `knowledge/` | Create: New shared team memory structure with domains and ships logs |
| N/A | `mcp/registry/` | Create: MCP manifest storage and schema definitions |
| N/A | `nusy_orchestrator/` | Create: Production FastAPI orchestrator with session management and ethics gating |
| N/A | `infra/dgx/` | Create: DGX Spark deployment automation and runbooks |
| N/A | `tests/concurrency/` | Create: Multi-agent concurrency test harness |
| N/A | `scaffolds/` | Create: Reusable templates for MCP manifests, RDF roster entries, and evolution cycles |

## Notes

**Agent Service Structure**

Each role's agent directory follows the pattern:
```
santiago_core/agents/<role>/
  service/
    main.py          # FastAPI or similar MCP service entry point
    <role>_logic.py  # Domain-specific reasoning and tool implementations
  __init__.py        # Package marker
```

This structure:
- Isolates each role as an independent service
- Enables separate deployment and scaling
- Maintains clear boundaries between role responsibilities

**MCP Manifest Organization**

The `mcp/manifests/` directory stores JSON files declaring:
- Role identity and metadata
- Skill level (Apprentice/Journeyman/Master)
- Knowledge scope (Pond/Lake/Sea/Ocean)
- Tool definitions with input/output contracts
- Dependencies on other services

This enables:
- Dynamic service discovery
- Capability-based routing in the orchestrator
- Evolutionary tracking of agent capabilities

**Knowledge Domain Separation**

The `knowledge/domains/` structure separates:
- `pm/` — Product management strategies, templates, patterns
- `ethics/` — Evolution reviews, risk assessments, ethical guidelines
- `architecture/` — Ontology definitions, system design patterns
- `development/` — Code standards, test patterns
- `qa/`, `ux/`, `platform/` — Role-specific domain knowledge

This allows:
- Domain experts (Santiago agents) to own their knowledge areas
- Clear boundaries for knowledge updates
- Parallel evolution of different domains

**Orchestrator vs Team Coordinator**

The migration separates concerns:
- **`nusy_orchestrator/`** handles:
  - HTTP/MCP protocol serving
  - Session lifecycle management
  - Ethics gating and policy enforcement
  - Service discovery and routing
- **`santiago_core/core/team_coordinator.py`** becomes:
  - Utility library for agent-to-agent communication patterns
  - Shared abstractions for task coordination
  - No longer responsible for HTTP serving

**Infrastructure Readiness**

The `infra/` structure provides:
- **`dgx/`** — Production DGX Spark deployment with provisioning automation and operational runbooks
- **`local-dev/`** — Docker Compose configurations for local development without DGX hardware
- Clear separation between production and development infrastructure concerns

### References Cited

- ocean-research/nusy_manolin_architecture.md
- ocean-research/building-on-DGX/dgx_spark_nusy_report.md
- ocean-research/features-capabilities-for-shared-memory-and-evolution.md
