# Chore: Update CONTRIBUTING.md for Personal & Ships Logs

## Summary

Ensure `CONTRIBUTING.md` explicitly references the use of **personal logs** and **ships logs** as part of completing work, so humans and agents consistently update these logs when finishing features, fixing issues, or performing architectural work.

## Context

- `santiago-pm/personal-logs/README.md` defines how personal logs are used for session work logs and context restoration.
- `santiago-pm/ships-logs/README.md` defines how ships logs are used for issues/tasks/work items at the team level.
- Recent Architecture Redux 3 and KnowledgeOps work added:
  - New personal and ships logs for Santiago-Ethicist and Santiago-PM.
  - New architecture and migration docs under `docs-arch-redux-3/`.

Currently, `CONTRIBUTING.md` does not explicitly remind contributors (human or agent) to:

- Create/update personal logs when completing significant work sessions.
- Create/update ships logs for new issues/tasks/architecture or migration work.

## Tasks

- [ ] Review `CONTRIBUTING.md` and identify appropriate sections to reference:
  - `santiago-pm/personal-logs/README.md`
  - `santiago-pm/ships-logs/README.md`
- [ ] Add a short subsection under **Development Workflow** or **Development Practices** that:
  - Instructs contributors to update personal logs after significant work sessions.
  - Instructs contributors to create/update ships logs for team-visible issues/tasks.
  - Links to the two README files for details.
- [ ] Optionally add a brief note under **Development Workflow Summary**:
  - E.g., “After tests pass and before/with PR creation, update personal/ships logs as appropriate.”
- [ ] Run markdown linting / CI to ensure `CONTRIBUTING.md` remains clean.

## Type

- Documentation / Code Quality (process clarity)

## Acceptance Criteria

- [ ] `CONTRIBUTING.md` mentions personal logs and ships logs as part of the standard workflow.
- [ ] References to `santiago-pm/personal-logs/README.md` and `santiago-pm/ships-logs/README.md` are present and correct.
- [ ] CI/markdown lint passes after the change.


