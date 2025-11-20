#!/usr/bin/env python3
"""
Santiago Kanban Integration Demo

Simple demonstration of how the Kanban system integrates with the autonomous platform.
"""

import sys
from pathlib import Path

# Add repo root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from self_improvement.santiago_pm.tackle.kanban.kanban_service import KanbanService
from self_improvement.santiago_pm.tackle.kanban.kanban_model import ColumnType, ItemType, BoardType


def main():
    print("🚀 Santiago Kanban Integration Demo")
    print("=" * 50)

    kanban = KanbanService()
    board_id = "integration-demo"

    try:
        # 1. Create autonomous workflow board
        print("\n1. 🏗️ Creating autonomous workflow board...")
        kanban.kanban_system.create_board(
            board_id=board_id,
            board_type=BoardType.AGENT,
            name="Autonomous Development Workflow",
            description="Board for coordinating autonomous agent work"
        )
        print(f"✅ Created board: {board_id}")

        # 2. Add work items from current expeditions
        print("\n2. 📋 Adding current expeditions to backlog...")
        expeditions = [
            ("dgx-readiness-preparation", "DGX Readiness Preparation", "high", "platform-team"),
            ("neurosymbolic-domain-expert", "Neurosymbolic Domain Expert", "high", "ai-team"),
        ]

        for exp_id, title, priority, assignee in expeditions:
            card_id = kanban.add_item_to_board(
                board_id=board_id,
                item_id=exp_id,
                item_type=ItemType.EXPEDITION,
                title=title,
                repository_path=f"expeditions/{exp_id}.md",
                priority=priority,
                assignee=assignee
            )
            print(f"✅ Added: {title} ({card_id})")

        # 3. Prioritize high-priority work
        print("\n3. 🎯 Prioritizing high-priority work...")
        high_priority = kanban.kanban_system.search_cards(
            board_id=board_id,
            query="high"
        )

        for card in high_priority:
            kanban.move_card_with_validation(
                board_id=board_id,
                card_id=card["card_id"],
                new_column=ColumnType.READY,
                moved_by="prioritization-agent",
                reason="High priority expedition ready for work"
            )
            print(f"✅ Prioritized: {card['title']} → Ready")

        # 4. Show what agents would pick up next
        print("\n4. 🤖 Getting next work for AI team...")
        board = kanban.kanban_system.boards[board_id]
        ready_cards = [
            card for card in board.columns["ready"].cards
            if card.item_reference.assignee == "ai-team"
        ]

        if ready_cards:
            next_card = ready_cards[0]  # Get first ready card
            print(f"🎯 Next work: {next_card.item_reference.title}")
            print(f"   Priority: {next_card.item_reference.priority}")
            print(f"   Repository: {next_card.item_reference.repository_path}")

            # Simulate starting work
            kanban.move_card_with_validation(
                board_id=board_id,
                card_id=next_card.card_id,
                new_column=ColumnType.IN_PROGRESS,
                moved_by="ai-agent",
                reason="Starting autonomous development"
            )
            print("✅ Started work")
        else:
            print("📋 No work ready for AI team")

        # 5. Generate team visibility report
        print("\n5. 📊 Generating team report...")
        import subprocess
        import os
        os.chdir(Path(__file__).parent / "santiago-pm")

        result = subprocess.run([
            "python", "-m", "tackle.kanban.kanban_cli",
            "generate-markdown",
            "--boards", board_id,
            "--output", "integration-demo-report.md"
        ], capture_output=True, text=True, cwd=Path(__file__).parent / "santiago-pm")

        if result.returncode == 0:
            print("✅ Generated report: integration-demo-report.md")
        else:
            print(f"❌ Report generation failed: {result.stderr}")

        # 6. Show board summary
        print("\n6. 📈 Final board state:")
        summary = kanban.kanban_system.get_board_summary(board_id)
        for col_name, col_data in summary["columns"].items():
            print(f"   {col_data['title']}: {col_data['card_count']} cards")

        print("\n" + "=" * 50)
        print("✅ Integration demo completed!")
        print("\n🎯 Autonomous workflow enables:")
        print("   • Agents populate boards with discovered work")
        print("   • Collaborative prioritization with tags/comments")
        print("   • Agents query for next work items")
        print("   • Progress tracking and coordination")
        print("   • Human-visible markdown reports")

    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()