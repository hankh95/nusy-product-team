# Santiago PM Builder - Development Plan

**Status**: In Progress (Tasks 11, 13, 14 complete)  
**Current Phase**: Knowledge Graph Ingestion (Tasks 9-18)  
**Started**: 2025-01-16  
**Last Updated**: 2025-01-16

## Vision

Build a self-bootstrapping factory that creates domain-specific Santiagos by ingesting domain knowledge and generating MCP services. Start with Santiago-PM ingesting its own domain structure to prove the bootstrap capability.

## Success Criteria

1. ✅ Santiago-PM can read its own domain structure (ontology created)
2. ✅ Extract 15-20 PM behaviors from santiago-pm docs (20 extracted)
3. ✅ Generate MCP manifest with proper tool schemas (20 tools, 6 categories)
4. 🚧 Implement Fishnet (BDD test generation from behaviors)
5. 🚧 Implement Navigator (10-step fishing process orchestration)
6. ⏳ Santiago-PM can manage itself using its own tools (demo)

## Architecture Context

### The 10-Step Fishing Process (from "Old Man and the Sea")

1. **Vision** - Define MCP services/behaviors for target domain
2. **Raw Materials** - Collect sources (docs, APIs, experts)
3. **Catchfish Extraction** - Process into structured knowledge (4 layers)
4. **Indexing** - Make knowledge highly referenceable
5. **Ontology Loading** - Apply schemas/naming conventions
6. **KG Building** - Store in knowledge graph with provenance
7. **Fishnet BDD Generation** - Generate behavior tests
8. **Navigator Validation Loop** - Iterate 3-5 cycles until ≥95% pass rate
9. **Deployment** - Generate MCP manifest, deploy service
10. **Learning** - Improve from logs/metrics

### Key Components

- **Catchfish**: 4-layer extraction (Raw Text → Entities → Structured Docs → KG Triples)
  - Location: `nusy_orchestrator/santiago_builder/catchfish.py`
  - Status: Implemented (demo version)
  
- **Fishnet**: BDD test generation from behaviors
  - Location: `nusy_orchestrator/santiago_builder/fishnet.py`
  - Status: Stub exists, needs implementation
  
- **Navigator**: Orchestrates 10-step process with validation cycles
  - Location: `nusy_orchestrator/santiago_builder/navigator.py`
  - Status: Skeleton exists, needs full implementation

## Task Breakdown (18 Tasks Total)

### Phase 1: Bootstrap Foundation (Tasks 1-8) ✅ COMPLETE
- Task 1-8: Prior work (vision docs, architecture patterns, fake team setup)

### Phase 2: Santiago-PM Ingestion (Tasks 9-18) 🚧 IN PROGRESS

#### ✅ Task 9: Map santiago-pm structure for ingestion
**Status**: Completed 2025-01-16  
**Output**: `knowledge/ingestion-maps/santiago-pm-ingestion-map.md` (636 lines)
- Classified 14 folders as data vs tools
- Identified 7 agent roles → 15+ MCP tool behaviors
- Mapped status system, notes relationships, experiment framework

#### ✅ Task 10: Design PM domain ontology
**Status**: Completed 2025-01-16  
**Output**: `knowledge/ontologies/pm-domain-ontology.ttl` (882 lines)
- Researched W3C standards (PROV-O, ORG, DCMI)
- Gap analysis: 40% coverage from standards, 60% custom needed
- 6-layer architecture: Foundation → Base → Domain → Status → Roles → Behaviors
- 8 artifact classes, 50+ properties, 6 note relationships
- 14 PM behaviors defined as prov:Activity subclasses
- CC BY 4.0 license for community adoption

#### ✅ Task 11: Extract PM behaviors from santiago-pm docs
**Status**: Completed 2025-01-16  
**Output**: `knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md` (1221 lines)
- Extraction Strategy: DocumentFirst + SchemaDriven
- 20 behaviors extracted across 6 categories
- 100% ontology coverage (14/14 defined behaviors mapped)
- Completeness: 0.85 (85% of PM domain)
- Sources: 11 key files analyzed

#### 🚧 Task 12: Run Navigator expedition on santiago-pm
**Status**: Ready to Start (Fishnet + Navigator implemented)  
**Dependencies**: Task 11 ✅, Fishnet ✅, Navigator v2.0.0 ✅
**Approach**: Full 10-step process (Vision → Learning)
- Input: 59 santiago-pm .md files
- Expected: 200-300 KG triples, 84+ BDD scenarios, ≥95% pass rate after 3-5 cycles
- **Phase 2 Complete**: Fishnet multi-strategy BDD + Navigator v2.0.0 merged to main
- **BDD Location**: knowledge/catches/[domain]/bdd-tests/ (generated tests)
- **Next**: Execute full Navigator expedition on santiago-pm domain

