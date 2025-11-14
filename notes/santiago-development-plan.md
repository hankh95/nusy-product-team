# Santiago Mini-Project Development Plan

## Vision

Launch the first Santiago iteration as a lightweight, self-reflective PM/PM-AI hybrid that captures every decision in the NuSy knowledge graph, proves a closed-loop "catchfish + fishnet" workflow, and keeps humans in sync through concise `notes/santiago` entries.

## Goals

- Establish a Santiago-specific code home (`santiago-code/`) where experiments and connectors live.
- Keep a human-readable, chronological narrative in `notes/santiago/` that maps to KG nodes and artifacts.
- Build instrumentation that proves the Santiago graph can answer questions about its own plan, outcomes, and next steps.
- Capture how humans and agents actually use notes, tasks, and chats so Santiago can infer the project rhythm (see "Team note practices" below).
- Maintain the `notes/notes_manifest.json` file using the NuSy Notes CLI so every narrative entry stays queryable.

## Milestones

1. **Land the scaffold** (Week 1) – Create folders, README updates, and baseline support docs (this step). ✅ COMPLETED
2. **Launch knowledge capture** (Week 2) – Add a first Santiago note describing the domain, mirror it into the KG, and verify Navigator can reference the note via UUID. ✅ COMPLETED
3. **Produce experimentation loop** (Week 3) – Implement BDD tests and code inside `santiago-code/`, run catchfish/fishnet loops, and log result metadata back into the KG. ✅ COMPLETED
4. **Build web interface** (Week 4) – Create interactive web interface for querying NuSy about ingested notes, following development practices. ✅ COMPLETED
5. **Reflect and iterate** (Week 5) – Execute a knowledge debrief, document lessons in `notes/santiago/`, and add a new issue for the next refactor.
6. **Conversation capture prep** (Future step) – Design adapters that ingest Slack/Matrix chats, issue comments, and Navigator-agent transcripts into the KG so Santiago records every human/AI conversation.

## Deliverables

- `santiago-code/README.md` detailing folder structure and entrypoints. ✅ COMPLETED
- `notes/santiago` entries for each working session, linked to KG nodes or sprint outcomes. ✅ COMPLETED
- KG entries describing the plan, experiments, and lessons learned (reference schema TBD). ✅ COMPLETED
- Interactive web interface (`nusy_query_interface.html`) for querying NuSy about ingested notes. ✅ COMPLETED
- FastAPI endpoints for natural language queries, SPARQL, and pipeline operations. ✅ COMPLETED
- A set of Copilot-friendly issues (see `/issues`) to keep automation progressing.

## Team & Roles

- **NuSy PM Agent**: Oversees instrumentation, ensures every note references a KG decision, and surfaces blockers.
- **Navigator**: Runs the catchfish/fishnet cycles, records timestamps, and stamps notes with system labels.
- **QA/Doc Agent**: Keeps `notes/santiago` readable and ensures README + plan stay up to date.

## Success Criteria

- Santiago notes are readable, linked to code, and cross-referenced in the KG. ✅ ACHIEVED
- Copilot agents have a clear backlog (`issues/`) and can deliver tests or features without guessing. ✅ ACHIEVED
- The graph can answer at least three questions about decisions made this week (who decided, what happened, what's next). ✅ EXCEEDED - Can answer many more questions via web interface
- Interactive web interface allows natural language queries about ingested notes. ✅ ACHIEVED
- Full Neurosymbolic pipeline (Seawater → CatchFish → FishNet → Navigator) implemented and working. ✅ ACHIEVED

## Dependencies

- NuSy knowledge graph schema for conversations (may reuse existing PM schema).
- `navigator` instrumentation capable of tagging actions with system labels (graph vs external).
- Access to the upcoming Santiago code components (to be created in `santiago-code/`).
- Chat ingestion adapters (Slack/Matrix/MCP logs) to capture conversation histories as graph edges.

## Team note practices

- Humans capture what they did for each issue and call out modified files, completed features, experiments run, and blockers.
- Agents mirror those summaries into Santiago notes, linking them to knowledge graph decisions and artifact URLs.
- Use `notes create --tag issue` when working on `issues/` so the note knows which issue is being resolved and can record contributions.

## Future architecture updates

- Nikolay (Santiago) will treat each note as a graph event (feature completed, file modified, decision published) with timestamps and responsible agents, enabling question-driven queries such as "who completed feature X" or "which files changed just before release."
- The graph should ingest chats/issues/traces later so narratives about blockers or decisions become queryable; this will eventually allow the PM AI to learn from the entire dialogue history.

## Risks & Mitigations

- **Risk**: Notes get stale because no one updates them after working sessions.
  **Mitigation**: Make `notes/santiago/README.md` the daily entry point and remind agents to add quick updates.
- **Risk**: KG nodes remain disconnected from notes.
  **Mitigation**: Use the plan's goal of linking each note to a reference ID (file path or KG URI).
