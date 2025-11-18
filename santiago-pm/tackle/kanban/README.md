# Santiago PM Kanban Board System

A unified workflow tracking system that serves as the single source of truth for all project work across the Santiago ecosystem.

## Overview

The Kanban board system provides hierarchical workflow management with linked references, eliminating data duplication while maintaining a unified view of all project work. It integrates with Santiago-PM's QA and knowledge graph systems for comprehensive project coordination.

## Features

- **Hierarchical Boards**: Master boards for overall coordination, agent boards for individual work
- **Linked References**: Cards reference repository items without duplication
- **Workflow Validation**: Automated validation of workflow transitions
- **Knowledge Graph Integration**: Semantic indexing and advanced querying
- **CLI Interface**: Command-line access for human developers and autonomous agents
- **Metrics and Insights**: Comprehensive analytics and bottleneck detection
- **Bulk Operations**: Efficient handling of multiple cards
- **Export Capabilities**: Data export in JSON and GraphML formats

## Architecture

```
santiago-pm/tackle/kanban/
├── __init__.py           # Package exports
├── kanban_model.py       # Core data models
├── kanban_service.py     # Business logic layer
├── kanban_cli.py         # Command-line interface
└── kanban_kg.py          # Knowledge graph integration
```

## Quick Start

### Command Line Usage

```bash
# Create a new board
kanban create-board my-project "My Project Board" --description "Main project workflow"

# Add a card to the board
kanban add-card my-project feature-123 "Implement user authentication" \
  --path "features/auth.feature" \
  --type feature \
  --priority high \
  --assignee "santiago-dev"

# Move a card through workflow
kanban move-card my-project card-001 in-progress --moved-by "developer"

# View board status
kanban show-board my-project

# Get board metrics
kanban metrics my-project

# Search for cards
kanban search my-project --query "authentication" --assignee "santiago-dev"
```

### Python API Usage

```python
from santiago_pm.tackle.kanban import KanbanService, ItemType, ColumnType

# Initialize service
service = KanbanService()

# Create a board
board_id = service.kanban_system.create_board(
    board_id="my-project",
    board_type="agent",
    name="My Project Board",
    description="Main project workflow"
)

# Add a card
card_id = service.add_item_to_board(
    board_id=board_id,
    item_id="feature-123",
    item_type=ItemType.FEATURE,
    title="Implement user authentication",
    repository_path="features/auth.feature",
    priority="high",
    assignee="santiago-dev"
)

# Move card through workflow
result = service.move_card_with_validation(
    board_id=board_id,
    card_id=card_id,
    new_column=ColumnType.IN_PROGRESS,
    moved_by="developer"
)

# Get board insights
insights = service.get_board_metrics(board_id)
```

## Board Types

### Master Boards
- Coordinate work across multiple agents
- Provide high-level project oversight
- Support complex workflow dependencies

### Agent Boards
- Individual agent workflow management
- Local task prioritization
- Integration with personal productivity systems

## Workflow States

The system supports standard Kanban workflow columns:

- **Backlog**: Items ready for work
- **Ready**: Items approved and prioritized
- **In Progress**: Currently being worked on
- **Review**: Items under review/QA
- **Done**: Completed items

## Item Types

- **Feature**: New functionality or capabilities
- **Bug**: Defect or issue resolution
- **Task**: General work item
- **Epic**: Large work item broken into smaller tasks
- **Expedition**: Complex multi-step initiative

## Knowledge Graph Integration

The system integrates with Santiago-PM's knowledge graph for advanced capabilities:

```python
from santiago_pm.tackle.kanban import KanbanKnowledgeGraph

# Initialize knowledge graph integration
kg = KanbanKnowledgeGraph(service)

# Index a board
kg.index_board("my-project")

# Search across all indexed content
results = kg.search_knowledge_graph("authentication")

# Get workflow insights
insights = kg.get_board_insights("my-project")

# Find dependencies
dependencies = kg.find_dependencies("card-001")

# Analyze workflow patterns
patterns = kg.get_workflow_patterns("my-project")
```

## Validation Rules

The system enforces workflow validation:

- Cards can only move forward in the workflow
- WIP limits prevent column overload
- Blocked cards require resolution before movement
- Dependencies must be satisfied
- Role-based permissions control operations

## Metrics and Analytics

Comprehensive metrics are available:

- Card counts by column, type, priority, and assignee
- Workflow velocity and cycle time
- Bottleneck identification
- Blockage rate analysis
- Work distribution analysis

## Export and Integration

Export capabilities for integration with other tools:

```python
# Export board data
json_data = service.export_board_data("my-project", "json")

# Export knowledge graph
graphml_data = kg.export_knowledge_graph("graphml")
```

## Configuration

The system uses YAML configuration files for board templates and validation rules. Default configurations are provided for common workflows.

## Integration Points

- **Santiago-PM QA**: Automated quality assurance for workflow compliance
- **Santiago-Core**: Complex reasoning for workflow optimization
- **Santiago-Dev**: Autonomous task execution and git integration
- **Knowledge Graph**: Semantic indexing and relationship mapping

## Development

### Testing

```bash
# Run unit tests
python -m pytest tests/

# Run integration tests
python -m pytest tests/integration/
```

### Adding New Features

1. Define the feature in a Gherkin file
2. Implement in the appropriate module
3. Add CLI commands if needed
4. Update knowledge graph indexing
5. Add tests and documentation

## Troubleshooting

### Common Issues

**Board not found**: Ensure the board ID is correct and the board exists
**Card movement blocked**: Check validation rules and resolve blocking conditions
**Knowledge graph empty**: Run indexing after creating boards and cards

### Logs

Check the following log files:
- `logs/kanban_service.log`: Service operations
- `logs/kanban_cli.log`: CLI operations
- `knowledge-graph/`: Knowledge graph data

## Contributing

Follow the Santiago-PM development workflow:

1. Create a feature branch
2. Add cards to the appropriate Kanban board
3. Implement with tests
4. Submit for QA review
5. Merge when approved

## License

Part of the Santiago autonomous development ecosystem.