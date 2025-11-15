# Santiago Four-Layer Model: Lessons Learned & Domain Expertise
# Clinical Knowledge Representation Framework

**Date:** November 9, 2025  
**Version:** 0.1.0  
**Focus:** Capturing domain expertise and lessons learned during four-layer model development  

---

## Overview

The **Santiago Four-Layer Model** represents a progressive formalization of clinical knowledge from raw guideline text to executable clinical workflows. This document captures lessons learned, domain insights, and expert knowledge gained during the research and implementation phases.

### Layer Progression
1. **Layer 1 - Raw Text**: Original guideline content and structure
2. **Layer 2 - Structured Knowledge**: Extracted clinical concepts and relationships
3. **Layer 3 - Computable Logic**: Formalized clinical rules and decision algorithms
4. **Layer 4 - Executable Workflows**: DAG-based clinical pathways and reasoning workflows

---

## Layer 1: Raw Text Processing

### Current Implementation Status
- ✅ Basic text extraction from PDFs, HTML, DOCX
- ✅ Section identification and document structure parsing
- ✅ Metadata extraction (title, author, date, source)

### Lessons Learned

#### Technical Lessons
- **PDF Parsing Challenges**: Medical PDFs often use complex layouts, tables, and images
- **Format Variability**: Different publishers use inconsistent formatting and terminology
- **Encoding Issues**: Special characters in medical terminology (μg, ≥, ≤) cause parsing problems

#### Clinical Domain Insights
- **Context Matters**: Same term can mean different things in different clinical contexts
- **Evidence Levels**: Guidelines include varying levels of evidence (Level A, B, C recommendations)
- **Conditional Logic**: Much clinical knowledge is expressed as "if-then" conditional statements

### Domain Expertise Needed

#### Clinical Guideline Patterns
**Question:** What are the common structural patterns in clinical guidelines?
- Executive summaries vs. detailed recommendations
- Evidence tables and quality assessments
- Risk stratification algorithms
- Monitoring and follow-up protocols

**Question:** How do different medical specialties structure their guidelines?
- Cardiology vs. Oncology vs. Primary Care
- Acute vs. chronic condition guidelines
- Preventive vs. therapeutic guidelines

#### Terminology Challenges
**Question:** What are the most problematic medical abbreviations and synonyms?
- BP vs. blood pressure
- MI vs. myocardial infarction vs. mental illness
- Multiple ways to express the same clinical concept

**Question:** How should we handle temporal expressions in guidelines?
- "Every 3 months" vs. "quarterly"
- "Within 24 hours" vs. "immediately"
- "Long-term" vs. specific timeframes

### Implementation Improvements Needed
- [ ] Advanced PDF parsing with table recognition
- [ ] Clinical section classification (diagnosis, treatment, monitoring)
- [ ] Evidence level extraction and tagging
- [ ] Conditional statement identification

---

## Layer 2: Structured Knowledge Extraction

### Current Implementation Status
- ✅ Basic concept extraction using spaCy
- ✅ Named entity recognition setup
- ✅ Relationship identification framework

### Lessons Learned

#### Technical Lessons
- **NLP Model Selection**: General NLP models miss medical terminology
- **Context Window Limitations**: Clinical relationships span multiple sentences
- **Ambiguity Resolution**: Many medical terms have multiple meanings

#### Clinical Domain Insights
- **Concept Hierarchies**: Clinical concepts have complex hierarchical relationships
- **Temporal Dependencies**: Clinical knowledge often involves time-based relationships
- **Conditional Dependencies**: "If patient has X and Y, then do Z"

### Domain Expertise Needed

#### Clinical Concept Types
**Question:** What are the primary categories of clinical concepts we should extract?
- Conditions/Diagnoses
- Medications/Treatments
- Procedures/Interventions
- Measurements/Lab Values
- Symptoms/Signs
- Risk Factors
- Outcomes

**Question:** How should we handle concept normalization?
- SNOMED CT vs. ICD-10 vs. custom terminology
- Drug name normalization (brand vs. generic)
- Unit standardization (mg vs. mcg)

#### Relationship Types
**Question:** What are the key relationship types in clinical guidelines?
- Causes/Leads to
- Treats/Prevents
- Contraindicated with
- Increases risk of
- Requires/Must be done with

**Question:** How do we represent clinical decision trees?
- Branching logic based on patient characteristics
- Risk stratification pathways
- Treatment escalation algorithms

### Implementation Improvements Needed
- [ ] Clinical NLP model integration (BioBERT, ClinicalBERT)
- [ ] SNOMED CT, LOINC, RxNorm terminology mapping
- [ ] Relationship extraction algorithms
- [ ] Concept disambiguation logic

---

## Layer 3: Computable Logic Formalization

### Current Implementation Status
- ✅ FHIR-CPG framework setup
- ✅ Basic rule structure definition
- ✅ Logic expression placeholders

### Lessons Learned

#### Technical Lessons
- **Logic Complexity**: Clinical logic often involves nested conditions and exceptions
- **Temporal Logic**: Many rules involve time-based conditions
- **Uncertainty Handling**: Clinical guidelines often include probabilistic elements

#### Clinical Domain Insights
- **Decision Support Logic**: Guidelines contain complex decision algorithms
- **Risk-Benefit Calculations**: Many recommendations involve weighing risks vs. benefits
- **Patient-Specific Factors**: Age, comorbidities, preferences affect recommendations

### Domain Expertise Needed

#### Clinical Logic Patterns
**Question:** What are common clinical decision logic patterns?
- Threshold-based decisions (BP > 140)
- Risk score calculations (CHA2DS2-VASc)
- Combination therapy logic
- Dose titration algorithms