#### ✅ Task 13: Identify MCP tool candidates from PM domain
**Status**: Completed 2025-01-16  
**Output**: `knowledge/catches/santiago-pm-behaviors/mcp-tool-classification.md` (428 lines)
- Classified all 20 behaviors as data vs tools
- Data: 7 artifact types (cargo-manifests, ships-logs, etc.)
- Tools: 20 MCP tools across 6 categories
- Mapped capability levels (Apprentice → Expert)
- Mapped knowledge scopes (Pond → Ocean)
- Identified concurrency risks (4 non-safe tools)

#### ✅ Task 14: Generate santiago-pm MCP manifest
**Status**: Completed 2025-01-16  
**Output**: `knowledge/catches/santiago-pm-behaviors/santiago-pm-mcp-manifest.json` (1131 lines)
- 20 tools with complete JSON schemas
- 6 categories: Status, Feature, Issue, Experiment, Knowledge, Strategic
- Input/output schemas for all tools
- Concurrency annotations (mutates_kg, safe flags)
- Quality gates defined (≥95% BDD pass, ≥95% coverage)
- Budget hints for each tool

#### ✅ Task 15: Implement PM domain scaffold system
**Status**: Completed 2025-11-17  
**Output**: `src/nusy_pm_core/adapters/scaffold_recognizer.py` (450+ lines)
**Approach**: Meta-learning system that learns organizational patterns by studying santiago-pm/
- Learned 14 organizational patterns (9 PM artifacts + 5 tackle implementations)
- Pattern recognition across multiple expertise sources:
  - EARS methodology (initial inspiration for project scaffolding)
  - External PM thought leaders (Jeff Patton, Jeff Gothelf, Nielsen Norman, SAFe)
  - Internal domain knowledge (vision docs, architecture patterns)
  - Human PM experience (real-world practices encoded in folder structure)
- Suggests missing folders based on related pattern presence
- Suggests tackle implementations for new domains (90% confidence from status template)
- Exports learned patterns to YAML for KG integration

**Key Capabilities**:
- `learn_patterns()`: Scans santiago-pm/ to extract organizational patterns
- `suggest_missing_folders()`: Identifies gaps in current structure
- `suggest_tackle_implementation()`: Proposes implementation structure for new domains
- `export_learned_patterns()`: Generates YAML for knowledge graph integration

**Demo Results**:
- Learned 9 PM artifact patterns (cargo-manifests, ships-logs, voyage-trials, etc.)
- Learned 5 tackle implementation patterns (status is most complete with 4 files)
- All expected folders present in santiago-pm/ (no suggestions needed)
- Successfully suggested "feedback" tackle implementation with 7 files
- Patterns exported to `knowledge/catches/scaffold-patterns-learned.yaml`

**Meta-Learning Achievement**: Santiago learned how to organize domains by studying its own structure ✨

#### ⏳ Task 16: Create santiago-pm-self-aware demo
**Status**: Not Started  
**Dependencies**: Tasks 11, 13, 14 ✅, Fishnet, Navigator implementations
**Approach**: End-to-end demonstration
- Input: santiago-pm/ folder
- Process: Navigator orchestrates full pipeline
- Output: Santiago that understands its own PM domain
- Validates: Bootstrap capability, self-awareness, meta-learning
- Demo script: Query KG, execute MCP tools, scaffold suggestions

#### ✅ Task 17: Scan docs/vision for additional sources
**Status**: Completed 2025-11-17  
**Output**: `knowledge/catches/vision-knowledge-extracted.md` (900+ lines)
- 4 categories: Factory Architecture, Fake Team Strategy, DGX Deployment, Development Patterns
- 11 new architectural behaviors identified (factory orchestration, deployment)
- Ontology Layer 8 design: Factory & Deployment (11 classes, 15 properties)
- Key insights: 30-60m Catchfish bottleneck, progressive replacement strategy, DGX Spark specs
- Completeness: 0.85 (85% vision domain coverage)

