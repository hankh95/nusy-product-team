# NuSy Components: Current and Future Requirements

**Date:** November 13, 2025
**Context:** Clinical Intelligence Pipeline Enhancement for Automated QA

## Current NuSy Components

### BDD-Fishnet
BDD-Fishnet serves as our core knowledge extraction engine within the clinical intelligence pipeline, processing Best Practice content through multiple sequential stages: L0 processing for initial content structuring, CI-tagging for clinical concept identification and relationship mapping, anchor extraction for identifying key clinical decision points, and finally knowledge graph construction to create structured, machine-readable clinical knowledge representations. This component forms the foundation of our clinical knowledge processing pipeline, transforming raw clinical content into structured knowledge graphs that can be queried and reasoned about by downstream systems.

The engine is particularly effective at handling the complexity of clinical terminology and relationships, using advanced natural language processing techniques to identify clinical entities, their properties, and the relationships between them. BDD-Fishnet's multi-stage approach ensures that clinical knowledge is not only extracted but also validated and structured in a way that maintains clinical accuracy while enabling computational reasoning. This component has proven essential for creating the initial structured representations that form the basis of our clinical decision support systems.

**Framework Link:** [BDD-Fishnet Repository](https://github.com/hhead-bmj/clinical-intelligence-starter-v10-simplified) (Internal implementation)

### Catchfish
Catchfish operates as an alternative processing pipeline that preserves significantly more clinical knowledge during extraction compared to traditional CI-tagging approaches. This component is specifically designed to maintain clinical nuances and relationships that may be filtered out or lost during the standard CI-tagging process, serving as a complementary approach that captures the full richness of clinical content. Catchfish excels at preserving contextual information and subtle clinical distinctions that are critical for accurate clinical decision-making.

The component's strength lies in its ability to handle the complexity and subtlety of clinical language, maintaining relationships and contextual information that might be considered noise by more rigid extraction systems. This makes Catchfish particularly valuable for scenarios where clinical accuracy depends on understanding the full context and nuance of medical information. By preserving more of the original clinical knowledge, Catchfish provides a more comprehensive foundation for downstream clinical reasoning and decision support systems.

**Framework Link:** [Catchfish Implementation](https://github.com/hhead-bmj/clinical-intelligence-starter-v10-simplified) (Internal implementation)

### Navigator
Navigator functions as an advanced reasoning engine that performs mathematical computations and handles complex clinical decision scenarios, extending beyond basic knowledge extraction to provide computational reasoning capabilities for clinical decision support. This component is designed to process the structured knowledge graphs produced by BDD-Fishnet and Catchfish, applying mathematical and logical reasoning to support clinical decision-making processes. Navigator's strength lies in its ability to handle numerical calculations, probability assessments, and complex clinical scenario analysis.

The engine integrates mathematical computation capabilities with clinical knowledge, enabling it to perform tasks such as risk probability calculations, drug dosing computations, and statistical analysis for clinical decisions. Navigator represents a bridge between symbolic clinical knowledge and mathematical reasoning, allowing the system to provide quantitative clinical decision support. This component is essential for transforming qualitative clinical knowledge into actionable quantitative recommendations that can directly support clinical workflows.

**Framework Link:** [Navigator Implementation](https://github.com/hhead-bmj/clinical-intelligence-starter-v10-simplified) (Internal implementation)

## Required Components to Add

### Enhanced Neurosymbolic Framework (PyTorch Geometric + LNN)
To achieve full mathematical reasoning capabilities, we would need to integrate a comprehensive neurosymbolic framework that combines neural network learning with symbolic reasoning. PyTorch Geometric provides the graph neural network foundation for processing complex knowledge structures, while Logical Neural Networks (LNN) enable differentiable logical reasoning. This combination would allow our system to learn from clinical data while maintaining logical consistency and explainability.

The enhanced framework would enable probabilistic reasoning over clinical knowledge graphs, allowing the system to handle uncertainty in clinical decision-making and provide confidence scores for different clinical recommendations. This would be particularly valuable for complex clinical scenarios where multiple factors need to be weighed and uncertainty needs to be quantified.

**Framework Links:**
- [PyTorch Geometric](https://github.com/pyg-team/pytorch_geometric) - Graph neural network library
- [Logical Neural Networks](https://github.com/IBM/LNN) - Differentiable logical reasoning

### Mathematical Computation Engine
A dedicated mathematical computation engine would be required to handle the numerical aspects of clinical decision-making, including pharmacokinetic calculations, risk stratification algorithms, and statistical analysis. This component would need to integrate with clinical knowledge graphs to perform real-time calculations based on patient-specific parameters and clinical context.

The engine would support complex mathematical operations such as Bayesian probability calculations, statistical modeling, and numerical optimization for clinical decision support. This would enable the system to provide quantitative clinical recommendations, calculate optimal drug dosages, and assess clinical risks with mathematical precision.

**Framework Links:**
- [SymPy](https://github.com/sympy/sympy) - Symbolic mathematics library
- [SciPy](https://github.com/scipy/scipy) - Scientific computing library
- [NumPy](https://github.com/numpy/numpy) - Numerical computing foundation

### Temporal Reasoning and Sequence Processing
Clinical decision-making often involves temporal aspects, such as disease progression over time, treatment response monitoring, and longitudinal patient data analysis. A temporal reasoning component would be needed to handle time-series clinical data and reason about clinical events across different time points.

This component would enable the system to understand clinical trajectories, predict disease progression, and provide temporally-aware clinical recommendations. It would integrate with existing knowledge graphs to add temporal dimensions to clinical reasoning, allowing for more sophisticated analysis of clinical scenarios that unfold over time.

**Framework Links:**
- [AllenNLP](https://github.com/allenai/allennlp) - NLP library with temporal reasoning capabilities
- [Kensho Temporal Reasoning](https://github.com/kensho-technologies/temporal-reasoning) - Specialized temporal reasoning framework

### Uncertainty Quantification and Confidence Scoring
Clinical decision-making inherently involves uncertainty, and we would need components to quantify and communicate this uncertainty effectively. An uncertainty quantification framework would assess confidence levels in clinical recommendations and provide probabilistic outputs rather than binary decisions.

This component would be crucial for responsible clinical AI, ensuring that clinicians understand the confidence levels associated with system recommendations. It would integrate probabilistic reasoning with clinical knowledge graphs to provide nuanced, uncertainty-aware clinical decision support.

**Framework Links:**
- [Pyro](https://github.com/pyro-ppl/pyro) - Probabilistic programming language
- [TensorFlow Probability](https://github.com/tensorflow/probability) - Probabilistic modeling toolkit

### Clinical Units Conversion Engine
A specialized units conversion component is essential for clinical decision support, as CDS engines frequently need to handle measurements in different units (e.g., glucose in mg/dL vs mmol/L, temperature in Fahrenheit vs Celsius). While FHIR and CQL standards use UCUM (Unified Code for Units of Measure) extensively, they provide no built-in conversion functions, requiring external libraries for clinical unit conversions.

This component would handle the complex unit relationships found in clinical practice, including laboratory measurements, vital signs, and medication dosing conversions. It would integrate with the mathematical computation engine to ensure consistent unit handling across all clinical calculations and reasoning processes.

**Framework Links:**
- [UCUM Java Library](https://github.com/ucum/ucum-java) - Reference UCUM implementation by Regenstrief Institute
- [ucum.js](https://github.com/lhncbc/ucum-lhc) - JavaScript/Node.js UCUM library for FHIR
- [ucum_unit](https://pypi.org/project/ucum-unit/) - Python UCUM wrapper for clinical conversions

**Clinical Unit Conversion Examples:**
- Glucose: `mg/dL` ↔ `mmol/L` (conversion factor: 0.0555)
- Temperature: `[degF]` ↔ `Cel` (Fahrenheit to Celsius formulas)
- Hemoglobin: `g/dL` ↔ `mmol/L` (multiply by 0.6206)
- Creatinine: `mg/dL` ↔ `μmol/L` (multiply by 88.42)

## Integration Strategy

The addition of these components would require a phased integration approach:

1. **Foundation Phase**: Integrate PyTorch Geometric + LNN for enhanced neurosymbolic reasoning
2. **Computation Phase**: Add mathematical computation engine and clinical units conversion for quantitative clinical support
3. **Temporal Phase**: Implement temporal reasoning for longitudinal clinical analysis
4. **Uncertainty Phase**: Add uncertainty quantification for responsible clinical AI

Each component would build upon the existing BDD-Fishnet, Catchfish, and Navigator foundation, extending the system's capabilities while maintaining clinical accuracy and safety standards.

## Implementation Timeline

- **Phase 1 (Weeks 1-3)**: PyTorch Geometric + LNN integration
- **Phase 2 (Weeks 4-6)**: Mathematical computation engine + clinical units conversion
- **Phase 3 (Weeks 7-9)**: Temporal reasoning capabilities
- **Phase 4 (Weeks 10-12)**: Uncertainty quantification and validation

This roadmap would transform our current clinical intelligence system into a comprehensive neurosymbolic platform capable of advanced mathematical reasoning, clinical unit conversions, and uncertainty-aware clinical decision support.</content>
<parameter name="filePath">/workspaces/clinical-intelligence-starter-v10-simplified/docs/nusy-components-analysis.md