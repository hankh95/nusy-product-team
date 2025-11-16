# Santiago Factory Architecture Plan

**Prepared by:** Grok Code Fast 1  
**Date:** 2025-11-16  
**Version:** 3.0

---

## Executive Summary

Santiago is a self-bootstrapping AI factory that generates domain-specific Santiagos on demand. It starts with "fake" Santiagos (MCP proxies to external APIs like OpenAI, Claude, Copilot), uses them to build the factory infrastructure (Navigator, Catchfish, Fishnet), catches real Santiagos via knowledge extraction from sources (30-60m per source, 3-5 validation cycles), and progressively replaces fake team members via A/B testing (≥90% performance parity). The system achieves self-improvement as real Santiagos enhance the factory itself.

---

## Current Architecture

The current implementation resides in `santiago_core/`, with active development ongoing. Legacy prototypes exist in `src/nusy_pm_core/` and `santiago-code/`, archived for reference. The `knowledge/` directory is missing, which should store generated Santiagos and factory artifacts. Peripheral directories like `config/`, `notes/`, `backlog/`, `experiments/`, and `reports/` provide context but are not core to the factory.

---

## Target Architecture

### Phase 0: Fake Team (Contractor Proxies)

Deploy thin MCP wrappers proxying to external AI APIs (OpenAI GPT-4, Claude Opus, Copilot). These serve as temporary "contractors" to build the factory. Each fake Santiago (PM, Architect, Developer, QA, Ethicist, UX, Platform) implements minimal MCP endpoints that route requests to external models with role-specific instructions from `knowledge/proxy-instructions/`. This phase takes weeks 1-2, enabling rapid bootstrapping without custom AI development.

### Phase 1: Factory Components (Built by Fake Team)

The fake team, coordinated via MCP, implements the factory infrastructure:

- **Navigator**: Orchestrates the 10-step fishing process from "Old Man and the Sea" (vision → raw materials → Catchfish → indexing → ontology → KG → Fishnet → validation cycles → deployment → learning).
- **Catchfish**: Extracts structured 4-layer knowledge from sources (30-60m per source, optimized to <15m). Processes PDFs, docs, APIs into Markdown + YAML for KG integration.
- **Fishnet**: Generates BDD tests from the KG, infers MCP tool capabilities, and validates coverage.

Fake team writes BDD scenarios for factory behavior, implements Python code in `nusy_orchestrator/santiago_builder/`, and validates end-to-end (PDF → deployed MCP service). This phase spans weeks 3-6.

### Phase 2: First Catch & Replacement

Factory catches first real Santiago (e.g., santiago-pm-safe-xp) from SAFe/XP sources:

1. Navigator initiates fishing expedition.
2. Catchfish extracts knowledge (30-60m total).
3. Fishnet generates BDD tests (10-15 scenarios).
4. Navigator runs validation cycles (3-5 until ≥95% pass rate).
5. Deploy as MCP service in `knowledge/catches/santiago-pm-safe-xp/`.
6. A/B test: Fake vs. real Santiago-PM on 10 identical tasks.
7. If real ≥90% parity, replace proxy (reduces API costs by 1/7th).

### Phase 3: Progressive Replacement

Repeat Phase 2 for each role (Architect, Developer, QA, etc.), using hypothesis-driven experiments. Hybrid team during transition. Each replacement is a hypothesis: "Real Santiago-X matches or exceeds fake performance."

### Phase 4: Self-Sustaining

Real Santiagos propose factory improvements (e.g., parallelize Catchfish). Factory evolves autonomously, generating new domain Santiagos on demand.

---

## Key Architectural Components

### Navigator

Orchestrates the 10-step fishing process from "Old Man and the Sea":

1. Vision: Define Santiago needs (MCP services, behaviors).
2. Raw Materials: Collect sources (PDFs, APIs, experts).
3. Catchfish: Extract structured knowledge.
4. Indexing: Make knowledge referenceable.
5. Ontology: Apply conventions/schemas.
6. KG Building: Store in knowledge graph.
7. Fishnet: Generate BDD tests.
8. Validation: Run cycles until quality threshold.
9. Deployment: Generate MCP manifest, deploy service.
10. Learning: Improve process from logs/metrics.

Runs 3-5 validation cycles per catch.

### Catchfish

Extracts 4-layer knowledge from sources:

- Layer 1: Raw text extraction.
- Layer 2: Entity/relationship identification.
- Layer 3: Semantic structuring (Markdown + YAML).
- Layer 4: KG integration.

Target: 30-60m → <15m optimization. Proven viable in clinical prototype (30-60m per guideline, 3 cycles).

### Fishnet

Generates BDD tests from KG:

- Top-down: From guideline structure.
- Bottom-up: From content analysis.
- External: APIs like PubMed.
- Logic-derived: From decision pathways.

Validates KG and MCP services. In prototype, achieved 94.9% coverage, aiming for 100%.

### Fake Team Proxies

`santiago_core/agents/_proxy/` — Thin MCP services routing to external APIs. Instructions in `knowledge/proxy-instructions/`. Purpose: Build factory, get replaced.

### Knowledge Storage

`knowledge/catches/<santiago>/` with `domain-knowledge/`, `bdd-tests/`, `mcp-manifest.json`, `provenance.yaml`. Trust registry in `knowledge/catches/index.yaml`. Markdown + YAML initially, upgrade to JSON/vector.

---

## MCP Integration

Each Santiago as independent MCP service, auto-generated manifests. Fake team coordinates via MCP protocol. Real Santiagos discovered via registry. Orchestrator routes requests based on domain expertise.

---

## DGX Deployment

Shared Mistral-7B-Instruct instance on NVIDIA DGX Spark (128 GB RAM, 4 TB NVMe, expandable to 8-16 TB). vLLM/TensorRT-LLM for batching. Supports 10 concurrent agents via multiplexed requests. P95 latency <6s for 10 agents. Tiered storage: NVMe for active, NAS for archives.

---

## Ethics & Concurrency Gating

Pre-execution review by Santiago-Ethicist. Session isolation, tool locking for external effects. Evolutionary monitoring. Queued KG writes with schema validation and provenance.

---

## References Cited

- ocean-research/00-ARCHITECTURE-PATTERN.md
- santiago-pm/strategic-charts/Old man and the sea.md
- ocean-research/building-on-DGX/dgx_spark_nusy_report.md
- nusy_prototype/ (clinical prototype evidence: 30-60m, 3 cycles)
- santiago-pm/expeditions/, tackle/, voyage-trials/ (development patterns)