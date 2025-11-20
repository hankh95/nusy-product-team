# ❓ FAQ & Troubleshooting

This document addresses frequently asked questions and common issues when working with Santiago. If you don't find your answer here, check the [troubleshooting guide](troubleshooting/README.md) or create an issue.

---

## 📚 General Questions

### What is Santiago?

**Santiago is a self-bootstrapping AI agent factory** that builds specialized AI agents (Santiagos) for specific domains. Unlike traditional AI systems, Santiago operates as a **contractor factory**—you hire specialized agents for specific work, they complete the job, and the factory learns from each engagement to improve itself.

### How is Santiago different from other AI systems?

| Aspect | Santiago | Traditional AI |
|--------|----------|----------------|
| **Architecture** | Factory pattern with specialized agents | General-purpose models |
| **Domain Focus** | Deep expertise in specific domains | Broad but shallow capabilities |
| **Learning** | Self-improvement through each build | Training on large datasets |
| **Trust** | Provenance tracking and validation | Statistical confidence |
| **Ownership** | Clear work ownership and contracts | Ambiguous responsibility |

### What domains does Santiago support?

Currently supported domains:
- **Clinical Intelligence**: Medical decision support and research
- **Product Management**: Development lifecycle and stakeholder management
- **Software Development**: Code generation, testing, and deployment
- **Quality Assurance**: Testing frameworks and validation
- **System Architecture**: Technical design and scalability

### How do I get started?

1. **Choose your path** based on your role (developer, agent, architect, etc.)
2. **Follow the getting started guide** for your role
3. **Set up your environment** (Python 3.11+, Git, Docker)
4. **Start with simple tasks** to learn the system
5. **Contribute back** improvements and documentation

---

## 🚀 Getting Started Issues

### Installation fails with Python version error

**Problem**: `python setup.py install` fails with "Python 3.11+ required"

**Solution**:
```bash
# Check your Python version
python --version

# If < 3.11, install Python 3.11+
# macOS with Homebrew
brew install python@3.11

# Ubuntu/Debian
sudo apt-get install python3.11 python3.11-venv

# Use Python 3.11 explicitly
python3.11 -m venv venv
source venv/bin/activate
python3.11 -m pip install -e .
```

### Import errors after installation

**Problem**: `ModuleNotFoundError` when importing Santiago modules

**Solutions**:

1. **Check virtual environment**:
   ```bash
   source venv/bin/activate
   which python  # Should point to venv
   ```

2. **Reinstall in development mode**:
   ```bash
   pip install -e .
   ```

3. **Check PYTHONPATH**:
   ```bash
   python -c "import sys; print(sys.path)"
   # Should include the project root
   ```

4. **Clear cache and reinstall**:
   ```bash
   # Clear pip cache
   pip cache purge

   # Remove and recreate venv
   rm -rf venv
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -e .
   ```

### Docker build fails

**Problem**: `make docker-build` fails with various errors

**Solutions**:

1. **Check Docker installation**:
   ```bash
   docker --version
   docker run hello-world
   ```

2. **Increase Docker resources** (Docker Desktop):
   - CPUs: 2+
   - Memory: 4GB+
   - Disk: 20GB+

3. **Clean Docker cache**:
   ```bash
   docker system prune -a
   ```

4. **Build with no cache**:
   ```bash
   make docker-build DOCKER_BUILD_OPTS="--no-cache"
   ```

---

## 🔧 Development Issues

### Tests fail with import errors

**Problem**: `pytest` fails with module import errors

**Solutions**:

1. **Install test dependencies**:
   ```bash
   pip install -e ".[dev]"
   ```

2. **Run from correct directory**:
   ```bash
   cd /path/to/santiago-factory
   python -m pytest tests/
   ```

3. **Check test configuration**:
   ```bash
   # Ensure pytest.ini or pyproject.toml is correct
   cat pytest.ini
   ```

### Code formatting/linting fails

**Problem**: `make lint` or `make format` fails

**Solutions**:

1. **Install development tools**:
   ```bash
   pip install black isort flake8 mypy
   ```

