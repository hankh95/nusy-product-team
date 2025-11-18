#!/usr/bin/env python3
"""
Unified Kanban Board System - Single Source of Truth for Workflow Management

This system provides a hierarchical Kanban board implementation that references
work items in the knowledge graph/git repository rather than duplicating data.
"""

import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict, field
from enum import Enum


class ColumnType(Enum):
    """Standard Kanban column types"""
    BACKLOG = "backlog"
    READY = "ready"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"


class BoardType(Enum):
    """Board hierarchy types"""
    MASTER = "master"  # Overall boat board
    AGENT = "agent"    # Individual Santiago sub-board


class ItemType(Enum):
    """Types of items that can be referenced on the board"""
    EXPEDITION = "expedition"
    FEATURE = "feature"
    TASK = "task"
    RESEARCH_LOG = "research_log"
    BUG = "bug"


@dataclass
class ItemReference:
    """Reference to a work item in the repository"""
    item_id: str  # Unique identifier (e.g., "EXP-042", "feature-memory-snapshot")
    item_type: ItemType
    repository_path: str  # Path to the item in git/KG
    title: str  # Display title
    description: str = ""  # Brief description
    priority: str = "medium"  # high, medium, low
    assignee: Optional[str] = None  # Santiago agent or human
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class KanbanCard:
    """A card on the Kanban board (references an item)"""
    card_id: str
    item_reference: ItemReference
    column: ColumnType
    position: int = 0  # Position within column (for ordering)
    notes: List[str] = field(default_factory=list)  # Card-specific notes
    blocked_reason: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    moved_at: datetime = field(default_factory=datetime.now)


@dataclass
class KanbanColumn:
    """A column on the Kanban board"""
    column_type: ColumnType
    title: str
    cards: List[KanbanCard] = field(default_factory=list)
    wip_limit: Optional[int] = None  # Work in progress limit


@dataclass
class KanbanBoard:
    """A Kanban board with columns and cards"""
    board_id: str
    board_type: BoardType
    name: str
    description: str = ""
    columns: Dict[str, KanbanColumn] = field(default_factory=dict)
    parent_board_id: Optional[str] = None  # For hierarchical boards
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        # Initialize standard columns if not provided
        if not self.columns:
            self._initialize_standard_columns()

    def _initialize_standard_columns(self):
        """Create standard Kanban columns"""
        for col_type in ColumnType:
            column = KanbanColumn(
                column_type=col_type,
                title=col_type.value.replace('_', ' ').title()
            )
            self.columns[col_type.value] = column


