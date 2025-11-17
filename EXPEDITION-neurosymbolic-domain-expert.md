# Expedition: Neurosymbolic Domain Expert

**Branch**: `expedition/neurosymbolic-bdd-executor`  
**Started**: 2025-11-17  
**Status**: In Progress  

## Mission Statement

Build a **unified neurosymbolic domain expert** that serves two primary use cases:
1. **BDD Test Coverage**: Answer test scenarios as questions, track provenance
2. **Human Q&A**: Answer human questions using validated knowledge with provenance

**Key Insight**: These are the *same capability* - knowledge-based question answering with provenance tracking. The domain expert validates its knowledge through BDD coverage, then uses that same validated knowledge to answer human questions.

## Architecture Vision

```
Domain Knowledge Sources (markdown, code, docs)
    ↓
CatchFish Extraction (4-layer L0-L3)
    ↓
Knowledge Graph (RDF triples)
    ↓
Neurosymbolic Reasoner (keyword + graph traversal)
    ↓
    ├─→ BDD Test Executor (validates coverage)
    └─→ Human Q&A Interface (answers questions)
```

**Quality Loop**: BDD coverage → identifies knowledge gaps → guides new ingestion → increases coverage → better Q&A

## Current State (Baseline)

### Implemented ✅
- `santiago_core_bdd_executor.py`: Neurosymbolic reasoner + BDD executor (380 lines)
- Clinical prototype pattern: Simple keyword extraction + graph traversal
- KG Storage: 3,300 triples from santiago-pm domain
- Notebook demonstration: End-to-end execution

### Metrics (Baseline)
- **BDD Pass Rate**: 46.5% (47/101 scenarios)
- **Confidence Threshold**: 0.7
- **Avg Confidence**: 0.465
- **Evidence**: 450 triples for passing tests
- **Execution Time**: 470ms for 101 scenarios

