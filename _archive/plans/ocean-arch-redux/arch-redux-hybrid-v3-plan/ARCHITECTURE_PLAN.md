# Santiago Factory Architecture Plan

**Prepared by:** Hybrid Synthesis (Claude Sonnet 4.5 + Combined Meta-Plan)
**Date:** 2025-11-16
**Version:** 3.0

---

## Executive Summary

Santiago is not a fixed team of AI agents but a self-bootstrapping factory that generates domain-specific Santiagos on demand. The system begins with Phase 0—deploying "fake" Santiagos as thin MCP proxies to external APIs (GPT-4, Claude, Copilot). This fake team then builds the factory itself in Phase 1: Navigator (orchestration), Catchfish (knowledge extraction), and Fishnet (BDD test generation). In Phase 2, the factory catches its first real Santiago—santiago-pm-safe-xp—from SAFe and XP sources, validates it through 3-5 cycles, and A/B tests it against the fake PM. Upon achieving ≥90% parity, the real Santiago replaces the proxy via canary routing (10% → 50% → 100%). Phase 3 repeats this progressive replacement for all roles. Phase 4 achieves self-sustainability: real Santiagos propose and implement factory improvements, optimizing Catchfish from 30-60m to <15m per source. The system becomes self-improving and can generate new domain Santiagos (finance, legal, healthcare) on demand, reducing operational costs by 85% while maintaining quality through contract-driven validation and schema-enforced governance.

---

## Current Architecture

`santiago_core/` contains active development with agent frameworks, ethical gating, and message passing, but lacks the MCP-facing factory machinery and the `knowledge/` directory for storing generated catches. `santiago-pm/` encodes development patterns (expeditions, tackle, voyage-trials) that teach hypothesis-driven development, but these aren't yet wired into automated fishing. `nusy_prototype/` proves the workflow: converting clinical guidelines to 4-layer models in 30-60 minutes with 3 validation cycles—this IS the factory pattern that needs industrialization. Legacy code in `src/nusy_pm_core/` and `santiago-code/` is archived. No MCP proxy layer exists, no Navigator/Catchfish/Fishnet implementation, and DGX Spark deployment (128GB RAM, 4TB+8TB NVMe, vLLM/TensorRT per `dgx_spark_nusy_report.md`) remains theoretical.

---

## Target Architecture

### Phase 0: Fake Team (Contractor Proxies)

Deploy thin MCP services in `santiago_core/agents/_proxy/` that proxy requests to external APIs. Each proxy loads role instructions from `knowledge/proxy-instructions/<role>.md`, exposes minimal tools (status, plan, execute_scenario), and queues requests through NuSy Orchestrator. MCP manifests define service contracts with versioned capabilities (e.g., `service.version: 1.0`), TTL, and budget hints. Goal: operational fake team in <1 week, capable of coordinated compound tasks like backlog grooming + design sessions, with outputs logged in `ships-logs/` for provenance.

### Phase 1: Factory Components (Built by Fake Team)

Fake PM proposes factory, fake Architect designs Navigator/Catchfish/Fishnet, fake Developers implement them in `nusy_orchestrator/santiago_builder/`, fake QA validates with voyage-trials. Navigator orchestrates the 10-step "Old Man and the Sea" process. Catchfish ingests sources and produces 4-layer Markdown+YAML packages (Layer 1: raw text, Layer 2: entities/relationships, Layer 3: structured docs, Layer 4: KG queue). Fishnet analyzes KG to generate BDD scenarios, MCP manifests with capability levels (Apprentice/Journeyman/Master), and knowledge scope tags (Pond/Lake/Sea/Ocean). Provenance tracking + queued writes with schema validation prevent KG corruption. Phase completes with dress rehearsal: PDF → `knowledge/catches/demo/` with ≥95% BDD pass rate and contract test validation.

### Phase 2: First Catch & Replacement

