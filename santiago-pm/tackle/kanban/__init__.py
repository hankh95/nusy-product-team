"""
Santiago PM Kanban Board System

A unified workflow tracking system that serves as the single source of truth
for all project work across the Santiago ecosystem.
"""

from .kanban_model import (
    UnifiedKanbanSystem,
    KanbanBoard,
    KanbanCard,
    ItemReference,
    ColumnType,
    ItemType,
    BoardType
)

from .kanban_service import KanbanService

from .kanban_cli import KanbanCLI

from .kanban_kg import KanbanKnowledgeGraph

__version__ = "1.0.0"

__all__ = [
    # Core models
    "UnifiedKanbanSystem",
    "KanbanBoard",
    "KanbanCard",
    "ItemReference",
    "ColumnType",
    "ItemType",
    "BoardType",

    # Service layer
    "KanbanService",

    # CLI interface
    "KanbanCLI",

    # Knowledge graph integration
    "KanbanKnowledgeGraph",

    # Version
    "__version__"
]