### Gap Analysis
- **Target**: 95% pass rate (simulated behave baseline)
- **Current**: 46.5% pass rate
- **Gap**: 48.5 percentage points
- **Root Causes**:
  - Threshold too high (0.7 vs clinical's 0.5)
  - Generic keyword extraction (not PM-optimized)
  - Single-hop reasoning only (no relationship traversal)

## Goals & Success Criteria

### Phase 1: Optimize for PM Domain (Current)
**Goal**: Close gap from 46.5% → 75% pass rate

**Success Criteria**:
- [ ] Lower threshold to 0.5 → expect ~65% pass rate
- [ ] Add PM-specific keyword filtering (remove noise words)
- [ ] Enhance question generation (extract entities from steps)
- [ ] Measure: Pass rate ≥ 75%, confidence scores align with correctness

**Deliverables**:
- Tuned reasoner with PM domain optimizations
- Updated notebook showing improvement
- Comparison report: baseline vs optimized

### Phase 2: Multi-Hop Reasoning
**Goal**: Close gap from 75% → 90% pass rate

**Success Criteria**:
- [ ] Implement relationship traversal (follow entity connections)
- [ ] Add SPARQL queries for complex patterns
- [ ] Support multi-entity questions
- [ ] Measure: Pass rate ≥ 90%, explanation quality improves

**Deliverables**:
- Enhanced reasoner with path-finding
- SPARQL query templates for PM domain
- Provenance shows reasoning paths

### Phase 3: Human Q&A Interface
**Goal**: Same reasoner, different interface

**Success Criteria**:
- [ ] CLI tool: `santiago-expert "What are the PM tools?"`
- [ ] Returns answer + provenance + confidence
- [ ] Uses same validated KG as BDD tests
- [ ] Measure: Human satisfaction, answer accuracy

**Deliverables**:
- `santiago_expert_cli.py`: Interactive Q&A
- Example questions with answers
- Provenance UI showing knowledge sources

### Phase 4: Integration & Coverage Loop
**Goal**: Close loop, integrate with Navigator

**Success Criteria**:
- [ ] Replace Navigator Step 7 simulated behave with neurosymbolic executor
- [ ] Failed tests → identify knowledge gaps
- [ ] Gap analysis → guide next ingestion (Lean-Kanban domain)
- [ ] Measure: Coverage improvement over iterations

**Deliverables**:
- Navigator integration complete
- Gap report: which scenarios need what knowledge
- Next domain ingestion plan

## Technical Approach

### Phase 1 Implementation Plan

#### 1.1 Lower Confidence Threshold
```python
# Change in executor initialization
executor = SantiagoCoreBDDExecutor(
    kg_store=kg_store,
    confidence_threshold=0.5  # Down from 0.7
)
```
**Expected Impact**: +18% pass rate (65% total)

#### 1.2 PM-Specific Keyword Filter
```python
def _extract_keywords(self, question: str) -> List[str]:
    # Remove PM noise words
    pm_noise = {'management', 'system', 'should', 'must', 'will'}
    
    # Add PM entity recognition
    pm_entities = r'\b(backlog|roadmap|sprint|epic|story|feature)\b'
    
    # Weight PM-specific terms higher
    ...
```
**Expected Impact**: +5% pass rate (better precision)

#### 1.3 Enhanced Question Generation
```python
def scenario_to_question(self, scenario: BDDScenario) -> str:
    # Extract quoted entities from steps
    entities = re.findall(r'"([^"]+)"', ' '.join(scenario.when_steps))
    
    # Combine: feature + scenario + key entities
    question = f"{scenario.feature_name} {scenario.scenario_name}"
    if entities:
        question += f" involving {', '.join(entities)}"
    
    return question
```
**Expected Impact**: +5% pass rate (richer questions)

### Validation Strategy

**After Each Phase**:
1. Run notebook: Execute all 101 BDD scenarios
2. Measure: Pass rate, avg confidence, execution time
3. Analyze: Which scenarios pass/fail, why?
4. Document: Changes, results, next steps
5. Commit: Feature branch with clear metrics

**Quality Gates**:
- Phase 1: Must achieve ≥75% pass rate
- Phase 2: Must achieve ≥90% pass rate
- Phase 3: Human users validate Q&A quality
- Phase 4: Navigator integration tests pass

### Rollback Plan

If approach fails:
1. **Keep**: KG storage, Catchfish/Fishnet pipeline
2. **Revert**: Back to simulated behave in Navigator
3. **Learn**: Document why neurosymbolic didn't work
4. **Alternative**: Hybrid approach (SPARQL + neural models)

## Resources & Timeline

### Current Session (6-8 hours)
- [x] Hour 1-3: Baseline implementation (DONE)
- [ ] Hour 4-5: Phase 1 optimization
- [ ] Hour 6-7: Phase 2 multi-hop reasoning
- [ ] Hour 8: Integration planning

### Future Sessions
- Session 2: Phase 3 Human Q&A interface
- Session 3: Phase 4 Navigator integration
- Session 4: Next domain (Lean-Kanban) ingestion

## Decision Log

### Decision 1: Use Clinical Prototype Pattern ✅
**Date**: 2025-11-17  
**Context**: Initial SPARQL approach failing (0% pass rate)  
**Decision**: Adopt simple clinical prototype pattern (keyword + graph traversal)  
**Rationale**: Clinical achieved 94.9% coverage with simple approach  
**Result**: 46.5% pass rate immediately (working baseline)

### Decision 2: Unified Domain Expert ✅
**Date**: 2025-11-17  
**Context**: User insight about dual use case  
**Decision**: Same reasoner for both BDD testing and human Q&A  
**Rationale**: Knowledge validation through BDD enables trusted Q&A  
**Impact**: Reframe as "domain expert" not just "test executor"

### Decision 3: [Next Decision]
**Date**: TBD  
**Context**: TBD  
**Decision**: TBD

## Next Steps

### Immediate (This Session)
1. **Tune Threshold**: Change 0.7 → 0.5, measure impact
2. **PM Keywords**: Add domain-specific filtering
3. **Question Enhancement**: Extract entities from steps
4. **Re-measure**: Run full test suite, document results
5. **Commit**: "feat: Phase 1 PM domain optimization"

### Next Session
6. **Multi-hop**: Implement relationship traversal
7. **SPARQL**: Add complex query patterns
8. **CLI Tool**: Build human Q&A interface
9. **Demo**: Show domain expert answering questions

### Integration
10. **Navigator Step 7**: Replace simulated behave
11. **Gap Analysis**: Which tests fail, what knowledge needed?
12. **Coverage Loop**: Use gaps to guide next ingestion

## Success Metrics

### Quantitative
- **BDD Pass Rate**: 46.5% → 75% → 90% → 95%
- **Confidence Alignment**: Confidence scores predict correctness
- **Execution Speed**: <1s for 101 scenarios
- **Provenance Coverage**: 100% of answers cite sources

### Qualitative
- **Explainability**: Users understand why tests pass/fail
- **Trust**: Provenance builds confidence in answers
- **Utility**: Human Q&A provides value to PM work
- **Maintainability**: Simple code, easy to extend

## Notes & Observations

### Key Insight: Domain Expert = Test Validator + Q&A System
The BDD tests validate the domain knowledge, creating a **quality-assured knowledge base** that can answer human questions with confidence. This is more powerful than either:
- **BDD alone**: Tests validate but don't expose knowledge
- **Q&A alone**: Answers without validation/provenance

**Combined**: Validated knowledge → trusted answers with proof

### Clinical Prototype Lessons
1. **Simple works**: Keyword matching + graph traversal beats complex SPARQL
2. **Domain matters**: PM needs different keywords than clinical
3. **Confidence calibration**: Threshold determines precision vs recall
4. **Provenance essential**: Knowing "why" builds trust

### PM Domain Characteristics
- **Entity-rich**: Many quoted strings (roadmap names, feature titles)
- **Relationship-heavy**: Tools link to concepts, concepts to outcomes
- **Hierarchical**: Features → stories → tasks → subtasks
- **Temporal**: Planning, execution, retrospection phases

---

**Branch**: `expedition/neurosymbolic-bdd-executor`  
**Merge When**: Pass rate ≥ 90%, human Q&A demo successful, Navigator integration ready  
**Review**: Compare with main branch behave simulation, document trade-offs
