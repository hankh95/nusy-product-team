# Future Expedition: Santiago-Core Self-Management

**Status**: Planned (Not Started)  
**Prerequisites**: Complete neurosymbolic-bdd-executor expedition  
**Estimated Effort**: 4-6 hours  
**Priority**: High (validates santiago-pm tools, enables self-improvement)

## Mission

Use **santiago-pm tools** to scaffold and manage **santiago-core** as a product, demonstrating:
1. Self-dogfooding (santiago-core uses santiago-pm)
2. Domain expertise on itself (santiago-core knows santiago-core)
3. Meta-validation (the tool validates the tool)

## Why This Matters

**The Bootstrap Problem**: How do you know santiago-pm tools work? Use them to manage santiago-core!

**Validation Loop**:
```
Santiago-PM tools manage Santiago-Core
    ↓
Santiago-Core becomes domain expert on itself
    ↓
Santiago-Core answers questions about its own capabilities
    ↓
Santiago-PM tools query Santiago-Core for PM guidance
    ↓
Self-improving system!
```

## Current State vs Target State

### Current: Scattered Santiago-Core Assets

```
src/nusy_pm_core/
├── santiago_core_bdd_executor.py    # In progress
├── adapters/kg_store.py             # Exists
├── models/                          # Various
└── knowledge/                       # Shared with all domains

EXPEDITION-neurosymbolic-domain-expert.md   # Root level
notebooks/                                   # Root level
scripts/demo_santiago_*.py                   # Root level
```

**Problems**:
- No structure
- No roadmap
- No backlog
- No experiments tracking
- Can't answer "What are santiago-core's capabilities?"

### Target: Santiago-Core as Managed Product

```
santiago-core/
├── README.md                        # Vision, architecture
├── cargo-manifests/                 # Features as BDD tests
│   ├── neurosymbolic-reasoning.feature
│   ├── bdd-test-execution.feature
│   ├── human-qa-interface.feature
│   └── mcp-tool-integration.feature
├── strategic-charts/                # Roadmap, vision
│   ├── roadmap-2025.md
│   └── architecture-vision.md
├── expeditions/                     # Research, experiments
│   ├── neurosymbolic-bdd-executor/
│   └── multi-hop-reasoning/
├── ships-logs/                      # Development logs
│   └── 2025-11-17-expedition-neurosymbolic.md
├── passages/                        # Milestones
│   ├── phase-1-bdd-executor.md
│   ├── phase-2-multi-hop.md
│   └── phase-3-human-qa.md
├── quality-assessments/             # Test results, coverage
│   └── neurosymbolic-test-coverage.md
├── knowledge/                       # Santiago-core domain
│   ├── catches/
│   │   └── santiago-core-architecture/
│   └── kg/
│       └── santiago_core.ttl
└── src/                            # Code (symlink to src/nusy_pm_core/)
    └── santiago_core/
```

**Benefits**:
- ✅ Structured like any PM product
- ✅ BDD tests define capabilities
- ✅ Knowledge graph knows itself
- ✅ Can answer "What can santiago-core do?"
- ✅ Proves santiago-pm tools work!

## Implementation Plan

### Phase 1: Scaffold Structure (1 hour)

**Task 1.1**: Create santiago-core/ directory structure
```bash
mkdir -p santiago-core/{cargo-manifests,strategic-charts,expeditions,ships-logs,passages,quality-assessments,knowledge/{catches,kg},templates}
```

**Task 1.2**: Move existing assets
- Move `EXPEDITION-neurosymbolic-domain-expert.md` → `santiago-core/expeditions/`
- Move `notebooks/santiago-core-*.ipynb` → `santiago-core/expeditions/neurosymbolic-bdd-executor/`
- Create symlink: `santiago-core/src/` → `../src/nusy_pm_core/`

**Task 1.3**: Create foundational documents
- `santiago-core/README.md`: Vision, architecture, getting started
- `santiago-core/strategic-charts/roadmap-2025.md`: Phases 1-4 from expedition
- `santiago-core/strategic-charts/architecture-vision.md`: Three-part architecture (BDD, Q&A, Tools)

