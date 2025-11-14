from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
from uuid import uuid4
from rdflib import URIRef, Literal
from rdflib.namespace import RDFS

from .knowledge.graph import KnowledgeGraph, NUSY
from .models.kg import KGNode, KGRelation
from .navigator import Navigator

DEFAULT_MANIFEST = Path(__file__).resolve().parents[2] / "notes" / "notes_manifest.json"


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Note:
    id: str
    title: str
    contributor: str
    summary: str
    source_links: List[str]
    next_steps: List[str]
    tags: List[str]
    created_at: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "id": self.id,
            "title": self.title,
            "contributor": self.contributor,
            "summary": self.summary,
            "source_links": self.source_links,
            "next_steps": self.next_steps,
            "tags": self.tags,
            "created_at": self.created_at,
        }

    @staticmethod
    def from_dict(value: Dict[str, object]) -> "Note":
        return Note(
            id=str(value.get("id", "")),
            title=str(value.get("title", "")),
            contributor=str(value.get("contributor", "")),
            summary=str(value.get("summary", "")),
            source_links=list(value.get("source_links", [])),
            next_steps=list(value.get("next_steps", [])),
            tags=list(value.get("tags", [])),
            created_at=str(value.get("created_at", "")),
        )


@dataclass
class NoteLink:
    note_id: str
    kg_node_id: str
    rationale: str
    linked_at: str

    def to_dict(self) -> Dict[str, object]:
        return {
            "note_id": self.note_id,
            "kg_node_id": self.kg_node_id,
            "rationale": self.rationale,
            "linked_at": self.linked_at,
        }

    @staticmethod
    def from_dict(value: Dict[str, object]) -> "NoteLink":
        return NoteLink(
            note_id=str(value.get("note_id", "")),
            kg_node_id=str(value.get("kg_node_id", "")),
            rationale=str(value.get("rationale", "")),
            linked_at=str(value.get("linked_at", "")),
        )


class NotesManager:
    def __init__(self, manifest_path: Optional[Path] = None):
        self.manifest_path = Path(manifest_path or DEFAULT_MANIFEST)
        self.manifest_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.manifest_path.exists():
            self._write({"notes": [], "links": []})
        self._data = self._read()
        self.kg = KnowledgeGraph()

    def _read(self) -> Dict[str, List[Dict[str, object]]]:
        with open(self.manifest_path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def _write(self, payload: Dict[str, List[Dict[str, object]]]) -> None:
        with open(self.manifest_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)

    def _commit(self) -> None:
        self._write(self._data)

    def list_notes(self) -> List[Note]:
        return [Note.from_dict(item) for item in self._data.get("notes", [])]

    def find_note(self, note_id: str) -> Optional[Note]:
        for item in self._data.get("notes", []):
            if item.get("id") == note_id:
                return Note.from_dict(item)
        return None

    def add_note(
        self,
        title: str,
        contributor: str,
        summary: str,
        source_links: Optional[List[str]] = None,
        next_steps: Optional[List[str]] = None,
        tags: Optional[List[str]] = None,
    ) -> Note:
        note_id = uuid4().hex
        note = Note(
            id=note_id,
            title=title,
            contributor=contributor,
            summary=summary,
            source_links=source_links or [],
            next_steps=next_steps or [],
            tags=tags or [],
            created_at=iso_now(),
        )
        self._data.setdefault("notes", []).append(note.to_dict())
        self._commit()

        # Add to KG
        note_uri = URIRef(f"{NUSY}note/{note_id}")
        self.kg.add_node(KGNode(note_uri, title, NUSY.Note))
        self.kg.add_relation(KGRelation(note_uri, NUSY.contributor, Literal(contributor)))
        self.kg.add_relation(KGRelation(note_uri, NUSY.summary, Literal(summary)))
        self.kg.add_relation(KGRelation(note_uri, NUSY.created_at, Literal(note.created_at)))
        for tag in note.tags:
            self.kg.add_relation(KGRelation(note_uri, NUSY.hasTag, Literal(tag)))
        for link in note.source_links:
            self.kg.add_relation(KGRelation(note_uri, NUSY.sourceLink, Literal(link)))
        for step in note.next_steps:
            self.kg.add_relation(KGRelation(note_uri, NUSY.nextStep, Literal(step)))
        self.kg.save()

        return note

    def link_to_graph(self, note_id: str, kg_node_id: str, rationale: str) -> NoteLink:
        if not self.find_note(note_id):
            raise ValueError(f"Note `{note_id}` not found")
        link = NoteLink(
            note_id=note_id,
            kg_node_id=kg_node_id,
            rationale=rationale,
            linked_at=iso_now(),
        )
        self._data.setdefault("links", []).append(link.to_dict())
        self._commit()
        return link

    def get_note_links(self, note_id: str) -> List[NoteLink]:
        return [
            NoteLink.from_dict(item)
            for item in self._data.get("links", [])
            if item.get("note_id") == note_id
        ]

    def list_links(self) -> List[NoteLink]:
        return [NoteLink.from_dict(item) for item in self._data.get("links", [])]

    def neurosymbolic_query(self, question: str):
        """Query the KG using the NeurosymbolicClinicalReasoner."""
        return self.kg.neurosymbolic_query(question)

    def run_pipeline(self):
        """Run the complete Neurosymbolic pipeline."""
        notes_dir = self.manifest_path.parent
        navigator = Navigator(notes_dir, self.kg)
        return navigator.run_pipeline()

    def validate_coverage(self):
        """Validate pipeline coverage."""
        notes_dir = self.manifest_path.parent
        navigator = Navigator(notes_dir, self.kg)
        return navigator.validate_coverage()

    def query_notes_by_contributor(self, contributor: str) -> List[Note]:
        results = self.kg.query_notes_by_contributor(contributor)
        notes = []
        for row in results:
            note_id = str(row[0]).split('/')[-1]
            note = self.find_note(note_id)
            if note:
                notes.append(note)
        return notes

    def query_notes_by_tag(self, tag: str) -> List[Note]:
        results = self.kg.query_notes_by_tag(tag)
        notes = []
        for row in results:
            note_id = str(row[0]).split('/')[-1]
            note = self.find_note(note_id)
            if note:
                notes.append(note)
        return notes
