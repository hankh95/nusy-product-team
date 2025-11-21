# 🚀 DGX LLM Selection - Phase 2: Mistral-7B Deployment

**Expedition:** EXP-DGX-LLM-SELECTION-PHASE2  
**Date:** November 20, 2025  
**Status:** Starting Mistral-7B Deployment  
**Target:** DGX Spark with Ubuntu LTS

---

## 📋 Deployment Overview

**Goal:** Deploy Mistral-7B-Instruct on DGX Spark for Santiago multi-agent inference

**Architecture:**
- **Model:** Mistral-7B-Instruct (4-bit quantized)
- **Inference Engine:** vLLM with CUDA optimization
- **Memory Target:** <4GB GPU memory usage
- **Concurrent Agents:** Support for 10+ simultaneous Santiago agents

---

## 🔧 Phase 2A: Environment Setup

### 1. System Prerequisites Check
```bash
# SSH into DGX and verify system
ssh nusy@<dgx-ip>

# Check NVIDIA drivers and CUDA
nvidia-smi
nvcc --version

# Verify Ubuntu version and kernel
lsb_release -a
uname -a

# Check available memory
free -h
df -h
```

### 2. Install Core Dependencies
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.10+ and pip
sudo apt install -y python3.10 python3.10-venv python3-pip

# Install NVIDIA CUDA toolkit (if not already installed)
# Note: DGX Spark should come with CUDA pre-installed
```

### 3. Create Python Environment
```bash
# Create virtual environment
python3 -m venv ~/nusy-dgx-env
source ~/nusy-dgx-env/bin/activate

# Upgrade pip and install core packages
pip install --upgrade pip wheel setuptools
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

---

## 📦 Phase 2B: vLLM Installation & Configuration

### 1. Install vLLM with CUDA Support
```bash
# Install vLLM (optimized for inference)
pip install vllm

# Install additional dependencies for Mistral
pip install transformers accelerate

# Verify installation
python -c "import vllm; print('vLLM version:', vllm.__version__)"
```

### 2. Download Mistral-7B Model
```bash
# Create models directory
mkdir -p ~/models/mistral-7b

# Download Mistral-7B-Instruct from Hugging Face
# Note: Requires HF_TOKEN environment variable
export HF_TOKEN="your-huggingface-token-here"

# Download the model
python -c "
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id='mistralai/Mistral-7B-Instruct-v0.1',
    local_dir='~/models/mistral-7b',
    token=os.getenv('HF_TOKEN')
)
"
```

### 3. Test Basic Model Loading
```bash
# Quick test of model loading
python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = '~/models/mistral-7b'
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,
    device_map='auto'
)

print('Model loaded successfully!')
print(f'Model size: {model.num_parameters()} parameters')
"
```

---

## ⚡ Phase 2C: vLLM Service Configuration

### 1. Create vLLM Configuration
```bash
# Create config directory
mkdir -p ~/nusy-dgx/config

# Create vLLM config file
cat > ~/nusy-dgx/config/vllm_config.yaml << 'EOF'
# vLLM Configuration for Mistral-7B on DGX
model: "/home/nusy/models/mistral-7b"
tensor-parallel-size: 1
gpu-memory-utilization: 0.8
max-model-len: 4096
max-num-seqs: 32
max-num-batched-tokens: 8192
quantization: "awq"  # 4-bit quantization
dtype: "half"
enforce-eager: false
disable-log-stats: false
EOF
```

### 2. Create Systemd Service
```bash
# Create systemd service file
sudo tee /etc/systemd/system/nusy-vllm.service > /dev/null << EOF
[Unit]
Description=NuSy vLLM Service (Mistral-7B)
After=network.target nvidia-persistenced.service
Requires=nvidia-persistenced.service

[Service]
Type=simple
User=nusy
Environment=HF_TOKEN=your-huggingface-token-here
WorkingDirectory=/home/nusy/nusy-dgx
ExecStart=/home/nusy/nusy-dgx-env/bin/python -m vllm.entrypoints.openai.api_server \\
    --config-file /home/nusy/nusy-dgx/config/vllm_config.yaml \\
    --host 0.0.0.0 \\
    --port 8001 \\
    --api-key nusy-dgx-2025
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable nusy-vllm
```

