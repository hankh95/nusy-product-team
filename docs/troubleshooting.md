# 🔧 Troubleshooting Guide

Comprehensive troubleshooting guide for common Santiago issues, with diagnostic procedures and solutions.

---

## 📋 Quick Diagnosis

### System Health Check

Run this first when encountering issues:

```bash
# Check overall system health
curl -s http://localhost:8000/health | jq .

# Check detailed health
curl -s http://localhost:8000/health/detailed | jq .

# Check database connectivity
curl -s http://localhost:8000/health/database | jq .

# Check knowledge graph
curl -s http://localhost:8000/health/knowledge-graph | jq .
```

Expected healthy response:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "uptime": "2d 4h 30m",
  "services": {
    "database": "healthy",
    "knowledge_graph": "healthy",
    "agent_factory": "healthy"
  }
}
```

---

## 🚨 Critical Issues

### System Won't Start

**Symptoms:**
- Docker containers fail to start
- Services crash immediately
- Port binding errors

**Diagnostic Steps:**

1. **Check Docker status:**
   ```bash
   docker ps -a
   docker logs santiago-api
   ```

2. **Check configuration:**
   ```bash
   # Validate .env file
   cat .env | grep -E "(HOST|PORT|PASSWORD)" | grep -v "PASSWORD"

   # Check for syntax errors
   python -c "import dotenv; dotenv.load_dotenv('.env'); print('Config OK')"
   ```

3. **Check resource availability:**
   ```bash
   # Memory
   free -h

   # Disk space
   df -h

   # CPU
   top -n 1
   ```

**Common Solutions:**

1. **Port conflicts:**
   ```bash
   # Find what's using port 8000
   lsof -i :8000

   # Change port in docker-compose.yml
   sed -i 's/8000:8000/8001:8000/' docker-compose.yml
   ```

2. **Memory issues:**
   ```bash
   # Increase Docker memory limit
   # Docker Desktop: Preferences > Resources > Memory > 4GB+

   # Or add memory limits to docker-compose.yml
   services:
     api:
       deploy:
         resources:
           limits:
             memory: 2G
           reservations:
             memory: 512M
   ```

3. **Configuration errors:**
   ```bash
   # Validate environment variables
   python -c "
   import os
   required = ['SANTIAGO_API_KEY', 'DATABASE_URL']
   missing = [k for k in required if not os.getenv(k)]
   if missing:
       print(f'Missing: {missing}')
   else:
       print('All required vars present')
   "
   ```

### Database Connection Failed

**Symptoms:**
- "Connection refused" errors
- Database health check fails
- Tasks fail with database errors

**Diagnostic Steps:**

1. **Check database service:**
   ```bash
   # Docker Compose
   docker-compose ps postgres

   # Kubernetes
   kubectl get pods -n santiago -l app=postgres

   # Direct connection
   pg_isready -h localhost -p 5432
   ```

2. **Check connection string:**
   ```bash
   # Test connection
   psql $DATABASE_URL -c "SELECT 1"

   # Or with explicit parameters
   psql -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER -d $POSTGRES_DB -c "SELECT 1"
   ```

3. **Check database logs:**
   ```bash
   # Docker
   docker logs santiago-postgres

   # Kubernetes
   kubectl logs -n santiago -l app=postgres
   ```

**Common Solutions:**

1. **Database not started:**
   ```bash
   # Start database service
   docker-compose up -d postgres

   # Wait for startup
   sleep 30
   ```

2. **Wrong connection parameters:**
   ```bash
   # Check environment variables
   echo $DATABASE_URL
   echo $POSTGRES_HOST
   echo $POSTGRES_PORT

   # Test with correct values
   export DATABASE_URL="postgresql://santiago:password@localhost:5432/santiago"
   ```

3. **Database initialization issues:**
   ```bash
   # Check if database exists
   psql -h localhost -U postgres -c "SELECT datname FROM pg_database WHERE datname = 'santiago'"

   # Create database if missing
   psql -h localhost -U postgres -c "CREATE DATABASE santiago OWNER santiago"
   ```

### Knowledge Graph Unavailable

**Symptoms:**
- SPARQL queries fail
- Knowledge-related features don't work
- Graph health check fails

**Diagnostic Steps:**

1. **Check Neo4j service:**
   ```bash
   # Docker
   docker-compose ps neo4j

   # Kubernetes
   kubectl get pods -n santiago -l app=neo4j

   # Direct connection
   curl -s http://localhost:7474 | head -5
   ```

2. **Check graph database logs:**
   ```bash
   # Docker
   docker logs santiago-neo4j

   # Kubernetes
   kubectl logs -n santiago -l app=neo4j
   ```

3. **Test basic connectivity:**
   ```bash
   # Using cypher-shell
   cypher-shell -u neo4j -p $GRAPH_PASSWORD "MATCH () RETURN count(*) as nodes"
   ```

**Common Solutions:**

1. **Neo4j not started:**
   ```bash
   docker-compose up -d neo4j
   sleep 60  # Neo4j takes time to start
   ```

2. **Authentication issues:**
   ```bash
   # Reset password if needed
   docker exec -it santiago-neo4j neo4j-admin set-initial-password newpassword
   ```

3. **Memory issues:**
   ```bash
   # Increase Neo4j memory
   # In docker-compose.yml
   neo4j:
     environment:
       NEO4J_dbms_memory_heap_initial__size: 512m
       NEO4J_dbms_memory_heap_max__size: 2G
       NEO4J_dbms_memory_pagecache_size: 512m
   ```

---

## ⚠️ Performance Issues

### Slow API Responses

**Symptoms:**
- API calls take >5 seconds
- High latency in monitoring
- Timeout errors

**Diagnostic Steps:**

1. **Check system resources:**
   ```bash
   # CPU usage
   top -n 1 | head -10

   # Memory usage
   free -h

   # Disk I/O
   iostat -x 1 5
   ```

2. **Check database performance:**
   ```sql
   -- Slow queries
   SELECT query, total_time/calls as avg_time, calls
   FROM pg_stat_statements
   ORDER BY total_time DESC
   LIMIT 10;

   -- Active connections
   SELECT count(*) FROM pg_stat_activity;

   -- Table bloat
   SELECT schemaname, tablename, n_dead_tup, n_live_tup
   FROM pg_stat_user_tables
   ORDER BY n_dead_tup DESC;
   ```

3. **Check application metrics:**
   ```bash
   # Response time percentiles
   curl -s http://localhost:8000/metrics | grep santiago_request_duration

   # Active connections
   curl -s http://localhost:8000/metrics | grep santiago_active_connections
   ```

**Common Solutions:**

1. **Database optimization:**
   ```sql
   -- Analyze tables
   ANALYZE;

   -- Vacuum dead tuples
   VACUUM ANALYZE;

   -- Add missing indexes
   CREATE INDEX CONCURRENTLY idx_tasks_status_created ON tasks(status, created_at);
   ```

2. **Connection pooling:**
   ```python
   # In application config
   DATABASE_POOL_MIN = 5
   DATABASE_POOL_MAX = 20
   DATABASE_POOL_TIMEOUT = 30
   ```

3. **Caching:**
   ```bash
   # Enable Redis caching
   export REDIS_URL=redis://localhost:6379

   # Restart services
   docker-compose restart api
   ```

4. **Horizontal scaling:**
   ```bash
   # Scale API instances
   docker-compose up -d --scale api=3
   ```

### High Memory Usage

**Symptoms:**
- Out of memory errors
- Services restarting
- Slow performance

**Diagnostic Steps:**

1. **Check memory usage:**
   ```bash
   # Container memory
   docker stats

   # Process memory
   ps aux --sort=-%mem | head -10

   # Application memory profiling
   python -c "
   import psutil
   process = psutil.Process()
   print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.1f} MB')
   "
   ```

2. **Check for memory leaks:**
   ```python
   # Add memory profiling
   from memory_profiler import profile

   @profile
   def memory_intensive_function():
       # Your code here
       pass
   ```

**Common Solutions:**

1. **Increase memory limits:**
   ```yaml
   # docker-compose.yml
   services:
     api:
       deploy:
         resources:
           limits:
             memory: 2G
           reservations:
             memory: 512M
   ```

2. **Optimize memory usage:**
   ```python
   # Use streaming for large datasets
   def process_large_file(file_path):
       with open(file_path, 'r') as f:
           for line in f:  # Process line by line
               process_line(line)
   ```

3. **Enable garbage collection tuning:**
   ```bash
   export PYTHONOPTIMIZE=1
   export PYTHONMALLOC=malloc
   ```

### Task Queue Backlog

**Symptoms:**
- Tasks not processing
- Queue length growing
- Task timeout errors

**Diagnostic Steps:**

1. **Check queue status:**
   ```bash
   # Queue length
   curl -s http://localhost:8000/metrics | grep queue_length

   # Active workers
   curl -s http://localhost:8000/metrics | grep active_workers
   ```

2. **Check worker processes:**
   ```bash
   # Running workers
   ps aux | grep worker

   # Worker logs
   docker logs santiago-worker
   ```

3. **Check task distribution:**
   ```sql
   -- Tasks by status
   SELECT status, count(*) FROM tasks GROUP BY status;

   -- Oldest queued tasks
   SELECT id, type, created_at FROM tasks
   WHERE status = 'queued'
   ORDER BY created_at ASC LIMIT 10;
   ```

**Common Solutions:**

1. **Scale workers:**
   ```bash
   # Increase worker count
   docker-compose up -d --scale worker=5
   ```

2. **Optimize task processing:**
   ```python
   # Batch task processing
   async def process_tasks_batch(tasks):
       # Process multiple tasks concurrently
       results = await asyncio.gather(*[
           process_task(task) for task in tasks
       ])
       return results
   ```

3. **Clear stuck tasks:**
   ```sql
   -- Reset stuck tasks (use carefully!)
   UPDATE tasks SET status = 'queued', started_at = NULL
   WHERE status = 'in_progress'
   AND started_at < NOW() - INTERVAL '1 hour';
   ```

---

## 🔧 Agent Issues

### Agent Not Responding

**Symptoms:**
- Agent status shows "busy" indefinitely
- Tasks assigned to agent don't complete
- Agent health checks fail

**Diagnostic Steps:**

1. **Check agent status:**
   ```bash
   # Agent list
   curl -s http://localhost:8000/api/v1/agents | jq .

   # Specific agent
   curl -s http://localhost:8000/api/v1/agents/agent-123 | jq .
   ```

2. **Check agent logs:**
   ```bash
   # Docker
   docker logs santiago-agent-123

   # Kubernetes
   kubectl logs -n santiago -l agent=agent-123
   ```

3. **Test agent connectivity:**
   ```bash
   # MCP ping
   echo '{"jsonrpc": "2.0", "id": 1, "method": "ping"}' | \
   websocat ws://localhost:8000/mcp
   ```

**Common Solutions:**

1. **Restart agent:**
   ```bash
   # Docker
   docker restart santiago-agent-123

   # Kubernetes
   kubectl delete pod -n santiago -l agent=agent-123
   ```

2. **Check agent configuration:**
   ```python
   # Validate agent config
   from santiago.agents import AgentConfig

   config = AgentConfig.from_env()
   print(f"Agent type: {config.type}")
   print(f"Capabilities: {config.capabilities}")
   ```

3. **Update agent software:**
   ```bash
   # Pull latest image
   docker pull santiago/agent:latest

   # Restart with new image
   docker-compose up -d agent-123
   ```

### Agent Quality Degradation

**Symptoms:**
- Lower quality scores
- More failed tasks
- Inconsistent results

**Diagnostic Steps:**

1. **Check performance metrics:**
   ```bash
   # Agent performance
   curl -s http://localhost:8000/api/v1/analytics/agents/agent-123/performance | jq .
   ```

2. **Review recent tasks:**
   ```sql
   SELECT id, quality_score, error_message
   FROM task_results
   WHERE agent_id = 'agent-123'
   ORDER BY created_at DESC LIMIT 20;
   ```

3. **Check agent learning:**
   ```bash
   # Learning history
   curl -s http://localhost:8000/api/v1/agents/agent-123/learning | jq .
   ```

**Common Solutions:**

1. **Retraining:**
   ```bash
   # Trigger agent retraining
   curl -X POST \
     -H "Authorization: Bearer $SANTIAGO_API_KEY" \
     http://localhost:8000/api/v1/agents/agent-123/retrain
   ```

2. **Update knowledge base:**
   ```bash
   # Refresh agent knowledge
   curl -X POST \
     -H "Authorization: Bearer $SANTIAGO_API_KEY" \
     http://localhost:8000/api/v1/agents/agent-123/update-knowledge
   ```

3. **Adjust parameters:**
   ```python
   # Fine-tune agent parameters
   agent.update_config({
       'temperature': 0.3,  # More deterministic
       'max_tokens': 1500,  # Shorter responses
       'quality_threshold': 0.9
   })
   ```

---

## 🔗 Integration Issues

### MCP Connection Problems

**Symptoms:**
- WebSocket connection fails
- Tool calls return errors
- Agent integration doesn't work

**Diagnostic Steps:**

1. **Test WebSocket connection:**
   ```bash
   # Basic connectivity
   websocat ws://localhost:8000/mcp

   # With authentication
   echo '{"jsonrpc": "2.0", "id": 1, "method": "ping"}' | \
   websocat -H "Authorization: Bearer $AGENT_TOKEN" ws://localhost:8000/mcp
   ```

2. **Check MCP logs:**
   ```bash
   docker logs santiago-api | grep -i mcp
   ```

3. **Validate agent token:**
   ```bash
   # Test token
   curl -H "Authorization: Bearer $AGENT_TOKEN" \
        http://localhost:8000/api/v1/auth/validate-token
   ```

**Common Solutions:**

1. **Fix WebSocket issues:**
   ```nginx
   # Nginx proxy for WebSocket
   location /mcp {
       proxy_pass http://santiago_api;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection "upgrade";
       proxy_set_header Host $host;
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_set_header X-Forwarded-Proto $scheme;
   }
   ```

2. **Regenerate agent token:**
   ```bash
   # Get new token
   curl -X POST \
     -H "Authorization: Bearer $SANTIAGO_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"agent_id": "my-agent", "capabilities": ["code-review"]}' \
     http://localhost:8000/api/v1/auth/agent-token
   ```

### API Authentication Issues

**Symptoms:**
- 401 Unauthorized errors
- API calls rejected
- Authentication failures

**Diagnostic Steps:**

1. **Check API key:**
   ```bash
   # Validate API key format
   echo $SANTIAGO_API_KEY | wc -c  # Should be ~100+ chars

   # Test API key
   curl -H "Authorization: Bearer $SANTIAGO_API_KEY" \
        http://localhost:8000/api/v1/auth/validate
   ```

2. **Check token expiration:**
   ```bash
   # Decode JWT (if using JWT)
   python -c "
   import jwt
   token = '$SANTIAGO_API_KEY'
   decoded = jwt.decode(token, verify=False)
   print('Expires:', decoded.get('exp'))
   "
   ```

**Common Solutions:**

1. **Regenerate API key:**
   ```bash
   # Through web interface or API
   curl -X POST \
     -H "Authorization: Bearer $OLD_API_KEY" \
     http://localhost:8000/api/v1/auth/regenerate-key
   ```

2. **Fix authorization header:**
   ```bash
   # Ensure correct format
   curl -H "Authorization: Bearer $SANTIAGO_API_KEY" \
        http://localhost:8000/api/v1/agents
   ```

---

## 💾 Data Issues

### Knowledge Graph Corruption

**Symptoms:**
- SPARQL queries return wrong results
- Missing knowledge facts
- Graph integrity errors

**Diagnostic Steps:**

1. **Check graph integrity:**
   ```cypher
   // Neo4j browser or cypher-shell
   MATCH (n) RETURN count(n) as nodes;
   MATCH ()-[r]-() RETURN count(r) as relationships;
   ```

2. **Validate data consistency:**
   ```bash
   # Run consistency check
   python -c "
   from santiago.knowledge import KnowledgeGraph
   kg = KnowledgeGraph()
   issues = kg.check_consistency()
   print('Consistency issues:', issues)
   "
   ```

**Common Solutions:**

1. **Repair graph data:**
   ```cypher
   // Remove orphaned nodes
   MATCH (n)
   WHERE NOT (n)--()
   DELETE n;

   // Fix constraint violations
   // (depends on your schema)
   ```

2. **Rebuild from backup:**
   ```bash
   # Stop services
   docker-compose down

   # Restore from backup
   neo4j-admin database load neo4j --from-path=/backups/neo4j --overwrite-destination=true

   # Restart services
   docker-compose up -d
   ```

### Database Corruption

**Symptoms:**
- PostgreSQL errors
- Data inconsistency
- Failed queries

**Diagnostic Steps:**

1. **Check database health:**
   ```bash
   # PostgreSQL logs
   docker logs santiago-postgres

   # Run diagnostics
   psql -c "SELECT version();"
   psql -c "SELECT * FROM pg_stat_database WHERE datname = 'santiago';"
   ```

2. **Check for corruption:**
   ```sql
   -- Check table integrity
   SELECT tablename, n_tup_ins, n_tup_upd, n_tup_del, n_live_tup, n_dead_tup
   FROM pg_stat_user_tables;

   -- Check indexes
   SELECT indexname, tablename, indisvalid
   FROM pg_indexes i
   JOIN pg_class c ON c.oid = i.indexrelid
   WHERE indisvalid = false;
   ```

**Common Solutions:**

1. **Repair corruption:**
   ```sql
   -- Reindex corrupted indexes
   REINDEX INDEX CONCURRENTLY corrupted_index_name;

   -- Vacuum full (expensive, use carefully)
   VACUUM FULL corrupted_table_name;
   ```

2. **Restore from backup:**
   ```bash
   # Stop application
   docker-compose stop api

   # Restore database
   gunzip < /backups/santiago.sql.gz | psql

   # Restart application
   docker-compose start api
   ```

---

## 🔄 Recovery Procedures

### Full System Recovery

1. **Assess damage:**
   ```bash
   # Check what services are affected
   docker-compose ps

   # Check logs for error patterns
   docker-compose logs --tail=100
   ```

2. **Stop all services:**
   ```bash
   docker-compose down
   ```

3. **Restore from backups:**
   ```bash
   # Restore databases
   make restore-database
   make restore-knowledge-graph

   # Clear caches
   docker run --rm -v santiago_redis:/data redis:alpine redis-cli -h redis FLUSHALL
   ```

4. **Restart services:**
   ```bash
   docker-compose up -d
   ```

5. **Verify recovery:**
   ```bash
   # Health checks
   curl http://localhost:8000/health

   # Basic functionality
   curl -H "Authorization: Bearer $SANTIAGO_API_KEY" \
        http://localhost:8000/api/v1/agents
   ```

### Emergency Shutdown

When system is unstable:

```bash
# Immediate shutdown
docker-compose down --timeout 10

