# Relevance Map

## Relevant

- `ocean-research/00-ARCHITECTURE-PATTERN.md` — Defines factory insight (Navigator + Catchfish + Fishnet) and bootstrapping order; foundation for every decision.
- `santiago-pm/strategic-charts/Old man and the sea.md` — 10-step fishing process that Navigator must encode.
- `santiago-pm/expeditions/`, `santiago-pm/tackle/`, `santiago-pm/voyage-trials/` — Encode hypothesis-driven workflow, modular build units, and BDD validation the fake team must follow.
- `ocean-research/building-on-DGX/` — Hardware, storage, and vLLM/TensorRT constraints for the shared DGX deployment.
- `ocean-research/nusy_manolin_multi_agent_test_plans.md` — Concurrency, ethics, and load test requirements for multi-agent operations.
- `ocean-research/fake_team_pack/` — Operational guidance for Phase 0 proxy roles, including working agreements.
- `nusy_prototype/` — Clinical prototype evidence proving 30-60 minute extraction with three validation cycles (basis for Catchfish targets).
- `santiago_core/` — Current orchestrator, agent wiring, and the place where factory-generated MCP services will be hosted.

## Peripheral

- `ocean-research/manolin_multi_agent_architecture.md` — Helpful reference for shared memory patterns but not directly changed by this plan.
- `experiments/*.md` — Captures past explorations; informs prioritization but not architectural guardrails.
- `notes/` (kg.ttl, READMEs) — Domain knowledge snapshots useful for seeding Catchfish but not structural requirements.
- `backlog/` — Provides historical context for planned work; not canonical for factory design decisions.

## Legacy-Duplicate

- `src/nusy_pm_core/` — Previous prototype; keep for archeology but do not fork patterns from it.
- `santiago-code/` — Early experiments predating current orchestrator; maintain for reference only.
- `santiago/` and `santiago-core/` (hyphen variant) — Earlier restructures; avoid modifying until migration complete.

## GAP

- `knowledge/` root (catches/templates/proxy instructions) — Must be created to store factory outputs and fake team guidance.
- `santiago_core/agents/_proxy/` — Fake team MCP proxies are not yet implemented.
- `nusy_orchestrator/santiago_builder/` — Dedicated package for Navigator, Catchfish, Fishnet, and pipelines is missing.
- `knowledge/catches/index.yaml` — Trust registry for generated Santiagos needed for orchestrator routing.
- `ships-logs/expeditions/` — Centralized log of fishing runs and A/B tests needs to exist for provenance and auditing.
