# NuSy PM Domain Folder Structure

## Overview

The `nusy_pm/` folder serves as the centralized domain for Product Management artifacts in the NuSy system. It follows nautical theming inspired by the Santiago ship metaphor, providing intuitive organization for autonomous agents and human developers.

## Folder Hierarchy

```
nusy_pm/
├── folder-structure.md          # This document
├── cargo-manifests/             # Feature specifications
├── ships-logs/                  # Issue tracking
├── voyage-trials/               # Experiment management
├── navigation-charts/           # Development plans
├── captains-journals/           # Knowledge capture
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

## Migration Guidelines

1. Move existing features/ to cargo-manifests/
2. Move existing issues/ to ships-logs/
3. Move existing experiments/ to voyage-trials/
4. Update all references and KG relations
5. Maintain backward compatibility links

## Agent Discovery

Santiago agents can:

- Read folder metadata for capabilities
- Navigate subfolders autonomously
- Create artifacts using templates
- Update KG relations automatically
