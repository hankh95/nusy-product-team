#!/usr/bin/env python3
"""
Santiago PM Kanban Module - Unified Workflow Management

This module provides the unified Kanban board system for Santiago-PM,
serving as the single source of truth for workflow management across
all project artifacts.
"""

import os
import json
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, asdict, field
from enum import Enum
import yaml

from pydantic import BaseModel, Field


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
    labels: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class Comment:
    """A comment/note on a Kanban card"""
    content: str
    author: str = "system"
    created_at: datetime = field(default_factory=datetime.now)
    tags: List[str] = field(default_factory=list)  # Tags extracted from this comment


@dataclass
class KanbanCard:
    """A card on the Kanban board (references an item)"""
    card_id: str
    item_reference: ItemReference
    column: ColumnType
    position: int = 0  # Position within column (for ordering)
    swimlane_id: Optional[str] = None  # Swimlane assignment
    comments: List[Comment] = field(default_factory=list)  # Structured comments with metadata
    tags: List[str] = field(default_factory=list)  # Dynamic tags that can trigger actions
    blocked_reason: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    moved_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None  # When work actually began
    completed_at: Optional[datetime] = None  # When work was completed


@dataclass
class Swimlane:
    """A swimlane for categorizing work on the Kanban board"""
    swimlane_id: str
    name: str
    description: str = ""
    color: Optional[str] = None  # Hex color for visual distinction
    wip_limit: Optional[int] = None  # Swimlane-specific WIP limit
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class KanbanColumn:
    """A column on the Kanban board"""
    column_type: ColumnType
    title: str
    cards: List[KanbanCard] = field(default_factory=list)
    wip_limit: Optional[int] = None  # Work in progress limit
    is_closed: bool = False  # Whether this column represents closed/completed work
    is_archived: bool = False  # Whether this column should hide completed items


