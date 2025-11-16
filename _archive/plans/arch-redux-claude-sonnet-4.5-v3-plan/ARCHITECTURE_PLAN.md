# Santiago Factory Architecture Plan

**Prepared by:** Claude-Sonnet-4.5
**Date:** 2025-11-16
**Version:** 3.0

---

## Executive Summary

Santiago is not a fixed team of AI agents but a self-bootstrapping factory that generates domain-specific Santiagos on demand. The system begins with Phase 0—deploying "fake" Santiagos as thin MCP proxies to external APIs (GPT-4, Claude, Copilot). This fake team then builds the factory itself in Phase 1: Navigator (orchestration), Catchfish (knowledge extraction), and Fishnet (BDD test generation). In Phase 2, the factory catches its first real Santiago—santiago-pm-safe-xp—from SAFe and XP sources, validates it through 3-5 cycles, and A/B tests it against the fake PM. Upon achieving ≥90% parity, the real Santiago replaces the proxy. Phase 3 repeats this progressive replacement for all roles. Phase 4 achieves self-sustainability: real Santiagos propose and implement factory improvements, optimizing Catchfish from 30-60m to <15m per source. The system becomes self-improving and can generate new domain Santiagos (finance, legal, healthcare) on demand.

---

## Current Architecture

`santiago_core/` contains active development with agent frameworks, ethical gating, and message passing, but lacks the MCP-facing factory machinery and the `knowledge/` directory for storing generated catches. `santiago-pm/` encodes development patterns (expeditions, tackle, voyage-trials) that teach hypothesis-driven development, but these aren't yet wired into automated fishing. `nusy_prototype/` proves the workflow: converting clinical guidelines to 4-layer models in 30-60 minutes with 3 validation cycles—this IS the factory pattern that needs industrialization. Legacy code in `src/nusy_pm_core/` and `santiago-code/` is archived. No MCP proxy layer exists, no Navigator/Catchfish/Fishnet implementation, and DGX Spark deployment (128GB RAM, 4TB+8TB NVMe, vLLM/TensorRT per `dgx_spark_nusy_report.md`) remains theoretical.

---

## Target Architecture

### Phase 0: Fake Team (Contractor Proxies)

Deploy thin MCP services in `santiago_core/agents/_proxy/` that proxy requests to external APIs. Each proxy loads role instructions from `knowledge/proxy-instructions/<role>.md`, exposes minimal tools (status, plan, execute_scenario), and queues requests through NuSy Orchestrator. Goal: operational fake team in <1 week, capable of coordinated compound tasks like backlog grooming + design sessions, with outputs logged in `ships-logs/` for provenance.

### Phase 1: Factory Components (Built by Fake Team)

Fake PM proposes factory, fake Architect designs Navigator/Catchfish/Fishnet, fake Developers implement them in `nusy_orchestrator/santiago_builder/`, fake QA validates with voyage-trials. Navigator orchestrates the 10-step "Old Man and the Sea" process. Catchfish ingests sources and produces 4-layer Markdown+YAML packages (Layer 1: raw text, Layer 2: entities/relationships, Layer 3: structured docs, Layer 4: KG queue). Fishnet analyzes KG to generate BDD scenarios and MCP manifests. Provenance tracking + queued writes prevent KG corruption. Phase completes with dress rehearsal: PDF → `knowledge/catches/demo/` with ≥95% BDD pass rate.

### Phase 2: First Catch & Replacement

Run full fishing expedition targeting santiago-pm-safe-xp. Navigator enforces 3-5 validation cycles, Catchfish iterates until <60m per source (target <15m), Fishnet emits BDDs and manifest. Fake QA scores each cycle. Deploy resulting MCP service in `santiago_core/agents/santiago-pm-safe-xp/service/`, spin it beside fake proxy, and A/B test on 10 canonical PM tasks. If real ≥90% of fake on quality (usually faster, cheaper), retire fake PM proxy and route all PM requests to new service. Store catch (domain-knowledge/, bdd-tests/, manifest, provenance) in `knowledge/catches/`.

### Phase 3: Progressive Replacement

Repeat Phase 2 for Architect-NuSy, Architect-Systems, Developer, QA, UX, Platform roles. Each replacement runs as hypothesis-driven expedition with BDD coverage and A/B testing. Some proxies may remain if sources lack depth—hybrid teams are acceptable. DGX Spark hosts shared Mistral-7B-Instruct via vLLM batching so 10+ Santiagos run concurrently sharing one loaded model. Concurrency and session-isolation tests follow `nusy_manolin_multi_agent_test_plans.md`.

### Phase 4: Self-Sustaining

Once most fake roles are replaced, real Santiagos form permanent crew. Santiago-PM proposes improving Catchfish parallelization, Santiago-Architect implements queue-aware KG writes, Santiago-Developer updates orchestrator, Santiago-QA runs regression voyage-trials. Improvements are treated as fishing expeditions, logged in ships-logs, validated through A/B deployments on DGX. Factory generates new domain Santiagos (finance, legal) on demand and continuously reduces Catchfish cycle time below 15 minutes.

