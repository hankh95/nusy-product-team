#!/usr/bin/env python3
"""
Santiago Kanban Workflow Demo

Demonstrates how autonomous agents can use the Kanban system for:
1. Populating the board with work items
2. Prioritizing work collaboratively
3. Getting next work items to execute
4. Tracking progress and coordination
"""

import asyncio
import sys
from pathlib import Path
from datetime import datetime

# Set PYTHONPATH for imports
repo_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(repo_root))

from self_improvement.santiago_pm.tackle.kanban.kanban_service import KanbanService
from self_improvement.santiago_pm.tackle.kanban.kanban_model import ColumnType, ItemType, BoardType


class SantiagoKanbanWorkflowDemo:
    """Demo of autonomous Kanban workflow management"""

    def __init__(self):
        self.kanban = KanbanService()
        self.board_id = "autonomous-workflow-demo"

    async def setup_demo_board(self):
        """Create a demo board for the autonomous workflow"""
        print("🏗️ Setting up autonomous workflow board...")

        # Create the board
        self.kanban.kanban_system.create_board(
            board_id=self.board_id,
            board_type=BoardType.AGENT,
            name="Autonomous Development Workflow",
            description="Demo board showing autonomous work prioritization and execution"
        )

        # Add a swimlane for different work types
        self.kanban.add_swimlane(
            board_id=self.board_id,
            swimlane_id="core-platform",
            name="Core Platform Development",
            wip_limit=3
        )

        self.kanban.add_swimlane(
            board_id=self.board_id,
            swimlane_id="ai-agents",
            name="AI Agent Development",
            wip_limit=2
        )

        print(f"✅ Created board: {self.board_id}")

    async def populate_backlog_from_expeditions(self):
        """Populate backlog from current expeditions"""
        print("\n📋 Populating backlog from expeditions...")

        expeditions = [
            {
                "id": "dgx-readiness-preparation",
                "title": "DGX Readiness Preparation",
                "description": "Prepare infrastructure for DGX deployment and scaling",
                "priority": "high",
                "assignee": "platform-team"
            },
            {
                "id": "neurosymbolic-domain-expert",
                "title": "Neurosymbolic Domain Expert",
                "description": "Build neurosymbolic AI agent for domain expertise",
                "priority": "high",
                "assignee": "ai-team"
            },
            {
                "id": "santiago-core-self-management",
                "title": "Santiago Core Self-Management",
                "description": "Enable Santiago agents to manage themselves autonomously",
                "priority": "medium",
                "assignee": "ai-team"
            }
        ]

        for exp in expeditions:
            card_id = self.kanban.add_item_to_board(
                board_id=self.board_id,
                item_id=exp["id"],
                item_type=ItemType.EXPEDITION,
                title=exp["title"],
                repository_path=f"expeditions/{exp['id']}.md",
                description=exp["description"],
                priority=exp["priority"],
                assignee=exp["assignee"]
            )

            # Assign to appropriate swimlane
            swimlane_id = "core-platform" if "platform" in exp["assignee"] else "ai-agents"
            self.kanban.assign_card_to_swimlane(self.board_id, card_id, swimlane_id)

            print(f"✅ Added expedition: {exp['title']} ({card_id})")

    async def demonstrate_prioritization_workflow(self):
        """Show how agents would prioritize work collaboratively"""
        print("\n🎯 Demonstrating prioritization workflow...")

        # Move high priority items to Ready
        high_priority_cards = self.kanban.kanban_system.search_cards(
            board_id=self.board_id,
            assignee="ai-team"
        )

        for card in high_priority_cards:
            if card["priority"] == "high":
                self.kanban.move_card_with_validation(
                    board_id=self.board_id,
                    card_id=card["card_id"],
                    new_column=ColumnType.READY,
                    moved_by="prioritization-agent",
                    reason="High priority item ready for development"
                )
                print(f"✅ Prioritized: {card['title']} → Ready")

        # Add some comments and tags to show collaboration
        if high_priority_cards:
            first_card = high_priority_cards[0]
            self.kanban.add_comment_to_card(
                self.board_id,
                first_card["card_id"],
                "This expedition is critical for Phase 2 deployment. Coordinate with platform team.",
                "santiago-pm"
            )

            # Add tags
            board = self.kanban.kanban_system.boards[self.board_id]
            card_obj = None
            for col in board.columns.values():
                for c in col.cards:
                    if c.card_id == first_card["card_id"]:
                        card_obj = c
                        break
                if card_obj:
                    break

            if card_obj:
                card_obj.tags.extend(["#critical-path", "@platform-team", "!high"])
                board.updated_at = datetime.now()
                self.kanban.kanban_system._save_boards()
                print(f"✅ Added collaboration tags to: {first_card['title']}")

    async def show_work_assignment_workflow(self):
        """Show how agents would get next work items"""
        print("\n👷 Demonstrating work assignment workflow...")

        # Simulate an agent getting next work
        next_work = self._get_next_work_for_agent("ai-team")

        if next_work:
            print(f"🤖 AI Team next work: {next_work['title']}")
            print(f"   Priority: {next_work['priority']}")
            print(f"   Repository: {next_work['repository_path']}")
            print(f"   Tags: {', '.join(next_work.get('tags', []))}")

            # Simulate starting work
            self.kanban.move_card_with_validation(
                board_id=self.board_id,
                card_id=next_work["card_id"],
                new_column=ColumnType.IN_PROGRESS,
                moved_by="ai-agent",
                reason="Starting autonomous development work"
            )
            print(f"✅ Started work on: {next_work['title']}")
        else:
            print("🤖 AI Team: No work ready")

    def _get_next_work_for_agent(self, assignee: str) -> dict:
        """Get next work item for a specific agent"""
        board = self.kanban.kanban_system.boards.get(self.board_id)
        if not board:
            return None

        ready_column = board.columns.get("ready")
        if not ready_column:
            return None

        # Find highest priority work for this assignee
        priority_order = {"high": 0, "medium": 1, "low": 2}

        candidate_cards = [
            card for card in ready_column.cards
            if card.item_reference.assignee == assignee
        ]

        if not candidate_cards:
            return None

        # Sort by priority, then by position
        next_card = min(
            candidate_cards,
            key=lambda c: (
                priority_order.get(c.item_reference.priority, 1),
                c.position
            )
        )

        return {
            "card_id": next_card.card_id,
            "title": next_card.item_reference.title,
            "priority": next_card.item_reference.priority,
            "repository_path": next_card.item_reference.repository_path,
            "assignee": next_card.item_reference.assignee,
            "tags": next_card.tags,
            "description": next_card.item_reference.description
        }

    async def demonstrate_progress_tracking(self):
        """Show progress tracking and completion"""
        print("\n📈 Demonstrating progress tracking...")

        # Find in-progress work
        board = self.kanban.kanban_system.boards.get(self.board_id)
        in_progress_column = board.columns.get("in_progress")

        if in_progress_column and in_progress_column.cards:
            card = in_progress_column.cards[0]

            # Add progress comment
            self.kanban.add_comment_to_card(
                self.board_id,
                card.card_id,
                "Completed initial analysis and created implementation plan. Ready for review.",
                "ai-agent"
            )

            # Move to review
            self.kanban.move_card_with_validation(
                board_id=self.board_id,
                card_id=card.card_id,
                new_column=ColumnType.REVIEW,
                moved_by="ai-agent",
                reason="Completed development work, ready for review"
            )

            print(f"✅ Completed work on: {card.item_reference.title}")
            print("   Moved to Review column for quality assurance")

    async def generate_team_report(self):
        """Generate a markdown report for team visibility"""
        print("\n📊 Generating team progress report...")

        # Generate markdown report
        import subprocess
        import os

        os.chdir(Path(__file__).parent.parent.parent / "self_improvement" / "santiago_pm")
        result = subprocess.run([
            "python", "-m", "tackle.kanban.kanban_cli",
            "generate-markdown",
            "--boards", self.board_id,
            "--output", "autonomous-workflow-report.md"
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Generated team report: autonomous-workflow-report.md")
        else:
            print(f"❌ Failed to generate report: {result.stderr}")

    async def show_query_examples(self):
        """Show examples of querying the board for different purposes"""
        print("\n🔍 Demonstrating board queries...")

        # Find all blocked items
        blocked = self.kanban.find_blocked_cards(self.board_id)
        print(f"🚫 Blocked items: {len(blocked)}")

        # Search for high priority items
        high_priority = self.kanban.kanban_system.search_cards(
            board_id=self.board_id,
            query="high"
        )
        print(f"🔴 High priority items: {len(high_priority)}")

        # Get team workload
        metrics = self.kanban.get_board_metrics(self.board_id)
        print("👥 Team workload:")
        for assignee, count in metrics.get("cards_by_assignee", {}).items():
            print(f"   {assignee}: {count} items")

    async def run_full_demo(self):
        """Run the complete autonomous workflow demo"""
        print("🚀 Starting Santiago Kanban Autonomous Workflow Demo")
        print("=" * 60)

        try:
            await self.setup_demo_board()
            await self.populate_backlog_from_expeditions()
            await self.demonstrate_prioritization_workflow()
            await self.show_work_assignment_workflow()
            await self.demonstrate_progress_tracking()
            await self.generate_team_report()
            await self.show_query_examples()

            print("\n" + "=" * 60)
            print("✅ Demo completed successfully!")
            print("\n🎯 Key takeaways:")
            print("   • Kanban system enables autonomous work coordination")
            print("   • Agents can populate, prioritize, and execute work independently")
            print("   • Rich metadata (tags, comments, assignees) enables collaboration")
            print("   • Markdown reports provide human-readable progress visibility")
            print("   • MCP service integration allows programmatic access")

        except Exception as e:
            print(f"\n❌ Demo failed: {e}")
            import traceback
            traceback.print_exc()


async def main():
    """Main demo entry point"""
    demo = SantiagoKanbanWorkflowDemo()
    await demo.run_full_demo()


if __name__ == "__main__":
    asyncio.run(main())