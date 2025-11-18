#!/usr/bin/env python3
"""
Kanban Knowledge Graph Integration

Integrates the Kanban board system with Santiago-PM's knowledge graph
for advanced querying, relationships, and insights.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import asdict

from .kanban_model import UnifiedKanbanSystem, KanbanBoard, KanbanCard, ItemReference, ColumnType, ItemType
from .kanban_service import KanbanService


class KanbanKnowledgeGraph:
    """
    Knowledge graph integration for Kanban board system.

    Provides semantic indexing, relationship mapping, and advanced querying
    capabilities for the Kanban board data.
    """

    def __init__(self, kanban_service: KanbanService, kg_path: Optional[Path] = None):
        """
        Initialize knowledge graph integration.

        Args:
            kanban_service: The Kanban service instance
            kg_path: Path to knowledge graph storage (optional)
        """
        self.service = kanban_service
        self.kg_path = kg_path or Path("knowledge-graph")
        self.kg_path.mkdir(exist_ok=True)

        # Knowledge graph storage
        self.nodes_file = self.kg_path / "kanban_nodes.json"
        self.edges_file = self.kg_path / "kanban_edges.json"
        self.index_file = self.kg_path / "kanban_index.json"

        # In-memory knowledge graph
        self.nodes: Dict[str, Dict] = {}
        self.edges: List[Dict] = []
        self.index: Dict[str, Set[str]] = {}

        # Load existing knowledge graph
        self._load_knowledge_graph()

    def _load_knowledge_graph(self):
        """Load existing knowledge graph from disk."""
        try:
            if self.nodes_file.exists():
                with open(self.nodes_file, 'r') as f:
                    self.nodes = json.load(f)

            if self.edges_file.exists():
                with open(self.edges_file, 'r') as f:
                    self.edges = json.load(f)

            if self.index_file.exists():
                with open(self.index_file, 'r') as f:
                    # Convert lists back to sets
                    self.index = {k: set(v) for k, v in json.load(f).items()}

        except (json.JSONDecodeError, FileNotFoundError):
            # Initialize empty knowledge graph
            self.nodes = {}
            self.edges = []
            self.index = {}

    def _save_knowledge_graph(self):
        """Save knowledge graph to disk."""
        # Convert sets to lists for JSON serialization
        index_serializable = {k: list(v) for k, v in self.index.items()}

        with open(self.nodes_file, 'w') as f:
            json.dump(self.nodes, f, indent=2, default=str)

        with open(self.edges_file, 'w') as f:
            json.dump(self.edges, f, indent=2, default=str)

        with open(self.index_file, 'w') as f:
            json.dump(index_serializable, f, indent=2, default=str)

    def index_board(self, board_id: str):
        """
        Index a board and all its cards in the knowledge graph.

        Args:
            board_id: The board to index
        """
        if board_id not in self.service.kanban_system.boards:
            raise ValueError(f"Board not found: {board_id}")

        board = self.service.kanban_system.boards[board_id]

        # Index the board itself
        self._index_board_node(board)

        # Index all cards
        for column in board.columns.values():
            for card in column.cards:
                self._index_card_node(card, board_id)

        # Create relationships
        self._create_board_relationships(board)

        # Update search index
        self._update_search_index(board)

        # Save changes
        self._save_knowledge_graph()

    def _index_board_node(self, board: KanbanBoard):
        """Index a board as a knowledge graph node."""
        node_id = f"board:{board.board_id}"

        self.nodes[node_id] = {
            "id": node_id,
            "type": "board",
            "board_id": board.board_id,
            "board_type": board.board_type.value,
            "name": board.name,
            "description": board.description,
            "created_at": board.created_at.isoformat(),
            "updated_at": board.updated_at.isoformat(),
            "column_count": len(board.columns),
            "card_count": sum(len(col.cards) for col in board.columns.values()),
            "labels": ["kanban", "board", board.board_type.value]
        }

    def _index_card_node(self, card: KanbanCard, board_id: str):
        """Index a card as a knowledge graph node."""
        node_id = f"card:{card.card_id}"

        # Extract metadata from item reference
        metadata = {}
        if card.item_reference:
            metadata = {
                "item_id": card.item_reference.item_id,
                "item_type": card.item_reference.item_type.value,
                "repository_path": card.item_reference.repository_path,
                "description": card.item_reference.description,
                "priority": card.item_reference.priority,
                "assignee": card.item_reference.assignee,
                "labels": card.item_reference.labels or []
            }

        self.nodes[node_id] = {
            "id": node_id,
            "type": "card",
            "card_id": card.card_id,
            "board_id": board_id,
            "title": card.item_reference.title,
            "column": card.column.value,
            "created_at": card.created_at.isoformat(),
            "moved_at": card.moved_at.isoformat() if card.moved_at else None,
            "blocked": card.blocked_reason is not None,
            "blocked_reason": card.blocked_reason,
            "labels": ["kanban", "card", card.column.value] + (card.item_reference.labels or []),
            "item_id": card.item_reference.item_id,
            "item_type": card.item_reference.item_type.value,
            "repository_path": card.item_reference.repository_path,
            "description": card.item_reference.description,
            "priority": card.item_reference.priority,
            "assignee": card.item_reference.assignee
        }

    def _create_board_relationships(self, board: KanbanBoard):
        """Create relationships between board and cards."""
        board_node_id = f"board:{board.board_id}"

        for column in board.columns.values():
            for card in column.cards:
                card_node_id = f"card:{card.card_id}"

                # Board contains card
                self.edges.append({
                    "source": board_node_id,
                    "target": card_node_id,
                    "relationship": "contains",
                    "properties": {
                        "column": card.column.value,
                        "created_at": datetime.now().isoformat()
                    }
                })

                # Card belongs to board
                self.edges.append({
                    "source": card_node_id,
                    "target": board_node_id,
                    "relationship": "belongs_to",
                    "properties": {
                        "column": card.column.value,
                        "created_at": datetime.now().isoformat()
                    }
                })

                # Create item reference relationships
                if card.item_reference.repository_path:
                    item_node_id = f"item:{card.item_reference.item_id}"
                    self.edges.append({
                        "source": card_node_id,
                        "target": item_node_id,
                        "relationship": "references",
                        "properties": {
                            "path": card.item_reference.repository_path,
                            "type": card.item_reference.item_type.value,
                            "created_at": datetime.now().isoformat()
                        }
                    })

    def _update_search_index(self, board: KanbanBoard):
        """Update the search index with board content."""
        # Index board by name and description
        board_text = f"{board.name} {board.description}".lower()
        for word in board_text.split():
            if len(word) > 2:  # Skip very short words
                self.index.setdefault(word, set()).add(f"board:{board.board_id}")

        # Index cards by title, description, and assignee
        for column in board.columns.values():
            for card in column.cards:
                card_text = f"{card.item_reference.title} {card.item_reference.description or ''}".lower()
                assignee = card.item_reference.assignee.lower() if card.item_reference.assignee else ""

                for text in [card_text, assignee]:
                    for word in text.split():
                        if len(word) > 2:
                            self.index.setdefault(word, set()).add(f"card:{card.card_id}")

    def search_knowledge_graph(self, query: str, node_type: Optional[str] = None) -> List[Dict]:
        """
        Search the knowledge graph for nodes matching the query.

        Args:
            query: Search query string
            node_type: Optional filter for node type ("board", "card", etc.)

        Returns:
            List of matching nodes
        """
        query_words = query.lower().split()
        candidate_nodes = set()

        # Find nodes containing any of the query words
        for word in query_words:
            if word in self.index:
                candidate_nodes.update(self.index[word])

        # Filter by node type if specified
        results = []
        for node_id in candidate_nodes:
            if node_id in self.nodes:
                node = self.nodes[node_id]
                if node_type is None or node.get("type") == node_type:
                    results.append(node)

        return results

    def get_related_nodes(self, node_id: str, relationship: Optional[str] = None,
                         direction: str = "both") -> List[Dict]:
        """
        Get nodes related to the given node.

        Args:
            node_id: The node to find relationships for
            relationship: Optional relationship type filter
            direction: "incoming", "outgoing", or "both"

        Returns:
            List of related nodes with relationship info
        """
        related = []

        for edge in self.edges:
            include_edge = False

            if direction in ["outgoing", "both"] and edge["source"] == node_id:
                include_edge = True
                related_node_id = edge["target"]
                rel_direction = "outgoing"

            if direction in ["incoming", "both"] and edge["target"] == node_id:
                include_edge = True
                related_node_id = edge["source"]
                rel_direction = "incoming"

            if include_edge and (relationship is None or edge["relationship"] == relationship):
                if related_node_id in self.nodes:
                    related.append({
                        "node": self.nodes[related_node_id],
                        "relationship": edge["relationship"],
                        "direction": rel_direction,
                        "properties": edge.get("properties", {})
                    })

        return related

    def get_board_insights(self, board_id: str) -> Dict[str, Any]:
        """
        Generate insights about a board using knowledge graph analysis.

        Args:
            board_id: The board to analyze

        Returns:
            Dictionary with various insights
        """
        board_node_id = f"board:{board_id}"
        if board_node_id not in self.nodes:
            raise ValueError(f"Board not indexed: {board_id}")

        board_node = self.nodes[board_node_id]
        related_cards = self.get_related_nodes(board_node_id, "contains")

        insights = {
            "board_info": board_node,
            "card_count": len(related_cards),
            "cards_by_column": {},
            "cards_by_type": {},
            "cards_by_assignee": {},
            "blocked_cards": [],
            "high_priority_cards": [],
            "recent_moves": []
        }

        for card_rel in related_cards:
            card = card_rel["node"]

            # Count by column
            column = card.get("column", "unknown")
            insights["cards_by_column"][column] = insights["cards_by_column"].get(column, 0) + 1

            # Count by type
            item_type = card.get("item_type", "unknown")
            insights["cards_by_type"][item_type] = insights["cards_by_type"].get(item_type, 0) + 1

            # Count by assignee
            assignee = card.get("assignee", "unassigned")
            insights["cards_by_assignee"][assignee] = insights["cards_by_assignee"].get(assignee, 0) + 1

            # Track blocked cards
            if card.get("blocked"):
                insights["blocked_cards"].append(card)

            # Track high priority cards
            if card.get("priority") == "high":
                insights["high_priority_cards"].append(card)

            # Track recent moves (simplified - would need move history)
            if card.get("moved_at"):
                insights["recent_moves"].append(card)

        return insights

    def find_dependencies(self, card_id: str) -> List[Dict]:
        """
        Find dependencies and related items for a card.

        Args:
            card_id: The card to analyze

        Returns:
            List of dependent items
        """
        card_node_id = f"card:{card_id}"
        if card_node_id not in self.nodes:
            return []

        # Get referenced item
        referenced_items = self.get_related_nodes(card_node_id, "references")

        dependencies = []

        for item_rel in referenced_items:
            item_node = item_rel["node"]
            item_path = item_node.get("path", "")

            # Find other cards that reference the same item
            related_cards = self.get_related_nodes(item_node["id"], "references", "incoming")

            for rel_card in related_cards:
                if rel_card["node"]["id"] != card_node_id:
                    dependencies.append({
                        "dependent_card": rel_card["node"],
                        "relationship": "shares_item",
                        "shared_item": item_node
                    })

        return dependencies

    def get_workflow_patterns(self, board_id: str) -> Dict[str, Any]:
        """
        Analyze workflow patterns in a board.

        Args:
            board_id: The board to analyze

        Returns:
            Dictionary with workflow pattern analysis
        """
        insights = self.get_board_insights(board_id)

        patterns = {
            "bottlenecks": [],
            "work_distribution": insights["cards_by_assignee"],
            "type_distribution": insights["cards_by_type"],
            "column_distribution": insights["cards_by_column"],
            "blockage_rate": len(insights["blocked_cards"]) / max(1, insights["card_count"]),
            "recommendations": []
        }

        # Identify bottlenecks (columns with high card counts)
        max_cards_per_column = max(insights["cards_by_column"].values()) if insights["cards_by_column"] else 0
        for column, count in insights["cards_by_column"].items():
            if count > max_cards_per_column * 0.7:  # Top 30% of column sizes
                patterns["bottlenecks"].append({
                    "column": column,
                    "card_count": count,
                    "percentage": count / insights["card_count"] if insights["card_count"] > 0 else 0
                })

        # Generate recommendations
        if patterns["blockage_rate"] > 0.2:
            patterns["recommendations"].append("High blockage rate detected - review blocked items")

        if len(patterns["bottlenecks"]) > 0:
            patterns["recommendations"].append("Consider redistributing work from bottleneck columns")

        unbalanced_assignees = [a for a, c in patterns["work_distribution"].items()
                              if c > insights["card_count"] * 0.3]  # More than 30% of work
        if unbalanced_assignees:
            patterns["recommendations"].append(f"Work distribution uneven - consider balancing load for: {', '.join(unbalanced_assignees)}")

        return patterns

    def export_knowledge_graph(self, format: str = "json") -> str:
        """
        Export the knowledge graph in the specified format.

        Args:
            format: Export format ("json" or "graphml")

        Returns:
            String representation of the knowledge graph
        """
        if format == "json":
            return json.dumps({
                "nodes": list(self.nodes.values()),
                "edges": self.edges,
                "metadata": {
                    "exported_at": datetime.now().isoformat(),
                    "node_count": len(self.nodes),
                    "edge_count": len(self.edges)
                }
            }, indent=2, default=str)

        elif format == "graphml":
            # Basic GraphML export
            graphml = '<?xml version="1.0" encoding="UTF-8"?>\n'
            graphml += '<graphml xmlns="http://graphml.graphdrawing.org/xmlns">\n'

            # Define node attributes
            graphml += '  <key id="type" for="node" attr.name="type" attr.type="string"/>\n'
            graphml += '  <key id="name" for="node" attr.name="name" attr.type="string"/>\n'

            # Define edge attributes
            graphml += '  <key id="relationship" for="edge" attr.name="relationship" attr.type="string"/>\n'

            graphml += '  <graph id="kanban" edgedefault="directed">\n'

            # Add nodes
            for node in self.nodes.values():
                node_id = node["id"].replace(":", "_")  # GraphML doesn't like colons
                node_name = node.get("name") or node.get("title") or node["id"]
                node_type = node["type"]

                graphml += f'    <node id="{node_id}">\n'
                graphml += f'      <data key="type">{node_type}</data>\n'
                graphml += f'      <data key="name">{node_name}</data>\n'
                graphml += '    </node>\n'

            # Add edges
            for i, edge in enumerate(self.edges):
                source_id = edge["source"].replace(":", "_")
                target_id = edge["target"].replace(":", "_")
                relationship = edge["relationship"]

                graphml += f'    <edge id="e{i}" source="{source_id}" target="{target_id}">\n'
                graphml += f'      <data key="relationship">{relationship}</data>\n'
                graphml += '    </edge>\n'

            graphml += '  </graph>\n'
            graphml += '</graphml>\n'

            return graphml

        else:
            raise ValueError(f"Unsupported export format: {format}")