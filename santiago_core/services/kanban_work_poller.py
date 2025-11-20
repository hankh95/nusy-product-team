#!/usr/bin/env python3
"""
Kanban Work Poller Service

This service continuously polls the kanban board for ready tickets and automatically
starts work on them when they become available. It integrates with the documentation
automation system to create documentation stubs when work begins.

Key features:
- Polls kanban boards for ready tickets at configurable intervals
- Automatically moves high-priority tickets to in_progress
- Triggers documentation automation for feature start events
- Supports multiple boards and configurable polling intervals
- Includes health monitoring and graceful shutdown
"""

import asyncio
import signal
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

from santiago_core.services.kanban_service import SantiagoKanbanService
from santiago_core.services.documentation_integration import DocumentationWorkflowIntegration


class KanbanWorkPoller:
    """Service that polls kanban boards for ready work and automatically starts it"""

    def __init__(self, workspace_path: Path, config: Optional[Dict[str, Any]] = None):
        self.workspace_path = workspace_path
        self.config = config or self._get_default_config()
        self.kanban_service = SantiagoKanbanService(workspace_path)
        self.docs_integration = DocumentationWorkflowIntegration(workspace_path)

        # Service state
        self.running = False
        self.last_poll_time = None
        self.processed_cards = set()  # Track cards we've already processed
        self.poll_interval = self.config.get('poll_interval_seconds', 30)
        self.max_concurrent_work = self.config.get('max_concurrent_work', 3)
        self.target_boards = self.config.get('target_boards', [])

        # Setup logging
        self.logger = logging.getLogger('KanbanWorkPoller')
        self.logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration"""
        return {
            'poll_interval_seconds': 30,  # Poll every 30 seconds
            'max_concurrent_work': 3,     # Maximum concurrent work items
            'target_boards': [],          # Empty means poll all boards
            'auto_start_work': True,      # Whether to automatically start work
            'documentation_enabled': True, # Whether to trigger documentation
            'log_level': 'INFO'
        }

    async def start(self):
        """Start the polling service"""
        self.logger.info("🚀 Starting Kanban Work Poller Service")
        self.running = True

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

        try:
            # Initial discovery of boards
            await self._discover_boards()

            # Main polling loop
            while self.running:
                try:
                    await self._poll_and_process_work()
                    await asyncio.sleep(self.poll_interval)
                except Exception as e:
                    self.logger.error(f"❌ Error in polling loop: {e}")
                    await asyncio.sleep(self.poll_interval)

        except Exception as e:
            self.logger.error(f"❌ Fatal error in poller service: {e}")
        finally:
            self.logger.info("🛑 Kanban Work Poller Service stopped")

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        self.logger.info(f"📡 Received signal {signum}, shutting down gracefully...")
        self.running = False

    async def _discover_boards(self):
        """Discover available kanban boards"""
        self.logger.info("🔍 Discovering kanban boards...")

        boards_result = await self.kanban_service.handle_tool_call('kanban_list_boards', {})
        if boards_result.error:
            self.logger.error(f"❌ Failed to list boards: {boards_result.error}")
            return

        boards = boards_result.result.get('boards', [])
        if not boards:
            self.logger.warning("⚠️  No kanban boards found")
            return

        if self.target_boards:
            # Filter to target boards
            available_board_ids = [b['board_id'] for b in boards]
            self.target_boards = [b for b in self.target_boards if b in available_board_ids]
            if not self.target_boards:
                self.logger.warning("⚠️  None of the target boards were found")
        else:
            # Use all boards
            self.target_boards = [b['board_id'] for b in boards]

        self.logger.info(f"✅ Discovered {len(self.target_boards)} board(s): {', '.join(self.target_boards)}")

    async def _poll_and_process_work(self):
        """Poll boards for ready work and process it"""
        self.last_poll_time = datetime.now()

        for board_id in self.target_boards:
            try:
                await self._process_board(board_id)
            except Exception as e:
                self.logger.error(f"❌ Error processing board {board_id}: {e}")

    async def _process_board(self, board_id: str):
        """Process a single board for ready work"""
        # Get next work items
        work_result = await self.kanban_service.handle_tool_call('kanban_get_next_work', {
            'board_id': board_id,
            'limit': self.max_concurrent_work * 2  # Get more than we can handle to have options
        })

        if work_result.error:
            self.logger.error(f"❌ Failed to get next work for board {board_id}: {work_result.error}")
            return

        ready_cards = work_result.result.get('cards', [])
        if not ready_cards:
            return  # No work ready

        self.logger.info(f"📋 Found {len(ready_cards)} ready ticket(s) on board {board_id}")

        # Filter out cards we've already processed
        new_cards = [card for card in ready_cards if card['card_id'] not in self.processed_cards]

        if not new_cards:
            return  # All cards already processed

        # Process cards up to the concurrency limit
        processed_count = 0
        for card in new_cards[:self.max_concurrent_work]:
            if not self.running:
                break

            try:
                await self._start_work_on_card(board_id, card)
                self.processed_cards.add(card['card_id'])
                processed_count += 1
            except Exception as e:
                self.logger.error(f"❌ Failed to start work on card {card['card_id']}: {e}")

        if processed_count > 0:
            self.logger.info(f"✅ Started work on {processed_count} ticket(s)")

    async def _start_work_on_card(self, board_id: str, card: Dict[str, Any]):
        """Start work on a specific card"""
        card_id = card['card_id']
        title = card['title']

        self.logger.info(f"🚀 Starting work on: {title} ({card_id})")

        # Move card to in_progress
        move_result = await self.kanban_service.handle_tool_call('kanban_move_card', {
            'board_id': board_id,
            'card_id': card_id,
            'column': 'in_progress',
            'moved_by': 'kanban-work-poller',
            'reason': 'Automatically started work via polling service'
        })

        if move_result.error:
            raise Exception(f"Failed to move card to in_progress: {move_result.error}")

        # Add a comment about automatic work start
        comment_result = await self.kanban_service.handle_tool_call('kanban_add_comment', {
            'board_id': board_id,
            'card_id': card_id,
            'comment': f"🤖 Work automatically started by Kanban Work Poller at {datetime.now().isoformat()}",
            'author': 'kanban-work-poller'
        })

        if comment_result.error:
            self.logger.warning(f"⚠️  Failed to add start comment: {comment_result.error}")

        # Trigger documentation automation if enabled
        if self.config.get('documentation_enabled', True):
            try:
                await self._trigger_documentation(board_id, card)
            except Exception as e:
                self.logger.error(f"❌ Documentation trigger failed: {e}")

    async def _trigger_documentation(self, board_id: str, card: Dict[str, Any]):
        """Trigger documentation automation for work start"""
        self.logger.info(f"📝 Triggering documentation for: {card['title']}")

        # Create transition data for documentation integration
        transition_data = {
            "board_id": board_id,
            "card_id": card["card_id"],
            "from_column": "ready",
            "to_column": "in_progress",
            "card_data": {
                "item_id": card["card_id"],
                "title": card["title"],
                "description": card.get("description", ""),
                "item_type": card.get("item_type", "task"),
                "assignee": card.get("assignee"),
                "repository_path": card.get("repository_path", ""),
                "tags": card.get("tags", [])
            }
        }

        # Call documentation integration
        result = await self.docs_integration.on_kanban_transition(transition_data)

        if not result.get('success', False):
            self.logger.warning(f"⚠️  Documentation trigger failed: {result.get('error', 'Unknown error')}")
        else:
            self.logger.info(f"✅ Documentation triggered for {card['title']}")

    async def get_status(self) -> Dict[str, Any]:
        """Get current status of the poller service"""
        return {
            'running': self.running,
            'last_poll_time': self.last_poll_time.isoformat() if self.last_poll_time else None,
            'poll_interval_seconds': self.poll_interval,
            'target_boards': self.target_boards,
            'processed_cards_count': len(self.processed_cards),
            'max_concurrent_work': self.max_concurrent_work,
            'config': self.config
        }

    def stop(self):
        """Stop the polling service"""
        self.logger.info("🛑 Stopping Kanban Work Poller Service...")
        self.running = False


# CLI interface
async def main():
    """CLI entry point for the Kanban Work Poller"""
    import argparse

    parser = argparse.ArgumentParser(description='Kanban Work Poller Service')
    parser.add_argument('--workspace', '-w', type=str, default='.',
                       help='Workspace path (default: current directory)')
    parser.add_argument('--poll-interval', '-i', type=int, default=30,
                       help='Poll interval in seconds (default: 30)')
    parser.add_argument('--max-concurrent', '-c', type=int, default=3,
                       help='Maximum concurrent work items (default: 3)')
    parser.add_argument('--boards', '-b', nargs='*',
                       help='Target board IDs (default: all boards)')
    parser.add_argument('--no-docs', action='store_true',
                       help='Disable documentation automation')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without actually starting work')
    parser.add_argument('--status', action='store_true',
                       help='Show service status and exit')

    args = parser.parse_args()

    workspace_path = Path(args.workspace).resolve()

    # Configuration
    config = {
        'poll_interval_seconds': args.poll_interval,
        'max_concurrent_work': args.max_concurrent,
        'target_boards': args.boards or [],
        'auto_start_work': not args.dry_run,
        'documentation_enabled': not args.no_docs,
        'log_level': 'INFO'
    }

    # Create and configure poller
    poller = KanbanWorkPoller(workspace_path, config)

    if args.status:
        # Just show status
        status = await poller.get_status()
        print("📊 Kanban Work Poller Status:")
        print(f"  Running: {status['running']}")
        print(f"  Last Poll: {status['last_poll_time'] or 'Never'}")
        print(f"  Poll Interval: {status['poll_interval_seconds']}s")
        print(f"  Target Boards: {', '.join(status['target_boards']) or 'All'}")
        print(f"  Processed Cards: {status['processed_cards_count']}")
        print(f"  Max Concurrent Work: {status['max_concurrent_work']}")
        return

    if args.dry_run:
        print("🔍 DRY RUN MODE - No actual work will be started")
        print("Configuration:")
        for key, value in config.items():
            print(f"  {key}: {value}")

    # Start the service
    try:
        await poller.start()
    except KeyboardInterrupt:
        poller.stop()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())