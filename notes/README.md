# Notes Hub for Santiago

This folder collects human-facing and agent-friendly notes tied to the Santiago mini-project.

- `notes/santiago/` houses progressive write-ups, insights, and experiment retrospectives for the current Santiago version.
- Use these notes to capture hypotheses, blockers, or sync items before they move into the NuSy knowledge graph.
- Entries should link back to `santiago-code/` artifacts when they reference code, tests, or deployment scripts.

The NuSy Notes tool (`python -m src.nusy_pm_core.cli notes`) backs the manifest in `notes/notes_manifest.json`.
Run `notes create`, `notes list`, or `notes link` to keep the manifest in sync with human write-ups.
