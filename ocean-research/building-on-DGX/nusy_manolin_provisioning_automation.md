# DGX Spark – Provisioning Automation Scripts (NuSy Manolin Cluster)

This document provides **starter automation scripts** for provisioning a DGX Spark node as a NuSy “Manolin Cluster” host.

> ⚠️ These are scaffolds, not production-hardened infra.  
> Customize paths, usernames, and versions before use.

---

## 1. Assumptions

- OS: Ubuntu LTS (or similar modern Linux)
- You have:
  - `sudo` access
  - Internet connectivity
  - SSH access (for remote provisioning)
- You want:
  - Base system tools
  - NVIDIA drivers & CUDA stack (if not preinstalled)
  - Container runtime
  - Python environment
  - NuSy core repo checkout
  - LLM runtime environment

---

## 2. High-Level Provisioning Steps

1. System prep & packages
2. NVIDIA drivers / container toolkit
3. Docker (or Podman) setup
4. Python and virtual env
5. NuSy repo checkout
6. Model runtime setup (Mistral-7B)
7. Basic services (FastAPI, orchestrator)

---

## 3. Script: `provision_dgx_spark_base.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

# Basic variables
USERNAME="${1:-$USER}"
NUSY_ROOT="/opt/nusy"
PYTHON_VERSION="3.11"

echo "==> Updating system packages"
sudo apt-get update -y
sudo apt-get upgrade -y

echo "==> Installing base tools"
sudo apt-get install -y \
    build-essential \
    git \
    curl \
    wget \
    htop \
    tmux \
    ca-certificates \
    software-properties-common \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-venv \
    python${PYTHON_VERSION}-distutils

echo "==> Setting default python symlink (if needed)"
if ! command -v python &>/dev/null; then
  sudo ln -s "$(command -v python${PYTHON_VERSION})" /usr/local/bin/python
fi

echo "==> Creating NuSy root at ${NUSY_ROOT}"
sudo mkdir -p "${NUSY_ROOT}"
sudo chown -R "${USERNAME}:${USERNAME}" "${NUSY_ROOT}"

echo "Base OS provisioning complete."
```

---

## 4. Script: `install_docker_and_nvidia_container_runtime.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "==> Installing Docker"
sudo apt-get remove -y docker docker-engine docker.io containerd runc || true
sudo apt-get update -y

sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

echo "==> Adding current user to docker group"
sudo usermod -aG docker "$USER"

echo "==> Installing NVIDIA Container Toolkit"
distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
  && curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | \
     sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
     sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
     sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update -y
sudo apt-get install -y nvidia-container-toolkit

sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

echo "Docker & NVIDIA container runtime installed."
echo "You may need to log out and back in for docker group changes."
```

---

## 5. Script: `setup_nusy_env.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

NUSY_ROOT="${NUSY_ROOT:-/opt/nusy}"
ENV_NAME="${ENV_NAME:-nusy-env}"
PYTHON_BIN="$(command -v python)"

echo "==> Creating Python virtual environment at ${NUSY_ROOT}/${ENV_NAME}"
mkdir -p "${NUSY_ROOT}"
cd "${NUSY_ROOT}"
"${PYTHON_BIN}" -m venv "${ENV_NAME}"

# shellcheck source=/dev/null
source "${ENV_NAME}/bin/activate"

echo "==> Installing core Python deps"
pip install --upgrade pip wheel setuptools

pip install \
    fastapi \
    uvicorn[standard] \
    typer \
    pydantic \
    python-dotenv \
    rdflib \
    networkx \
    pytest \
    vllm \
    transformers \
    accelerate \
    bitsandbytes

echo "NuSy Python environment is ready at ${NUSY_ROOT}/${ENV_NAME}"
```

---

## 6. Script: `clone_nusy_product_team_repo.sh`

Replace the repo URL with your actual remote.

```bash
#!/usr/bin/env bash
set -euo pipefail

NUSY_ROOT="${NUSY_ROOT:-/opt/nusy}"
REPO_URL="${REPO_URL:-git@github.com:your-org/nusy-product-team.git}"

echo "==> Cloning NuSy Product Team repo"
mkdir -p "${NUSY_ROOT}"
cd "${NUSY_ROOT}"

if [ ! -d "nusy-product-team" ]; then
  git clone "${REPO_URL}" nusy-product-team
else
  echo "Repo already exists, pulling latest."
  cd nusy-product-team
  git pull
fi

echo "NuSy product team repo ready at ${NUSY_ROOT}/nusy-product-team"
```

---

## 7. Script: `download_mistral_7b_instruct.sh`

This assumes you are using a Hugging Face model that’s compatible with your licensing and environment.

```bash
#!/usr/bin/env bash
set -euo pipefail

# You may need HF_TOKEN env var exported for private models.
MODEL_DIR="${MODEL_DIR:-/opt/nusy/models/mistral-7b-instruct}"

echo "==> Preparing model directory at ${MODEL_DIR}"
mkdir -p "${MODEL_DIR}"

python - << 'PYCODE'
from pathlib import Path
from huggingface_hub import snapshot_download

model_name = "mistralai/Mistral-7B-Instruct-v0.2"  # Example; adjust as needed.
target = Path("${MODEL_DIR}")

print(f"Downloading model {model_name} to {target}")
snapshot_download(repo_id=model_name, local_dir=str(target), local_dir_use_symlinks=False)
PYCODE

echo "Mistral-7B-Instruct downloaded to ${MODEL_DIR}"
```

---

## 8. Script: `run_nusy_orchestrator.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

NUSY_ROOT="${NUSY_ROOT:-/opt/nusy}"
ENV_NAME="${ENV_NAME:-nusy-env}"

source "${NUSY_ROOT}/${ENV_NAME}/bin/activate"

cd "${NUSY_ROOT}/nusy-product-team"

echo "==> Running NuSy Orchestrator API"
uvicorn src.nusy_pm_core.api:app --host 0.0.0.0 --port 8000 --reload
```

---

## 9. Putting It Together

You can create a master script like `bootstrap_manolin_cluster.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

./provision_dgx_spark_base.sh "$USER"
./install_docker_and_nvidia_container_runtime.sh
./setup_nusy_env.sh
./clone_nusy_product_team_repo.sh
./download_mistral_7b_instruct.sh

echo "Base Manolin Cluster provisioning done. Next steps:"
echo " - Configure NuSy repo (env files, secrets)."
echo " - Run: ./run_nusy_orchestrator.sh"
```

These scripts can be adapted into:

- Ansible roles
- Terraform `remote-exec` scripts
- GitHub Actions or GitLab CI jobs targeting the DGX Spark host

as your infrastructure matures.