2. **Run formatters individually**:
   ```bash
   # Format code
   black .
   isort .

   # Check types
   mypy santiago_core/

   # Lint
   flake8 santiago_core/
   ```

3. **Fix common issues**:
   - **Line too long**: Break long lines
   - **Unused imports**: Remove unused imports
   - **Type hints**: Add missing type annotations

### Git workflow issues

**Problem**: Merge conflicts, branch issues, or commit problems

**Solutions**:

1. **Sync with main**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b my-feature
   ```

2. **Resolve conflicts**:
   ```bash
   git status
   # Edit conflicted files
   git add <resolved-files>
   git commit
   ```

3. **Clean up branches**:
   ```bash
   git branch -d my-old-branch  # Delete merged branch
   git remote prune origin      # Clean remote branches
   ```

---

## 🤖 Agent Integration Issues

### Cannot connect to Santiago agents

**Problem**: MCP or API connections fail

**Solutions**:

1. **Check service status**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Verify configuration**:
   ```bash
   # Check .env file
   cat .env | grep -E "(HOST|PORT|API_KEY)"
   ```

3. **Restart services**:
   ```bash
   make docker-restart
   # or
   python santiago_core/run_team.py
   ```

4. **Check network/firewall**:
   ```bash
   telnet localhost 8000
   ```

### Agent responses are slow or timeout

**Problem**: Agent tasks take too long or timeout

**Solutions**:

1. **Check system resources**:
   ```bash
   # CPU usage
   top

   # Memory usage
   free -h

   # Disk I/O
   iostat
   ```

2. **Optimize task size**:
   ```python
   # Break large tasks into smaller ones
   small_tasks = split_large_task(big_task)
   results = await execute_parallel(small_tasks)
   ```

3. **Use caching**:
   ```python
   from santiago_core.cache import ResultCache

   cache = ResultCache()
   result = await cache.get_or_compute(task, compute_function)
   ```

4. **Monitor agent metrics**:
   ```python
   metrics = await monitor.get_agent_metrics(agent_id)
   print(f"Queue length: {metrics['queue_length']}")
   ```

### Knowledge graph queries return no results

**Problem**: SPARQL queries return empty results

**Solutions**:

1. **Check query syntax**:
   ```sparql
   # Test basic query
   SELECT * WHERE { ?s ?p ?o } LIMIT 10
   ```

2. **Verify data loading**:
   ```bash
   # Check if knowledge base is populated
   python -c "from santiago_core.knowledge import KG; kg = KG(); print(kg.stats())"
   ```

3. **Use semantic search**:
   ```python
   # Fallback to semantic search
   results = await semantic_search.find("your query", threshold=0.3)
   ```

4. **Check namespace/prefixes**:
   ```sparql
   # Use correct prefixes
   PREFIX santiago: <http://santiago/>
   SELECT * WHERE { santiago:entity santiago:property ?value }
   ```

---

## 🏗️ Architecture & Design Issues

### How do I add a new agent type?

**Solution**: Follow the agent development pattern:

1. **Create agent class**:
   ```python
   from santiago_core.agents import BaseAgent

   class NewDomainAgent(BaseAgent):
       def __init__(self):
           super().__init__(agent_type="new-domain")
           self.capabilities = ["analysis", "generation", "validation"]
   ```

2. **Implement required methods**:
   ```python
   async def analyze(self, context):
       # Domain analysis logic
       pass

   async def generate(self, requirements):
       # Content generation logic
       pass

   async def validate(self, result):
       # Quality validation logic
       pass
   ```

3. **Add to factory**:
   ```python
   # In agent factory
   factory.register_agent("new-domain", NewDomainAgent)
   ```

4. **Create knowledge domain**:
   ```python
   # Set up domain knowledge
   kg.create_domain("new_domain", ontology=new_ontology)
   ```

### How do I extend existing agent capabilities?

**Solution**: Use the extension pattern:

```python
from santiago_core.agents import AgentExtension

