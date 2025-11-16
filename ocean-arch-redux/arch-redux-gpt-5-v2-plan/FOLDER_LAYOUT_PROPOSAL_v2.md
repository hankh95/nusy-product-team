# Folder Layout Proposal — v2 (Plan-Only)

A proposed structure aligning with MCP services, an orchestrator, and a root `knowledge/` tree, while preserving existing code and minimizing churn.

## Proposed Structure

```text
knowledge/
  shared/
    roster.ttl
    working-agreements.md
    ships-log.md
    evolution-cycles/
      0001-cycle-template.md
  domains/
    core/
      graph.ttl
      glossary.md

orchestrator/
  (plan-only docs + API contracts)

services/
  mcp-pm/
    (manifest.json, tool specs, adapters)
  mcp-developer/
    (manifest.json, tool specs, adapters)
  mcp-qa/
  mcp-architect/
  mcp-systems/
  mcp-platform/
  mcp-ux/
```

## Mapping From Current Repo

| Current Path | Target | Action |
| --- | --- | --- |
| `src/nusy_pm_core/` | Archived | Prototype runtime removed; future orchestrator will be regenerated under `orchestrator/` and `services/mcp-*`. |
| `santiago_core/agents/` | `services/*` | Split agent behaviors into role-specific MCP services. |
| `santiago_core/core/` | `orchestrator/` | Reuse ethics/concurrency patterns for middleware design. |
| `notes/kg.ttl` | `knowledge/domains/core/graph.ttl` | Consolidate with provenance. |
| `santiago_core/knowledge/*.ttl` | `knowledge/domains/core/graph.ttl` | Consolidate. |
| `santiago-pm/ships-logs/` | `knowledge/shared/ships-log.md` | Normalize to shared log with links to originals. |
| `DEVELOPMENT_PRACTICES.md` | `knowledge/shared/working-agreements.md` | Move or link. |
| `ocean-research/*` | Reference docs | Link from orchestrator/service docs. |

## Relevance Table (Summary)

| Path | Category |
| --- | --- |
| `src/nusy_pm_core/` | Archived |
| `santiago_core/` | Relevant |
| `ocean-research/` | Relevant |
| `notes/` | Relevant |
| `santiago-pm/` | Relevant |
| `nusy_prototype/` | Peripheral |
| `santiago/` | Peripheral |
| `santiago-code/` | Legacy/Duplicate |
| `.git/`, `.venv/` | Irrelevant |
