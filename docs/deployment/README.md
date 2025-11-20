# 🚀 Deployment & Operations Guide

Complete guide for deploying, operating, and maintaining Santiago in production environments.

---

## 📋 Deployment Overview

Santiago can be deployed in multiple ways depending on your infrastructure and scaling requirements:

| Deployment Type | Use Case | Complexity | Scaling |
|----------------|----------|------------|---------|
| **Docker Compose** | Development, small teams | Low | Single node |
| **Kubernetes** | Production, large scale | Medium | Auto-scaling |
| **AWS/Azure/GCP** | Cloud-native | High | Cloud-managed |
| **On-premises** | Enterprise, air-gapped | High | Manual |

---

## 🐳 Docker Compose Deployment

### Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+
- 4GB RAM minimum
- 20GB disk space

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/santiago/santiago-factory.git
   cd santiago-factory
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Start services:**
   ```bash
   make docker-deploy
   # or
   docker-compose up -d
   ```

4. **Verify deployment:**
   ```bash
   curl http://localhost:8000/health
   ```

### Configuration

Create a `.env` file with your settings:

```bash
# API Configuration
SANTIAGO_API_KEY=your-secret-api-key
SANTIAGO_BASE_URL=http://localhost:8000

# Database
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=santiago
POSTGRES_USER=santiago
POSTGRES_PASSWORD=your-db-password

# Knowledge Graph
GRAPH_DB_URL=bolt://neo4j:7687
GRAPH_DB_USER=neo4j
GRAPH_DB_PASSWORD=your-graph-password

# Redis (optional, for caching)
REDIS_URL=redis://redis:6379

# External Services
GITHUB_TOKEN=your-github-token  # For GitHub integration
SLACK_WEBHOOK_URL=https://hooks.slack.com/...  # For notifications

# Security
JWT_SECRET=your-jwt-secret
ENCRYPTION_KEY=your-32-char-encryption-key

# Monitoring
SENTRY_DSN=https://...@sentry.io/...  # Error tracking
DATADOG_API_KEY=your-datadog-key  # Metrics
```

### Docker Compose File

```yaml
# docker-compose.yml
version: '3.8'

services:
  api:
    image: santiago/api:latest
    ports:
      - "8000:8000"
    environment:
      - SANTIAGO_ENV=production
    env_file:
      - .env
    depends_on:
      - postgres
      - neo4j
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: santiago
      POSTGRES_USER: santiago
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  neo4j:
    image: neo4j:5.15
    environment:
      NEO4J_AUTH: neo4j/${GRAPH_DB_PASSWORD}
      NEO4J_PLUGINS: '["graph-data-science"]'
    volumes:
      - neo4j_data:/data
      - neo4j_logs:/logs
    ports:
      - "7474:7474"  # HTTP
      - "7687:7687"  # Bolt
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl/certs
    depends_on:
      - api
    restart: unless-stopped

volumes:
  postgres_data:
  neo4j_data:
  neo4j_logs:
  redis_data:
```

