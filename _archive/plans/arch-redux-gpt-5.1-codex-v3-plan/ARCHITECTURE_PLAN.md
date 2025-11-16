# Santiago Factory Architecture Plan

**Prepared by:** GPT-5.1-Codex
**Date:** 2025-11-16
**Version:** 3.0

---

## Executive Summary

NuSy is shifting from hand-crafted agent teams to a Santiago factory that bootstraps its own workforce. Phase 0 establishes a "fake" MCP team by wrapping external APIs so we can start shipping in hours. That fake team immediately builds the factory itself—Navigator to run fishing expeditions, Catchfish to convert raw sources in 30-60 minutes (with a <15 minute target), and Fishnet to turn the knowledge graph into behavior tests and MCP manifests. Once the factory is live, it catches a real Santiago-PM (e.g., SAFe+XP blend), A/B tests it against the fake contractor, and replaces the proxy at ≥90% parity. Further catches progressively retire the rest of the fake crew until the system becomes self-sustaining and improvements originate from real Santiagos.

---

## Current Architecture

- **santiago_core/** hosts the active autonomous framework (PM, Architect, Developer) with ethical gating, message passing, and partial knowledge facilities, but no MCP-facing factory machinery or shared catches.
- **santiago-pm/** encodes the development patterns (expeditions, tackle, voyage-trials) that fake team members must follow; these artifacts already teach hypothesis-driven development but remain disconnected from automated fishing.
- **nusy_prototype/** proves the workflow: converting clinical guidelines to a 4-layer model takes 30-60 minutes and needs ~3 validation cycles, and once converted everything runs in-memory with real-time query performance.
- **src/nusy_pm_core/** is archived; knowledge/ folder is missing entirely, so there is nowhere to store generated catches.
- No MCP proxy layer exists yet, no Navigator/Catchfish/Fishnet implementation, and DGX Spark deployment (4 TB internal + 8-16 TB external NVMe per `building-on-DGX/dgx_spark_nusy_report.md`) is still theoretical.

---

## Target Architecture

### Phase 0: Fake Team (Contractor Proxies)

Create thin MCP services under `santiago_core/agents/_proxy/` that forward role-specific prompts to GPT-4/Claude/Copilot. Each proxy loads a role card from `knowledge/proxy-instructions/<role>.md`, exposes a minimal manifest (`status`, `plan`, `execute_scenario`), and queues requests through the NuSy Orchestrator. Shared guidance (captains journals, navigation charts) lives in repo, and all outputs land in ships-logs to establish provenance. Goal: operational fake team in <1 week.

### Phase 1: Factory Components (Built by Fake Team)

Fake PM proposes and prioritizes the factory, fake Architect designs Navigator/Catchfish/Fishnet, fake Developers implement them under `nusy_orchestrator/santiago_builder/`, and fake QA validates them with voyage-trials. Navigator orchestrates the "Old Man and the Sea" 10-step process. Catchfish ingests SAFe, XP, Lean Startup, and other sources, producing 4-layer Markdown+YAML packages plus a KG insert queue. Fishnet analyzes the KG to generate BDD scenarios and MCP manifests. Provenance tracking + queued writes prevent knowledge graph corruption. Phase completes with a full dress rehearsal: PDF → knowledge/catches/santiago-pm-safe-xp/ with >=95% BDD pass rate.

### Phase 2: First Catch & Replacement

Run a full fishing expedition targeting a blended Santiago-PM. Navigator enforces 3 validation cycles, Catchfish iterates until <15m per source, Fishnet emits BDDs and manifest, and the fake QA agent scores each cycle. Deploy the resulting MCP service under `santiago_core/agents/santiago-pm-safe-xp/service/`, spin it beside the fake proxy, and A/B test on 10 canonical PM tasks. If real ≥90% of fake on quality (and usually faster, cheaper), retire the fake PM proxy and route all PM requests to the new service. Store the catch (domain-knowledge/, bdd-tests/, manifest, provenance) in `knowledge/catches/`.

### Phase 3: Progressive Replacement

Repeat Phase 2 for Architect-NuSy, Architect-Systems, Developer, QA, UX, and Platform roles. Each replacement is run as a hypothesis-driven expedition with BDD coverage and A/B testing. Some proxies may remain (e.g., Ethicist) if sources lack depth; that is acceptable—the plan assumes hybrid teams with transparent metrics. DGX Spark hosts shared Mistral-7B-Instruct via vLLM batching so 10+ Santiagos can run concurrently while sharing one loaded model. Concurrency and session-isolation tests follow `nusy_manolin_multi_agent_test_plans.md`.

### Phase 4: Self-Sustaining

Once most fake roles are replaced, the real Santiagos form the permanent crew. Santiago-PM proposes improving Catchfish parallelization, Santiago-Architect implements queue-aware KG writes, Santiago-Developer updates the orchestrator, and Santiago-QA runs regression voyage-trials. Improvements are treated as fishing expeditions, logged in ships-logs, and validated through A/B deployments on DGX. The factory now generates new domain Santiagos (finance, legal, etc.) on demand and continuously reduces Catchfish cycle time below 15 minutes.

---

## Key Architectural Components

### Navigator

Implements the 10-step fishing process from `santiago-pm/strategic-charts/Old man and the sea.md`. It sequences gathering raw materials, Catchfish extraction, indexing, ontology loading, KG writes, Fishnet BDD generation, validation cycles, deployment, and learning loops. It enforces that each expedition runs 3-5 iterations until KPIs (≥95% BDD pass rate, provenance completeness) hold, and it records hypotheses/decisions in voyage-trials.

### Catchfish

The core converter that turns raw PDFs, APIs, and notes into the 4-layer structure proven in the clinical prototype. Layer 1 extracts raw text, Layer 2 identifies entities/relationships, Layer 3 writes Markdown+YAML packages, Layer 4 queues KG triples. Catchfish must track per-source timing (baseline 30-60m, target <15m) and maintain provenance (source hash, timestamp, fake/real agent id). It should support pluggable extractors (LLM summarization, deterministic parsing) so domains beyond PM can be ingested later.

### Fishnet

A BDD+manifest generator that inspects the KG and writes behavior tests plus MCP descriptors. It emits `.feature` files mapped to voyage-trials plus machine-readable manifest JSON describing available tools, levels (Apprentice/Journeyman/Master), and knowledge scope (Pond/Lake/Sea/Ocean). Fishnet also infers concurrency risks (e.g., if tool mutates KG) and contributes metadata for Ethics & Concurrency gating.

### Fake Team Proxies

Located under `santiago_core/agents/_proxy/`, each proxy MCP service reads its role instructions, forwards reasoning to GPT-4/Claude/Copilot, and returns structured responses. They expose metrics (latency, cost) so replacement benefits are measurable. They rely on shared memory in `knowledge/shared/` (team roster TTL, working agreements) per `fake_team_pack/` guidance.

### Knowledge Storage

Create `knowledge/` with:

- `catches/<santiago-name>/domain-knowledge/` (Layer 3 files)
- `catches/<santiago-name>/bdd-tests/`
- `catches/<santiago-name>/mcp-manifest.json`
- `catches/<santiago-name>/provenance.yaml`
- `templates/` for base catch structure
- `proxy-instructions/` for fake team role cards

Storage lives on DGX Spark's 4 TB NVMe, with overflow and historical catches on the external 8-16 TB NVMe RAID recommended by `dgx_spark_nusy_report.md`.

---

## MCP Integration

Every fake and real Santiago is an MCP service with:

- Auto-generated `mcp.json` from Fishnet summarizing tools (`provide_backlog_plan`, `design_kg_extension`, etc.), auth, and invocation semantics.
- Tooling that routes through NuSy Orchestrator for shared governance, logging, and Ethics gating.
- Manifest regeneration triggered whenever Fishnet updates tests or knowledge; Navigator invalidates older manifests automatically.
- A manifest registry in `knowledge/catches/index.yaml` so orchestrator knows which Santiagos are trustworthy (≥90% parity) and which are experimental.

---

## DGX Deployment

Per `ocean-research/building-on-DGX/dgx_spark_nusy_report.md` the DGX Spark provides 128 GB unified memory and 4 TB NVMe; add an 8-16 TB external NVMe RAID for model zoo and KG history. vLLM or TensorRT-LLM hosts Mistral-7B-Instruct once, exposing batched inference to all agents. Kubernetes is overkill initially; use systemd services or lightweight orchestration plus observability (Prometheus + Loki) for GPU/memory metrics. Storage tiers: hot (internal NVMe) for working catches and models, warm (external RAID) for historical catches and experiments, cold (NAS) for archives.

---

## Ethics & Concurrency Gating

Embed Ethics & Concurrency gating inside NuSy Orchestrator:

- Every tool call is queued with metadata (role, intent, knowledge references) and screened by the fake (later real) Santiago-Ethicist before execution.
- Concurrency guardrails follow `nusy_manolin_multi_agent_test_plans.md`: session isolation, tool locking, and load SLOs (P95 latency <6s under 10-agent load).
- All KG mutations run through a queued write pipeline with automated provenance stamping (agent id, timestamp, hypothesis reference) to prevent corruption. Ethics gating also verifies that fishing expeditions respect source licensing and usage constraints.

---

## References Cited

- `ocean-research/00-ARCHITECTURE-PATTERN.md`
- `santiago-pm/strategic-charts/Old man and the sea.md`
- `ocean-research/building-on-DGX/dgx_spark_nusy_report.md`
- `ocean-research/nusy_manolin_architecture.md`
- `ocean-research/nusy_manolin_multi_agent_test_plans.md`
- `ocean-research/fake_team_pack/fake_team_steps_for_hank_and_copilot.md`
- `nusy_prototype/neurosymbolic-clinical-reasoner-technical-summary.md`
- `santiago-pm/README.md`
