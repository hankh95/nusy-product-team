# GitHub Copilot Custom Agents

This directory contains custom agent configurations for GitHub Copilot in the Clinical Intelligence Starter project. These are **not** API agent instructions.

**For complete development practices, see [DEVELOPMENT_PRACTICES.md](../DEVELOPMENT_PRACTICES.md) - the single source of truth for all development standards.**

## About GitHub Copilot Custom Agents

GitHub Copilot Agents allow you to create specialized AI assistants tailored to specific development tasks and domains. Each agent is defined by a markdown file in this directory with specific instructions and capabilities for use within GitHub Copilot.

## Agent Instruction Hierarchy

The project maintains a comprehensive hierarchy of AI agent instructions to ensure consistent development practices and domain expertise:

### 0. Universal Development Practices ([`DEVELOPMENT_PRACTICES.md`](../DEVELOPMENT_PRACTICES.md))
**Purpose**: Single source of truth for all development practices
**Scope**: TDD/BDD workflow, code quality, testing standards, Git workflow, domain practices
**Files**: [`DEVELOPMENT_PRACTICES.md`](../DEVELOPMENT_PRACTICES.md)
**Audience**: All developers and AI agents
**Status**: Primary reference - all other documents reference this

### 1. Universal Agent Rules (`.cursorrules`)
**Purpose**: Repository-wide custom instructions for all AI coding assistants (Cursor, Claude, GitHub Copilot, etc.)
**Scope**: Mandatory TDD/BDD development workflow, technical standards, and project references
**Files**: [`.cursorrules`](../.cursorrules)
**Audience**: All AI assistants working on code development
**Relationship**: References DEVELOPMENT_PRACTICES.md for complete standards

### 2. GitHub Copilot Custom Agents (`.github/agents/*.md`)
**Purpose**: Specialized AI assistants for specific development tasks within GitHub Copilot
**Scope**: Domain-specific development expertise and task-focused capabilities
**Files**: 
- `development.agent.md` - Technical development for Clinical Intelligence Starter project
- `neuroSym-clinical-architect.agent.md` - Clinical architecture and knowledge graph design
- `clinical-knowledge-qa.agent.md` - BDD testing and clinical QA validation
- `clinical-informaticist.agent.md` - Clinical informatics and knowledge representation
- `hanks-product-manager.agent.md` - Product management and hypothesis-driven development
**Audience**: GitHub Copilot users assigning specialized development tasks
**Relationship**: Extends DEVELOPMENT_PRACTICES.md with task-specific expertise

### 3. API Agent Instructions (`docs/*.agent.instructions.md`)
**Purpose**: Instructions sent to external AI APIs for specific domain tasks
**Scope**: Specialized domain expertise for clinical content authoring and QA
**Files**:
- `docs/development-agent.instructions.md` - General technical architecture and development practices
- `docs/authoring-agent.instructions.md` - Clinical content authoring and CIKG standards
- `docs/clinical-knowledge-qa.agent.instructions.md` - Clinical QA validation and BDD testing
**Audience**: External AI services called by the application code
**Relationship**: Extends DEVELOPMENT_PRACTICES.md with API-specific domain expertise

### 4. Development Workflow Documentation (`CONTRIBUTING.md`)
**Purpose**: Complete TDD/BDD development process and contribution guidelines with detailed examples
**Scope**: Issue management, pull request process, quality gates, and team coordination
**Files**: [`CONTRIBUTING.md`](../CONTRIBUTING.md)
**Audience**: All developers and AI assistants
**Relationship**: Implements DEVELOPMENT_PRACTICES.md with detailed examples and processes

## Implementation Notes

- **Universal Practices First**: All documentation references [DEVELOPMENT_PRACTICES.md](../DEVELOPMENT_PRACTICES.md) for core standards
- **Universal Rules**: All agent instructions reference `.cursorrules` for mandatory workflow compliance
- **Layered Specialization**: Each layer adds domain-specific expertise while maintaining workflow consistency
- **Cross-References**: Agent instructions reference each other and core documentation
- **Standards Compliance**: All instructions align with GitHub Copilot documentation and best practices

## Agent Structure

Each agent file should follow this naming convention:
- `{agent-name}.md` - The agent configuration file

### Required Front Matter

Each agent file must include YAML front matter:

```yaml
---
name: "Agent Display Name"
description: "Brief description of what this agent does"
instructions: |
  Detailed instructions for the agent...
  Multiple lines supported.
---
```

### Agent Categories for This Project

We recommend creating specialized agents for different development tasks:

1. **`catchfish-dev-agent.md`** - CatchFish development and debugging tasks
2. **`fishnet-dev-agent.md`** - BDD FishNet development tasks
3. **`navigator-dev-agent.md`** - Navigator orchestration development
4. **`ai-review-dev-agent.md`** - AI Knowledge Review development
5. **`infrastructure-dev-agent.md`** - DevOps and infrastructure development

## How to Use Custom Agents

Once configured, you can invoke agents in GitHub Copilot by mentioning them:

```
/@catchfish-dev-agent Please help me debug this BigFish pipeline issue
```

## Agent Guidelines

### General Principles
- **Development Focus**: Each agent should specialize in development tasks for specific modules
- **Code Quality**: Emphasize best practices, testing, and documentation
- **Project Standards**: Follow CIKG architecture, FHIR-CPG compliance, and project conventions
- **Integration**: Work with existing codebase and development workflows

### Module-Specific Focus

#### CatchFish Development Agent
- L0-L3 asset generation implementation
- BigFish/LittleFish/Krill pipeline development
- Clinical content processing algorithms
- FHIR resource validation and testing

#### FishNet Development Agent
- BDD scenario generation implementation
- Clinical QA validation logic
- Test automation frameworks
- Patient fixture and assertion development

#### Navigator Development Agent
- Pipeline orchestration implementation
- Multi-cycle automation logic
- Service interface development
- Status monitoring and error handling

#### AI Review Development Agent
- Coverage analysis algorithms
- Gap identification logic
- Quality metrics implementation
- BDD test validation integration

#### Infrastructure Development Agent
- CI/CD pipeline development
- Environment configuration
- Deployment automation
- Performance monitoring and optimization

## Best Practices

### Instruction Writing
- **Clear Scope**: Define exactly what development tasks the agent should handle
- **Code Examples**: Include concrete examples of implementations and patterns
- **Testing**: Specify testing requirements and validation approaches
- **Integration**: Include guidance on working with existing codebase

### File Organization
- Keep instructions focused on development tasks
- Use consistent formatting and structure
- Reference project architecture and standards
- Include troubleshooting guidance

## Getting Started

1. Create agent markdown files in this directory
2. Follow the front matter format above
3. Test agents with sample development tasks
4. Refine instructions based on effectiveness
5. Document agent capabilities in project wiki

## References

- [GitHub Copilot Agents Documentation](https://docs.github.com/en/copilot/concepts/agents/coding-agent/about-custom-agents)
- [Clinical Intelligence Starter Development Plan](../DEVELOPMENT_PLAN.md)
- [API Agent Instructions](../agent-instructions/README.md)
- [Universal Agent Work Practices](../.cursorrules) - Standard practices for all AI coding assistants