# Santiago PM - Neurosymbolic Product Management System

The Santiago PM system is Santiago's central nervous system for autonomous development. It provides a structured, knowledge-graph backed framework for managing all aspects of product development, from features and issues to experiments and strategic planning.

## Nautical Theme

Inspired by the Santiago ship metaphor, NuSy PM uses nautical terminology to create an intuitive, thematic organization that aids both human developers and autonomous agents in navigation and discovery.

## Folder Structure

| Nautical Name | Common Name | Description |
|---------------|-------------|-------------|
| cargo-manifests | Features | BDD feature specifications and requirements |
| ships-logs | Issues | Issue tracking, bug reports, and incident logs |
| voyage-trials | Experiments | Experiment planning, execution, and results |
| expeditions | Expeditions | Structured hypothesis-driven development expeditions |
| navigation-charts | Plans | Development plans, milestones, and roadmaps |
| captains-journals | Notes | Knowledge capture, insights, and documentation |
| research-logs | Research | Research findings, analysis, and discoveries |
| crew-manifests | Roles | Agent roles, responsibilities, and capabilities |
| quality-assessments | Tests | Test suites, quality metrics, and assessments |
| strategic-charts | Vision | Strategic vision, goals, and long-term planning |
| **tackle** | **Implementations** | Python modules, CLI tools, and KG integrations |

## Folder Details

### cargo-manifests/ (Features)
**Purpose**: Define and track product features using BDD specifications
**Template**: `cargo-manifest-template.md` (Gherkin format)
**CLI**: `nusy features [command]` (planned)
**Contents**: Feature files with scenarios and acceptance criteria

### ships-logs/ (Issues)
**Purpose**: Track issues, bugs, and development tasks
**Template**: `ships-log-template.md` (structured issue format)
**CLI**: `nusy issues [command]` (implemented)
**Contents**: Issue reports with status, priority, and comments

### voyage-trials/ (Experiments)
**Purpose**: Design, execute, and analyze development experiments
**Template**: `voyage-trial-template.md` (experimental design framework)
**CLI**: `nusy experiments [command]` (implemented)
**Contents**: Experiment plans, results, and success metrics

### expeditions/ (Expeditions)
**Purpose**: Structured hypothesis-driven development expeditions
**Template**: `voyage-trial-template.md` (for new expeditions)
**CLI**: `nusy expeditions [command]` (planned)
**Contents**: Expedition plans, execution tracking, and comprehensive results

### navigation-charts/ (Plans)
**Purpose**: Strategic planning and development roadmapping
**Template**: `navigation-chart-template.md` (milestone-based planning)
**CLI**: `nusy plans [command]` (implemented)
**Contents**: Development plans with tasks and progress tracking

### captains-journals/ (Notes)
**Purpose**: Capture knowledge, insights, and project history
**Template**: `captains-journal-template.md` (narrative knowledge format)
**CLI**: `nusy notes [command]` (implemented)
**Contents**: Session notes, learnings, and linked artifacts

### research-logs/ (Research)
**Purpose**: Document research findings and analytical work
**Template**: `research-log-template.md` (research report format)
**CLI**: `nusy research [command]` (planned)
**Contents**: Research papers, analysis results, and findings

### crew-manifests/ (Roles)
**Purpose**: Define agent roles and human responsibilities
**Template**: `crew-manifest-template.md` (role specification format)
**CLI**: `nusy roles [command]` (planned)
**Contents**: Agent instructions, role definitions, and capabilities

### quality-assessments/ (Tests)
**Purpose**: Quality assurance, testing, and validation
**Template**: `quality-assessment-template.md` (test report format)
**CLI**: `nusy tests [command]` (planned)
**Contents**: Test suites, results, and quality metrics

### strategic-charts/ (Vision)
**Purpose**: Long-term strategic planning and vision
**Template**: `strategic-chart-template.md` (strategic planning format)
**CLI**: `nusy vision [command]` (planned)
**Contents**: Vision documents, strategic goals, and roadmaps

## System Architecture

NuSy PM integrates with Santiago's core components:

- **Knowledge Graph**: Central storage for all PM data and relationships
- **Agent Framework**: Autonomous agents that read/write PM artifacts
- **CLI Interface**: Human and agent access to PM functions
- **Web API**: RESTful access for external integrations
- **Evolution Engine**: Continuous improvement of PM processes

## Implementation Architecture

NuSy PM uses a **domain-driven design** with clear separation between specifications and implementations:

### Domain Specifications

The main `nusy_pm/` folders contain **domain specifications** - the "what" and "why" of each component:

- Feature requirements (cargo-manifests/)
- Issue definitions (ships-logs/)
- Experiment designs (voyage-trials/)
- Expedition frameworks (expeditions/)
- Strategic plans (navigation-charts/)
- Knowledge capture (captains-journals/)

### Tackle Implementations

The `tackle/` subdirectory contains **implementations** - the "how" of each component:

- Python modules that realize domain specifications
- CLI tools for human and agent interaction
- Knowledge graph integration
- Testing and validation suites

### Santiago Integration

Santiago reads domain specifications from the main folders and autonomously generates corresponding tackle implementations, creating a complete feedback loop between specification and execution.

## Current Tackle

| Tackle | Status | Purpose |
|--------|--------|---------|
| **status** | ✅ **PRODUCTION READY** | Universal status tracking system |
| **notes** | 🚧 **PLANNED** | Notes management with relationships |
| **experiments** | 🚧 **PLANNED** | Experiment execution framework |

Each tackle follows the standard structure:

- `models.py` - Data models and business logic
- `services.py` - Core functionality
- `cli.py` - Command-line interface
- `kg.py` - Knowledge graph integration
- `test_*.py` - Comprehensive test suite
- `development-plan.md` - Individual implementation plan

## Development Workflow

1. **Feature Definition**: Create cargo manifests with BDD scenarios
2. **Planning**: Develop navigation charts with milestones
3. **Implementation**: Track progress through ships logs
4. **Experimentation**: Run voyage trials to validate approaches
5. **Expedition Execution**: Conduct structured expeditions for major capabilities
6. **Knowledge Capture**: Document insights in captains journals
7. **Quality Assurance**: Validate through quality assessments
8. **Evolution**: Use feedback to improve processes

## Future CLI Commands

As features are implemented, the following CLI commands will be available:

- `nusy status` - ✅ **IMPLEMENTED** (universal status tracking)
- `nusy features` - Manage feature specifications
- `nusy expeditions` - Manage hypothesis-driven development expeditions
- `nusy research` - Handle research documentation
- `nusy roles` - Define and manage roles
- `nusy tests` - Run and manage test suites
- `nusy vision` - Work with strategic planning
- `nusy knowledge` - Semantic wiki and ingestion
- `nusy improvements` - Feedback and hypothesis management

## Integration Points

- **Git**: Version control for all PM artifacts
- **KG**: Semantic relationships between all PM elements
- **Agents**: Autonomous reading/writing of PM data
- **APIs**: External tool integration via MCP
- **Evolution**: Self-improvement based on PM data patterns

This structure ensures NuSy PM serves as the central coordination point for all Santiago development activities, providing both human developers and autonomous agents with a comprehensive, semantically-rich framework for product management.