### Nginx Configuration

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream santiago_api {
        server api:8000;
    }

    server {
        listen 80;
        server_name your-domain.com;

        # Redirect to HTTPS
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name your-domain.com;

        ssl_certificate /etc/ssl/certs/fullchain.pem;
        ssl_certificate_key /etc/ssl/certs/privkey.pem;

        # Security headers
        add_header X-Frame-Options DENY;
        add_header X-Content-Type-Options nosniff;
        add_header X-XSS-Protection "1; mode=block";
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains";

        # API endpoints
        location /api/ {
            proxy_pass http://santiago_api;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }

        # Health check
        location /health {
            proxy_pass http://santiago_api/health;
            access_log off;
        }

        # Static files (if serving frontend)
        location / {
            root /usr/share/nginx/html;
            try_files $uri $uri/ /index.html;
        }
    }
}
```

---

## ☸️ Kubernetes Deployment

### Prerequisites

- Kubernetes 1.24+
- Helm 3.0+
- kubectl configured
- 8GB RAM minimum per node
- 50GB storage per node

### Using Helm Chart

1. **Add Santiago Helm repository:**
   ```bash
   helm repo add santiago https://charts.santiago.ai
   helm repo update
   ```

2. **Install Santiago:**
   ```bash
   helm install santiago santiago/santiago \
     --namespace santiago \
     --create-namespace \
     --values values.yaml
   ```

3. **Create values.yaml:**
   ```yaml
   # values.yaml
   api:
     replicaCount: 3
     image:
       tag: "latest"
     env:
       - name: SANTIAGO_API_KEY
         valueFrom:
           secretKeyRef:
             name: santiago-secrets
             key: api-key

   database:
     enabled: true
     postgresql:
       auth:
         database: santiago
         username: santiago
         password: "your-password"

   knowledgeGraph:
     enabled: true
     neo4j:
       auth:
         password: "your-password"

   ingress:
     enabled: true
     className: nginx
     hosts:
       - host: santiago.your-domain.com
         paths:
           - path: /
             pathType: Prefix

   monitoring:
     enabled: true
     prometheus:
       enabled: true
     grafana:
       enabled: true
   ```

### Manual Kubernetes Deployment

1. **Create namespace:**
   ```bash
   kubectl create namespace santiago
   ```

2. **Apply manifests:**
   ```bash
   kubectl apply -f k8s/
   ```

3. **Check deployment:**
   ```bash
   kubectl get pods -n santiago
   kubectl get services -n santiago
   ```

### Kubernetes Manifests

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: santiago-api
  namespace: santiago
spec:
  replicas: 3
  selector:
    matchLabels:
      app: santiago-api
  template:
    metadata:
      labels:
        app: santiago-api
    spec:
      containers:
      - name: api
        image: santiago/api:latest
        ports:
        - containerPort: 8000
        envFrom:
        - secretRef:
            name: santiago-secrets
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
```

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: santiago-api
  namespace: santiago
spec:
  selector:
    app: santiago-api
  ports:
  - port: 80
    targetPort: 8000
  type: ClusterIP
```

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: santiago-ingress
  namespace: santiago
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - santiago.your-domain.com
    secretName: santiago-tls
  rules:
  - host: santiago.your-domain.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: santiago-api
            port:
              number: 80
```

### Horizontal Pod Autoscaling

```yaml
# k8s/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: santiago-api-hpa
  namespace: santiago
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: santiago-api
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## ☁️ Cloud Deployments

### AWS ECS/Fargate

1. **Create ECR repository:**
   ```bash
   aws ecr create-repository --repository-name santiago/api
   ```

2. **Build and push image:**
   ```bash
   make docker-build
   make docker-push ECR_REPO=your-repo-url
   ```

3. **Deploy with CloudFormation:**
   ```bash
   aws cloudformation deploy \
     --template-file cloudformation/santiago.yaml \
     --stack-name santiago-prod \
     --parameter-overrides ApiKey=your-key DatabasePassword=your-db-pass
   ```

### Azure Container Apps

```bash
# Deploy to Azure Container Apps
az containerapp create \
  --name santiago-api \
  --resource-group your-rg \
  --environment your-env \
  --image your-registry.azurecr.io/santiago/api:latest \
  --target-port 8000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 10 \
  --env-vars SANTIAGO_API_KEY=your-key \
  --secrets database-password=your-db-pass
```

### Google Cloud Run

```bash
# Deploy to Cloud Run
gcloud run deploy santiago-api \
  --image gcr.io/your-project/santiago/api:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8000 \
  --memory 1Gi \
  --cpu 1 \
  --min-instances 1 \
  --max-instances 10 \
  --set-env-vars SANTIAGO_API_KEY=your-key \
  --set-secrets DATABASE_PASSWORD=database-password:latest
