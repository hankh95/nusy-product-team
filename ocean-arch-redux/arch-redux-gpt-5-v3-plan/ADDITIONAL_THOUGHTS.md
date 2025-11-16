# Additional Thoughts — GPT-5 v3

Date: 2025-11-16

## Architectural Perspective

- Semi-autonomous NuSy team: Navigator (10-step orchestration), Catchfish (4-layer extraction with provenance), Fishnet (BDD + MCP manifest generation) working as a self-improving factory.
- Self-improvement loop: BDD gaps → MCP manifests → targeted “catches” → provenance + trust registry → upgraded Santiagos; closes the learning loop with measurable deltas.
- Concurrency + safety: session isolation, tool locking, ethics gate before external effects, and queued KG writes with schema validation.


## DGX-Local Model Plan

- Serving stack: vLLM or TensorRT-LLM with continuous batching; one shared 7–8B instruction model to keep latency predictable.
- Targets: P95 < 6s for 10 concurrent agents; cost-controlled via shared host inference.
- Observability: Prometheus + Loki; track prompts/sec, batch efficiency, error rates, and tail latency.
- Guardrails: per-agent rate limits, token budgets, tool caps, and explicit allowlists.


## Knowledge + Provenance

- Storage: `knowledge/catches/<santiago>/` with `domain-knowledge/`, `bdd-tests/`, `mcp-manifest.json`, `provenance.yaml`.
- Trust registry: `knowledge/catches/index.yaml` summarizing approvals, schema versions, and integration status.
- Provenance fields: prompt, context, tools, constraints, reviewers/approvals, hashes of artifacts, and timestamps.
- Writes: enqueue KG updates; apply schema validation and provenance checks before merging.


## Independence Guarantees

- This GPT-5 v3 set is authored independently of other model folders. References align only to canonical repo sources (patterns, DGX notes, clinical prototype evidence), not to other plan directories.


## Next Steps

- Optional: add a short README index for the v3 set.
- Run a light self-check vs the v3 checklist; tidy lint (blank lines; EOF newline).
- Pilot DGX inference; record baseline P50/P95 latency and batch efficiency under a 10-agent load.

