# NuSy Product Team Development Plan

## Context

- Vision holder: Hank’s product expertise combined with NuSy NeuroSymbolic reasoning.
- Primary domains: AI agents, MCP services, and domain experts built on a shared NuSy knowledge graph.
- Primary goal: Deliver a continuous stream of validated features that are grounded in hypotheses, executable BDD specs, and knowledge graph reasoning.

## Strategic Canonicals

- Canonical strategic doc (Santiago-PM): `santiago-pm/strategic-charts/Santiago-Trains-Manolin.md`
- Index for strategic charts: `santiago-pm/strategic-charts/README.md`

## Phased Milestones

1. **Scaffold the NuSy PM Core** *(Week 0-1)* ✅ **COMPLETED**
   - Create repo-level practices, plans, roles instructions, and backlog artifacts.
   - Establish the NuSy knowledge graph contract and define the initial MCP service endpoints.
   - Hypothesis: If we have clear artifacts mapping vision → backlog → BDD, then the team can start delivering testable features faster.

2. **Implement Autonomous Multi-Agent Experiment** *(Week 1-2)* ✅ **COMPLETED**
   - Build AI agent framework with OpenAI integration
   - Implement autonomous decision-making and collaboration
   - Create full experiment runner with ethical oversight
   - Hypothesis: AI agents can autonomously develop features without human intervention

3. **Automate NuSy Knowledge Imports** *(Week 2-4)*
   - Implement Secrets Management Service for secure API key storage
   - Reorganize PM-related files under `domains/pm-expert/` folder structure
   - Define KG schemas with Architect – NuSy
   - Create Source Knowledge Loading System for ingesting domain expertise:
     - Jeff Patton (user story mapping, discovery)
     - Jeff Gothelf (Lean UX, continuous discovery)
     - Popular methodologies: Agile, Scrum, Kanban, XP, Lean, SAFe, DAD
   - Create data transformation agents that populate the KG from product stories
   - Hypothesis: A reusable KG adapter accelerates future feature planning by 30%.

4. **Implement Core Tackle** *(Week 4-6)*
   - Complete status tackle (✅ COMPLETED - production ready)
   - Implement notes tackle with relationship features
   - Build experiments tackle for autonomous execution
   - Hypothesis: Modular tackle architecture enables autonomous code generation and maintainable implementations

## Current Status Summary

| Phase | Milestone | Status | Key Deliverables |
| --- | --- | --- | --- |
| Phase 0 | Bootstrap Fake Team | 🔄 In Progress | MCP proxies, knowledge infrastructure, contracts |
| Phase 1 | Factory Infrastructure | 📋 Planned | Navigator, Catchfish, Fishnet implementations |
| Phase 2 | First Santiago Catch | 📋 Planned | santiago-pm-safe-xp deployed and A/B tested |
| Phase 3 | Progressive Replacement | 📋 Planned | Architect, Developer, QA, UX, Platform replacements |
| Phase 4 | Self-Sustaining | 📋 Future | Real Santiagos improve factory |
| DGX | Production Hardening | 📋 Parallel | vLLM deployment, ethics gating, concurrency |

## Immediate Next Steps (Phase 0 Completion)

1. **Create Knowledge Infrastructure** *(Priority 1)*
   - [ ] Create `knowledge/` directory structure
   - [ ] Define trust registry schema in `knowledge/catches/index.yaml`
   - [ ] Create role cards in `knowledge/proxy-instructions/` for 7 roles

2. **Implement MCP Proxy Layer** *(Priority 2)*
   - [ ] Build thin MCP services in `santiago_core/agents/_proxy/`
   - [ ] Wire to external APIs (GPT-4, Claude, Copilot)
   - [ ] Implement basic tools: `status`, `plan`, `execute_scenario`

3. **Validate Fake Team Coordination** *(Priority 3)*
   - [ ] Test compound task: backlog grooming + design session
   - [ ] Verify logging to `ships-logs/` with provenance
   - [ ] Validate budgets and rate limits

4. **Document Contracts** *(Priority 4)*
   - [ ] Write MCP manifest specification
   - [ ] Create contract acceptance tests
   - [ ] Document A/B testing framework

## Knowledge Graph Commitments

- All fishing expeditions captured as provenance metadata
- Trust registry tracks versions, hashes, BDD pass rates, capability levels
- Hypotheses and experiments logged in `santiago-pm/expeditions/` and `ships-logs/`
- Role definitions maintained in `knowledge/proxy-instructions/` and `.github/agents/`

## References

- **Architecture**: See `ARCHITECTURE.md` for detailed component specifications
- **Roadmap**: See `zarchive/migration-artifacts/MIGRATION_ROADMAP.md` for milestone tasks
- **Vision**: See `docs/vision/README-START-HERE.md` for conceptual overview
- **Fake Team**: See `docs/vision/fake_team_pack/` for Phase 0 guidance
- **PM Patterns**: See `santiago-pm/` for development practices and tactical patterns