**Deliverable**: Santiago-core has PM structure

### Phase 2: Define Features as BDD Tests (1.5 hours)

**Task 2.1**: Neurosymbolic Reasoning Feature
```gherkin
# santiago-core/cargo-manifests/neurosymbolic-reasoning.feature
Feature: Neurosymbolic Reasoning Over Knowledge Graphs
  As a domain expert
  I want to reason over RDF knowledge graphs
  So that I can answer questions with confidence and provenance

  Scenario: Extract keywords from natural language
    Given a natural language question "What are the PM tools?"
    When I extract keywords
    Then I should get ["tools"] (>3 chars filter)
    
  Scenario: Query knowledge graph for evidence
    Given keywords ["tools", "management"]
    When I traverse the knowledge graph
    Then I should find matching triples
    And calculate confidence based on evidence
```

**Task 2.2**: BDD Test Execution Feature
```gherkin
# santiago-core/cargo-manifests/bdd-test-execution.feature
Feature: BDD Test Execution via Knowledge Graph
  As a quality engineer
  I want to validate test coverage using KG reasoning
  So that I can identify knowledge gaps

  Scenario: Execute BDD scenario as question
    Given a BDD scenario "Create roadmap with milestones"
    When I convert to natural language question
    And query the knowledge graph
    Then I should return pass/fail with provenance
```

**Task 2.3**: Human Q&A Feature
```gherkin
# santiago-core/cargo-manifests/human-qa-interface.feature
Feature: Human Question Answering
  As a product manager
  I want to ask questions about the domain
  So that I can get trusted answers with sources

  Scenario: Answer question with provenance
    Given a human asks "How do I create a roadmap?"
    When I query the validated knowledge graph
    Then I should return answer with sources
    And include confidence score
```

**Task 2.4**: MCP Tool Integration Feature
```gherkin
# santiago-core/cargo-manifests/mcp-tool-integration.feature
Feature: MCP Tool Execution Backed by Knowledge
  As a tool user
  I want tools backed by validated knowledge
  So that I can trust the tool behavior

  Scenario: Tool queries validated knowledge
    Given an MCP tool "create_roadmap"
    When the tool executes
    Then it should query the knowledge graph
    And return results with provenance
```

**Deliverable**: Santiago-core capabilities defined as BDD features

### Phase 3: Ingest Santiago-Core Knowledge (1.5 hours)

**Task 3.1**: Catchfish Santiago-Core Architecture
- Source: `ARCHITECTURE.md`, `DEVELOPMENT_PLAN.md`, expedition docs
- Run: `catchfish ingest santiago-core-architecture`
- Output: `santiago-core/knowledge/catches/santiago-core-architecture/`

**Task 3.2**: Catchfish Santiago-Core Code
- Source: `src/nusy_pm_core/santiago_core_bdd_executor.py`, `kg_store.py`
- Run: `catchfish ingest santiago-core-code`
- Output: Code entities, relationships, docstrings

**Task 3.3**: **Catchfish Neurosymbolic Domain Knowledge**
- **Source**: Search and ingest everything about neurosymbolic reasoning and systems
  - Academic papers: Neurosymbolic AI, hybrid reasoning, knowledge graphs
  - Reference implementations: Clinical prototype, other neurosymbolic systems
  - Theory: Symbolic reasoning + neural networks, confidence scoring
  - Best practices: Keyword extraction, graph traversal, provenance tracking
- **Run**: `catchfish ingest neurosymbolic-reasoning-domain`
- **Output**: `santiago-core/knowledge/catches/neurosymbolic-reasoning/`
- **Purpose**: Santiago-core becomes expert on neurosymbolic reasoning itself
  - Can answer "What is neurosymbolic reasoning?"
  - Can explain "How does confidence scoring work?"
  - Can guide "How to improve keyword extraction?"

