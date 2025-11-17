---
task: 13
title: Santiago-PM MCP Tool Classification
source: knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md
ontology: knowledge/ontologies/pm-domain-ontology.ttl
classification_date: 2025-01-16
total_behaviors: 20
mcp_tools: 20
data_entities: 7
---

# Santiago-PM MCP Tool Classification

> **Purpose**: Classify extracted PM behaviors as MCP tools (agent capabilities) with metadata  
> **Source**: 20 PM behaviors from Task 11 extraction  
> **Output**: Tool specifications ready for MCP manifest generation (Task 14)

## Classification Summary

| Category | Tools | Mutates KG | Concurrency Risk | Capability Range | Scope Range |
|----------|-------|------------|------------------|------------------|-------------|
| Status Management | 3 | 1/3 | Low | Apprentice-Journeyman | Pond-Sea |
| Feature Management | 5 | 4/5 | High | Journeyman-Master | Lake-Sea |
| Issue Tracking | 2 | 2/2 | Medium | Apprentice-Journeyman | Pond-Lake |
| Experiment Management | 3 | 3/3 | Medium | Master | Sea |
| Knowledge Capture | 3 | 2/3 | Medium | Journeyman | Lake |
| Strategic Planning | 2 | 2/2 | High | Master-Expert | Sea-Ocean |
| Quality Assurance | 2 | 1/2 | Low | Journeyman | Lake-Sea |
| **TOTAL** | **20** | **15/20** | **Mixed** | **Apprentice-Expert** | **Pond-Ocean** |

---

## MCP Tool Definitions

### Category 1: Status Management Tools

#### Tool 1.1: status_query

**Type**: MCP Tool (Read-Only Query)  
**Classification**: Data Access (no mutation)

**Metadata**:
```json
{
  "name": "status_query",
  "category": "status_management",
  "capability_level": "apprentice",
  "knowledge_scope": "pond",
  "mutates_kg": false,
  "concurrency_safe": true,
  "autonomy": "supervised",
  "budget_hint": "$0.001-0.01 per query"
}
```

**Use Case**: Query artifacts by status, assignee, type  
**Concurrency**: Safe (read-only, no side effects)  
**Error Handling**: Returns empty array if no matches  
**Rate Limiting**: 100 queries/minute

---

#### Tool 1.2: status_transition

**Type**: MCP Tool (State Machine Mutation)  
**Classification**: KG Write Operation

**Metadata**:
```json
{
  "name": "status_transition",
  "category": "status_management",
  "capability_level": "journeyman",
  "knowledge_scope": "lake",
  "mutates_kg": true,
  "concurrency_safe": false,
  "autonomy": "moderate",
  "budget_hint": "$0.01-0.05 per transition",
  "requires_validation": true
}
```

**Use Case**: Change artifact status with provenance  
**Concurrency Risk**: HIGH - State machine must be atomic  
**Validation Rules**: Enforce valid state transitions  
**Provenance**: Creates StatusTransition entity in KG  
**Rate Limiting**: 10 transitions/minute (human-paced)

---

#### Tool 1.3: status_dashboard

**Type**: MCP Tool (Aggregation Query)  
**Classification**: Data Visualization

**Metadata**:
```json
{
  "name": "status_dashboard",
  "category": "status_management",
  "capability_level": "apprentice",
  "knowledge_scope": "sea",
  "mutates_kg": false,
  "concurrency_safe": true,
  "autonomy": "supervised",
  "budget_hint": "$0.05-0.20 per dashboard",
  "caching_recommended": true
}
```

**Use Case**: Visualize project status metrics  
**Concurrency**: Safe (read-only aggregation)  
**Caching**: 5-minute TTL for dashboard data  
**Rate Limiting**: 20 dashboards/minute

---

### Category 2: Feature Management Tools

#### Tool 2.1: create_feature

**Type**: MCP Tool (Artifact Creation)  
**Classification**: KG Write + File Creation

**Metadata**:
```json
{
  "name": "create_feature",
  "category": "feature_management",
  "capability_level": "journeyman",
  "knowledge_scope": "lake",
  "mutates_kg": true,
  "concurrency_safe": false,
  "autonomy": "moderate",
  "budget_hint": "$0.10-0.50 per feature",
  "requires_validation": true,
  "file_operations": ["write santiago-pm/cargo-manifests/"]
}
```

