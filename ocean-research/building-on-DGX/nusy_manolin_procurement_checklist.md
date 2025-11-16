# NuSy Manolin Cluster – Procurement Checklist  
*Target Platform: NVIDIA DGX Spark + Storage Expansion*  

## 1. Core Compute Node

### 1.1 NVIDIA DGX Spark

- [ ] **DGX Spark unit**
  - Target price: ≈ **$3,999**
  - Includes:
    - 4 TB NVMe M.2 SSD (self-encrypting)
    - 128 GB unified LPDDR5x memory
    - Grace/Blackwell-based compute
- [ ] Power cable(s) & adapters appropriate for local region
- [ ] Warranty / support package (if separately selectable)
- [ ] Shipping & handling included in budget

### 1.2 Physical Requirements

- [ ] Desk or rack space for DGX Spark chassis  
- [ ] Adequate ventilation (clearances per NVIDIA guidelines)  
- [ ] Environment:
  - [ ] Stable power (consider UPS)
  - [ ] Ambient temperature within recommended range
  - [ ] Dust and noise considerations

---

## 2. Storage Expansion (Under $1,000)

### 2.1 External NVMe RAID Enclosure (Preferred)

- [ ] **Thunderbolt 3/4 NVMe enclosure** (e.g., OWC Express 4M2 or equivalent)
  - Target cost: **$300–$350**
  - Requirements:
    - Thunderbolt 3 or 4 connectivity
    - At least 4× M.2 NVMe slots
    - Active cooling (fan)
    - macOS/Linux compatibility

### 2.2 NVMe SSDs

Initial configuration (Phase 0–1):

- [ ] 2 × **4 TB NVMe SSD** (PCIe Gen3/Gen4, TLC preferred)
  - Target cost per drive: **$120–$250**
  - Total additional capacity: **8 TB**
- [ ] (Optional) 2 additional 4 TB drives for future expansion
  - Gives 16 TB total in enclosure

### 2.3 Optional NAS (Cold Storage / Team Archives)

*(Can be deferred to later phase)*

- [ ] 2–4 bay NAS (e.g., Synology DS224+ or similar)
- [ ] 2 × 8 TB NAS HDD (for RAID1/RAID10)
- [ ] NAS UPS (optional but recommended)

---

## 3. Networking

- [ ] Gigabit Ethernet connectivity for DGX Spark
  - [ ] At least 1× Cat6 cable
  - [ ] Port available on switch/router
- [ ] (Optional) 2.5G/10G switch if high-throughput LAN access is needed
- [ ] (Optional) NAS connected to same switch
- [ ] Confirm firewall / routing rules for:
  - SSH access
  - Web UI (FastAPI, Grafana, etc.)
  - Internal services (vector DB, KG, etc.)

---

## 4. Software & Licenses

### 4.1 Base OS & Drivers

- [ ] Compatible Linux distribution selected (e.g., Ubuntu LTS)
- [ ] NVIDIA drivers & CUDA toolkit (if required for stack)
- [ ] Container runtime:
  - [ ] Docker or Podman
  - [ ] NVIDIA Container Toolkit

### 4.2 NuSy / LLM Stack

- [ ] Python 3.11+  
- [ ] Virtual environment tooling (e.g., `venv`, `conda`, `uv`)  
- [ ] Required Python libraries:
  - [ ] `fastapi`, `uvicorn`
  - [ ] `typer`
  - [ ] `pydantic`
  - [ ] `vllm` or `transformers` + `bitsandbytes`
  - [ ] `rdflib`, `networkx` (for KG)
  - [ ] `pytest`, `pytest-asyncio`
- [ ] Model weights:
  - [ ] **Mistral-7B-Instruct** (primary Santiago base model)
  - [ ] Any auxiliary smaller models (for supporting agents)
- [ ] Vector database (optional):
  - [ ] Qdrant / Weaviate / Milvus / pgvector
- [ ] Git forge / CI integration:
  - [ ] GitHub / GitLab / Gitea account and access tokens  
  - [ ] CI runner provisioning plan

### 4.3 Security & Identity

- [ ] SSH keys for admin & development users
- [ ] (Optional) Identity provider:
  - [ ] Keycloak / Authentik (if used)
- [ ] Secrets storage:
  - [ ] `.env` files
  - [ ] Vault (HashiCorp or similar) – optional but recommended
- [ ] LLM API keys (if using any remote APIs as fallback/baseline)

---

## 5. Monitoring & Ops

- [ ] Basic system monitoring:
  - [ ] `htop`, `nvidia-smi` / DCGM
- [ ] (Optional) observability stack:
  - [ ] Prometheus + Grafana
  - [ ] Loki for logs
- [ ] Backup strategy:
  - [ ] External NVMe or NAS target
  - [ ] Schedule and retention period

---

## 6. Documentation & Process

- [ ] Repository for cluster configuration:
  - [ ] `nusy-infra` or `nusy-manolin-cluster` Git repo
- [ ] Docs to create:
  - [ ] `DGX_SPARK_SETUP.md`
  - [ ] `MANOLIN_CLUSTER_ARCHITECTURE.md`
  - [ ] `CLUSTER_OPERATIONS_RUNBOOK.md`
- [ ] Roles:
  - [ ] Named owner for hardware & infra
  - [ ] Named owner for NuSy software stack
  - [ ] Named owner for security/secrets

---

## 7. Final Sanity Check

Before placing orders:

- [ ] Verify total hardware cost (DGX Spark + storage expansion) is within budget
- [ ] Confirm lead times & availability
- [ ] Confirm rack/desk space and power availability
- [ ] Confirm that selected storage meets:
  - [ ] Capacity goals (≥ 8 TB additional)
  - [ ] Performance goals (NVMe-level for hot data)

Once all boxes are checked, procurement is **GO** for the NuSy Manolin Cluster.
