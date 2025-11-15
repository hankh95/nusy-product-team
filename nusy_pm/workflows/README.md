# NuSy PM Workflows

This directory contains workflow definitions and specifications for coordinating work between humans, agents, and automated systems in the NuSy development ecosystem.

## Directory Structure

```text
workflows/
├── workflow-system.md          # Domain specification for workflow system
├── examples/                   # Example workflow definitions
│   ├── santiago-general-code-generation.yaml
│   └── nusy-pm-tackle-development.yaml
└── README.md                   # This file
```

## Workflow Categories

### Generalized Santiago Workflows

These workflows enable Santiago to operate autonomously across different domains and projects:

- **Code Generation**: From specifications to complete implementations
- **System Analysis**: Understanding and documenting complex systems
- **Quality Assurance**: Automated testing and validation processes
- **Documentation**: Generating and maintaining project documentation

### NuSy PM Domain Workflows

These workflows are specific to the NuSy PM domain and tackle development:

- **Tackle Development**: End-to-end process for implementing new tackle
- **Experiment Management**: Coordinating autonomous experiments
- **Knowledge Integration**: Processing and storing domain knowledge
- **System Evolution**: Managing system updates and improvements

## Workflow Types

### Team Workflows

Processes involving human collaboration, decision-making, and oversight.

### Agent Workflows

Fully autonomous processes executed by AI agents without human intervention.

### Hybrid Workflows

Collaborative processes combining human expertise with agent automation.

### Integration Workflows

System-level processes for deployment, monitoring, and maintenance.

## Development Status

- **Specification**: ✅ Complete (`workflow-system.md`)
- **Examples**: ✅ Available (2 example workflows)
- **Implementation**: 🚧 Planned (see tackle/workflows development plan)
- **Integration**: 🚧 Planned (KG, MCP, tackle system integration)

## Usage

### For Santiago (Generalized Workflows)

Santiago can use these workflows to:

1. **Understand Process Requirements**: Parse workflow definitions to understand required steps
2. **Execute Autonomous Tasks**: Follow workflow steps for code generation, testing, etc.
3. **Coordinate with Humans**: Request approvals and provide status updates
4. **Maintain Quality**: Execute quality gates and validation steps

### For NuSy PM Team

The team can use these workflows to:

1. **Standardize Processes**: Ensure consistent execution of complex tasks
2. **Delegate to Agents**: Define clear handoffs between humans and agents
3. **Track Progress**: Monitor workflow execution and identify bottlenecks
4. **Capture Knowledge**: Document successful patterns for future reuse

## Implementation Roadmap

See `../tackle/workflows/development-plan.md` for detailed implementation timeline and requirements.

## Related Components

- **Cargo Manifests**: Feature definitions that workflows may implement
- **Crew Manifests**: Agent instructions that workflows coordinate
- **Tackle System**: Implementation components that workflows orchestrate
- **Knowledge Graph**: Storage for workflow metadata and execution history
