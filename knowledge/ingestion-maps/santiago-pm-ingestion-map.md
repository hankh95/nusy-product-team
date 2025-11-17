# Santiago-PM Ingestion Map

**Created**: 2025-11-16  
**Purpose**: Complete mapping of santiago-pm/ folder structure for Catchfish extraction  
**Target**: santiago-pm-self-aware Santiago (understands its own PM domain)

---

## 🎯 Executive Summary

The `santiago-pm/` folder (59 .md files, 14 subfolders) is a **goldmine** for Santiago ingestion because it contains:

1. **Domain Specifications** (what/why) - PM artifacts and their semantics
2. **Behavioral Specifications** (how) - Agent roles and tool implementations  
3. **Scaffold Templates** (EARS-inspired) - Folder structures that teach Santiago how to build itself

**Key Insight**: By ingesting santiago-pm/, Santiago learns to be its own Product Manager (bootstrap capability).

---

## 📊 Classification Matrix

### Domain Specifications → Data/Entities (KG Nodes)

| Folder | Nautical Name | Entity Type | Purpose | Template | Count |
|--------|---------------|-------------|---------|----------|-------|
| `cargo-manifests/` | Cargo Manifests | **Feature** | BDD feature specifications | cargo-manifest-template.md | 1 template |
| `ships-logs/` | Ship's Logs | **Issue** | Issue tracking, bug reports | ships-log-slug.md | 14+ issues |
| `voyage-trials/` | Voyage Trials | **Experiment** | Hypothesis testing, trials | voyage-trial-template.md | 1 template |
| `navigation-charts/` | Navigation Charts | **Plan** | Development plans, roadmaps | (implicit) | 1+ plans |
| `captains-journals/` | Captain's Journals | **Note** | Knowledge capture, insights | (implicit) | 1+ journals |
| `research-logs/` | Research Logs | **Research** | Analysis, findings | (implicit) | 4+ research docs |
| `quality-assessments/` | Quality Assessments | **Test** | Quality metrics, validation | 3 slug templates | 3 assessments |

**Extraction Pattern**: Each markdown file → Entity with:
- YAML frontmatter → structured properties (id, status, assignees, labels, epic)
- Markdown body → content/description
- Relationships → extracted from frontmatter fields (epic, related_artifacts, etc.)

---

### Behavioral Specifications → MCP Tools (Agent Capabilities)

| Folder | Tool Category | MCP Tools Extracted | Capability Level | Knowledge Scope |
|--------|---------------|---------------------|------------------|-----------------|
| `crew-manifests/` | **Agent Roles** | 7 roles → 15+ behaviors | Journeyman-Master | Lake-Sea |
| `tackle/status/` | **Status Management** | status_query, status_transition | Apprentice-Journeyman | Pond-Lake |
| `notes-domain-model.md` | **Semantic Linking** | link_related_notes (6 types) | Journeyman | Lake |
| `templates/` | **Scaffold Generation** | generate_from_template | Journeyman | Lake |
| `expeditions/` | **Experiment Execution** | design_experiment, run_trial | Master | Sea |

#### 7 Agent Roles (crew-manifests/)
1. **nusy-product-manager.role-spec.md** → PM behaviors (backlog, features, experiments)
2. **architect-nusy.agent.instructions.md** → KG schema design, coverage reports
3. **architect-systems.agent.instructions.md** → System architecture, deployment
4. **developer.agent.instructions.md** → Code implementation, TDD
5. **qa.agent.instructions.md** → Testing, validation, quality gates
6. **ux.agent.instructions.md** → User research, design
7. **platform.agent.instructions.md** → Infrastructure, DevOps

**Extraction Pattern**: Each role file → 2-5 MCP tools based on "Outputs" and "Practices" sections

---

## 🔗 Relationship Types (From notes-domain-model.md)

### Semantic Relationship Taxonomy

| Relationship | Inverse | Strength | Use Case | Example |
|--------------|---------|----------|----------|---------|
| **relatedTo** | relatedTo | 0.5-0.8 | Thematic connection | Feature A relates to Feature B (similar domain) |
| **follows** | precededBy | 0.7-0.9 | Temporal sequence | Plan B follows Plan A (chronological) |
| **references** | referencedBy | 0.6-0.9 | Citation/building upon | Note X references Research Y |
| **contradicts** | contradictedBy | 0.8-1.0 | Conflicting information | Hypothesis A contradicts Hypothesis B |
| **supports** | supportedBy | 0.7-0.9 | Supporting evidence | Experiment X supports Feature Y |
| **elaborates** | elaboratedBy | 0.6-0.8 | Detailed explanation | Journal Z elaborates Note W |

