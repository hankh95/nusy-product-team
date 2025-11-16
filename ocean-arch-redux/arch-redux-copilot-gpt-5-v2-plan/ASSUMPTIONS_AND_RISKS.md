# Assumptions & Risks — Copilot GPT-5 v2 (2025-11-16)

```text
**Metadata**
Model Name: copilot-gpt-5
Model Version: unknown
Date: 2025-11-16
Repo Commit SHA: 53a9fc4
Run ID: assumptions-copilot-gpt-5-2025-11-16-1
```text

## Assumptions
- A1: Root `knowledge/` tree creation precedes orchestrator/service regeneration.
- A2: MCP manifests (PM & Ethicist) drive consistent interface normalization across future role services.
- A3: Unified KG interaction layer will reduce write duplication and enable batch provenance.
- A4: DGX/Manolin cluster resources are eventually available; local mode must not block cluster adoption.
- A5: Ethics & Concurrency Gating middleware can be inserted without invasive refactors due to earlier archival of prototype runtime.
- A6: Fake-team mode continues to provide interim multi-agent simulation until MCP services are live.
- A7: Legacy documentation suffices to reconstruct required role capabilities without reading archived code.

## Risks
| ID | Risk | Impact | Likelihood | Mitigation |
| --- | --- | --- | --- | --- |
| R1 | Delay in knowledge consolidation | Schema drift & inconsistent queries | Medium | Enforce Milestone 1 acceptance criteria early |
| R2 | Over-engineering KG interaction layer | Slowed regeneration velocity | Medium | Define minimal interface + iterative enhancements |
| R3 | Ethics gating complexity overload | Developer friction & bypass attempts | Medium | Start with small allowlist + escalation path |
| R4 | Missing `santiago_core/` confuses responsibilities | Ambiguous ownership of core logic | High | Explicit orchestrator + services separation, mark GAP |
| R5 | DGX provisioning blockers | Deployment delay | Medium | Provide fallback local performance harness |
| R6 | Insufficient provenance fields | Weak audit trail & trust | Low | Mandate source_file, actor, timestamp, confidence |
| R7 | Citation drift in future planning runs | Reduced evaluation consistency | Medium | Standardize References Cited section template |

## Mitigation Details
- M1 (R1): Reject progressing to manifests until consolidation checklist passes.
- M2 (R3): Provide gating policy DSL with <10 starter rules; expand only after telemetry.
- M3 (R6): Provenance record includes hash of content segment to enable later integrity checks.
- M4 (R4): Add explicit GAP record in relevance map and migration milestone mapping table.

## Provenance & KG Strategy (Reducing Risk)
Queued, batched writes (interaction layer) attach provenance attributes: `source_file`, `line_span`, `extracted_at`, `actor_role`, `confidence_score`, `hash`. On flush, a batch provenance summary is stored in `provenance-log.ttl` referencing all newly inserted triples. This ensures reproducibility and strengthens audit/ethics review.

## Open Questions
- Q1: Should ontology versioning use semantic version (major.minor.patch) or timestamp-based tagging?
- Q2: Which vector store backend (pgvector vs Milvus) best aligns with DGX resource patterns?
- Q3: What threshold triggers mandatory Ethicist escalation (risk score > X or sensitive domain classification)?

### References Cited
- ocean-research/dgx_spark_nusy_report.md
- ocean-research/nusy_manolin_architecture.md
- ocean-research/nusy_manolin_provisioning_automation.md
- ocean-research/nusy_manolin_multi_agent_test_plans.md
- ocean-research/fake_team_feature_plan.md
- ocean-research/fake_team_steps_for_hank_and_copilot.md
