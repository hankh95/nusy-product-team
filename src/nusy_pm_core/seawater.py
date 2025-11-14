"""Seawater Module: Source-indexed L0 processing for notes."""

from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class NoteSource:
    """Represents a source document for notes."""
    path: Path
    content: str
    metadata: Dict[str, str]


class SeawaterProcessor:
    """Processes notes with source indexing and L0 generation."""

    def __init__(self, notes_dir: Path):
        self.notes_dir = notes_dir
        self.sources: List[NoteSource] = []

    def process_notes_directory(self) -> List[Dict]:
        """Process all notes in directory with source indexing."""
        l0_content = []
        for file_path in self.notes_dir.rglob("*.md"):
            if file_path.is_file():
                source = self._load_source(file_path)
                self.sources.append(source)
                l0 = self._generate_l0(source)
                l0_content.extend(l0)
        return l0_content

    def _load_source(self, file_path: Path) -> NoteSource:
        """Load a source file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        metadata = {
            'filename': file_path.name,
            'path': str(file_path),
            'size': str(file_path.stat().st_size)
        }
        return NoteSource(file_path, content, metadata)

    def _generate_l0(self, source: NoteSource) -> List[Dict]:
        """Generate L0 content from source."""
        # Simple parsing for markdown notes
        lines = source.content.split('\n')
        l0_items = []
        current_section = None
        current_content = []

        for line in lines:
            if line.startswith('#'):
                if current_section:
                    l0_items.append({
                        'type': 'section',
                        'title': current_section,
                        'content': '\n'.join(current_content),
                        'source': source.metadata
                    })
                current_section = line.lstrip('#').strip()
                current_content = []
            else:
                current_content.append(line)

        if current_section:
            l0_items.append({
                'type': 'section',
                'title': current_section,
                'content': '\n'.join(current_content),
                'source': source.metadata
            })

        return l0_items