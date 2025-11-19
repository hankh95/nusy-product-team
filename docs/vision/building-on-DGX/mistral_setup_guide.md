# 🚀 NuSy Mistral-7B-Instruct Setup Guide
## Complete DGX Spark Deployment Instructions

**Date:** November 18, 2025
**Target:** NVIDIA DGX Spark with Ubuntu LTS
**Goal:** Deploy Mistral-7B-Instruct for 10 concurrent Santiago agents

---

## 📋 Prerequisites Checklist

### System Requirements
- ✅ **DGX Spark** (4TB NVMe, 128GB RAM) - arrives tomorrow
- ✅ **Ubuntu LTS** (will be installed via provisioning script)
- ✅ **SSH access** configured
- ✅ **Internet connectivity** for model downloads
- ✅ **Hugging Face token** (optional, recommended for faster downloads)

### Pre-Setup Tasks
- [ ] Receive DGX Spark delivery
- [ ] Connect to network and assign IP address
- [ ] Generate SSH keys: `ssh-keygen -t ed25519 -C "nusy-admin@nvidia.com"`
- [ ] Copy SSH public key for passwordless access
- [ ] Verify NVIDIA drivers are available

---

## 🔧 Step-by-Step Setup Process

### Phase 1: Base System Provisioning
```bash
# 1. Connect to DGX via SSH
ssh nusy@<dgx-ip-address>

# 2. Run base provisioning (as root or with sudo)
sudo ./expeditions/exp_041/provisioning/provision_dgx.sh

# This installs:
# - Ubuntu system updates
# - Base tools (git, python, docker, etc.)
# - NVIDIA drivers and container toolkit
# - NuSy directory structure (/opt/nusy)
# - Python virtual environment
# - Firewall and security settings
```

### Phase 2: Model Download and Optimization
```bash
# 1. Switch to nusy user
sudo su - nusy

# 2. Activate Python environment
cd /opt/nusy
source nusy-env/bin/activate

# 3. Set Hugging Face token (optional but recommended)
export HF_TOKEN="your-huggingface-token-here"

# 4. Download and optimize Mistral models
./expeditions/exp_041/provisioning/download_models.sh

# This creates:
# - Base Mistral-7B-Instruct model (~14GB)
# - 8-bit quantized version (~7GB, better performance)
# - 4-bit quantized version (~4GB, maximum memory efficiency)
# - Model registry and validation tests
```

### Phase 3: vLLM Inference Service Setup
```bash
# 1. Configure vLLM service
./expeditions/exp_041/provisioning/configure_vllm.sh

# This sets up:
# - vLLM installation with CUDA support
# - Service configuration optimized for multi-agent use
# - Systemd service for automatic startup
# - Management scripts (start/stop/status/logs)
# - Prometheus metrics endpoint

# 2. Start the service
/opt/nusy/services/scripts/start_vllm.sh
```

### Phase 4: Comprehensive Testing
```bash
# Run full inference test suite
./expeditions/exp_041/provisioning/test_inference.sh

# Tests include:
# - Basic inference functionality
# - Santiago agent role simulation (PM, Architect, Developer, QA)
# - Concurrent requests (5 simultaneous agents)
# - Performance metrics and GPU utilization
# - Error handling validation
```

---

## 🏗️ Architecture Overview

### Model Selection Logic
The setup automatically selects the optimal model based on GPU memory:

| GPU Memory | Model Used | Memory Usage | Use Case |
|------------|------------|--------------|----------|
| 80GB+ | Full precision | ~28GB | Maximum quality |
| 40-80GB | 8-bit quantized | ~14GB | Balanced performance |
| <40GB | 4-bit quantized | ~7GB | Memory constrained |

### Service Configuration
```json
{
  "server": {
    "host": "0.0.0.0",
    "port": 8001
  },
  "inference": {
    "max_num_seqs": 32,
    "gpu_memory_utilization": 0.9,
    "max_context_len_to_capture": 8192
  },
  "multi_agent": {
    "max_concurrent_agents": 10,
    "session_isolation": true
  }
}
```

### API Endpoints
- **Inference:** `http://localhost:8001/v1/chat/completions`
- **Health Check:** `http://localhost:8001/health`
- **Metrics:** `http://localhost:9091/metrics`
- **Models List:** `http://localhost:8001/v1/models`

---

## 🔄 Santiago Agent Integration

