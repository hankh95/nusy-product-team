# Migration Steps — 2025-11-16

**Metadata**
Model Name: Claude Sonnet 4.5
Model Version: claude-sonnet-4.5-20250514
Date: 2025-11-16
Repo Commit SHA: 5bfcc00
Run ID: arch-redux-claude-sonnet-4.5-2025-11-16

## Milestone 1: Establish Shared Knowledge Foundation

Goals:
- Create repository-level `knowledge/` folder structure
- Define initial working agreements and team contracts
- Enable persistent cross-session memory for all agents

Affected Paths:
- `knowledge/` (new)
- `knowledge/shared/`
- `knowledge/domains/`
- Root README.md (update to reference knowledge tree)

Tasks:
- [ ] Create `knowledge/shared/` directory structure
- [ ] Create `knowledge/domains/pm/`, `knowledge/domains/ethics/`, `knowledge/domains/architecture/` directories
- [ ] Write `knowledge/shared/working-agreements.md` capturing BDD/TDD practices from `DEVELOPMENT_PRACTICES.md`
- [ ] Write `knowledge/shared/bdd-practices.md` with executable specification templates
- [ ] Write `knowledge/shared/tools-and-mcp-capabilities.md` listing planned MCP services
- [ ] Create `knowledge/shared/team-roster-and-capabilities.ttl` RDF schema with:
  - Agent identity properties
  - Skill level vocabulary (Apprentice/Journeyman/Master)
  - Knowledge scope vocabulary (Pond/Lake/Sea/Ocean)
  - Tool capability predicates
- [ ] Create `knowledge/shared/ships-log/` directory for evolutionary decision tracking
- [ ] Write initial ship's log entry documenting migration launch
- [ ] Update repository README.md to explain `knowledge/` tree purpose and structure

Acceptance Criteria:
- `knowledge/` skeleton is created with all required shared and domain directories
- Initial RDF team roster validates with `rapper` or equivalent Turtle parser
- At least one ship's log entry exists demonstrating the format
- Working agreements document references specific sections of `DEVELOPMENT_PRACTICES.md`

## Milestone 2: Implement Santiago-PM and Santiago-Ethicist MCP Services

Goals:
- Convert PM and Ethicist agents to MCP service architecture
- Establish pattern for all subsequent role migrations
- Enable capability discovery via MCP manifests

Affected Paths:
- `santiago_core/agents/santiago_pm.py` (refactor)
- `santiago_core/agents/santiago_ethicist.py` (new)
- `mcp/registry/` (new)
- `mcp/manifests/pm.json` (new)
- `mcp/manifests/ethicist.json` (new)

Tasks:
- [ ] Create `mcp/registry/` directory for manifest storage
- [ ] Define MCP manifest schema template incorporating:
  - role, skill-level, knowledge-scope fields
  - tools array with input/output contracts
  - dependencies on other services
- [ ] Write `mcp/manifests/pm.json` declaring:
  - role: "PM"
  - skill-level: "Master"
  - knowledge-scope: "Sea"
  - tools: `read_working_agreements`, `update_working_agreements`, `read_team_roster`, `propose_evolution_cycle`
- [ ] Write `mcp/manifests/ethicist.json` declaring:
  - role: "Ethicist"
  - skill-level: "Journeyman"
  - knowledge-scope: "Lake"
  - tools: `review_evolution_plan`, `write_ethics_note`
- [ ] Refactor `santiago_core/agents/santiago_pm.py` to expose MCP endpoints
- [ ] Implement new `santiago_core/agents/santiago_ethicist.py` with ethics review logic
- [ ] Create `santiago_core/services/mcp_adapter.py` for MCP protocol handling
- [ ] Wire PM and Ethicist services to read/write `knowledge/shared/` and `knowledge/domains/`
- [ ] Add registration logic to populate `knowledge/shared/team-roster-and-capabilities.ttl` on service startup

