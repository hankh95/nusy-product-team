# NuSy Prototype - Research Package

This directory contains all the files needed for another AI to understand, install, and build the Neurosymbolic Clinical Reasoner (NuSy) prototype.

## Files Overview

### 📋 Requirements & Dependencies
- **`requirements-nusy.txt`**: Complete package list with versions and installation instructions
- **`nusy-setup-guide.md`**: Step-by-step installation and setup guide
- **`verify_nusy_install.py`**: Automated verification script to test installation

### 📚 Documentation
- **`neurosymbolic-clinical-reasoner-technical-summary.md`**: Comprehensive technical documentation
- **`clinical-intelligence-pipeline-architecture.md`**: Full pipeline architecture design

### 🔧 Source Code
- **`../neurosymbolic_prototype.py`**: Main prototype implementation
- **`../ai-knowledge-review/docs/`**: Evaluation reports and analysis

## Quick Start for Another AI

### 1. Install Dependencies
```bash
# Install all required packages
pip install -r research/requirements-nusy.txt
```

### 2. Verify Installation
```bash
# Run automated verification
python research/verify_nusy_install.py
```

### 3. Review Documentation
```bash
# Read the technical summary
cat research/neurosymbolic-clinical-reasoner-technical-summary.md

# Check the setup guide
cat research/nusy-setup-guide.md
```

### 4. Run Basic Example
```python
from neurosymbolic_prototype import NeurosymbolicClinicalReasoner, load_ci_tagged_graph

# Initialize reasoner
reasoner = NeurosymbolicClinicalReasoner()

# Load a knowledge graph (you'll need a JSON-LD file)
# graph = load_ci_tagged_graph('path/to/knowledge_graph.jsonld')

# Query example
question = "What are the symptoms of ischemic stroke?"
# result = reasoner.query_graph(question, graph)
# print(result)
```

## Package Categories

### Core Dependencies (Required)
- `rdflib>=6.0.0`: RDF graph processing
- `typing>=3.7.4`: Type hints
- `pathlib>=1.0.1`: Path handling

### Optional Extensions (Recommended)
- `SPARQLWrapper`: Advanced querying
- `networkx`: Graph algorithms
- `scikit-learn`: Machine learning
- `transformers`: Neural language models
- `torch`: PyTorch for neural networks

### Development Tools
- `pytest`: Testing
- `black`: Code formatting
- `mypy`: Type checking
- `flake8`: Linting

## Architecture Summary

The NuSy prototype implements a **hybrid symbolic-neural approach** for clinical knowledge evaluation:

1. **Symbolic Layer**: RDF graph reasoning with SPARQL queries
2. **Neural Layer**: Keyword-based NLP with clinical term recognition
3. **Integration**: Combined evidence assessment for clinical questions

### Key Features
- **Question Types**: Diagnostic, treatment, risk assessment, management
- **Graph Support**: JSON-LD, RDF/XML, Turtle formats
- **Output**: Structured evidence with entity/relationship extraction
- **Performance**: O(n) complexity, 70-80% accuracy for clinical questions

### Extension Points
- SPARQL query integration
- Neural language models (BERT, BioBERT)
- Rule-based clinical reasoning
- Uncertainty modeling
- Multi-hop inference

## Integration with Clinical Pipeline

The prototype integrates with:
- **BDD-FishNet**: QA validation and scenario generation
- **CatchFish**: Alternative knowledge source comparison
- **Navigator**: Orchestration and evaluation cycles

## Research Context

This prototype was evaluated on ischemic stroke content achieving:
- **94.9% Coverage**: On 99 BDD scenarios
- **100% CDS Coverage**: Across clinical decision support scenarios
- **5.1% Gap**: Due to pipeline translation failures (not reasoning limitations)

The evaluation demonstrated that the neurosymbolic approach is highly effective for clinical reasoning, with clear pathways for enhancement through symbolic rule engines and neural components.

## Next Steps for Extension

1. **Immediate**: Add SPARQL query support to replace keyword matching
2. **Short-term**: Integrate BioBERT for clinical entity recognition
3. **Medium-term**: Add clinical reasoning rules and uncertainty modeling
4. **Long-term**: Implement multi-hop inference and temporal reasoning

## Contact & Support

For questions about the prototype:
- Review the technical summary for implementation details
- Check the evaluation reports in `ai-knowledge-review/docs/`
- Run the verification script to test your setup

---

*This package provides everything needed to understand, install, and extend the NuSy prototype.*