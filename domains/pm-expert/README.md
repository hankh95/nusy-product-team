# PM Domain Expert System

This directory contains the complete Product Management (PM) domain expert system for Santiago's autonomous multi-agent platform.

## Overview

The PM Domain Expert provides comprehensive knowledge and capabilities for product management, including:

- Agile methodologies (Scrum, Kanban, XP)
- Lean UX and continuous discovery
- User story mapping and discovery practices
- Team management and coordination
- Risk assessment and mitigation
- Stakeholder communication

## Directory Structure

```
pm-expert/
├── knowledge-sources/       # Source material for PM knowledge
│   ├── jeff-patton/        # User story mapping, discovery practices
│   ├── jeff-gothelf/       # Lean UX, continuous discovery
│   └── methodologies/      # Agile, Scrum, Kanban, etc.
├── models/                 # Domain models and knowledge structures
│   ├── pm_domain_model.py  # Core PM concepts and relationships
│   ├── ethical_framework.py # Baha'i principles applied to PM
│   └── knowledge_graph.py  # Knowledge graph implementation
├── features/               # BDD test scenarios
├── tests/                  # Unit and integration tests
├── kg-schema.ttl          # RDF/OWL knowledge graph schema
└── README.md              # This file
```

## Knowledge Sources

### Expert Sources

1. **Jeff Patton** - User Story Mapping, Discovery Practices
   - Focus: User-centered product development
   - Key concepts: Story mapping, discovery, outcome-focused planning

2. **Jeff Gothelf** - Lean UX, Continuous Discovery
   - Focus: Lean product development, hypothesis-driven design
   - Key concepts: Build-measure-learn, continuous discovery, OKRs

3. **Agile Manifesto** - Core principles of Agile development
4. **Scrum Guide** - Scrum framework and practices
5. **Kanban Method** - Flow-based work management
6. **Lean Startup** - Build-measure-learn cycle

### Ethical Foundation

All PM knowledge and practices are validated against Baha'i principles:

- **Service to Humanity**: Products should benefit society
- **Unity in Diversity**: Inclusive teams and user-centered design
- **Consultation**: Collaborative decision-making
- **Progressive Revelation**: Continuous learning and improvement
- **Elimination of Prejudice**: Fair and unbiased practices

## Usage

The PM domain expert integrates with Santiago's agent framework to provide:

1. **Planning Assistance**: Sprint planning, backlog refinement
2. **Team Coordination**: Facilitating retrospectives, daily standups
3. **Risk Management**: Identifying and mitigating project risks
4. **Stakeholder Communication**: Managing expectations and reporting
5. **Quality Assurance**: Ensuring PM best practices

## Integration

This domain expert is used by the "Pilot" agent in Santiago's autonomous multi-agent swarm. It provides the knowledge base and reasoning capabilities for product management decisions.

## Development

To extend the PM domain knowledge:

1. Add new source materials to `knowledge-sources/`
2. Update domain models in `models/`
3. Create BDD scenarios in `features/`
4. Implement tests in `tests/`
5. Update the knowledge graph schema as needed

All changes must pass ethical validation through the Quartermaster agent.
