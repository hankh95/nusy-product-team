#!/bin/bash
# Download DGX Deployment Scripts
# Run this on your DGX Spark to get all deployment files

echo "📥 Downloading DGX Mistral-7B Deployment Scripts..."
echo "=================================================="

# Create deployment directory
DEPLOY_DIR="$HOME/dgx-deployment"
mkdir -p "$DEPLOY_DIR"
cd "$DEPLOY_DIR"

echo "📂 Created deployment directory: $DEPLOY_DIR"

# Base URL for raw files
BASE_URL="https://raw.githubusercontent.com/hankh95/nusy-product-team/main/expeditions/dgx-deployment-scripts"

# Download files
echo "📥 Downloading deployment script..."
curl -s -o deploy_mistral_dgx.sh "$BASE_URL/deploy_mistral_dgx.sh"

echo "📥 Downloading benchmark script..."
curl -s -o benchmark_mistral.py "$BASE_URL/benchmark_mistral.py"

echo "📥 Downloading Santiago agent test..."
curl -s -o test_santiago_agents.py "$BASE_URL/test_santiago_agents.py"

echo "📥 Downloading documentation..."
curl -s -o README.md "$BASE_URL/README.md"

# Make scripts executable
chmod +x deploy_mistral_dgx.sh
chmod +x benchmark_mistral.py
chmod +x test_santiago_agents.py

echo ""
echo "✅ Download complete!"
echo ""
echo "📋 Files downloaded:"
echo "  - deploy_mistral_dgx.sh (main deployment script)"
echo "  - benchmark_mistral.py (performance testing)"
echo "  - test_santiago_agents.py (agent integration testing)"
echo "  - README.md (documentation)"
echo ""
echo "🚀 Ready to deploy! Run:"
echo "  cd $DEPLOY_DIR"
echo "  ./deploy_mistral_dgx.sh"
echo ""
echo "💡 Don't forget to set your Hugging Face token:"
echo "  export HF_TOKEN='your-token-here'"</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/dgx-deployment-scripts/download_dgx_scripts.sh