@dataclass
class KanbanBoard:
    """A Kanban board with columns and cards"""
    board_id: str
    board_type: BoardType
    name: str
    description: str = ""
    columns: Dict[str, KanbanColumn] = field(default_factory=dict)
    swimlanes: Dict[str, Swimlane] = field(default_factory=dict)  # Swimlanes for categorization
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

    def add_swimlane(self,
                    board_id: str,
                    swimlane_id: str,
                    name: str,
                    description: str = "",
                    color: Optional[str] = None,
                    wip_limit: Optional[int] = None) -> str:
        """
        Add a swimlane to a board.

        Args:
            board_id: Target board
            swimlane_id: Unique swimlane identifier
            name: Display name
            description: Swimlane description
            color: Hex color for visual distinction
            wip_limit: Swimlane-specific WIP limit

        Returns:
            Swimlane ID
        """
        if board_id not in self.boards:
            raise ValueError(f"Board {board_id} not found")

        board = self.boards[board_id]
        if swimlane_id in board.swimlanes:
            raise ValueError(f"Swimlane {swimlane_id} already exists")

        swimlane = Swimlane(
            swimlane_id=swimlane_id,
            name=name,
            description=description,
            color=color,
            wip_limit=wip_limit
        )

        board.swimlanes[swimlane_id] = swimlane
        board.updated_at = datetime.now()
        self._save_boards()

        return swimlane_id

    def assign_card_to_swimlane(self, board_id: str, card_id: str, swimlane_id: Optional[str]) -> bool:
        """
        Assign a card to a swimlane.

        Args:
            board_id: Board containing the card
            card_id: Card to assign
            swimlane_id: Target swimlane (None to remove assignment)

        Returns:
            Success status
        """
        if board_id not in self.boards:
            return False

        board = self.boards[board_id]
        if swimlane_id and swimlane_id not in board.swimlanes:
            return False

        # Find and update the card
        for column in board.columns.values():
            for card in column.cards:
                if card.card_id == card_id:
                    card.swimlane_id = swimlane_id
                    board.updated_at = datetime.now()
                    self._save_boards()
                    return True

        return False

    def add_comment_to_card(self,
                           board_id: str,
                           card_id: str,
                           comment_text: str,
                           author: str = "system") -> bool:
        """
        Add a comment to a card.

        Args:
            board_id: Board containing the card
            card_id: Card to comment on
            comment_text: Comment content
            author: Comment author

        Returns:
            Success status
        """
        if board_id not in self.boards:
            return False

        board = self.boards[board_id]

        # Find the card
        card = None
        for column in board.columns.values():
            for c in column.cards:
                if c.card_id == card_id:
                    card = c
                    break
            if card:
                break

        if not card:
            return False

        # Parse tags from comment
        parsed_tags = self._parse_tags_from_text(comment_text)

        # Create comment
        comment = Comment(
            content=comment_text,
            author=author,
            tags=parsed_tags
        )

        # Add comment to card
        card.comments.append(comment)

        # Add tags to card's tag list
        for tag in parsed_tags:
            if tag not in card.tags:
                card.tags.append(tag)

        board.updated_at = datetime.now()
        self._save_boards()

        return True

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
                 notes: Optional[str] = None,
                 moved_by: str = "system") -> bool:
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
            # Parse tags from notes and add as comment
            parsed_tags = self._parse_tags_from_text(notes)
            comment = Comment(
                content=notes,
                author=moved_by if moved_by else "system",
                tags=parsed_tags
            )
            card.comments.append(comment)
            # Add tags to card's tag list
            for tag in parsed_tags:
                if tag not in card.tags:
                    card.tags.append(tag)

        # Track cycle time milestones
        if new_column == ColumnType.IN_PROGRESS and not card.started_at:
            card.started_at = datetime.now()
        elif new_column == ColumnType.DONE and not card.completed_at:
            card.completed_at = datetime.now()

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

    def get_lean_flow_metrics(self, board_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Calculate lean flow metrics for a board.

        Args:
            board_id: Board to analyze
            days: Number of days to look back

        Returns:
            Dictionary with cycle time, lead time, throughput, and other metrics
        """
        if board_id not in self.boards:
            return {"error": "Board not found"}

        board = self.boards[board_id]
        cutoff_date = datetime.now() - timedelta(days=days)

        completed_cards = []
        active_cards = []
        all_cards = []

        # Collect cards by status
        for column in board.columns.values():
            for card in column.cards:
                all_cards.append(card)
                if card.completed_at and card.completed_at >= cutoff_date:
                    completed_cards.append(card)
                elif card.started_at and not card.completed_at:
                    active_cards.append(card)

        # Calculate cycle times (time from start to completion)
        cycle_times = []
        for card in completed_cards:
            if card.started_at and card.completed_at:
                cycle_time = (card.completed_at - card.started_at).total_seconds() / 3600  # hours
                cycle_times.append(cycle_time)

        # Calculate lead times (time from creation to completion)
        lead_times = []
        for card in completed_cards:
            if card.completed_at:
                lead_time = (card.completed_at - card.created_at).total_seconds() / 3600  # hours
                lead_times.append(lead_time)

        # Calculate throughput (items completed per day)
        completed_count = len(completed_cards)
        throughput_per_day = completed_count / days if days > 0 else 0

        # Calculate WIP (Work in Progress)
        wip_count = len(active_cards)

        # Calculate average cycle time and lead time
        avg_cycle_time_hours = sum(cycle_times) / len(cycle_times) if cycle_times else 0
        avg_lead_time_hours = sum(lead_times) / len(lead_times) if lead_times else 0

        # Calculate percentiles
        cycle_times_sorted = sorted(cycle_times)
        lead_times_sorted = sorted(lead_times)

        def percentile(data, p):
            if not data:
                return 0
            k = (len(data) - 1) * p
            f = int(k)
            c = k - f
            if f + 1 < len(data):
                return data[f] + c * (data[f + 1] - data[f])
            return data[f]

        return {
            "board_id": board_id,
            "analysis_period_days": days,
            "total_cards": len(all_cards),
            "completed_cards": completed_count,
            "active_cards": wip_count,
            "throughput_per_day": throughput_per_day,
            "average_cycle_time_hours": avg_cycle_time_hours,
            "average_lead_time_hours": avg_lead_time_hours,
            "cycle_time_p50": percentile(cycle_times_sorted, 0.5),
            "cycle_time_p85": percentile(cycle_times_sorted, 0.85),
            "cycle_time_p95": percentile(cycle_times_sorted, 0.95),
            "lead_time_p50": percentile(lead_times_sorted, 0.5),
            "lead_time_p85": percentile(lead_times_sorted, 0.85),
            "lead_time_p95": percentile(lead_times_sorted, 0.95),
            "wip_aging": self._calculate_wip_aging(active_cards),
            "bottlenecks": self._identify_bottlenecks(board),
            "flow_efficiency": self._calculate_flow_efficiency(completed_cards)
        }

    def _calculate_wip_aging(self, active_cards: List[KanbanCard]) -> Dict[str, Any]:
        """Calculate aging information for work in progress."""
        if not active_cards:
            return {"oldest_days": 0, "average_age_days": 0, "aging_distribution": {}}

        now = datetime.now()
        ages_days = []

        for card in active_cards:
            if card.started_at:
                age = (now - card.started_at).total_seconds() / 86400  # days
            else:
                age = (now - card.created_at).total_seconds() / 86400  # days
            ages_days.append(age)

        # Age distribution
        distribution = {
            "0-1_days": len([a for a in ages_days if a <= 1]),
            "1-3_days": len([a for a in ages_days if 1 < a <= 3]),
            "3-7_days": len([a for a in ages_days if 3 < a <= 7]),
            "7-14_days": len([a for a in ages_days if 7 < a <= 14]),
            "14+_days": len([a for a in ages_days if a > 14])
        }

        return {
            "oldest_days": max(ages_days) if ages_days else 0,
            "average_age_days": sum(ages_days) / len(ages_days) if ages_days else 0,
            "aging_distribution": distribution
        }

    def _identify_bottlenecks(self, board: KanbanBoard) -> List[Dict[str, Any]]:
        """Identify bottleneck columns based on WIP limits and card distribution."""
        bottlenecks = []

        for col_key, column in board.columns.items():
            card_count = len(column.cards)
            wip_limit = column.wip_limit

            if wip_limit and card_count >= wip_limit:
                bottlenecks.append({
                    "column": col_key,
                    "card_count": card_count,
                    "wip_limit": wip_limit,
                    "over_limit": card_count - wip_limit,
                    "severity": "critical" if card_count > wip_limit * 1.5 else "warning"
                })
            elif card_count > 10:  # Arbitrary threshold for columns without explicit limits
                bottlenecks.append({
                    "column": col_key,
                    "card_count": card_count,
                    "wip_limit": None,
                    "over_limit": card_count - 10,
                    "severity": "warning"
                })

        return bottlenecks

    def _calculate_flow_efficiency(self, completed_cards: List[KanbanCard]) -> float:
        """
        Calculate flow efficiency (ratio of active work time to total lead time).

        Flow efficiency = (Sum of cycle times) / (Sum of lead times)
        """
        if not completed_cards:
            return 0.0

        total_cycle_time = 0
        total_lead_time = 0

        for card in completed_cards:
            if card.started_at and card.completed_at:
                cycle_time = (card.completed_at - card.started_at).total_seconds()
                lead_time = (card.completed_at - card.created_at).total_seconds()

                total_cycle_time += cycle_time
                total_lead_time += lead_time

        return total_cycle_time / total_lead_time if total_lead_time > 0 else 0.0

    def _parse_tags_from_text(self, text: str) -> List[str]:
        """
        Parse tags from text content.

        Supports formats:
        - #tag (hashtags)
        - @assignee (mentions)
        - !priority (priority indicators)

        Args:
            text: Text to parse for tags

        Returns:
            List of extracted tags
        """
        import re

        tags = []

        # Find hashtags (#tag)
        hashtags = re.findall(r'#(\w+)', text)
        tags.extend(f"#{tag}" for tag in hashtags)

        # Find mentions (@assignee)
        mentions = re.findall(r'@(\w+)', text)
        tags.extend(f"@{mention}" for mention in mentions)

        # Find priority indicators (!high, !medium, !low)
        priorities = re.findall(r'!(\w+)', text)
        tags.extend(f"!{priority}" for priority in priorities)

        return tags

    def process_card_tags(self, board_id: str, card_id: str) -> Dict[str, Any]:
        """
        Process tags on a card and trigger system actions.

        Args:
            board_id: Board containing the card
            card_id: Card to process

        Returns:
            Dictionary with processing results and triggered actions
        """
        if board_id not in self.boards:
            return {'error': 'Board not found'}

        board = self.boards[board_id]

        # Find the card
        card = None
        for column in board.columns.values():
            for c in column.cards:
                if c.card_id == card_id:
                    card = c
                    break
            if card:
                break

        if not card:
            return {'error': 'Card not found'}

        actions_triggered = []
        status_updates = {}

        # Process tags
        for tag in card.tags:
            if tag.startswith('#'):
                # Hashtag processing
                tag_value = tag[1:]  # Remove #

                if tag_value == 'blocked':
                    status_updates['blocked'] = True
                    actions_triggered.append({
                        'type': 'status_update',
                        'action': 'mark_blocked',
                        'tag': tag
                    })

                elif tag_value == 'user-research':
                    actions_triggered.append({
                        'type': 'integration',
                        'action': 'notify_research_team',
                        'tag': tag
                    })

                # Add more hashtag handlers here

            elif tag.startswith('@'):
                # Mention processing
                assignee = tag[1:]  # Remove @
                if assignee:
                    # Update assignee if not already set
                    if not card.item_reference.assignee:
                        card.item_reference.assignee = assignee
                        card.item_reference.updated_at = datetime.now()
                        status_updates['assignee_updated'] = assignee

                    actions_triggered.append({
                        'type': 'notification',
                        'action': 'notify_assignee',
                        'assignee': assignee,
                        'tag': tag
                    })

            elif tag.startswith('!'):
                # Priority processing
                priority = tag[1:]  # Remove !
                if priority in ['high', 'medium', 'low']:
                    if card.item_reference.priority != priority:
                        card.item_reference.priority = priority
                        card.item_reference.updated_at = datetime.now()
                        status_updates['priority_updated'] = priority

                    actions_triggered.append({
                        'type': 'priority_update',
                        'action': 'set_priority',
                        'priority': priority,
                        'tag': tag
                    })

        # Update blocked status based on tags
        if status_updates.get('blocked') and not card.blocked_reason:
            card.blocked_reason = "Tagged as blocked"

        # Save changes
        self._save_boards()

        return {
            'card_id': card_id,
            'tags_processed': len(card.tags),
            'actions_triggered': actions_triggered,
            'status_updates': status_updates
        }

    def get_cumulative_flow_data(self, board_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Generate cumulative flow diagram data.

        Args:
            board_id: Board to analyze
            days: Number of days to look back

        Returns:
            Data for cumulative flow diagram
        """
        if board_id not in self.boards:
            return {"error": "Board not found"}

        board = self.boards[board_id]

        # This is a simplified implementation
        # In a real system, you'd track historical snapshots
        column_counts = {}
        for col_key, column in board.columns.items():
            column_counts[col_key] = len(column.cards)

        return {
            "board_id": board_id,
            "current_counts": column_counts,
            "note": "Historical data tracking would be needed for full CFD"
        }

    def _load_boards(self):
        """Load boards from storage"""
        boards_file = self.storage_path / "boards.json"
        if boards_file.exists():
            try:
                with open(boards_file, 'r') as f:
                    data = json.load(f)

                for board_data in data.values():
                    # Convert timestamps
                    board_data['created_at'] = self._parse_timestamp(board_data['created_at'])
                    board_data['updated_at'] = self._parse_timestamp(board_data['updated_at'])

                    # Convert board type
                    if isinstance(board_data['board_type'], str):
                        board_data['board_type'] = BoardType(board_data['board_type'])
                    elif hasattr(board_data['board_type'], 'value'):
                        # Already an enum
                        pass
                    else:
                        board_data['board_type'] = BoardType(board_data['board_type'])

                    # Convert columns and cards
                    for col_key, col_data in board_data.get('columns', {}).items():
                        reconstructed_cards = []
                        for card_data in col_data.get('cards', []):
                            # Convert item reference
                            item_ref_data = card_data['item_reference']
                            item_ref_data['created_at'] = self._parse_timestamp(item_ref_data['created_at'])
                            item_ref_data['updated_at'] = self._parse_timestamp(item_ref_data['updated_at'])
                            if isinstance(item_ref_data['item_type'], str):
                                item_ref_data['item_type'] = ItemType(item_ref_data['item_type'])
                            elif hasattr(item_ref_data['item_type'], 'value'):
                                # Already an enum
                                pass
                            else:
                                item_ref_data['item_type'] = ItemType(item_ref_data['item_type'])

                            card_data['item_reference'] = ItemReference(**item_ref_data)

                            # Convert card timestamps
                            card_data['created_at'] = self._parse_timestamp(card_data['created_at'])
                            card_data['moved_at'] = self._parse_timestamp(card_data['moved_at'])
                            if isinstance(card_data['column'], str):
                                card_data['column'] = ColumnType(card_data['column'])
                            elif hasattr(card_data['column'], 'value'):
                                # Already an enum
                                pass
                            else:
                                card_data['column'] = ColumnType(card_data['column'])

                            # Convert comments
                            if 'comments' in card_data:
                                converted_comments = []
                                for comment_data in card_data['comments']:
                                    comment_data['created_at'] = self._parse_timestamp(comment_data['created_at'])
                                    converted_comments.append(Comment(**comment_data))
                                card_data['comments'] = converted_comments
                            else:
                                # Backward compatibility - convert old notes to comments
                                card_data['comments'] = []
                                if 'notes' in card_data:
                                    for note in card_data['notes']:
                                        card_data['comments'].append(Comment(
                                            content=note,
                                            author="system",
                                            created_at=card_data['created_at']
                                        ))
                                card_data.pop('notes', None)

                            # Reconstruct card and add to list
                            card = KanbanCard(**card_data)
                            reconstructed_cards.append(card)
                        
                        # Replace the card data with reconstructed cards
                        col_data['cards'] = reconstructed_cards

                        # Reconstruct column
                        if isinstance(col_key, str):
                            col_data['column_type'] = ColumnType(col_key)
                        elif hasattr(col_key, 'value'):
                            col_data['column_type'] = col_key
                        else:
                            col_data['column_type'] = ColumnType(col_key)
                        board_data['columns'][col_key] = KanbanColumn(**col_data)

                    # Convert swimlanes
                    for sl_key, sl_data in board_data.get('swimlanes', {}).items():
                        sl_data['created_at'] = self._parse_timestamp(sl_data['created_at'])
                        board_data['swimlanes'][sl_key] = Swimlane(**sl_data)

                    board = KanbanBoard(**board_data)
                    self.boards[board.board_id] = board

            except Exception as e:
                print(f"Warning: Could not load boards: {e}")

    def _parse_timestamp(self, timestamp_str):
        """Parse timestamp that could be ISO format or Unix timestamp"""
        if isinstance(timestamp_str, str):
            try:
                # Try ISO format first
                return datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except ValueError:
                try:
                    # Try Unix timestamp (float)
                    return datetime.fromtimestamp(float(timestamp_str), tz=timezone.utc)
                except (ValueError, TypeError):
                    # Fallback to current time
                    return datetime.now(timezone.utc)
        elif isinstance(timestamp_str, (int, float)):
            # Unix timestamp as number
            return datetime.fromtimestamp(timestamp_str, tz=timezone.utc)
        elif isinstance(timestamp_str, datetime):
            return timestamp_str
        else:
            # Fallback
            return datetime.now(timezone.utc)

    def _save_boards(self):
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

                        # Convert comments
                        if 'comments' in card:
                            for comment in card['comments']:
                                comment['created_at'] = comment['created_at'].isoformat()

                # Convert swimlanes
                for sl_key, swimlane in board_dict.get('swimlanes', {}).items():
                    swimlane['created_at'] = swimlane['created_at'].isoformat()

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