# NuSy PM CatchFish / FishNet / Navigator Plan

## 1. Architecture summary

This project repurposes the NuSy clinical prototype (rdflib-powered knowledge graphs, verification scripts, and BDD tests) into a product management learning cycle. The core modules are:

- **CatchFish (knowledge ingestion & graph builder):** Instead of clinical guidelines, CatchFish ingests PM knowledge (vision docs, backlog, experiment reports) and outputs an RDF/JSON-LD graph where triples capture experiments, stakeholders, success metrics, and dependencies. This mirrors the prototype’s graph/JSON-LD assets (`generate_comprehensive_cds_report.py`, etc.) but for PM semantics.
- **FishNet (behavior test generator):** Inspired by the prototype’s `test_ci_tagged_*_bdd.py`, FishNet emits BDD-style coverage checks ("Given this stakeholder priority, When we review the portfolio, Then an experiment must have success metrics") that validate the structure and expected behaviors of the CatchFish graph rather than software code.
- **Navigator (cycle orchestrator):** Navigator runs CatchFish → FishNet → NuSy core cycles. It executes the tests, uses the NuSy reasoning engine (`NeurosymbolicClinicalReasoner`) to identify failed coverage or contradictory triples, and then recommends additions to the knowledge graph, new BDD scenarios, or NuSy core behavior changes. The NuSy core maintains its ability to act like an MCP (answering questions, planning roadmaps, inferring dependencies) but now over PM knowledge.

Navigator keeps iterating catches and tests until FishNet reports 100% coverage of the expected PM behaviors and capabilities.

## 2. Experiment plan for PM domain knowledge

1. **Collect PM corpus:** Gather vision/strategy docs, backlog descriptions, persona statements, experiment logs, metrics dashboards, and existing AI-agent guidance.
2. **CatchFish graph generation:** Parse the corpus, build RDF/JSON-LD triples, and attach metadata describing knowledge types (experimentation, user research) and the tools/behaviors expected from the NuSy PM MCP (e.g., hypothesis orchestration, experiment reporting, roadmap synthesis).
3. **FishNet behavior tests:** Produce tests that scan the CatchFish graph for required patterns (e.g., each hypothesis has success metrics, each persona has journeys, dependencies are captured). Tests are stored as BDD scenarios so Navigator can track behavior coverage.
4. **Navigator execution cycle:** Run CatchFish + FishNet, pass results to NuSy core, collect failed tests/gaps, then apply Navigator prompts to (a) extend the knowledge graph, (b) add new FishNet scenarios, or (c) iterate on the NuSy core reasoning (e.g., add new question templates). Repeat until FishNet coverage hits 100% for the defined behavior plane.
5. **Observation & outputs:** Use NuSy to output "care plan"/roadmap artifacts from the graph, ensure these are part of the behavior validation (FishNet should check these outputs), and log Navigator recommendations for future knowledge or behavior experiments.

## 3. Data access & ingestion notes

- To fully retrieve the other project, copy its relevant directories (e.g., existing `research/`, `ai-knowledge-review/`, and any graph fixtures) into this workspace. Once the files exist here, the NuSy agent can read and generalize the non-clinical CatchFish/FishNet pattern.
- Alternatively, provide a zipped snapshot or point to the shared remote and pull the data locally before summarizing it.
- The verification/analysis scripts already add the repo root to `sys.path`, so the NuSy core can import `neurosymbolic_prototype` to drive the Navigator evaluation cycle.