Run full fishing expedition targeting santiago-pm-safe-xp. Navigator enforces 3-5 validation cycles, Catchfish iterates until <60m per source (target <15m), Fishnet emits BDDs and manifest. Fake QA scores each cycle. Deploy resulting MCP service in `santiago_core/agents/santiago-pm-safe-xp/service/`, spin it beside fake proxy, and A/B test on 10 canonical PM tasks. Canary routing starts at 10% for 1-2 hours; if parity holds, ramp to 50%, then 100%. If real ≥90% of fake on quality (usually faster, cheaper due to DGX-served model), retire fake PM proxy and route all PM requests to new service. Store catch (domain-knowledge/, bdd-tests/, manifest, provenance) in `knowledge/catches/` with trust registry entry showing version, hash, BDD pass rate, and replacement decision.

### Phase 3: Progressive Replacement

Repeat Phase 2 for Architect-NuSy, Architect-Systems, Developer, QA, UX, Platform roles. Each replacement runs as hypothesis-driven expedition with BDD coverage and A/B testing. Hybrid routing allows 80/20 traffic splits during transition periods with metrics dashboards tracking parity, latency, cost per role. Some proxies may remain if sources lack depth—hybrid teams are acceptable. DGX Spark hosts shared Mistral-7B-Instruct via vLLM batching so 10+ Santiagos run concurrently sharing one loaded model. Concurrency and session-isolation tests follow `nusy_manolin_multi_agent_test_plans.md`.

### Phase 4: Self-Sustaining

Once most fake roles are replaced, real Santiagos form permanent crew. Santiago-PM proposes improving Catchfish parallelization, Santiago-Architect implements queue-aware KG writes, Santiago-Developer updates orchestrator, Santiago-QA runs regression voyage-trials. Improvements are treated as fishing expeditions, logged in ships-logs, validated through A/B deployments on DGX, and promoted via RFC process with rehearsal gates (≥95% BDD pass). Factory generates new domain Santiagos (finance, legal) on demand and continuously reduces Catchfish cycle time below 15 minutes while real Santiagos improve the factory itself.

---

## Key Architectural Components

### Navigator

Implements 10-step fishing process from `santiago-pm/strategic-charts/Old man and the sea.md`: (1) Vision—define MCP services/behaviors, (2) Raw Materials—collect sources, (3) Catchfish extraction, (4) Indexing for referenceability, (5) Ontology loading—schemas/naming, (6) KG Building, (7) Fishnet BDD generation, (8) Navigator validation loop (3-5 cycles), (9) Deployment—generate MCP manifest, (10) Learning—improve from logs/metrics. Navigator sequences these steps, enforces quality KPIs (≥95% BDD pass rate, provenance completeness), tracks metrics (cycle count, pass rate, time per source), records hypotheses/decisions in voyage-trials, and coordinates Catchfish and Fishnet.

### Catchfish

Converts raw PDFs, APIs, notes into 4-layer structure proven in clinical prototype. Tracks per-source timing (baseline 30-60m, target <15m), maintains provenance (source hash, timestamp, agent ID). Supports pluggable extractors (LLM summarization, deterministic parsing) so domains beyond PM can be ingested. Layer 1: extract raw text, Layer 2: identify entities/relationships, Layer 3: write Markdown+YAML packages, Layer 4: queue KG triples with schema validation. Outputs feed Fishnet and the KG write queue.

### Fishnet

BDD+manifest generator that inspects KG and writes `.feature` files mapped to voyage-trials plus `mcp-manifest.json` describing tools, capability levels (Apprentice/Journeyman/Master), knowledge scope (Pond/Lake/Sea/Ocean), and budget hints. Fishnet infers concurrency risks (if tool mutates KG), generates contract acceptance tests, maintains coverage ratios, links tests back to knowledge nodes for traceability, and proposes new tests for gaps. Contributes metadata for Ethics & Concurrency gating.

### Fake Team Proxies

Located in `santiago_core/agents/_proxy/`, each proxy MCP service reads role instructions, forwards reasoning to GPT-4/Claude/Copilot, returns structured responses. Expose metrics (latency, cost) so replacement benefits are measurable. Implement the same MCP interface contract as real Santiagos, enabling seamless replacement. Rely on shared memory in `knowledge/shared/` (team roster TTL, working agreements) per `fake_team_pack/` guidance. Each proxy loads `knowledge/proxy-instructions/<role>.md`.

### Knowledge Storage

