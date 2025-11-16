# Folder Layout Proposal

## Proposed Directory Tree

```text
knowledge/
├── catches/
│   ├── santiago-pm-safe-xp/
│   │   ├── domain-knowledge/
│   │   │   ├── safe-framework.md
│   │   │   ├── xp-practices.md
│   │   │   └── pm-workflows.yaml
│   │   ├── bdd-tests/
│   │   │   ├── backlog-management.feature
│   │   │   ├── release-planning.feature
│   │   │   └── stakeholder-communication.feature
│   │   ├── mcp-manifest.json
│   │   └── provenance.yaml
│   ├── santiago-architect-nusy/
│   ├── santiago-developer/
│   └── index.yaml
├── templates/
│   ├── catch-package-template/
│   │   ├── domain-knowledge/
│   │   ├── bdd-tests/
│   │   ├── mcp-manifest.json
│   │   └── provenance.yaml
│   └── proxy-template/
└── proxy-instructions/
    ├── pm-role.md
    ├── architect-role.md
    ├── developer-role.md
    ├── qa-role.md
    ├── ux-role.md
    ├── platform-role.md
    └── ethicist-role.md

santiago_core/
├── agents/
│   ├── _proxy/
│   │   ├── __init__.py
│   │   ├── pm_proxy.py
│   │   ├── architect_proxy.py
│   │   ├── developer_proxy.py
│   │   ├── qa_proxy.py
│   │   ├── ux_proxy.py
│   │   ├── platform_proxy.py
│   │   └── ethicist_proxy.py
│   └── santiago-pm-safe-xp/
│       └── service/
│           ├── __init__.py
│           ├── tools.py
│           └── manifest.json
└── orchestrator/
    ├── ethics/
    │   ├── __init__.py
    │   └── gating.py
    └── concurrency/
        ├── __init__.py
        ├── session_isolation.py
        └── tool_locking.py

nusy_orchestrator/
└── santiago_builder/
    ├── __init__.py
    ├── navigator.py
    ├── catchfish.py
    ├── fishnet.py
    ├── pipelines/
    │   ├── __init__.py
    │   ├── provenance_queue.py
    │   ├── kg_writer.py
    │   └── schema_validator.py
    └── tests/
        ├── test_navigator.py
        ├── test_catchfish.py
        └── test_fishnet.py

ships-logs/
└── expeditions/
    ├── 2025-11-16-first-pm-catch.md
    ├── 2025-11-20-architect-catch.md
    └── 2025-11-25-developer-catch.md
```

## Mapping Table

| Current Path | Target Path | Action | Rationale |
|-------------|-------------|--------|-----------|
| _missing_ (`knowledge/`) | `knowledge/` | **Create** | Root directory for all factory outputs (catches, templates, proxy instructions) |
| _missing_ | `knowledge/catches/<santiago-name>/` | **Create** | Storage for generated Santiagos with domain-knowledge/, bdd-tests/, manifest, provenance |
| _missing_ | `knowledge/templates/` | **Create** | Base structures for generating new catches |
| _missing_ | `knowledge/proxy-instructions/` | **Create** | Role definitions for fake team MCP proxies |
| `santiago_core/agents/` | `santiago_core/agents/_proxy/` | **Refactor** | Split existing role logic into explicit proxy wrappers for Phase 0 |
| `santiago_core/agents/` | `santiago_core/agents/santiago-pm-safe-xp/service/` | **Add** | Generated MCP service folders per catch (Phase 2+) |
| `santiago_core/orchestrator/` | `santiago_core/orchestrator/ethics/` | **Extract** | Dedicated ethics gating module for pre-execution review |
| `santiago_core/orchestrator/` | `santiago_core/orchestrator/concurrency/` | **Extract** | Session isolation and tool locking for multi-agent safety |
| `nusy_orchestrator/` (misc files) | `nusy_orchestrator/santiago_builder/` | **Organize** | Factory components (Navigator, Catchfish, Fishnet) under dedicated package |
| `nusy_orchestrator/queues/` | `nusy_orchestrator/santiago_builder/pipelines/` | **Consolidate** | Queued writes, provenance handling, schema validation in single pipeline |
| `santiago-pm/ships-logs/` (scattered) | `ships-logs/expeditions/` | **Normalize** | Centralized expedition outcomes with timestamped markdown |
| `santiago_core/voyage-trials/` | `santiago_core/voyage-trials/` | **Keep** | BDD scenarios stay local to santiago_core for validation |
| `ocean-arch-redux/arch-redux-claude-sonnet-4.5-v3-plan/` | same | **Keep** | Planning artifacts, no code move |
| `src/nusy_pm_core/` | same | **Deprecate** | Legacy archive, reference only |
| `santiago-code/` | same | **Deprecate** | Early experiments, reference only |
