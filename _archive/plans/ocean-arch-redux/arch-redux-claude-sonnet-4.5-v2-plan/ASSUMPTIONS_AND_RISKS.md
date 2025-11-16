# Assumptions and Risks — 2025-11-16

**Metadata**
Model Name: Claude Sonnet 4.5
Model Version: claude-sonnet-4.5-20250514
Date: 2025-11-16
Repo Commit SHA: 5bfcc00
Run ID: arch-redux-claude-sonnet-4.5-2025-11-16

## Assumptions

- **DGX Spark Availability:** The migration plan assumes DGX Spark hardware will be procured and available for deployment by Milestone 6. If delayed, the interim "fake team" strategy using external LLM APIs (per `ocean-research/fake_team_pack/fake_team_steps_for_hank_and_copilot.md`) provides a fallback.

- **Mistral-7B-Instruct Sufficiency:** All Santiago agents share a single Mistral-7B-Instruct model instance. This assumes 7B parameter scale provides adequate domain reasoning for PM, Ethicist, Architect, Developer, QA, UX, and Platform roles. If specialized domains require larger models, the architecture supports multiple model instances but would increase memory requirements.

- **MCP Protocol Maturity:** The migration assumes MCP (Model Context Protocol) as the inter-service communication standard. If MCP tooling proves immature or incompatible, the architecture can fall back to REST APIs with similar manifest-based discovery patterns.

- **RDF/Turtle for Team Roster:** The team roster uses RDF/Turtle (`team-roster-and-capabilities.ttl`) for semantic queries. This assumes familiarity with RDF tools and SPARQL. If this proves burdensome, a simpler JSON schema can replace the RDF format without architectural changes.

- **Hank as Captain:** The architecture assumes Hank retains final authority over evolutionary decisions, DGX procurement, and high-risk approvals. The Ethics & Concurrency Gating layer routes certain operations to human review rather than full autonomy.

- **BDD/TDD Discipline:** The migration assumes continued adherence to BDD/TDD practices defined in `DEVELOPMENT_PRACTICES.md`. Agent quality depends on maintaining executable specifications and test-first workflows.

- **Single-Node Deployment Initially:** The DGX Spark deployment is single-node with no horizontal scaling in Phase 0-1. Multi-node expansion (Manolin-Node-2, etc.) is deferred to future phases when workload demands justify it.

## Risks & Mitigations

**Risk: Knowledge Graph Corruption During Concurrent Writes**

Without proper coordination, multiple agents writing to the KG simultaneously could produce inconsistent or corrupted state.

*Mitigation:* Milestone 3 implements a unified KG interaction layer with:
- Queued/batched writes preventing simultaneous updates to the same triples
- Conflict detection flagging when multiple agents attempt conflicting changes
- Provenance tracking enabling rollback if corruption is detected
- Schema validation rejecting malformed updates before they reach the KG

**Risk: Session Context Leakage**

Concurrent agent sessions might expose sensitive context from one session to another (e.g., PM working on confidential product A sees data from Developer working on product B).

*Mitigation:* Milestone 4 implements session isolation in `nusy_orchestrator/session_manager.py` with:
- Unique session IDs for all requests
- Context scoping preventing cross-session data access
- Comprehensive test suite in Milestone 5 validating zero leakage under load
- Audit logging of all cross-service data flows

**Risk: Ethics Gating Bottleneck**

If all operations require synchronous ethics review, the Santiago-Ethicist service could become a bottleneck limiting concurrent throughput.

*Mitigation:* Ethics gating is **selective**, not universal:
- Only operations flagged as high-risk trigger synchronous review
- Low-risk operations proceed immediately with post-hoc audit
- Configurable risk thresholds in `nusy_orchestrator/config/policies.yaml`
- Ethicist service can be horizontally scaled if load demands it

**Risk: DGX Procurement Delay**

The DGX Spark may be unavailable for weeks or months due to supply chain or budget constraints, blocking Milestone 6.

*Mitigation:* Interim "fake team" deployment strategy:
- MCP services implemented and testable locally without DGX
- External LLM API proxy (`llm_proxy.call()`) as temporary Santiago backend
- All orchestrator, session management, and ethics gating features functional on standard hardware
- DGX deployment becomes a "drop-in" replacement for the LLM proxy with no architectural changes

**Risk: Model Capacity Exhaustion**

A single Mistral-7B-Instruct instance may struggle with 10+ concurrent agents if context windows grow large or request rate spikes.

