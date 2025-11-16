# Santiago Factory Relevance Map

## Relevant

Files/directories critical to architecture decisions:

- `ocean-research/00-ARCHITECTURE-PATTERN.md` — Mandatory reading; explains factory pattern, phases, fake team bootstrapping.
- `santiago-pm/strategic-charts/Old man and the sea.md` — 10-step fishing process literal workflow.
- `santiago-pm/expeditions/` — Hypothesis-driven experiments; teaches fake team improvement loops.
- `santiago-pm/tackle/` — Modular implementation units; teaches fake team code structuring.
- `santiago-pm/voyage-trials/` — BDD test scenarios; teaches fake team validation patterns.
- `ocean-research/building-on-DGX/` — DGX deployment specs (128 GB RAM, vLLM/TensorRT-LLM, 10-agent concurrency).
- `nusy_prototype/` — Clinical prototype evidence (30-60m conversion, 3 validation cycles, 94.9% coverage).

## Peripheral

Context that informs but doesn't drive decisions:

- `santiago_core/` — Current implementation; reference for existing structure.
- `src/nusy_pm_core/` — Legacy prototype; archived reference.
- `santiago-code/` — Early experiments; archived reference.
- `ocean-research/manolin_multi_agent_architecture.md` — Shared memory patterns.
- `ocean-research/nusy_manolin_multi_agent_test_plans.md` — Multi-agent testing strategy.
- `ocean-research/fake_team_pack/` — Proxy strategy details.
- `config/`, `notes/`, `backlog/`, `experiments/`, `reports/` — Project context.

## Legacy-Duplicate

Archived code to preserve but not use:

- `src/nusy_pm_core/` — Legacy NuSy PM prototype; superseded by factory approach.
- `santiago-code/` — Early Santiago experiments; superseded by santiago_core/.

## GAP

Missing items that should exist:

- `knowledge/` — Needs creation; stores generated Santiagos and factory artifacts.
- `santiago_core/agents/_proxy/` — Needs creation; fake team MCP proxies for Phase 0.
- `nusy_orchestrator/santiago_builder/` — Needs fake team to build; factory components (Navigator, Catchfish, Fishnet).