Create `knowledge/` with:

- `catches/index.yaml` — Trust registry (versions, hashes, BDD pass rates, capability levels, replacement decisions)
- `catches/<santiago-name>/domain-knowledge/` — Markdown + YAML frontmatter (Layer 3 files)
- `catches/<santiago-name>/bdd-tests/` — Fishnet outputs linked to knowledge nodes
- `catches/<santiago-name>/mcp-manifest.json` — Auto-generated with contract schema
- `catches/<santiago-name>/provenance.yaml` — Expedition metadata (sources, cycles, timestamps, authorship)
- `templates/` — Base structures for generating Santiagos
- `proxy-instructions/` — Role definitions for fake team

Storage on DGX Spark's 4TB internal NVMe (hot tier), with overflow to 8-16TB external NVMe RAID (warm tier) per `dgx_spark_nusy_report.md`, and historical archives to NAS (cold tier).

---

## Interfaces & Contracts

### MCP Service Interface Contract

Each Santiago exposes a versioned service interface with declared tools, parameters, and guarantees. Contracts are validated via contract tests and manifests include TTL, capability level, and budget gates.

```json
{
  "service": {
    "id": "santiago-pm-safe-xp",
    "version": "1.0",
    "capability_level": "Journeyman",
    "knowledge_scope": "Lake",
    "ttl_seconds": 3600,
    "capabilities": ["planning", "bdd.validate", "kg.query"],
    "budget": {"unit": "usd", "daily_limit": 25.0}
  },
  "tools": [
    {"name": "plan_epic", "inputs": {"goal": "string"}, "returns": {"plan_id": "string"}},
    {"name": "bdd_validate", "inputs": {"feature": "string"}, "returns": {"pass_rate": "number"}}
  ]
}
```

### Contract Acceptance Tests

- Given a valid manifest, the service advertises all tools with correct I/O shapes
- When a tool is invoked with schema-valid inputs, it must return schema-valid outputs within SLO latency
- When budget is exceeded, service responds with a throttling error and retry-after
- When capability level is Apprentice, complex requests must escalate or defer

---

## MCP Integration

Every fake and real Santiago is an MCP service with auto-generated `mcp-manifest.json` from Fishnet summarizing tools (`provide_backlog_plan`, `design_kg_extension`, etc.), capability levels, knowledge scope, auth, and invocation semantics. Tooling routes through NuSy Orchestrator for shared governance, logging, Ethics gating. Manifest regeneration triggered whenever Fishnet updates tests or knowledge; Navigator invalidates older manifests. Orchestrator invokes services via MCP; tools are declared in manifests; services communicate through queued requests with backpressure and budget gates. Discovery reads from trust registry (`knowledge/catches/index.yaml`).

---

## DGX Deployment

DGX Spark provides 128GB unified memory and 4TB internal NVMe; add 8-16TB external NVMe RAID for model zoo and KG history. vLLM or TensorRT-LLM hosts Mistral-7B-Instruct once, exposing batched inference to all agents. Kubernetes is overkill initially; use systemd services or lightweight orchestration plus observability (Prometheus + Loki) for GPU/memory metrics.

### Storage Tiers

- **Hot (Internal 4TB NVMe)**: Working catches, active models, current KG state
- **Warm (External 8-16TB RAID)**: Historical catches, experiments, older model checkpoints
- **Cold (NAS)**: Long-term archives, audit logs, provenance ledgers

### SLOs & Budgets

- **SLO Targets (per request, steady-state):**
  - p95 latency: ≤ 1800 ms (proxy) / ≤ 2500 ms (real, DGX-served)
  - Error rate: ≤ 1%
  - Cost per request: ≤ 0.03 USD (real, DGX-served)
- **Throughput**: Sustain ≥ 20 RPS aggregate across roles with continuous batching; nominal batch size 8–16
- **Budgets**: Per-role daily budgets enforced at orchestrator; default 25 USD/day/role, adjustable via config
- **Dashboards**: Latency histograms, throughput, cost-per-request, queue depth, rejection rate, A/B parity trend, capability level distribution

---

## Ethics & Concurrency Gating

