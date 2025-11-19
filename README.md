# Santiago Factory

**A self-bootstrapping AI agent factory that builds domain-specific contractors**

Santiago is NOT a team. It IS a factory that builds specialized AI agents (Santiagos) for specific domains. Each Santiago is a contractor—you hire them, they do the work, they leave. The factory learns from each build and improves itself.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -e .

# 2. Read the vision
cat docs/vision/README-START-HERE.md

# 3. See the architecture
cat ARCHITECTURE.md

# 4. Check the roadmap
cat zarchive/migration-artifacts/MIGRATION_ROADMAP.md

# 5. Review development plan
cat _archive/docs/DEVELOPMENT_PLAN.md
```

---

## Development & Deployment

### Local Development

```bash
# Run full CI pipeline locally
make ci

# Run tests with coverage
make test-cov

# Start development server
make serve-reload

# Deploy to local development
make deploy-dev
```

### Testing

```bash
# Run all tests
make test

# Run smoke tests (API connectivity)
make test-smoke

# Run tests with coverage report
make test-cov
```

### Docker Deployment

```bash
# Build Docker image
make docker-build

# Run with Docker Compose
make docker-run

# View logs
make docker-logs

# Stop containers
make docker-stop
```

### CI/CD Pipeline

The project uses GitHub Actions for automated testing and deployment:

- **Linting**: Markdown and code quality checks
- **Testing**: Unit tests with 80% coverage requirement
- **Quality Gates**: Security scanning and complexity analysis
- **Multi-stage Deployment**: Development → Staging → Production

#### Deployment Environments

- **Development**: Local deployment with hot reload
- **Staging**: Docker-based deployment for integration testing
- **Production**: Full production deployment with monitoring

#### Manual Deployment

```bash
# Deploy to staging
make deploy-staging

# Deploy to production
make deploy-prod