### 3. Start vLLM Service
```bash
# Start the service
sudo systemctl start nusy-vllm

# Check status
sudo systemctl status nusy-vllm

# View logs
sudo journalctl -u nusy-vllm -f
```

---

## 🧪 Phase 2D: Basic Testing & Validation

### 1. Test API Endpoint
```bash
# Test basic connectivity
curl -X POST http://localhost:8001/v1/chat/completions \\
  -H "Content-Type: application/json" \\
  -H "Authorization: Bearer nusy-dgx-2025" \\
  -d '{
    "model": "mistralai/Mistral-7B-Instruct-v0.1",
    "messages": [
      {"role": "user", "content": "Hello, test message"}
    ],
    "max_tokens": 100
  }'
```

### 2. Performance Benchmarking
```bash
# Create benchmark script
cat > ~/nusy-dgx/benchmark_mistral.py << 'EOF'
#!/usr/bin/env python3
"""
Mistral-7B Performance Benchmark for DGX
"""
import time
import requests
import json
from concurrent.futures import ThreadPoolExecutor

API_URL = "http://localhost:8001/v1/chat/completions"
API_KEY = "nusy-dgx-2025"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

def single_request(prompt: str) -> dict:
    """Make a single API request"""
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 100,
        "temperature": 0.7
    }
    
    start_time = time.time()
    response = requests.post(API_URL, headers=HEADERS, json=data)
    end_time = time.time()
    
    return {
        "latency": end_time - start_time,
        "status": response.status_code,
        "response_length": len(response.json().get("choices", [{}])[0].get("message", {}).get("content", ""))
    }

def benchmark_concurrent_requests(num_requests: int = 10) -> dict:
    """Benchmark concurrent requests"""
    prompts = [
        f"Explain the concept of {topic} in simple terms."
        for topic in ["machine learning", "neural networks", "software architecture", 
                     "agile development", "cloud computing", "data science", 
                     "artificial intelligence", "computer vision", "natural language processing", 
                     "distributed systems"]
    ]
    
    print(f"🚀 Starting benchmark with {num_requests} concurrent requests...")
    
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        results = list(executor.map(single_request, prompts[:num_requests]))
    end_time = time.time()
    
    latencies = [r["latency"] for r in results]
    success_rate = sum(1 for r in results if r["status"] == 200) / len(results)
    
    return {
        "total_time": end_time - start_time,
        "avg_latency": sum(latencies) / len(latencies),
        "p95_latency": sorted(latencies)[int(len(latencies) * 0.95)],
        "success_rate": success_rate,
        "requests_per_second": len(results) / (end_time - start_time)
    }

if __name__ == "__main__":
    print("🧪 Mistral-7B DGX Performance Benchmark")
    print("=" * 50)
    
    # Single request test
    print("\\n📊 Single Request Test:")
    result = single_request("What is the capital of France?")
    print(".2f")
    print(f"Status: {result['status']}")
    
    # Concurrent test
    print("\\n📊 Concurrent Requests Test:")
    benchmark = benchmark_concurrent_requests(10)
    print(".2f")
    print(".2f")
    print(".2f")
    print(".1%")
    print(".1f")
    
    print("\\n✅ Benchmark complete!")
EOF

# Run benchmark
python ~/nusy-dgx/benchmark_mistral.py
```

