# Relevance Map

## Relevant

Files/directories critical to architecture decisions that must guide the design:

- `ocean-research/00-ARCHITECTURE-PATTERN.md` — **Mandatory reading**. Defines factory insight (Navigator + Catchfish + Fishnet) and bootstrapping order; foundation for every architectural decision
- `santiago-pm/strategic-charts/Old man and the sea.md` — 10-step fishing process that Navigator must encode as literal workflow
- `santiago-pm/expeditions/` — Hypothesis-driven experiments showing how fake team improves factory (e.g., `autonomous-santiago-synthesis/`, `pm-domain-knowledge-expansion/`)
- `santiago-pm/tackle/` — Modular implementation units teaching how fake team structures code incrementally
- `santiago-pm/voyage-trials/` — BDD validation patterns that Fishnet must generate and Navigator must enforce
- `ocean-research/building-on-DGX/dgx_spark_nusy_report.md` — Hardware, storage (4TB+8-16TB NVMe), vLLM/TensorRT constraints for shared DGX deployment
- `ocean-research/nusy_manolin_multi_agent_test_plans.md` — Concurrency, ethics, load test requirements (P95 <6s, 10-agent sessions, tool locking)
- `ocean-research/fake_team_pack/` — Operational guidance for Phase 0 proxy roles, working agreements, team roster patterns
- `nusy_prototype/neurosymbolic-clinical-reasoner-technical-summary.md` — Clinical prototype evidence: 30-60 minute extraction, 3 validation cycles, 4-layer knowledge model
- `santiago_core/` — Current orchestrator, agent wiring; where factory-generated MCP services will be hosted

## Peripheral

Context that informs but doesn't drive core decisions:

- `ocean-research/nusy_manolin_architecture.md` — Shared memory patterns useful for reference but not structural requirements
- `ocean-research/features-capabilities-for-shared-memory-and-evolution.md` — Background on evolution patterns
- `experiments/` (various `.md` files) — Past explorations inform prioritization but aren't architectural guardrails
- `notes/kg.ttl`, `notes/README.md` — Domain knowledge snapshots useful for seeding Catchfish examples
- `backlog/autonomous-multi-agent-backlog.md` — Historical context for planned work, not canonical for factory design
- `config/experiment.json` — Experimental configuration, may need updates but not foundational
- `santiago_core/PHASE1_REPORT.md`, `PHASE2_REPORT.md` — Progress reports providing context

## Legacy-Duplicate

Archived code to preserve but not use as foundation:

- `src/nusy_pm_core/` — Previous prototype; keep for archaeology but do not fork patterns from it
- `santiago-code/` — Early experiments predating current orchestrator; maintain for reference only
- `santiago/` (if exists, hyphen variant) — Earlier restructuring; avoid modifying until migration complete

## GAP

Missing items that must be created:

- `knowledge/` root directory — Must be created to store factory outputs and fake team guidance
- `knowledge/catches/` — Storage for generated Santiagos with domain-knowledge/, bdd-tests/, manifests, provenance
- `knowledge/templates/` — Base structures for catch packages and proxy templates
- `knowledge/proxy-instructions/` — Role definition markdown files for fake team (pm-role.md, architect-role.md, etc.)
- `knowledge/catches/index.yaml` — Trust registry for generated Santiagos tracking parity metrics, validation status
- `santiago_core/agents/_proxy/` — Fake team MCP proxies not yet implemented (pm_proxy.py, architect_proxy.py, etc.)
- `nusy_orchestrator/santiago_builder/` — Dedicated package for Navigator, Catchfish, Fishnet, pipelines is missing
- `nusy_orchestrator/santiago_builder/pipelines/` — Queued write pipeline, provenance queue, schema validator
- `santiago_core/orchestrator/ethics/` — Ethics gating module for pre-execution review
- `santiago_core/orchestrator/concurrency/` — Session isolation and tool locking for multi-agent safety
- `ships-logs/expeditions/` — Centralized log of fishing runs and A/B tests for provenance and auditing