# Force kill if needed
docker kill $(docker ps -q)

# Clean up
docker system prune -f
```

### Data Export for Migration

```bash
# Export knowledge graph
docker exec santiago-neo4j neo4j-admin database dump neo4j --to-path=/tmp/export

# Export database
docker exec santiago-postgres pg_dump -U santiago santiago > /tmp/santiago.sql

# Copy files out
docker cp santiago-neo4j:/tmp/export ./export
docker cp santiago-postgres:/tmp/santiago.sql ./santiago.sql
```

---

## 📊 Diagnostic Tools

### System Information Script

```bash
#!/bin/bash
# diagnostic.sh

echo "=== Santiago Diagnostic Report ==="
echo "Timestamp: $(date)"
echo "Hostname: $(hostname)"
echo ""

echo "=== Docker Status ==="
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

echo "=== Resource Usage ==="
echo "Memory:"
free -h
echo ""
echo "Disk:"
df -h
echo ""

echo "=== Service Health ==="
services=("api" "postgres" "neo4j" "redis")
for service in "${services[@]}"; do
    if docker-compose ps $service | grep -q "Up"; then
        echo "✅ $service: Healthy"
    else
        echo "❌ $service: Unhealthy"
    fi
done
echo ""

echo "=== Recent Logs ==="
docker-compose logs --tail=20
echo ""

