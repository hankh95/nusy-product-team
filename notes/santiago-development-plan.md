# Santiago Mini-Project Development Plan

## Vision

Launch the first Santiago iteration as a lightweight, self-reflective PM/PM-AI hybrid that captures every decision in the NuSy knowledge graph, proves a closed-loop "catchfish + fishnet" workflow, and keeps humans in sync through concise `notes/santiago` entries.

## Goals

- Establish a Santiago-specific code home (`santiago-code/`) where experiments and connectors live.
- Keep a human-readable, chronological narrative in `notes/santiago/` that maps to KG nodes and artifacts.
- Build instrumentation that proves the Santiago graph can answer questions about its own plan, outcomes, and next steps.

## Milestones

1. **Land the scaffold** (Week 1) – Create folders, README updates, and baseline support docs (this step).
2. **Launch knowledge capture** (Week 2) – Add a first Santiago note describing the domain, mirror it into the KG, and verify Navigator can reference the note via UUID.
3. **Produce experimentation loop** (Week 3) – Implement BDD tests and code inside `santiago-code/`, run catchfish/fishnet loops, and log result metadata back into the KG.
4. **Reflect and iterate** (Week 4) – Execute a knowledge debrief, document lessons in `notes/santiago/`, and add a new issue for the next refactor.

## Deliverables

- `santiago-code/README.md` detailing folder structure and entrypoints.
- `notes/santiago` entries for each working session, linked to KG nodes or sprint outcomes.
- KG entries describing the plan, experiments, and lessons learned (reference schema TBD).
- A set of Copilot-friendly issues (see `/issues`) to keep automation progressing.

## Team & Roles

- **NuSy PM Agent**: Oversees instrumentation, ensures every note references a KG decision, and surfaces blockers.
- **Navigator**: Runs the catchfish/fishnet cycles, records timestamps, and stamps notes with system labels.
- **QA/Doc Agent**: Keeps `notes/santiago` readable and ensures README + plan stay up to date.

## Success Criteria

- Santiago notes are readable, linked to code, and cross-referenced in the KG.
- Copilot agents have a clear backlog (`issues/`) and can deliver tests or features without guessing.
- The graph can answer at least three questions about decisions made this week (who decided, what happened, what’s next).

## Dependencies

- NuSy knowledge graph schema for conversations (may reuse existing PM schema).
- `navigator` instrumentation capable of tagging actions with system labels (graph vs external).
- Access to the upcoming Santiago code components (to be created in `santiago-code/`).

## Risks & Mitigations

- **Risk**: Notes get stale because no one updates them after working sessions.
  **Mitigation**: Make `notes/santiago/README.md` the daily entry point and remind agents to add quick updates.
- **Risk**: KG nodes remain disconnected from notes.
  **Mitigation**: Use the plan's goal of linking each note to a reference ID (file path or KG URI).