---

## Key Architectural Components

### Navigator

Implements 10-step fishing process from `santiago-pm/strategic-charts/Old man and the sea.md`: (1) Vision—define MCP services/behaviors, (2) Raw Materials—collect sources, (3) Catchfish extraction, (4) Indexing for referenceability, (5) Ontology loading—schemas/naming, (6) KG Building, (7) Fishnet BDD generation, (8) Navigator validation loop (3-5 cycles), (9) Deployment—generate MCP manifest, (10) Learning—improve from logs/metrics. Navigator sequences these steps, enforces quality KPIs (≥95% BDD pass rate, provenance completeness), records hypotheses/decisions in voyage-trials.

### Catchfish

Converts raw PDFs, APIs, notes into 4-layer structure proven in clinical prototype. Tracks per-source timing (baseline 30-60m, target <15m), maintains provenance (source hash, timestamp, agent ID). Supports pluggable extractors (LLM summarization, deterministic parsing) so domains beyond PM can be ingested. Layer 1: extract raw text, Layer 2: identify entities/relationships, Layer 3: write Markdown+YAML packages, Layer 4: queue KG triples with schema validation.

### Fishnet

BDD+manifest generator that inspects KG and writes `.feature` files mapped to voyage-trials plus `mcp-manifest.json` describing tools, capability levels (Apprentice/Journeyman/Master), knowledge scope (Pond/Lake/Sea/Ocean). Fishnet infers concurrency risks (if tool mutates KG) and contributes metadata for Ethics & Concurrency gating.

### Fake Team Proxies

Located in `santiago_core/agents/_proxy/`, each proxy MCP service reads role instructions, forwards reasoning to GPT-4/Claude/Copilot, returns structured responses. Expose metrics (latency, cost) so replacement benefits are measurable. Rely on shared memory in `knowledge/shared/` (team roster TTL, working agreements) per `fake_team_pack/` guidance.

### Knowledge Storage

Create `knowledge/` with:

- `catches/<santiago-name>/domain-knowledge/` (Layer 3 files)
- `catches/<santiago-name>/bdd-tests/` (Fishnet outputs)
- `catches/<santiago-name>/mcp-manifest.json` (auto-generated)
- `catches/<santiago-name>/provenance.yaml` (expedition metadata)
- `templates/` for base catch structure
- `proxy-instructions/` for fake team role cards

Storage on DGX Spark's 4TB NVMe, with overflow to 8-16TB external NVMe RAID per `dgx_spark_nusy_report.md`.

---

## MCP Integration

Every fake and real Santiago is an MCP service with auto-generated `mcp-manifest.json` from Fishnet summarizing tools (`provide_backlog_plan`, `design_kg_extension`, etc.), auth, invocation semantics. Tooling routes through NuSy Orchestrator for shared governance, logging, Ethics gating. Manifest regeneration triggered whenever Fishnet updates tests or knowledge; Navigator invalidates older manifests. Manifest registry in `knowledge/catches/index.yaml` shows which Santiagos are trustworthy (≥90% parity) vs experimental.

---

## DGX Deployment

DGX Spark provides 128GB unified memory and 4TB NVMe; add 8-16TB external NVMe RAID for model zoo and KG history. vLLM or TensorRT-LLM hosts Mistral-7B-Instruct once, exposing batched inference to all agents. Kubernetes is overkill initially; use systemd services or lightweight orchestration plus observability (Prometheus + Loki) for GPU/memory metrics. Storage tiers: hot (internal NVMe) for working catches and models, warm (external RAID) for historical catches and experiments, cold (NAS) for archives.

---

## Ethics & Concurrency Gating

Embed Ethics & Concurrency gating inside NuSy Orchestrator:

- Every tool call is queued with metadata (role, intent, knowledge references) and screened by fake (later real) Santiago-Ethicist before execution
- Concurrency guardrails follow `nusy_manolin_multi_agent_test_plans.md`: session isolation, tool locking, load SLOs (P95 latency <6s under 10-agent load)
- All KG mutations run through queued write pipeline with automated provenance stamping (agent id, timestamp, hypothesis reference) to prevent corruption
- Ethics gating verifies fishing expeditions respect source licensing and usage constraints

---

## References Cited

- `ocean-research/00-ARCHITECTURE-PATTERN.md`
- `santiago-pm/strategic-charts/Old man and the sea.md`
- `ocean-research/building-on-DGX/dgx_spark_nusy_report.md`
- `ocean-research/nusy_manolin_architecture.md`
- `ocean-research/nusy_manolin_multi_agent_test_plans.md`
- `ocean-research/fake_team_pack/`
- `nusy_prototype/neurosymbolic-clinical-reasoner-technical-summary.md` (30-60m conversion, 3 validation cycles)
- `santiago-pm/expeditions/`, `santiago-pm/tackle/`, `santiago-pm/voyage-trials/` (development patterns)
