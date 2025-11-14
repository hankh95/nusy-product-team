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


def test_query_by_contributor(tmp_path: Path) -> None:
    manifest_path = tmp_path / "notes_manifest.json"
    manager = NotesManager(manifest_path=manifest_path)
    manager.add_note(
        title="Test Note 1",
        contributor="Alice",
        summary="First note",
        tags=["test"]
    )
    manager.add_note(
        title="Test Note 2",
        contributor="Bob",
        summary="Second note",
        tags=["test"]
    )
    manager.add_note(
        title="Test Note 3",
        contributor="Alice",
        summary="Third note",
        tags=["other"]
    )

    alice_notes = manager.query_notes_by_contributor("Alice")
    assert len(alice_notes) == 2
    assert all(note.contributor == "Alice" for note in alice_notes)


def test_query_by_tag(tmp_path: Path) -> None:
    manifest_path = tmp_path / "notes_manifest.json"
    manager = NotesManager(manifest_path=manifest_path)
    manager.add_note(
        title="Test Note 1",
        contributor="Alice",
        summary="First note",
        tags=["test"]
    )
    manager.add_note(
        title="Test Note 2",
        contributor="Bob",
        summary="Second note",
        tags=["test"]
    )
    manager.add_note(
        title="Test Note 3",
        contributor="Alice",
        summary="Third note",
        tags=["other"]
    )

    test_notes = manager.query_notes_by_tag("test")
    assert len(test_notes) == 2
    assert all("test" in note.tags for note in test_notes)