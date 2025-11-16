# Relevance Map — Copilot GPT-5 v2 (2025-11-16)

```text
**Metadata**
Model Name: copilot-gpt-5
Model Version: unknown
Date: 2025-11-16
Repo Commit SHA: 53a9fc4
Run ID: relevance-copilot-gpt-5-2025-11-16-1
```text

Categories: Relevant / Peripheral / Legacy-Duplicate / Historical / GAP / Irrelevant.

## Top-Level Directories
| Path | Category | Notes |
| --- | --- | --- |
| `src/nusy_pm_core/` | Historical | Archived prototype runtime (tag `prototype-archive-2025-11-16`). |
| `santiago_core/` | GAP | Referenced in strategy; absent; will be subsumed by orchestrator + services. |
| `santiago-pm/` | Relevant | Domain-specific PM artifacts (strategic charts, manifests, ships logs). |
| `ocean-arch-redux/` | Relevant | Planning outputs; ensure independence (no calibration yet). |
| `ocean-research/` | Relevant | Authoritative target-state references (DGX, fake-team, evolution, concurrency). |
| `notes/` | Relevant | Source notes & legacy KG TTL for consolidation. |
| `nusy_prototype/` | Peripheral | Clinical/other prototype insights; not core to v2 scope. |
| `experiments/` | Peripheral | Experiment descriptions; contextual. |
| `templates/` | Peripheral | Generic scaffolds; low direct impact. |
| `backlog/` | Peripheral | Improvement items (e.g., markdown hardening). |
| `config/` | Peripheral | Experiment configuration; not central post-archive. |
| `.github/` | Peripheral | Agent instructions; supportive. |
| `.venv/`, `.git/`, caches | Irrelevant | Tooling and SCM internals. |

## Key Files (Selected)
| File | Category | Notes |
| --- | --- | --- |
| `architecture-redux-prompt-v2.md` | Relevant | Governing evaluation prompt. |
| `DEVELOPMENT_PLAN.md` | Relevant | Migration alignment. |
| `DEVELOPMENT_PRACTICES.md` | Relevant | Working agreements to move under knowledge/shared. |
| `notes/kg.ttl` | Relevant | Legacy graph to consolidate. |
| `santiago-pm/strategic-charts/Santiago-Trains-Manolin.md` | Relevant | Strategic direction & metaphors. |
| `ocean-research/nusy_manolin_architecture.md` | Relevant | DGX/Manolin model. |
| `ocean-research/nusy_manolin_multi_agent_test_plans.md` | Relevant | Concurrency & ethics gating references. |
| `ocean-research/dgx_spark_nusy_report.md` | Relevant | Deployment insights. |
| `ocean-research/fake_team_feature_plan.md` | Relevant | Fake-team mode for interim operations. |
| `nusy_prototype/clinical-intelligence-pipeline-architecture.md` | Peripheral | Domain-specific extension possibility later. |
| `requirements.txt` | Peripheral | Environment baseline; not changed in plan phase. |

## Legacy / Duplicate
| Path | Rationale | Action |
| --- | --- | --- |
| `santiago/` | Older doc set overlapping with `santiago-pm/` | Mark for eventual deprecation post consolidation. |
| `santiago-code/` | Archived | Keep tag reference only. |
| Multiple TTL graphs (`notes/kg.ttl`, any legacy knowledge/*) | Redundancy & fragmentation | Merge into `knowledge/domains/core/graph.ttl`. |

## GAP Identification
| Gap | Impact | Mitigation |
| --- | --- | --- |
| Missing `knowledge/` root | Inconsistent knowledge access & provenance | Milestone 1 creation + consolidation. |
| Missing `santiago_core/` | Ambiguity around core engine location | Encode functionality via orchestrator + MCP services; note gap. |
| No ethics/concurrency middleware code | Risks ungoverned agent actions | Define gating spec in Milestone 4. |

(No calibration appendix included; independence maintained.)

### References Cited
- ocean-research/dgx_spark_nusy_report.md
- ocean-research/nusy_manolin_architecture.md
- ocean-research/nusy_manolin_provisioning_automation.md
- ocean-research/nusy_manolin_multi_agent_test_plans.md
- ocean-research/fake_team_feature_plan.md
- ocean-research/fake_team_steps_for_hank_and_copilot.md
