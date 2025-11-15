# NuSy Product Team Development Plan

## Context

- Vision holder: Hank’s product expertise combined with NuSy NeuroSymbolic reasoning.
- Primary domains: AI agents, MCP services, and domain experts built on a shared NuSy knowledge graph.
- Primary goal: Deliver a continuous stream of validated features that are grounded in hypotheses, executable BDD specs, and knowledge graph reasoning.

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

## Backlog Sketch (Hypotheses + Experiments)

| Epic | Hypothesis | Experiment | Success Metric |
| --- | --- | --- | --- |
| Scaffold NuSy PM Core | A structured scaffolding artifact set accelerates onboarding | Create README, plan, practices, roles instructions, and first feature | Team can run `npm`/`poetry` setup and run first BDD spec without help |
| Integrate Git & CI | Consistent Git workflows + CI reduce merge conflicts and regressions | Define CI job skeleton + gating tests for features | `main` build stays green and BDD spec runs within 90 seconds |
| Add Developer agent | Expressing specs to a developer persona speeds implementation | Add dev instructions + sample commit pattern | Developer commits with linked BDD references in PR |

## Knowledge Graph Commitments

- Capture hypotheses, experiments, and results as KG triples (`hypothesis → experiment → outcome`).
- Track role responsibilities (`role → expectation`) to keep instructions current.

## Next Steps

1. Run the autonomous multi-agent experiment using `experiment_runner.py`
2. Implement Secrets Management Service for API key storage
3. Create `domains/pm-expert/` folder structure and reorganize PM files
4. Develop Source Knowledge Loading System for domain expertise ingestion
5. Complete notes and experiments tackle implementations (see individual `tackle/*/development-plan.md` files)

## Tackle Development Approach

Each tackle (implementation module) follows a structured development process:

- **Domain Specification**: Requirements defined in `nusy_pm/` directory
- **Implementation**: Code generated in `nusy_pm/tackle/` subdirectories
- **Individual Plans**: Each tackle has its own `development-plan.md`
- **Santiago Integration**: Autonomous code generation reads specs and writes implementations
