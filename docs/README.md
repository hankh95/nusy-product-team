# 📚 Santiago Documentation Hub

## Welcome to Santiago Factory

Santiago is a **self-bootstrapping AI agent factory** that builds specialized AI agents (Santiagos) for specific domains. Each Santiago is a contractor—you hire them, they do the work, they leave. The factory learns from each build and improves itself.

> **"Old Man and the Sea" Pattern**: Santiago fishes for 84 days without a catch, then lands a giant marlin through skill, patience, and learning from each failure.

---

## 🚀 Quick Start

### For New Users
- **[Getting Started Guide](getting-started/README.md)** - Choose your path based on your role
- **[System Overview](system-overview.md)** - High-level understanding of Santiago
- **[Installation Guide](deployment/installation.md)** - Set up your development environment

### For Developers
- **[Developer Handbook](development/handbook.md)** - TDD/BDD practices, kanban workflow
- **[API Reference](api-reference/README.md)** - REST endpoints, MCP contracts, Python SDK
- **[Contributing Guide](CONTRIBUTING.md)** - Development workflow and standards

### For AI Agents
- **[Agent Manual](getting-started/agent.md)** - How to interact with Santiago agents
- **[MCP Integration](api-reference/mcp-integration.md)** - Model Context Protocol usage
- **[Knowledge Graph API](api/knowledge-graph.md)** - Accessing domain knowledge

---

## 📖 Documentation by Audience

### 👥 For Everyone

| Document | Description | Audience |
|----------|-------------|----------|
| **[System Overview](system-overview.md)** | High-level architecture and concepts | All users |
| **[FAQ & Troubleshooting](faq-troubleshooting.md)** | Common questions, issues, and solutions | All users |
| **[Troubleshooting Guide](troubleshooting.md)** | Debug guides, diagnostic tools, recovery | All users |
| **[Changelog](CHANGELOG.md)** | What's new and changed | All users |

### 👨‍💻 For Human Developers

| Document | Description | Purpose |
|----------|-------------|---------|
| **[Getting Started](getting-started/developer.md)** | Development environment setup | Onboarding |
| **[Developer Handbook](development/handbook.md)** | TDD/BDD, kanban, standards | Development practices |
| **[API Reference](api-reference/README.md)** | REST APIs, MCP contracts, Python SDK | Integration |
| **[REST API Guide](api-reference/rest-api.md)** | Complete HTTP API reference | Integration |
| **[Python SDK](api-reference/python-sdk.md)** | Python client library and examples | Integration |
| **[Deployment Guide](deployment/README.md)** | Docker, Kubernetes, cloud deployment | Operations |
| **[Architecture Deep Dive](architecture/deep-dive.md)** | System internals | Understanding |
| **[Troubleshooting](troubleshooting.md)** | Debug guides, common issues | Problem solving |

### 🤖 For AI Agents

| Document | Description | Purpose |
|----------|-------------|---------|
| **[Agent Manual](getting-started/agent.md)** | Agent capabilities and workflows | Usage |
| **[MCP Integration](api-reference/mcp-integration.md)** | Model Context Protocol guide | Integration |
| **[Knowledge Graph](api/knowledge-graph.md)** | Domain knowledge access | Data access |
| **[Agent Development](agents/development.md)** | Building new agents | Extension |
| **[Factory API](api/factory.md)** | Agent factory operations | Management |

### 🏗️ For System Architects

| Document | Description | Purpose |
|----------|-------------|---------|
| **[Architecture Vision](docs/vision/README-START-HERE.md)** | Core design principles | Foundation |
| **[Knowledge Graph Design](architecture/knowledge-graph.md)** | KG architecture and patterns | Design |
| **[Multi-Agent Patterns](docs/vision/multi-agent-patterns/)** | Agent coordination | Architecture |
| **[DGX Integration](deployment/dgx-deployment.md)** | High-performance deployment | Scaling |
| **[Security Model](security/README.md)** | Security architecture | Compliance |

---

## 🏛️ Core Concepts

### The Factory Pattern

Santiago implements a **factory pattern** for AI agent construction:

1. **Navigator** — 10-step domain extraction process
2. **CatchFish** — 4-layer knowledge refinement (30-60m → <15m target)
3. **FishNet** — BDD validation + MCP manifest generation

### Agent Lifecycle

```text
Knowledge Loading → Autonomous Development → Self-Evaluation → Factory Improvement
```

### Quality Gates

- **Apprentice**: Pond scope, basic tasks, proxy level
- **Journeyman**: Lake scope, production-ready, A/B ≥90%
- **Master**: Sea/Ocean scope, self-improving, teaches others

---

## 🛠️ Development Workflow

### Kanban-Based Development
All work follows a kanban workflow with clear ownership:

