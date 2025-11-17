# Feature: Multi-Strategy BDD Test Generation in Fishnet

**Status:** planned  
**Epic:** Santiago Builder Factory  
**Component:** Fishnet (BDD + MCP Manifest Generator)  
**Priority:** High  
**Created:** 2025-01-16

## Hypothesis

By supporting 4 distinct BDD generation strategies (top-down, bottom-up, external, logic-focused) plus experiment-driven unknown resolution, Fishnet can create comprehensive test suites that validate both domain knowledge coverage AND computational capabilities, while treating unknowns as scientific hypotheses requiring experimentation.

## Context

Current Fishnet implementation (demo_fishnet.py) generates BDD scenarios primarily from Catchfish-extracted knowledge (bottom-up approach). This works well for coverage testing but misses:

1. **Domain-first validation**: Testing against independent domain understanding (not just what we extracted)
2. **External validation**: Tough questions from research papers, expert interviews, AI analysis
3. **Computational logic**: Complex calculations, formulas, decision tables, DAGs, workflows, temporal sequences
4. **Unknown handling**: When we can't answer a question → design experiment to find out

These strategies became CLI configurations in prior system. Need to formalize as Fishnet capability.

## User Story

**As a** Santiago architect building domain-specific catches  
**I want** multiple BDD generation strategies with experiment-driven unknown resolution  
**So that** test suites validate both knowledge coverage AND computational capabilities while treating gaps as scientific opportunities

## Acceptance Criteria

### Strategy 1: Top-Down Domain Analysis
- [ ] Fishnet can analyze raw domain documents INDEPENDENT of Catchfish extraction
- [ ] Generates scenarios from domain expert perspective (what SHOULD be in KG)
- [ ] Compares top-down expectations vs. bottom-up extractions to find gaps
- [ ] Example: Clinical domain → "Given lab results from standard panel, calculate eGFR" (even if not in docs)

### Strategy 2: Bottom-Up KG Coverage
- [ ] Fishnet generates scenarios from all 4 Catchfish layers (current behavior)
- [ ] Layer 1 (raw text) → entity extraction scenarios
- [ ] Layer 2 (entities) → relationship mapping scenarios
- [ ] Layer 3 (KG triples) → graph traversal scenarios
- [ ] Layer 4 (metadata) → provenance tracking scenarios
- [ ] Ensures 100% coverage of extracted knowledge

### Strategy 3: External Expert Validation
- [ ] Fishnet searches web/research papers for domain tough questions
- [ ] Queries AI assistants: "What are hardest questions in [domain]?"
- [ ] Reads academic papers to extract validation scenarios
- [ ] Example: PM domain → Jeff Patton's story mapping edge cases, Lean UX validation patterns
- [ ] Example: Clinical domain → NEJM case studies, diagnostic dilemmas

### Strategy 4: Logic & Computation Focus
- [ ] Fishnet identifies computational requirements in domain (Layer 3-4 heavy)
- [ ] Formulas: mathematical expressions requiring calculation
- [ ] Decision tables: conditional logic with multiple branches
- [ ] DAGs: directed acyclic graphs (dependencies, workflows)
- [ ] Temporal sequences: time-based state machines
- [ ] Example: Clinical → unit conversions, dose calculations, lab result formulas
- [ ] Example: PM → velocity calculations, story point trending, cycle time analysis

### Strategy 5: Experiment-Driven Unknown Resolution (NEW)
- [ ] When Fishnet encounters unanswerable question → creates Experiment artifact
- [ ] Experiment types:
  - Human research: UX interviews, surveys, usability tests
  - Data analysis: statistical analysis, A/B tests, cohort studies
  - Literature review: search papers, consult domain experts
- [ ] Experiment has: hypothesis, success criteria, methodology, timeline
- [ ] Integrates with santiago-pm/voyage-trials/ structure
- [ ] Example: "We don't know optimal story point range" → Design experiment to analyze team velocity data

## Fishnet CLI Configuration (Future)

```bash
# Single strategy
fishnet generate --strategy top-down --domain clinical --input raw_docs/

# Multiple strategies combined
fishnet generate --strategy bottom-up,external,logic --domain pm --input catches/santiago-pm/

# With experiment generation for unknowns
fishnet generate --strategy all --resolve-unknowns experiment --domain clinical

# Strategy-specific options
fishnet generate --strategy external \
  --sources "research_papers,web_search,ai_query" \
  --ai-prompt "What are hardest questions in clinical decision support?"

fishnet generate --strategy logic \
  --focus "formulas,decision_tables,workflows" \
  --layer-emphasis "3,4"
```

## Technical Design

### Fishnet Architecture Enhancement

