# Issue: Link Santiago notes to the knowledge graph

- **Assignees:** Copilot agents and ATS connectors.

## Description

We need to ensure every Santiago note links to at least one KG node or artifact so Navigator can answer questions about why decisions were made.

## Tasks

- [ ] Identify the KG schema for conversations or experiments and add metadata fields (e.g., `source_note`, `decision_reference`).
- [ ] For the kickoff note from Issue 001, store a KG entry that references the note’s filename and key hypotheses.
- [ ] Document the linking pattern in both `notes/santiago/README.md` and `notes/santiago-development-plan.md` so future sessions follow the same ritual.
- [ ] Verify the Navigator instrumentation logs the KG ID whenever it records a decision from a Santiago note.
