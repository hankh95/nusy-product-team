# NuSy PM Status System

## Overview

All NuSy PM artifacts (features, ships logs, experiments, etc.) use a standardized status system that enables querying and tracking across the entire system. Status is stored as semantic triples in YAML frontmatter headers.

## Status Values

### Primary States

- **open**: Newly created, ready for work
- **in_progress**: Actively being worked on
- **blocked**: Waiting on dependencies or decisions
- **closed**: Final state (see reasons below)

### Closed State Reasons

When an item reaches "closed" status, it must include a `state_reason`:

- **completed**: Successfully finished all acceptance criteria
- **cancelled**: No longer needed or relevant
- **duplicate**: Superseded by another item
- **not_planned**: Decided not to implement
- **transferred**: Moved to different system/tracking

## YAML Frontmatter Format

```yaml
---
id: feature-001
type: feature
status: in_progress
state_reason: null  # Only set when status is "closed"
created_at: 2025-11-15T10:00:00Z
updated_at: 2025-11-15T14:30:00Z
assignees: ["santiago", "architect"]
labels: ["type:feature", "priority:high"]
epic: nusy-pm-core
related_experiments: []
related_artifacts: []
---

# Feature Title
```

## Semantic Triples

Status information is automatically converted to knowledge graph triples:

```
(feature-001, hasStatus, in_progress)
(feature-001, hasStateReason, null)
(feature-001, createdAt, 2025-11-15T10:00:00Z)
(feature-001, updatedAt, 2025-11-15T14:30:00Z)
(feature-001, hasAssignee, santiago)
(feature-001, hasAssignee, architect)
(feature-001, hasLabel, type:feature)
(feature-001, hasLabel, priority:high)
(feature-001, belongsToEpic, nusy-pm-core)
```

## Querying Status

### CLI Queries
```bash
# Find all open features
nusy query status --type feature --status open

# Find features by assignee
nusy query status --assignee santiago

# Find completed items this month
nusy query status --status closed --state-reason completed --since 2025-11-01
```

### Knowledge Graph Queries (SPARQL)
```sparql
# Find all in-progress features
SELECT ?feature WHERE {
  ?feature rdf:type :Feature .
  ?feature :hasStatus "in_progress" .
}

# Find features assigned to Santiago
SELECT ?feature WHERE {
  ?feature :hasAssignee "santiago" .
}
```

## Status Transition Rules

1. **Creation**: All new items start with `status: open`
2. **Assignment**: Can move to `in_progress` when work begins
3. **Blocking**: Can be marked `blocked` with explanation
4. **Completion**: Must move to `closed` with appropriate `state_reason`
5. **No Deletion**: Items are never deleted, only closed

## Integration Points

### Services That Query Status
- **Feature Service**: Tracks feature implementation status
- **Experiment Service**: Monitors experiment progress
- **Ships Logs Service**: Issue tracking and resolution
- **Quality Assessment Service**: Review and validation status
- **Knowledge Graph Service**: Ontology and schema status

### Automatic Updates
- **Git Hooks**: Update timestamps on file changes
- **CI/CD**: Update status based on pipeline results
- **Agent Actions**: Update status as work progresses
- **CLI Commands**: Manual status updates

## Status Dashboard

The system provides status dashboards:

```bash
# Overall project status
nusy dashboard status

# Feature completion burndown
nusy dashboard features --burndown

# Agent productivity metrics
nusy dashboard agents --productivity
```

## Migration

Existing files without status will be automatically assigned `status: open` during migration. Closed items from external systems will be imported with appropriate `state_reason` values.