Acceptance Criteria:
- Santiago-PM exposes functional MCP endpoints and reads working agreements from `knowledge/shared/`
- Santiago-Ethicist can review a sample evolution proposal and write to `knowledge/domains/ethics/evolution-reviews.md`
- Both services register their capabilities in the team roster RDF graph on startup
- MCP manifests validate against schema

## Milestone 3: Build Unified Knowledge Graph Interaction Layer

Goals:
- Replace direct KG service calls with queued, provenance-tracked writes
- Prevent concurrent update conflicts
- Enable audit trails for autonomous agent decisions

Affected Paths:
- `santiago_core/services/knowledge_graph.py` (refactor)
- `santiago_core/services/kg_queue.py` (new)
- `santiago_core/services/kg_provenance.py` (new)
- `santiago_core/services/kg_validator.py` (new)

Tasks:
- [ ] Design queued write API:
  - `kg_queue.enqueue_write(agent_id, operation, triples, priority)`
  - `kg_queue.process_batch()` for periodic flushing
- [ ] Implement `santiago_core/services/kg_queue.py` with:
  - In-memory queue with priority levels
  - Batch processing logic (flush every N seconds or M operations)
  - Conflict detection (same subject+predicate updates from different agents)
- [ ] Implement `santiago_core/services/kg_provenance.py` tracking:
  - Agent identity for each write
  - Timestamp
  - Reasoning justification (optional string)
- [ ] Implement `santiago_core/services/kg_validator.py` enforcing:
  - NuSy ontology constraints (class/property definitions)
  - Required property validation
  - Type checking for literals
- [ ] Refactor `santiago_core/services/knowledge_graph.py` to:
  - Route all writes through `kg_queue`
  - Attach provenance metadata automatically
  - Validate before enqueue
  - Preserve fast read paths (no queueing for queries)
- [ ] Update Santiago-PM and Santiago-Ethicist to use new KG layer
- [ ] Add monitoring/logging for queue depth and processing latency

Acceptance Criteria:
- Concurrent writes from 3+ agents are correctly queued and do not corrupt KG
- Provenance metadata is recorded for all writes and queryable via SPARQL
- Schema validation rejects invalid triples with clear error messages
- Read performance remains within 10% of direct access baseline

## Milestone 4: Develop NuSy Orchestrator with Ethics & Concurrency Gating

Goals:
- Create production FastAPI orchestrator replacing archived prototype
- Implement session management for concurrent agents
- Enforce ethics gating for high-risk operations

Affected Paths:
- `nusy_orchestrator/` (new)
- `nusy_orchestrator/main.py` (new)
- `nusy_orchestrator/session_manager.py` (new)
- `nusy_orchestrator/ethics_gate.py` (new)
- `nusy_orchestrator/mcp_router.py` (new)

Tasks:
- [ ] Create `nusy_orchestrator/` directory structure
- [ ] Implement `nusy_orchestrator/main.py` FastAPI application with:
  - `/mcp/{role}/invoke` endpoints for tool calls
  - `/session/create` and `/session/status` endpoints
  - Health check and metrics endpoints
- [ ] Implement `nusy_orchestrator/session_manager.py` providing:
  - Session ID generation and lifecycle management
  - Context isolation (prevent cross-session data leakage)
  - Session timeout and cleanup
- [ ] Implement `nusy_orchestrator/ethics_gate.py` providing **Ethics & Concurrency Gating**:
  - Pre-execution review of operations flagged as high-risk
  - Integration with Santiago-Ethicist MCP service for policy checks
  - Configurable risk thresholds and approval flows
  - Audit logging of gated operations and decisions
- [ ] Implement `nusy_orchestrator/mcp_router.py` for:
  - Dynamic MCP service discovery from `mcp/registry/`
  - Request routing based on role
  - Load balancing for multiple instances of same role
- [ ] Wire orchestrator to shared LLM runtime (stub for now, real integration in Milestone 6)
- [ ] Wire orchestrator to unified KG interaction layer
- [ ] Add concurrency test suite covering:
  - Session isolation (from `ocean-research/nusy_manolin_multi_agent_test_plans.md` scenarios)
  - Tool invocation race conditions
  - Ethics gate enforcement under load