**Additional Relationships (Derived)**:
- **hasIssue**: Feature → Issue (from ships-logs links)
- **testsBehavior**: Experiment → Behavior (from voyage-trials)
- **hasCapability**: Role → Tool (from crew-manifests)
- **belongsToEpic**: Feature → Epic (from frontmatter)
- **hasStatus**: Artifact → Status (universal system)

---

## 🏗️ EARS-Inspired Scaffold System

### Folder Structure as Scaffold Template

Each santiago-pm subfolder = **Investigation Template**:

```
santiago-pm/
└── [domain-folder]/           # e.g., tackle/status/
    ├── README.md              # Context: What this domain is
    ├── [domain]-system.md     # Specification: How it works
    ├── development-plan.md    # Progression: Implementation steps
    ├── [domain]_models.py     # Implementation: Data models
    ├── [domain]_services.py   # Implementation: Business logic
    ├── [domain]_kg.py         # Implementation: KG integration
    └── test_[domain].py       # Validation: Test suite
```

**EARS Mapping**:
- **E** (Easy): README.md provides easy entry point
- **A** (Approach): development-plan.md shows the approach
- **R** (Requirements): [domain]-system.md lists requirements
- **S** (Syntax): Templates + code define the syntax

**Scaffold → Investigation → Suggestion Loop**:
1. Santiago reads `tackle/status/README.md` → understands status domain
2. Santiago scans `status-system.md` → extracts status transitions as behavior
3. Santiago sees `status_kg.py` → understands KG integration pattern
4. **Santiago suggests**: "I can create similar tackle for notes/experiments!"

This is **meta-learning**: Santiago learns how to build itself by studying its own structure.

---

## 📦 Extraction Targets (Task 11: Catchfish)

### Priority 1: Core PM Behaviors (15-20 behaviors)

**From crew-manifests/nusy-product-manager.role-spec.md**:
1. `create_feature` - Generate BDD feature from vision
2. `create_backlog_item` - Add story to backlog
3. `prioritize_backlog` - Rank items by value/risk
4. `define_acceptance_criteria` - Write testable criteria
5. `track_velocity` - Measure team throughput

**From tackle/status/status-system.md**:
6. `status_query` - Query artifacts by status
7. `status_transition` - Change artifact status (open → in_progress → closed)
8. `status_dashboard` - Visualize project status

**From notes-domain-model.md**:
9. `create_note` - Capture knowledge/insights
10. `link_related_notes` - Create semantic relationships (6 types)
11. `query_note_network` - Traverse relationship graph

