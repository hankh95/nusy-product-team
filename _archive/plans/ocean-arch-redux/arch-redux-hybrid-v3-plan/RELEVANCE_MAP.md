# Relevance Map — Hybrid v3 Plan

---

## Relevant

- `ocean-research/00-ARCHITECTURE-PATTERN.md` — Mandatory factory pattern guidance; defines Santiago as self-bootstrapping factory
- `santiago-pm/strategic-charts/Old man and the sea.md` — 10-step fishing process (Navigator blueprint with validation loops)
- `santiago-pm/expeditions/` — Hypothesis-driven experiments (progressive replacement methodology, A/B testing patterns)
- `santiago-pm/tackle/` — Modular implementation units (factory code structuring hints)
- `santiago-pm/voyage-trials/` — BDD testing style and expectations (Fishnet alignment, acceptance criteria patterns)
- `ocean-research/building-on-DGX/` — DGX deployment specs (vLLM/TensorRT, storage tiers, SLIs)
- `ocean-research/dgx_spark_nusy_report.md` — DGX Spark hardware specifications (128GB RAM, 4TB+8TB NVMe, batch inference)
- `ocean-research/nusy_manolin_architecture.md` — Shared memory & concurrency patterns
- `ocean-research/nusy_manolin_multi_agent_test_plans.md` — Multi-agent testing (P95 <6s, session isolation, tool locking)
- `ocean-research/fake_team_pack/` — Proxy strategy and thin MCP wrapper patterns
- `nusy_prototype/` — Evidence for 30–60m extraction, 3 validation cycles (Catchfish design validation)
- `santiago_core/` — Active service scaffolding and integration surface for proxies/real Santiagos

## Peripheral

- `experiments/`, `backlog/`, `reports/`, `notes/` — Contextual strategy and historical artifacts
- `docs/`, `calibration/`, `tools/` — Tooling and documentation support

## Legacy-Duplicate

- `santiago-code/` — Archived experiments; preserve for reference, avoid duplication
- `src/nusy_pm_core/` — Legacy prototype; reference only, do not refactor into factory

## GAP

- `knowledge/` — Must be created with `catches/`, `templates/`, `proxy-instructions/`, `shared/`, and trust registry (`knowledge/catches/index.yaml`) with capability levels and replacement decisions
- `santiago_core/agents/_proxy/` — Fake team proxy directory; create thin MCP services per role with versioned contracts
- `nusy_orchestrator/santiago_builder/` — Factory components (Navigator, Catchfish, Fishnet) built by fake team
- `nusy_orchestrator/santiago_builder/pipelines/` — Provenance queue implementation with idempotency and schema validation
- Storage tier management — Lifecycle policies for hot/warm/cold migration