**Use Case**: Generate BDD feature from vision  
**Concurrency Risk**: HIGH - Race condition on cargo-manifests/ directory  
**File Operations**: Creates cargo-manifest-[slug].md  
**Validation**: Hypothesis + acceptance criteria required  
**Provenance**: Creates nusy:Feature entity with dcterms:creator  
**Rate Limiting**: 5 features/minute

---

#### Tool 2.2: prioritize_backlog

**Type**: MCP Tool (Strategic Decision)  
**Classification**: KG Update + Ranking Algorithm

**Metadata**:
```json
{
  "name": "prioritize_backlog",
  "category": "feature_management",
  "capability_level": "master",
  "knowledge_scope": "sea",
  "mutates_kg": true,
  "concurrency_safe": false,
  "autonomy": "high",
  "budget_hint": "$0.20-1.00 per prioritization",
  "requires_human_review": true
}
```

**Use Case**: Rank features by value/risk/dependencies  
**Concurrency Risk**: HIGH - Race condition on shared backlog  
**Decision Criteria**: User value, technical risk, strategic alignment, effort  
**Human Review**: Recommended for Master capability level  
**Rate Limiting**: 3 prioritizations/hour (strategic pacing)

---

#### Tool 2.3: define_acceptance_criteria

**Type**: MCP Tool (Specification Writing)  
**Classification**: KG Update + BDD Generation

**Metadata**:
```json
{
  "name": "define_acceptance_criteria",
  "category": "feature_management",
  "capability_level": "journeyman",
  "knowledge_scope": "lake",
  "mutates_kg": true,
  "concurrency_safe": false,
  "autonomy": "moderate",
  "budget_hint": "$0.10-0.30 per criteria set",
  "file_operations": ["update cargo-manifests/", "create features/"]
}
```

**Use Case**: Write testable BDD acceptance criteria  
**Concurrency Risk**: MEDIUM - Updates feature document  
**File Operations**: Updates cargo-manifest + creates .feature file  
**Validation**: All scenarios must be Given-When-Then format  
**Rate Limiting**: 10 criteria sets/minute

---

#### Tool 2.4: track_velocity

**Type**: MCP Tool (Metrics Calculation)  
**Classification**: Data Analysis

**Metadata**:
```json
{
  "name": "track_velocity",
  "category": "feature_management",
  "capability_level": "journeyman",
  "knowledge_scope": "sea",
  "mutates_kg": true,
  "concurrency_safe": true,
  "autonomy": "moderate",
  "budget_hint": "$0.05-0.15 per calculation",
  "caching_recommended": true
}
```

**Use Case**: Measure team throughput with trends  
**Concurrency**: Safe (append-only velocity measurements)  
**Metrics**: Completed features, story points, cycle time, burndown  
**Caching**: 1-hour TTL for velocity data  
**Rate Limiting**: 30 calculations/hour

---

#### Tool 2.5: update_backlog

**Type**: MCP Tool (Artifact Update)  
**Classification**: KG Update

**Metadata**:
```json
{
  "name": "update_backlog",
  "category": "feature_management",
  "capability_level": "journeyman",
  "knowledge_scope": "lake",
  "mutates_kg": true,
  "concurrency_safe": false,
  "autonomy": "moderate",
  "budget_hint": "$0.05-0.15 per update",
  "requires_reason": true
}
```

**Use Case**: Modify feature metadata post-creation  
**Concurrency Risk**: MEDIUM - Concurrent updates may conflict  
**Change Tracking**: Requires reason field for audit  
**Provenance**: Records previous values + change agent  
**Rate Limiting**: 20 updates/minute

---

### Category 3: Issue Tracking Tools

#### Tool 3.1: log_issue

**Type**: MCP Tool (Issue Creation)  
**Classification**: KG Write + File Creation

**Metadata**:
```json
{
  "name": "log_issue",
  "category": "issue_tracking",
  "capability_level": "apprentice",
  "knowledge_scope": "pond",
  "mutates_kg": true,
  "concurrency_safe": false,
  "autonomy": "supervised",
  "budget_hint": "$0.05-0.15 per issue",
  "file_operations": ["write santiago-pm/ships-logs/"]
}
```

