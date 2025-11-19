#!/usr/bin/env bash
# vLLM Service Configuration Script
# Sets up vLLM for Mistral-7B-Instruct with multi-agent batching

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly NUSY_ROOT="/opt/nusy"
readonly MODEL_DIR="$NUSY_ROOT/models"
readonly SERVICE_DIR="$NUSY_ROOT/services"
readonly LOG_DIR="$NUSY_ROOT/logs"
readonly CONFIG_FILE="$SERVICE_DIR/vllm_config.json"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_DIR/vllm_setup_$(date +%Y%m%d).log"
}

error() {
    log "ERROR: $*" >&2
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking vLLM setup prerequisites..."

    # Check if running as nusy user
    if [[ $USER != "nusy" ]]; then
        error "This script should be run as the nusy user"
    fi

    # Check Python environment
    if ! source "$NUSY_ROOT/nusy-env/bin/activate" 2>/dev/null; then
        error "NuSy Python environment not found"
    fi

    # Check if models exist
    if [[ ! -d "$MODEL_DIR/mistral-7b-instruct" ]]; then
        error "Mistral model not found. Run download_models.sh first"
    fi

    # Check GPU availability
    if ! nvidia-smi &>/dev/null; then
        error "NVIDIA GPU not detected"
    fi

    log "Prerequisites check passed"
}

# Install vLLM and dependencies
install_vllm() {
    log "Installing vLLM and dependencies..."

    source "$NUSY_ROOT/nusy-env/bin/activate"

    # Install vLLM with CUDA support
    pip install vllm

    # Additional inference optimization packages
    pip install \
        torch \
        torchvision \
        torchaudio --index-url https://download.pytorch.org/whl/cu118 \
        transformers \
        accelerate \
        ray[serve]  # For distributed serving if needed

    log "vLLM installed successfully"
}

# Create vLLM configuration
create_config() {
    log "Creating vLLM configuration..."

    mkdir -p "$SERVICE_DIR"

    # Determine optimal model based on available memory
    local total_memory
    total_memory=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)

    local model_path
    if [[ $total_memory -ge 80000 ]]; then  # 80GB+ GPU memory
        model_path="$MODEL_DIR/mistral-7b-instruct"
        log "Using full precision model (GPU memory: ${total_memory}MB)"
    elif [[ $total_memory -ge 40000 ]]; then  # 40GB+ GPU memory
        model_path="$MODEL_DIR/optimized/mistral-7b-instruct-8bit"
        log "Using 8-bit quantized model (GPU memory: ${total_memory}MB)"
    else  # Less than 40GB
        model_path="$MODEL_DIR/optimized/mistral-7b-instruct-4bit"
        log "Using 4-bit quantized model (GPU memory: ${total_memory}MB)"
    fi

    # Create configuration file
    cat > "$CONFIG_FILE" << EOF
{
  "model": {
    "path": "$model_path",
    "name": "mistral-7b-instruct",
    "type": "chat",
    "max_model_len": 4096,
    "dtype": "auto"
  },
  "server": {
    "host": "0.0.0.0",
    "port": 8001,
    "ssl": false,
    "api_key": null
  },
  "inference": {
    "tensor_parallel_size": 1,
    "pipeline_parallel_size": 1,
    "max_num_batched_tokens": 4096,
    "max_num_seqs": 32,
    "max_paddings": 256,
    "block_size": 16,
    "swap_space": 4,
    "gpu_memory_utilization": 0.9,
    "max_context_len_to_capture": 8192
  },
  "multi_agent": {
    "max_concurrent_agents": 10,
    "session_isolation": true,
    "rate_limiting": {
      "requests_per_minute": 60,
      "burst_limit": 10
    },
    "load_balancing": {
      "strategy": "round_robin",
      "health_check_interval": 30
    }
  },
  "monitoring": {
    "prometheus_port": 9091,
    "metrics_interval": 10,
    "log_level": "INFO"
  },
  "optimization": {
    "enable_prefix_caching": true,
    "enable_chunked_prefill": true,
    "cpu_offload_gb": 0,
    "enable_triton_attention": true
  }
}
EOF

    log "vLLM configuration created at $CONFIG_FILE"
}

# Create systemd service
create_service() {
    log "Creating systemd service for vLLM..."

    local service_file="/etc/systemd/system/nusy-vllm.service"

    sudo tee "$service_file" > /dev/null << EOF
[Unit]
Description=NuSy vLLM Inference Service
After=network.target nvidia-persistenced.service
Requires=nvidia-persistenced.service

[Service]
Type=simple
User=nusy
Group=nusy
Environment=PATH=$NUSY_ROOT/nusy-env/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
Environment=PYTHONPATH=$NUSY_ROOT/nusy-product-team/src
WorkingDirectory=$NUSY_ROOT
ExecStart=$NUSY_ROOT/nusy-env/bin/python -m vllm.entrypoints.openai.api_server \
    --model $MODEL_DIR/mistral-7b-instruct \
    --host 0.0.0.0 \
    --port 8001 \
    --tensor-parallel-size 1 \
    --max-model-len 4096 \
    --gpu-memory-utilization 0.9 \
    --max-num-batched-tokens 4096 \
    --max-num-seqs 32
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=nusy-vllm

[Install]
WantedBy=multi-user.target
EOF

    sudo systemctl daemon-reload
    sudo systemctl enable nusy-vllm

    log "vLLM systemd service created and enabled"
}

