#!/usr/bin/env python3
"""
Kanban Board Regenerator

Automatically regenerates the kanban-boards.md file every 10 minutes
with the latest data from the kanban system.
"""

import asyncio
import logging
import sys
import time
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Add santiago-pm to path for kanban imports
sys.path.insert(0, str(project_root / "santiago-pm"))

def generate_kanban_markdown():
    """Generate the kanban-boards.md file with current data"""
    try:
        from tackle.kanban.kanban_service import KanbanService

        kanban_service = KanbanService()
        board_id = "master_board"

        # Get board data
        board_data = kanban_service.kanban_system.get_board_summary(board_id)
        if "error" in board_data:
            print(f"Error getting board data: {board_data['error']}")
            return

        # Get metrics
        metrics = kanban_service.get_board_metrics(board_id)

        # Generate markdown content
        markdown_content = generate_markdown_content(board_data, metrics)

        # Write to file
        output_path = project_root / "kanban-boards.md"
        with open(output_path, 'w') as f:
            f.write(markdown_content)

        print(f"Kanban board regenerated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"Error regenerating kanban board: {e}")

def generate_markdown_content(board_data, metrics):
    """Generate the markdown content for the kanban board"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    content = f"""# 🏗️ Santiago Project Kanban Boards

## Unified workflow tracking for the entire Santiago ecosystem

**Board ID:** `master_board` | **Type:** master

## Master Board - Overall Project Priorities

### Work Columns

| **AI Team Work** *{metrics.get('ai_team_count', 0)} cards* | **Platform Team Work** *{metrics.get('platform_team_count', 0)} cards* | **Product Team Work** *{metrics.get('product_team_count', 0)} cards* | **Research** *{metrics.get('research_count', 0)} cards* |
|:---:|:---:|:---:|:---:|
"""

    # Get columns data
    columns = board_data.get('columns', {})

    # Find the maximum number of rows needed
    max_rows = max(len(col.get('cards', [])) for col in columns.values()) if columns else 0

    # Build table rows
    for i in range(max_rows):
        row = "| "
        for col_name in ['ai_team', 'platform_team', 'product_team', 'research']:
            col_data = columns.get(col_name, {})
            cards = col_data.get('cards', [])

            if i < len(cards):
                card = cards[i]
                title = card.get('title', 'Unknown')
                item_type = card.get('item_type', 'task')
                priority = card.get('priority', 'medium')
                assignee = card.get('assignee', '')

                # Format priority emoji
                priority_emoji = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(priority, '⚪')

                # Format assignee
                assignee_str = f" 👤 {assignee}" if assignee else ""

                cell_content = f"**{title}** *{item_type}*{assignee_str} {priority_emoji} {priority}"
            else:
                cell_content = "   "

            row += cell_content + " | "

        content += row.rstrip() + "\n"

    # Add DGX readiness section
    content += """

### 🎯 Ready for DGX Deployment (High Priority)

- **🚀 Mistral LLM Integration** - Load real LLM for production use
- **🚀 DGX Provisioning Automation** - Configure DGX hardware
- **🚀 DGX Readiness Preparation** - Final deployment preparation

### 📊 Active Work Metrics

- **Total Active Work:** {total_cards} items
- **Santiago Agents:** 7 (3 PM, 2 Architect, 2 Developer)
- **Work in Progress:** All items assigned and active
- **Expected Completion:** 8-12 items in next 16 hours

---

## 👥 Human Task Board

*Tasks available for human contributors and collaborators*

**Board ID:** `human-tasks` | **Type:** human-work

### Board Columns

| **Available Tasks** *6 cards* | **In Progress** *0 cards* | **Review** *0 cards* | **Completed** *0 cards* |
|:---:|:---:|:---:|:---:|
| **📝 Documentation Review** *Review and improve project docs* |   |   |   |
| **🧪 Manual Testing** *Test new features manually* |   |   |   |
| **🎨 UI/UX Design** *Design user interfaces* |   |   |   |
| **📊 Data Analysis** *Analyze system performance data* |   |   |   |
| **🤝 Stakeholder Communication** *Coordinate with external parties* |   |   |   |
| **🔧 DevOps Support** *Infrastructure and deployment help* |   |   |   |

### 💡 How to Pick Up Tasks

**As a human contributor, you can:**

1. **Check this board** for tasks you can help with
2. **Claim a task** by commenting on the card
3. **Move to "In Progress"** when you start working
4. **Move to "Review"** when ready for feedback
5. **Move to "Completed"** when done

**Current Status:** All tasks available - pick what interests you!

---

## 📝 How to Use

This file shows the complete project status across all boards.

### 🤖 For Santiago Agents (Autonomous Work)
- **Master Board**: Overall project priorities and planning
- **Active Development**: Current autonomous work in progress
- **Kanban Rules**: Move cards through Ready → In Progress → Review → Done

### 👥 For Human Contributors
- **Human Task Board**: Tasks suitable for human involvement
- **Claim tasks** by adding comments and moving to "In Progress"
- **Collaborate** with autonomous agents on complex tasks

### 📊 Board Management
```bash
# View all boards
cd santiago-pm && python -m tackle.kanban.kanban_cli list-boards

# Show specific board
cd santiago-pm && python -m tackle.kanban.kanban_cli show-board master_board

# Move cards between columns
cd santiago-pm && python -m tackle.kanban.kanban_cli move-card master_board "Task Name" ready
```

---

*Generated by Santiago PM Kanban System on {timestamp}*
*Auto-regenerated every 10 minutes*
"""

    return content

async def main():
    """Main regeneration loop"""
    print("Starting Kanban Board Regenerator - will update every 10 minutes")

    while True:
        generate_kanban_markdown()
        await asyncio.sleep(600)  # 10 minutes = 600 seconds

if __name__ == "__main__":
    asyncio.run(main())