**Question:** How should we handle clinical uncertainty?
- "Consider" vs. "Recommend" vs. "Must"
- Evidence quality levels
- Patient preference integration

#### FHIR-CPG Mapping
**Question:** How do clinical guidelines map to FHIR-CPG structures?
- PlanDefinition vs. ActivityDefinition
- Library resources for CQL logic
- ValueSet and CodeSystem usage

**Question:** What CQL patterns work best for clinical guidelines?
- Simple conditionals
- Complex nested logic
- Temporal operators
- Aggregation functions

### Implementation Improvements Needed
- [ ] CQL/ELM expression generation
- [ ] FHIR-CPG resource creation
- [ ] Clinical logic validation
- [ ] Decision support integration

---

## Layer 4: Executable Workflow Compilation

### Current Implementation Status
- ✅ DAG structure framework
- ✅ Workflow node definitions
- ✅ Basic traversal logic

### Lessons Learned

#### Technical Lessons
- **Workflow Complexity**: Clinical pathways can be highly complex
- **Parallel Execution**: Many clinical steps can happen simultaneously
- **Exception Handling**: Clinical workflows need robust error handling

#### Clinical Domain Insights
- **Care Coordination**: Multiple providers and specialties involved
- **Monitoring Loops**: Ongoing assessment and adjustment
- **Quality Metrics**: Clinical workflows include measurement and feedback

### Domain Expertise Needed

#### Clinical Workflow Patterns
**Question:** What are typical clinical workflow structures?
- Diagnostic workups
- Treatment initiation and monitoring
- Care transitions
- Follow-up and surveillance

**Question:** How do we represent clinical decision points?
- Provider judgment calls
- Patient preferences
- Resource availability
- Risk tolerance

#### Execution Semantics
**Question:** What are the execution semantics for clinical workflows?
- Sequential vs. parallel steps
- Conditional branching
- Loop structures for monitoring
- Exception and error handling

**Question:** How should we integrate with existing clinical systems?
- EHR integration points
- Order set generation
- Clinical decision support triggers
- Documentation requirements

### Implementation Improvements Needed
- [ ] Advanced workflow engine
- [ ] Clinical execution semantics
- [ ] Integration with EHR systems
- [ ] Workflow validation and simulation

---

## Cross-Layer Lessons

### Integration Challenges
- **Data Flow**: Ensuring information flows correctly between layers
- **Error Propagation**: How errors in one layer affect downstream processing
- **Validation**: Ensuring clinical accuracy at each layer

### Quality Assurance
- **Clinical Validation**: Domain expert review at each layer
- **Consistency Checks**: Ensuring logical consistency across layers
- **Performance Metrics**: Measuring accuracy and completeness

### Scalability Considerations
- **Processing Time**: Balancing accuracy with performance
- **Memory Usage**: Large knowledge graphs require efficient storage
- **Update Mechanisms**: How to update knowledge without full reprocessing

---

## Research Questions & Hypotheses

### Technical Hypotheses
1. **NLP Accuracy**: Clinical-specific models will achieve >95% concept extraction accuracy
2. **Logic Formalization**: 80% of clinical guidelines can be formalized as computable logic
3. **Workflow Execution**: 70% of clinical pathways can be automated

### Clinical Hypotheses
1. **Decision Support**: Four-layer models will improve clinical decision accuracy by 30%
2. **Guideline Adherence**: Automated workflows will increase guideline adherence by 25%
3. **Efficiency Gains**: Clinical workflows will reduce time-to-treatment by 40%

---

## Future Research Directions

### Short Term (3-6 months)
- Clinical NLP model evaluation and selection
- FHIR-CPG implementation patterns
- Graph database schema optimization

### Medium Term (6-12 months)
- Multi-institutional validation studies
- Integration with existing CDS systems
- Performance benchmarking against human experts

### Long Term (1-2 years)
- Machine learning for knowledge graph completion
- Real-time clinical decision support
- Global healthcare system integration

---

## Domain Expert Input Template

### For Each Layer, Please Provide:

1. **Clinical Accuracy Assessment**
   - How accurate is the current extraction/representation?
   - What common errors are occurring?
   - What improvements would increase clinical utility?

2. **Missing Clinical Concepts**
   - What important clinical concepts are being missed?
   - What relationships are not being captured?
   - What clinical context is being lost?

3. **Use Case Validation**
   - Does this representation support real clinical workflows?
   - What clinical scenarios work well vs. poorly?
   - What additional capabilities are needed?

4. **Safety Considerations**
   - Are there safety risks with the current approach?
   - What validation is needed before clinical use?
   - What guardrails should be implemented?

---

## References & Resources

### Clinical Guidelines
- [AHA/ACC Hypertension Guidelines](https://www.ahajournals.org/doi/10.1161/HYP.0000000000000065)
- [NCCN Clinical Practice Guidelines](https://www.nccn.org/guidelines)
- [WHO Essential Medicines](https://www.who.int/publications/i/item/9789240014460)

### Technical Standards
- [FHIR Clinical Reasoning](https://hl7.org/fhir/clinicalreasoning-module.html)
- [CDS Hooks](https://cds-hooks.hl7.org/)
- [CQL Language](https://cql.hl7.org/)

### Research Papers
- [Computable Clinical Practice Guidelines](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5977718/)
- [Knowledge Graphs in Healthcare](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7391517/)

---

*This document will be updated regularly as we gain more experience with the four-layer model and incorporate clinical domain expertise. Please add your insights in the sections above.*