# Experiment: Graph-native PM knowledge vs External Tooling

## Motivation

The NuSy PM system is becoming the canonical brain for coordinating multi-agent work. Traditionally we linked this brain to external tools (GitLab/Gitea, Taiga, Matrix, etc.) to manage features, stories, tests, and conversations. However, there is a compelling alternative: store all of that project intelligence directly in the knowledge graph itself, letting NuSy manage the entire product artifact lifecycle (features, experiments, BDD tests, research, discussions) alongside the domain expertise.

This experiment will compare two systems operating over the same PM body of knowledge, driven by the same NuSy agent (the "fisherman" domain expert), but with differing persistence layers:

1. **System A – External Tool Integration ("Xternal"):** Navigator orchestrates the domain expert while writing artifacts into the external tools we outlined (project boards, repo files, chat logs). NuSy observes the tools and keeps its own derived model of the data (similar to our current approach). For this system we ignore the up-front setup cost (initial Git board, chat rooms) but focus on ongoing maintenance and brittleness caused by the many moving parts.
2. **System B – Graph-native PM Brain:** All artifacts normally kept in folders or tool chains (`development_plan.md`, features/BDD, issues, research notes) are encoded directly into the NuSy knowledge graph. Navigator cycles using that graph, updating features/stories/tests/conversations within the KG, while the external tools (repos, boards, chat) become secondary mirrors rather than primary sources.

## Hypotheses

1. Graph-native storage will reduce latency between decisions and test updates because Navigator can write knowledge and behaviors directly without requiring tool syncing.
2. System A will still be necessary for integrations that humans rely on, but System B may produce higher knowledge fidelity and faster experiment iterations because everything lives co-located with the domain expertise (fishman / fisherman).

## Plan

1. Capture the current `development_plan.md`, `research/`, `features/`, and `tests/` content in a NuSy graph schema (features, epics, hypotheses, experiments, BDD tests, research notes). Use the PM knowledge base as a starting domain for both systems.
2. Implement checkpoints for Navigator that show whether each artifact update happened via external tool sync (System A) or graph-native writes (System B).
3. Track Signals (focus on speed & cost of delay plus brittleness):
   - time-to-green (BDD passing) per feature, comparing how quickly each system can respond once the initial graph is captured
   - maintenance overhead for System A (number of tool integrations touched, webhook failures, manual sync steps per cycle)
   - brittleness incidents in System A (broken adapters, stale data, missed events) vs stability of System B
   - number of KG-only updates in System B and how often Navigator can close gaps without touching external tools
   - coverage of PM behaviors/tests captured in the graph vs in tool artifacts (assess completeness of knowledge)
   - perceived cost-of-delay (how long features/BDD checks sit before completion) for each system, measured by Navigator logs and human/agent wait times
4. Evaluate: which approach yields cleaner knowledge, faster iteration cycles, reduced cost-of-delay and bottlenecks, and easier reasoning/maintenance when new domain-specific versions (e.g., fisherman) are created. Pay attention to how System B reduces the brittle surface area of connectors, and how System A continues to impose ongoing sync costs.
5. Treat every cycle as a hypothesis-driven experiment: Navigator should run the NuSy "catchfish" ingestion plus "fishnet" BDD-generation loops in small batches, document each decision/outcome in the knowledge graph, and run a quick knowledge debrief so the KG stays self-reflective before the next iteration.

## Measurement Extensions

1. **Total time to completion** – Track the clock from when Navigator/ NuSy PM first receives a new domain question or feature to when the corresponding BDD tests are green and the KG is updated. Measure for both systems over multiple cycles.
2. **Human bottleneck** – Log every time a human answer, clarification, or decision is required (per system). In parallel runs give both systems the same domain expertise file so they are not advantaged by missing knowledge. In serial runs, let the second system see the same answers only after the human bottleneck delay you want to measure (i.e., record how many minutes each system waited for your response and how that affects throughput).
3. **Usability / satisfaction** – After each cycle, collect subjective feedback (via short checklist or quick score) whether the system’s workspace felt cohesive, transparent, and responsive. Compare System A’s multi-tool workflow to System B’s graph-native knowledge store.
4. **Cost of delay** – In System A, quantify the time lost due to waiting on tool syncs or brittle adapters. In System B, measure how often Navigator can proceed without external input because the KG already contains the needed artifact.
5. **Knowledge graph reflexivity and growth** – Track how many new edges/nodes capture decisions, lessons, and feedback per cycle as Navigator updates the KG; use the recorded outcome metadata to power the self-reflective experiment cycle described above.
6. **Generalizability and quality** – Measure improvement in development speed, defect reduction, and how easily the stored PM brain can spin up new domain-specific Santiagos (e.g., healthcare, finance) without rebuilding the external tool mesh.

## Implementation Details

1. **Shared domain file** – Prepare a single source-of-truth file (`research/domain-expertise/pm-domain.jsonld` or similar) describing the PM plan, goals, personas, experiments, and expected behaviors. Feed this file into both systems before running the experiment to ensure they start with identical domain knowledge.
2. **Navigator instrumentation** – Instrument Navigator to tag each change with the system label (A or B), record timestamps for each phase (knowledge ingestion, behavior synthesis, test execution, human waiting), and log when human input was needed.
3. **Graph schema & adapters** – Implement the graph schema for System B that can store artifacts like features, stories, tests, and conversations. Build adapters that allow Navigator to read/write these artifacts directly in the KG and emit BDD tests from them.
4. **Tool harness for System A** – Maintain the current connectors (Git repo files, boards, chat). Ensure the system logs every integration call, its success/failure, and the latency of the round trip. Track maintenance events (e.g., broken webhook) separately.
5. **Parallel vs serial execution** – Decide whether to run both systems simultaneously or back-to-back. If running in parallel, supply answers/human decisions to both at the same time. If running serially, delay providing answers to the second system and log the induced waiting period as part of the cost-of-delay.
6. **Data capture & reporting** – Store the logs, timing data, KG updates, and test results in the KG itself so NuSy can reason about them (and because that's part of the hypothesis for System B). Generate a dashboard/report for each cycle summarizing total time, human waits, brittle events, and usability scores.
7. **Catchfish + Fishnet orchestration** – Use the vision’s "catchfish" process to pull raw materials (documents, APIs, expertise) into structured KG nodes, then run "fishnet" to validate behaviors with BDD before Navigator commits updates. Include a knowledge debrief after each pass so feedback loops and lessons learned are stored in the graph.
8. **CI/CD and feedback loops** – Keep an automated pipeline that enforces the test-first discipline, captures pipeline latency (time to green) for both systems, and funnels user/human feedback back into the KG so Navigator can adapt.

## Pressing GO

1. Confirm the PM knowledge base file and ensure both systems can consume it.
2. Set up Navigator instrumentation and clarify how human responses will be tagged for each system run.
3. Implement the graph schema and adapters for System B, along with the logging needed for measurements.
4. Run the first cycle for both systems (parallel or serial as decided), gather the logs/timestamps, and iterate based on which measures signal brittleness, delay, or usability concerns.

## Next Steps

- Build the NuSy graph schema for storing project artifacts alongside domain knowledge.
- Update Navigator to record tool interactions and graph writes separately so we can measure both systems in parallel.
- Use this experiment to inform whether future NuSy PM incarnations should lean fully graph-native, keep the external tool chain, or blend both.
