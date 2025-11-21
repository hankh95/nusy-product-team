# 🚀 DGX Mistral-7B Deployment Package

**Ready-to-deploy scripts for Mistral-7B on DGX Spark**

## 📦 What's Included

- `deploy_mistral_dgx.sh` - Complete automated deployment script
- `benchmark_mistral.py` - Performance benchmarking tool
- `test_santiago_agents.py` - Santiago agent integration testing
- `README.md` - This documentation

## 🚀 Quick Start

### 1. Download to DGX
```bash
# On your DGX Spark system
cd ~
wget https://github.com/hankh95/nusy-product-team/raw/main/expeditions/dgx-deployment-scripts/deploy_mistral_dgx.sh
chmod +x deploy_mistral_dgx.sh
```

### 2. Set Hugging Face Token (Recommended)
```bash
export HF_TOKEN="your-huggingface-token-here"
echo "export HF_TOKEN=$HF_TOKEN" >> ~/.bashrc
```

### 3. Run Deployment
```bash
# This will take 30-60 minutes
./deploy_mistral_dgx.sh
```

### 4. Verify Installation
```bash
# Check service status
~/nusy-dgx/scripts/status.sh

# Test basic API
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer nusy-dgx-2025" \
  -d '{"model": "mistralai/Mistral-7B-Instruct-v0.1", "messages": [{"role": "user", "content": "Hello!"}]}'
```

## 🧪 Testing & Validation

### Performance Benchmark
```bash
cd ~/nusy-dgx
python ~/nusy-dgx/benchmark_mistral.py --concurrency 10
```

### Santiago Agent Testing
```bash
cd ~/nusy-dgx
python ~/nusy-dgx/test_santiago_agents.py
```

### Expected Results
- **Single Request:** <3 seconds latency
- **10 Concurrent Agents:** <6 seconds P95 latency
- **GPU Memory:** <4GB usage
- **All Santiago Roles:** Successful responses

## 📊 Service Management

```bash
# Start service
~/nusy-dgx/scripts/start.sh

# Stop service
~/nusy-dgx/scripts/stop.sh

# Check status
~/nusy-dgx/scripts/status.sh

# View logs
~/nusy-dgx/scripts/logs.sh
```

## 🔧 Configuration

### Files Location
- **Scripts:** `~/nusy-dgx/scripts/`
- **Config:** `~/nusy-dgx/config/vllm_config.yaml`
- **Environment:** `~/nusy-dgx/.env`
- **Models:** `~/models/mistral-7b/`

### Key Settings
```yaml
# vLLM Configuration
gpu-memory-utilization: 0.8    # Use 80% of GPU memory
max-num-seqs: 32              # Max concurrent sequences
max-model-len: 4096           # Context window
dtype: "half"                 # FP16 for efficiency
```

## 🚨 Troubleshooting

### Service Won't Start
```bash
# Check GPU status
nvidia-smi

# Check logs
sudo journalctl -u nusy-vllm -n 50

# Manual test
cd ~/nusy-dgx
source ../nusy-dgx-env/bin/activate
python -m vllm.entrypoints.openai.api_server --model ~/models/mistral-7b --host 0.0.0.0 --port 8001
```

### Out of Memory
```bash
# Reduce memory usage in config
# gpu-memory-utilization: 0.7
# max-num-seqs: 16

# Restart service
~/nusy-dgx/scripts/stop.sh
~/nusy-dgx/scripts/start.sh
```

### Model Download Issues
```bash
# Check token
echo $HF_TOKEN

# Manual download
cd ~/models
source ~/nusy-dgx-env/bin/activate
python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='mistralai/Mistral-7B-Instruct-v0.1',
    local_dir='mistral-7b',
    token='$HF_TOKEN'
)
"
```

## 📈 Performance Tuning

### For Higher Throughput
```yaml
# Increase in vllm_config.yaml
max-num-seqs: 64
max-num-batched-tokens: 8192
gpu-memory-utilization: 0.9
```

### For Lower Latency
```yaml
# Decrease in vllm_config.yaml
max-num-seqs: 16
max-model-len: 2048
```

## 🔒 Security Notes

- Service runs as system user `nusy`
- API key required for all requests
- Localhost-only binding by default
- No external network access needed

## 📋 Next Steps

Once deployed and tested:

1. **Phase 3:** Add Vicuna-13B and Qwen-3-4B models
2. **Integration:** Connect real Santiago agents
3. **Optimization:** Fine-tune for production workloads
4. **Monitoring:** Set up long-term performance tracking

---

**Ready to deploy Mistral-7B on DGX! 🚀**</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/dgx-deployment-scripts/README.md