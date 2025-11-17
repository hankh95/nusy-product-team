# Santiago - Domain-Specific NuSy PM Agent

This directory contains the **domain-specific Santiago implementation** - a specialized NuSy PM agent focused on product management workflows.

## Architecture Separation

This project maintains a clear separation of concerns:

- **`nusy_pm/`**: The **NuSy Builder Toolkit** - generic tools and frameworks for building any domain-specific NuSy AI
- **`santiago/`**: The **Domain-Specific Implementation** - Santiago's specialized product management capabilities
- **`src/nusy_pm_core/`**: The **Core Runtime** - shared implementation that both builder toolkit and domain agents use

## Santiago's Domain Specialization

Santiago is specialized for:

- Product management and development coordination
- Lean hypothesis testing and experimentation
- Multi-agent team orchestration
- Knowledge capture and continuous learning
- Nautical-themed workflow management (passages)

## Directory Structure

```text
santiago/
├── agents/           # Santiago's specialized agent definitions
├── passages/         # Santiago's domain-specific passage definitions
├── config/           # Santiago-specific configuration
├── docs/             # Santiago documentation and specifications
└── README.md         # This file
```

## Development Workflow

1. **Use `nusy_pm/` tools** to define new capabilities (passages, tackle, etc.)
2. **Implement in `santiago/`** for domain-specific specialization
3. **Test integration** through `src/nusy_pm_core/`
4. **Deploy and monitor** using the combined system

## Key Santiago Features

- **Passage Execution**: Autonomous execution of complex workflows
- **Hypothesis Testing**: Lean experimentation framework
- **Knowledge Synthesis**: Continuous learning from development activities
- **Multi-Agent Coordination**: Orchestrating human-AI collaborative processes
- **Nautical Metaphors**: Santiago-themed workflow language and concepts
