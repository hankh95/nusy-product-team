#!/usr/bin/env python3
"""
Santiago Kanban MCP Service

MCP service wrapper for the Kanban board system, enabling autonomous agents
to manage workflow, track progress, and coordinate work through the board.
"""

import json
import asyncio
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime

from santiago_core.core.mcp_service import MCPServer, MCPTool, MCPToolResult
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "santiago-pm"))
from self_improvement.santiago_pm.tackle.kanban.kanban_service import KanbanService
from self_improvement.santiago_pm.tackle.kanban.kanban_model import ColumnType, ItemType, BoardType

# Import the neurosymbolic prioritizer
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
from domain.src.nusy_pm_core.adapters.neurosymbolic_prioritizer import NeurosymbolicPrioritizer


class SantiagoKanbanService(MCPServer):
    """MCP service for Kanban board management in Santiago Factory"""

    def __init__(self, workspace_path: Path):
        super().__init__(
            name="santiago-kanban",
            version="1.0.0",
            description="Kanban board system for workflow management and team coordination"
        )

        self.workspace_path = workspace_path
        self.kanban_service = KanbanService()
        self.prioritizer = NeurosymbolicPrioritizer(workspace_path)

        # Register tools
        self.register_tools()

    def register_tools(self):
        """Register all Kanban-related MCP tools"""

        # Board management tools
        self.register_tool(MCPTool(
            name="kanban_create_board",
            description="Create a new Kanban board",
            parameters={
                "board_id": {"type": "string", "description": "Unique board identifier"},
                "name": {"type": "string", "description": "Board display name"},
                "description": {"type": "string", "description": "Board description", "required": False}
            }
        ))

        self.register_tool(MCPTool(
            name="kanban_list_boards",
            description="List all available Kanban boards",
            parameters={}
        ))

        self.register_tool(MCPTool(
            name="kanban_get_board_summary",
            description="Get summary of a specific board",
            parameters={
                "board_id": {"type": "string", "description": "Board identifier"}
            }
        ))

        # Card management tools
        self.register_tool(MCPTool(
            name="kanban_add_card",
            description="Add a new card to a board",
            parameters={
                "board_id": {"type": "string", "description": "Target board"},
                "item_id": {"type": "string", "description": "Item identifier"},
                "title": {"type": "string", "description": "Card title"},
                "item_type": {"type": "string", "description": "Item type (expedition, feature, task, research_log, bug)", "enum": ["expedition", "feature", "task", "research_log", "bug"]},
                "repository_path": {"type": "string", "description": "Path to item in repository"},
                "description": {"type": "string", "description": "Item description", "required": False},
                "priority": {"type": "string", "description": "Priority level", "enum": ["high", "medium", "low"], "required": False},
                "assignee": {"type": "string", "description": "Assigned person/agent", "required": False}
            }
        ))

        self.register_tool(MCPTool(
            name="kanban_move_card",
            description="Move a card to a different column",
            parameters={
                "board_id": {"type": "string", "description": "Board containing the card"},
                "card_id": {"type": "string", "description": "Card to move"},
                "column": {"type": "string", "description": "Target column", "enum": ["backlog", "ready", "in_progress", "review", "done"]},
                "moved_by": {"type": "string", "description": "Person/agent performing move", "required": False},
                "reason": {"type": "string", "description": "Reason for the move", "required": False}
            }
        ))

        self.register_tool(MCPTool(
            name="kanban_search_cards",
            description="Search for cards on a board",
            parameters={
                "board_id": {"type": "string", "description": "Board to search"},
                "query": {"type": "string", "description": "Text search query", "required": False},
                "item_type": {"type": "string", "description": "Filter by item type", "enum": ["expedition", "feature", "task", "research_log", "bug"], "required": False},
                "assignee": {"type": "string", "description": "Filter by assignee", "required": False}
            }
        ))

        # Comment and tagging tools
        self.register_tool(MCPTool(
            name="kanban_add_comment",
            description="Add a comment to a card",
            parameters={
                "board_id": {"type": "string", "description": "Board containing the card"},
                "card_id": {"type": "string", "description": "Card to comment on"},
                "comment": {"type": "string", "description": "Comment text"},
                "author": {"type": "string", "description": "Comment author", "required": False}
            }
        ))

        self.register_tool(MCPTool(
            name="kanban_add_tags",
            description="Add tags to a card",
            parameters={
                "board_id": {"type": "string", "description": "Target board"},
                "card_id": {"type": "string", "description": "Card to tag"},
                "tags": {"type": "array", "description": "Tags to add", "items": {"type": "string"}}
            }
        ))

        # Workflow intelligence tools
        self.register_tool(MCPTool(
            name="kanban_get_next_work",
            description="Get highest priority work ready to be started",
            parameters={
                "board_id": {"type": "string", "description": "Board to query"},
                "assignee": {"type": "string", "description": "Filter by assignee", "required": False},
                "limit": {"type": "integer", "description": "Maximum number of items to return", "required": False, "default": 5}
            }
        ))

        self.register_tool(MCPTool(
            name="kanban_get_blocked_items",
            description="Get all blocked items that need attention",
            parameters={
                "board_id": {"type": "string", "description": "Board to query"}
            }
        ))

        self.register_tool(MCPTool(
            name="kanban_get_team_workload",
            description="Get current workload distribution across team members",
            parameters={
                "board_id": {"type": "string", "description": "Board to analyze"}
            }
        ))

        # Intelligent prioritization tools
        self.register_tool(MCPTool(
            name="kanban_prioritize_backlog",
            description="Use neurosymbolic AI to intelligently prioritize the entire backlog",
            parameters={
                "board_id": {"type": "string", "description": "Board to prioritize"},
                "context": {"type": "object", "description": "Context for prioritization", "required": False}
            }
        ))

        self.register_tool(MCPTool(
            name="kanban_prioritize_item",
            description="Calculate intelligent priority score for a specific item",
            parameters={
                "item": {"type": "object", "description": "Item to prioritize with id, title, etc."},
                "context": {"type": "object", "description": "Context for prioritization", "required": False}
            }
        ))

        self.register_tool(MCPTool(
            name="kanban_close_issue",
            description="Close an issue when work is completed (moves card to done and marks issue closed)",
            parameters={
                "board_id": {"type": "string", "description": "Board containing the card"},
                "card_id": {"type": "string", "description": "Card/issue to close"},
                "closed_by": {"type": "string", "description": "Person/agent closing the issue", "required": False},
                "close_reason": {"type": "string", "description": "Reason for closing", "required": False}
            }
        ))

    async def handle_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> MCPToolResult:
        """Handle MCP tool calls for Kanban operations"""

        try:
            if tool_name == "kanban_create_board":
                return await self._handle_create_board(parameters)
            elif tool_name == "kanban_list_boards":
                return await self._handle_list_boards(parameters)
            elif tool_name == "kanban_get_board_summary":
                return await self._handle_get_board_summary(parameters)
            elif tool_name == "kanban_add_card":
                return await self._handle_add_card(parameters)
            elif tool_name == "kanban_move_card":
                return await self._handle_move_card(parameters)
            elif tool_name == "kanban_search_cards":
                return await self._handle_search_cards(parameters)
            elif tool_name == "kanban_add_comment":
                return await self._handle_add_comment(parameters)
            elif tool_name == "kanban_add_tags":
                return await self._handle_add_tags(parameters)
            elif tool_name == "kanban_get_next_work":
                return await self._handle_get_next_work(parameters)
            elif tool_name == "kanban_get_blocked_items":
                return await self._handle_get_blocked_items(parameters)
            elif tool_name == "kanban_get_team_workload":
                return await self._handle_get_team_workload(parameters)
            elif tool_name == "kanban_generate_markdown_report":
                return await self._handle_generate_markdown_report(parameters)
            elif tool_name == "kanban_prioritize_backlog":
                return await self._handle_prioritize_backlog(parameters)
            elif tool_name == "kanban_prioritize_item":
                return await self._handle_prioritize_item(parameters)
            elif tool_name == "kanban_get_dgx_readiness_priorities":
                return await self._handle_dgx_readiness_priorities(parameters)
            elif tool_name == "kanban_close_issue":
                return await self._handle_close_issue(parameters)
            else:
                return MCPToolResult(error=f"Unknown tool: {tool_name}")

        except Exception as e:
            return MCPToolResult(error=f"Error executing {tool_name}: {str(e)}")

    async def _handle_create_board(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle board creation"""
        board_id = self.kanban_service.kanban_system.create_board(
            board_id=params["board_id"],
            board_type=BoardType.AGENT,  # Default to agent board
            name=params["name"],
            description=params.get("description", "")
        )
        return MCPToolResult(result={"board_id": board_id, "status": "created"})

    async def _handle_list_boards(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle board listing"""
        boards = []
        for board_id, board in self.kanban_service.kanban_system.boards.items():
            boards.append({
                "board_id": board_id,
                "name": board.name,
                "type": board.board_type.value,
                "description": board.description
            })
        return MCPToolResult(result={"boards": boards})

    async def _handle_get_board_summary(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle board summary retrieval"""
        summary = self.kanban_service.kanban_system.get_board_summary(params["board_id"])
        if "error" in summary:
            return MCPToolResult(error=summary["error"])
        return MCPToolResult(result=summary)

    async def _handle_add_card(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle card addition"""
        card_id = self.kanban_service.add_item_to_board(
            board_id=params["board_id"],
            item_id=params["item_id"],
            item_type=ItemType(params["item_type"]),
            title=params["title"],
            repository_path=params["repository_path"],
            description=params.get("description", ""),
            priority=params.get("priority", "medium"),
            assignee=params.get("assignee")
        )
        return MCPToolResult(result={"card_id": card_id, "status": "added"})

    async def _handle_move_card(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle card movement"""
        result = self.kanban_service.move_card_with_validation(
            board_id=params["board_id"],
            card_id=params["card_id"],
            new_column=ColumnType(params["column"]),
            moved_by=params.get("moved_by", "mcp-service"),
            reason=params.get("reason")
        )
        return MCPToolResult(result=result)

    async def _handle_search_cards(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle card search"""
        item_type = ItemType(params["item_type"]) if params.get("item_type") else None
        results = self.kanban_service.kanban_system.search_cards(
            board_id=params["board_id"],
            query=params.get("query", ""),
            item_type=item_type,
            assignee=params.get("assignee")
        )
        return MCPToolResult(result={"cards": results})

    async def _handle_add_comment(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle comment addition"""
        success = self.kanban_service.add_comment_to_card(
            board_id=params["board_id"],
            card_id=params["card_id"],
            comment_text=params["comment"],
            author=params.get("author", "mcp-service")
        )
        return MCPToolResult(result={"success": success})

    async def _handle_add_tags(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle tag addition"""
        # Find the card and add tags
        board = self.kanban_service.kanban_system.boards.get(params["board_id"])
        if not board:
            return MCPToolResult(error=f"Board {params['board_id']} not found")

        card = None
        for column in board.columns.values():
            for c in column.cards:
                if c.card_id == params["card_id"]:
                    card = c
                    break
            if card:
                break

        if not card:
            return MCPToolResult(error=f"Card {params['card_id']} not found")

        # Add new tags
        for tag in params["tags"]:
            if tag not in card.tags:
                card.tags.append(tag)

        board.updated_at = datetime.now()
        self.kanban_service.kanban_system._save_boards()

        return MCPToolResult(result={"success": True, "tags_added": params["tags"]})

    async def _handle_get_next_work(self, params: Dict[str, Any]) -> MCPToolResult:
        """Get highest priority work ready to be started"""
        board = self.kanban_service.kanban_system.boards.get(params["board_id"])
        if not board:
            return MCPToolResult(error=f"Board {params['board_id']} not found")

        ready_column = board.columns.get("ready")
        if not ready_column:
            return MCPToolResult(result={"cards": []})

        # Sort by priority and position
        priority_order = {"high": 0, "medium": 1, "low": 2}
        cards = sorted(
            ready_column.cards,
            key=lambda c: (
                priority_order.get(c.item_reference.priority, 1),
                c.position
            )
        )

        # Filter by assignee if specified
        if params.get("assignee"):
            cards = [c for c in cards if c.item_reference.assignee == params["assignee"]]

        # Limit results
        limit = params.get("limit", 5)
        cards = cards[:limit]

        result_cards = []
        for card in cards:
            result_cards.append({
                "card_id": card.card_id,
                "title": card.item_reference.title,
                "item_type": card.item_reference.item_type.value,
                "priority": card.item_reference.priority,
                "assignee": card.item_reference.assignee,
                "repository_path": card.item_reference.repository_path,
                "description": card.item_reference.description,
                "tags": card.tags,
                "comments": [{"content": c.content, "author": c.author, "created_at": c.created_at.isoformat()} for c in card.comments]
            })

        return MCPToolResult(result={"cards": result_cards})

    async def _handle_get_blocked_items(self, params: Dict[str, Any]) -> MCPToolResult:
        """Get all blocked items"""
        blocked = self.kanban_service.find_blocked_cards(params["board_id"])
        return MCPToolResult(result={"blocked_cards": blocked})

    async def _handle_get_team_workload(self, params: Dict[str, Any]) -> MCPToolResult:
        """Get team workload distribution"""
        metrics = self.kanban_service.get_board_metrics(params["board_id"])
        if "error" in metrics:
            return MCPToolResult(error=metrics["error"])

        # Group by assignee
        assignee_work = {}
        for card in metrics.get("all_cards", []):
            assignee = card.get("assignee", "unassigned")
            if assignee not in assignee_work:
                assignee_work[assignee] = {"total": 0, "by_column": {}}

            assignee_work[assignee]["total"] += 1
            column = card.get("column", "unknown")
            assignee_work[assignee]["by_column"][column] = assignee_work[assignee]["by_column"].get(column, 0) + 1

        return MCPToolResult(result={"team_workload": assignee_work})

    async def _handle_prioritize_backlog(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle intelligent backlog prioritization"""
        board_id = params["board_id"]
        context = params.get("context", {})

        # Get all items from the board
        board = self.kanban_service.kanban_system.boards.get(board_id)
        if not board:
            return MCPToolResult(error=f"Board {board_id} not found")

        # Convert Kanban cards to prioritizer format
        backlog_items = []
        for column in board.columns.values():
            for card in column.cards:
                item = {
                    'id': card.card_id,
                    'title': card.item_reference.title,
                    'type': card.item_reference.item_type.value,
                    'description': card.item_reference.description or "",
                    'estimated_effort': 5,  # Default effort
                    'blocked_by': [],  # TODO: Add dependency tracking
                    'blocks': [],  # TODO: Add dependency tracking
                    'required_skills': [],  # TODO: Add skill requirements
                    'customer_value_hint': 0.5,  # Default
                    'learning_value_hint': 0.5,  # Default
                }
                backlog_items.append(item)

        # Prioritize using neurosymbolic engine
        results = self.prioritizer.prioritize_backlog(backlog_items, context)

        # Format results
        prioritized_items = []
        for result in results:
            prioritized_items.append({
                'rank': len(prioritized_items) + 1,
                'item_id': result.item_id,
                'title': next((item['title'] for item in backlog_items if item['id'] == result.item_id), ""),
                'priority_score': result.priority_score,
                'category': result.category,
                'rationale': result.rationale,
                'factors': {
                    'customer_value': result.factors.customer_value,
                    'unblock_impact': result.factors.unblock_impact,
                    'worker_availability': result.factors.worker_availability,
                    'learning_value': result.factors.learning_value
                }
            })

        return MCPToolResult(result={"prioritized_backlog": prioritized_items})

    async def _handle_prioritize_item(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle single item prioritization"""
        item = params["item"]
        context = params.get("context", {})

        result = self.prioritizer.calculate_priority(item, context)

        return MCPToolResult(result={
            'item_id': result.item_id,
            'priority_score': result.priority_score,
            'category': result.category,
            'rationale': result.rationale,
            'factors': {
                'customer_value': result.factors.customer_value,
                'unblock_impact': result.factors.unblock_impact,
                'worker_availability': result.factors.worker_availability,
                'learning_value': result.factors.learning_value
            }
        })

    async def _handle_dgx_readiness_priorities(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle DGX readiness prioritization"""
        board_id = params["board_id"]

        # Create DGX-focused context
        dgx_context = {
            'available_workers': [
                {'skills': ['infrastructure', 'deployment', 'dgx'], 'capacity_remaining': 1.0},
                {'skills': ['ai', 'ml', 'training'], 'capacity_remaining': 0.8},
                {'skills': ['platform', 'devops'], 'capacity_remaining': 0.9},
                {'skills': ['testing', 'qa'], 'capacity_remaining': 0.7}
            ],
            'hypotheses': [
                {'related_to': 'dgx-readiness', 'confidence': 0.95},  # High confidence for DGX work
                {'related_to': 'infrastructure', 'confidence': 0.90},
                {'related_to': 'deployment', 'confidence': 0.85}
            ]
        }

        # Get all items and enhance with DGX readiness factors
        board = self.kanban_service.kanban_system.boards.get(board_id)
        if not board:
            return MCPToolResult(error=f"Board {board_id} not found")

        backlog_items = []
        for column in board.columns.values():
            for card in column.cards:
                item = {
                    'id': card.card_id,
                    'title': card.item_reference.title,
                    'type': card.item_reference.item_type.value,
                    'description': card.item_reference.description or "",
                    'estimated_effort': 5,
                    'blocked_by': [],
                    'blocks': [],
                    'required_skills': self._infer_skills_from_title(card.item_reference.title),
                    # Boost customer value for DGX-related items
                    'customer_value_hint': self._calculate_dgx_customer_value(card),
                    'learning_value_hint': 0.5,
                }
                backlog_items.append(item)

        # Prioritize with DGX context
        results = self.prioritizer.prioritize_backlog(backlog_items, dgx_context)

        # Format results with DGX readiness focus
        dgx_priorities = []
        for result in results:
            dgx_readiness = self._assess_dgx_readiness(result.item_id, board)
            dgx_priorities.append({
                'rank': len(dgx_priorities) + 1,
                'item_id': result.item_id,
                'title': next((item['title'] for item in backlog_items if item['id'] == result.item_id), ""),
                'priority_score': result.priority_score,
                'category': result.category,
                'rationale': result.rationale,
                'dgx_readiness': dgx_readiness,
                'factors': {
                    'customer_value': result.factors.customer_value,
                    'unblock_impact': result.factors.unblock_impact,
                    'worker_availability': result.factors.worker_availability,
                    'learning_value': result.factors.learning_value
                }
            })

        return MCPToolResult(result={"dgx_priorities": dgx_priorities})

    def _infer_skills_from_title(self, title: str) -> List[str]:
        """Infer required skills from item title"""
        title_lower = title.lower()
        skills = []

        if any(word in title_lower for word in ['dgx', 'gpu', 'infrastructure', 'deployment']):
            skills.extend(['infrastructure', 'deployment'])
        if any(word in title_lower for word in ['ai', 'ml', 'training', 'model']):
            skills.extend(['ai', 'ml'])
        if any(word in title_lower for word in ['platform', 'devops', 'scaling']):
            skills.extend(['platform', 'devops'])
        if any(word in title_lower for word in ['test', 'qa', 'validation']):
            skills.extend(['testing', 'qa'])

        return list(set(skills))  # Remove duplicates

    def _calculate_dgx_customer_value(self, card) -> float:
        """Calculate customer value with DGX readiness bias"""
        title_lower = card.item_reference.title.lower()
        description_lower = (card.item_reference.description or "").lower()

        # High value for DGX-critical items
        dgx_keywords = ['dgx', 'gpu', 'infrastructure', 'deployment', 'scaling', 'performance']
        if any(keyword in title_lower or keyword in description_lower for keyword in dgx_keywords):
            return 0.95  # Critical for DGX readiness

        # Medium value for platform/infrastructure items
        platform_keywords = ['platform', 'devops', 'monitoring', 'reliability']
        if any(keyword in title_lower or keyword in description_lower for keyword in platform_keywords):
            return 0.75

        # Default medium value
        return 0.5

    def _assess_dgx_readiness(self, item_id: str, board) -> Dict[str, Any]:
        """Assess how this item contributes to DGX readiness"""
        # Find the card
        card = None
        for column in board.columns.values():
            for c in column.cards:
                if c.card_id == item_id:
                    card = c
                    break
            if card:
                break

        if not card:
            return {"readiness_level": "unknown", "blocks_dgx": False}

        title_lower = card.item_reference.title.lower()
        desc_lower = (card.item_reference.description or "").lower()

        # Critical DGX blockers
        if any(word in title_lower or word in desc_lower for word in
               ['dgx deployment', 'gpu setup', 'infrastructure ready', 'scaling test']):
            return {"readiness_level": "critical", "blocks_dgx": True, "timeline": "immediate"}

        # Important for DGX success
        if any(word in title_lower or word in desc_lower for word in
               ['performance', 'monitoring', 'reliability', 'platform']):
            return {"readiness_level": "important", "blocks_dgx": False, "timeline": "week1"}

        # Nice to have
        return {"readiness_level": "nice_to_have", "blocks_dgx": False, "timeline": "post_dgx"}

    async def _handle_close_issue(self, params: Dict[str, Any]) -> MCPToolResult:
        """Handle issue closing by moving card to done column"""
        try:
            # Move card to done column
            result = self.kanban_service.move_card_with_validation(
                board_id=params["board_id"],
                card_id=params["card_id"],
                new_column=ColumnType.DONE,
                moved_by=params.get("closed_by", "santiago-developer"),
                reason=params.get("close_reason", "Work completed following full development workflow")
            )

            # Add a completion comment
            self.kanban_service.add_comment_to_card(
                board_id=params["board_id"],
                card_id=params["card_id"],
                comment_text=f"✅ Issue closed by {params.get('closed_by', 'santiago-developer')}. {params.get('close_reason', 'Work completed successfully.')}",
                author=params.get("closed_by", "santiago-developer")
            )

            return MCPToolResult(result={
                "success": True,
                "card_id": params["card_id"],
                "moved_to": "done",
                "closed_by": params.get("closed_by", "santiago-developer")
            })

        except Exception as e:
            return MCPToolResult(error=f"Failed to close issue {params['card_id']}: {str(e)}")


# Service entry point
async def main():
    """Main entry point for the Kanban MCP service"""
    import sys
    workspace_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    service = SantiagoKanbanService(workspace_path)
    await service.start()


if __name__ == "__main__":
    asyncio.run(main())