**Use Case**: Create ship's log for bug/blocker  
**Concurrency Risk**: MEDIUM - Race on ships-logs/ directory  
**File Operations**: Creates YYYY-MM-DD-[slug].md  
**Severity Levels**: Critical, High, Medium, Low  
**Rate Limiting**: 10 issues/minute

---

#### Tool 3.2: link_issue_to_feature

**Type**: MCP Tool (Relationship Creation)  
**Classification**: KG Relationship

**Metadata**:
```json
{
  "name": "link_issue_to_feature",
  "category": "issue_tracking",
  "capability_level": "journeyman",
  "knowledge_scope": "lake",
  "mutates_kg": true,
  "concurrency_safe": true,
  "autonomy": "moderate",
  "budget_hint": "$0.01-0.05 per link"
}
```

**Use Case**: Bidirectional issue ↔ feature relationship  
**Concurrency**: Safe (relationship creation is commutative)  
**Relationship Types**: blocks, caused-by, discovered-in  
**Rate Limiting**: 50 links/minute

---

### Category 4: Experiment Management Tools

#### Tool 4.1: design_experiment

**Type**: MCP Tool (Experiment Creation)  
**Classification**: KG Write + File Creation

**Metadata**:
```json
{
  "name": "design_experiment",
  "category": "experiment_management",
  "capability_level": "master",
  "knowledge_scope": "sea",
  "mutates_kg": true,
  "concurrency_safe": false,
  "autonomy": "high",
  "budget_hint": "$0.50-2.00 per experiment",
  "requires_human_review": true,
  "file_operations": ["write santiago-pm/voyage-trials/"]
}
```

**Use Case**: Hypothesis-driven voyage trial creation  
**Concurrency Risk**: MEDIUM - Writes to voyage-trials/ directory  
**Components**: Hypothesis, phases, success criteria, risk mitigation  
**Human Review**: Recommended for strategic experiments  
**Rate Limiting**: 2 experiments/hour (strategic pacing)

---

#### Tool 4.2: record_experiment_results

**Type**: MCP Tool (Data Recording)  
**Classification**: KG Update

**Metadata**:
```json
{
  "name": "record_experiment_results",
  "category": "experiment_management",
  "capability_level": "journeyman",
  "knowledge_scope": "sea",
  "mutates_kg": true,
  "concurrency_safe": false,
  "autonomy": "moderate",
  "budget_hint": "$0.10-0.30 per recording"
}
```

**Use Case**: Document experiment outcomes/metrics  
**Concurrency Risk**: MEDIUM - Updates experiment document  
**Metrics**: Quantitative + qualitative observations  
**Phase Progression**: design → execution → analysis → complete  
**Rate Limiting**: 10 recordings/hour

---

#### Tool 4.3: analyze_experiment_outcomes

**Type**: MCP Tool (Statistical Analysis)  
**Classification**: Data Analysis

**Metadata**:
```json
{
  "name": "analyze_experiment_outcomes",
  "category": "experiment_management",
  "capability_level": "master",
  "knowledge_scope": "sea",
  "mutates_kg": true,
  "concurrency_safe": true,
  "autonomy": "high",
  "budget_hint": "$0.50-2.00 per analysis"
}
```

**Use Case**: Hypothesis validation + recommendations  
**Concurrency**: Safe (read-heavy, append-only analysis)  
**Analysis Types**: Comparative, longitudinal, cohort  
**Output**: Key findings, hypothesis validation, action items  
**Rate Limiting**: 5 analyses/hour

---

### Category 5: Knowledge Capture Tools

#### Tool 5.1: create_note

**Type**: MCP Tool (Note Creation)  
**Classification**: KG Write + File Creation

**Metadata**:
```json
{
  "name": "create_note",
  "category": "knowledge_capture",
  "capability_level": "journeyman",
  "knowledge_scope": "lake",
  "mutates_kg": true,
  "concurrency_safe": false,
  "autonomy": "moderate",
  "budget_hint": "$0.05-0.20 per note",
  "file_operations": ["write santiago-pm/captains-journals/"]
}
```

