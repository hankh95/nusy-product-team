# Folder Layout Proposal — Copilot GPT-5 v2 (2025-11-16)

```text
**Metadata**
Model Name: copilot-gpt-5
Model Version: unknown
Date: 2025-11-16
Repo Commit SHA: 53a9fc4
Run ID: layout-copilot-gpt-5-2025-11-16-1
```text

## Proposed Target Tree (Plan-Only)
```text
knowledge/
  shared/
    roster.ttl
    working-agreements.md
    ships-log.md
    evolution-cycles/
      0001-cycle-template.md
    policies.ttl
  domains/
    core/
      graph.ttl
      glossary.md
      ontology.ttl
      provenance-log.ttl
orchestrator/
  README.md (plan-only)
  openapi-draft.yaml
services/
  mcp-pm/
    manifest.json
    tools/ (spec only)
  mcp-ethicist/
    manifest.json
  mcp-architect/
    manifest.json
  mcp-developer/
    manifest.json
  mcp-qa/
    manifest.json
  mcp-ux/
    manifest.json
  mcp-platform/
    manifest.json
deployment/
  dgx-manolin-plan.md
  env-schema.md
features/
  orchestrator-pilot/ (Gherkin stubs)
```

## Mapping Table (Current → Target)
| Current Path | Target Path | Action |
| --- | --- | --- |
| (missing) `knowledge/` | `knowledge/` | Create skeleton (Milestone 1) |
| `notes/kg.ttl` | `knowledge/domains/core/graph.ttl` | Merge + add provenance |
| `santiago-pm/ships-logs/` | `knowledge/shared/ships-log.md` | Consolidate to single log with domain tags |
| `DEVELOPMENT_PRACTICES.md` | `knowledge/shared/working-agreements.md` | Link or relocate for shared agreements |
| `santiago-pm/strategic-charts/*` | `knowledge/shared/evolution-cycles/` | Extract canonical evolution cycle patterns |
| Archived `src/nusy_pm_core/` (tag) | `orchestrator/` + `services/mcp-*` | Regenerate specs/new code post-plan |
| (missing) `santiago_core/` | Integrated in orchestrator + services | Treat absence as GAP; embed roles via MCP services |
| `nusy_prototype/*` | Out of scope for v2 | Keep peripheral; integrate later if needed |
| `experiments/` | Reference docs | Link from manifests if applicable |

## Category Summary
| Path | Category |
| --- | --- |
| `knowledge/` | New Core |
| `orchestrator/` | Core |
| `services/mcp-*` | Core |
| `deployment/` | Supporting |
| `features/` | Supporting |
| Archived `src/nusy_pm_core/` | Historical |
| `nusy_prototype/` | Peripheral |
| Missing `santiago_core/` | GAP |

## Justification Highlights
- Single KG tree eliminates graph duplication and inconsistent provenance.
- Explicit services directory enforces manifest-driven interfaces & evolution.
- Separation of deployment concerns reduces local vs cluster conflation.
- Cycle templates under `evolution-cycles/` standardize self-improvement artifacts.

### References Cited
- ocean-research/dgx_spark_nusy_report.md
- ocean-research/nusy_manolin_architecture.md
- ocean-research/nusy_manolin_provisioning_automation.md
- ocean-research/nusy_manolin_multi_agent_test_plans.md
- ocean-research/fake_team_feature_plan.md
- ocean-research/fake_team_steps_for_hank_and_copilot.md