```

---

## 🔧 Configuration Management

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SANTIAGO_API_KEY` | API authentication key | - | Yes |
| `SANTIAGO_ENV` | Environment (development/production) | development | No |
| `DATABASE_URL` | PostgreSQL connection URL | - | Yes |
| `GRAPH_DB_URL` | Neo4j connection URL | - | Yes |
| `REDIS_URL` | Redis connection URL | - | No |
| `JWT_SECRET` | JWT signing secret | - | Yes |
| `ENCRYPTION_KEY` | Data encryption key (32 chars) | - | Yes |
| `LOG_LEVEL` | Logging level | INFO | No |
| `SENTRY_DSN` | Sentry error tracking | - | No |
| `CORS_ORIGINS` | CORS allowed origins | - | No |

### Secrets Management

#### Using Kubernetes Secrets

```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: santiago-secrets
  namespace: santiago
type: Opaque
data:
  api-key: <base64-encoded-key>
  database-password: <base64-encoded-password>
  jwt-secret: <base64-encoded-secret>
  encryption-key: <base64-encoded-key>
```

#### Using AWS Secrets Manager

```python
# config/secrets.py
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name):
    client = boto3.client('secretsmanager')
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        raise Exception(f"Failed to retrieve secret: {e}")

# Usage
api_key = get_secret('santiago/api-key')
db_password = get_secret('santiago/database-password')
```

#### Using HashiCorp Vault

```python
# config/vault_secrets.py
import hvac

def get_vault_secrets():
    client = hvac.Client(url='https://vault.your-domain.com')
    client.auth.approximate_token('your-token')

    secrets = client.secrets.kv.v2.read_secret_version(
        path='santiago/prod',
        mount_point='secret'
    )

    return secrets['data']['data']

# Usage
secrets = get_vault_secrets()
api_key = secrets['api_key']
```

---

## 📊 Monitoring & Observability

### Health Checks

Santiago provides multiple health check endpoints:

```bash
# Overall health
curl https://your-domain.com/health

# Detailed health
curl https://your-domain.com/health/detailed

# Database health
curl https://your-domain.com/health/database

# Knowledge graph health
curl https://your-domain.com/health/knowledge-graph
```

### Metrics Collection

#### Prometheus Metrics

Santiago exposes Prometheus metrics at `/metrics`:

```python
# Example metrics
santiago_requests_total{endpoint="/api/tasks", method="POST", status="200"} 150
santiago_request_duration_seconds{endpoint="/api/tasks", quantile="0.5"} 0.15
santiago_agents_active_total 5
santiago_tasks_queue_length 12
santiago_knowledge_facts_total 15420
```

#### Custom Metrics

```python
from santiago.monitoring import MetricsCollector

metrics = MetricsCollector()

# Counter metrics
metrics.increment('tasks_submitted', tags={'type': 'code-review'})

# Gauge metrics
metrics.gauge('active_agents', 5)

# Histogram metrics
with metrics.timer('task_execution_time', tags={'type': 'code-review'}):
    # Execute task
    result = execute_task(task)
```

### Logging

#### Structured Logging

```python
import structlog
from santiago.logging import SantiagoLogger

logger = SantiagoLogger()

# Structured log entry
logger.info(
    "Task completed",
    task_id="task-123",
    agent_id="agent-456",
    duration=45.2,
    quality_score=0.92,
    user_id="user-789"
)
```

#### Log Aggregation

```yaml
# fluent-bit config for Kubernetes
apiVersion: v1
kind: ConfigMap
metadata:
  name: fluent-bit-config
  namespace: santiago
data:
  fluent-bit.conf: |
    [INPUT]
        Name              tail
        Path              /var/log/containers/*santiago*.log
        Parser            docker
        Tag               santiago.*
        Refresh_Interval  5

    [OUTPUT]
        Name  elasticsearch
        Host  elasticsearch.santiago.svc.cluster.local
        Port  9200
        Index santiago-logs
```

### Alerting

#### Prometheus Alert Rules

