# Feature: Multi-Strategy Domain Knowledge Capture in Catchfish

**Status:** planned  
**Epic:** Santiago Builder Factory  
**Component:** Catchfish (4-Layer Knowledge Extraction)  
**Priority:** High  
**Created:** 2025-01-16  
**Related:** fishnet-bdd-generation-strategies.feature.md (BDD strategies inform extraction strategies)

## Hypothesis

By aligning Catchfish extraction strategies with Fishnet BDD validation strategies, we create a bi-directional feedback loop where:
1. **Extraction strategies determine WHAT knowledge to capture**
2. **BDD strategies validate we captured it CORRECTLY**
3. **BDD failures inform extraction improvements** (close the loop)

This ensures comprehensive domain coverage while maintaining quality gates.

## Context

Current Catchfish (nusy_orchestrator/santiago_builder/catchfish.py) implements **one extraction path**:
1. Layer 1: Raw text extraction (30-60m baseline)
2. Layer 2: Entity/relationship extraction (NLP patterns)
3. Layer 3: Structured markdown + YAML
4. Layer 4: KG triples with provenance

But domains have **multiple knowledge types** requiring different extraction approaches:

### Knowledge Type Taxonomy

```
Domain Knowledge Types:
├── Explicit Knowledge (written, documented)
│   ├── Structured Documents (PDFs, markdown, specs)
│   ├── Unstructured Text (notes, emails, chats)
│   └── Data Sources (APIs, databases, spreadsheets)
├── Implicit Knowledge (patterns, relationships)
│   ├── Computational Logic (formulas, algorithms)
│   ├── Process Flows (workflows, DAGs, state machines)
│   └── Decision Trees (conditionals, lookup tables)
├── External Knowledge (outside our sources)
│   ├── Research Literature (papers, books, articles)
│   ├── Industry Standards (ISO, NIST, W3C)
│   └── Expert Interviews (recorded, transcribed)
└── Meta Knowledge (knowledge about knowledge)
    ├── Provenance (who created what, when, why)
    ├── Quality Metrics (confidence, completeness, consistency)
    └── Usage Patterns (what gets queried, how often)
```

**Key Insight:** Different BDD strategies (top-down, bottom-up, external, logic) require different Catchfish extraction strategies.

## BDD ↔ Catchfish Strategy Mapping

### Strategy 1: Document-First Extraction (→ Bottom-Up BDD)

**What:** Extract everything explicitly written in source documents  
**How:** Current Catchfish 4-layer approach  
**Output:** Entities, relationships, attributes from text  
**BDD Validation:** Bottom-up scenarios test KG coverage of extracted knowledge

**Example (PM Domain):**
- Source: `santiago-pm/cargo-manifests/feature-template.md`
- Extract: Feature entity with hypothesis, acceptanceCriteria, status properties
- BDD Test: "Given feature entity X, then it has hypothesis property"

**Strengths:** Complete coverage of documented knowledge  
**Weaknesses:** Misses implicit patterns, external context, computational logic

---

### Strategy 2: Schema-Driven Extraction (→ Top-Down BDD)