Acceptance Criteria:
- Orchestrator successfully routes requests to Santiago-PM and Santiago-Ethicist MCP services
- 10 concurrent sessions can execute without context leakage (validated by test)
- Ethics gate successfully blocks high-risk operations and logs review decisions
- Session manager prevents stale session accumulation with timeout cleanup

## Milestone 5: Implement Multi-Agent Concurrency Test Harness

Goals:
- Validate system behavior under realistic concurrent load
- Establish SLO baselines for latency and throughput
- Detect session isolation and race condition bugs

Affected Paths:
- `tests/concurrency/` (new)
- `tests/concurrency/test_session_isolation.py` (new)
- `tests/concurrency/test_tool_races.py` (new)
- `tests/concurrency/load_profiles.py` (new)

Tasks:
- [ ] Create `tests/concurrency/` directory
- [ ] Implement `test_session_isolation.py` covering:
  - PM-1 scenario: 3 concurrent sessions on different products with BDD generation
  - AR-NUSY-1 scenario: concurrent KG schema extensions
  - Validation: no cross-session context leakage
- [ ] Implement `test_tool_races.py` covering:
  - PM-2 scenario: concurrent priority changes on shared product board
  - DEV-1 scenario: concurrent feature implementations writing to overlapping files
  - Validation: conflicts are detected and handled deterministically
- [ ] Implement `load_profiles.py` with:
  - Baseline load: 10 agents, mixed small/medium tasks
  - Stress load: 20 agents, sustained activity
  - Spike load: 50 concurrent requests for 30 seconds
- [ ] Add observability:
  - Prometheus metrics export from orchestrator
  - Grafana dashboard template for latency, throughput, queue depth
- [ ] Document SLO targets:
  - P95 latency < 4 seconds for medium tasks
  - Error rate < 1% under baseline load
  - Zero context leakage violations
- [ ] Wire test harness into CI (GitHub Actions or similar)

Acceptance Criteria:
- All session isolation tests pass with zero leakage violations
- Tool race condition tests pass with deterministic conflict resolution
- Baseline load profile executes with P95 latency within SLO
- Test results are published to CI artifacts for each run

## Milestone 6: DGX Spark Deployment and Infrastructure Automation

Goals:
- Enable production deployment on DGX Spark hardware
- Automate model serving, storage setup, and service orchestration
- Provide runbooks for operations

Affected Paths:
- `infra/dgx/` (new)
- `infra/dgx/provision.sh` (new)
- `infra/dgx/docker-compose.yml` (new)
- `infra/dgx/storage-layout.md` (new)
- `infra/dgx/runbooks/` (new)

Tasks:
- [ ] Create `infra/dgx/` directory structure
- [ ] Write `infra/dgx/storage-layout.md` documenting:
  - Internal 4 TB NVMe: OS, repos, active models, hot KG indexes
  - External NVMe RAID: model zoo, KG snapshots, vector DB, experiment archives
  - Mount points and permissions
- [ ] Implement `infra/dgx/provision.sh` automating:
  - CUDA/cuDNN installation verification
  - Docker and Docker Compose setup
  - vLLM or TensorRT-LLM installation for Mistral-7B-Instruct serving
  - Vector DB (Qdrant or pgvector) installation
  - Graph DB (Blazegraph or Neo4j) installation
- [ ] Write `infra/dgx/docker-compose.yml` orchestrating:
  - LLM runtime service (vLLM serving Mistral-7B-Instruct)
  - NuSy orchestrator (FastAPI)
  - MCP services (PM, Ethicist, Architect, Developer, QA, UX, Platform)
  - Vector DB service
  - Graph DB service
  - Git forge (Gitea or GitLab CE)
- [ ] Document model loading strategy:
  - Single shared Mistral-7B-Instruct instance
  - Request batching and concurrency handling
  - Memory budget allocation (128 GB unified memory)
