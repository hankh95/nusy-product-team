from pathlib import Path

import pytest

from nusy_pm_core.notes import NotesManager


def test_add_note_and_persistence(tmp_path: Path) -> None:
    manifest_path = tmp_path / "notes_manifest.json"
    manager = NotesManager(manifest_path=manifest_path)
    note = manager.add_note(
        title="Initial Santiago Sync",
        contributor="Human - Hank",
        summary="Captured the kickoff decisions.",
        source_links=["notes/santiago-development-plan.md"],
        next_steps=["Run KG import"],
        tags=["santiago", "kickoff"],
    )

    assert note.title == "Initial Santiago Sync"
    assert note.tags == ["santiago", "kickoff"]

    # Reload manager to ensure persistence
    reloaded = NotesManager(manifest_path=manifest_path)
    notes = reloaded.list_notes()
    assert len(notes) == 1
    assert notes[0].id == note.id
    assert notes[0].summary == "Captured the kickoff decisions."


def test_link_requires_existing_note(tmp_path: Path) -> None:
    manager = NotesManager(manifest_path=tmp_path / "notes_manifest.json")
    with pytest.raises(ValueError):
        manager.link_to_graph(note_id="missing", kg_node_id="KG-001", rationale="no note yet")