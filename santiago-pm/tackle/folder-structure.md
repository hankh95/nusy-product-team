# Santiago Repository Folder Structure

## Overview

The repository implements a **two-namespace model** separating production domain code from self-improvement system code:

- **`domain/`**: Production code implementing the core business domain
- **`self-improvement/`**: Code implementing the autonomous self-improvement capabilities

The `santiago-pm/` folder serves as the canonical scaffold for self-improvement artifacts, following nautical theming inspired by the Santiago ship metaphor.

## Repository Structure

```text
repository/
├── domain/                      # Production domain code
│   ├── features/               # Feature implementations
│   ├── models/                 # Domain models
│   ├── services/               # Business services
│   └── tests/                  # Domain tests
├── self-improvement/           # Self-improvement system
│   ├── santiago-pm/           # Canonical PM scaffold
│   ├── santiago-dev/          # Development tools
│   └── agents/                # Agent implementations
├── docs/                       # Documentation
├── _archive/                   # Historical artifacts
└── [infrastructure files]      # Root-level config files
```

## Two-Namespace Model

### domain/ (Production Domain)

Contains all code that implements the core business functionality:

- **Purpose**: Deliver business value and domain capabilities
- **Contents**: Production-ready features, models, services
- **Testing**: Full test coverage, CI/CD integration
- **Stability**: High stability requirements

### self-improvement/ (Self-Improvement System)

Contains code that implements autonomous improvement capabilities:

- **Purpose**: Enable the system to improve itself autonomously
- **Contents**: PM scaffold, development agents, experimentation tools
- **Testing**: Experimental validation, rapid iteration
- **Stability**: Lower stability requirements, experimental features

## Santiago-PM Scaffold Structure

```text
santiago-pm/
├── folder-structure.md          # This document (moved to tackle/)
├── notes-domain-model.md        # Notes domain specification
├── status-system.md             # Universal status system spec (moved to tackle/status/)
├── status_query.py              # [DEPRECATED: moved to modules/]
├── cargo-manifests/             # Feature specifications
├── ships-logs/                  # Issue tracking
├── voyage-trials/               # Experiment management
├── navigation-charts/           # Development plans
├── captains-journals/           # Knowledge capture
├── expeditions/                 # Experiment artifacts
├── modules/                     # Implementation modules
└── crew-standards.md            # Agent naming standards
```

## Subfolder Purposes

### cargo-manifests/ (Cargo Manifests)

- **Purpose**: Feature specifications and requirements
- **Nautical Meaning**: What the ship carries and delivers
- **Contents**: Feature files, acceptance criteria, user stories
- **KG Integration**: Links to issues and experiments

### ships-logs/ (Ship's Logs)

- **Purpose**: Issue tracking and problem resolution
- **Nautical Meaning**: Daily records of events and problems
- **Contents**: Issue reports, bug tracking, incident logs
- **KG Integration**: Links to features and commits

### voyage-trials/ (Voyage Trials)

- **Purpose**: Experiment management and testing
- **Nautical Meaning**: Testing new routes and capabilities
- **Contents**: Experiment plans, results, trial data
- **KG Integration**: Links to features and success metrics

### navigation-charts/ (Navigation Charts)

- **Purpose**: Development planning and roadmapping
- **Nautical Meaning**: Maps for planning journeys
- **Contents**: Development plans, milestones, timelines
- **KG Integration**: Links to all PM artifacts

### captains-journals/ (Captain's Journals)

- **Purpose**: Knowledge capture and insights
- **Nautical Meaning**: Personal reflections and discoveries
- **Contents**: Notes, learnings, research findings
- **KG Integration**: Core knowledge graph nodes

### modules/ (Implementation Modules)

- **Purpose**: Code implementations of domain concepts
- **Contents**: Python modules corresponding to domain specifications
- **Organization**: Each module implements specs from parent directory
- **Santiago Integration**: Target for autonomous code generation

### tackle/ (Implementation Tackle)

- **Purpose**: Code implementations of domain concepts
- **Nautical Meaning**: Ship's equipment and rigging for implementation
- **Contents**: Python tackle corresponding to domain specifications
- **Organization**: Each tackle implements specs from parent directory
- **Santiago Integration**: Target for autonomous code generation

## Naming Conventions

All artifacts follow the format: `[Nautical Type] - [Descriptive Title]`

Examples:

- `Cargo Manifest - User Authentication`
- `Ship's Log - API Timeout Issues`
- `Voyage Trial - Multi-Agent Collaboration`

## KG Integration

Each subfolder contains:

- `.metadata.json`: Agent-readable folder information
- Templates with KG relation definitions
- Automatic relation establishment on artifact creation

## Migration Status

**Current State**: Repository transitioning to two-namespace model

**Completed**:

- Architecture vision and migration plan documented
- Root artifact triage report generated
- Expedition infrastructure established

**In Progress**:

- Folder structure documentation updates
- Namespace separation planning

**Pending**:

- Physical directory restructuring
- Import/reference updates
- Test reorganization

## Agent Discovery

Santiago agents can:

- Read folder metadata for capabilities
- Navigate subfolders autonomously
- Create artifacts using templates
- Update KG relations automatically
- Distinguish between domain/ and self-improvement/ contexts
