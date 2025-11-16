# Santiago Factory Folder Layout Proposal

## Proposed Directory Tree

```text
ocean-arch-redux/
├── arch-redux-grok-code-fast-1-v3-plan/  # This plan
└── ... (other model plans)

santiago_core/
├── agents/
│   ├── _proxy/                          # Phase 0: Fake team MCP proxies
│   │   ├── pm_proxy.py
│   │   ├── architect_proxy.py
│   │   ├── developer_proxy.py
│   │   ├── qa_proxy.py
│   │   ├── ethicist_proxy.py
│   │   ├── ux_proxy.py
│   │   └── platform_proxy.py
│   └── santiago-pm-safe-xp/             # Phase 2+: Real Santiagos (factory-generated)
│       └── service/                     # MCP service implementation
└── ...

nusy_orchestrator/
└── santiago_builder/                    # Factory components (built by fake team)
    ├── navigator.py                     # Orchestrates fishing expeditions
    ├── catchfish.py                     # Knowledge extraction (30-60m → <15m)
    └── fishnet.py                       # BDD test generation

knowledge/                               # Generated Santiagos and factory artifacts
├── catches/                             # Factory outputs (generated Santiagos)
│   ├── santiago-pm-safe-xp/
│   │   ├── domain-knowledge/           # Markdown + YAML from sources
│   │   ├── bdd-tests/                  # Feature files from Fishnet
│   │   ├── mcp-manifest.json           # Auto-generated
│   │   └── provenance.yaml             # Fishing expedition metadata
│   └── index.yaml                      # Trust registry (approvals, versions)
├── templates/                          # Base structures for generating Santiagos
└── proxy-instructions/                 # Role definitions for fake team
    ├── pm-role.md
    ├── architect-role.md
    ├── developer-role.md
    ├── qa-role.md
    ├── ethicist-role.md
    ├── ux-role.md
    └── platform-role.md
```

## Mapping Table

| Current Path | Target Path | Action | Rationale |
|--------------|-------------|--------|-----------|
| `santiago_core/agents/` | `santiago_core/agents/_proxy/` | Extract | Create dedicated proxy directory for Phase 0 fake team |
| `santiago_core/agents/` | `santiago_core/agents/santiago-pm-safe-xp/` | Extract | Add real Santiagos as factory catches |
| (missing) | `nusy_orchestrator/santiago_builder/` | Create | Factory components built by fake team |
| (missing) | `knowledge/catches/` | Create | Store generated Santiagos (not pre-authored domains) |
| (missing) | `knowledge/templates/` | Create | Base structures for Santiago generation |
| (missing) | `knowledge/proxy-instructions/` | Create | Role instructions for fake team |
| `src/nusy_pm_core/` | (deprecate) | Deprecate | Legacy prototype, reference only |
| `santiago-code/` | (deprecate) | Deprecate | Early experiments, reference only |
