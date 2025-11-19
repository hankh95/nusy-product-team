#!/usr/bin/env python3
"""
Santiago Autonomous Development Team Runner

This script initializes and runs the Santiago autonomous development team.
"""

import asyncio
import logging
import sys
import argparse
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import sys
from pathlib import Path

# Add the santiago_core directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from santiago_core.core.team_coordinator import SantiagoTeamCoordinator
from santiago_core.core.agent_framework import Task


async def main(continuous=False, max_agents=3, assign_all_features=False):
    """Main entry point for the Santiago autonomous development team"""
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    logger = logging.getLogger("santiago-runner")
    logger.info("Starting Santiago Autonomous Development Team")

    # Initialize the team coordinator
    workspace_path = project_root
    coordinator = SantiagoTeamCoordinator(workspace_path)

    try:
        # Initialize the team
        init_task = asyncio.create_task(coordinator.initialize_team())

        # Wait a bit for initialization
        await asyncio.sleep(2)

        if assign_all_features:
            # Load all features from kanban board and assign them
            logger.info("Assigning all features from kanban board...")
            await _assign_features_from_kanban(coordinator, project_root)

        # Create and assign a demo task only if not assigning all features
        if not assign_all_features:
            await coordinator.create_demo_task()

        if continuous:
            logger.info("Team is now active. Running continuously...")
            # Run indefinitely with kanban regeneration every 10 minutes
            kanban_regeneration_counter = 0
            while True:
                await asyncio.sleep(60)  # Check every minute
                kanban_regeneration_counter += 1
                
                # Regenerate kanban board every 10 minutes (600 seconds = 10 minutes)
                if kanban_regeneration_counter >= 10:
                    await _regenerate_kanban_board(project_root)
                    kanban_regeneration_counter = 0
        else:
            # Let the team run for a limited time (30 seconds for testing)
            logger.info("Team is now active. Running for 30 seconds...")

            # Run for 30 seconds then shutdown
            await asyncio.sleep(30)

            logger.info("Test run completed, shutting down...")
            await coordinator.shutdown_team()

    except Exception as e:
        logger.error(f"Error running Santiago team: {e}")
        await coordinator.shutdown_team()
        sys.exit(1)


async def _assign_features_from_kanban(coordinator, workspace_path):
    """Assign features from the kanban board to agents"""
    try:
        # Import the kanban service
        from santiago_core.services.kanban_service import SantiagoKanbanService
        
        # Initialize kanban service
        kanban_service = SantiagoKanbanService(workspace_path)
        
        # Get the master board (where the high priority items are)
        board_id = "master_board"
        
        # Get next work items (ready to be started)
        next_work_result = await kanban_service.handle_tool_call("kanban_get_next_work", {
            "board_id": board_id,
            "limit": 10  # Get up to 10 highest priority items
        })
        
        if next_work_result.error:
            print(f"Failed to get next work: {next_work_result.error}")
            return
        
        ready_cards = next_work_result.result.get("cards", [])
        print(f"Found {len(ready_cards)} ready work items")
        
        # Assign each ready card to the appropriate agent
        for card in ready_cards:
            await _assign_kanban_card_to_agent(coordinator, card)
            
    except Exception as e:
        print(f"Error assigning features from kanban: {e}")