### 3. Santiago Agent Simulation Test
```bash
# Create agent simulation script
cat > ~/nusy-dgx/test_santiago_agents.py << 'EOF'
#!/usr/bin/env python3
"""
Test Santiago Agent Integration with Mistral-7B
"""
import asyncio
import requests
import json
import time
from concurrent.futures import ThreadPoolExecutor

API_URL = "http://localhost:8001/v1/chat/completions"
API_KEY = "nusy-dgx-2025"

SANTIAGO_ROLES = {
    "Product Manager": "You are a Product Manager in an autonomous AI development team. Focus on strategy, prioritization, and stakeholder management.",
    "Architect": "You are a Systems Architect designing scalable AI infrastructure. Focus on technical design, patterns, and system integration.",
    "Developer": "You are a Software Developer implementing features and fixing bugs. Focus on code quality, testing, and best practices.",
    "QA Specialist": "You are a QA Specialist ensuring software quality. Focus on testing strategies, defect prevention, and validation.",
    "UX Researcher": "You are a UX Researcher studying user needs and interface design. Focus on user experience and usability."
}

def create_agent_prompt(role: str, task: str) -> str:
    """Create a role-specific prompt for Santiago agent"""
    system_prompt = SANTIAGO_ROLES[role]
    return f"{system_prompt}\\n\\nTask: {task}\\n\\nProvide a detailed response as a {role.lower()} would."

async def test_single_agent(role: str, task: str) -> dict:
    """Test a single Santiago agent interaction"""
    prompt = create_agent_prompt(role, task)
    
    data = {
        "model": "mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.7
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    start_time = time.time()
    response = requests.post(API_URL, headers=headers, json=data)
    end_time = time.time()
    
    if response.status_code == 200:
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return {
            "role": role,
            "success": True,
            "latency": end_time - start_time,
            "response_length": len(content),
            "content_preview": content[:200] + "..."
        }
    else:
        return {
            "role": role,
            "success": False,
            "error": response.text,
            "latency": end_time - start_time
        }

async def test_multi_agent_simulation():
    """Test multiple Santiago agents working concurrently"""
    print("🎭 Testing Santiago Multi-Agent Simulation")
    print("=" * 50)
    
    # Define test scenarios for each role
    test_scenarios = {
        "Product Manager": "Design a roadmap for implementing AI-powered code review in a development team",
        "Architect": "Design the system architecture for a multi-agent AI development platform",
        "Developer": "Implement a REST API endpoint for user authentication with JWT tokens",
        "QA Specialist": "Create a comprehensive testing strategy for an AI-powered application",
        "UX Researcher": "Analyze user needs for an AI-assisted coding environment"
    }
    
    print("\\n🚀 Testing individual agents...")
    results = []
    for role, task in test_scenarios.items():
        print(f"\\n🤖 Testing {role}...")
        result = await test_single_agent(role, task)
        results.append(result)
        
        if result["success"]:
            print(".2f"        else:
            print(f"❌ Failed: {result['error']}")
    
    # Test concurrent execution
    print("\\n\\n🔄 Testing concurrent multi-agent execution...")
    start_time = time.time()
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        concurrent_results = list(executor.map(
            lambda item: asyncio.run(test_single_agent(item[0], item[1])), 
            test_scenarios.items()
        ))
    
    end_time = time.time()
    
    successful = sum(1 for r in concurrent_results if r["success"])
    total_time = end_time - start_time
    
    print(f"\\n📊 Concurrent Test Results:")
    print(f"Total agents: {len(concurrent_results)}")
    print(f"Successful: {successful}")
    print(f"Success rate: {successful/len(concurrent_results)*100:.1f}%")
    print(".2f")
    print(".1f")
    
    print("\\n✅ Santiago agent integration test complete!")

if __name__ == "__main__":
    asyncio.run(test_multi_agent_simulation())
EOF

# Run Santiago agent tests
python ~/nusy-dgx/test_santiago_agents.py
```

---

## 📊 Phase 2E: Monitoring & Optimization

