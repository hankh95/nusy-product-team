#!/usr/bin/env bash
# Model Download and Optimization Script
# Downloads and optimizes Mistral-7B-Instruct for DGX deployment

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly NUSY_ROOT="/opt/nusy"
readonly MODEL_DIR="$NUSY_ROOT/models"
readonly MODEL_NAME="mistralai/Mistral-7B-Instruct-v0.2"
readonly LOG_FILE="$NUSY_ROOT/logs/model_download_$(date +%Y%m%d_%H%M%S).log"

# Logging
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
    log "ERROR: $*" >&2
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    # Check if running as nusy user
    if [[ $USER != "nusy" ]]; then
        error "This script should be run as the nusy user"
    fi

    # Check Python environment
    if ! source "$NUSY_ROOT/nusy-env/bin/activate" 2>/dev/null; then
        error "NuSy Python environment not found at $NUSY_ROOT/nusy-env"
    fi

    # Check available disk space (need ~50GB for model + optimizations)
    local free_space
    free_space=$(df "$MODEL_DIR" | tail -1 | awk '{print $4}')
    if [[ $free_space -lt 52428800 ]]; then  # 50GB in KB
        error "Insufficient disk space in $MODEL_DIR. Need at least 50GB free"
    fi

    # Check Hugging Face token (optional but recommended)
    if [[ -z "${HF_TOKEN:-}" ]]; then
        log "WARNING: HF_TOKEN not set. Download may be rate-limited"
    fi

    log "Prerequisites check passed"
}

# Install model download dependencies
install_dependencies() {
    log "Installing model download dependencies..."

    source "$NUSY_ROOT/nusy-env/bin/activate"

    pip install \
        transformers \
        accelerate \
        bitsandbytes \
        huggingface_hub \
        torch \
        torchvision \
        torchaudio --index-url https://download.pytorch.org/whl/cu118

    log "Dependencies installed"
}

# Download base model
download_model() {
    log "Downloading Mistral-7B-Instruct model..."

    source "$NUSY_ROOT/nusy-env/bin/activate"

    local model_path="$MODEL_DIR/mistral-7b-instruct"

    mkdir -p "$model_path"

    # Set Hugging Face token if available
    export HF_HUB_DISABLE_PROGRESS_BARS=0
    if [[ -n "${HF_TOKEN:-}" ]]; then
        export HF_TOKEN="$HF_TOKEN"
        log "Using Hugging Face token for authentication"
    fi

    # Download model
    python -c "
from huggingface_hub import snapshot_download
import os

model_name = '$MODEL_NAME'
target_dir = '$model_path'

print(f'Downloading {model_name} to {target_dir}')
snapshot_download(
    repo_id=model_name,
    local_dir=target_dir,
    local_dir_use_symlinks=False,
    token=os.environ.get('HF_TOKEN')
)
print('Model download completed')
"

    log "Model downloaded to $model_path"
}

# Create optimized model variants
create_optimized_variants() {
    log "Creating optimized model variants..."

    source "$NUSY_ROOT/nusy-env/bin/activate"

    local base_model="$MODEL_DIR/mistral-7b-instruct"
    local optimized_dir="$MODEL_DIR/optimized"

    mkdir -p "$optimized_dir"

    # Create 4-bit quantized version
    log "Creating 4-bit quantized version..."
    python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

model_path = '$base_model'
output_path = '$optimized_dir/mistral-7b-instruct-4bit'

print(f'Loading model from {model_path}')
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map='auto',
    torch_dtype=torch.float16,
    quantization_config=BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type='nf4'
    )
)

tokenizer = AutoTokenizer.from_pretrained(model_path)

print(f'Saving optimized model to {output_path}')
model.save_pretrained(output_path)
tokenizer.save_pretrained(output_path)
print('4-bit model saved')
"

    # Create 8-bit quantized version
    log "Creating 8-bit quantized version..."
    python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

model_path = '$base_model'
output_path = '$optimized_dir/mistral-7b-instruct-8bit'

print(f'Loading model for 8-bit quantization')
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map='auto',
    torch_dtype=torch.float16,
    quantization_config=BitsAndBytesConfig(
        load_in_8bit=True,
        bnb_8bit_compute_dtype=torch.float16
    )
)