```yaml
# prometheus/alerts.yaml
groups:
  - name: santiago
    rules:
      - alert: HighErrorRate
        expr: rate(santiago_requests_total{status=~"5.."}[5m]) / rate(santiago_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }}%"

      - alert: TaskQueueGrowing
        expr: increase(santiago_tasks_queue_length[10m]) > 50
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "Task queue is growing rapidly"
          description: "Queue length increased by {{ $value }} in 10 minutes"
```

---

## 🔄 Backup & Recovery

### Database Backup

#### PostgreSQL Backup

```bash
# Daily backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=/backups/postgres

# Create backup
pg_dump -h $POSTGRES_HOST -U $POSTGRES_USER $POSTGRES_DB > $BACKUP_DIR/santiago_$DATE.sql

# Compress
gzip $BACKUP_DIR/santiago_$DATE.sql

# Clean old backups (keep last 30 days)
find $BACKUP_DIR -name "*.sql.gz" -mtime +30 -delete
```

#### Neo4j Backup

```bash
# Neo4j backup
neo4j-admin database dump neo4j --to-path=/backups/neo4j/ --overwrite-destination=true
```

### Automated Backups

#### Kubernetes CronJob

```yaml
# k8s/backup-cronjob.yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: santiago-backup
  namespace: santiago
spec:
  schedule: "0 2 * * *"  # Daily at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: backup
            image: santiago/backup:latest
            envFrom:
            - secretRef:
                name: santiago-secrets
            volumeMounts:
            - name: backup-storage
              mountPath: /backups
          volumes:
          - name: backup-storage
            persistentVolumeClaim:
              claimName: backup-pvc
          restartPolicy: OnFailure
```

### Recovery Procedures

#### Database Recovery

```bash
# PostgreSQL recovery
gunzip santiago_20240115_020000.sql.gz
psql -h $POSTGRES_HOST -U $POSTGRES_USER $POSTGRES_DB < santiago_20240115_020000.sql

# Neo4j recovery
neo4j-admin database load neo4j --from-path=/backups/neo4j/ --overwrite-destination=true
```

#### Full System Recovery

1. **Stop all services:**
   ```bash
   kubectl scale deployment santiago-api --replicas=0 -n santiago
   ```

2. **Restore databases:**
   ```bash
   # Restore PostgreSQL
   # Restore Neo4j
   ```

3. **Clear caches:**
   ```bash
   # Clear Redis
   redis-cli FLUSHALL
   ```

4. **Restart services:**
   ```bash
   kubectl scale deployment santiago-api --replicas=3 -n santiago
   ```

5. **Verify recovery:**
   ```bash
   curl https://your-domain.com/health
   ```

---

## 🔒 Security

### Network Security

#### Firewall Configuration

```bash
# UFW rules for Santiago
ufw allow 22/tcp                    # SSH
ufw allow 80/tcp                    # HTTP
ufw allow 443/tcp                   # HTTPS
ufw allow 8000/tcp                  # API (internal only)
ufw --force enable
```

#### Kubernetes Network Policies

```yaml
# k8s/network-policy.yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: santiago-network-policy
  namespace: santiago
spec:
  podSelector:
    matchLabels:
      app: santiago-api
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          name: ingress-nginx
    ports:
    - protocol: TCP
      port: 8000
  egress:
  - to:
    - podSelector:
        matchLabels:
          app: postgres
    ports:
    - protocol: TCP
      port: 5432
  - to:
    - podSelector:
        matchLabels:
          app: neo4j
    ports:
    - protocol: TCP
      port: 7687
```

### Data Encryption

#### At Rest Encryption

```python
# config/encryption.py
from cryptography.fernet import Fernet
import os

class DataEncryption:
    def __init__(self):
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            raise ValueError("ENCRYPTION_KEY environment variable required")
        self.fernet = Fernet(key.encode())

    def encrypt(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data: str) -> str:
        return self.fernet.decrypt(encrypted_data.encode()).decode()

# Usage
encryptor = DataEncryption()
sensitive_data = encryptor.encrypt("secret information")
decrypted = encryptor.decrypt(sensitive_data)
```

