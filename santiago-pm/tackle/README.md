# Santiago PM Tackle

This directory contains the implementation tackle for Santiago PM functionality. Each tackle corresponds to a domain concept defined in the parent `santiago-pm/` directory specifications.

## Tackle Organization

```text
tackle/
├── status/           # Status system implementation
├── notes/            # Notes and relationships implementation
├── experiments/      # Experiment management implementation
└── [future tackle]
```

## Tackle Development Guidelines

### Code Generation Source

- **Domain Specifications**: Read from parent `santiago-pm/` directory
- **Status System**: `status/status-system.md`
- **Notes Domain**: `../notes-domain-model.md`
- **Experiments**: `../expeditions/` artifacts

### Santiago Integration

When Santiago analyzes the domain and generates code:

1. Read domain specifications from parent directory
2. Generate/update code in appropriate tackle folders
3. Maintain separation between specs and implementations

### Tackle Structure Template

Each tackle should follow this structure:

```text
tackle_name/
├── __init__.py
├── models.py        # Data models
├── services.py      # Business logic
├── api.py          # External interfaces
├── cli.py          # Command-line tools
└── tests/          # Tackle tests
```

## Current Tackle

### status/

- **Purpose**: Universal status tracking system
- **Source**: `status/status-system.md`
- **Contents**: CLI tools for querying artifact status
- **Plan**: `[STATUS] Status Tackle Development Plan`

### notes/

- **Purpose**: Notes management with relationships
- **Source**: `../notes-domain-model.md`
- **Contents**: Note storage, relationship management, queries
- **Plan**: `[NOTES] Notes Tackle Development Plan`

### experiments/

- **Purpose**: Experiment execution and management
- **Source**: `../expeditions/` artifacts
- **Contents**: Experiment runners, result processing
- **Plan**: `[EXPERIMENTS] Experiments Tackle Development Plan`
