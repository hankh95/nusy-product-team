# Migration Steps — Copilot GPT-5 v2 (2025-11-16)

```text
**Metadata**
Model Name: copilot-gpt-5
Model Version: unknown
Date: 2025-11-16
Repo Commit SHA: 53a9fc4
Run ID: migration-copilot-gpt-5-2025-11-16-1
```text

Plan-only phase: No production code modifications; deliverables are scaffolds and specifications.

## Milestone 1: Knowledge Tree Initialization
Goals: Establish canonical root `knowledge/` structure and consolidate scattered graphs.
Affected Paths: (new) `knowledge/`, existing `notes/`, archived tag for legacy graphs.
Tasks:
- [ ] Create `knowledge/shared/` with `roster.ttl`, `working-agreements.md`, `ships-log.md`, `evolution-cycles/`.
- [ ] Create `knowledge/domains/core/graph.ttl` consolidating `notes/kg.ttl` + any legacy TTL (add provenance stubs).
- [ ] Add `knowledge/domains/core/glossary.md` with initial term list.
- [ ] Define provenance annotation pattern (named graph or reification guidelines).
- [ ] Draft ontology skeleton `knowledge/domains/core/ontology.ttl`.
Acceptance Criteria:
- [ ] Directory tree exists with required seed files.
- [ ] Provenance pattern documented.
- [ ] Glossary has at least 10 core terms.

## Milestone 2: Unified KG Interaction Layer Spec
Goals: Replace eager write prototype pattern with queued, validated, provenance-rich interface.
Affected Paths: `knowledge/` (spec docs), future runtime placeholder `orchestrator/`.
Tasks:
- [ ] Specify Python interface methods (queue_write, validate, flush, get_history).
- [ ] Define batching thresholds (size/time) and rollback semantics.
- [ ] Outline provenance metadata fields (source_file, timestamp, actor, confidence).
- [ ] Add event schema draft (JSON) for queued writes.
Acceptance Criteria:
- [ ] Interface spec documented.
- [ ] Event schema draft passes JSON lint.
- [ ] Provenance fields enumerated with rationale.

## Milestone 3: MCP Manifests (PM & Ethicist Priority)
Goals: Formalize role capabilities and initial tool contracts for PM and Ethicist services.
Affected Paths: `services/mcp-pm/`, `services/mcp-ethicist/` (plan docs only), `knowledge/shared/`.
Tasks:
- [ ] Draft `manifest.json` structure (name, version, capabilities, tools, knowledge_mounts, policies).
- [ ] Enumerate PM capabilities (story drafting, hypothesis linking, backlog annotation).
- [ ] Enumerate Ethicist capabilities (risk classification, approval workflow, policy evaluation).
- [ ] Define knowledge mounts for both services (shared roster, policies, ships-log).
- [ ] Provide example tool schema (input validation contract) per service.
Acceptance Criteria:
- [ ] Two manifest drafts present and lint-friendly.
- [ ] Capability lists cross-reference existing knowledge artifacts.
- [ ] Tool schema examples include required validation constraints.

## Milestone 4: Orchestrator & Ethics & Concurrency Gating Specification
Goals: Document orchestrator API and gating middleware contract.
Affected Paths: `orchestrator/` (spec only), `services/` (references), `ocean-research/` (citations).
Tasks:
- [ ] Define OpenAPI endpoints: tasks, evolution cycles, knowledge search, audit retrieval.
- [ ] Specify gating middleware hooks (before_tool_call, check_policy, record_decision).
- [ ] Map risk escalation flow referencing `ocean-research/nusy_manolin_multi_agent_test_plans.md`.
- [ ] Add concurrency control policy draft (quotas per role, rate limit rules).
Acceptance Criteria:
- [ ] OpenAPI draft includes all primary endpoints.
- [ ] Middleware hooks documented with input/output fields.
- [ ] Escalation path includes Ethicist approval step.

## Milestone 5: DGX/Manolin Deployment Readiness
Goals: Prepare cluster-mode adaptation plan.
Affected Paths: `deployment/` (plan docs), `ocean-research/` references.
Tasks:
- [ ] Outline container composition (orchestrator, role services, vector store, Spark gateway).
- [ ] Environment variable schema for cluster vs local mode.
- [ ] Staging vs production config separation plan.
- [ ] Snapshot/backup strategy for `knowledge/` on DGX.
Acceptance Criteria:
- [ ] Deployment plan doc lists all containers & dependencies.
- [ ] Env schema includes required secrets placeholders.
- [ ] Snapshot strategy enumerates frequency + retention.

## Milestone 6: Pilot Flow & Test Harness (Plan-Level)
Goals: Define initial cross-service workflow and validation approach.
Affected Paths: `features/` (new planning scenarios), `services/mcp-pm/`, `services/mcp-developer/`.
Tasks:
- [ ] Gherkin feature stub for PM → Developer task handoff with ethics gate.
- [ ] Concurrency test scenario referencing risk classification.
- [ ] Checklist for validating manifest integrity (fields present, mounts resolvable).
- [ ] Define metrics collection outline (latency, approval turnaround, queue depth).
Acceptance Criteria:
- [ ] At least one feature file stub documented.
- [ ] Metrics outline covers four key dimensions (performance, ethics, concurrency, knowledge coverage).
- [ ] Manifest integrity checklist complete.

## Milestone 7: Consolidation & Cleanup (Historical + Forward)
Goals: Finalize archival awareness & remove ambiguity for future regeneration.
Affected Paths: Archived tag contents (read-only), planning docs.
Tasks:
- [ ] Explicitly mark legacy references in any remaining docs.
- [ ] Map each planned path to future regeneration counterpart.
- [ ] Add deprecation notes for duplicate directories (`santiago/` vs `santiago-pm/`).
Acceptance Criteria:
- [ ] All legacy mentions annotated as historical.
- [ ] Regeneration mapping table published.

### References Cited
- ocean-research/dgx_spark_nusy_report.md
- ocean-research/nusy_manolin_architecture.md
- ocean-research/nusy_manolin_provisioning_automation.md
- ocean-research/nusy_manolin_multi_agent_test_plans.md
- ocean-research/fake_team_feature_plan.md
- ocean-research/fake_team_steps_for_hank_and_copilot.md