#### In Transit Encryption

All Santiago communications use TLS 1.3 by default. Configure SSL/TLS:

```nginx
# nginx SSL configuration
ssl_protocols TLSv1.3;
ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512;
ssl_prefer_server_ciphers off;
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 10m;
```

### Access Control

#### API Key Management

```python
# Rotate API keys
from santiago.auth import APIKeyManager

key_manager = APIKeyManager()

# Create new key
new_key = key_manager.create_key(
    name="production-key",
    permissions=["read", "write"],
    expires_in_days=365
)

# Rotate existing key
key_manager.rotate_key(
    old_key_id="key-123",
    new_permissions=["read", "write", "admin"]
)

# Revoke key
key_manager.revoke_key("key-123")
```

#### Role-Based Access Control

```python
# config/rbac.py
from santiago.auth import RBACManager

rbac = RBACManager()

# Define roles
rbac.create_role("developer", permissions=[
    "tasks.submit",
    "tasks.read",
    "knowledge.read"
])

rbac.create_role("admin", permissions=[
    "tasks.*",
    "agents.*",
    "knowledge.*",
    "analytics.*"
])

# Assign role to user
rbac.assign_role(user_id="user-123", role="developer")

# Check permission
if rbac.has_permission(user_id="user-123", permission="tasks.submit"):
    # Allow action
    pass
```

---

## 🚀 Scaling & Performance

### Performance Optimization

#### Database Optimization

```sql
-- PostgreSQL optimizations
-- Create indexes
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_agent_id ON tasks(agent_id);
CREATE INDEX idx_knowledge_subject ON knowledge_facts(subject);

-- Analyze tables
ANALYZE tasks;
ANALYZE knowledge_facts;

-- Vacuum regularly
VACUUM ANALYZE;
```

#### Caching Strategy

```python
# config/caching.py
from santiago.cache import CacheManager

cache = CacheManager(
    redis_url=os.getenv('REDIS_URL'),
    default_ttl=3600  # 1 hour
)

# Cache knowledge queries
@cache.cached(key_prefix="knowledge", ttl=1800)
def query_knowledge(sparql_query):
    return execute_sparql_query(sparql_query)

# Cache agent performance
@cache.cached(key_prefix="agent_performance", ttl=300)
def get_agent_performance(agent_id):
    return calculate_performance_metrics(agent_id)
```

#### Connection Pooling

```python
# config/database.py
from santiago.database import DatabasePool

db_pool = DatabasePool(
    host=os.getenv('POSTGRES_HOST'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD'),
    min_connections=5,
    max_connections=20,
    connection_timeout=30
)

# Usage
async with db_pool.get_connection() as conn:
    result = await conn.fetch("SELECT * FROM tasks WHERE status = $1", "completed")
```

### Horizontal Scaling

#### Load Balancing

```nginx
# nginx load balancer config
upstream santiago_api {
    least_conn;
    server api-1:8000 weight=1;
    server api-2:8000 weight=1;
    server api-3:8000 weight=1;

    keepalive 32;
}

server {
    listen 80;
    location / {
        proxy_pass http://santiago_api;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Database Sharding

```python
# config/sharding.py
from santiago.database import ShardManager

shard_manager = ShardManager(
    shards=[
        {"id": "shard1", "host": "db1", "databases": ["tasks", "agents"]},
        {"id": "shard2", "host": "db2", "databases": ["knowledge", "analytics"]}
    ]
)

# Route queries to appropriate shard
def get_shard_for_table(table_name):
    if table_name in ["tasks", "agents"]:
        return shard_manager.get_shard("shard1")
    else:
        return shard_manager.get_shard("shard2")
```

### Performance Monitoring

#### Key Metrics to Monitor

```python
# config/monitoring.py
from santiago.monitoring import PerformanceMonitor

monitor = PerformanceMonitor()

# Track response times
@monitor.timed("api_request")
async def handle_request(request):
    # Handle request
    return response

