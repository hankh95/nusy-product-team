# Phase 3 Integration Test Plan

**Expedition**: hybrid-coordination-001  
**Phase**: 3 - Integration & Validation  
**Purpose**: Verify that Fishnet + Navigator implementations work end-to-end with 28 PM behaviors

---

## Test Objectives

1. **Functional Correctness**: All 84 .feature files generated correctly
2. **Quality Gates Met**: ≥95% BDD pass rate, ≥95% coverage, ≥90% KG completeness
3. **Integration Works**: Navigator orchestrates Catchfish → Fishnet → Validation successfully
4. **Architecture Alignment**: Implementations match architecture specs from Phase 1
5. **Performance Acceptable**: Within estimated time budgets

---

## Pre-Integration Checklist

### PR Review Criteria (Phase 3 Start)

**For each PR (#8, #9, #10, #11):**

- [ ] **Code Quality**
  - [ ] Follows Python standards (type hints, docstrings, formatting)
  - [ ] No linting errors (flake8, black, isort, mypy)
  - [ ] Code structure matches architecture spec
  - [ ] Proper error handling and logging

- [ ] **Testing Coverage**
  - [ ] Unit tests for all classes/functions
  - [ ] Unit test coverage ≥95%
  - [ ] Tests pass locally and in CI
  - [ ] Edge cases and error conditions tested

- [ ] **Architecture Alignment**
  - [ ] Strategy pattern implemented correctly (Fishnet)
  - [ ] Data classes match specification (BehaviorSpec, BDDScenario, BDDFeatureFile)
  - [ ] 10-step orchestration follows design (Navigator)
  - [ ] Validation loop logic correct (3-5 cycles)

- [ ] **Documentation**
  - [ ] README updated with usage instructions
  - [ ] API documentation complete
  - [ ] Example code provided
  - [ ] Comments explain complex logic

- [ ] **Integration Points**
  - [ ] Interfaces match between components
  - [ ] File paths and naming conventions correct
  - [ ] Import statements resolve correctly
  - [ ] No circular dependencies

---

## Integration Test Scenarios

### Scenario 1: BDD File Generation (Issue #5 / PR #8)

**Test**: Verify 84 .feature files generated correctly

```bash
# Expected output structure
knowledge/catches/santiago-pm-behaviors/bdd-tests/
├── create_feature.feature
├── update_feature.feature
├── delete_feature.feature
... (84 total files)
```

**Validation Checklist:**
- [ ] 84 .feature files exist (28 behaviors × 3 scenarios - if separate files)
- [ ] OR 28 .feature files exist with 3 scenarios each
- [ ] All files have valid Gherkin syntax
- [ ] Each file has Background section
- [ ] Each scenario has Given/When/Then steps
- [ ] Tags include @capability_level and @knowledge_scope
- [ ] Input/output schemas referenced in steps
- [ ] `behave --dry-run bdd-tests/` passes without errors

**Test Command:**
```bash
cd knowledge/catches/santiago-pm-behaviors/
behave --dry-run bdd-tests/ --no-skipped
```

**Success Criteria:**
- All .feature files parse successfully
- No syntax errors reported
- Scenario count matches expectation (84 total or 3 per file)

---

### Scenario 2: Fishnet Multi-Strategy Implementation (Issue #6 / PRs #9, #10)

**Test**: Verify Fishnet can generate BDD files programmatically

```bash
# Test Fishnet CLI
python nusy_orchestrator/santiago_builder/fishnet.py \
  --behaviors knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md \
  --ontology knowledge/ontologies/pm-domain-ontology.ttl \
  --output /tmp/fishnet-test-output/ \
  --strategies bottom_up
```

**Validation Checklist:**
- [ ] Fishnet.py runs without errors
- [ ] BottomUpStrategy class exists and works
- [ ] Base strategy pattern implemented (base_strategy.py)
- [ ] Data classes exist (BehaviorSpec, BDDScenario, BDDFeatureFile)
- [ ] 84 .feature files generated in output directory
- [ ] Generated files match hand-crafted files from PR #8
- [ ] CLI arguments work (--behaviors, --ontology, --output, --strategies)
- [ ] Unit tests pass: `pytest tests/test_fishnet.py`

**Test Command:**
```bash
# Run Fishnet
python nusy_orchestrator/santiago_builder/fishnet.py \
  --behaviors knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md \
  --behaviors knowledge/catches/santiago-pm-behaviors/passage-behaviors-extracted.md \
  --ontology knowledge/ontologies/pm-domain-ontology.ttl \
  --output /tmp/fishnet-test/ \
  --strategies bottom_up

# Validate output
behave --dry-run /tmp/fishnet-test/ --no-skipped

# Run unit tests
pytest tests/test_fishnet.py -v --cov=nusy_orchestrator/santiago_builder/fishnet
```

**Success Criteria:**
- CLI completes successfully
- 84 files generated
- All files validate with behave
- Unit test coverage ≥95%
- Tests pass in CI

---

### Scenario 3: Navigator 10-Step Orchestration (Issue #7 / PR #11)

**Test**: Verify Navigator can run complete expedition

```bash
# Test Navigator CLI
python nusy_orchestrator/santiago_builder/navigator.py \
  --domain product-management \
  --source santiago-pm/ \
  --output /tmp/navigator-test-output/ \
  --ontology knowledge/ontologies/pm-domain-ontology.ttl
```

**Validation Checklist:**
- [ ] Navigator.py runs without errors
- [ ] All 10 steps execute in sequence
- [ ] StepResult, ValidationCycle, ExpeditionLog data classes work
- [ ] Validation loop runs 3-5 times
- [ ] Quality gates enforced (≥95% BDD, ≥95% coverage, ≥90% KG)
- [ ] Integration with Catchfish works (Step 3)
- [ ] Integration with Fishnet works (Step 7)
- [ ] Expedition log written to ships-logs/
- [ ] CLI arguments work
- [ ] Unit tests pass: `pytest tests/test_navigator.py`

**Test Command:**
```bash
# Run Navigator (may take 30-60 minutes)
python nusy_orchestrator/santiago_builder/navigator.py \
  --domain product-management \
  --source santiago-pm/ \
  --output /tmp/navigator-test/ \
  --ontology knowledge/ontologies/pm-domain-ontology.ttl

# Check expedition log
cat santiago-pm/ships-logs/product-management-*.md

# Run unit tests
pytest tests/test_navigator.py -v --cov=nusy_orchestrator/santiago_builder/navigator
```

**Success Criteria:**
- Complete expedition runs successfully
- Validation loop executes 3-5 times
- Quality gates met (≥95%/≥95%/≥90%)
- Expedition log contains all metrics
- Unit test coverage ≥95%
- Tests pass in CI

---

### Scenario 4: End-to-End Integration

**Test**: Full pipeline from raw docs to validated BDD tests

**Validation Checklist:**
- [ ] Navigator starts with santiago-pm/ source documents
- [ ] Catchfish extracts 28 behaviors (already done, verify integration)
- [ ] Fishnet generates 84 .feature files
- [ ] behave runs tests against Santiago PM MCP (if available)
- [ ] Quality metrics collected (pass rate, coverage, completeness)
- [ ] Expedition log documents full workflow
- [ ] All components integrate without manual intervention

**Test Command:**
```bash
# Full end-to-end test (if MCP available)
# 1. Run Navigator expedition
python nusy_orchestrator/santiago_builder/navigator.py \
  --domain product-management \
  --source santiago-pm/ \
  --output knowledge/catches/santiago-pm-behaviors/ \
  --ontology knowledge/ontologies/pm-domain-ontology.ttl

# 2. Verify BDD files generated
ls -l knowledge/catches/santiago-pm-behaviors/bdd-tests/*.feature | wc -l
# Should output: 84 (or 28 if 3 scenarios per file)

# 3. Run BDD tests (if MCP server running)
# behave knowledge/catches/santiago-pm-behaviors/bdd-tests/

# 4. Check expedition log
cat santiago-pm/ships-logs/product-management-*.md
```

**Success Criteria:**
- Complete automation works
- No manual intervention required
- All quality gates met
- Expedition log complete

---

## Quality Metrics Validation

### BDD Pass Rate (Target: ≥95%)

**Measurement:**
```bash
# Run behave and capture results
behave knowledge/catches/santiago-pm-behaviors/bdd-tests/ \
  --format json --outfile behave-results.json

# Parse results
python -c "
import json
with open('behave-results.json') as f:
    data = json.load(f)
    total = len([s for f in data for s in f['elements']])
    passed = len([s for f in data for s in f['elements'] if s['status'] == 'passed'])
    pass_rate = passed / total if total > 0 else 0
    print(f'BDD Pass Rate: {pass_rate:.2%} ({passed}/{total})')
"
```

**Acceptance:**
- Pass rate ≥ 95%
- If < 95%, identify failing scenarios and reasons

### Test Coverage (Target: ≥95%)

**Measurement:**
```bash
# Run pytest with coverage
pytest tests/ --cov=nusy_orchestrator/santiago_builder --cov-report=term-missing

# Generate HTML report
pytest tests/ --cov=nusy_orchestrator/santiago_builder --cov-report=html
open htmlcov/index.html
```

**Acceptance:**
- Line coverage ≥ 95%
- Branch coverage ≥ 90%
- No critical paths uncovered

### KG Completeness (Target: ≥90%)

**Measurement:**
```bash
# Check ontology coverage
# Count behaviors in ontology vs behaviors in extractions
python -c "
import re
ontology_file = 'knowledge/ontologies/pm-domain-ontology.ttl'
behaviors_file = 'knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md'

# Count PMBehavior classes in ontology
with open(ontology_file) as f:
    ontology_behaviors = len(re.findall(r'nusy:\w+ a nusy:PMBehavior', f.read()))

# Count behaviors in extraction
with open(behaviors_file) as f:
    extracted_behaviors = len(re.findall(r'^### Behavior \d+\.\d+:', f.read(), re.MULTILINE))

completeness = extracted_behaviors / ontology_behaviors if ontology_behaviors > 0 else 0
print(f'KG Completeness: {completeness:.2%} ({extracted_behaviors}/{ontology_behaviors})')
"
```

**Acceptance:**
- Completeness ≥ 90%
- All extracted behaviors have ontology mappings

---

## Performance Benchmarks

### Fishnet Generation Time

**Target**: < 5 minutes for 84 files

**Measurement:**
```bash
time python nusy_orchestrator/santiago_builder/fishnet.py \
  --behaviors knowledge/catches/santiago-pm-behaviors/pm-behaviors-extracted.md \
  --ontology knowledge/ontologies/pm-domain-ontology.ttl \
  --output /tmp/fishnet-perf-test/ \
  --strategies bottom_up
```

**Acceptance:**
- Total time < 5 minutes
- Average time per file < 3.5 seconds

### Navigator Execution Time

**Target**: 30-60 minutes for complete expedition (3-5 cycles)

**Measurement:**
```bash
time python nusy_orchestrator/santiago_builder/navigator.py \
  --domain product-management \
  --source santiago-pm/ \
  --output /tmp/navigator-perf-test/ \
  --ontology knowledge/ontologies/pm-domain-ontology.ttl
```

**Acceptance:**
- Total time < 60 minutes
- Per-cycle time < 15 minutes

---

## Regression Testing

### Existing Functionality

**Ensure no breaking changes:**
- [ ] Catchfish still works (extract behaviors)
- [ ] Existing scripts still run
- [ ] Imports don't conflict
- [ ] No circular dependencies introduced

**Test Command:**
```bash
# Run existing tests
pytest tests/ -v

# Check for import issues
python -c "
from nusy_orchestrator.santiago_builder import fishnet
from nusy_orchestrator.santiago_builder import navigator
print('✓ Imports successful')
"
```

---

## Issue Resolution

### If Tests Fail

**Debugging Process:**

1. **Identify Failure Type**
   - Syntax error (Gherkin validation)
   - Logic error (test assertions)
   - Integration error (component mismatch)
   - Performance error (timeout/slowness)

2. **Collect Diagnostics**
   ```bash
   # Run with verbose output
   behave bdd-tests/ --no-capture --verbose
   pytest tests/ -vv --tb=long
   
   # Check logs
   tail -f navigator.log
   ```

3. **Fix and Retest**
   - Make minimal fix
   - Run specific failing test
   - Verify no new failures introduced
   - Update test plan with lessons learned

4. **Document in Expedition Log**
   - What failed and why
   - How it was fixed
   - Time spent debugging
   - Prevention for future

---

## Phase 3 Completion Criteria

**Ready to Complete Mini Expedition:**

- [ ] All 4 PRs reviewed and merged
- [ ] All integration tests pass
- [ ] Quality metrics meet thresholds (≥95%/≥95%/≥90%)
- [ ] Performance benchmarks acceptable
- [ ] No regressions in existing functionality
- [ ] Documentation updated
- [ ] Expedition log finalized with metrics
- [ ] Lessons learned captured

**Expedition Tracking:**
- Total time recorded (Phase 1 + Phase 2 + Phase 3)
- Coordination overhead calculated
- Rework percentage measured
- Context preservation verified
- Comparison to serial baseline (4.4h)

---

## Next Steps After Integration

1. **Update Expedition Tracker**
   - Record final Phase 3 metrics
   - Calculate total time and overhead
   - Document effectiveness vs baseline
   - Mark expedition COMPLETE

2. **Run Task 12: Navigator Expedition**
   - Use completed Navigator on santiago-pm
   - Validate full 10-step process
   - Generate new expedition log
   - Compare to bootstrap results

3. **Build Task 16 Demo**
   - Santiago-PM-Self-Aware demonstration
   - Use implemented Fishnet + Navigator
   - Show recursive self-improvement
   - Document for stakeholders

4. **Continue Development Plan**
   - Task 15: EARS scaffold
   - Task 17: Scan docs/vision
   - Task 18: Ingest external websites
   - Future phases: NeuroSymbolic integration
