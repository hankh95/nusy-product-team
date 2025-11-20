# 👨‍💻 Developer Getting Started Guide

Welcome, developer! This guide will help you set up your development environment and start contributing to Santiago. We'll cover everything from installation to your first contribution.

---

## 📋 Prerequisites

### Required
- **Python 3.11+**: Santiago requires modern Python features
- **Git**: Version control for all contributions
- **Terminal**: Command-line interface (zsh, bash, etc.)

### Recommended
- **VS Code**: Our recommended editor with Python extensions
- **Docker**: For containerized development and testing
- **GitHub Account**: For contributing and issue tracking

### System Requirements
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **Network**: Stable internet for dependencies

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
# Clone the main repository
git clone https://github.com/hankh95/nusy-product-team.git
cd nusy-product-team

# Verify clone
ls -la
# Should see: docs/ santiago_core/ self_improvement/ etc.
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate     # On Windows

# Upgrade pip
pip install --upgrade pip
```

### 3. Install Dependencies

```bash
# Install Santiago in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Verify installation
python -c "import santiago_core; print('✅ Santiago installed successfully!')"
```

### 4. Environment Configuration

```bash
# Copy environment template
cp .env.template .env

# Edit .env with your configuration
# At minimum, you'll need:
# - Database connection strings
# - API keys for external services
# - Development mode settings
```

### 5. Run Initial Tests

```bash
# Run basic health checks
python -m pytest tests/test_health.py -v

# Run a small subset of tests
python -m pytest tests/unit/ -k "test_basic" --tb=short
```

---

## 🏗️ Development Environment

### VS Code Setup (Recommended)

1. **Install Extensions**:
   - Python (Microsoft)
   - Pylance
   - Python Docstring Generator
   - GitLens
   - Docker

2. **Workspace Settings**:
   ```json
   {
     "python.defaultInterpreterPath": "./venv/bin/python",
     "python.linting.enabled": true,
     "python.linting.pylintEnabled": true,
     "python.formatting.provider": "black",
     "editor.formatOnSave": true
   }
   ```

3. **Debug Configuration**:
   ```json
   {
     "name": "Santiago Debug",
     "type": "python",
     "request": "launch",
     "program": "${workspaceFolder}/santiago_core/run_team.py",
     "console": "integratedTerminal",
     "args": ["--config", "config/dev.json"]
   }
   ```

### Docker Development

```bash
# Build development container
make docker-build-dev

# Run with hot reload
make docker-run-dev

# View logs
make docker-logs
```

---

## 📖 Understanding the Codebase

### Project Structure

```
santiago-factory/
├── santiago_core/          # Core Santiago components
│   ├── agents/            # AI agent implementations
│   ├── services/          # Business logic services
│   └── core/              # Core infrastructure
├── domain/                # Domain-specific code
│   ├── src/               # Domain implementations
│   └── examples/          # Usage examples
├── self_improvement/      # Self-improvement components
│   ├── santiago_pm/       # PM scaffold and tools
│   └── santiago_dev/      # Development tools
├── docs/                  # Documentation
├── tests/                 # Test suites
└── tools/                 # Development utilities
```

### Key Concepts

#### 1. The Factory Pattern
Santiago uses a **factory pattern** for agent construction:
- **Navigator**: Domain analysis and planning
- **CatchFish**: Knowledge extraction and refinement
- **FishNet**: Quality validation and manifest generation

#### 2. Knowledge Graph
All domain knowledge is stored in a **knowledge graph**:
- **SPARQL queries** for knowledge access
- **Provenance tracking** for trust
- **Ontology-based** structure

#### 3. Kanban Workflow
Development follows **kanban principles**:
- **Work ownership**: Single owner per task
- **Quality gates**: Automated testing and validation
- **Session logging**: Context preservation

---

## 🧪 Development Workflow

### TDD/BDD Development Cycle

Santiago follows **Test-Driven Development** and **Behavior-Driven Development**:

#### 1. Red Phase - Write Failing Tests

```python
# tests/test_my_feature.py
import pytest
from santiago_core.services.my_service import MyService

def test_my_feature_basic():
    """Test basic functionality of my feature."""
    service = MyService()
    # This test will fail until we implement the feature
    result = service.do_something()
    assert result is not None
```

#### 2. Green Phase - Make Tests Pass

```python
# santiago_core/services/my_service.py
class MyService:
    """My new service implementation."""

    def do_something(self):
        """Implement the basic functionality."""
        return "Hello, World!"
```

#### 3. Refactor Phase - Improve Code Quality

```python
# santiago_core/services/my_service.py
class MyService:
    """Service for handling my feature operations."""

    def __init__(self, config=None):
        self.config = config or {}

    def do_something(self) -> str:
        """
        Perform the main operation.

        Returns:
            str: The result of the operation
        """
        return "Hello, World!"