**What:** Extract knowledge based on domain ontology expectations (not just what's written)  
**How:** Use ontology as extraction template, find instances of classes/properties  
**Output:** Entities conforming to ontology schema, gaps identified  
**BDD Validation:** Top-down scenarios test domain completeness (not just extraction coverage)

**Example (PM Domain):**
- Ontology: `nusy:Feature` has properties (hypothesis, acceptanceCriteria, belongsToEpic, hasIssue)
- Extraction: Search for Feature instances, ensure ALL properties populated (or mark null)
- Gap Detection: "Found 10 Features, but only 3 have belongsToEpic" → incomplete extraction or domain
- BDD Test: "Given PM domain, then every Feature belongs to an Epic"

**Strengths:** Validates domain completeness, identifies gaps  
**Weaknesses:** May impose structure where none exists naturally

---

### Strategy 3: Web/Research Extraction (→ External BDD)

**What:** Extract knowledge from external sources (web, papers, APIs) for benchmarking  
**How:** Web scraping, API calls, PDF parsing of research papers  
**Output:** External knowledge for comparison/validation  
**BDD Validation:** External scenarios test against published standards

**Example (Clinical Domain):**
- Source: PubMed search "eGFR calculation methods"
- Extract: CKD-EPI formula, MDRD formula, recommended thresholds
- Compare: Internal clinical protocols vs. published guidelines
- BDD Test: "Given lab results, eGFR calculation matches NEJM 2009 paper"

**Example (PM Domain):**
- Source: jpattonassociates.com articles on story mapping
- Extract: Story mapping process, principles, edge cases
- Compare: Santiago's story mapping vs. Jeff Patton's canonical approach
- BDD Test: "Given user stories, mapping follows Patton's theme-activity-task structure"

**Strengths:** Benchmarks against external truth, finds best practices  
**Weaknesses:** External sources may conflict, require disambiguation

---

### Strategy 4: Computational Extraction (→ Logic BDD)

**What:** Extract formulas, algorithms, decision logic, workflows from code/docs  
**How:** AST parsing, formula recognition, workflow diagram parsing  
**Output:** Executable logic, decision tables, DAGs, state machines  
**BDD Validation:** Logic scenarios test calculations work correctly

**Example (Clinical Domain):**
- Source: Clinical decision support rules (if-then-else chains)
- Extract: Decision table (age ranges, lab values → diagnosis codes)
- Parse: `if (eGFR < 60 && age > 65) then stage_3_ckd`
- BDD Test: "Given eGFR=55 and age=70, then diagnosis is stage_3_ckd"

**Example (PM Domain):**
- Source: `santiago-pm/tackle/status/status-system.md`
- Extract: State machine (Open → InProgress → Blocked | Closed)
- Parse: Valid transitions, closure reasons (Completed, Cancelled, etc.)
- BDD Test: "Given status=Open, when transition to Cancelled, then stateReason required"

**Example (Financial Domain):**
- Source: Black-Scholes formula in trading docs
- Extract: Formula components (S, K, T, r, σ)
- Parse: `C = S*N(d1) - K*e^(-rT)*N(d2)`
- BDD Test: "Given stock=$100, strike=$105, T=1yr, r=5%, σ=20%, then call option = $8.92"

**Strengths:** Validates computational correctness, not just text extraction  
**Weaknesses:** Requires domain-specific parsers (clinical rules ≠ financial formulas)

---

### Strategy 5: Interactive Extraction (→ Experiment BDD)

**What:** Extract knowledge through conversation, interviews, experiments  
**How:** Prompt engineering, guided questions, A/B testing, data analysis  
**Output:** New knowledge NOT in existing sources (discoveries)  
**BDD Validation:** Experiment scenarios test hypotheses

**Example (UX Research):**
- Question: "What's optimal story point range for 2-week sprints?"
- Extraction Method: Query team velocity data, run retrospective analysis
- Output: Experiment result (25-35 story points shows lowest variance)
- BDD Test: "Given team velocity data, then optimal range is 25-35 points"

**Example (Clinical Discovery):**
- Question: "Which lab panel predicts readmission risk?"
- Extraction Method: Retrospective chart review, logistic regression
- Output: Predictive model (eGFR + albumin + hemoglobin → 78% accuracy)
- BDD Test: "Given lab values, readmission prediction accuracy ≥75%"

**Strengths:** Discovers new knowledge, fills gaps scientifically  
**Weaknesses:** Time-intensive, requires human/data access

---

## Catchfish Architecture Enhancement

### Current (Single Strategy)

```python
class Catchfish:
    async def extract_from_source(source_path, target_layer):
        # Fixed 4-layer pipeline
        # Layer 1: Raw text
        # Layer 2: NLP entity extraction
        # Layer 3: Markdown + YAML
        # Layer 4: KG triples
```

### Proposed (Multi-Strategy)

```python
class ExtractionStrategy(ABC):
    """Base class for knowledge extraction strategies."""
    
    @abstractmethod
    async def extract(self, source: Source, ontology: Ontology) -> ExtractionResult:
        """Extract knowledge using this strategy."""
        pass
    
    @abstractmethod
    def required_source_types(self) -> List[SourceType]:
        """What source types this strategy handles."""
        pass
    
    @abstractmethod
    def validates_with_bdd_strategy(self) -> BDDGenerationStrategy:
        """Which BDD strategy validates this extraction."""
        pass

class DocumentFirstStrategy(ExtractionStrategy):
    """Extract everything written in documents (current approach)."""
    
    async def extract(self, source: Source, ontology: Ontology) -> ExtractionResult:
        # Layer 1-4 pipeline as currently implemented
        # NLP extraction, entity recognition, relationship mapping
        pass
    
    def required_source_types(self) -> List[SourceType]:
        return [SourceType.MARKDOWN, SourceType.PDF, SourceType.TXT]
    
    def validates_with_bdd_strategy(self) -> BDDGenerationStrategy:
        return BottomUpStrategy()  # Tests KG coverage of documents

class SchemaDrivenStrategy(ExtractionStrategy):
    """Extract based on ontology expectations (find instances of classes)."""
    
    async def extract(self, source: Source, ontology: Ontology) -> ExtractionResult:
        # For each class in ontology (nusy:Feature, nusy:Issue, etc.)
        # Search documents for instances
        # Ensure all required properties present
        # Flag gaps (missing properties, incomplete entities)
        # Output includes completeness metrics
        pass
    
    def required_source_types(self) -> List[SourceType]:
        return [SourceType.MARKDOWN, SourceType.JSON, SourceType.YAML]
    
    def validates_with_bdd_strategy(self) -> BDDGenerationStrategy:
        return TopDownStrategy()  # Tests domain completeness

class WebResearchStrategy(ExtractionStrategy):
    """Extract from external sources (web, APIs, papers)."""
    
    async def extract(self, source: Source, ontology: Ontology) -> ExtractionResult:
        # Web scraping (BeautifulSoup, Playwright)
        # API calls (REST, GraphQL)
        # PDF parsing (PyPDF2, pdfplumber for papers)
        # Citation extraction (DOI lookup)
        # Deduplication (compare internal vs external)
        pass
    
    def required_source_types(self) -> List[SourceType]:
        return [SourceType.URL, SourceType.API, SourceType.PDF]
    
    def validates_with_bdd_strategy(self) -> BDDGenerationStrategy:
        return ExternalValidationStrategy()  # Tests against external truth

class ComputationalLogicStrategy(ExtractionStrategy):
    """Extract formulas, algorithms, decision logic, workflows."""
    
    async def extract(self, source: Source, ontology: Ontology) -> ExtractionResult:
        # Formula extraction (regex patterns for math notation)
        # AST parsing (Python/JS code → logic tree)
        # Decision table parsing (if-then rules → table format)
        # Workflow extraction (Mermaid diagrams → DAG)
        # State machine detection (status transitions → FSM)
        pass
    
    def required_source_types(self) -> List[SourceType]:
        return [SourceType.CODE, SourceType.MARKDOWN, SourceType.DIAGRAM]
    
    def validates_with_bdd_strategy(self) -> BDDGenerationStrategy:
        return LogicComputationStrategy()  # Tests calculations/logic

class InteractiveDiscoveryStrategy(ExtractionStrategy):
    """Extract through interviews, experiments, data analysis."""
    
    async def extract(self, source: Source, ontology: Ontology) -> ExtractionResult:
        # Guided interview questions
        # Data analysis queries (SQL, pandas)
        # A/B test result parsing
        # Survey response aggregation
        # Human feedback integration
        # Creates Experiment artifacts when unknowns found
        pass
    
    def required_source_types(self) -> List[SourceType]:
        return [SourceType.DATABASE, SourceType.SURVEY, SourceType.INTERVIEW]
    
    def validates_with_bdd_strategy(self) -> BDDGenerationStrategy:
        return ExperimentResolutionStrategy()  # Tests hypotheses

class Catchfish:
    """Enhanced Catchfish with multi-strategy support."""
    
    def __init__(
        self,
        workspace_path: Path,
        strategies: List[ExtractionStrategy],
        ontology: Ontology,
    ):
        self.workspace_path = workspace_path
        self.strategies = strategies
        self.ontology = ontology
    
    async def extract_domain(
        self,
        sources: List[Source],
        target_completeness: float = 0.95,
    ) -> DomainCatch:
        """
        Extract complete domain knowledge using all strategies.
        
        Workflow:
        1. Run DocumentFirstStrategy (baseline extraction)
        2. Run SchemaDrivenStrategy (check ontology completeness)
        3. Identify gaps (missing properties, low confidence)
        4. Run WebResearchStrategy for gaps (find external sources)
        5. Run ComputationalLogicStrategy for formulas/workflows
        6. Run InteractiveDiscoveryStrategy for remaining unknowns
        7. Validate with corresponding BDD strategies
        8. Repeat until target_completeness achieved
        """
        
        results = {}
        gaps = []
        iteration = 1
        
        while True:
            print(f"\n🔄 Extraction Iteration {iteration}")
            
            # Run all strategies
            for strategy in self.strategies:
                print(f"   Running {strategy.__class__.__name__}...")
                
                # Filter sources for this strategy
                compatible_sources = [
                    s for s in sources 
                    if s.type in strategy.required_source_types()
                ]
                
                if not compatible_sources:
                    print(f"   ⚠️  No compatible sources")
                    continue
                
                # Extract
                result = await strategy.extract(compatible_sources, self.ontology)
                results[strategy.__class__.__name__] = result
                
                # Validate with corresponding BDD strategy
                bdd_strategy = strategy.validates_with_bdd_strategy()
                scenarios = bdd_strategy.generate_scenarios(result)
                validation = await self._run_bdd_validation(scenarios)
                
                print(f"   ✅ {len(result.entities)} entities, {validation.pass_rate:.1%} BDD pass")
                
                # Identify gaps
                new_gaps = self._identify_gaps(result, validation, self.ontology)
                gaps.extend(new_gaps)
            
            # Calculate completeness
            completeness = self._calculate_completeness(results, self.ontology)
            print(f"\n   📊 Domain Completeness: {completeness:.1%}")
            
            if completeness >= target_completeness:
                print(f"   🎯 Target {target_completeness:.1%} achieved!")
                break
            
            if iteration >= 5:
                print(f"   ⚠️  Max iterations reached, stopping at {completeness:.1%}")
                break
            
            # Prepare for next iteration (focus on gaps)
            sources = self._sources_for_gaps(gaps)
            iteration += 1
        
        return DomainCatch(
            domain_name=self.workspace_path.name,
            results=results,
            completeness=completeness,
            gaps=gaps,
            ontology=self.ontology,
        )
```

## Extraction Strategy Selection Guide

### By Domain Type

**Product Management (santiago-pm):**
- Primary: DocumentFirst (cargo-manifests, ships-logs, etc.)
- Secondary: SchemaDriven (validate against pm-domain-ontology.ttl)
- Tertiary: WebResearch (Jeff Patton, Jeff Gothelf sites)
- Quaternary: ComputationalLogic (status state machine, velocity calculations)

**Clinical/Healthcare:**
- Primary: DocumentFirst (clinical protocols, guidelines)
- Secondary: ComputationalLogic (dose calculations, lab formulas)
- Tertiary: WebResearch (PubMed, NEJM, clinical trials)
- Quaternary: SchemaDriven (validate against FHIR/HL7 standards)

**Financial/Trading:**
- Primary: ComputationalLogic (pricing models, risk formulas)
- Secondary: DocumentFirst (trading policies, regulations)
- Tertiary: WebResearch (SEC filings, market data)
- Quaternary: InteractiveDiscovery (backtest strategies)

**Legal/Compliance:**
- Primary: DocumentFirst (statutes, contracts, case law)
- Secondary: WebResearch (Westlaw, legal databases)
- Tertiary: ComputationalLogic (jurisdiction rules, deadline calculations)
- Quaternary: SchemaDriven (validate against legal ontologies)

### By Knowledge Gap Type

**Gap: Missing Entities** → DocumentFirst + WebResearch  
**Gap: Incomplete Properties** → SchemaDriven  
**Gap: Wrong Calculations** → ComputationalLogic  
**Gap: Unknown Values** → InteractiveDiscovery  
**Gap: Conflicting Info** → WebResearch (find authoritative source)

## CLI Configuration

```bash
# Single strategy (quick extraction)
catchfish extract --strategy document-first --source santiago-pm/

# Multiple strategies (comprehensive)
catchfish extract \
  --strategy document-first,schema-driven,web-research \
  --source santiago-pm/ \
  --ontology knowledge/ontologies/pm-domain-ontology.ttl \
  --target-completeness 0.95

# Strategy-specific options
catchfish extract --strategy web-research \
  --urls "jpattonassociates.com,jeffgothelf.com" \
  --max-depth 3 \
  --extract-citations

catchfish extract --strategy computational-logic \
  --source clinical-protocols/ \
  --formula-patterns "dosing,eGFR,BMI" \
  --extract-decision-tables

# With BDD validation
catchfish extract --strategy all \
  --validate-with-bdd \
  --bdd-pass-threshold 0.95
```

## Success Metrics

- [ ] All 5 extraction strategies implemented
- [ ] Strategy-BDD mapping validated (each extraction strategy has corresponding BDD strategy)
- [ ] Santiago-pm extraction uses DocumentFirst + SchemaDriven
- [ ] Clinical demo uses ComputationalLogic for dose calculations
- [ ] Completeness metric reaches ≥95% with multi-strategy approach
- [ ] Gap identification working (flags incomplete/missing knowledge)

## Implementation Phases

### Phase 1: Strategy Framework (Foundation)
- [ ] Define `ExtractionStrategy` abstract base class
- [ ] Refactor existing code as `DocumentFirstStrategy`
- [ ] Add strategy selection to Catchfish constructor
- [ ] Support multiple strategies in single run

### Phase 2: Schema-Driven (Completeness Validation)
- [ ] Ontology loader (read .ttl, extract classes/properties)
- [ ] Instance finder (search docs for class instances)
- [ ] Property validator (check all required properties present)
- [ ] Gap reporter (missing/incomplete entities)

### Phase 3: Web Research (External Benchmarking)
- [ ] Web scraper (BeautifulSoup, Playwright)
- [ ] API client (REST/GraphQL with rate limiting)
- [ ] PDF parser for research papers
- [ ] Citation extractor (DOI, PubMed ID)
- [ ] Deduplication (internal vs. external comparison)

### Phase 4: Computational Logic (Formula Extraction)
- [ ] Formula parser (LaTeX, AsciiMath, natural language)
- [ ] AST parser for Python/JS code
- [ ] Decision table extractor (if-then rules → table)
- [ ] Workflow parser (Mermaid, DOT diagrams → DAG)
- [ ] State machine detector (status transitions → FSM)

### Phase 5: Interactive Discovery (Unknown Resolution)
- [ ] Guided interview system (generate questions from gaps)
- [ ] Data analysis queries (SQL, pandas for historical data)
- [ ] A/B test result parser
- [ ] Survey integration (Qualtrics, Google Forms)
- [ ] Experiment artifact generator (nusy:Experiment)

### Phase 6: Multi-Strategy Orchestration
- [ ] Iterative extraction with completeness tracking
- [ ] Gap-driven strategy selection (which strategy for this gap?)
- [ ] BDD validation integration (validate after each strategy)
- [ ] Convergence detection (stop when target completeness reached)

### Phase 7: Domain-Specific Optimizations
- [ ] PM domain: optimize DocumentFirst + SchemaDriven
- [ ] Clinical domain: optimize ComputationalLogic + WebResearch
- [ ] Financial domain: optimize ComputationalLogic + InteractiveDiscovery
- [ ] Legal domain: optimize DocumentFirst + WebResearch

## Key Insights

1. **Bi-Directional Mapping**: Every Catchfish extraction strategy maps to a Fishnet BDD strategy
   - DocumentFirst ↔ BottomUp (test extraction coverage)
   - SchemaDriven ↔ TopDown (test domain completeness)
   - WebResearch ↔ External (test against standards)
   - ComputationalLogic ↔ Logic (test calculations)
   - InteractiveDiscovery ↔ Experiment (test hypotheses)

2. **Completeness Metric**: Combine all strategies to measure domain coverage
   - DocumentFirst: % of source docs processed
   - SchemaDriven: % of ontology classes/properties populated
   - WebResearch: % of external benchmarks validated
   - ComputationalLogic: % of formulas/workflows extracted
   - InteractiveDiscovery: % of unknowns resolved

3. **Gap-Driven Iteration**: Gaps from one strategy inform next strategy
   - BDD fails → identify knowledge gap → select strategy to fill gap → re-extract → re-test

4. **Domain-Specific Needs**: Different domains emphasize different strategies
   - PM: Heavy DocumentFirst (well-documented practices)
   - Clinical: Heavy ComputationalLogic (formulas, protocols)
   - Financial: Heavy ComputationalLogic + InteractiveDiscovery (models, backtests)
   - Legal: Heavy DocumentFirst + WebResearch (statutes, case law)

5. **Bootstrap Alignment**: For santiago-pm self-awareness
   - SchemaDriven strategy uses pm-domain-ontology.ttl as template
   - Extracts instances of nusy:Feature, nusy:Issue, nusy:Experiment
   - Validates santiago-pm structure matches its own ontology
   - Meta: Santiago checks if its documentation follows its own rules!

## Related Features

- `fishnet-bdd-generation-strategies.feature.md` - BDD strategies that validate extractions
- `knowledge/ontologies/pm-domain-ontology.ttl` - Schema for SchemaDriven strategy
- `nusy_orchestrator/santiago_builder/catchfish.py` - Current single-strategy implementation

## Notes

This feature transforms Catchfish from a single-path extractor into a comprehensive knowledge capture framework. The key insight: **BDD strategies tell us HOW to validate, extraction strategies tell us WHAT to capture**. By aligning them, we ensure both coverage (capture everything) and correctness (validate it works).

The InteractiveDiscovery strategy is particularly powerful for unknown resolution - instead of leaving gaps, Santiago designs experiments to find answers. This closes the loop: Extract → Validate → Find Gaps → Experiment → Learn → Re-extract.

For santiago-pm (Task 11), we'll start with DocumentFirst (get baseline) then add SchemaDriven (validate against ontology). Later tasks can add WebResearch (Jeff Patton) and ComputationalLogic (status state machine).
