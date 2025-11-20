# EXP-057: Architecture Redux 3 – Target Runtime & Repo Alignment

## Overview

This expedition implements the migration plan outlined in `docs-arch-redux-3/arch-migration-plan.md` to align the repository and runtime with the target architecture defined in `docs-arch-redux-3/arch-vision-merged-plan.md`.

**Goal:** Evolve the current repository into the Santiago target architecture, focusing on:

- Two-namespace model (`domain/*` vs `self-improvement/*`)
- Canonical self-improvement scaffold based on `santiago-pm/`
- Production vs experimental code separation
- Updated documentation and glossary

## Objectives

1. **Docs Alignment**: Update architecture docs to point to merged plan
2. **Folder Structure Updates**: Implement two-namespace model documentation
3. **Root Artifact Triage**: Generate and review triage report for root-level files
4. **Glossary Updates**: Extend GLOSSARY.md with new terms
5. **Kanban Setup**: Create epic and initial tasks
6. **Code Organization**: Mark experimental code and prepare production migrations

## Status

- [x] Expedition branch created
- [x] Initial README created
- [x] Root artifact triage report generated
- [x] Folder structure docs updated
- [x] Glossary extended
- [x] Kanban epic created
- [x] Questions list for Captain review

## Deliverables

- `triage-report.md`: Proposed homes for root-level artifacts
- Updated `santiago-pm/tackle/folder-structure.md`
- Extended `GLOSSARY.md`
- Kanban cards under `santiago-pm/cargo-manifests/`
- `docs-arch-redux-3/questions.md`: Questions for Captain review

## Approach

Following the migration plan's principles:

- Preserve history (archive, don't delete)
- Small, reviewed changes
- Non-destructive operations first
- Focus on documentation and planning before structural changes

## Timeline

- Phase 1 (This expedition): Planning and documentation updates
- Phase 2 (Future): Structural code moves and runtime changes