1. **Backlog** → **Ready** → **In Progress** → **Review** → **Done**
2. Cards are owned by specific agents/humans
3. TDD/BDD practices ensure quality
4. Session logs maintain context

### Testing Standards
- **Unit Tests**: Public interfaces and complex logic
- **BDD Scenarios**: Business workflows and user journeys
- **Integration Tests**: Component interactions
- **Load Tests**: Performance and concurrency validation

---

## 🔌 API Ecosystem

### REST APIs
- `GET /health` - Service health checks
- `POST /tasks` - Create development tasks
- `GET /agents` - List available agents
- `POST /agents/{name}/execute` - Execute with specific agents

### MCP Contracts
- **Knowledge Access**: Domain knowledge retrieval
- **Agent Coordination**: Multi-agent orchestration
- **Factory Operations**: Agent creation and management
- **Quality Validation**: BDD testing and validation

### Knowledge Graph
- **SPARQL Endpoints**: Semantic query interface
- **Provenance Tracking**: Trust and lineage metadata
- **Domain Ontologies**: Structured knowledge models
- **Learning Records**: Continuous improvement data

---

## 🚀 Deployment Options

### Development
```bash
# Local development with hot reload
make serve-reload

# Run tests
make test

# Development Docker
make docker-dev
```

### Production
```bash
# Production deployment
make deploy-prod

# High-performance DGX deployment
make deploy-dgx

# Multi-region deployment
make deploy-multi-region
```

### Monitoring
- **Health Checks**: Automated service monitoring
- **Metrics**: Performance and usage analytics
- **Logging**: Structured logging with correlation IDs
- **Alerting**: Proactive issue detection

---

## 📊 Domain Knowledge

### Core Domains
- **Clinical Intelligence**: Medical decision support
- **Research Synthesis**: Academic knowledge integration
- **Product Management**: Development lifecycle management
- **Quality Assurance**: Testing and validation frameworks

### Knowledge Sources
- **Structured Data**: Databases, APIs, ontologies
- **Unstructured Content**: Documents, papers, web content
- **Expert Knowledge**: Domain specialist contributions
- **Generated Content**: AI-synthesized knowledge

---

## 🤝 Contributing

### Development Process
1. **Claim Work**: Use kanban to claim work items
2. **TDD/BDD Cycle**: Red → Green → Refactor
3. **Quality Gates**: Tests, linting, documentation
4. **Code Review**: Peer review before merge
5. **Session Logging**: Maintain context for continuity

### Documentation Standards
- **Markdown**: Consistent formatting and structure
- **Cross-references**: Link related documentation
- **Examples**: Practical code and usage examples
- **Version Control**: Track documentation changes
- **Accessibility**: Clear for both humans and agents

---

## 📈 Roadmap

### Phase 0: Bootstrap (Current)
- ✅ Repository scaffolding
- ✅ Autonomous multi-agent framework
- 🔄 MCP proxy layer
- 🔄 Knowledge infrastructure

### Phase 1: First Santiago
- Factory builds first real Santiago
- Self-improvement capabilities
- Production deployment validation

### Phase 2+: Santiago Ecosystem
- Multiple domain specialists
- Cross-domain knowledge sharing
- Advanced self-improvement

---

## 🆘 Support

### Getting Help
- **[FAQ & Troubleshooting](faq-troubleshooting.md)** - Common questions and solutions
- **[Troubleshooting Guide](troubleshooting.md)** - Debug guides, diagnostic tools, recovery
- **[Community](community/README.md)** - Discussion forums and resources

### Issue Reporting
- **Bug Reports**: Use GitHub Issues with `bug` label
- **Feature Requests**: Use GitHub Issues with `enhancement` label
- **Security Issues**: Contact security team directly

### Contact
- **Documentation Issues**: Create docs improvement issues
- **Technical Support**: Use project communication channels
- **Agent Development**: Join agent development discussions

---

## 📚 Additional Resources

### External Documentation
- **[Python Documentation](https://docs.python.org/3/)** - Language reference
- **[FastAPI](https://fastapi.tiangolo.com/)** - Web framework docs
- **[SPARQL 1.1](https://www.w3.org/TR/sparql11-query/)** - Query language spec
- **[Docker](https://docs.docker.com/)** - Container platform docs

### Research Papers
- **[Neurosymbolic AI](research/neurosymbolic-ai.md)** - Core research references
- **[Multi-Agent Systems](research/multi-agent-systems.md)** - MAS literature
- **[Knowledge Graphs](research/knowledge-graphs.md)** - KG research papers

### Tools and Utilities
- **[Development Tools](tools/README.md)** - Custom development utilities
- **[Testing Framework](testing/README.md)** - Testing tools and practices
- **[CI/CD Pipeline](deployment/ci-cd.md)** - Build and deployment automation

---

*This documentation is maintained by the Santiago Documentation Agent. Last updated: November 20, 2025*