# 2025-11-20-hank-architecture-redux-3-knowledge-ops-planning

## Description

Architecture Redux 3 + KnowledgeOps planning and documentation.  
Consolidate Santiago/Noesis architecture into a single merged plan, define a migration plan, and introduce a KnowledgeOps (knowledge-as-code) pipeline that parallels CI/CD for code.

## Acceptance Criteria

- [ ] `docs-arch-redux-3/arch-vision-merged-plan.md` describes the target runtime, memory model, KnowledgeOps pipeline, and agent roles clearly.
- [ ] `docs-arch-redux-3/arch-migration-plan.md` captures folder mappings, root artifact triage, glossary upgrades, and Kanban reprioritization.
- [ ] Architecture Redux 3 and KnowledgeOps are represented as cargo manifests under `santiago-pm/cargo-manifests/`.
- [ ] Open questions and ambiguous artifacts (e.g., root-level features/expeditions/research logs) are documented for Captain review.

## Assignees

- Hank
- Santiago-PM (agents)

## Labels

- type:feature
- priority:high
- component:architecture
- component:santiago-core
- component:knowledge-ops

## Status

- [x] Open
- [ ] In-Progress
- [ ] Blocked
- [ ] Completed
- [ ] Cancelled

## Tasks

- [x] Create merged architecture doc (`arch-vision-merged-plan.md`).
- [x] Create migration plan doc (`arch-migration-plan.md`).
- [x] Add cargo manifests:
  - [x] `architecture-redux-3.feature`
  - [x] `knowledge-ops-pipeline.feature`
- [x] Create KnowledgeOps brain-dump stub (`knowledge-ops-brain-dump.md`).
- [ ] Generate root artifact triage report and proposed mappings.
- [ ] Align glossary and runtime terminology.
- [ ] Review and refine migration plan and features with Hank.

## Linked PRs

- [ ] PR #? (to be created) – Architecture Redux 3 & KnowledgeOps docs + features

## Comments

- Initial planning and documentation completed with copilot-gpt5 session on 2025-11-20.
- Future work will happen on a dedicated feature branch with small, reviewed PRs.

## Knowledge Graph Updates

- **New Relationships**:
  - (log → docs-arch-redux-3/arch-vision-merged-plan.md)
  - (log → docs-arch-redux-3/arch-migration-plan.md)
  - (log → santiago-pm/cargo-manifests/architecture-redux-3.feature)
  - (log → santiago-pm/cargo-manifests/knowledge-ops-pipeline.feature)
  - (log → santiago-pm/research-logs/knowledge-ops-brain-dump.md)
- **Updated Concepts**:
  - Noesis (ship runtime)
  - KnowledgeOps pipeline (ingest/validate/version/deploy)
- **Related Entities**:
  - Santiago-Core
  - Santiago-PM
  - Santiago-Ethicist


