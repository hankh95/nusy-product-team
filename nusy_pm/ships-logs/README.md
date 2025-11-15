# Ships Logs

## Overview

Ships Logs are the issue tracking system for the NuSy Product Team. Each log represents a specific task, issue, or work item that needs to be addressed by the development team. Logs are created by agents and humans to track progress, document decisions, and maintain accountability.

## Naming Convention

Ships Logs use date-based naming with the format: `YYYY-MM-DD-[agent]-[description].md`

- **Date**: ISO format (YYYY-MM-DD) when the log was created
- **Agent**: The agent or person who created the log (e.g., `santiago`, `architect`, `developer`, `hank`)
- **Description**: Brief, kebab-case description of the issue/task

### Examples

- `2025-11-15-santiago-component-diagrams.md`
- `2025-11-15-architect-kg-schema-update.md`
- `2025-11-15-hank-experiment-review.md`
- `2025-11-15-developer-api-endpoint-fix.md`

### Multiple Logs Per Day

Different agents can create multiple logs per day. Use descriptive names to distinguish them:

- `2025-11-15-santiago-morning-standup.md`
- `2025-11-15-santiago-experiment-results.md`
- `2025-11-15-architect-knowledge-update.md`

## Log Structure

Each ships log follows a standardized template with the following sections:

### Required Sections

- **Title**: Clear, actionable description
- **Description**: Detailed explanation of the issue/task
- **Acceptance Criteria**: Specific, measurable completion conditions
- **Assignees**: Who is responsible for this log
- **Labels**: Categorization tags (type, priority, component)
- **Status**: Current state (open, in-progress, completed, blocked)

### Optional Sections

- **Tasks**: Checklist of subtasks
- **Linked PRs**: Related pull requests
- **Comments**: Additional context or discussion
- **Knowledge Graph Updates**: KG triples or concepts affected

## Status Workflow

1. **Open**: Newly created, ready for work
2. **In-Progress**: Actively being worked on
3. **Blocked**: Waiting on dependencies or decisions
4. **Completed**: All acceptance criteria met
5. **Cancelled**: No longer relevant

## Integration with Knowledge Graph

Ships Logs are automatically captured in the NuSy Knowledge Graph with relationships:

- `(log → assignee)`
- `(log → component)`
- `(log → status)`
- `(log → related_artifacts)`

## CLI Integration

Ships Logs can be managed through the NuSy PM CLI:

```bash
# Create a new ships log
nusy ships-log create --agent santiago --description "component-diagrams"

# List logs by status
nusy ships-log list --status open

# Update log status
nusy ships-log update 2025-11-15-santiago-component-diagrams.md --status completed
```

## Best Practices

1. **Atomic Logs**: Each log should represent one specific, actionable item
2. **Clear Ownership**: Always assign logs to specific agents or people
3. **Regular Updates**: Update status and add comments as work progresses
4. **Link Dependencies**: Reference related logs, features, or artifacts
5. **Knowledge Capture**: Document decisions and learnings for future reuse

## Migration from Numbered System

Existing numbered logs (001-011) will be migrated to the date-based system. The migration will:

- Convert creation dates to YYYY-MM-DD format
- Preserve original content and relationships
- Update all references in the knowledge graph
- Maintain backward compatibility through redirects
