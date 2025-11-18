#!/bin/bash
set -euo pipefail

echo "🚀 Deploying Santiago-Dev Autonomous System..."

# Create necessary directories
mkdir -p workspace/{personal-logs,ships-logs,captains-journals,crew-manifests}
mkdir -p tackle/{personal_logging,qa_integration,qa_guidance,autonomous_task_execution}

# Set up virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --break-system-packages -r requirements.txt

# Start the continuous autonomous service
echo "🤖 Starting continuous autonomous operation..."
python3 continuous_autonomous_service.py start

echo "✅ Santiago-Dev deployment completed!"