*Mitigation:*
- vLLM or TensorRT-LLM provides batching and efficient KV cache management
- Context length limits enforced per session (e.g., max 4K tokens per agent)
- Orchestrator includes request queueing and backpressure signals when model is saturated
- If capacity issues persist, add a second model instance (DGX Spark's 128 GB memory supports multiple 7B models)

**Risk: Missing Knowledge Folder Adoption**

Agents might continue using ad-hoc notes and logs instead of writing to `knowledge/shared/ships-log/` and `knowledge/domains/`, undermining the shared memory architecture.

*Mitigation:*
- Milestone 1 creates the folder structure with clear README documentation
- Santiago-PM explicitly includes `read_working_agreements` and ships log tools in its MCP manifest
- Orchestrator can enforce policy requiring certain operations to update ships logs
- Periodic audits (manual or via Santiago-Ethicist) check for stale knowledge folders

**Risk: Inadequate Test Coverage for Concurrency**

If concurrency tests don't cover realistic multi-agent scenarios, production deployment might encounter race conditions or deadlocks.

*Mitigation:* Milestone 5 implements comprehensive test harness directly derived from `ocean-research/nusy_manolin_multi_agent_test_plans.md`:
- Session isolation tests (PM-1, AR-NUSY-1 scenarios)
- Tool race condition tests (PM-2, DEV-1 scenarios)
- Load profiles (baseline, stress, spike) with SLO validation
- CI integration ensures tests run on every commit

**Risk: Evolutionary Drift Without Oversight**

Autonomous agents proposing and implementing evolutionary changes could gradually drift from intended behavior or introduce subtle bugs.

*Mitigation:*
- Ethics & Concurrency Gating requires Santiago-Ethicist review for all evolutionary proposals
- Ships logs provide audit trail of all evolutionary decisions
- Hank (Captain) retains approval authority for major changes
- BDD/TDD discipline ensures every evolution has executable specifications and tests

## Open Questions

- **Which Vector DB?** Qdrant vs pgvector vs Milvus — needs benchmark on DGX Spark with typical NuSy workload (embedding dimensions, query patterns, index size).

- **Which Graph DB?** Blazegraph vs Neo4j vs GraphDB — RDF native vs property graph tradeoffs; need to validate performance with NuSy ontology scale.

- **MCP vs REST?** If MCP tooling proves immature, should we standardize on REST + OpenAPI with similar manifest patterns, or wait for MCP ecosystem maturity?

- **Horizontal Scaling Timeline?** At what workload threshold (number of agents, request rate, model inference load) does single-node DGX Spark become insufficient, requiring multi-node deployment?

- **Fine-Tuning Strategy?** Should Santiago agents use base Mistral-7B-Instruct, or invest in domain-specific fine-tunes (e.g., PM-tuned, Architect-tuned models)? What are the accuracy vs infrastructure tradeoffs?

- **Knowledge Scope Evolution?** The Pond/Lake/Sea/Ocean knowledge scope metaphor is defined, but how do we measure and enforce scope boundaries in practice? What metrics indicate an agent has outgrown its current scope?

## Provenance & Queued Writes

The unified KG interaction layer (Milestone 3) introduces **provenance tracking** and **queued/batched writes** as key risk mitigations:

**Provenance Tracking**

Every KG write operation records:
- Agent ID (which Santiago made the change)
- Timestamp (when)
- Session ID (in what context)
- Optional reasoning justification (why)

This enables:
- **Audit trails** for autonomous decisions, critical for understanding evolutionary changes and debugging unexpected behavior
- **Rollback capability** when a problematic update is detected, we can identify all triples from that agent/session and revert them
- **Trust scoring** over time, we can measure which agents produce high-quality vs noisy KG updates

**Queued/Batched Writes**

Instead of direct synchronous KG writes, agents enqueue operations:
- Orchestrator flushes queue periodically (e.g., every 2 seconds or 50 operations)
- Conflicting writes (same subject+predicate) are detected and either merged or escalated for review
- Batch processing amortizes KG transaction overhead

This reduces risk of:
- **Race conditions** where two agents simultaneously update the same entity
- **Partial failures** corrupting KG state (batch is atomic)
- **Performance bottlenecks** from high write frequency

Together, provenance and queued writes provide the foundation for safe, auditable multi-agent KG collaboration in the Manolin Cluster architecture.

### References Cited

- ocean-research/nusy_manolin_architecture.md
- ocean-research/building-on-DGX/dgx_spark_nusy_report.md
- ocean-research/nusy_manolin_multi_agent_test_plans.md
- ocean-research/features-capabilities-for-shared-memory-and-evolution.md
- ocean-research/fake_team_pack/fake_team_steps_for_hank_and_copilot.md