# Or use the deployment script directly
./scripts/deploy.sh production
```

### API Endpoints

Once deployed, Santiago provides REST API endpoints:

- `GET /health` - Health check
- `POST /tasks` - Create development tasks
- `GET /tasks` - List active tasks
- `GET /agents` - List available agents
- `POST /agents/{name}/execute` - Execute tasks with specific agents

---

## Documentation

- **[CI/CD & Deployment Guide](docs/CI_CD_DEPLOYMENT.md)**: Complete CI/CD and deployment documentation
- **[API Reference](docs/API_REFERENCE.md)**: REST API documentation and examples
- **[Development Practices](DEVELOPMENT_PRACTICES.md)**: TDD/BDD and development standards
- **[Architecture](ARCHITECTURE.md)**: System architecture and design decisions

---

## What is Santiago?

Santiago implements the **"Old Man and the Sea"** pattern:

1. **Navigator** — 10-step fishing process (domain extraction)
2. **Catchfish** — 4-layer refinement (30-60m baseline → <15m target)
3. **Fishnet** — Test + manifest generation (BDD + MCP contract)

Each Santiago built by the factory:
- Has **domain knowledge** stored in `knowledge/catches/<santiago>/`
- Has **BDD tests** validating that knowledge
- Has **MCP manifest** defining its service contract
- Has **provenance metadata** for trustworthiness

The factory **self-improves**: as it builds more Santiagos, it learns patterns and gets faster/better.

---

## The Fake Team (Phase 0)

Before real Santiagos exist, we use **proxy agents**—thin wrappers around external APIs:

```
Phase 0: Proxy agents (external APIs) ← WE ARE HERE
Phase 1: First real Santiago built (factory can self-improve)
Phase 2+: Real Santiagos replace proxies one by one
```

See `santiago_core/agents/_proxy/` and `docs/vision/fake_team_pack/`.

---

## Architecture Highlights

### Knowledge Storage
```
knowledge/
├── catches/
│   ├── index.yaml              # Trust registry
│   └── <santiago>/
│       ├── domain-knowledge/   # Extracted knowledge
│       ├── bdd-tests/          # Validation tests
│       ├── mcp-manifest.json   # Service contract
│       └── provenance.yaml     # Trustworthiness metadata
├── templates/                  # Reusable patterns
└── proxy-instructions/         # Phase 0 proxy configs
```

### Capability Levels
- **Apprentice** — Pond scope, basic tasks, proxy level
- **Journeyman** — Lake scope, production-ready, A/B ≥90%
- **Master** — Sea/Ocean scope, self-improving, teaches others

### Governance
- **Queue-first** KG writes (idempotency, validation, provenance)
- **A/B parity** ≥90% before promotion
- **Rehearsal pass rate** ≥95% BDD tests
- **Hybrid routing** with 80/20 traffic splits
- **Rollback strategy** with warm proxy + canary

---

## Project Structure

```
/santiago-factory/
├── ARCHITECTURE.md              # Full architecture (canonical)
├── MIGRATION_ROADMAP.md         # M0-M4 implementation plan
├── ASSUMPTIONS_AND_RISKS.md     # Risks & mitigation
├──
├── docs/
│   ├── vision/                  # Core vision documents
│   │   ├── 00-ARCHITECTURE-PATTERN.md
│   │   ├── README-START-HERE.md
│   │   ├── building-on-DGX/
│   │   └── fake_team_pack/
│   ├── FOLDER_LAYOUT.md
│   └── RELEVANCE_MAP.md
├──
├── santiago-pm/                 # PM/development patterns
│   ├── strategic-charts/        # High-level strategy
│   ├── expeditions/             # Feature explorations
│   ├── tackle/                  # Tools & techniques
│   └── ...                      # 14 subdirectories
├──
├── knowledge/                   # Factory knowledge base
│   ├── catches/                 # Built Santiagos
│   ├── templates/               # Reusable patterns
│   └── proxy-instructions/      # Phase 0 proxies
├──
├── nusy_orchestrator/
│   └── santiago_builder/        # Factory components
│       ├── navigator.py         # 10-step process
│       ├── catchfish.py         # 4-layer extraction
│       └── fishnet.py           # Test + manifest gen
├──
├── santiago_core/
│   └── agents/
│       └── _proxy/              # Phase 0 fake team
├──
├── evaluation/                  # Quality metrics
├── config/                      # Configuration
└── tools/                       # Utilities
```

---

## Development

### Current Status

**Phase 0** (Bootstrap Fake Team) — In Progress

- ✅ Repository scaffolding and strategic artifacts
- ✅ Autonomous multi-agent experiment framework
- 🔄 MCP proxy layer implementation
- 🔄 Knowledge infrastructure creation

See `zarchive/migration-artifacts/MIGRATION_ROADMAP.md` for detailed milestones and `_archive/docs/DEVELOPMENT_PLAN.md` for phased approach.

### Key Documents

1. **Start Here**: `docs/vision/README-START-HERE.md`
2. **Architecture**: `ARCHITECTURE.md` (v3.0, hybrid synthesis, 2025-11-16)
3. **Roadmap**: `zarchive/migration-artifacts/MIGRATION_ROADMAP.md` (Milestones 0-6)
4. **Development Plan**: `_archive/docs/DEVELOPMENT_PLAN.md` (Phase-aligned approach)
5. **Domain Knowledge**: `santiago-pm/` (PM patterns and practices)
6. **Contributing**: `CONTRIBUTING.md`

### Running Tests

```bash
# Run evaluation harness
python evaluation/run_evaluation.py

# Run factory tests (TODO: M0)
pytest santiago_core/tests/
```

---

## Why "Santiago"?

From Hemingway's *The Old Man and the Sea*:

> Santiago fishes for 84 days without a catch, then lands a giant marlin through skill, patience, and learning from each failure.

The factory embodies this:
- **Persistent iteration** (keeps trying, learns from failures)
- **Deep expertise** (domain knowledge extraction)
- **Self-improvement** (meta-learning from each build)
- **Respect for the craft** (quality over speed)

---

## DGX Deployment

Designed for shared 7-8B models via vLLM/TensorRT-LLM:

- **Storage tiers**: Hot (4TB NVMe) / Warm (8-16TB RAID) / Cold (NAS)
- **SLOs**: p95 ≤2500ms, ≥20 RPS, ≤0.03 USD/req
- **Concurrency**: 50-100 parallel requests
- **Scale**: 100+ Santiagos on single DGX

See `docs/vision/building-on-DGX/`.

---

## License

[Your license here]

---

## Contact

[Your contact info here]

---

## Archive

Historical artifacts preserved in `_archive/`:
- Research explorations (`_archive/research/`)
- Old architecture plans (`_archive/plans/`)
- Legacy code (`_archive/legacy/`)
- Development history (`_archive/development/`)

To restore pre-migration state: `git checkout v1.0-pre-migration`