# Create management scripts
create_management_scripts() {
    log "Creating vLLM management scripts..."

    mkdir -p "$SERVICE_DIR/scripts"

    # Start script
    cat > "$SERVICE_DIR/scripts/start_vllm.sh" << 'EOF'
#!/bin/bash
echo "Starting NuSy vLLM service..."
sudo systemctl start nusy-vllm
sleep 5
if sudo systemctl is-active --quiet nusy-vllm; then
    echo "✅ vLLM service started successfully"
    echo "📊 Service status:"
    sudo systemctl status nusy-vllm --no-pager -l
else
    echo "❌ Failed to start vLLM service"
    echo "📋 Check logs:"
    sudo journalctl -u nusy-vllm -n 20 --no-pager
    exit 1
fi
EOF

    # Stop script
    cat > "$SERVICE_DIR/scripts/stop_vllm.sh" << 'EOF'
#!/bin/bash
echo "Stopping NuSy vLLM service..."
sudo systemctl stop nusy-vllm
echo "✅ vLLM service stopped"
EOF

    # Status script
    cat > "$SERVICE_DIR/scripts/status_vllm.sh" << 'EOF'
#!/bin/bash
echo "🔍 NuSy vLLM Service Status"
echo "=========================="
sudo systemctl status nusy-vllm --no-pager -l
echo ""
echo "🌐 API Endpoint: http://localhost:8001"
echo "📊 Metrics: http://localhost:9091"
echo ""
echo "🔧 GPU Status:"
nvidia-smi --query-gpu=name,memory.used,memory.total,temperature.gpu --format=csv,noheader,nounits
EOF

    # Logs script
    cat > "$SERVICE_DIR/scripts/logs_vllm.sh" << 'EOF'
#!/bin/bash
echo "📋 NuSy vLLM Service Logs (last 50 lines)"
echo "========================================"
sudo journalctl -u nusy-vllm -n 50 --no-pager -f
EOF

    chmod +x "$SERVICE_DIR/scripts"/*.sh

    log "Management scripts created in $SERVICE_DIR/scripts/"
}

# Test basic functionality
test_service() {
    log "Testing vLLM service..."

    # Start service
    "$SERVICE_DIR/scripts/start_vllm.sh"

    # Wait for service to be ready
    local max_attempts=30
    local attempt=1
    while [[ $attempt -le $max_attempts ]]; do
        if curl -s http://localhost:8001/health > /dev/null 2>&1; then
            log "vLLM service is responding"
            break
        fi
        log "Waiting for vLLM service... (attempt $attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done

    if [[ $attempt -gt $max_attempts ]]; then
        error "vLLM service failed to start properly"
    fi

    # Test inference
    log "Testing inference..."
    local test_response
    test_response=$(curl -s -X POST http://localhost:8001/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{
          "model": "mistral-7b-instruct",
          "messages": [{"role": "user", "content": "Hello, test message"}],
          "max_tokens": 50,
          "temperature": 0.1
        }')

    if echo "$test_response" | jq -e '.choices[0].message.content' > /dev/null 2>&1; then
        log "✅ Inference test passed"
    else
        error "❌ Inference test failed. Response: $test_response"
    fi

    log "vLLM service test completed successfully"
}

# Create setup report
create_report() {
    log "Creating vLLM setup report..."

    local report_file="$SERVICE_DIR/vllm_setup_report_$(date +%Y%m%d_%H%M%S).txt"

    cat > "$report_file" << EOF
vLLM Setup Report
Generated: $(date)
Configuration: $CONFIG_FILE

Service Status:
$(sudo systemctl status nusy-vllm --no-pager -l 2>/dev/null || echo "Service not running")

GPU Information:
$(nvidia-smi --query-gpu=name,memory.used,memory.total --format=csv)

Management Scripts:
- Start: $SERVICE_DIR/scripts/start_vllm.sh
- Stop: $SERVICE_DIR/scripts/stop_vllm.sh
- Status: $SERVICE_DIR/scripts/status_vllm.sh
- Logs: $SERVICE_DIR/scripts/logs_vllm.sh

API Endpoints:
- Inference: http://localhost:8001/v1/chat/completions
- Health: http://localhost:8001/health
- Metrics: http://localhost:9091

Next Steps:
1. Test multi-agent integration: ./test_multi_agent.sh
2. Configure MCP services to use vLLM endpoint
3. Set up monitoring and alerting

Log files: $LOG_DIR/vllm_*.log
EOF

    log "Setup report created: $report_file"
}

# Main function
main() {
    log "Starting vLLM configuration for NuSy Mistral-7B-Instruct"
    log "Target: Multi-agent inference service on DGX Spark"

    check_prerequisites
    install_vllm
    create_config
    create_service
    create_management_scripts
    test_service
    create_report

    log "vLLM configuration completed successfully!"
    log "Service will start automatically on boot"
    log "Use '$SERVICE_DIR/scripts/status_vllm.sh' to check status"
}

# Run main function
main "$@"
</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/exp_041/provisioning/configure_vllm.sh