# Track throughput
@monitor.counter("requests_per_second")
async def process_request(request):
    # Process request
    pass

# Track errors
@monitor.counter("error_rate")
def handle_error(error):
    # Handle error
    pass

# Custom metrics
monitor.gauge("active_connections", lambda: get_connection_count())
monitor.histogram("task_duration", lambda: get_recent_task_durations())
```

---

## 🔄 Maintenance Procedures

### Regular Maintenance Tasks

#### Daily Tasks

```bash
# Daily maintenance script
#!/bin/bash

# Backup databases
make backup

# Update SSL certificates
certbot renew

# Rotate logs
logrotate /etc/logrotate.d/santiago

# Clean old Docker images
docker image prune -f

# Update monitoring dashboards
make update-dashboards
```

#### Weekly Tasks

```bash
# Weekly maintenance
#!/bin/bash

# Analyze database performance
make db-analyze

# Update dependencies
make update-deps

# Security scan
make security-scan

# Performance test
make load-test
```

#### Monthly Tasks

```bash
# Monthly maintenance
#!/bin/bash

# Full backup verification
make verify-backups

# Capacity planning review
make capacity-review

# Compliance audit
make compliance-check

# Cost optimization
make cost-optimization
```

### Update Procedures

#### Rolling Updates

```bash
# Zero-downtime deployment
kubectl set image deployment/santiago-api api=santiago/api:v2.1.0
kubectl rollout status deployment/santiago-api

# Verify deployment
curl https://your-domain.com/health
```

#### Database Migrations

```python
# migrations/001_add_new_table.py
from santiago.migrations import Migration

class AddNewTable(Migration):
    version = "001"
    description = "Add new table for enhanced analytics"

    async def up(self):
        await self.execute("""
            CREATE TABLE analytics_events (
                id SERIAL PRIMARY KEY,
                event_type VARCHAR(50) NOT NULL,
                event_data JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        await self.execute("""
            CREATE INDEX idx_analytics_events_type ON analytics_events(event_type)
        """)

    async def down(self):
        await self.execute("DROP TABLE analytics_events")
```

### Troubleshooting

#### Common Issues

1. **High Memory Usage**
   ```bash
   # Check memory usage
   kubectl top pods -n santiago

   # Restart problematic pods
   kubectl delete pod <pod-name> -n santiago
   ```

2. **Slow Database Queries**
   ```sql
   -- Find slow queries
   SELECT query, total_time, calls
   FROM pg_stat_statements
   ORDER BY total_time DESC
   LIMIT 10;

   -- Add missing indexes
   CREATE INDEX CONCURRENTLY idx_slow_column ON slow_table(slow_column);
   ```

3. **API Timeouts**
   ```bash
   # Check API logs
   kubectl logs -f deployment/santiago-api -n santiago

   # Increase timeout settings
   helm upgrade santiago santiago/santiago \
     --set api.timeout=60 \
     --set api.maxRetries=5
   ```

---

## 📞 Support & Resources

### Getting Help

- **Documentation**: [docs.santiago.ai](https://docs.santiago.ai)
- **Community Forum**: [community.santiago.ai](https://community.santiago.ai)
- **GitHub Issues**: [github.com/santiago/issues](https://github.com/santiago/issues)
- **Enterprise Support**: [enterprise.santiago.ai](https://enterprise.santiago.ai)

### Additional Resources

- **Helm Charts**: [github.com/santiago/helm-charts](https://github.com/santiago/helm-charts)
- **Docker Images**: [hub.docker.com/r/santiago](https://hub.docker.com/r/santiago)
- **Terraform Modules**: [github.com/santiago/terraform](https://github.com/santiago/terraform)
- **Ansible Playbooks**: [github.com/santiago/ansible](https://github.com/santiago/ansible)

---

*This deployment guide covers the most common deployment scenarios. For specific cloud provider integrations or advanced configurations, check the [deployment examples repository](https://github.com/santiago/deployment-examples).* 