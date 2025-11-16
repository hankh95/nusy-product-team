# Architecture Redux — GPT-5 v2 (2025-11-16)

This is a plan-only artifact. It reflects a full-repo review and updates the target architecture, constraints, and migration priorities toward an MCP-based multi-agent system running on the Manolin/DGX stack with shared knowledge and evolution cycles.

## Goals

- Establish clear MCP service boundaries for each role (PM, Architect, Developer, QA, Platform, UX).
- Introduce a shared knowledge tree usable by humans and agents.
- Define orchestrator/service topology compatible with Manolin (DGX Spark) and local dev.
- Ensure concurrency safety and ethics gating at both agent and orchestrator layers.

## Current State Summary (From Full-Repo Read)

- Implementation centers on `src/nusy_pm_core` (FastAPI, Typer) and `santiago_core` (agents + framework).
- Multiple documentation silos: `santiago/`, `santiago_core/docs`, `notes/`, `santiago-pm/ships-logs`, `ocean-research/`.
- Knowledge artifacts exist but lack a canonical root `knowledge/` hierarchy.
- Prior architecture redux outputs exist under `ocean-arch-redux/` (keep for history; avoid biasing decisions).
- Manolin/DGX target is well-documented in `ocean-research/*`, but not codified in scripts or CI.

## Target Architecture (v2)

- Orchestrator: `nusy-orchestrator` (service) mediates tasks, policies, and evolution cycles.
- MCP Services (one per role): PM, Architect, Systems Architect, Developer, QA, Platform, UX.
  - Each exposes: capabilities manifest, tool contracts, knowledge scopes, and audit hooks.
- Shared Knowledge Tree: `knowledge/` at repo root, with domains and shared artifacts.
  - `knowledge/shared/`: roster.ttl, working-agreements.md, ships-log.md, evolution-cycles/*.
  - `knowledge/domains/<domain>/`: graphs (TTL), glossaries, playbooks, datasets, prompts.
- Ethics & Concurrency Gate:
  - Orchestrator middleware enforces rate limits, resource quotas, disallowed-actions, and multi-step approval.
  - Agent-level guardrails in each MCP service plus org-wide policy.
- Deployment Modes: local dev (uvicorn + lightweight storage) and DGX Manolin (Spark, vector store, vLLM backends).

## Interfaces

- Orchestrator API: Task submit, status, audit log, evolution cycle CRUD, knowledge search/query.
- MCP per Role: tool schema (typed), capability discovery, knowledge mounts, policy hooks.
- Knowledge Access: rdflib/TTL, vector search, and file-indexing with provenance metadata.

## Data and Knowledge

- Canonicalize TTL graphs under `knowledge/domains/core/graph.ttl` and add per-domain graphs.
- Introduce roster entries per person/agent, evolution cycles, and ships-log structure at `knowledge/shared/`.
- Embed content indexing (file + chunk metadata) for search across shared and domain knowledge.

## Security, Ethics, and Auditability

- Include policy-as-code for disallowed operations and escalation paths.
- Record every orchestrator action with rationale, tool calls, inputs/outputs, and approvals.
- Differential privacy and redaction for sensitive notes/logs (configurable).

## DGX/Manolin Considerations

- Containerized services; Spark for data ops; vLLM for model serving.
- Clear adapter boundary: local dev uses mocks or light backends; Manolin uses production adapters.
- CI artifacts validate both modes via feature flags.

## Risks and Mitigations

- Drift between `santiago_core` and `santiago/`: choose `santiago_core` as canonical; deprecate leftovers post-merge.
- Duplicate graphs/notes: consolidate into `knowledge/` with provenance.
- Over-broad agent permissions: default-deny policies; tool-level allowlists.
- Lint and TTL correctness: add CI checks for MD and Turtle.

## Success Criteria

- Clear MCP manifests for at least PM and Developer services.
- A working orchestrator with ethics/concurrency gates for basic flows.
- A populated root `knowledge/` with shared and at least one domain (core).
- DGX-compatible configs and a minimal provisioning runbook.