### MCP Service Connection
Each Santiago agent connects to vLLM via MCP (Model Context Protocol):

```python
# Example MCP tool for inference
@tool
async def generate_response(context: str, role: str) -> str:
    """Generate AI response for specific Santiago role"""

    system_prompt = f"You are a {role} in the Santiago autonomous factory."

    response = await client.chat.completions.create(
        model="mistral-7b-instruct",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context}
        ],
        max_tokens=1000,
        temperature=0.7
    )

    return response.choices[0].message.content
```

### Multi-Agent Coordination
- **Shared Model Instance:** One Mistral-7B model serves all 10 agents
- **Request Batching:** vLLM automatically batches concurrent requests
- **Session Isolation:** Each agent maintains separate conversation context
- **Load Balancing:** Round-robin distribution across available GPU resources

---

## 📊 Monitoring and Management

### Service Management Scripts
```bash
# Check status
/opt/nusy/services/scripts/status_vllm.sh

# View logs
/opt/nusy/services/scripts/logs_vllm.sh

# Restart service
/opt/nusy/services/scripts/stop_vllm.sh
/opt/nusy/services/scripts/start_vllm.sh
```

### Key Metrics to Monitor
- **GPU Utilization:** Should stay under 90%
- **Memory Usage:** Monitor for memory pressure
- **Request Latency:** Target <6 seconds P95
- **Concurrent Agents:** Maximum 10 simultaneous
- **Error Rate:** Should be <1%

### Log Locations
- **Service Logs:** `journalctl -u nusy-vllm`
- **Application Logs:** `/opt/nusy/logs/vllm_*.log`
- **Test Results:** `/opt/nusy/logs/inference_test_*.log`

---

## 🚨 Troubleshooting Guide

### Common Issues

#### Service Won't Start
```bash
# Check GPU status
nvidia-smi

# Check service status
sudo systemctl status nusy-vllm

# Check logs
sudo journalctl -u nusy-vllm -n 50
```

#### Out of Memory Errors
```bash
# Switch to smaller model
# Edit /opt/nusy/services/vllm_config.json
# Change model path to 4-bit version
# Restart service
```

#### Slow Inference
```bash
# Check GPU utilization
nvidia-smi

# Reduce concurrent agents in config
# Lower max_num_seqs in vllm_config.json
```

#### Network Issues
```bash
# Test local connectivity
curl http://localhost:8001/health

# Check firewall
sudo ufw status

# Test from remote machine
curl http://<dgx-ip>:8001/health
```

---

## 📈 Performance Optimization

### Current Baselines (Expected)
- **Single Request:** 2-4 seconds
- **Concurrent (5 agents):** <6 seconds P95
- **Memory Usage:** 7-28GB depending on model
- **GPU Utilization:** 60-90% during active inference

### Optimization Strategies
1. **Model Quantization:** Use smaller models for memory-constrained scenarios
2. **Request Batching:** vLLM automatically optimizes batch sizes
3. **Prefix Caching:** Enabled for repeated conversation patterns
4. **GPU Memory Management:** Automatic memory optimization

---

## 🔐 Security Considerations

### Network Security
- Service bound to localhost by default
- Firewall configured with minimal open ports
- No authentication required (internal network only)

### Model Security
- Models downloaded from Hugging Face (trusted source)
- No external API keys exposed in logs
- Local inference prevents data leakage

### Access Control
- SSH key-based authentication only
- Sudo access restricted to nusy user
- Service runs as unprivileged user

---

## 📋 Post-Setup Checklist

- [ ] vLLM service starts automatically on boot
- [ ] All inference tests pass
- [ ] Santiago agents can connect via MCP
- [ ] Monitoring dashboards show healthy metrics
- [ ] Backup strategy implemented for models
- [ ] Documentation updated with actual IP addresses

---

## 🎯 Next Steps After Setup

1. **MCP Service Integration:** Configure Santiago agents to use vLLM endpoint
2. **Multi-Agent Testing:** Run full Santiago factory simulation
3. **Performance Tuning:** Optimize based on actual usage patterns
4. **Monitoring Setup:** Configure alerts and dashboards
5. **Backup Strategy:** Implement model and configuration backups

---

*This guide ensures reliable Mistral-7B-Instruct deployment for the Santiago autonomous AI factory on DGX Spark hardware.*</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/docs/vision/building-on-DGX/mistral_setup_guide.md