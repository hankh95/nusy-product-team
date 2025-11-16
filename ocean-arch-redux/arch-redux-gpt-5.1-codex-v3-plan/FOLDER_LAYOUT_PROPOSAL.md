# Folder Layout Proposal

## Proposed Directory Tree

```text
knowledge/
├── catches/
│   └── santiago-pm-safe-xp/
│       ├── domain-knowledge/
│       ├── bdd-tests/
│       ├── mcp-manifest.json
│       └── provenance.yaml
├── templates/
│   ├── catch-package.md
│   ├── bdd-feature-template.feature
│   ├── manifest-template.json
│   └── provenance-ledger.yaml
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
    └── concurrency/

nusy_orchestrator/
└── santiago_builder/
    ├── navigator.py
    ├── catchfish.py
    ├── fishnet.py
    ├── pipelines/
    │   ├── provenance_queue.py
    │   └── kg_writer.py
    └── tests/
        ├── test_navigator.py
        ├── test_catchfish.py
        └── test_fishnet.py

ships-logs/
└── expeditions/
    └── <date>-<expedition-name>.md
```

## Mapping Table

| Current Path | Target Path | Action |
| --- | --- | --- |
| _missing_ (`knowledge/`) | `knowledge/` | **Create** folder hierarchy for catches, templates, and proxy instructions |
| `santiago_core/agents/` | `santiago_core/agents/_proxy/` | **Refactor**: split existing role logic into explicit proxy wrappers |
| `santiago_core/agents/` | `santiago_core/agents/santiago-pm-safe-xp/service/` | **Add** generated MCP service folders per catch |
| `santiago_core/orchestrator/` | `santiago_core/orchestrator/ethics/` & `.../concurrency/` | **Extract** ethics + concurrency gating modules |
| `nusy_orchestrator/` (misc files) | `nusy_orchestrator/santiago_builder/` | **Organize** factory components (Navigator, Catchfish, Fishnet) under dedicated package |
| `nusy_orchestrator/queues/` | `nusy_orchestrator/santiago_builder/pipelines/` | **Consolidate** queued writes + provenance handling |
| `santiago-pm/ships-logs/` scattered notes | `ships-logs/expeditions/` | **Normalize** expedition outcomes with timestamped markdown |
| `ocean-arch-redux/arch-redux-gpt-5.1-codex-v3-plan/` | same | **Keep** as planning artifacts, no code move |