tokenizer = AutoTokenizer.from_pretrained(model_path)

print(f'Saving 8-bit model to {output_path}')
model.save_pretrained(output_path)
tokenizer.save_pretrained(output_path)
print('8-bit model saved')
"

    log "Optimized variants created"
}

# Validate model integrity
validate_models() {
    log "Validating model integrity..."

    source "$NUSY_ROOT/nusy-env/bin/activate"

    local base_model="$MODEL_DIR/mistral-7b-instruct"
    local optimized_4bit="$MODEL_DIR/optimized/mistral-7b-instruct-4bit"
    local optimized_8bit="$MODEL_DIR/optimized/mistral-7b-instruct-8bit"

    # Test base model
    log "Testing base model..."
    python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained('$base_model', torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained('$base_model')

# Quick inference test
inputs = tokenizer('Hello, world!', return_tensors='pt')
with torch.no_grad():
    outputs = model.generate(**inputs, max_length=20, do_sample=False)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f'Base model test result: {result}')
print('Base model validation passed')
"

    # Test optimized models
    for model_path in "$optimized_4bit" "$optimized_8bit"; do
        if [[ -d "$model_path" ]]; then
            log "Testing optimized model at $model_path..."
            python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model = AutoModelForCausalLM.from_pretrained('$model_path')
tokenizer = AutoTokenizer.from_pretrained('$model_path')

inputs = tokenizer('Test inference', return_tensors='pt')
with torch.no_grad():
    outputs = model.generate(**inputs, max_length=15, do_sample=False)

result = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f'Optimized model test result: {result}')
print('Optimized model validation passed')
"
        fi
    done

    log "Model validation completed"
}

# Create model registry
create_registry() {
    log "Creating model registry..."

    local registry_file="$MODEL_DIR/model_registry.json"

    cat > "$registry_file" << EOF
{
  "models": {
    "mistral-7b-instruct": {
      "path": "$MODEL_DIR/mistral-7b-instruct",
      "type": "base",
      "quantization": "none",
      "size_gb": 14.5,
      "description": "Base Mistral-7B-Instruct model"
    },
    "mistral-7b-instruct-4bit": {
      "path": "$MODEL_DIR/optimized/mistral-7b-instruct-4bit",
      "type": "optimized",
      "quantization": "4bit",
      "size_gb": 4.0,
      "description": "4-bit quantized Mistral-7B-Instruct for memory efficiency"
    },
    "mistral-7b-instruct-8bit": {
      "path": "$MODEL_DIR/optimized/mistral-7b-instruct-8bit",
      "type": "optimized",
      "quantization": "8bit",
      "size_gb": 7.5,
      "description": "8-bit quantized Mistral-7B-Instruct for balanced performance"
    }
  },
  "metadata": {
    "created": "$(date -Iseconds)",
    "source": "$MODEL_NAME",
    "framework": "transformers",
    "intended_use": "NuSy Santiago agent reasoning"
  }
}
EOF

    log "Model registry created at $registry_file"
}

# Generate download report
create_report() {
    log "Generating download report..."

    local report_file="$MODEL_DIR/download_report_$(date +%Y%m%d_%H%M%S).txt"

    cat > "$report_file" << EOF
Model Download Report
Generated: $(date)
Model: $MODEL_NAME
Download Location: $MODEL_DIR

Disk Usage:
$(du -sh "$MODEL_DIR"/* 2>/dev/null || echo "No models found")

Available Models:
$(ls -la "$MODEL_DIR")

Next Steps:
1. Configure vLLM service: ./configure_vllm.sh
2. Test inference service: ./test_inference.sh
3. Review complete setup guide: docs/vision/building-on-DGX/mistral_setup_guide.md

Log file: $LOG_FILE
Registry: $MODEL_DIR/model_registry.json
EOF

    log "Download report created: $report_file"
}

# Main function
main() {
    log "Starting model download and optimization for DGX"
    log "Target model: $MODEL_NAME"

    check_prerequisites
    install_dependencies
    download_model
    create_optimized_variants
    validate_models
    create_registry
    create_report

    log "Model download and optimization completed successfully!"
    log "Models are ready for vLLM deployment"
}

# Run main function
main "$@"