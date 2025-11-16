# Proposed Folder Layout — Shared Memory + MCP Agents

```text
nusy-product-team/
├── knowledge/
│   ├── shared/
│   │   ├── working-agreements.md
│   │   ├── bdd-practices.md
│   │   ├── tools-and-mcp-capabilities.md
│   │   ├── team-roster-and-capabilities.ttl
│   │   ├── ships-log/
│   │   │   └── YYYY-MM-DD-*.md
│   │   └── evolution-cycles/
│   │       └── YYYY-MM-DD-evolution-cycle-*.md
│   ├── domains/
│   │   ├── pm/
│   │   │   └── domain-memory.md
│   │   ├── ethics/
│   │   │   └── evolution-reviews.md
│   │   └── <other-domain>/
│   └── kg/
│       └── santiago_kg.ttl
├── santiago_core/
│   ├── agents/
│   │   ├── santiago_pm/
│   │   │   ├── service/
│   │   │   │   ├── main.py
│   │   │   │   └── tools/
│   │   │   └── mcp/manifest.json
│   │   ├── santiago_ethicist/
│   │   │   └── ...
│   │   └── santiago_developer/
│   ├── core/
│   │   ├── agent_framework.py
│   │   └── team_coordinator.py
│   ├── services/
│   │   └── knowledge_graph.py (reads/writes knowledge/kg)
│   └── run_team.py (dev harness)
├── src/nusy_pm_core/
│   ├── api.py (orchestrator HTTP/MCP gateway)
│   ├── services/
│   │   ├── mcp_registry.py
│   │   ├── shared_memory.py
│   │   └── ships_log.py
│   └── cli.py (commands: scaffold, evolution-cycle, roster sync)
├── infrastructure/
│   └── manolin/
│       ├── provision_dgx_spark_base.sh
│       ├── install_docker_and_nvidia_container_runtime.sh
│       ├── setup_nusy_env.sh
│       ├── download_mistral_7b_instruct.sh
│       └── runbooks/
├── ocean-arch-redux/
│   └── arch-redux-gpt-5_1-codex-plan/
│       ├── ARCHITECTURE_PLAN.md
│       ├── MIGRATION_STEPS.md
│       ├── FOLDER_LAYOUT_PROPOSAL.md
│       └── scaffolds/
│           ├── mcp-manifest-template.json
│           └── roster-entry-template.ttl
└── tests/
    └── concurrency/
        └── test_session_isolation.py
```

**Key Ideas:**

- Move knowledge artifacts to repo root so every agent/service consumes the same source of truth.
- Give each MCP agent its own `service/` implementation + manifest for discoverability and onboarding.
- Consolidate provisioning assets under `infrastructure/manolin/` with scripts + runbooks ready for DGX Spark deployment.
- Store reusable scaffolds (manifest templates, roster TTL snippets) inside the architecture plan folder for future agents.