```python
class BDDGenerationStrategy(ABC):
    """Base class for BDD generation strategies."""
    
    @abstractmethod
    def generate_scenarios(self, context: DomainContext) -> List[Scenario]:
        """Generate BDD scenarios using this strategy."""
        pass
    
    @abstractmethod
    def identify_unknowns(self, context: DomainContext) -> List[Unknown]:
        """Identify questions we cannot answer."""
        pass

class TopDownStrategy(BDDGenerationStrategy):
    """Generate scenarios from domain model independent of extraction."""
    
    def generate_scenarios(self, context: DomainContext) -> List[Scenario]:
        # Analyze domain ontology, industry standards, expert knowledge
        # Generate "expected behavior" scenarios
        # Compare against KG to find gaps
        pass

class BottomUpStrategy(BDDGenerationStrategy):
    """Generate scenarios from Catchfish 4-layer extraction (current)."""
    
    def generate_scenarios(self, context: DomainContext) -> List[Scenario]:
        # Layer 1: Text extraction scenarios
        # Layer 2: Entity recognition scenarios
        # Layer 3: Relationship mapping scenarios
        # Layer 4: Provenance tracking scenarios
        pass

class ExternalValidationStrategy(BDDGenerationStrategy):
    """Generate scenarios from external sources (web, papers, AI)."""
    
    def generate_scenarios(self, context: DomainContext) -> List[Scenario]:
        # Search research papers (PubMed, arXiv, etc.)
        # Query domain experts via AI
        # Web search for "tough questions in [domain]"
        # Extract validation cases from academic literature
        pass

class LogicComputationStrategy(BDDGenerationStrategy):
    """Generate scenarios for complex logic and calculations."""
    
    def generate_scenarios(self, context: DomainContext) -> List[Scenario]:
        # Identify formulas in domain docs
        # Extract decision tables
        # Map DAG dependencies
        # Find temporal/sequential patterns
        # Generate computation validation scenarios
        pass

class ExperimentResolutionStrategy(BDDGenerationStrategy):
    """Generate experiments for unknowns."""
    
    def identify_unknowns(self, context: DomainContext) -> List[Unknown]:
        # Cross-reference all strategies to find gaps
        # Questions with no answer in KG
        # Ambiguous or conflicting information
        pass
    
    def generate_experiments(self, unknowns: List[Unknown]) -> List[Experiment]:
        # For each unknown, design experiment
        # Human research: UX interviews, surveys
        # Data analysis: statistical tests, A/B tests
        # Literature review: paper searches
        # Return Experiment artifacts (santiago-pm/voyage-trials/)
        pass

class Fishnet:
    """Enhanced Fishnet with multi-strategy support."""
    
    def __init__(self, strategies: List[BDDGenerationStrategy]):
        self.strategies = strategies
    
    def generate_bdd_suite(self, catch: Catch) -> BDDSuite:
        """Generate comprehensive BDD suite using all strategies."""
        all_scenarios = []
        all_unknowns = []
        
        for strategy in self.strategies:
            scenarios = strategy.generate_scenarios(catch.domain_context)
            unknowns = strategy.identify_unknowns(catch.domain_context)
            
            all_scenarios.extend(scenarios)
            all_unknowns.extend(unknowns)
        
        # Deduplicate and organize
        suite = self._organize_scenarios(all_scenarios)
        
        # Generate experiments for unknowns
        if self.resolve_unknowns == "experiment":
            experiments = self._generate_experiments(all_unknowns)
            suite.experiments = experiments
        
        return suite
```

### Integration with Santiago PM Ontology

```turtle
# Experiment generated by Fishnet for unknowns
:unknown-optimal-story-points a nusy:Unknown ;
    dcterms:title "What is optimal story point range for 2-week sprints?" ;
    nusy:identifiedBy nusy:BDDGenerationStrategy-TopDown ;
    nusy:confidence 0.0 ;  # We have no answer
    nusy:relatedDomain "velocity-tracking" ;
    nusy:resolvedBy :experiment-story-point-analysis .

:experiment-story-point-analysis a nusy:Experiment ;
    dcterms:title "Analyze story point distributions across teams" ;
    nusy:hypothesis "Teams with 20-40 story points per sprint have highest consistency" ;
    nusy:methodology "Retrospective cohort analysis of 6 months velocity data" ;
    nusy:successCriteria "Identify story point range with <15% variance" ;
    nusy:phase nusy:Phase-Design ;
    prov:wasAttributedTo :ux-researcher ;
    nusy:hasStatus nusy:StatusValue-Open .
```

## Examples by Domain

### Clinical Domain

**Top-Down**: "Given standard metabolic panel, system calculates eGFR using CKD-EPI formula"  
**Bottom-Up**: "Given extracted lab result entities, system maps to LOINC codes"  
**External**: "Reproduce diagnostic accuracy from NEJM case study XYZ"  
**Logic**: "Calculate pediatric dosing using Clark's rule with weight in kg or lbs"  
**Unknown → Experiment**: "Optimal alert threshold for hyperkalemia?" → Design retrospective chart review

### PM Domain (Santiago-PM)

