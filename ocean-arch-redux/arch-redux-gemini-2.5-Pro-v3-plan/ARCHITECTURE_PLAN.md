# Santiago Factory Architecture Plan

**Prepared by:** Gemini-2.5-Pro
**Date:** 2025-11-16
**Version:** 3.0

---

## Executive Summary

This plan reframes the Santiago project away from a static team of AI agents and toward its true purpose: a self-bootstrapping factory that generates domain-specific Santiagos on demand. The architecture follows a four-phase rollout, beginning with a "fake team" of MCP proxies to external APIs. This fake team's sole initial purpose is to build the core factory components: Navigator, Catchfish, and Fishnet.

Once the factory is operational, it will "catch" its first real Santiago—a Product Manager expert—by processing domain sources like SAFe and XP. This real agent will be A/B tested against its fake counterpart and, upon reaching ≥90% performance parity, will replace the proxy. This progressive replacement model will be applied to all roles, systematically reducing API costs and increasing institutional knowledge. Ultimately, the real Santiagos will become the permanent crew, responsible for maintaining and improving the factory itself, creating a self-sustaining and continuously improving system.

---

## Current Architecture

The current repository shows a project in transition. `santiago_core/` contains an active but incomplete implementation of the agent framework. Key factory components and the crucial `knowledge/` directory for storing generated agents ("catches") are missing. Legacy code exists in `src/nusy_pm_core/` and `santiago-code/`, serving as archaeological references but not as a foundation for future work. The vision is clearly articulated in `ocean-research/` and the development patterns in `santiago-pm/`, but the code has not yet implemented the full factory pattern. The DGX deployment is theoretical, and no MCP proxy layer for a fake team exists.

---

## Target Architecture

### Phase 0: Fake Team (Contractor Proxies)

The process begins by deploying a "fake team" composed of thin MCP services located in `santiago_core/agents/_proxy/`. Each service is a simple wrapper that forwards requests to powerful external APIs (like GPT-4, Claude, etc.), guided by role-specific instructions in `knowledge/proxy-instructions/`. This allows for the rapid establishment of a functional team capable of complex, coordinated tasks, providing the workforce needed to build the factory.

### Phase 1: Factory Components (Built by Fake Team)

The fake team's first and primary project is to build the Santiago factory itself within `nusy_orchestrator/santiago_builder/`. Following the development patterns in `santiago-pm/`, they will implement:

- **Navigator:** To orchestrate the 10-step "fishing" process from `"Old man and the sea.md"`.
- **Catchfish:** To extract structured, 4-layer knowledge from raw source documents.
- **Fishnet:** To generate BDD tests and MCP manifests from the resulting knowledge graph.
 
This phase includes building robust provenance tracking and a queued-write pipeline to ensure KG integrity.

### Phase 2: First Catch & Replacement

With the factory built, the first "fishing expedition" is launched to catch a real Santiago-PM. The factory will process sources like the SAFe framework and XP methodologies. Navigator will enforce 3-5 validation cycles until the generated agent achieves a high-quality score (e.g., ≥95% BDD pass rate). The resulting `santiago-pm-safe-xp` agent is then deployed and A/B tested against the fake PM proxy. If it meets or exceeds 90% performance parity, the proxy is retired, and all PM tasks are routed to the new, real agent.

### Phase 3: Progressive Replacement

The successful pattern from Phase 2 is repeated for all other roles: Architect, Developer, QA, UX, and Platform. Each replacement is treated as a scientific experiment, with clear hypotheses, BDD-driven validation, and A/B testing. This iterative approach allows for a gradual, controlled transition from a fully fake team to a hybrid one, and eventually to a fully real team, with decisions at each step backed by performance data.

### Phase 4: Self-Sustaining

Once a critical mass of real Santiagos is active, the system becomes self-sustaining. The real Santiago-PM will propose improvements to the factory itself (e.g., "Hypothesis: We can reduce Catchfish time to <15 minutes by parallelizing extraction"). The real Architect and Developer will design and implement these changes. The factory, now maintained and enhanced by its own creations, can produce new domain experts on demand while continuously improving its own efficiency.

---

## Key Architectural Components

### Navigator

The Navigator is the master orchestrator of the factory. It implements the 10-step fishing process outlined in `santiago-pm/strategic-charts/Old man and the sea.md`. It manages the entire lifecycle of a catch, from source collection to final deployment, and critically, enforces the 3-5 validation cycles required to ensure the quality of the generated Santiago.

### Catchfish

Catchfish is the heart of the knowledge extraction pipeline. It ingests raw source materials (PDFs, docs, APIs) and transforms them into the structured 4-layer knowledge model proven in the clinical prototype. Its primary performance metric is extraction time, with an initial baseline of 30-60 minutes per source and a target for optimization to under 15 minutes.

### Fishnet

Fishnet is the quality and integration engine. After Catchfish structures the knowledge and populates a knowledge graph, Fishnet inspects the KG to automatically generate BDD tests (`.feature` files) that validate the agent's behavior. It also generates the `mcp-manifest.json` file, which defines the tools and capabilities of the newly caught Santiago.

### Fake Team Proxies

Located in `santiago_core/agents/_proxy/`, these are lightweight MCP services that route requests to external LLMs. They are configured with role-specific instructions and are designed to be easily replaced by real, factory-generated Santiagos once the A/B tests pass.

### Knowledge Storage

The `knowledge/` directory is the factory's warehouse. All generated assets are stored here, primarily within `knowledge/catches/`. Each catch is a self-contained package including the extracted `domain-knowledge/`, the `bdd-tests/`, the `mcp-manifest.json`, and a `provenance.yaml` file that logs the entire fishing expedition for auditability.

---

## MCP Integration

Every Santiago, whether fake or real, is an independent MCP service. This ensures a consistent interface for the NuSy Orchestrator. Manifests for fake proxies are handwritten, but manifests for real Santiagos are auto-generated by Fishnet. The orchestrator uses a manifest registry (`knowledge/catches/index.yaml`) to discover available Santiagos and their capabilities, enabling dynamic routing and coordination.

---

## DGX Deployment

The target deployment environment is the DGX Spark system, as detailed in `ocean-research/building-on-DGX/dgx_spark_nusy_report.md`. A shared instance of a model like Mistral-7B-Instruct will be hosted using vLLM or TensorRT-LLM for efficient, batched inference. This allows numerous real Santiagos to operate concurrently while sharing a single, powerful base model, minimizing resource overhead.

---

## Ethics & Concurrency Gating

To ensure safe and reliable operation, all tool calls from any Santiago are funneled through the NuSy Orchestrator. This central point of control implements:

- **Ethics Gating:** A pre-execution review by a dedicated Santiago-Ethicist (initially fake, later real) to screen for policy violations.
- **Concurrency Gating:** Following the patterns in `nusy_manolin_multi_agent_test_plans.md`, the system will use a queued-write pipeline for all KG mutations, session isolation, and tool locking to prevent race conditions and data corruption.

---

## References Cited

- `ocean-research/00-ARCHITECTURE-PATTERN.md`
- `santiago-pm/strategic-charts/Old man and the sea.md`
- `ocean-research/building-on-DGX/dgx_spark_nusy_report.md`
- `nusy_prototype/` (as evidence for 30-60m extraction and 3-cycle validation)
- `santiago-pm/expeditions/`, `tackle/`, `voyage-trials/` (as development patterns for the fake team)
- `ocean-research/nusy_manolin_multi_agent_test_plans.md`