echo "=== Configuration Check ==="
if [ -f .env ]; then
    echo "✅ .env file exists"
    # Check for required variables (without showing values)
    required_vars=("SANTIAGO_API_KEY" "POSTGRES_PASSWORD" "GRAPH_DB_PASSWORD")
    for var in "${required_vars[@]}"; do
        if grep -q "^$var=" .env; then
            echo "✅ $var: Set"
        else
            echo "❌ $var: Missing"
        fi
    done
else
    echo "❌ .env file missing"
fi
```

### Performance Profiling

```python
# profiling.py
import cProfile
import pstats
from io import StringIO

def profile_function(func, *args, **kwargs):
    pr = cProfile.Profile()
    pr.enable()

    result = func(*args, **kwargs)

    pr.disable()
    s = StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())

    return result

# Usage
@profile_function
def slow_function():
    # Your code here
    pass
```

### Log Analysis

```bash
# Analyze error patterns
docker-compose logs | grep -i error | head -20

# Count errors by hour
docker-compose logs | grep -i error | awk '{print $1}' | cut -d: -f1 | sort | uniq -c

# Find slow requests
docker-compose logs | grep -E "duration=[0-9]+" | sort -k2 -n | tail -10
```

---

## 📞 Getting Help

### Support Resources

1. **Community Support:**
   - GitHub Issues: [github.com/santiago/issues](https://github.com/santiago/issues)
   - Community Forum: [community.santiago.ai](https://community.santiago.ai)
   - Stack Overflow: Tag `santiago-ai`

2. **Enterprise Support:**
   - Email: enterprise@santiago.ai
   - Phone: +1 (555) 123-4567
   - Portal: [enterprise.santiago.ai](https://enterprise.santiago.ai)

3. **Documentation:**
   - Main Docs: [docs.santiago.ai](https://docs.santiago.ai)
   - API Reference: [api.santiago.ai](https://api.santiago.ai)
   - Troubleshooting: [troubleshoot.santiago.ai](https://troubleshoot.santiago.ai)

### Information to Provide

When requesting help, include:

```bash
# System information
uname -a
docker --version
docker-compose --version

# Santiago version
curl -s http://localhost:8000/health | jq .version

# Error logs
docker-compose logs --tail=100 > santiago_logs.txt

# Configuration (redacted)
grep -v PASSWORD .env > config_redacted.txt

# Diagnostic output
./diagnostic.sh > diagnostic_report.txt
```

---

*This troubleshooting guide covers the most common issues. If you encounter an issue not covered here, please check the [GitHub issues](https://github.com/santiago/issues) or create a new issue with detailed information.*