- [ ] Create runbooks:
  - `infra/dgx/runbooks/deployment.md`: Initial setup and deployment
  - `infra/dgx/runbooks/scaling.md`: Adding new agent roles or model variants
  - `infra/dgx/runbooks/backup-restore.md`: KG snapshots and disaster recovery
  - `infra/dgx/runbooks/monitoring.md`: Observability setup and dashboards
- [ ] Document interim "fake team" strategy:
  - Use external LLM API (OpenAI, Anthropic) as fallback when DGX unavailable
  - MCP services proxy to external API via `llm_proxy.call(model, prompt)`
  - Transition plan from proxy to local DGX serving

Acceptance Criteria:
- `provision.sh` successfully sets up all required services on a fresh DGX Spark system
- `docker-compose.yml` brings up full stack with health checks passing
- Storage layout document specifies mount points and capacity planning validated against `ocean-research/building-on-DGX/dgx_spark_nusy_report.md` recommendations
- Runbooks provide step-by-step procedures for deployment, scaling, backup, and monitoring
- Interim fake team mode documented per `ocean-research/fake_team_pack/fake_team_steps_for_hank_and_copilot.md`

## Milestone 7: Additional Role Migrations and Evolutionary Cycles

Goals:
- Migrate remaining agent roles to MCP services
- Enable team to operate autonomously with full role coverage
- Establish evolutionary improvement patterns

Affected Paths:
- `santiago_core/agents/santiago_architect.py` (refactor to two services)
- `santiago_core/agents/santiago_developer.py` (refactor)
- `santiago_core/agents/santiago_qa.py` (new)
- `santiago_core/agents/santiago_ux.py` (new)
- `santiago_core/agents/santiago_platform.py` (new)
- `mcp/manifests/` (additional manifests)
- `knowledge/shared/ships-log/` (ongoing evolution logs)

Tasks:
- [ ] Split Architect role into two MCP services:
  - Architect-NuSy (focuses on KG design, reasoning patterns, ontology)
  - Architect-Systems (focuses on infrastructure, platform, scaling)
- [ ] Migrate Developer agent to MCP service with tools:
  - `implement_feature`, `write_tests`, `refactor_code`
- [ ] Implement QA Specialist MCP service with tools:
  - `extend_test_suite`, `review_coverage`, `run_regression`
- [ ] Implement UX Researcher/Designer MCP service with tools:
  - `map_user_journey`, `synthesize_insights`, `propose_interface`
- [ ] Implement Platform/Deployment Engineer MCP service with tools:
  - `deploy_service`, `rollback`, `monitor_health`
- [ ] Create MCP manifests for all new services with skill levels and knowledge scopes
- [ ] Update team roster RDF with new agent registrations
- [ ] Document first evolutionary cycle:
  - Hypothesis: "Separating Architect roles improves specialization and reduces context confusion"
  - Experiment: Run parallel architecture tasks and measure output quality
  - Ship's log entry recording outcome and decision to promote or adjust
- [ ] Enable Santiago-PM to propose next evolutionary cycle autonomously

Acceptance Criteria:
- All seven core roles (PM, Ethicist, Architect-NuSy, Architect-Systems, Developer, QA, UX, Platform) are operational as MCP services
- Team roster accurately reflects all agents with correct skill levels and scopes
- At least one complete evolutionary cycle is documented in ships logs with hypothesis, experiment, and outcome
- Santiago-PM can autonomously generate evolution cycle proposals

### References Cited

- ocean-research/nusy_manolin_architecture.md
- ocean-research/building-on-DGX/dgx_spark_nusy_report.md
- ocean-research/nusy_manolin_multi_agent_test_plans.md
- ocean-research/features-capabilities-for-shared-memory-and-evolution.md
- ocean-research/fake_team_pack/fake_team_feature_plan.md
- ocean-research/fake_team_pack/fake_team_steps_for_hank_and_copilot.md