**Use Case**: Capture insight/learning/decision  
**Concurrency Risk**: LOW - Different notes unlikely to conflict  
**File Operations**: Creates note document in captains-journals/  
**Note Types**: insight, decision, learning, question  
**Rate Limiting**: 20 notes/minute

---

#### Tool 5.2: link_related_notes

**Type**: MCP Tool (Semantic Linking)  
**Classification**: KG Relationship

**Metadata**:
```json
{
  "name": "link_related_notes",
  "category": "knowledge_capture",
  "capability_level": "journeyman",
  "knowledge_scope": "lake",
  "mutates_kg": true,
  "concurrency_safe": true,
  "autonomy": "moderate",
  "budget_hint": "$0.02-0.08 per link"
}
```

**Use Case**: Create semantic note relationships  
**Concurrency**: Safe (relationship creation is commutative)  
**Relationship Types**: relatedTo, follows, references, elaborates, contradicts, supports  
**Strength**: 0.0-1.0 optional weight for graph queries  
**Rate Limiting**: 50 links/minute

---

#### Tool 5.3: query_note_network

**Type**: MCP Tool (Graph Traversal)  
**Classification**: Data Query

**Metadata**:
```json
{
  "name": "query_note_network",
  "category": "knowledge_capture",
  "capability_level": "journeyman",
  "knowledge_scope": "lake",
  "mutates_kg": false,
  "concurrency_safe": true,
  "autonomy": "moderate",
  "budget_hint": "$0.05-0.20 per query",
  "caching_recommended": true
}
```

**Use Case**: Traverse note relationship graph  
**Concurrency**: Safe (read-only)  
**Traversal**: Transitive queries (follows+), depth limits (1-5)  
**Filtering**: Minimum strength, relationship types  
**Caching**: 5-minute TTL for network queries  
**Rate Limiting**: 30 queries/minute

---

### Category 6: Strategic Planning Tools

#### Tool 6.1: define_vision

**Type**: MCP Tool (Vision Creation)  
**Classification**: KG Write + File Creation

**Metadata**:
```json
{
  "name": "define_vision",
  "category": "strategic_planning",
  "capability_level": "expert",
  "knowledge_scope": "ocean",
  "mutates_kg": true,
  "concurrency_safe": false,
  "autonomy": "full",
  "budget_hint": "$2.00-10.00 per vision",
  "requires_human_review": true,
  "file_operations": ["write santiago-pm/strategic-charts/"]
}
```

**Use Case**: High-level strategic vision definition  
**Concurrency Risk**: HIGH - Single vision document per product  
**Components**: Mission, principles, goals, stakeholders  
**Human Review**: REQUIRED for Expert capability level  
**Rate Limiting**: 1 vision/day (strategic pacing)

---

#### Tool 6.2: create_roadmap

**Type**: MCP Tool (Roadmap Creation)  
**Classification**: KG Write + File Creation

**Metadata**:
```json
{
  "name": "create_roadmap",
  "category": "strategic_planning",
  "capability_level": "master",
  "knowledge_scope": "sea",
  "mutates_kg": true,
  "concurrency_safe": false,
  "autonomy": "high",
  "budget_hint": "$1.00-5.00 per roadmap",
  "requires_human_review": true,
  "file_operations": ["write santiago-pm/navigation-charts/"]
}
```

**Use Case**: Navigation chart with milestones/epics  
**Concurrency Risk**: HIGH - Single roadmap per product  
**Components**: Timeline, milestones, epics, dependencies, themes  
**Roadmap Types**: Quarterly, annual, multi-year  
**Human Review**: Recommended for strategic alignment  
**Rate Limiting**: 1 roadmap/week (strategic pacing)

---

### Category 7: Quality Assurance Tools

#### Tool 7.1: run_quality_gate

**Type**: MCP Tool (Validation)  
**Classification**: Data Analysis + Decision

**Metadata**:
```json
{
  "name": "run_quality_gate",
  "category": "quality_assurance",
  "capability_level": "journeyman",
  "knowledge_scope": "lake",
  "mutates_kg": true,
  "concurrency_safe": true,
  "autonomy": "moderate",
  "budget_hint": "$0.20-0.80 per gate",
  "blocking_decision": true
}
```

