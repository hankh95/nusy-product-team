# GPT-5 v3 Plan (Independent)

Date: 2025-11-16

This folder contains an independently authored v3 deliverable set for the NuSy architecture redux. It follows the v3 prompt requirements and references only canonical repo sources (patterns, DGX notes, clinical prototype evidence), not other model-labeled plan folders.

## Files

- `ARCHITECTURE_PLAN.md`: Phased architecture (0–4), Navigator/Catchfish/Fishnet definitions, MCP integration, DGX serving, ethics/concurrency, references.
- `MIGRATION_STEPS.md`: Milestones with tasks and acceptance criteria.
- `FOLDER_LAYOUT_PROPOSAL.md`: Proposed repo tree and mapping to components/pipelines.
- `RELEVANCE_MAP.md`: Relevant/peripheral/legacy/gaps across the repo.
- `ASSUMPTIONS_AND_RISKS.md`: Assumptions, risks, and provenance/queueing details.
- `ADDITIONAL_THOUGHTS.md`: Concise notes on architecture, DGX plan, provenance, independence, and next steps.

## Quick Review Checklist

- Navigator/Catchfish/Fishnet described with roles and interfaces.
- DGX-local shared model plan (vLLM/TensorRT-LLM) with targets and observability.
- Ethics gate, session isolation, tool locking, and queued KG writes with schema validation.
- Knowledge storage and trust registry structure defined.
- Independence: no content pulled from other model plan folders.
- References tied to canonical repo materials only.

## How To Use

- Start with `ARCHITECTURE_PLAN.md` for the big picture.
- Use `MIGRATION_STEPS.md` to plan execution by milestone.
- Align folder structure with `FOLDER_LAYOUT_PROPOSAL.md` before wiring pipelines.
- Validate scope and sources with `RELEVANCE_MAP.md`.
- Confirm safety/assumptions via `ASSUMPTIONS_AND_RISKS.md`.
- Keep `ADDITIONAL_THOUGHTS.md` for quick context and next actions.

## Independence Note

This GPT-5 v3 set is intentionally isolated from other model-specific plan folders to maintain clean comparative evaluation and provenance.