**From expeditions/ + voyage-trials/**:
12. `design_experiment` - Create hypothesis-driven trial
13. `run_experiment` - Execute voyage trial
14. `record_experiment_results` - Capture outcomes
15. `analyze_experiment_metrics` - Validate success criteria

**From quality-assessments/**:
16. `run_quality_assessment` - Validate against quality gates
17. `generate_quality_report` - Summarize quality metrics

**From navigation-charts/**:
18. `create_navigation_chart` - Define development plan
19. `update_milestone` - Track plan progress

**From strategic-charts/**:
20. `define_vision` - Articulate strategic goals

### Priority 2: Entity Extraction (20-30 entities per category)

**Features (cargo-manifests/)**:
- Extract: title, hypothesis, signals, BDD scenarios, impact
- Count target: 5-10 features

**Issues (ships-logs/)**:
- Extract: description, acceptance criteria, assignees, status, tasks
- Count target: 14 existing issues

**Experiments (voyage-trials/)**:
- Extract: hypothesis, phases, metrics, success criteria, risks
- Count target: 5-7 experiments (from expeditions/)

**Notes (captains-journals/)**:
- Extract: title, summary, content, contributor, tags, relationships
- Count target: 3-5 journal entries

**Plans (navigation-charts/)**:
- Extract: milestones, tasks, dependencies, progress
- Count target: 2-3 plans

**Roles (crew-manifests/)**:
- Extract: mission, inputs, outputs, practices, capabilities
- Count target: 7 agent roles

---

## 🎣 Ontology Schema (Task 10: Design)

### RDF/OWL Class Hierarchy

```turtle
# Base Classes
kg:Artifact a rdfs:Class ;
    rdfs:comment "Base class for all PM artifacts" .

nusy:Feature a rdfs:Class ;
    rdfs:subClassOf kg:Artifact ;
    rdfs:comment "BDD feature specification (Cargo Manifest)" .

nusy:Issue a rdfs:Class ;
    rdfs:subClassOf kg:Artifact ;
    rdfs:comment "Issue/bug tracking (Ship's Log)" .

nusy:Experiment a rdfs:Class ;
    rdfs:subClassOf kg:Artifact ;
    rdfs:comment "Hypothesis testing trial (Voyage Trial)" .

nusy:Plan a rdfs:Class ;
    rdfs:subClassOf kg:Artifact ;
    rdfs:comment "Development plan/roadmap (Navigation Chart)" .

nusy:Note a rdfs:Class ;
    rdfs:subClassOf kg:Artifact ;
    rdfs:comment "Knowledge capture (Captain's Journal)" .

nusy:Role a rdfs:Class ;
    rdfs:comment "Agent role specification (Crew Manifest)" .

nusy:Status a rdfs:Class ;
    rdfs:comment "Universal status value (open/in_progress/blocked/closed)" .

# Properties
nusy:hasStatus a rdf:Property ;
    rdfs:domain kg:Artifact ;
    rdfs:range nusy:Status .

nusy:hasAssignee a rdf:Property ;
    rdfs:domain kg:Artifact ;
    rdfs:range xsd:string .

nusy:belongsToEpic a rdf:Property ;
    rdfs:domain nusy:Feature ;
    rdfs:range xsd:string .

nusy:hasIssue a rdf:Property ;
    rdfs:domain nusy:Feature ;
    rdfs:range nusy:Issue .

nusy:testsBehavior a rdf:Property ;
    rdfs:domain nusy:Experiment ;
    rdfs:range xsd:string .

# Semantic Relationships (Notes Domain)
nusy:relatedTo a rdf:Property ;
    rdfs:domain nusy:Note ;
    rdfs:range nusy:Note ;
    owl:inverseOf nusy:relatedTo .

nusy:follows a rdf:Property ;
    rdfs:domain nusy:Note ;
    rdfs:range nusy:Note ;
    owl:inverseOf nusy:precededBy .

nusy:references a rdf:Property ;
    rdfs:domain nusy:Note ;
    rdfs:range nusy:Note ;
    owl:inverseOf nusy:referencedBy .

nusy:contradicts a rdf:Property ;
    rdfs:domain nusy:Note ;
    rdfs:range nusy:Note ;
    owl:inverseOf nusy:contradictedBy .

nusy:supports a rdf:Property ;
    rdfs:domain nusy:Note ;
    rdfs:range nusy:Note ;
    owl:inverseOf nusy:supportedBy .

nusy:elaborates a rdf:Property ;
    rdfs:domain nusy:Note ;
    rdfs:range nusy:Note ;
    owl:inverseOf nusy:elaboratedBy .

# Role Capabilities
nusy:hasCapability a rdf:Property ;
    rdfs:domain nusy:Role ;
    rdfs:range xsd:string .
```

### Target KG Metrics (After Full Ingestion)

- **Entities**: 50-70 nodes (14 issues + 7 roles + 5 features + 5 experiments + 5 notes + 3 plans + 10 misc)
- **Triples**: 200-300 triples (50 entities × 4-6 properties each)
- **Relationships**: 30-50 semantic links (hasIssue, testsBehavior, relatedTo, supports, etc.)
- **Behaviors**: 20 PM behaviors extracted → 20 MCP tools

---

## 🛠️ MCP Manifest Structure (Task 14: Generate)

### Tool Categories

#### 1. Status Management (Apprentice-Journeyman, Pond-Lake)
```json
{
  "name": "status_query",
  "description": "Query artifacts by status, assignee, or update date",
  "input_schema": {
    "status": "string (open|in_progress|blocked|closed)",
    "assignee": "string",
    "artifact_type": "string (feature|issue|experiment|plan|note)"
  },
  "output_schema": {
    "artifacts": "array of artifact objects"
  },
  "mutates_kg": false,
  "concurrency_safe": true,
  "capability_level": "apprentice",
  "knowledge_scope": "pond"
}
```

#### 2. Feature Management (Journeyman, Lake)
```json
{
  "name": "create_backlog_item",
  "description": "Generate feature from vision statement",
  "input_schema": {
    "title": "string",
    "hypothesis": "string",
    "signals": "array of strings",
    "epic": "string"
  },
  "output_schema": {
    "feature_id": "string",
    "cargo_manifest_path": "string"
  },
  "mutates_kg": true,
  "concurrency_safe": false,
  "capability_level": "journeyman",
  "knowledge_scope": "lake"
}
```

#### 3. Issue Tracking (Apprentice-Journeyman, Pond-Lake)
```json
{
  "name": "log_issue",
  "description": "Create ship's log entry for bug/task",
  "input_schema": {
    "title": "string",
    "description": "string",
    "acceptance_criteria": "array of strings",
    "assignees": "array of strings"
  },
  "output_schema": {
    "issue_id": "string",
    "ships_log_path": "string"
  },
  "mutates_kg": true,
  "concurrency_safe": false,
  "capability_level": "journeyman",
  "knowledge_scope": "lake"
}
```

#### 4. Experiment Management (Master, Sea)
```json
{
  "name": "design_experiment",
  "description": "Create hypothesis-driven voyage trial",
  "input_schema": {
    "hypothesis": "string",
    "phases": "array of phase objects",
    "success_criteria": "array of strings",
    "risk_mitigation": "array of strings"
  },
  "output_schema": {
    "experiment_id": "string",
    "voyage_trial_path": "string"
  },
  "mutates_kg": true,
  "concurrency_safe": false,
  "capability_level": "master",
  "knowledge_scope": "sea"
}
```

#### 5. Knowledge Capture (Journeyman, Lake)
```json
{
  "name": "link_related_notes",
  "description": "Create semantic relationship between notes",
  "input_schema": {
    "source_note_id": "string",
    "target_note_id": "string",
    "relationship_type": "string (relatedTo|follows|references|contradicts|supports|elaborates)",
    "strength": "number (0.0-1.0)",
    "context": "string"
  },
  "output_schema": {
    "relationship_id": "string",
    "semantic_triple": "string"
  },
  "mutates_kg": true,
  "concurrency_safe": false,
  "capability_level": "journeyman",
  "knowledge_scope": "lake"
}
```

#### 6. Strategic Planning (Master-Expert, Sea-Ocean)
```json
{
  "name": "define_vision",
  "description": "Articulate strategic goals and direction",
  "input_schema": {
    "vision_statement": "string",
    "goals": "array of strings",
    "success_metrics": "array of strings",
    "time_horizon": "string"
  },
  "output_schema": {
    "vision_id": "string",
    "strategic_chart_path": "string"
  },
  "mutates_kg": true,
  "concurrency_safe": false,
  "capability_level": "expert",
  "knowledge_scope": "ocean"
}
```

### Manifest Metadata
```json
{
  "manifest_version": "1.0.0",
  "santiago_id": "santiago-pm-self-aware",
  "domain": "product-management",
  "capability_level": "master",
  "knowledge_scope": "sea",
  "total_tools": 20,
  "tool_categories": [
    "status_management",
    "feature_management",
    "issue_tracking",
    "experiment_management",
    "knowledge_capture",
    "strategic_planning"
  ],
  "concurrency_risks": [
    "create_backlog_item (mutates cargo-manifests/)",
    "log_issue (mutates ships-logs/)",
    "design_experiment (mutates voyage-trials/)",
    "link_related_notes (mutates KG relationship graph)"
  ],
  "quality_gates": {
    "bdd_pass_rate": 0.95,
    "test_coverage": 0.95,
    "kg_completeness": 0.90
  }
}
```

---

## 🚀 Ingestion Workflow (Navigator Orchestration)

### Step 1: Vision (Define Catch Goal)
- **Domain**: Product Management
- **Goal**: Santiago-PM-Self-Aware (understands its own domain)
- **Behaviors**: 20 PM behaviors (status, features, issues, experiments, notes, plans, vision)

### Step 2: Raw Materials (Collect Sources)
- **Directory**: `santiago-pm/`
- **File Count**: 59 .md files
- **Subfolders**: 14 (cargo-manifests, ships-logs, voyage-trials, etc.)
- **Key Files**:
  - `crew-manifests/*.md` (7 agent roles)
  - `tackle/status/status-system.md` (status transitions)
  - `notes-domain-model.md` (semantic relationships)
  - `strategic-charts/Old man and the sea.md` (10-step process)

### Step 3: Catchfish Extraction (30-60m target, <15m optimized)
- **Layer 1 (Raw Text)**: Parse all 59 .md files
- **Layer 2 (Entities)**: Extract 50-70 entities (features, issues, experiments, roles, etc.)
- **Layer 3 (Structured Docs)**: Generate YAML frontmatter + Markdown docs
- **Layer 4 (KG Triples)**: Produce 200-300 triples with provenance SHA-256 hashing

### Step 4: Indexing
- **Entity Index**: 50-70 entities with IDs
- **Behavior Index**: 20 PM behaviors
- **Relationship Index**: 30-50 semantic links

### Step 5: Ontology Loading
- **Load Schema**: PM domain ontology (Artifact, Feature, Issue, Experiment, etc.)
- **Validate**: All entities match ontology classes
- **Relationship Types**: 6 semantic + 5 structural relationships

### Step 6: KG Building
- **Populate Graph**: Insert 200-300 triples
- **Link Entities**: Connect features ↔ issues, experiments ↔ behaviors
- **Semantic Network**: Build notes relationship graph (relatedTo, supports, contradicts, etc.)

### Step 7: Fishnet BDD Generation
- **Features**: 20 behaviors → 20 .feature files
- **Scenarios**: 3 per behavior (happy path, edge case, error) = 60 scenarios
- **Gherkin**: Given/When/Then format with KG node references
- **Example**:
  ```gherkin
  Feature: Link Related Notes
    Scenario: Create semantic relationship between notes
      Given I have two notes "note-123" and "note-456" in the knowledge graph
      When I link them with relationship type "supports" and strength 0.9
      Then a new triple "(note-123 nusy:supports note-456)" should be created
      And the relationship should have metadata with strength 0.9
  ```

### Step 8: Navigator Validation Loop (3-5 cycles)
- **Cycle 1**: 87-90% BDD pass rate (baseline)
- **Cycle 2**: 90-93% (improve entity extraction)
- **Cycle 3**: 93-96% (refine relationships)
- **Cycle 4**: 96-98% (polish edge cases) ← Target: ≥95%
- **Quality Gate**: Pass if ≥95% BDD pass rate + ≥95% coverage

### Step 9: Deployment
- **Output Directory**: `knowledge/catches/santiago-pm-self-aware/`
- **Artifacts**:
  - `domain-knowledge/` (50-70 structured docs)
  - `bdd-tests/` (20 .feature files, 60 scenarios)
  - `mcp-manifest.json` (20 tools, 6 categories)
  - `ontology.ttl` (PM domain schema)
  - `knowledge-graph.ttl` (200-300 triples)
- **Provenance**: `ships-logs/catchfish/santiago-pm_*.json` (extraction metadata)

### Step 10: Learning
- **Lessons**:
  - "EARS scaffold pattern enables self-learning"
  - "Notes semantic relationships create knowledge network"
  - "Status system provides universal tracking"
  - "7 agent roles map to 15+ MCP tool behaviors"
- **Improvements**:
  - Catchfish can recognize scaffold patterns
  - Navigator can suggest new tackle implementations
  - Fishnet can generate EARS-style templates

---

## 🎯 Success Metrics (Task 16: Demo Validation)

### Extraction Quality
- ✅ **Entities Extracted**: 50-70 (target: ≥40)
- ✅ **Triples Generated**: 200-300 (target: ≥150)
- ✅ **Behaviors Identified**: 20 (target: ≥15)
- ✅ **Relationships Mapped**: 30-50 (target: ≥20)

### BDD Coverage
- ✅ **Features Generated**: 20 (1 per behavior)
- ✅ **Scenarios Created**: 60 (3 per feature)
- ✅ **BDD Pass Rate**: ≥95% (after 3-5 cycles)
- ✅ **Test Coverage**: 100% (all behaviors have tests)

### MCP Manifest
- ✅ **Tools Defined**: 20 (6 categories)
- ✅ **Capability Levels**: Apprentice (2) + Journeyman (10) + Master (6) + Expert (2)
- ✅ **Knowledge Scopes**: Pond (2) + Lake (12) + Sea (5) + Ocean (1)
- ✅ **Concurrency Annotations**: 8 tools flagged as mutates_kg

### Bootstrap Capability
- ✅ **Self-Awareness**: Santiago understands its own PM domain
- ✅ **Scaffold Recognition**: Can identify EARS patterns in folder structure
- ✅ **Meta-Learning**: Suggests new tackle implementations based on existing patterns
- ✅ **Generalization**: Proves factory can build Santiagos for ANY domain

---

## 📝 Implementation Notes

### Catchfish Optimizations
- **Parallel Processing**: Process 59 files concurrently (reduce from 60m to <15m)
- **Template Recognition**: Detect templates vs instances (skip templates in entity extraction)
- **YAML Parsing**: Use frontmatter library for structured data extraction
- **Relationship Inference**: Parse `related_artifacts` fields to auto-link entities

### Navigator Improvements
- **Cycle Heuristics**: If pass rate improves <2% between cycles, stop (avoid diminishing returns)
- **Entity Validation**: Check all entities have required properties (id, type, status)
- **Relationship Validation**: Verify all relationships have valid source/target entities
- **Coverage Gaps**: Identify behaviors without BDD tests, auto-generate placeholders

### Fishnet Enhancements
- **Tool Type Inference**: 
  - Contains "query" → input tool (reads KG)
  - Contains "create/update/delete/link" → output tool (writes KG)
  - Contains "status/dashboard" → communication tool (reports)
- **Concurrency Detection**:
  - "create/update/delete" → mutates_kg = true
  - "query/get/list" → mutates_kg = false
  - Multiple writers to same folder → concurrency_safe = false
- **Capability Mapping**:
  - CRUD operations → Journeyman
  - Complex queries/analysis → Master
  - Strategic/vision work → Expert

---

## 🔄 Next Steps (Tasks 10-16)

1. **Task 10**: Design PM domain ontology (use this map's RDF schema)
2. **Task 11**: Run Catchfish on santiago-pm/ (extract 50-70 entities)
3. **Task 12**: Full Navigator expedition (10-step process, 3-5 cycles)
4. **Task 13**: Classify behaviors as data vs tools (use tool categories above)
5. **Task 14**: Generate MCP manifest (20 tools, 6 categories)
6. **Task 15**: Implement EARS scaffold system (folder structure recognition)
7. **Task 16**: Create santiago-pm-self-aware demo (end-to-end validation)

**After Tasks 10-16**: Santiago understands its own PM domain and can be its own Product Manager! 🎣

---

## 🌊 The Bootstrap Loop

```
santiago-pm/ (domain docs)
    ↓ (Catchfish)
PM Knowledge (entities, behaviors, relationships)
    ↓ (Fishnet)
BDD Tests + MCP Manifest (20 tools, 60 scenarios)
    ↓ (Navigator validation)
santiago-pm-self-aware (deployed Santiago)
    ↓ (Uses tools)
Manages its own development (reads cargo-manifests, creates ships-logs, runs voyage-trials)
    ↓ (Meta-learning)
Suggests improvements to santiago-pm/ structure (new tackle, better templates)
    ↓ (Feedback loop)
santiago-pm/ evolves (Santiago improves itself!)
```

**This is the core insight**: Santiago doesn't just learn PM practices—it learns **how to learn** by studying its own structure. The EARS scaffold pattern (folder structure + templates + development plans) teaches Santiago the **pattern of patterns**: how domain knowledge should be organized, how tackle should be structured, how validation should work.

**Result**: Santiago can ingest ANY well-structured domain folder and generate a specialized Santiago for that domain. The PM domain is just the first catch—the pattern works for clinical guidelines, legal reasoning, financial analysis, scientific research, etc.

---

**Status**: Task 9 COMPLETE ✅  
**Next**: Task 10 - Design PM domain ontology from this map