async def _regenerate_kanban_board(workspace_path):
    """Regenerate the kanban board markdown file"""
    try:
        from datetime import datetime
        import os
        
        # Import the kanban service
        from santiago_core.services.kanban_service import SantiagoKanbanService
        
        # Initialize kanban service
        kanban_service = SantiagoKanbanService(workspace_path)
        
        # Get board data
        board_id = "master_board"
        board_summary = await kanban_service.handle_tool_call("kanban_get_board_summary", {"board_id": board_id})
        
        if board_summary.error:
            print(f"Failed to get board summary: {board_summary.error}")
            return
        
        # Get next work items
        next_work = await kanban_service.handle_tool_call("kanban_get_next_work", {
            "board_id": board_id,
            "limit": 20
        })
        
        # Generate markdown content
        markdown_content = await _generate_kanban_markdown(board_summary.result, next_work.result if not next_work.error else {"cards": []})
        
        # Write to file
        kanban_file_path = os.path.join(workspace_path, "kanban-boards.md")
        with open(kanban_file_path, 'w') as f:
            f.write(markdown_content)
        
        print(f"Kanban board regenerated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"Error regenerating kanban board: {e}")


async def _assign_kanban_card_to_agent(coordinator, card):
    """Assign a kanban card to the appropriate agent"""
    try:
        # Create a task from the card data
        task = Task(
            id=card["card_id"],
            title=card["title"],
            description=card.get("description", f"Work on {card['title']}"),
            priority=card.get("priority", "medium"),
            assignee=card.get("assignee"),
            item_type=card.get("item_type", "feature")
        )
        
        # Assign to coordinator which will route to appropriate agent
        await coordinator.assign_task(task)
        print(f"Assigned kanban card '{card['title']}' to agent")
        
    except Exception as e:
        print(f"Error assigning kanban card {card.get('card_id', 'unknown')}: {e}")
async def _generate_kanban_markdown(board_summary, next_work_data):
    """Generate markdown content for kanban boards"""
    from datetime import datetime
    
    # Extract data from the kanban service responses
    board_data = board_summary if board_summary else {}
    next_work_cards = next_work_data.get('cards', []) if next_work_data else []
    
    # Count cards by assignee and type
    ai_cards = [c for c in next_work_cards if c.get('assignee') == 'ai-team']
    platform_cards = [c for c in next_work_cards if c.get('assignee') == 'platform-team']
    product_cards = [c for c in next_work_cards if c.get('assignee') == 'product-team']
    research_cards = [c for c in next_work_cards if c.get('item_type') == 'research']
    
    # Get total work count from board summary
    total_cards = 0
    if 'columns' in board_data:
        for column_data in board_data['columns'].values():
            total_cards += column_data.get('card_count', 0)
    
    markdown = f"""# Santiago Kanban Boards

## Unified workflow tracking for the entire Santiago ecosystem

**Board ID:** `master_board` | **Type:** master

## Current autonomous work in progress - Santiago agents actively working

**Board ID:** `noesis-active` | **Type:** active-work

### Work Columns

| **AI Team Work** *{len(ai_cards)} cards* | **Platform Team Work** *{len(platform_cards)} cards* | **Product Team Work** *{len(product_cards)} cards* | **Research** *{len(research_cards)} cards* |
|:---:|:---:|:---:|:---:|
"""
    
    # Add work items to the table
    ai_items = [c for c in next_work_data.get('cards', []) if c.get('assignee') == 'ai-team'][:5]
    platform_items = [c for c in next_work_data.get('cards', []) if c.get('assignee') == 'platform-team'][:5]
    product_items = [c for c in next_work_data.get('cards', []) if c.get('assignee') == 'product-team'][:5]
    research_items = [c for c in next_work_data.get('cards', []) if c.get('item_type') == 'research'][:5]
    
    max_rows = max(len(ai_items), len(platform_items), len(product_items), len(research_items))
    
    for i in range(max_rows):
        ai_item = ai_items[i] if i < len(ai_items) else {}
        platform_item = platform_items[i] if i < len(platform_items) else {}
        product_item = product_items[i] if i < len(product_items) else {}
        research_item = research_items[i] if i < len(research_items) else {}
        
        ai_cell = f"**🔄 {ai_item.get('title', '')}** *{ai_item.get('item_type', '')}*" if ai_item else ""
        platform_cell = f"**🔄 {platform_item.get('title', '')}** *{platform_item.get('item_type', '')}*" if platform_item else ""
        product_cell = f"**🔄 {product_item.get('title', '')}** *{product_item.get('item_type', '')}*" if product_item else ""
        research_cell = f"**🔄 {research_item.get('title', '')}** *{research_item.get('item_type', '')}*" if research_item else ""
        
        markdown += f"| {ai_cell} | {platform_cell} | {product_cell} | {research_cell} |\n"
    
    # Add ready items section
    ready_items = []
    if 'columns' in board_data and 'ready' in board_data['columns']:
        ready_cards = board_data['columns']['ready'].get('cards', [])
        for card in ready_cards[:3]:  # Show top 3 ready items
            ready_items.append(f"- **🚀 {card.get('title', '')}** - {card.get('description', '')}")
    
    if ready_items:
        markdown += "\n### 🎯 Ready for DGX Deployment (High Priority)\n\n"
        markdown += "\n".join(ready_items)
        markdown += "\n"
    else:
        markdown += "\n### 🎯 Ready for DGX Deployment (High Priority)\n\n"
        markdown += "- No items currently ready for deployment\n"
    
    markdown += f"""

### 📊 Active Work Metrics

- **Total Active Work:** {total_cards} items
- **Santiago Agents:** 7 (3 PM, 2 Architect, 2 Developer)
- **Work in Progress:** All items assigned and active
- **Expected Completion:** 8-12 items in next 16 hours

---

## 👥 Human Task Board

## Tasks available for human contributors and collaborators

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

*Generated by Santiago PM Kanban System on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
    
    return markdown


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run Santiago Autonomous Development Team')
    parser.add_argument('--continuous', action='store_true', help='Run continuously instead of for 30 seconds')
    parser.add_argument('--max-agents', type=int, default=3, help='Maximum number of agents (default: 3)')
    parser.add_argument('--assign-all-features', action='store_true', help='Assign all features from kanban board')

    args = parser.parse_args()
    asyncio.run(main(continuous=args.continuous, max_agents=args.max_agents, assign_all_features=args.assign_all_features))