#### ✅ Task 18: Extract External PM Thought Leader Knowledge
**Status**: Completed 2025-01-16  
**Output**: `knowledge/catches/external-pm-knowledge-extracted.md` (1300+ lines)
**Approach**: Fetched 5 websites (Jeff Patton, Jeff Gothelf, Nielsen Norman, SAFe PO/PM)
- Extracted 30 PM behaviors related to UX research competency and expedition-based learning
- 4 categories: Discovery & Hypothesis, Expedition Execution, Measurement & ROI, Infrastructure & Enablement, Strategic Alignment
- Layer 9 ontology design: Discovery & Research (6 classes, 13 properties)
- Santiago-UX role specification (draft)
- Lean UX → Santiago-PM methodology crossover documented
- Key insight: "How to run expeditions to learn when we don't know something" = core PM competency
- Completeness: 0.90 (90%) - 5 of 5 sources processed

#### ✅ Task 19: Implement multi-strategy BDD generation in Fishnet
**Status**: Completed 2025-01-17 (Phase 2)  
**Output**: Multi-strategy Fishnet + Navigator v2.0.0 + 84 BDD scenarios
**Phase 2 Components**:
- **PR #8**: 84 BDD scenarios (28 files in knowledge/catches/santiago-pm-behaviors/bdd-tests/)
  - All scenarios pass behave validation (672 steps)
  - Common step definitions in steps/common_steps.py
  - GENERATION_REPORT.md documents strategy usage
- **PR #9**: Multi-strategy BDD generation framework
  - nusy_orchestrator/santiago_builder/strategies/ module
  - 4 strategies implemented: top-down, bottom-up, external, logic
- **PR #10**: Fishnet refactoring with strategy pattern
  - FishnetStrategy base class + concrete implementations
  - Enhanced BDD generation pipeline
  - 11 Fishnet tests passing
- **PR #11**: Navigator v2.0.0 with 10-step orchestration
  - Full fishing expedition workflow
  - Validation cycle management (3-5 cycles, 95% target)
  - Expedition logging to voyage-trials/
  - 22 Navigator tests passing