class CustomCapability(AgentExtension):
    def __init__(self, agent):
        self.agent = agent

    async def custom_method(self, params):
        # Custom logic
        pass

# Add to agent
agent.add_extension(CustomCapability(agent))
```

### How do I add new knowledge domains?

**Solution**: Define ontology and populate knowledge:

1. **Create ontology**:
   ```python
   ontology = {
       "classes": ["Entity", "Concept", "Relationship"],
       "properties": ["hasProperty", "relatedTo", "instanceOf"],
       "axioms": ["domain-specific rules"]
   }
   ```

2. **Set up knowledge graph domain**:
   ```python
   kg.create_domain("new_domain", ontology=ontology)
   ```

3. **Populate with data**:
   ```python
   kg.add_fact("entity1", "hasProperty", "value1", domain="new_domain")
   ```

---

## 🚀 Performance Issues

### High memory usage

**Problem**: Santiago consumes too much RAM

**Solutions**:

1. **Enable memory profiling**:
   ```python
   from memory_profiler import profile

   @profile
   def memory_intensive_function():
       pass
   ```

2. **Use streaming for large datasets**:
   ```python
   # Instead of loading all data
   for chunk in data_stream:
       process_chunk(chunk)
   ```

3. **Implement caching**:
   ```python
   from santiago_core.cache import LRUCache

   cache = LRUCache(max_size=1000)
   result = cache.get_or_compute(key, expensive_function)
   ```

4. **Monitor memory usage**:
   ```python
   import psutil
   process = psutil.Process()
   print(f"Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB")
   ```

### Slow response times

**Problem**: API calls or agent responses are slow

**Solutions**:

1. **Profile performance**:
   ```python
   import cProfile
   cProfile.run('your_function()', 'profile_output.prof')
   ```

2. **Optimize database queries**:
   ```sql
   -- Add indexes
   CREATE INDEX idx_entity_property ON facts(entity, property);

   -- Use EXPLAIN to analyze queries
   EXPLAIN SELECT * FROM facts WHERE entity = 'target';
   ```

3. **Implement connection pooling**:
   ```python
   from santiago_core.connection import ConnectionPool

   pool = ConnectionPool(max_connections=20, timeout=30)
   ```

4. **Use async processing**:
   ```python
   # Instead of synchronous calls
   results = await asyncio.gather(*[process_item(item) for item in items])
   ```

### Database connection issues

**Problem**: Cannot connect to knowledge graph database

**Solutions**:

1. **Check database status**:
   ```bash
   # For PostgreSQL
   pg_isready -h localhost -p 5432

   # For SQLite
   sqlite3 knowledge.db "SELECT COUNT(*) FROM facts;"
   ```

2. **Verify connection string**:
   ```python
   # Check .env configuration
   import os
   db_url = os.getenv('DATABASE_URL')
   print(f"DB URL: {db_url}")
   ```

3. **Test connection**:
   ```python
   from santiago_core.database import Database

   db = Database()
   try:
       await db.connect()
       print("✅ Database connection successful")
   except Exception as e:
       print(f"❌ Connection failed: {e}")
   ```

---

## 🔒 Security & Compliance

### API authentication issues

**Problem**: Cannot authenticate API requests

**Solutions**:

1. **Check API key**:
   ```bash
   # Verify API key in .env
   grep API_KEY .env
   ```

2. **Use correct headers**:
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" \
        -H "Content-Type: application/json" \
        http://localhost:8000/agents
   ```

3. **Verify token expiration**:
   ```python
   import jwt
   # Decode and check exp claim
   decoded = jwt.decode(token, verify=False)
   print(f"Expires: {decoded.get('exp')}")
   ```

### Data privacy concerns

**Problem**: Need to ensure data privacy and compliance

**Solutions**:

1. **Use encryption**:
   ```python
   from cryptography.fernet import Fernet

   key = Fernet.generate_key()
   cipher = Fernet(key)

   encrypted = cipher.encrypt(b"sensitive data")
   decrypted = cipher.decrypt(encrypted)
   ```

