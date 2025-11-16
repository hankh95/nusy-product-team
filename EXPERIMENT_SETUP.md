# Autonomous Multi-Agent Experiment Setup Guide

This guide provides instructions for setting up and running the autonomous multi-agent experiment that will develop Santiago as a self-improving AI system.

## 🎯 Experiment Overview

The experiment runs a 21-day autonomous development cycle where AI agents collaborate to build PM (Product Management) capabilities. The system operates without human intervention until completion, queuing decisions that require human input.

### Key Features

- **Autonomous Operation**: Runs for 21 days without human feedback
- **Ethical Oversight**: Quartermaster agent ensures moral compliance
- **Usability Testing**: Built-in testing framework validates agent behaviors
- **Decision Queue**: Human input requested only when necessary
- **Self-Improvement**: Agents analyze performance and propose improvements

## 🚀 Quick Start

### Option 1: Local Setup (Recommended)

1. **Clone and setup**:

   ```bash
   git clone <your-repo-url>
   cd nusy-product-team
   ```

2. **Run setup script**:

   ```bash
   ./setup_experiment.sh
   ```

3. **Configure environment**:

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

4. **Start experiment**:

   ```bash
   source .venv/bin/activate
   python experiment_runner.py
   ```

### Option 2: GitHub Codespaces Setup

1. **Create codespace** from your repository
2. **Run setup**:

   ```bash
   ./setup_experiment.sh
   ```

3. **Configure API keys** in codespace secrets or .env file
4. **Start experiment**:

   ```bash
   python experiment_runner.py
   ```

## 📋 Prerequisites

- **Python 3.9+**
- **Git**
- **API Keys** for AI services (OpenAI, Anthropic, etc.)
- **4GB RAM** minimum (8GB recommended)

## 🔧 Detailed Setup Instructions

### 1. Environment Setup

The `setup_experiment.sh` script handles most setup automatically. It will:

- Create virtual environment
- Install dependencies
- Validate installation
- Create configuration templates

### 2. API Configuration

Create a `.env` file with your API keys:

```bash
# Required for agent interactions
OPENAI_API_KEY=sk-your-key-here

# Optional additional providers
ANTHROPIC_API_KEY=your-anthropic-key
XAI_API_KEY=your-xai-key
```

### 3. Experiment Configuration

The experiment is configured via `config/experiment.json`. Key settings:

```json
{
  "experiment_name": "autonomous-multi-agent-swarm",
  "duration_days": 21,
  "success_criteria": {
    "autonomy_level": 0.8,
    "feature_velocity": 0.5
  }
}
```

## 🎮 Running the Experiment

### Start Experiment

```bash
python experiment_runner.py
```

### Dry Run (Testing)

```bash
python experiment_runner.py --dry-run
```

### Custom Configuration

```bash
python experiment_runner.py --config path/to/config.json
```

## 📊 Monitoring Progress

### Logs

- Main log: `logs/experiment_runner.log`
- Agent logs: `logs/agent_*.log`

### Reports

- Daily progress: `reports/daily_progress.json`
- Final assessment: `reports/final_assessment.json`

### Decision Queue

- Pending decisions: `data/decision_queue.json`
- Requires human input when autonomy limits are reached

## 🧪 Usability Test Framework

The experiment includes comprehensive usability testing:

### Test Phases

1. **Bootstrapping** (Days 1-3): Agent initialization
2. **Knowledge Loading** (Days 4-7): PM expertise ingestion
3. **Autonomous Development** (Days 8-14): Feature implementation
4. **Self-Evaluation** (Days 15-21): Performance analysis

### Success Metrics

- **Autonomy Level**: % of time running without human input (>80%)
- **Feature Velocity**: New capabilities per day (>0.5)
- **Quality Maintenance**: Test pass rates (>90%)
- **Learning Rate**: Performance improvements over time

## 🛠️ Troubleshooting

### Common Issues

#### Import Errors (Prototype Runtime Archived)

The former `nusy_pm_core` module was archived (tag `prototype-archive-2025-11-16`). Import checks against it are historical. For current planning-only phase just ensure environment activation works:

```bash
cd /path/to/nusy-product-team
source .venv/bin/activate
python -c "print('env ok')"
```

#### API Key Issues

```bash
# Check .env file exists and contains valid keys
cat .env
# Test API connectivity
python -c "import openai; openai.api_key='your-key'; print('API key valid')"
```

#### Memory Issues

- Increase codespace memory allocation
- Run with `--dry-run` first
- Monitor resource usage in logs

### Getting Help

1. Check experiment logs in `logs/` directory
2. Review decision queue in `data/decision_queue.json`
3. Run diagnostic: `python experiment_runner.py --diagnose`

## 🎯 Expected Outcomes

### Successful Experiment Results

- 3+ new PM features implemented autonomously
- Knowledge graph with 500+ triples
- Self-improvement proposals generated
- Comprehensive performance analysis

### Decision Points

The system will queue decisions for:

- Ethical dilemmas requiring human judgment
- Major architecture changes
- Resource limit exceedances
- Innovation opportunities needing validation

## 🔄 Next Steps After Completion

1. **Review Results**: Analyze final assessment report
2. **Process Decisions**: Address queued human decisions
3. **Iterate**: Use learnings to improve the system
4. **Scale**: Expand to additional domains or agent types

## 📚 Additional Resources

- [Usability Test Framework](experiments/usability-test-framework.md)
- [Autonomous Multi-Agent Experiment](experiments/autonomous-multi-agent-swarm.md)
- [Backlog](backlog/autonomous-multi-agent-backlog.md)

## 🤝 Support

For issues or questions:

1. Check the troubleshooting section above
2. Review experiment logs and reports
3. File issues in the project repository

---

**Experiment Status**: Ready to run
**Estimated Duration**: 21 days autonomous operation
**Human Input Required**: Only for queued decisions