**Task 3.4**: Build Santiago-Core KG
- Combine catches into RDF graph
- Store: `santiago-core/knowledge/kg/santiago_core.ttl`
- Triples: 
  - Architecture concepts (santiago-core design)
  - Code entities (implementation details)
  - Capability mappings (BDD, Q&A, Tools)
  - **Neurosymbolic domain knowledge** (theory, methods, best practices)

**Task 3.5**: Validate with BDD Tests
- Run santiago-core BDD tests against santiago-core KG
- Measure: Can santiago-core answer questions about itself AND neurosymbolic reasoning?
- Target: 80%+ coverage on self-knowledge, 70%+ on neurosymbolic domain

**Example Questions Santiago-Core Should Answer**:
- "What are santiago-core's three capabilities?" (self-knowledge)
- "How does neurosymbolic reasoning work?" (domain expertise)
- "What is the difference between symbolic and neural reasoning?" (theory)
- "How should I tune confidence thresholds?" (best practices)
- "What are the limitations of keyword-based matching?" (domain knowledge)

**Deliverable**: Santiago-core knowledge graph about itself + neurosymbolic reasoning domain

### Phase 4: Self-Query Demonstration (1 hour)

**Task 4.1**: Build Santiago-Core Q&A CLI
```python
# santiago-core/scripts/santiago_expert.py
@click.command()
@click.argument("question")
def ask(question: str):
    """Ask santiago-core about itself."""
    kg = load_santiago_core_kg()
    reasoner = SantiagoCoreNeurosymbolicReasoner()
    
    result = reasoner.query_graph(question, kg)
    
    print(f"Answer: {result['answer']}")
    print(f"Confidence: {result['confidence']:.2f}")
    print(f"Sources: {', '.join(result['sources'])}")
```

**Task 4.2**: Demo Questions (Self-Knowledge + Domain Expertise)

**Self-Knowledge Questions**:
```bash
$ santiago-expert "What are santiago-core's three capabilities?"
Answer: BDD test execution, human Q&A, and MCP tool integration
Confidence: 0.95
Sources: architecture-vision.md, santiago_core_bdd_executor.py

$ santiago-expert "What is the current test pass rate?"
Answer: 46.5% (47/101 scenarios passing)
Confidence: 0.92
Sources: quality-assessments/neurosymbolic-test-coverage.md
```

**Domain Expertise Questions (Neurosymbolic Reasoning)**:
```bash
$ santiago-expert "What is neurosymbolic AI?"
Answer: Hybrid approach combining symbolic reasoning (knowledge graphs, logic) 
        with neural networks for interpretable, provable AI systems
Confidence: 0.94
Sources: neurosymbolic-ai-survey.md, clinical-prototype-architecture.md

$ santiago-expert "How does confidence scoring work in neurosymbolic systems?"
Answer: Evidence-based calculation using triple counts, keyword matches, and 
        graph connectivity. Common approaches: linear, logarithmic, or Bayesian
Confidence: 0.88
Sources: confidence-scoring-methods.md, santiago_core_bdd_executor.py

$ santiago-expert "What are best practices for keyword extraction?"
Answer: Filter stop words, use domain-specific terms, consider stemming/lemmatization,
        balance precision vs recall based on use case
Confidence: 0.85
Sources: keyword-extraction-best-practices.md, nlp-for-kg-queries.md

$ santiago-expert "Why use RDF for knowledge representation?"
Answer: Standard format, supports reasoning, enables SPARQL queries, 
        provides semantic interoperability across domains
Confidence: 0.91
Sources: rdf-primer.md, knowledge-graph-standards.md
```

**Task 4.3**: Meta-validation
- Santiago-core answers questions about santiago-core
- Provenance shows which santiago-core docs were used
- Confidence indicates knowledge quality
- **Proves the concept works!**

**Deliverable**: Working self-aware santiago-core

### Phase 5: Integration & Documentation (1 hour)

**Task 5.1**: Update ARCHITECTURE.md
- Add santiago-core as product
- Show santiago-pm managing santiago-core
- Document bootstrap relationship

**Task 5.2**: Create ships-log entry
- Document expedition results
- Show before/after structure
- Demonstrate self-query capability

