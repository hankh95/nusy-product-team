# NuSy Prototype Setup and Installation Guide

## Overview
This guide provides step-by-step instructions for setting up the Neurosymbolic Clinical Reasoner (NuSy) prototype environment. The prototype implements a hybrid symbolic-neural approach for clinical knowledge graph evaluation.

## Prerequisites
- **Python**: 3.7 or higher
- **pip**: Latest version recommended
- **Git**: For cloning repositories
- **Virtual Environment**: Recommended for isolation

## Quick Start Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd clinical-intelligence-starter-v10-simplified
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv nusy-env

# Activate virtual environment
# On macOS/Linux:
source nusy-env/bin/activate
# On Windows:
# nusy-env\Scripts\activate
```

### 3. Install Dependencies
```bash
# Install core NuSy requirements
pip install -r research/requirements-nusy.txt

# Verify installation
python -c "import rdflib; print('RDFLib version:', rdflib.__version__)"
```

## Installation Options

### Minimal Installation (Core Only)
For basic functionality without optional extensions:
```bash
pip install rdflib>=6.0.0
```

### Full Installation (All Features)
For complete prototype with all optional components:
```bash
pip install -r research/requirements-nusy.txt
```

### Development Installation
For contributors and developers:
```bash
pip install -r research/requirements-nusy.txt
pip install -e .  # Install in development mode
```

## Package Details

### Core Packages
- **rdflib**: RDF graph processing and JSON-LD parsing
- **typing**: Type hints support (Python 3.7+)
- **pathlib**: Modern path handling

### Optional Extensions
- **SPARQLWrapper**: Advanced SPARQL query capabilities
- **networkx**: Graph algorithms for complex reasoning
- **scikit-learn**: Machine learning utilities
- **transformers**: Neural language models (BERT, BioBERT)
- **torch**: PyTorch for neural computations

### Development Tools
- **pytest**: Testing framework
- **black**: Code formatting
- **mypy**: Type checking
- **flake8**: Code linting

## Testing Installation

### Basic Functionality Test
```python
# Create test script
cat > test_nusy_install.py << 'EOF'
#!/usr/bin/env python3
"""
Test script to verify NuSy prototype installation
"""

import sys
import rdflib

def test_imports():
    """Test core imports"""
    try:
        import rdflib
        print(f"✓ RDFLib {rdflib.__version__} imported successfully")

        # Test optional imports
        optional_imports = [
            ('SPARQLWrapper', 'SPARQL querying'),
            ('networkx', 'Graph algorithms'),
            ('sklearn', 'Machine learning'),
            ('transformers', 'Neural models'),
            ('torch', 'PyTorch'),
        ]

        for module, description in optional_imports:
            try:
                __import__(module)
                print(f"✓ {module} available for {description}")
            except ImportError:
                print(f"⚠ {module} not available for {description}")

        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic RDFLib functionality"""
    try:
        # Create a simple graph
        g = rdflib.Graph()
        print("✓ RDFLib graph creation successful")

        # Test JSON-LD parsing capability
        test_data = {
            "@context": {"@vocab": "http://example.org/"},
            "@id": "test",
            "label": "Test Resource"
        }

        g.parse(data=str(test_data).replace("'", '"'), format='json-ld')
        print("✓ JSON-LD parsing functional")

        return True
    except Exception as e:
        print(f"✗ Functionality test failed: {e}")
        return False

if __name__ == "__main__":
    print("NuSy Prototype Installation Test")
    print("=" * 40)

    imports_ok = test_imports()
    functionality_ok = test_basic_functionality()

    print("\n" + "=" * 40)
    if imports_ok and functionality_ok:
        print("✓ All tests passed! NuSy prototype ready to use.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Check installation.")
        sys.exit(1)
EOF

# Run test
python test_nusy_install.py
```

### Run Prototype Test
```python
# Test the actual prototype
python -c "
from neurosymbolic_prototype import NeurosymbolicClinicalReasoner, load_ci_tagged_graph
print('✓ NuSy prototype imports successful')
reasoner = NeurosymbolicClinicalReasoner()
print('✓ NeurosymbolicClinicalReasoner initialized')
"
```

## Configuration

### Environment Variables
```bash
# Optional: Set environment variables for configuration
export NUSY_CACHE_DIR=/path/to/cache
export NUSY_LOG_LEVEL=INFO
export NUSY_MAX_GRAPH_SIZE=100000
```

### Configuration File
Create `nusy_config.yaml`:
```yaml
# NuSy Prototype Configuration
reasoner:
  max_keywords: 10
  similarity_threshold: 0.8
  enable_caching: true

graph:
  max_triples: 100000
  supported_formats: ['json-ld', 'turtle', 'rdf-xml']

logging:
  level: INFO
  format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
```

## Usage Examples

### Basic Usage
```python
from neurosymbolic_prototype import NeurosymbolicClinicalReasoner, load_ci_tagged_graph

# Initialize reasoner
reasoner = NeurosymbolicClinicalReasoner()

# Load knowledge graph
graph = load_ci_tagged_graph('path/to/knowledge_graph.jsonld')

# Query
question = "What are the symptoms of ischemic stroke?"
result = reasoner.query_graph(question, graph)

print(f"Found {result['triples']} relevant triples")
print(f"Entities: {result['entities']}")
```

### Advanced Usage with Neural Components
```python
# If transformers package is installed
from transformers import AutoTokenizer, AutoModel
import torch

# Load BioBERT for clinical entity recognition
tokenizer = AutoTokenizer.from_pretrained("dmis-lab/biobert-base-cased-v1.1")
model = AutoModel.from_pretrained("dmis-lab/biobert-base-cased-v1.1")

# Use with NuSy reasoner for enhanced question understanding
# (Integration code would go here)
```

## Troubleshooting

### Common Issues

#### Import Errors
```bash
# If rdflib import fails
pip install --upgrade rdflib

# If typing import fails (Python < 3.7)
# Upgrade to Python 3.7+
python --version
```

#### Memory Issues
```bash
# For large knowledge graphs, increase memory limits
export PYTHONPATH=/path/to/nusy:$PYTHONPATH
python -c "import resource; resource.setrlimit(resource.RLIMIT_AS, (4*1024*1024*1024, -1))"
```

#### GPU Acceleration
```bash
# Install PyTorch with CUDA support
pip uninstall torch
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify GPU availability
python -c "import torch; print('CUDA available:', torch.cuda.is_available())"
```

## Development Setup

### Code Formatting
```bash
# Format code
black neurosymbolic_prototype.py

# Type checking
mypy neurosymbolic_prototype.py

# Linting
flake8 neurosymbolic_prototype.py
```

### Running Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=neurosymbolic_prototype tests/

# Run specific test
pytest tests/test_neurosymbolic_prototype.py::test_keyword_extraction
```

## Performance Optimization

### For Large Graphs
- Use graph indexing for faster queries
- Implement caching for repeated queries
- Consider graph partitioning for very large datasets

### Memory Management
- Stream processing for large JSON-LD files
- Garbage collection tuning
- Use memory-mapped files for read-only graphs

## Support and Documentation

### Documentation
- Technical summary: `research/neurosymbolic-clinical-reasoner-technical-summary.md`
- API documentation: Inline docstrings in source code
- Examples: See usage examples above

### Getting Help
- Check existing issues in the repository
- Review the technical summary for implementation details
- Test with provided examples before custom modifications

---

*This setup guide ensures reproducible installation of the NuSy prototype across different environments.*