**Architecture Decisions**:
- BDD location: knowledge/catches/[domain]/bdd-tests/ (generated tests)
- Human specs: santiago-pm/cargo-manifests/*.feature (requirements)
- Fishnet writes to catches/, Navigator validates from catches/
- No code changes needed - PR #8 location aligned with implementation

**Merged**: 2025-01-17 to main branch

## Current Focus: Run Navigator Expedition (Task 12)

**Phase 2 Complete**: ✅ Fishnet + Navigator implemented and merged
- Fishnet multi-strategy BDD generation working
- Navigator v2.0.0 orchestrates full 10-step fishing process
- 84 BDD scenarios generated and validated
- All tests passing (behave + unit tests)

**Ready for Task 12**: Full Navigator expedition on santiago-pm domain
1. Execute Navigator.run_expedition() on santiago-pm/
2. Catchfish extracts PM knowledge (already have 20 behaviors)
3. Fishnet generates comprehensive BDD tests (targeting 95%+ pass rate)
4. Navigator manages 3-5 validation cycles
5. Deploy santiago-pm-self-aware catch with MCP manifest
6. Learning phase captures expedition metrics

**Expected Outcomes**:
- 200-300 KG triples (PM domain knowledge)
- 84+ BDD scenarios with 95%+ pass rate
- Complete MCP manifest with 20 tools
- Expedition log in voyage-trials/
- Validated self-bootstrap capability

## Implementation Status

### Completed Components ✅
- PM domain ontology (pm-domain-ontology.ttl)
- Behavior extraction (20 behaviors documented)
- MCP tool classification (6 categories)
- MCP manifest generation (20 tools with schemas)
- PM domain scaffold system (meta-learning from santiago-pm/)
- Vision knowledge extraction (factory architecture + deployment)
- External PM knowledge (Lean UX, ResearchOps, Story Mapping, SAFe)
- **Phase 2: Fishnet multi-strategy + Navigator v2.0.0** ✅
- **84 BDD scenarios generated and validated** ✅

### Ready to Execute 🚀
- Task 12: Navigator expedition on santiago-pm domain
- Full fishing process validation
- Self-aware Santiago demonstration

### Future Tasks ⏳
- Task 16: Santiago-PM-self-aware demo (after Task 12)
- Lean-Kanban domain ingestion (feature created, ready to pull)
- Artifact orchestration implementation (5 phases)

## Quality Gates

### For Deployment (Navigator Step 9)
- ✅ BDD pass rate ≥95%
- ✅ Test coverage ≥95%
- ✅ KG completeness ≥90%
- ✅ Extraction time <60m per source (baseline), <15m target
- ✅ 3-5 validation cycles completed
- ✅ Complete provenance tracking

### For Self-Awareness (Task 16 Demo)
- ⏳ Santiago can query its own PM knowledge graph
- ⏳ Santiago can execute MCP tools to manage itself
- ⏳ Santiago can suggest improvements to its own structure
- ⏳ Bootstrap loop validated (reads own ontology → improves self)

## Risks & Mitigations

### Risk 1: Context Loss (AI Session Limits)
**Impact**: Lose progress, have to re-explain architecture  
**Mitigation**: 
- ✅ This development plan captures full context
- ✅ Ships-logs capture daily progress
- ✅ Each task produces committed artifacts (ontology, extractions, manifests)
- ✅ Git commits preserve provenance

### Risk 2: Navigator Complexity
**Impact**: Full 10-step orchestration is complex, may take time  
**Mitigation**:
- ✅ Built components incrementally (Catchfish → Fishnet → Navigator)
- ✅ Defer Task 12 (Navigator expedition) until Fishnet working
- ⏳ Test each component independently before integration

### Risk 3: Incomplete Domain Coverage
**Impact**: 85% completeness on Task 11, some PM behaviors missing  
**Mitigation**:
- ✅ Ontology designed to be extensible
- ⏳ Task 17-18 will add more PM knowledge (vision docs, external sources)
- ⏳ Validation cycles (Task 12) will identify gaps
- ⏳ Scaffold system (Task 15) enables incremental learning

### Risk 4: BDD Test Quality
**Impact**: Generated BDD tests may not adequately validate behaviors  
**Mitigation**:
- ⏳ Task 19 implements 4 BDD strategies (comprehensive coverage)
- ⏳ Navigator validation loops enforce ≥95% pass rate
- ⏳ Human review of BDD scenarios before deployment
- ⏳ Experiment-driven resolution for unknown edge cases

## Next Steps (Immediate)

1. **Implement Fishnet BDD Generation**
   - Enhance `nusy_orchestrator/santiago_builder/fishnet.py`
   - Generate 60 BDD scenarios (20 behaviors × 3 scenarios)
   - Output to `knowledge/catches/santiago-pm-behaviors/bdd-tests/`
   - Validate against Task 11 extracted behaviors

2. **Test Fishnet Output**
   - Manually review generated .feature files
   - Ensure Gherkin syntax correct
   - Verify KG node references
   - Check scenario coverage (happy path, edge case, error)

3. **Implement Navigator Orchestration**
   - Enhance `nusy_orchestrator/santiago_builder/navigator.py`
   - Implement validation loop (steps 3-7 repeated 3-5 times)
   - Add quality gates (≥95% BDD pass rate)
   - Provenance logging to ships-logs/

4. **Run Task 12 (Navigator Expedition)**
   - Full 10-step process on all 59 santiago-pm files
   - Generate complete catch: KG + BDD + MCP manifest
   - Prove bootstrap capability

5. **Build Task 16 Demo**
   - Santiago queries its own PM knowledge graph
   - Santiago executes MCP tools to manage itself
   - Santiago suggests scaffold improvements
   - Validate self-awareness

## Dependencies

```
Task 9 → Task 10 → Task 11 → Task 13 → Task 14
                      ↓
                   Task 12 (deferred) → Task 16
                      ↑
                   Fishnet impl → Navigator impl
                      
Task 17, 18 (parallel, no dependencies)

Task 15 (EARS scaffolds) ← Task 16 (demo shows scaffold usage)

Task 19 (multi-strategy BDD) ← Fishnet basic impl
```

## Lessons Learned (So Far)

1. **Research First**: Task 10 emphasized researching W3C standards before creating custom ontology - found PROV-O, ORG, DCMI cover 40%, custom 60%
2. **Bootstrap Validates Design**: Extracting Santiago-PM's own behaviors (Task 11) proved ontology design works
3. **Build Order Matters**: Realized Navigator needs Fishnet working first - better to build incrementally
4. **Documentation Prevents Context Loss**: Development plan + ships-logs + committed artifacts = recoverable state
5. **Multi-Strategy Is Powerful**: Tasks 19 & Catchfish strategies show single approach insufficient - need 4-5 strategies for completeness

## References

- Santiago-PM Vision: `santiago-pm/strategic-charts/Old man and the sea.md`
- Architecture Pattern: `docs/vision/00-ARCHITECTURE-PATTERN.md`
- Ingestion Map: `knowledge/ingestion-maps/santiago-pm-ingestion-map.md`
- PM Ontology: `knowledge/ontologies/pm-domain-ontology.ttl`
- Extracted Behaviors: `knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md`
- MCP Manifest: `knowledge/catches/santiago-pm-behaviors/santiago-pm-mcp-manifest.json`

---

**Note**: This development plan is a living document. Update after each task completion or architectural decision.
