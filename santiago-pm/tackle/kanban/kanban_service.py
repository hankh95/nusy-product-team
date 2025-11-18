#!/usr/bin/env python3
"""
Santiago PM Kanban Service - Core Business Logic

This module provides the core business logic for the Kanban board system,
integrating with Santiago-PM's knowledge graph and workflow management.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import json

from .kanban_model import (
    UnifiedKanbanSystem, KanbanBoard, KanbanCard, KanbanColumn,
    ItemReference, ColumnType, BoardType, ItemType
)


class KanbanService:
    """
    Core service for Kanban board operations within Santiago-PM.

    Provides business logic for board management, card operations,
    and integration with the broader PM ecosystem.
    """

    def __init__(self, base_path: Optional[Path] = None):
        """
        Initialize the Kanban service.

        Args:
            base_path: Base path for kanban data storage
        """
        if base_path is None:
            base_path = Path(__file__).parent.parent.parent / ".kanban"

        self.kanban_system = UnifiedKanbanSystem(
            storage_path=str(base_path),
            auto_init=True
        )

    def create_agent_board(self, agent_name: str, description: str = "") -> str:
        """
        Create a board for a specific Santiago agent.

        Args:
            agent_name: Name of the agent (e.g., "santiago-dev", "santiago-ethicist")
            description: Board description

        Returns:
            Board ID
        """
        board_id = f"{agent_name}_board"
        board_name = f"{agent_name.replace('_', ' ').title()} Board"

        return self.kanban_system.create_board(
            board_id=board_id,
            board_type=BoardType.AGENT,
            name=board_name,
            description=description or f"Workflow board for {agent_name}",
            parent_board_id=self.kanban_system.master_board_id
        )

    def add_item_to_board(self,
                         board_id: str,
                         item_id: str,
                         item_type: ItemType,
                         title: str,
                         repository_path: str,
                         description: str = "",
                         priority: str = "medium",
                         assignee: Optional[str] = None,
                         labels: Optional[List[str]] = None) -> str:
        """
        Add a work item to a Kanban board.

        Args:
            board_id: Target board
            item_id: Unique item identifier
            item_type: Type of item
            title: Display title
            repository_path: Path to item in repository
            description: Item description
            priority: Priority level
            assignee: Assigned agent/person
            labels: Categorization labels

        Returns:
            Card ID
        """
        item_ref = ItemReference(
            item_id=item_id,
            item_type=item_type,
            repository_path=repository_path,
            title=title,
            description=description,
            priority=priority,
            assignee=assignee,
            labels=labels or []
        )

        return self.kanban_system.add_card_from_item(
            board_id=board_id,
            item_reference=item_ref,
            initial_column=ColumnType.BACKLOG
        )

    def move_card_with_validation(self,
                                board_id: str,
                                card_id: str,
                                new_column: ColumnType,
                                moved_by: str,
                                reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Move a card with business rule validation.

        Args:
            board_id: Board containing the card
            card_id: Card to move
            new_column: Target column
            moved_by: Agent/person performing the move
            reason: Reason for the move

        Returns:
            Result dictionary with success status and details
        """
        # Validate move based on business rules
        validation_result = self._validate_card_move(board_id, card_id, new_column)
        if not validation_result['valid']:
            return {
                'success': False,
                'error': validation_result['reason'],
                'card_id': card_id
            }

        # Create detailed notes
        notes = f"Moved to {new_column.value} by {moved_by}"
        if reason:
            notes += f": {reason}"

        # Perform the move
        success = self.kanban_system.move_card(
            board_id=board_id,
            card_id=card_id,
            new_column=new_column,
            notes=notes,
            moved_by=moved_by
        )

        if success:
            return {
                'success': True,
                'card_id': card_id,
                'new_column': new_column.value,
                'moved_by': moved_by,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'success': False,
                'error': 'Move operation failed',
                'card_id': card_id
            }

    def _validate_card_move(self, board_id: str, card_id: str, new_column: ColumnType) -> Dict[str, Any]:
        """
        Validate a card move based on business rules.

        Args:
            board_id: Board ID
            card_id: Card ID
            new_column: Target column

        Returns:
            Validation result
        """
        if board_id not in self.kanban_system.boards:
            return {'valid': False, 'reason': 'Board not found'}

        board = self.kanban_system.boards[board_id]

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
            return {'valid': False, 'reason': 'Card not found'}

        # Business rule validations
        current_column = card.column

        # Cannot move from DONE back to earlier states
        if current_column == ColumnType.DONE and new_column != ColumnType.DONE:
            return {'valid': False, 'reason': 'Cannot move completed items back to active states'}

        # Must go through READY before IN_PROGRESS
        if new_column == ColumnType.IN_PROGRESS and current_column not in [ColumnType.READY, ColumnType.IN_PROGRESS]:
            return {'valid': False, 'reason': 'Items must be READY before moving to IN_PROGRESS'}

        # Check WIP limits
        new_col_key = new_column.value
        if new_col_key in board.columns:
            wip_limit = board.columns[new_col_key].wip_limit
            current_count = len(board.columns[new_col_key].cards)
            if wip_limit and current_count >= wip_limit:
                return {'valid': False, 'reason': f'WIP limit ({wip_limit}) exceeded for {new_column.value}'}

        return {'valid': True}

    def get_board_metrics(self, board_id: str) -> Dict[str, Any]:
        """
        Get comprehensive metrics for a board.

        Args:
            board_id: Board to analyze

        Returns:
            Metrics dictionary
        """
        if board_id not in self.kanban_system.boards:
            return {'error': 'Board not found'}

        board = self.kanban_system.boards[board_id]
        summary = self.kanban_system.get_board_summary(board_id)

        metrics = {
            'board_id': board_id,
            'board_name': board.name,
            'total_cards': sum(len(col['cards']) for col in summary['columns'].values()),
            'cards_by_column': {k: v['card_count'] for k, v in summary['columns'].items()},
            'cards_by_priority': {'high': 0, 'medium': 0, 'low': 0},
            'cards_by_type': {t.value: 0 for t in ItemType},
            'blocked_cards': 0,
            'average_cycle_time': None,  # Would need historical data
            'throughput': None  # Would need historical data
        }

        # Calculate distributions
        for column in board.columns.values():
            for card in column.cards:
                item_ref = card.item_reference

                # Priority distribution
                priority = item_ref.priority
                if priority in metrics['cards_by_priority']:
                    metrics['cards_by_priority'][priority] += 1

                # Type distribution
                item_type = item_ref.item_type.value
                if item_type in metrics['cards_by_type']:
                    metrics['cards_by_type'][item_type] += 1

                # Blocked count
                if card.blocked_reason:
                    metrics['blocked_cards'] += 1

        return metrics

    def find_blocked_cards(self, board_id: str) -> List[Dict[str, Any]]:
        """
        Find all blocked cards on a board.

        Args:
            board_id: Board to search

        Returns:
            List of blocked cards
        """
        if board_id not in self.kanban_system.boards:
            return []

        board = self.kanban_system.boards[board_id]
        blocked_cards = []

        for column in board.columns.values():
            for card in column.cards:
                if card.blocked_reason:
                    blocked_cards.append({
                        'card_id': card.card_id,
                        'title': card.item_reference.title,
                        'column': card.column.value,
                        'blocked_reason': card.blocked_reason,
                        'assignee': card.item_reference.assignee
                    })

        return blocked_cards

    def bulk_move_cards(self,
                       board_id: str,
                       card_ids: List[str],
                       new_column: ColumnType,
                       moved_by: str,
                       reason: str = "") -> Dict[str, Any]:
        """
        Move multiple cards at once.

        Args:
            board_id: Target board
            card_ids: Cards to move
            new_column: Target column
            moved_by: Agent performing moves
            reason: Reason for bulk move

        Returns:
            Bulk operation results
        """
        results = {
            'total': len(card_ids),
            'successful': 0,
            'failed': 0,
            'details': []
        }

        for card_id in card_ids:
            result = self.move_card_with_validation(
                board_id=board_id,
                card_id=card_id,
                new_column=new_column,
                moved_by=moved_by,
                reason=reason
            )

            if result['success']:
                results['successful'] += 1
            else:
                results['failed'] += 1

            results['details'].append(result)

        return results

    def export_board_data(self, board_id: str, format: str = 'json') -> str:
        """
        Export board data for external use.

        Args:
            board_id: Board to export
            format: Export format ('json' or 'yaml')

        Returns:
            Exported data as string
        """
        summary = self.kanban_system.get_board_summary(board_id)
        if 'error' in summary:
            return json.dumps(summary)

        if format.lower() == 'yaml':
            try:
                import yaml
                return yaml.dump(summary, default_flow_style=False)
            except ImportError:
                pass  # Fall back to JSON

        return json.dumps(summary, indent=2)

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
        return self.kanban_system.add_swimlane(
            board_id=board_id,
            swimlane_id=swimlane_id,
            name=name,
            description=description,
            color=color,
            wip_limit=wip_limit
        )

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
        return self.kanban_system.assign_card_to_swimlane(board_id, card_id, swimlane_id)

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
        return self.kanban_system.add_comment_to_card(board_id, card_id, comment_text, author)

    def get_lean_flow_metrics(self, board_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get comprehensive lean flow metrics for a board.

        Args:
            board_id: Board to analyze
            days: Number of days to look back for analysis

        Returns:
            Dictionary with cycle time, lead time, throughput, and other lean metrics
        """
        return self.kanban_system.get_lean_flow_metrics(board_id, days)

    def get_cumulative_flow_data(self, board_id: str, days: int = 30) -> Dict[str, Any]:
        """
        Get cumulative flow diagram data for a board.

        Args:
            board_id: Board to analyze
            days: Number of days to look back

        Returns:
            Data suitable for generating cumulative flow diagrams
        """
        return self.kanban_system.get_cumulative_flow_data(board_id, days)

    def get_wip_status(self, board_id: str) -> Dict[str, Any]:
        """
        Get current WIP (Work in Progress) status with warnings.

        Args:
            board_id: Board to check

        Returns:
            WIP status with limit violations and recommendations
        """
        if board_id not in self.kanban_system.boards:
            return {'error': 'Board not found'}

        board = self.kanban_system.boards[board_id]
        wip_status = {
            'board_id': board_id,
            'columns': {},
            'swimlanes': {},
            'violations': [],
            'recommendations': []
        }

        # Check column WIP limits
        for col_key, column in board.columns.items():
            card_count = len(column.cards)
            wip_status['columns'][col_key] = {
                'card_count': card_count,
                'wip_limit': column.wip_limit,
                'status': 'ok'
            }

            if column.wip_limit:
                if card_count > column.wip_limit:
                    wip_status['columns'][col_key]['status'] = 'exceeded'
                    wip_status['violations'].append({
                        'type': 'column',
                        'id': col_key,
                        'current': card_count,
                        'limit': column.wip_limit,
                        'over': card_count - column.wip_limit
                    })
                elif card_count == column.wip_limit:
                    wip_status['columns'][col_key]['status'] = 'at_limit'

        # Check swimlane WIP limits
        for swimlane_id, swimlane in board.swimlanes.items():
            # Count cards in this swimlane
            swimlane_cards = 0
            for column in board.columns.values():
                for card in column.cards:
                    if card.swimlane_id == swimlane_id:
                        swimlane_cards += 1

            wip_status['swimlanes'][swimlane_id] = {
                'card_count': swimlane_cards,
                'wip_limit': swimlane.wip_limit,
                'status': 'ok'
            }

            if swimlane.wip_limit and swimlane_cards > swimlane.wip_limit:
                wip_status['swimlanes'][swimlane_id]['status'] = 'exceeded'
                wip_status['violations'].append({
                    'type': 'swimlane',
                    'id': swimlane_id,
                    'current': swimlane_cards,
                    'limit': swimlane.wip_limit,
                    'over': swimlane_cards - swimlane.wip_limit
                })

        # Generate recommendations
        if wip_status['violations']:
            wip_status['recommendations'].append("WIP limits exceeded - focus on completing work before starting new items")
            wip_status['recommendations'].append("Consider swarm on bottleneck areas to improve flow")

        return wip_status