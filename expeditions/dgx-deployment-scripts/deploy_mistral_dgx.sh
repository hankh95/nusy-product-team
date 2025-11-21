#!/bin/bash
# DGX Mistral-7B Deployment Script
# Run this script on your DGX Spark system

set -e

echo "🚀 Starting DGX Mistral-7B Deployment"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$HOME/nusy-dgx"
MODEL_DIR="$HOME/models/mistral-7b"
VENV_DIR="$HOME/nusy-dgx-env"

# Logging
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}" >&2
}

warn() {
    echo -e "${YELLOW}[WARN] $1${NC}"
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    # Check if running on Linux
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        error "This script is designed for Linux systems (DGX Ubuntu)"
        exit 1
    fi

    # Check NVIDIA GPU
    if ! command -v nvidia-smi &> /dev/null; then
        error "nvidia-smi not found. Please ensure NVIDIA drivers are installed."
        exit 1
    fi

    # Check CUDA
    if ! command -v nvcc &> /dev/null; then
        warn "nvcc not found. CUDA toolkit may not be installed."
    fi

    # Check available memory
    TOTAL_MEM=$(free -g | awk 'NR==2{printf "%.0f", $2}')
    if [ "$TOTAL_MEM" -lt 64 ]; then
        warn "System has ${TOTAL_MEM}GB RAM. DGX Spark should have 128GB."
    fi

    log "Prerequisites check complete"
}

# Setup directories
setup_directories() {
    log "Setting up directories..."

    mkdir -p "$WORKSPACE_DIR"
    mkdir -p "$WORKSPACE_DIR/config"
    mkdir -p "$WORKSPACE_DIR/logs"
    mkdir -p "$WORKSPACE_DIR/scripts"
    mkdir -p "$MODEL_DIR"

    log "Directories created"
}

# Install system dependencies
install_system_deps() {
    log "Installing system dependencies..."

    sudo apt update
    sudo apt install -y \
        python3.10 \
        python3.10-venv \
        python3-pip \
        git \
        curl \
        wget \
        htop \
        nvtop \
        tmux

    log "System dependencies installed"
}

# Setup Python environment
setup_python_env() {
    log "Setting up Python virtual environment..."

    python3 -m venv "$VENV_DIR"
    source "$VENV_DIR/bin/activate"

    pip install --upgrade pip wheel setuptools

    # Install PyTorch with CUDA support
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

    log "Python environment ready"
}

# Install vLLM and dependencies
install_vllm() {
    log "Installing vLLM and ML dependencies..."

    source "$VENV_DIR/bin/activate"

    # Install vLLM
    pip install vllm

    # Install additional dependencies
    pip install transformers accelerate huggingface-hub

    # Verify installation
    python -c "import vllm; print(f'vLLM version: {vllm.__version__}')"

    log "vLLM installed successfully"
}

# Download Mistral model
download_model() {
    log "Downloading Mistral-7B-Instruct model..."

    # Check for Hugging Face token
    if [ -z "$HF_TOKEN" ]; then
        warn "HF_TOKEN not set. Model download may fail or be slow."
        warn "Set it with: export HF_TOKEN='your-token-here'"
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    source "$VENV_DIR/bin/activate"

    # Download model
    python -c "
from huggingface_hub import snapshot_download
import os

model_path = '$MODEL_DIR'
token = os.getenv('HF_TOKEN')

print('Downloading Mistral-7B-Instruct...')
snapshot_download(
    repo_id='mistralai/Mistral-7B-Instruct-v0.1',
    local_dir=model_path,
    token=token
)
print('Model downloaded successfully!')
"

    # Verify model files
    if [ ! -f "$MODEL_DIR/config.json" ]; then
        error "Model download failed - config.json not found"
        exit 1
    fi

    log "Mistral-7B model downloaded and verified"
}

# Create configuration files
create_config() {
    log "Creating configuration files..."

    # vLLM configuration
    cat > "$WORKSPACE_DIR/config/vllm_config.yaml" << EOF
# vLLM Configuration for Mistral-7B on DGX
model: "$MODEL_DIR"
tensor-parallel-size: 1
gpu-memory-utilization: 0.8
max-model-len: 4096
max-num-seqs: 32
max-num-batched-tokens: 8192
quantization: null  # Will use 4-bit if available
dtype: "half"
enforce-eager: false
disable-log-stats: false
EOF

    # Environment configuration
    cat > "$WORKSPACE_DIR/.env" << EOF
# NuSy DGX Environment Configuration
HF_TOKEN=$HF_TOKEN
VLLM_HOST=0.0.0.0
VLLM_PORT=8001
VLLM_API_KEY=nusy-dgx-2025
MODEL_PATH=$MODEL_DIR
WORKSPACE_DIR=$WORKSPACE_DIR
EOF

    log "Configuration files created"
}

