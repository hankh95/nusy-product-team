# Folder Layout Proposal (v3)

## Proposed Directory Tree

```text
knowledge/
├── catches/
│   ├── santiago-pm/
│   │   ├── domain-knowledge/
│   │   ├── bdd-tests/
│   │   ├── mcp-manifest.json
│   │   └── provenance.yaml
│   └── index.yaml
├── templates/
│   ├── catch-package/
│   │   ├── domain-knowledge/
│   │   ├── bdd-tests/
│   │   ├── mcp-manifest.json
│   │   └── provenance.yaml
│   └── proxy-role-template.md
└── proxy-instructions/
    ├── pm.md
    ├── architect.md
    ├── developer.md
    ├── qa.md
    ├── ux.md
    ├── platform.md
    └── ethicist.md

santiago_core/
├── agents/
│   ├── _proxy/
│   │   ├── pm_proxy.py
│   │   ├── architect_proxy.py
│   │   ├── developer_proxy.py
│   │   ├── qa_proxy.py
│   │   ├── ux_proxy.py
│   │   ├── platform_proxy.py
│   │   └── ethicist_proxy.py
│   └── santiago-pm/
│       └── service/
│           ├── __init__.py
│           ├── tools.py
│           └── manifest.json
└── orchestrator/
    ├── ethics/
    │   └── gating.py
    └── concurrency/
        ├── session_isolation.py
        └── tool_locking.py

nusy_orchestrator/
└── santiago_builder/
    ├── navigator.py
    ├── catchfish.py
    ├── fishnet.py
    ├── pipelines/
    │   ├── provenance_queue.py
    │   ├── kg_writer.py
    │   └── schema_validator.py
    └── tests/
        ├── test_navigator.py
        ├── test_catchfish.py
        └── test_fishnet.py

ships-logs/
└── expeditions/
    └── <date>-<expedition>.md
```

## Mapping Table

| Current Path | Target Path | Action | Rationale |
|-------------|-------------|--------|-----------|
| (missing) | `knowledge/` | Create | Canonical home for catches, templates, proxy instructions |
| (missing) | `knowledge/catches/<santiago>/` | Create | Self-contained packages (knowledge, BDD, manifest, provenance) |
| (missing) | `knowledge/catches/index.yaml` | Create | Trust registry (parity %, last validation, capabilities) |
| `santiago_core/agents/` | `santiago_core/agents/_proxy/` | Refactor | Explicit proxies per role for Phase 0 |
| `nusy_orchestrator/` (misc) | `nusy_orchestrator/santiago_builder/` | Organize | Factory components under one package |
| (missing) | `.../pipelines/` | Create | Queued writes, schema checks, provenance ledger |
| scattered logs | `ships-logs/expeditions/` | Normalize | Central, timestamped expedition outcomes |
| legacy prototypes | leave-as-is | Deprecate | Keep for archaeology; do not fork patterns |
