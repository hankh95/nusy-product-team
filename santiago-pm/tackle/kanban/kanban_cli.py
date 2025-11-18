#!/usr/bin/env python3
"""
Santiago PM Kanban CLI - Command Line Interface

Provides command-line access to the Kanban board system for
human developers and autonomous agents.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from .kanban_service import KanbanService
from .kanban_model import ColumnType, ItemType, BoardType


class KanbanCLI:
    """Command-line interface for Kanban board operations."""

    def __init__(self):
        self.service = KanbanService()

    def run(self, args: Optional[list] = None):
        """Run the CLI with given arguments."""
        parser = self._create_parser()

        if args is None:
            args = sys.argv[1:]

        parsed_args = parser.parse_args(args)

        if not hasattr(parsed_args, 'command'):
            parser.print_help()
            return

        # Dispatch to appropriate command
        method_name = f"cmd_{parsed_args.command.replace('-', '_')}"
        command_method = getattr(self, method_name, None)
        if command_method:
            try:
                result = command_method(parsed_args)
                if result:
                    print(result)
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Unknown command: {parsed_args.command}", file=sys.stderr)
            sys.exit(1)

    def _create_parser(self):
        """Create the argument parser."""
        parser = argparse.ArgumentParser(
            description="Santiago PM Kanban Board System",
            prog="kanban"
        )

        subparsers = parser.add_subparsers(dest='command', help='Available commands')

        # Board management commands
        self._add_board_commands(subparsers)

        # Card management commands
        self._add_card_commands(subparsers)

        # Swimlane management commands
        self._add_swimlane_commands(subparsers)

        # Lean flow metrics commands
        self._add_metrics_commands(subparsers)

        # Query commands
        self._add_query_commands(subparsers)

        return parser

    def _add_board_commands(self, subparsers):
        """Add board management commands."""

        # Create board
        create_parser = subparsers.add_parser('create-board', help='Create a new Kanban board')
        create_parser.add_argument('board_id', help='Unique board identifier')
        create_parser.add_argument('name', help='Board display name')
        create_parser.add_argument('--description', '-d', help='Board description')
        create_parser.add_argument('--type', choices=['master', 'agent'], default='agent',
                                 help='Board type (default: agent)')

        # List boards
        list_parser = subparsers.add_parser('list-boards', help='List all boards')

        # Show board
        show_parser = subparsers.add_parser('show-board', help='Show board details')
        show_parser.add_argument('board_id', help='Board identifier')

    def _add_card_commands(self, subparsers):
        """Add card management commands."""

        # Add card
        add_parser = subparsers.add_parser('add-card', help='Add a card to a board')
        add_parser.add_argument('board_id', help='Target board')
        add_parser.add_argument('item_id', help='Item identifier')
        add_parser.add_argument('title', help='Card title')
        add_parser.add_argument('--type', choices=[t.value for t in ItemType],
                              default='feature', help='Item type')
        add_parser.add_argument('--path', required=True, help='Repository path to item')
        add_parser.add_argument('--description', '-d', help='Item description')
        add_parser.add_argument('--priority', choices=['high', 'medium', 'low'],
                              default='medium', help='Priority level')
        add_parser.add_argument('--assignee', '-a', help='Assigned person/agent')
        add_parser.add_argument('--labels', nargs='*', help='Labels for categorization')

        # Move card
        move_parser = subparsers.add_parser('move-card', help='Move a card to a different column')
        move_parser.add_argument('board_id', help='Board containing the card')
        move_parser.add_argument('card_id', help='Card to move')
        move_parser.add_argument('column', choices=[c.value for c in ColumnType],
                               help='Target column')
        move_parser.add_argument('--moved-by', default='cli', help='Person/agent performing move')
        move_parser.add_argument('--reason', '-r', help='Reason for the move')

        # Bulk move
        bulk_parser = subparsers.add_parser('bulk-move', help='Move multiple cards')
        bulk_parser.add_argument('board_id', help='Target board')
        bulk_parser.add_argument('column', choices=[c.value for c in ColumnType],
                               help='Target column')
        bulk_parser.add_argument('card_ids', nargs='+', help='Cards to move')
        bulk_parser.add_argument('--moved-by', default='cli', help='Person/agent performing moves')
        bulk_parser.add_argument('--reason', '-r', help='Reason for bulk move')

    def _add_swimlane_commands(self, subparsers):
        """Add swimlane management commands."""

        # Add swimlane
        add_swimlane_parser = subparsers.add_parser('add-swimlane', help='Add a swimlane to a board')
        add_swimlane_parser.add_argument('board_id', help='Target board')
        add_swimlane_parser.add_argument('swimlane_id', help='Unique swimlane identifier')
        add_swimlane_parser.add_argument('name', help='Swimlane display name')
        add_swimlane_parser.add_argument('--color', default='#808080', help='Swimlane color (hex)')
        add_swimlane_parser.add_argument('--wip-limit', type=int, help='WIP limit for this swimlane')

        # Assign card to swimlane
        assign_parser = subparsers.add_parser('assign-swimlane', help='Assign a card to a swimlane')
        assign_parser.add_argument('board_id', help='Target board')
        assign_parser.add_argument('card_id', help='Card to assign')
        assign_parser.add_argument('swimlane_id', help='Swimlane to assign to')

        # Add comment to card
        comment_parser = subparsers.add_parser('add-comment', help='Add a comment to a card')
        comment_parser.add_argument('board_id', help='Target board')
        comment_parser.add_argument('card_id', help='Card to comment on')
        comment_parser.add_argument('comment', help='Comment text')
        comment_parser.add_argument('--author', '-a', default='cli', help='Comment author')

        # Add tags to card
        tag_parser = subparsers.add_parser('add-tags', help='Add tags to a card')
        tag_parser.add_argument('board_id', help='Target board')
        tag_parser.add_argument('card_id', help='Card to tag')
        tag_parser.add_argument('tags', nargs='+', help='Tags to add (e.g., #blocked @assignee !high)')

        # Process card tags
        process_parser = subparsers.add_parser('process-tags', help='Process tags on a card and trigger actions')
        process_parser.add_argument('board_id', help='Target board')
        process_parser.add_argument('card_id', help='Card to process')

    def _add_metrics_commands(self, subparsers):
        """Add lean flow metrics commands."""

        # Lean flow metrics
        lean_parser = subparsers.add_parser('lean-metrics', help='Show lean flow metrics')
        lean_parser.add_argument('board_id', help='Board to analyze')
        lean_parser.add_argument('--swimlane', help='Filter by swimlane')

        # WIP status
        wip_parser = subparsers.add_parser('wip-status', help='Show WIP status and violations')
        wip_parser.add_argument('board_id', help='Board to analyze')
        wip_parser.add_argument('--swimlane', help='Filter by swimlane')

        # Cumulative flow diagram data
        cfd_parser = subparsers.add_parser('cfd', help='Show cumulative flow diagram data')
        cfd_parser.add_argument('board_id', help='Board to analyze')
        cfd_parser.add_argument('--days', type=int, default=30, help='Days of history to include')

    def _add_query_commands(self, subparsers):
        """Add query commands."""

        # Search cards
        search_parser = subparsers.add_parser('search', help='Search for cards')
        search_parser.add_argument('board_id', help='Board to search')
        search_parser.add_argument('--query', '-q', help='Text search query')
        search_parser.add_argument('--type', choices=[t.value for t in ItemType],
                                 help='Filter by item type')
        search_parser.add_argument('--assignee', '-a', help='Filter by assignee')

        # Show metrics
        metrics_parser = subparsers.add_parser('metrics', help='Show board metrics')
        metrics_parser.add_argument('board_id', help='Board to analyze')

        # Find blocked
        blocked_parser = subparsers.add_parser('blocked', help='Find blocked cards')
        blocked_parser.add_argument('board_id', help='Board to search')

        # Export board
        export_parser = subparsers.add_parser('export', help='Export board data')
        export_parser.add_argument('board_id', help='Board to export')
        export_parser.add_argument('--format', choices=['json', 'yaml'], default='json',
                                 help='Export format')

        # Generate markdown board view
        markdown_parser = subparsers.add_parser('generate-markdown', help='Generate markdown board overview')
        markdown_parser.add_argument('--output', '-o', default='kanban-boards.md',
                                   help='Output file path (default: kanban-boards.md)')
        markdown_parser.add_argument('--boards', nargs='*', help='Specific boards to include (default: all)')
        markdown_parser.add_argument('--include-links', action='store_true', default=True,
                                   help='Include clickable links to repository files')
        markdown_parser.add_argument('--include-metadata', action='store_true', default=True,
                                   help='Include card metadata (assignee, priority, tags)')

    # Command implementations

    def cmd_create_board(self, args):
        """Create a new board."""
        board_type = BoardType.MASTER if args.type == 'master' else BoardType.AGENT

        try:
            board_id = self.service.kanban_system.create_board(
                board_id=args.board_id,
                board_type=board_type,
                name=args.name,
                description=args.description or ""
            )
            return f"✅ Created board: {board_id}"
        except ValueError as e:
            return f"❌ Error: {e}"

    def cmd_list_boards(self, args):
        """List all boards."""
        boards = []
        for board_id, board in self.service.kanban_system.boards.items():
            boards.append(f"- {board_id}: {board.name} ({board.board_type.value})")

        if not boards:
            return "No boards found"

        return "Available boards:\n" + "\n".join(boards)

    def cmd_show_board(self, args):
        """Show board details."""
        summary = self.service.kanban_system.get_board_summary(args.board_id)

        if 'error' in summary:
            return f"❌ Error: {summary['error']}"

        output = []
        output.append(f"Board: {summary['name']} ({summary['type']})")
        output.append("")

        for col_name, col_data in summary['columns'].items():
            output.append(f"{col_data['title']} ({col_data['card_count']} cards)")
            if col_data['wip_limit']:
                output.append(f"  WIP Limit: {col_data['wip_limit']}")

            for card in col_data['cards']:
                assignee = f" [{card['assignee']}]" if card['assignee'] else ""
                output.append(f"  - {card['title']}{assignee} ({card['item_type']})")

            output.append("")

        return "\n".join(output)

    def cmd_add_card(self, args):
        """Add a card to a board."""
        try:
            card_id = self.service.add_item_to_board(
                board_id=args.board_id,
                item_id=args.item_id,
                item_type=ItemType(args.type),
                title=args.title,
                repository_path=args.path,
                description=args.description or "",
                priority=args.priority,
                assignee=args.assignee,
                labels=args.labels
            )
            return f"✅ Added card: {card_id}"
        except Exception as e:
            return f"❌ Error: {e}"

    def cmd_move_card(self, args):
        """Move a card to a different column."""
        result = self.service.move_card_with_validation(
            board_id=args.board_id,
            card_id=args.card_id,
            new_column=ColumnType(args.column),
            moved_by=args.moved_by,
            reason=args.reason
        )

        if result['success']:
            return f"✅ Moved card {result['card_id']} to {result['new_column']}"
        else:
            return f"❌ Failed to move card: {result.get('error', 'Unknown error')}"

    def cmd_bulk_move(self, args):
        """Move multiple cards."""
        result = self.service.bulk_move_cards(
            board_id=args.board_id,
            card_ids=args.card_ids,
            new_column=ColumnType(args.column),
            moved_by=args.moved_by,
            reason=args.reason or "Bulk move operation"
        )

        return f"✅ Bulk move completed: {result['successful']}/{result['total']} cards moved"

    def cmd_search(self, args):
        """Search for cards."""
        item_type = ItemType(args.type) if args.type else None

        results = self.service.kanban_system.search_cards(
            board_id=args.board_id,
            query=args.query or "",
            item_type=item_type,
            assignee=args.assignee
        )

        if not results:
            return "No cards found matching criteria"

        output = [f"Found {len(results)} cards:"]
        for card in results:
            assignee = f" [{card['assignee']}]" if card['assignee'] else ""
            output.append(f"- {card['title']}{assignee} ({card['item_type']}) - {card['column']}")

        return "\n".join(output)

    def cmd_metrics(self, args):
        """Show board metrics."""
        metrics = self.service.get_board_metrics(args.board_id)

        if 'error' in metrics:
            return f"❌ Error: {metrics['error']}"

        output = []
        output.append(f"Board Metrics: {metrics['board_name']}")
        output.append(f"Total Cards: {metrics['total_cards']}")
        output.append("")

        output.append("Cards by Column:")
        for col, count in metrics['cards_by_column'].items():
            output.append(f"  {col}: {count}")
        output.append("")

        output.append("Cards by Priority:")
        for priority, count in metrics['cards_by_priority'].items():
            output.append(f"  {priority}: {count}")
        output.append("")

        output.append("Cards by Type:")
        for item_type, count in metrics['cards_by_type'].items():
            output.append(f"  {item_type}: {count}")
        output.append("")

        output.append(f"Blocked Cards: {metrics['blocked_cards']}")

        return "\n".join(output)

    def cmd_blocked(self, args):
        """Find blocked cards."""
        blocked = self.service.find_blocked_cards(args.board_id)

        if not blocked:
            return "No blocked cards found"

        output = [f"Found {len(blocked)} blocked cards:"]
        for card in blocked:
            output.append(f"- {card['title']} [{card['assignee'] or 'unassigned'}]")
            output.append(f"  Reason: {card['blocked_reason']}")
            output.append(f"  Column: {card['column']}")

        return "\n".join(output)

    def cmd_export(self, args):
        """Export board data."""
        data = self.service.export_board_data(args.board_id, args.format)
        return data

    def cmd_generate_markdown(self, args):
        """Generate markdown board overview."""
        try:
            # Generate markdown content
            markdown_content = self._generate_board_markdown(
                board_ids=args.boards,
                include_links=args.include_links,
                include_metadata=args.include_metadata
            )

            # Write to file
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(markdown_content)

            return f"✅ Generated markdown board overview: {args.output}"
        except Exception as e:
            return f"❌ Error generating markdown: {e}"

    def _generate_board_markdown(self, board_ids=None, include_links=True, include_metadata=True):
        """Generate markdown content for board overview."""
        from datetime import datetime

        lines = []
        lines.append("# 🏗️ Santiago PM Kanban Boards")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Get boards to include
        if board_ids:
            boards_to_process = {bid: self.service.kanban_system.boards.get(bid)
                               for bid in board_ids if bid in self.service.kanban_system.boards}
        else:
            boards_to_process = self.service.kanban_system.boards

        if not boards_to_process:
            lines.append("No boards found.")
            return "\n".join(lines)

        # Process each board
        for board_id, board in boards_to_process.items():
            if board is None:
                continue
            lines.append(f"## 📋 {board.name}")
            lines.append("")
            if board.description:
                lines.append(f"*{board.description}*")
                lines.append("")

            lines.append(f"**Board ID:** `{board_id}` | **Type:** {board.board_type.value}")
            lines.append("")

            # Get board summary for column structure
            summary = self.service.kanban_system.get_board_summary(board_id)
            if 'error' in summary:
                lines.append(f"❌ Error loading board: {summary['error']}")
                lines.append("")
                continue

            # Get full board data for detailed card information
            full_board = self.service.kanban_system.boards.get(board_id)
            if not full_board:
                lines.append("❌ Error: Board not found in full data")
                lines.append("")
                continue

            # Column headers
            columns = list(summary['columns'].keys())
            lines.append("### Columns")
            lines.append("")

            # Create table header
            header = "| " + " | ".join([f"**{summary['columns'][col]['title']}**<br/>*{summary['columns'][col]['card_count']} cards*" for col in columns]) + " |"
            lines.append(header)

            # Table separator
            separator = "|" + "|".join([":---:" for _ in columns]) + "|"
            lines.append(separator)

            # Find max cards in any column for table height
            max_cards = max(len(summary['columns'][col]['cards']) for col in columns) if columns else 0

            # Generate table rows
            for row_idx in range(max_cards):
                row_cells = []
                for col in columns:
                    cards = summary['columns'][col]['cards']
                    if row_idx < len(cards):
                        card = cards[row_idx]
                        # Get full card data from board
                        full_card = None
                        for c in full_board.columns[col].cards:
                            if c.card_id == card['card_id']:
                                full_card = c
                                break
                        cell_content = self._format_card_markdown(full_card, include_links, include_metadata)
                        row_cells.append(cell_content)
                    else:
                        row_cells.append(" ")
                lines.append("| " + " | ".join(row_cells) + " |")

            lines.append("")

            # Add swimlane information if any
            if board.swimlanes:
                lines.append("### 🏊 Swimlanes")
                lines.append("")
                for swimlane_id, swimlane in board.swimlanes.items():
                    wip_info = f" (WIP: {swimlane.wip_limit})" if swimlane.wip_limit else ""
                    lines.append(f"- **{swimlane.name}** (`{swimlane_id}`){wip_info}")
                lines.append("")

            # Add board metrics summary
            try:
                metrics = self.service.get_board_metrics(board_id)
                if 'error' not in metrics:
                    lines.append("### 📊 Quick Metrics")
                    lines.append("")
                    lines.append(f"- **Total Cards:** {metrics['total_cards']}")
                    lines.append(f"- **Blocked Cards:** {metrics['blocked_cards']}")

                    # Priority breakdown
                    priorities = [f"{k}: {v}" for k, v in metrics['cards_by_priority'].items() if v > 0]
                    if priorities:
                        lines.append(f"- **Priorities:** {', '.join(priorities)}")

                    lines.append("")
            except Exception:
                pass  # Skip metrics if there's an error

            lines.append("---")
            lines.append("")

        # Footer
        lines.append("## 📝 How to Use")
        lines.append("")
        lines.append("This file is auto-generated. To update:")
        lines.append("```bash")
        lines.append("kanban generate-markdown")
        lines.append("```")
        lines.append("")
        lines.append("To work with cards:")
        lines.append("- Click links to open files in your editor")
        lines.append("- Use CLI commands to move cards between columns")
        lines.append("- Add comments and tags for better tracking")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append(f"*Generated by Santiago PM Kanban System on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

        return "\n".join(lines)

    def _format_card_markdown(self, card, include_links=True, include_metadata=True):
        """Format a card for markdown display."""
        if not card:
            return " "

        lines = []

        # Card title with link
        if include_links and hasattr(card, 'item_reference') and card.item_reference.repository_path:
            # Create relative link (assuming this file is in project root)
            link_path = card.item_reference.repository_path
            title_link = f"[{card.item_reference.title}]({link_path})"
        else:
            title_link = card.item_reference.title

        lines.append(f"**{title_link}**")

        # Item type badge
        item_type = card.item_reference.item_type.value if hasattr(card.item_reference, 'item_type') else 'unknown'
        lines.append(f"*{item_type}*")

        # Metadata
        if include_metadata:
            metadata_parts = []

            # Assignee
            if card.item_reference.assignee:
                metadata_parts.append(f"👤 {card.item_reference.assignee}")

            # Priority
            priority = card.item_reference.priority
            if priority:
                priority_icons = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }
                icon = priority_icons.get(priority, '⚪')
                metadata_parts.append(f"{icon} {priority}")

            # Tags (show first few)
            tags = getattr(card, 'tags', [])
            if tags:
                tag_str = " ".join(tags[:3])  # Show first 3 tags
                if len(tags) > 3:
                    tag_str += f" +{len(tags)-3} more"
                metadata_parts.append(f"🏷️ {tag_str}")

            # Comments count
            comments = getattr(card, 'comments', [])
            if comments:
                lines.append(f"💬 {len(comments)} comments")

            # Blocked status
            if getattr(card, 'blocked_reason', None):
                lines.append(f"🚫 Blocked: {card.blocked_reason}")

            if metadata_parts:
                lines.append(" | ".join(metadata_parts))

        return "<br/>".join(lines)

    def cmd_add_swimlane(self, args):
        """Add a swimlane to a board."""
        try:
            swimlane_id = self.service.add_swimlane(
                board_id=args.board_id,
                swimlane_id=args.swimlane_id,
                name=args.name,
                color=args.color,
                wip_limit=args.wip_limit
            )
            return f"✅ Added swimlane: {swimlane_id}"
        except Exception as e:
            return f"❌ Error: {e}"

    def cmd_assign_swimlane(self, args):
        """Assign a card to a swimlane."""
        try:
            success = self.service.assign_card_to_swimlane(
                board_id=args.board_id,
                card_id=args.card_id,
                swimlane_id=args.swimlane_id
            )
            if success:
                return f"✅ Assigned card {args.card_id} to swimlane {args.swimlane_id}"
            else:
                return f"❌ Failed to assign card: Card or swimlane not found"
        except Exception as e:
            return f"❌ Error: {e}"

    def cmd_lean_metrics(self, args):
        """Show lean flow metrics."""
        try:
            metrics = self.service.get_lean_flow_metrics(
                board_id=args.board_id,
                days=30  # Default to 30 days
            )

            output = []
            output.append(f"Lean Flow Metrics: {args.board_id}")
            output.append("")

            # Cycle time metrics (convert hours to days)
            cycle_avg_days = metrics.get('average_cycle_time_hours', 0) / 24
            cycle_p50_days = metrics.get('cycle_time_p50', 0) / 24  # already in hours
            cycle_p85_days = metrics.get('cycle_time_p85', 0) / 24
            cycle_p95_days = metrics.get('cycle_time_p95', 0) / 24

            output.append("Cycle Time (days):")
            output.append(f"  Average: {cycle_avg_days:.1f}")
            output.append(f"  P50: {cycle_p50_days:.1f}")
            output.append(f"  P85: {cycle_p85_days:.1f}")
            output.append(f"  P95: {cycle_p95_days:.1f}")
            output.append("")

            # Lead time metrics (convert hours to days)
            lead_avg_days = metrics.get('average_lead_time_hours', 0) / 24
            lead_p50_days = metrics.get('lead_time_p50', 0) / 24
            lead_p85_days = metrics.get('lead_time_p85', 0) / 24
            lead_p95_days = metrics.get('lead_time_p95', 0) / 24

            output.append("Lead Time (days):")
            output.append(f"  Average: {lead_avg_days:.1f}")
            output.append(f"  P50: {lead_p50_days:.1f}")
            output.append(f"  P85: {lead_p85_days:.1f}")
            output.append(f"  P95: {lead_p95_days:.1f}")
            output.append("")

            # Throughput
            throughput_daily = metrics.get('throughput_per_day', 0)
            output.append("Throughput:")
            output.append(f"  Daily: {throughput_daily:.2f}")
            output.append(f"  Weekly: {throughput_daily * 7:.2f}")
            output.append(f"  Monthly: {throughput_daily * 30:.2f}")
            output.append("")

            # Flow efficiency
            flow_eff = metrics.get('flow_efficiency', 0)
            output.append("Flow Efficiency:")
            output.append(f"  Average: {flow_eff:.1%}")
            output.append("")

            # WIP info
            output.append("Current Status:")
            output.append(f"  Total Cards: {metrics.get('total_cards', 0)}")
            output.append(f"  Active Cards: {metrics.get('active_cards', 0)}")
            output.append(f"  Completed (30 days): {metrics.get('completed_cards', 0)}")

            return "\n".join(output)
        except Exception as e:
            return f"❌ Error: {e}"

    def cmd_wip_status(self, args):
        """Show WIP status and violations."""
        try:
            status = self.service.get_wip_status(board_id=args.board_id)

            if 'error' in status:
                return f"❌ Error: {status['error']}"

            output = []
            output.append(f"WIP Status: {args.board_id}")
            output.append("")

            # Column WIP
            output.append("Column WIP Limits:")
            for col_key, col_data in status.get('columns', {}).items():
                limit_str = f"/{col_data['wip_limit']}" if col_data['wip_limit'] else ""
                status_icon = "❌" if col_data['status'] == 'exceeded' else "⚠️" if col_data['status'] == 'at_limit' else "✅"
                output.append(f"  {status_icon} {col_key}: {col_data['card_count']}{limit_str}")

            output.append("")

            # Swimlane WIP
            if status.get('swimlanes'):
                output.append("Swimlane WIP Limits:")
                for sl_key, sl_data in status['swimlanes'].items():
                    limit_str = f"/{sl_data['wip_limit']}" if sl_data['wip_limit'] else ""
                    status_icon = "❌" if sl_data['status'] == 'exceeded' else "✅"
                    output.append(f"  {status_icon} {sl_key}: {sl_data['card_count']}{limit_str}")
                output.append("")

            # Violations
            violations = status.get('violations', [])
            if violations:
                output.append(f"❌ WIP Limit Violations: {len(violations)}")
                for v in violations[:5]:  # Show first 5
                    output.append(f"  - {v['type'].title()} {v['id']}: {v['current']}/{v['limit']} (+{v['over']})")
                output.append("")

            # Recommendations
            recommendations = status.get('recommendations', [])
            if recommendations:
                output.append("Recommendations:")
                for rec in recommendations:
                    output.append(f"  • {rec}")

            return "\n".join(output)
        except Exception as e:
            return f"❌ Error: {e}"

    def cmd_cfd(self, args):
        """Show cumulative flow diagram data."""
        try:
            cfd_data = self.service.get_cumulative_flow_data(
                board_id=args.board_id,
                days=args.days
            )

            if 'error' in cfd_data:
                return f"❌ Error: {cfd_data['error']}"

            output = []
            output.append(f"Cumulative Flow Data: {args.board_id}")
            output.append(f"Time Period: Last {args.days} days")
            output.append("")

            # Current counts
            counts = cfd_data.get('current_counts', {})
            if counts:
                output.append("Current Card Distribution:")
                for col, count in counts.items():
                    output.append(f"  {col}: {count} cards")
                output.append("")

            output.append("Note: Historical cumulative flow data requires")
            output.append("additional data collection and storage implementation.")
            output.append("Currently showing current snapshot only.")

            return "\n".join(output)
        except Exception as e:
            return f"❌ Error: {e}"

    def cmd_add_comment(self, args):
        """Add a comment to a card."""
        try:
            success = self.service.add_comment_to_card(
                board_id=args.board_id,
                card_id=args.card_id,
                comment_text=args.comment,
                author=args.author
            )
            if success:
                return f"✅ Comment added to card {args.card_id}"
            else:
                return f"❌ Failed to add comment: Card or board not found"
        except Exception as e:
            return f"❌ Error: {e}"

    def cmd_add_tags(self, args):
        """Add tags to a card."""
        try:
            # Find the card and add tags
            board = self.service.kanban_system.boards.get(args.board_id)
            if not board:
                return f"❌ Board {args.board_id} not found"

            card = None
            for column in board.columns.values():
                for c in column.cards:
                    if c.card_id == args.card_id:
                        card = c
                        break
                if card:
                    break

            if not card:
                return f"❌ Card {args.card_id} not found"

            # Add new tags
            for tag in args.tags:
                if tag not in card.tags:
                    card.tags.append(tag)

            board.updated_at = datetime.now()
            self.service.kanban_system._save_boards()

            return f"✅ Added tags {args.tags} to card {args.card_id}"
        except Exception as e:
            return f"❌ Error: {e}"

    def cmd_process_tags(self, args):
        """Process tags on a card and trigger actions."""
        try:
            result = self.service.kanban_system.process_card_tags(args.board_id, args.card_id)

            if 'error' in result:
                return f"❌ Error: {result['error']}"

            output = []
            output.append(f"✅ Processed {result['tags_processed']} tags on card {args.card_id}")
            output.append("")

            if result['actions_triggered']:
                output.append("Actions triggered:")
                for action in result['actions_triggered']:
                    output.append(f"  • {action['type']}: {action['action']} ({action.get('tag', '')})")
                output.append("")

            if result['status_updates']:
                output.append("Status updates:")
                for key, value in result['status_updates'].items():
                    output.append(f"  • {key}: {value}")

            return "\n".join(output)
        except Exception as e:
            return f"❌ Error: {e}"


def main():
    """Main entry point for the CLI."""
    cli = KanbanCLI()
    cli.run()


if __name__ == "__main__":
    main()