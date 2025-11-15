#!/bin/bash
# Autonomous Multi-Agent Experiment Setup Script

set -e

echo "🚀 Setting up Autonomous Multi-Agent Experiment Environment"
echo "========================================================="

# Check if we're in the right directory
if [ ! -f "experiment_runner.py" ]; then
    echo "❌ Error: Please run this script from the nusy-product-team directory"
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p logs data reports config

# Check Python environment
echo "🐍 Checking Python environment..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not found"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Found $PYTHON_VERSION"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Validate installation
echo "🔍 Validating installation..."
python3 -c "import sys; print(f'✅ Python executable: {sys.executable}')"

# Test imports
echo "🧪 Testing imports..."
PYTHONPATH=src python3 -c "
try:
    from nusy_pm_core.models.experiment import ExperimentConfig
    from nusy_pm_core.services.experiment_runner import ExperimentRunnerService
    from nusy_pm_core.adapters.agent_adapter import AgentAdapter
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import error: {e}')
    exit(1)
"

# Create environment file template
if [ ! -f ".env" ]; then
    echo "📝 Creating .env template..."
    cat > .env << 'EOF'
# Environment variables for autonomous experiment
# Copy this file and fill in your API keys

# OpenAI API Key (for agent interactions)
OPENAI_API_KEY=your_openai_api_key_here

# Other API keys as needed
# ANTHROPIC_API_KEY=your_anthropic_key_here
# XAI_API_KEY=your_xai_key_here

# Experiment configuration
EXPERIMENT_CONFIG=config/experiment.json
EXPERIMENT_DRY_RUN=false

# Logging configuration
LOG_LEVEL=INFO
LOG_FILE=logs/experiment.log
EOF
    echo "⚠️  Please edit .env file with your API keys before running the experiment"
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your API keys"
echo "2. Review the experiment configuration in config/experiment.json"
echo "3. Run the experiment:"
echo "   source .venv/bin/activate"
echo "   python experiment_runner.py"
echo ""
echo "For dry run (simulation mode):"
echo "   python experiment_runner.py --dry-run"
echo ""
echo "📖 See experiments/usability-test-framework.md for details on the experiment structure"