# Create systemd service
create_service() {
    log "Creating systemd service..."

    # Create service file
    sudo tee /etc/systemd/system/nusy-vllm.service > /dev/null << EOF
[Unit]
Description=NuSy vLLM Service (Mistral-7B)
After=network.target nvidia-persistenced.service
Requires=nvidia-persistenced.service

[Service]
Type=simple
User=$USER
EnvironmentFile=$WORKSPACE_DIR/.env
WorkingDirectory=$WORKSPACE_DIR
ExecStart=$VENV_DIR/bin/python -m vllm.entrypoints.openai.api_server \\
    --model $MODEL_DIR \\
    --host 0.0.0.0 \\
    --port 8001 \\
    --tensor-parallel-size 1 \\
    --gpu-memory-utilization 0.8 \\
    --max-model-len 4096 \\
    --max-num-seqs 32 \\
    --dtype half \\
    --api-key nusy-dgx-2025
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

    # Reload systemd
    sudo systemctl daemon-reload

    log "Systemd service created"
}

# Create utility scripts
create_scripts() {
    log "Creating utility scripts..."

    # Start script
    cat > "$WORKSPACE_DIR/scripts/start.sh" << 'EOF'
#!/bin/bash
echo "🚀 Starting NuSy vLLM Service..."
sudo systemctl start nusy-vllm
sleep 2
sudo systemctl status nusy-vllm --no-pager
EOF

    # Stop script
    cat > "$WORKSPACE_DIR/scripts/stop.sh" << 'EOF'
#!/bin/bash
echo "🛑 Stopping NuSy vLLM Service..."
sudo systemctl stop nusy-vllm
EOF

    # Status script
    cat > "$WORKSPACE_DIR/scripts/status.sh" << 'EOF'
#!/bin/bash
echo "📊 NuSy vLLM Service Status:"
sudo systemctl status nusy-vllm --no-pager

echo -e "\n🔍 GPU Status:"
nvidia-smi --query-gpu=index,name,memory.used,memory.total,utilization.gpu --format=csv,noheader,nounits

echo -e "\n🌐 API Endpoint: http://localhost:8001"
echo "🔑 API Key: nusy-dgx-2025"
EOF

    # Logs script
    cat > "$WORKSPACE_DIR/scripts/logs.sh" << 'EOF'
#!/bin/bash
echo "📋 NuSy vLLM Service Logs:"
sudo journalctl -u nusy-vllm -f
EOF

    # Make scripts executable
    chmod +x "$WORKSPACE_DIR/scripts/"*.sh

    log "Utility scripts created"
}

# Test installation
test_installation() {
    log "Testing installation..."

    source "$VENV_DIR/bin/activate"

    # Test basic import
    python -c "import vllm, transformers, torch; print('✅ All imports successful')"

    # Test model loading (quick test)
    python -c "
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained('$MODEL_DIR')
print(f'✅ Tokenizer loaded: {tokenizer.__class__.__name__}')
print(f'Vocab size: {tokenizer.vocab_size}')
"

    log "Installation tests passed"
}

# Main deployment function
main() {
    echo "🎯 DGX Mistral-7B Deployment Starting..."
    echo "This will take approximately 30-60 minutes"
    echo ""

    check_prerequisites
    setup_directories
    install_system_deps
    setup_python_env
    install_vllm
    download_model
    create_config
    create_service
    create_scripts
    test_installation

    echo ""
    log "🎉 Deployment complete!"
    echo ""
    echo "📋 Next steps:"
    echo "1. Start the service: $WORKSPACE_DIR/scripts/start.sh"
    echo "2. Check status: $WORKSPACE_DIR/scripts/status.sh"
    echo "3. View logs: $WORKSPACE_DIR/scripts/logs.sh"
    echo "4. Test API: curl -X POST http://localhost:8001/v1/chat/completions \\"
    echo "     -H 'Content-Type: application/json' \\"
    echo "     -H 'Authorization: Bearer nusy-dgx-2025' \\"
    echo "     -d '{\"model\": \"mistralai/Mistral-7B-Instruct-v0.1\", \"messages\": [{\"role\": \"user\", \"content\": \"Hello!\"}]}'"
    echo ""
    echo "🔧 Configuration files:"
    echo "   - vLLM config: $WORKSPACE_DIR/config/vllm_config.yaml"
    echo "   - Environment: $WORKSPACE_DIR/.env"
    echo "   - Model path: $MODEL_DIR"
    echo ""
    echo "📊 Monitoring:"
    echo "   - GPU: nvidia-smi"
    echo "   - System: htop"
    echo "   - API: Check /health endpoint"
}

# Run main function
main "$@"</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/dgx-deployment-scripts/deploy_mistral_dgx.sh