```

### Kanban Workflow

#### Claim Work
```bash
# Use kanban CLI to claim work
cd self_improvement/santiago_pm
python -m tackle.kanban.kanban_cli claim-next exp-057-migration --agent "your-name"
```

#### Development Process
1. **Claim a card** from the kanban board
2. **Write tests first** (TDD/BDD)
3. **Implement minimal code** to pass tests
4. **Refactor** for quality and readability
5. **Run full test suite** locally
6. **Create pull request** with session context

#### Session Logging
```bash
# Save session context after work
python save-chat-log.py --paste --with-summary --topic "my-feature-implementation"
```

---

## 🐛 Your First Contribution

### Find an Issue

1. **Check GitHub Issues** for `good first issue` labels
2. **Use Kanban** to find available work:
   ```bash
   cd self_improvement/santiago_pm
   python -m tackle.kanban.kanban_cli show-board exp-057-migration
   ```

### Example: Fix a Small Bug

Let's say you find an issue about a typo in documentation:

1. **Claim the work**:
   ```bash
   python -m tackle.kanban.kanban_cli claim-card exp-057-migration card-issue-123 --agent "your-name"
   ```

2. **Create a branch**:
   ```bash
   git checkout -b fix/typo-in-readme
   ```

3. **Make the fix**:
   ```bash
   # Edit the file with the typo
   vim docs/README.md
   ```

4. **Test your changes**:
   ```bash
   # Run relevant tests
   make test-docs
   ```

5. **Commit and push**:
   ```bash
   git add docs/README.md
   git commit -m "fix: Correct typo in README.md

   Fixes #123"
   git push origin fix/typo-in-readme
   ```

6. **Create PR**:
   ```bash
   gh pr create --title "fix: Correct typo in README.md" --body "Closes #123"
   ```

### Example: Add a Test

1. **Find untested code** or improve test coverage
2. **Write test first**:
   ```python
   # tests/test_new_feature.py
   def test_new_feature():
       # Test implementation
       pass
   ```
3. **Implement the feature** to make test pass
4. **Refactor** for quality
5. **Run tests**: `make test-cov`

---

## 🧪 Testing & Quality

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
python -m pytest tests/test_my_feature.py -v

# Run tests matching pattern
python -m pytest -k "test_feature" -v
```

### Code Quality

```bash
# Run linting
make lint

# Format code
make format

# Type checking
make type-check

# Security scan
make security-scan
```

### Pre-commit Checks

Before pushing, ensure:
- ✅ All tests pass
- ✅ Code is formatted
- ✅ No linting errors
- ✅ Type hints are correct
- ✅ Security checks pass

---

## 📚 Learning Resources

### Essential Reading
- **[System Overview](../system-overview.md)** - High-level understanding
- **[Developer Handbook](../development/handbook.md)** - Detailed practices
- **[API Reference](../api/reference.md)** - Technical integration
- **[Contributing Guide](../../CONTRIBUTING.md)** - Development standards

### Key Documents
- **[Architecture Vision](../vision/README-START-HERE.md)** - Core principles
- **[Knowledge Graph Design](../architecture/knowledge-graph.md)** - Data architecture
- **[TDD/BDD Examples](../../CONTRIBUTING.md#practical-tdd-bdd-workflow-examples)** - Code examples

### Tools & Utilities
- **[Development Tools](../tools/README.md)** - Custom utilities
- **[Testing Framework](../testing/README.md)** - Testing practices
- **[CI/CD Pipeline](../deployment/ci-cd.md)** - Build automation

---

## 🆘 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure you're in the virtual environment
source venv/bin/activate

# Check Python path
python -c "import sys; print(sys.path)"

# Reinstall dependencies
pip install -e .
```

#### Test Failures
```bash
# Run tests with verbose output
python -m pytest tests/ -v --tb=long

# Run specific failing test
python -m pytest tests/test_failing.py::TestClass::test_method -v

# Check test dependencies
pip list | grep pytest
```

#### Git Issues
```bash
# Check repository status
git status

# Reset to clean state
git reset --hard origin/main

# Clean untracked files
git clean -fd
```

### Getting Help

1. **Check the FAQ**: `docs/faq-troubleshooting.md`
2. **Search Issues**: Look for similar problems
3. **Ask the Community**: Create a discussion or issue
4. **Debug Together**: Share logs and error messages

---

## 🎯 Next Steps

### Week 1: Getting Comfortable
- [ ] Complete environment setup
- [ ] Run the full test suite
- [ ] Fix 1-2 small issues
- [ ] Understand the codebase structure

### Week 2: Building Skills
- [ ] Implement a small feature using TDD
- [ ] Contribute to documentation
- [ ] Review someone else's PR
- [ ] Learn about the knowledge graph

### Week 3: Taking Ownership
- [ ] Own a complete feature implementation
- [ ] Improve test coverage in an area
- [ ] Help onboard another developer
- [ ] Contribute to architecture discussions

### Ongoing: Mastery
- [ ] Become a maintainer of a component
- [ ] Lead major feature development
- [ ] Mentor junior contributors
- [ ] Drive architectural improvements

---

## 🤝 Community & Culture

### Development Culture
- **Quality First**: Tests and documentation are paramount
- **Learning Mindset**: Every interaction improves the system
- **Collaboration**: We work together, not in silos
- **Transparency**: Open communication and decision-making

### Contributing Back
- **Share Knowledge**: Document what you learn
- **Help Others**: Answer questions and review code
- **Improve Processes**: Suggest workflow improvements
- **Grow the Community**: Help onboard new contributors

---

*Ready to start coding? Remember: every expert was once a beginner. Take it one test at a time, and you'll be contributing valuable improvements to Santiago in no time!* 🚀

**Need help?** Don't hesitate to ask questions in GitHub Discussions or create an issue. The community is here to help you succeed.