### 1. GPU Monitoring Setup
```bash
# Install monitoring tools
pip install nvidia-ml-py3 psutil

# Create monitoring script
cat > ~/nusy-dgx/monitor_dgx.py << 'EOF'
#!/usr/bin/env python3
"""
DGX Resource Monitoring for Mistral-7B Deployment
"""
import time
import psutil
import GPUtil
import json
from datetime import datetime

def get_gpu_stats():
    """Get GPU utilization statistics"""
    gpus = GPUtil.getGPUs()
    if not gpus:
        return None
    
    gpu = gpus[0]  # Primary GPU
    return {
        "gpu_id": gpu.id,
        "name": gpu.name,
        "utilization": gpu.load * 100,
        "memory_used": gpu.memoryUsed,
        "memory_total": gpu.memoryTotal,
        "memory_free": gpu.memoryFree,
        "temperature": gpu.temperature
    }

def get_system_stats():
    """Get system resource statistics"""
    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "memory_used_gb": psutil.virtual_memory().used / (1024**3),
        "memory_total_gb": psutil.virtual_memory().total / (1024**3)
    }

def monitor_resources(duration_seconds: int = 60):
    """Monitor resources for specified duration"""
    print(f"📊 Monitoring DGX resources for {duration_seconds} seconds...")
    
    stats = []
    start_time = time.time()
    
    while time.time() - start_time < duration_seconds:
        timestamp = datetime.now().isoformat()
        gpu_stats = get_gpu_stats()
        system_stats = get_system_stats()
        
        if gpu_stats:
            stats.append({
                "timestamp": timestamp,
                "gpu": gpu_stats,
                "system": system_stats
            })
        
        time.sleep(5)  # Sample every 5 seconds
    
    # Save to file
    with open(f"~/nusy-dgx/monitoring_{int(start_time)}.json", "w") as f:
        json.dump(stats, f, indent=2)
    
    # Print summary
    if stats:
        avg_gpu_util = sum(s["gpu"]["utilization"] for s in stats) / len(stats)
        avg_memory_used = sum(s["gpu"]["memory_used"] for s in stats) / len(stats)
        max_memory_used = max(s["gpu"]["memory_used"] for s in stats)
        
        print("\\n📈 Monitoring Summary:")
        print(".1f"        print(".1f"        print(".1f"        print(f"Samples collected: {len(stats)}")
    
    return stats

if __name__ == "__main__":
    monitor_resources(60)  # Monitor for 1 minute
EOF

# Run monitoring during load test
python ~/nusy-dgx/monitor_dgx.py &
python ~/nusy-dgx/benchmark_mistral.py
```

### 2. Performance Tuning
```bash
# Adjust vLLM configuration based on monitoring results
# Edit ~/nusy-dgx/config/vllm_config.yaml as needed

# Key parameters to tune:
# - gpu-memory-utilization: Try 0.7-0.9
# - max-num-seqs: Increase for more concurrent requests
# - max-num-batched-tokens: Adjust based on memory
# - quantization: Try different quantization methods
```

---

## 🎯 Success Criteria

**Phase 2A (Environment Setup):**
- ✅ NVIDIA drivers and CUDA working
- ✅ Python environment created
- ✅ Basic dependencies installed

**Phase 2B (Model Installation):**
- ✅ Mistral-7B model downloaded
- ✅ Basic model loading test passes
- ✅ Model size confirmed (~7B parameters)

**Phase 2C (Service Configuration):**
- ✅ vLLM service installed and configured
- ✅ Systemd service running
- ✅ API endpoint accessible

**Phase 2D (Testing & Validation):**
- ✅ Single request test: <3s latency
- ✅ Concurrent test (10 agents): <6s P95 latency
- ✅ Santiago agent simulation: All roles respond appropriately

**Phase 2E (Monitoring):**
- ✅ GPU utilization <80%
- ✅ Memory usage <4GB
- ✅ Service stability confirmed

---

## 🚨 Troubleshooting

### Common Issues

**CUDA Out of Memory:**
```bash
# Reduce batch size in config
# max-num-seqs: 16
# max-num-batched-tokens: 4096
```

**Model Loading Failures:**
```bash
# Check HF_TOKEN
echo $HF_TOKEN

# Verify model path
ls -la ~/models/mistral-7b/
```

**Service Startup Issues:**
```bash
# Check logs
sudo journalctl -u nusy-vllm -n 50

# Test manual startup
source ~/nusy-dgx-env/bin/activate
python -m vllm.entrypoints.openai.api_server --model ~/models/mistral-7b --host 0.0.0.0 --port 8001
```

---

## 📋 Next Steps (Phase 3)

Once Phase 2 is complete:
1. **Multi-Model Support:** Add Vicuna-13B and Qwen-3-4B
2. **Dynamic Model Loading:** Implement model switching
3. **Production Santiago Integration:** Connect real agents
4. **Performance Optimization:** Fine-tune for production workloads

---

*Ready to deploy Mistral-7B on DGX! SSH in and run these commands when ready.*</content>
<parameter name="filePath">/Users/hankhead/Projects/Personal/nusy-product-team/expeditions/exp_dgx_llm_selection_phase2_mistral_deployment.md