class UnifiedKanbanSystem:
    """
    Unified Kanban Board System for Santiago-PM

    Provides hierarchical boards with linked references to work items,
    eliminating duplication while maintaining a single source of truth.
    """

    def __init__(self, storage_path: str = ".kanban_boards", auto_init: bool = True):
        """
        Initialize the Kanban system.

        Args:
            storage_path: Path to store board data
            auto_init: Automatically create storage directory
        """
        self.storage_path = Path(storage_path)
        self.boards: Dict[str, KanbanBoard] = {}
        self.master_board_id = "master_board"

        if auto_init and not self.storage_path.exists():
            self.storage_path.mkdir(parents=True, exist_ok=True)

        self._load_boards()

        # Ensure master board exists
        if self.master_board_id not in self.boards:
            self.create_board(
                board_id=self.master_board_id,
                board_type=BoardType.MASTER,
                name="Master Boat Board",
                description="Unified workflow tracking for the entire Santiago ecosystem"
            )

    def create_board(self,
                    board_id: str,
                    board_type: BoardType,
                    name: str,
                    description: str = "",
                    parent_board_id: Optional[str] = None) -> str:
        """
        Create a new Kanban board.

        Args:
            board_id: Unique identifier for the board
            board_type: Type of board (master or agent)
            name: Display name
            description: Board description
            parent_board_id: Parent board for hierarchical relationships

        Returns:
            Board ID
        """
        if board_id in self.boards:
            raise ValueError(f"Board {board_id} already exists")

        board = KanbanBoard(
            board_id=board_id,
            board_type=board_type,
            name=name,
            description=description,
            parent_board_id=parent_board_id
        )

        self.boards[board_id] = board
        self._save_boards()

        return board_id

    def add_card_from_item(self,
                          board_id: str,
                          item_reference: ItemReference,
                          initial_column: ColumnType = ColumnType.BACKLOG) -> str:
        """
        Add a card to a board by referencing an existing item.

        Args:
            board_id: Board to add card to
            item_reference: Reference to the work item
            initial_column: Initial column placement

        Returns:
            Card ID
        """
        if board_id not in self.boards:
            raise ValueError(f"Board {board_id} not found")

        board = self.boards[board_id]
        column_key = initial_column.value

        if column_key not in board.columns:
            raise ValueError(f"Column {initial_column.value} not found in board")

        # Generate card ID
        card_id = f"card_{item_reference.item_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Create card
        card = KanbanCard(
            card_id=card_id,
            item_reference=item_reference,
            column=initial_column,
            position=len(board.columns[column_key].cards)  # Add to end
        )

        # Add to column
        board.columns[column_key].cards.append(card)
        board.updated_at = datetime.now()

        self._save_boards()
        return card_id

    def move_card(self,
                 board_id: str,
                 card_id: str,
                 new_column: ColumnType,
                 new_position: int = 0,
                 notes: Optional[str] = None) -> bool:
        """
        Move a card to a different column and position.

        Args:
            board_id: Board containing the card
            card_id: Card to move
            new_column: Target column
            new_position: Position within the column
            notes: Optional notes about the move

        Returns:
            Success status
        """
        if board_id not in self.boards:
            return False

        board = self.boards[board_id]
        card = None
        old_column = None

        # Find the card and its current column
        for col_key, column in board.columns.items():
            for c in column.cards:
                if c.card_id == card_id:
                    card = c
                    old_column = col_key
                    break
            if card:
                break

        if not card or old_column is None:
            return False

        # Check WIP limits
        new_col_key = new_column.value
        if new_col_key in board.columns:
            wip_limit = board.columns[new_col_key].wip_limit
            if wip_limit and len(board.columns[new_col_key].cards) >= wip_limit:
                return False  # WIP limit exceeded

        # Remove from old column
        board.columns[old_column].cards.remove(card)

        # Update card
        card.column = new_column
        card.position = new_position
        card.moved_at = datetime.now()
        if notes:
            card.notes.append(f"{datetime.now().isoformat()}: {notes}")

        # Add to new column at specified position
        target_column = board.columns[new_col_key]
        target_column.cards.insert(min(new_position, len(target_column.cards)), card)

        # Reorder positions
        for i, c in enumerate(target_column.cards):
            c.position = i

        board.updated_at = datetime.now()
        self._save_boards()

        # Update the referenced item's state
        self._update_item_state(card.item_reference, new_column)

        return True

    def _update_item_state(self, item_ref: ItemReference, new_column: ColumnType):
        """
        Update the state of the referenced item.

        This would integrate with the knowledge graph/git system to update
        the actual item's status.
        """
        # Placeholder for KG/git integration
        # In a real implementation, this would update the item's metadata
        # based on the column transition
        state_mapping = {
            ColumnType.BACKLOG: "backlog",
            ColumnType.READY: "ready",
            ColumnType.IN_PROGRESS: "in_progress",
            ColumnType.REVIEW: "review",
            ColumnType.DONE: "completed"
        }

        new_state = state_mapping.get(new_column, "unknown")
        print(f"Updating item {item_ref.item_id} state to: {new_state}")

        # TODO: Integrate with actual KG/git system to update item metadata

    def get_board_summary(self, board_id: str) -> Dict[str, Any]:
        """Get a summary of a board's current state"""
        if board_id not in self.boards:
            return {"error": "Board not found"}

        board = self.boards[board_id]
        summary = {
            "board_id": board.board_id,
            "name": board.name,
            "type": board.board_type.value,
            "columns": {}
        }

        for col_key, column in board.columns.items():
            summary["columns"][col_key] = {
                "title": column.title,
                "card_count": len(column.cards),
                "wip_limit": column.wip_limit,
                "cards": [
                    {
                        "card_id": card.card_id,
                        "title": card.item_reference.title,
                        "item_type": card.item_reference.item_type.value,
                        "assignee": card.item_reference.assignee,
                        "priority": card.item_reference.priority
                    }
                    for card in column.cards
                ]
            }

        return summary

    def search_cards(self,
                    board_id: str,
                    query: str = "",
                    item_type: Optional[ItemType] = None,
                    assignee: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Search for cards on a board.

        Args:
            board_id: Board to search
            query: Text search in title/description
            item_type: Filter by item type
            assignee: Filter by assignee

        Returns:
            List of matching cards
        """
        if board_id not in self.boards:
            return []

        board = self.boards[board_id]
        results = []

        for column in board.columns.values():
            for card in column.cards:
                item_ref = card.item_reference

                # Apply filters
                if item_type and item_ref.item_type != item_type:
                    continue
                if assignee and item_ref.assignee != assignee:
                    continue
                if query:
                    search_text = f"{item_ref.title} {item_ref.description}".lower()
                    if query.lower() not in search_text:
                        continue

                results.append({
                    "card_id": card.card_id,
                    "column": card.column.value,
                    "title": item_ref.title,
                    "item_type": item_ref.item_type.value,
                    "assignee": item_ref.assignee,
                    "priority": item_ref.priority
                })

        return results

    def _load_boards(self):
        """Load boards from storage"""
        boards_file = self.storage_path / "boards.json"
        if boards_file.exists():
            try:
                with open(boards_file, 'r') as f:
                    data = json.load(f)

                for board_data in data.values():
                    # Convert timestamps
                    board_data['created_at'] = datetime.fromisoformat(board_data['created_at'])
                    board_data['updated_at'] = datetime.fromisoformat(board_data['updated_at'])

                    # Convert board type
                    board_data['board_type'] = BoardType(board_data['board_type'])

                    # Convert columns and cards
                    for col_key, col_data in board_data.get('columns', {}).items():
                        for card_data in col_data.get('cards', []):
                            # Convert item reference
                            item_ref_data = card_data['item_reference']
                            item_ref_data['created_at'] = datetime.fromisoformat(item_ref_data['created_at'])
                            item_ref_data['updated_at'] = datetime.fromisoformat(item_ref_data['updated_at'])
                            item_ref_data['item_type'] = ItemType(item_ref_data['item_type'])

                            card_data['item_reference'] = ItemReference(**item_ref_data)

                            # Convert card timestamps
                            card_data['created_at'] = datetime.fromisoformat(card_data['created_at'])
                            card_data['moved_at'] = datetime.fromisoformat(card_data['moved_at'])
                            card_data['column'] = ColumnType(card_data['column'])

                            # Reconstruct card
                            card = KanbanCard(**card_data)
                            col_data['cards'] = [card for card_data in col_data['cards']]

                        # Reconstruct column
                        col_data['column_type'] = ColumnType(col_key)
                        board_data['columns'][col_key] = KanbanColumn(**col_data)

                    board = KanbanBoard(**board_data)
                    self.boards[board.board_id] = board

            except Exception as e:
                print(f"Warning: Could not load boards: {e}")

    def _save_boards(self):
        """Save boards to storage"""
        boards_file = self.storage_path / "boards.json"
        try:
            data = {}
            for board_id, board in self.boards.items():
                board_dict = asdict(board)
                # Convert datetime objects
                board_dict['created_at'] = board.created_at.isoformat()
                board_dict['updated_at'] = board.updated_at.isoformat()

                # Convert board type enum
                board_dict['board_type'] = board_dict['board_type'].value

                # Convert nested objects
                for col_key, column in board_dict.get('columns', {}).items():
                    # Convert column type
                    column['column_type'] = column['column_type'].value
                    for card in column.get('cards', []):
                        card['created_at'] = card['created_at'].isoformat()
                        card['moved_at'] = card['moved_at'].isoformat()
                        card['column'] = card['column'].value
                        card['item_reference']['created_at'] = card['item_reference']['created_at'].isoformat()
                        card['item_reference']['updated_at'] = card['item_reference']['updated_at'].isoformat()
                        card['item_reference']['item_type'] = card['item_reference']['item_type'].value

                data[board_id] = board_dict

            with open(boards_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save boards: {e}")


# Convenience functions
def create_master_board() -> UnifiedKanbanSystem:
    """Create and return the master Kanban system"""
    return UnifiedKanbanSystem()


def add_expedition_to_board(kanban: UnifiedKanbanSystem,
                           board_id: str,
                           expedition_id: str,
                           title: str,
                           description: str = "",
                           priority: str = "medium") -> str:
    """Convenience function to add an expedition to a board"""
    item_ref = ItemReference(
        item_id=expedition_id,
        item_type=ItemType.EXPEDITION,
        repository_path=f"research-logs/{expedition_id.lower().replace('-', '_')}.md",
        title=title,
        description=description,
        priority=priority
    )

    return kanban.add_card_from_item(board_id, item_ref)


if __name__ == "__main__":
    # Demo usage
    print("Unified Kanban Board System Demo")
    print("=" * 40)

    # Initialize system
    kanban = create_master_board()
    print("✓ Master board initialized")

    # Create an agent sub-board
    agent_board_id = kanban.create_board(
        board_id="santiago_dev_board",
        board_type=BoardType.AGENT,
        name="Santiago-Dev Board",
        description="Development workflow for Santiago-Dev agent",
        parent_board_id=kanban.master_board_id
    )
    print(f"✓ Agent board created: {agent_board_id}")

    # Add some expeditions from our memory architecture analysis
    expeditions = [
        ("EXP-042", "Three-Tier Memory Architecture", "Implement working/episodic/semantic memory layers"),
        ("EXP-043", "Observational Learning Systems", "Enhance human-AI collaborative learning"),
        ("EXP-044", "Memory Refactoring Engine", "Autonomous memory system evolution"),
        ("EXP-045", "Domain Expert Assembly", "Self-organizing specialist teams")
    ]

    for exp_id, title, desc in expeditions:
        card_id = add_expedition_to_board(kanban, kanban.master_board_id, exp_id, title, desc)
        print(f"✓ Added expedition: {exp_id}")

    # Move a card to demonstrate workflow
    kanban.move_card(kanban.master_board_id, card_id, ColumnType.READY, notes="Ready for implementation")
    print("✓ Moved card to Ready column")

    # Get board summary
    summary = kanban.get_board_summary(kanban.master_board_id)
    print(f"✓ Board summary: {summary['columns']['ready']['card_count']} cards in Ready")

    print("\n🎉 Unified Kanban Board System operational!")
    print("Ready to provide single source of truth for workflow management.")