2. **Implement access controls**:
   ```python
   from santiago_core.auth import AccessControl

   acl = AccessControl()
   if acl.has_permission(user, "read", resource):
       return resource_data
   ```

3. **Audit logging**:
   ```python
   from santiago_core.audit import AuditLogger

   logger = AuditLogger()
   logger.log_access(user, action, resource, success=True)
   ```

---

## 📊 Monitoring & Observability

### How do I monitor agent performance?

**Solution**: Use the monitoring APIs:

```python
from santiago_core.monitoring import AgentMonitor

monitor = AgentMonitor()

# Get agent metrics
metrics = monitor.get_agent_metrics("santiago-developer")
print(f"Success rate: {metrics['success_rate']}%")
print(f"Average response time: {metrics['avg_response_time']}ms")

# Get system health
health = monitor.get_system_health()
print(f"Overall status: {health['status']}")
```

### How do I debug failed tasks?

**Solution**: Use the debugging tools:

```python
from santiago_core.debug import TaskDebugger

debugger = TaskDebugger()

# Analyze failed task
analysis = debugger.analyze_failure(task_id)
print(f"Failure reason: {analysis['reason']}")
print(f"Suggested fixes: {analysis['fixes']}")

# Get execution trace
trace = debugger.get_execution_trace(task_id)
for step in trace:
    print(f"{step['timestamp']}: {step['action']} - {step['status']}")
```

---

## 🤝 Contributing & Community

### How do I report bugs?

**Solution**: Follow the bug reporting process:

1. **Check existing issues**:
   ```bash
   # Search for similar issues
   gh issue list --search "bug title"
   ```

2. **Create detailed issue**:
   - Clear title describing the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Logs and error messages

3. **Use issue templates** when available

### How do I contribute code?

**Solution**: Follow the contribution workflow:

1. **Claim work** using kanban:
   ```bash
   python -m tackle.kanban.kanban_cli claim-next exp-057-migration --agent "your-name"
   ```

2. **Follow TDD/BDD**:
   - Write tests first
   - Implement minimal code
   - Refactor for quality

3. **Create PR**:
   ```bash
   gh pr create --title "feat: Add new feature" --body "Closes #123"
   ```

4. **Address review feedback**

### How do I get help?

**Solutions**:

1. **Check documentation first**:
   - This FAQ
   - Troubleshooting guide
   - API documentation

2. **Search existing resources**:
   - GitHub issues
   - Discussions
   - Stack Overflow

3. **Ask the community**:
   - Create GitHub discussion
   - Join community calls
   - Post on forums

4. **Contact maintainers** (for urgent issues)

---

## 🔄 Version & Migration

### How do I upgrade Santiago?

**Solution**: Follow the upgrade process:

1. **Check release notes**:
   ```bash
   # View latest changes
   git log --oneline v1.0..HEAD
   ```

2. **Backup data**:
   ```bash
   # Backup knowledge graph
   pg_dump knowledge_db > backup.sql
   ```

3. **Update code**:
   ```bash
   git pull origin main
   pip install -e . --upgrade
   ```

4. **Run migrations**:
   ```bash
   # Run database migrations
   python santiago_core/migrations/run_migrations.py

   # Update configurations
   python santiago_core/migrations/update_config.py
   ```

5. **Test upgrade**:
   ```bash
   make test
   make test-integration
   ```

### Breaking changes between versions

**Problem**: Code breaks after upgrade

**Solutions**:

1. **Check migration guide**:
   ```bash
   cat MIGRATION_GUIDE.md
   ```

2. **Update deprecated APIs**:
   ```python
   # Old way (deprecated)
   result = agent.execute_task(task)

   # New way
   result = await agent.execute_task_async(task)
   ```

3. **Use compatibility layer** (if available):
   ```python
   from santiago_core.compat import CompatibilityLayer

   compat = CompatibilityLayer()
   result = compat.execute_task(agent, task)  # Works with old and new APIs
   ```

---

*This FAQ is continuously updated. If you have a question that's not covered here, please create an issue or discussion on GitHub. Your questions help improve the documentation for everyone!*