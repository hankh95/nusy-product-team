# NuSy PM Status Module

This module implements the comprehensive status tracking system for all NuSy PM artifacts as specified in `../status-system.md`.

## Features

- **Artifact Status Tracking**: Standardized status management for features, experiments, ships logs, and quality assessments
- **YAML Frontmatter Integration**: Status stored in markdown file headers
- **Status Transitions**: Enforced valid state transitions with business rules
- **Knowledge Graph Integration**: Automatic RDF triple generation for the knowledge graph
- **CLI Tools**: Command-line interface for status management
- **SPARQL Queries**: Pre-built queries for common status operations

## Installation

The module is part of the NuSy PM system. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### CLI Interface

```bash
# Create a new artifact with status
python -m nusy_pm.modules.status.status_cli create path/to/feature.md \
    --id feature-001 --type feature --assignees alice bob --labels "priority:high"

# Update artifact status
python -m nusy_pm.modules.status.status_cli update path/to/feature.md \
    --status in_progress

# Close an artifact with reason
python -m nusy_pm.modules.status.status_cli update path/to/feature.md \
    --status closed --reason completed

# Show artifact status
python -m nusy_pm.modules.status.status_cli show path/to/feature.md
```

### Python API

```python
from nusy_pm.modules.status import StatusManager, Status, StateReason

# Initialize manager
manager = StatusManager()

# Create new artifact
manager.create_new_artifact(
    "feature.md", "feature-001", "feature",
    assignees=["alice"], labels=["priority:high"]
)

# Update status
manager.update_status("feature.md", Status.IN_PROGRESS)

# Load status
status = manager.load_status_from_file("feature.md")
print(f"Status: {status.status.value}")
```

### Knowledge Graph Integration

```python
from nusy_pm.modules.status import StatusRDFConverter, StatusSPARQLQueries

# Convert status to RDF
converter = StatusRDFConverter()
status_graph = converter.status_to_rdf(artifact_status)

# Get SPARQL queries
query = StatusSPARQLQueries.find_by_status("open")
query = StatusSPARQLQueries.find_by_assignee("alice")
```

## Status Values

### Primary States

- `open`: Newly created, ready for work
- `in_progress`: Actively being worked on
- `blocked`: Waiting on dependencies or decisions
- `closed`: Final state (requires state_reason)

### Closure Reasons

- `completed`: Successfully finished
- `cancelled`: No longer needed
- `duplicate`: Superseded by another item
- `not_planned`: Decided not to implement
- `transferred`: Moved to different system

## File Format

Status is stored in YAML frontmatter of markdown files:

```yaml
---
id: feature-001
type: feature
status: in_progress
state_reason: null
created_at: 2025-11-15T10:00:00Z
updated_at: 2025-11-15T14:30:00Z
assignees: ["alice", "bob"]
labels: ["priority:high", "type:feature"]
epic: nusy-pm-core
related_experiments: []
related_artifacts: []
---

# Feature Title
Content here...
```

## Testing

Run the test suite:

```bash
python -m nusy_pm.modules.status.test_status
```

## Integration Points

This module integrates with:

- **Knowledge Graph Service**: RDF triples for semantic querying
- **CLI Tools**: Status management commands
- **Git Hooks**: Automatic timestamp updates
- **CI/CD**: Status updates based on pipeline results
- **Agent Actions**: Status updates during autonomous operations

## Architecture

- `status_model.py`: Core data models and business logic
- `status_cli.py`: Command-line interface
- `status_kg.py`: Knowledge graph integration
- `status_query.py`: Legacy query functionality (being migrated)
- `test_status.py`: Unit tests