**Use Case**: Execute quality checks with pass/fail  
**Concurrency**: Safe (read-heavy, append-only results)  
**Checks**: Functional quality, test coverage, code complexity, security, BDD pass rate  
**Threshold**: Default 0.95 (95% pass rate)  
**Blocking**: Can prevent deployment if fail  
**Rate Limiting**: 10 gates/hour

---

#### Tool 7.2: generate_quality_report

**Type**: MCP Tool (Reporting)  
**Classification**: Data Aggregation

**Metadata**:
```json
{
  "name": "generate_quality_report",
  "category": "quality_assurance",
  "capability_level": "journeyman",
  "knowledge_scope": "sea",
  "mutates_kg": true,
  "concurrency_safe": true,
  "autonomy": "moderate",
  "budget_hint": "$0.50-2.00 per report",
  "caching_recommended": true
}
```

**Use Case**: Aggregate quality metrics with trends  
**Concurrency**: Safe (read-heavy)  
**Scopes**: Feature, epic, product, system  
**Sections**: Summary, breakdown, issue analysis, trends, recommendations  
**Caching**: 1-hour TTL for report data  
**Rate Limiting**: 5 reports/hour

---

## Concurrency Risk Analysis

### HIGH Risk (Require Locking/Serialization)
- `status_transition`: State machine atomicity
- `create_feature`: File write race condition
- `prioritize_backlog`: Shared backlog updates
- `define_vision`: Single document per product
- `create_roadmap`: Single document per product

### MEDIUM Risk (Require Conflict Detection)
- `define_acceptance_criteria`: Feature document updates
- `update_backlog`: Concurrent metadata changes
- `log_issue`: File write to same directory
- `design_experiment`: Voyage trial creation
- `record_experiment_results`: Experiment updates

### LOW/SAFE (Concurrent Execution OK)
- All read-only queries (status_query, dashboard, query_note_network)
- Relationship creation (link_issue_to_feature, link_related_notes) - commutative
- Append-only metrics (track_velocity, analyze_experiment_outcomes)
- Quality assessments (run_quality_gate, generate_quality_report)

---

## Budget Recommendations

### Cost Tiers
- **Micro** ($0.001-0.01): Read queries, simple lookups
- **Small** ($0.01-0.10): CRUD operations, basic writes
- **Medium** ($0.10-0.50): Structured artifact creation, analysis
- **Large** ($0.50-2.00): Complex analysis, experiment design
- **Strategic** ($2.00-10.00): Vision/roadmap planning

### Daily Budget Allocation (Example)
- Status queries: 100 calls × $0.005 = $0.50
- Feature management: 10 operations × $0.30 = $3.00
- Issue tracking: 20 operations × $0.10 = $2.00
- Experiments: 2 operations × $1.00 = $2.00
- Knowledge capture: 30 operations × $0.10 = $3.00
- Strategic planning: 1 operation × $5.00 = $5.00
- Quality assurance: 5 operations × $0.50 = $2.50
- **TOTAL**: ~$18/day for moderate usage

---

## Capability Level Distribution

| Level | Tools | Autonomy | Human Review |
|-------|-------|----------|--------------|
| Apprentice | 3 | Supervised | Optional |
| Journeyman | 11 | Moderate | Situational |
| Master | 5 | High | Recommended |
| Expert | 1 | Full | Required |

**Progression Path**: Apprentice (read) → Journeyman (CRUD) → Master (strategic) → Expert (vision)

---

## Knowledge Scope Distribution

| Scope | Tools | Coverage |
|-------|-------|----------|
| Pond (Component) | 2 | Single artifact/feature |
| Lake (Module/Epic) | 11 | Project-level operations |
| Sea (Product) | 6 | Cross-epic strategic work |
| Ocean (Platform) | 1 | Cross-product/system vision |

**Scalability**: Most tools operate at Lake/Sea level (85%)

---

## Next Steps (Task 14)

Generate full MCP manifest with:
1. Tool definitions (input/output schemas from Task 11)
2. Capability metadata (from this classification)
3. Concurrency annotations (from risk analysis)
4. Budget hints (from cost tiers)
5. Category groupings (7 categories defined)
6. Dependency graph (which tools call which)
7. Autonomy policies (when to require human review)

**Output**: `knowledge/catches/santiago-pm-behaviors/santiago-pm-mcp-manifest.json`