**Top-Down**: "Given feature spec, system validates acceptance criteria completeness"  
**Bottom-Up**: "Given extracted note relationships, system builds semantic graph"  
**External**: "Handle edge cases from Jeff Patton's Story Mapping book Chapter 7"  
**Logic**: "Calculate team velocity trend using exponential moving average"  
**Unknown → Experiment**: "Best relationship strength threshold for note clustering?" → A/B test different values

### Legal Domain

**Top-Down**: "Given contract, system identifies non-standard clauses"  
**Bottom-Up**: "Given extracted legal entities, system builds jurisdiction graph"  
**External**: "Validate against precedent cases from Westlaw database"  
**Logic**: "Calculate statute of limitations based on jurisdiction + offense type + filing date"  
**Unknown → Experiment**: "Most predictive features for case outcome?" → ML model analysis

### Financial Domain

**Top-Down**: "Given portfolio, system calculates risk-adjusted returns"  
**Bottom-Up**: "Given extracted transaction entities, system detects patterns"  
**External**: "Reproduce SEC fraud detection scenarios from academic papers"  
**Logic**: "Calculate Black-Scholes option pricing with volatility surface"  
**Unknown → Experiment**: "Optimal rebalancing frequency for tax efficiency?" → Historical simulation study

## Benefits

1. **Comprehensive Coverage**: 4 strategies ensure no gaps in testing
2. **Domain Validation**: Top-down validates against expert knowledge (not just what we extracted)
3. **Computational Rigor**: Logic strategy ensures formulas/calculations work correctly
4. **External Benchmarking**: Compare against published research and industry standards
5. **Scientific Method**: Unknowns become experiments (hypothesis-driven investigation)
6. **Adaptability**: Different domains need different strategy emphasis

## Implementation Phases

### Phase 1: Current State (Completed)
- ✅ Bottom-up strategy implemented in demo_fishnet.py
- ✅ Generates scenarios from Catchfish 4-layer extraction

### Phase 2: Strategy Framework (Next)
- [ ] Define BDDGenerationStrategy abstract base class
- [ ] Refactor existing code as BottomUpStrategy
- [ ] Add strategy selection to Fishnet constructor
- [ ] Support multiple strategies in single run

### Phase 3: Top-Down Implementation
- [ ] Domain ontology analyzer
- [ ] Expected behavior generator
- [ ] Gap detection (expected vs. extracted)

### Phase 4: External Validation
- [ ] Research paper search integration (PubMed, arXiv, Google Scholar)
- [ ] AI query system ("tough questions in domain")
- [ ] Web scraping for domain-specific challenges
- [ ] Expert interview template generator

### Phase 5: Logic & Computation
- [ ] Formula extraction from domain docs
- [ ] Decision table parser
- [ ] DAG dependency analyzer
- [ ] Temporal sequence detector
- [ ] Computation scenario template generator

### Phase 6: Experiment Resolution
- [ ] Unknown detection across all strategies
- [ ] Experiment artifact generator (santiago-pm/voyage-trials/ format)
- [ ] Hypothesis formulation system
- [ ] Success criteria recommendation
- [ ] Integration with UX research workflow

### Phase 7: CLI Configuration
- [ ] Add --strategy flag to fishnet CLI
- [ ] Strategy-specific options (--sources, --focus, --layer-emphasis)
- [ ] --resolve-unknowns experiment flag
- [ ] Configuration file support (fishnet.yaml)

## Success Metrics

- [ ] All 4 strategies implemented and tested
- [ ] Experiment generation working for unknowns
- [ ] Santiago-pm ingestion uses multi-strategy approach
- [ ] Clinical demo shows formula validation (Logic strategy)
- [ ] PM demo shows external validation (Jeff Patton scenarios)
- [ ] At least 1 real experiment generated and executed

## Related Features

- `santiago-pm/voyage-trials/` - Experiment tracking structure (already exists)
- `nusy:Experiment` ontology class (defined in pm-domain-ontology.ttl)
- Catchfish 4-layer extraction (provides bottom-up input)
- Navigator validation loops (incorporates BDD feedback)

## Notes

This enhancement transforms Fishnet from a single-strategy generator (bottom-up coverage) into a comprehensive validation framework that:
1. Tests against independent domain knowledge (top-down)
2. Validates extracted knowledge (bottom-up) 
3. Benchmarks against external standards (external)
4. Ensures computational correctness (logic)
5. Treats unknowns scientifically (experiments)

The experiment-driven resolution is particularly powerful - instead of ignoring gaps or making assumptions, Santiago explicitly acknowledges what it doesn't know and designs studies to find out. This mirrors real PM practice where hypotheses drive learning.

## Prior System Reference

This feature existed as CLI flags in previous Santiago implementation:
- `--strategy [top-down|bottom-up|external|logic]`
- `--resolve-unknowns experiment`
- Configuration stored in `fishnet.yaml`

Reimplementing with lessons learned and integration with new ontology + santiago-pm structure.