Embed Ethics & Concurrency gating inside NuSy Orchestrator:

- **Queue-first tool execution**: All KG writes pass through a queue with schema validation, provenance stamping, and trust checks before commit
- **Santiago-Ethicist proxy/service**: Pre-execution review for risky actions and post-execution audits. Escalate to human-in-the-loop for flagged items
- **Concurrency guardrails** follow `nusy_manolin_multi_agent_test_plans.md`: session isolation, tool locking, load SLOs (P95 latency <6s under 10-agent load), per-entity locks in KG write pipeline
- **Budget gates and rate limiting** at orchestrator; A/B gates require ≥90% parity before replacement; rehearsal gates require ≥95% BDD pass before deploy
- **Ethics gating** verifies fishing expeditions respect source licensing and usage constraints

### KG Write Queue Contract

Event Schema (write-intent):

```yaml
schema_version: 1
event_id: uuid
entity_key: "knowledge:catches:santiago-pm-safe-xp:node-123"
operation: upsert # or delete
author: { type: "santiago", id: "santiago-pm-safe-xp@1.0" }
provenance_ref: "knowledge/catches/santiago-pm-safe-xp/provenance.yaml#2025-11-16T12:34:56Z"
diff: { before: {}, after: { title: "XP Pairing", links: ["..."] } }
approvals: ["ethicist@1.0"]
idempotency_key: "sha256:..."
```

Guarantees:

- Per-entity locks (advisory) to serialize writes by `entity_key`
- Idempotent processing via `idempotency_key`
- Schema validation before commit; on failure, write is rejected with actionable diagnostics
- Queue runs on idempotent jobs with retry + dead-letter semantics
- Failed mutations logged separately for debugging
- All queue events stream to observability stack (Loki) for forensics

---

## Provenance & Trust Registry

### Orchestrator Registry

`knowledge/catches/index.yaml` consolidates all caught Santiagos and their validation status:

```yaml
schema_version: 1
catches:
  - id: santiago-pm-safe-xp
    version: 1.0.0
    hash: "sha256:..."
    capability_level: Journeyman
    knowledge_scope: Lake
    sources:
      - ocean-research/dgx_spark_nusy_report.md
      - ocean-research/nusy_manolin_architecture.md
    bdd_pass_rate: 0.96
    replacement:
      proxy: santiago-pm-proxy@1.0
      decision: approved
      rationale: ">=90% A/B parity across 15 tasks"
      traffic_split: {real: 100, proxy: 0}
    provenance: knowledge/catches/santiago-pm-safe-xp/provenance.yaml
    signed_by: copilot@2025-11-16
    timestamp: 2025-11-16T16:45:00Z
```

### Registry Guarantees

- Every deployed real Santiago has an entry with version, hash, pass rate, capability level, and replacement decision
- Orchestrator consults the registry to route traffic and enforce fallbacks
- Allows hybrid deployments: route 80% to real, 20% to fake during transition
- Registry records trust scores (A/B parity %), validation count, last updated

### Audit & Replay

- Queue assigns sequence numbers, validates against schema
- If corruption detected, replay from provenance ledger to last known good state
- All merged changes update `index.yaml`
- Failed mutations logged with diagnostics for retrospective analysis

---

## References Cited

- `ocean-research/00-ARCHITECTURE-PATTERN.md`
- `santiago-pm/strategic-charts/Old man and the sea.md`
- `ocean-research/building-on-DGX/dgx_spark_nusy_report.md`
- `ocean-research/dgx_spark_nusy_report.md`
- `ocean-research/nusy_manolin_architecture.md`
- `ocean-research/nusy_manolin_provisioning_automation.md`
- `ocean-research/nusy_manolin_multi_agent_test_plans.md`
- `ocean-research/fake_team_feature_plan.md`
- `ocean-research/fake_team_steps_for_hank_and_copilot.md`
- `ocean-research/fake_team_pack/`
- `nusy_prototype/neurosymbolic-clinical-reasoner-technical-summary.md` (30-60m conversion, 3 validation cycles)
- `santiago-pm/expeditions/`, `santiago-pm/tackle/`, `santiago-pm/voyage-trials/` (development patterns)