**Task 5.3**: Update Navigator
- Add santiago-core domain
- Enable santiago-core expeditions
- Support santiago-core ingestion

**Task 5.4**: README updates
- Root README: Mention santiago-core self-management
- Santiago-core README: Complete getting started
- Santiago-pm README: Add "Managing Santiago-Core" example

**Deliverable**: Documented, integrated, demo-ready

## Success Metrics

### Quantitative
- **Structure**: Santiago-core has complete PM folder structure ✅
- **Features**: 4+ BDD feature files defining capabilities ✅
- **Knowledge**: Santiago-core KG with 2000+ triples (self + neurosymbolic domain) ✅
- **Self-Query**: 80%+ coverage answering questions about itself ✅
- **Domain-Query**: 70%+ coverage answering neurosymbolic reasoning questions ✅
- **Integration**: Navigator supports santiago-core domain ✅

### Qualitative
- **Dogfooding**: Santiago-pm tools manage santiago-core product ✅
- **Self-Awareness**: Santiago-core knows its own architecture ✅
- **Domain Expertise**: Santiago-core is expert on neurosymbolic reasoning ✅
- **Meta-Validation**: Proves the neurosymbolic approach works ✅
- **Teaching Capability**: Can explain neurosymbolic concepts to users ✅
- **Reusable**: Pattern applies to other domains (lean-kanban, SAFe) ✅

## Risks & Mitigations

### Risk 1: Circular Dependency
**Problem**: Santiago-core manages santiago-core  
**Mitigation**: Santiago-pm tools are domain-agnostic, santiago-core is just another domain  
**Status**: Not a real risk - separation of concerns maintained

### Risk 2: Knowledge Sparsity
**Problem**: Not enough docs/code to build meaningful KG  
**Mitigation**: Supplement with expedition notes, commit messages, test results  
**Status**: Manageable - have expedition doc, code, notebooks, tests

### Risk 3: Scope Creep
**Problem**: Could expand into full self-hosting system  
**Mitigation**: Timebox to 6 hours, focus on scaffolding + basic self-query  
**Status**: Clear scope, defined deliverables

## Prerequisites (from Current Expedition)

**Must Complete First**:
1. ✅ Neurosymbolic BDD executor working (baseline established)
2. ⏳ Pass rate ≥75% (Phase 1 optimization)
3. ⏳ Multi-hop reasoning (Phase 2)
4. ⏳ CLI tool for human Q&A (Phase 3 foundation)
5. ✅ Navigator integration (Phase 4)

**Why Wait**: Need working santiago-core before managing it as product

## When to Execute

**After Current Expedition** when:
- ✅ Neurosymbolic BDD executor merged to main
- ✅ Pass rate ≥90% (validated approach)
- ✅ CLI tool exists (can demo self-query)
- ✅ Navigator integrated (proves production-ready)

**Estimated Start**: After current expedition completes (~1 week)

## Decision: Do It After Expedition

**Recommendation**: ⏸️ **Pause this plan, continue current expedition**

**Reasoning**:
1. **Current expedition focused**: 46.5% → 90%+ pass rate is critical
2. **Need working product first**: Can't manage what doesn't fully exist
3. **Clean separation**: Finish one, start next (good workflow)
4. **Validates completion**: Self-management is graduation ceremony

**Next Steps** (for current expedition):
1. Fix keyword→KG matching (54 zero-triple tests)
2. Phase 1 optimization: Reach 75% pass rate
3. Phase 2 multi-hop: Reach 90% pass rate
4. Phase 3 CLI: Human Q&A interface
5. Phase 4 integration: Replace Navigator Step 7

**Then** (next session):
6. Execute this self-management expedition
7. Demonstrate santiago-core managing itself
8. Move to next domain (Lean-Kanban)

---

**Status**: 📋 **Planned - Execute After Current Expedition**  
**Confidence**: High - clear plan, validated approach, proper sequencing  
**Value**: Maximum - proves concept, enables scaling to other domains
