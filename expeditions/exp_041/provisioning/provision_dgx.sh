#!/usr/bin/env bash
# DGX Spark Provisioning Automation (Sub-EXP-041B)
# Production-ready Ubuntu LTS setup for NuSy Manolin Cluster

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="/var/log/dgx_provisioning.log"
readonly NUSY_ROOT="/opt/nusy"
readonly PYTHON_VERSION="3.11"

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
    log "ERROR: $*" >&2
    exit 1
}

# Pre-flight checks
preflight_checks() {
    log "Running pre-flight checks..."

    # Check if running as root or with sudo
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root or with sudo"
    fi

    # Check Ubuntu version
    if ! grep -q "Ubuntu" /etc/os-release; then
        error "This script is designed for Ubuntu Linux"
    fi

    # Check internet connectivity
    if ! ping -c 1 8.8.8.8 &>/dev/null; then
        error "No internet connectivity detected"
    fi

    # Check available disk space (need at least 50GB free)
    local free_space
    free_space=$(df / | tail -1 | awk '{print $4}')
    if [[ $free_space -lt 52428800 ]]; then  # 50GB in KB
        error "Insufficient disk space. Need at least 50GB free"
    fi

    log "Pre-flight checks passed"
}

# Update system packages
update_system() {
    log "Updating system packages..."

    apt-get update -y
    apt-get upgrade -y
    apt-get autoremove -y
    apt-get autoclean -y

    log "System packages updated"
}

# Install base tools and dependencies
install_base_tools() {
    log "Installing base tools and dependencies..."

    local packages=(
        # Development tools
        build-essential
        git
        curl
        wget
        htop
        tmux
        vim
        jq
        tree

        # System utilities
        ca-certificates
        software-properties-common
        apt-transport-https
        gnupg
        lsb-release
        ufw
        unattended-upgrades

        # Python
        "python${PYTHON_VERSION}"
        "python${PYTHON_VERSION}-venv"
        "python${PYTHON_VERSION}-dev"
        "python${PYTHON_VERSION}-distutils"

        # Networking
        net-tools
        openssh-server
        iptables-persistent

        # Monitoring
        sysstat
        iotop
        ncdu
        lm-sensors
    )

    apt-get install -y "${packages[@]}"

    # Set Python symlink if needed
    if ! command -v python &>/dev/null || [[ $(python --version 2>&1 | grep -oP '\d+\.\d+') != "$PYTHON_VERSION" ]]; then
        ln -sf "/usr/bin/python${PYTHON_VERSION}" /usr/local/bin/python
        log "Python ${PYTHON_VERSION} set as default"
    fi

    log "Base tools installed"
}

# Configure firewall
configure_firewall() {
    log "Configuring firewall..."

    # Enable UFW
    ufw --force enable

    # Allow SSH
    ufw allow ssh

    # Allow HTTP/HTTPS for potential web services
    ufw allow 80/tcp
    ufw allow 443/tcp

    # Allow custom ports for NuSy services
    ufw allow 8000/tcp  # FastAPI
    ufw allow 8080/tcp  # Alternative web
    ufw allow 9090/tcp  # Prometheus (if used)

    ufw reload

    log "Firewall configured"
}

# Create NuSy directories and users
setup_nusy_environment() {
    log "Setting up NuSy environment..."

    # Create nusy user if it doesn't exist
    if ! id -u nusy &>/dev/null; then
        useradd -m -s /bin/bash -G sudo,docker nusy
        log "Created nusy user"
    fi

    # Create directory structure
    mkdir -p "$NUSY_ROOT"/{models,workspace,data,logs,backups}

    # Set ownership
    chown -R nusy:nusy "$NUSY_ROOT"

    # Create workspace subdirectories
    su - nusy -c "mkdir -p $NUSY_ROOT/workspace/{cargo-manifests,personal-logs,ships-logs,captains-journals,crew-manifests}"

    log "NuSy environment created"
}

# Install Docker and NVIDIA Container Toolkit
install_docker_nvidia() {
    log "Installing Docker and NVIDIA Container Toolkit..."

    # Remove old Docker installations
    apt-get remove -y docker docker-engine docker.io containerd runc || true

    # Install Docker
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg

    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    # Start and enable Docker
    systemctl start docker
    systemctl enable docker

    # Add nusy user to docker group
    usermod -aG docker nusy

    # Install NVIDIA Container Toolkit
    distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
    curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

    apt-get update -y
    apt-get install -y nvidia-container-toolkit

    # Configure NVIDIA runtime
    nvidia-ctk runtime configure --runtime=docker
    systemctl restart docker

    log "Docker and NVIDIA Container Toolkit installed"
}

# Setup Python virtual environment
setup_python_env() {
    log "Setting up Python virtual environment..."

    su - nusy -c "
        cd '$NUSY_ROOT'
        python -m venv nusy-env
        source nusy-env/bin/activate
        pip install --upgrade pip wheel setuptools

        # Install core dependencies
        pip install \\
            fastapi \\
            uvicorn[standard] \\
            typer \\
            pydantic \\
            python-dotenv \\
            rdflib \\
            networkx \\
            pytest \\
            pytest-asyncio \\
            aiofiles \\
            requests \\
            pyyaml \\
            jinja2
    "

    log "Python environment configured"
}

# Configure system monitoring
setup_monitoring() {
    log "Setting up system monitoring..."

    # Enable sysstat for performance monitoring
    sed -i 's/ENABLED="false"/ENABLED="true"/' /etc/default/sysstat
    systemctl enable sysstat
    systemctl start sysstat

    # Install NVIDIA System Management Interface if available
    apt-get install -y nvidia-driver-470 2>/dev/null || log "NVIDIA drivers not auto-installed (may need manual installation)"

    log "System monitoring configured"
}

# Create provisioning report
create_report() {
    log "Creating provisioning report..."

    local report_file="$NUSY_ROOT/provisioning_report_$(date +%Y%m%d_%H%M%S).txt"

    cat > "$report_file" << EOF
DGX Spark Provisioning Report
Generated: $(date)
Hostname: $(hostname)
OS: $(lsb_release -d | cut -f2)
Kernel: $(uname -r)
CPU: $(nproc) cores
Memory: $(free -h | grep '^Mem:' | awk '{print $2}')
Disk: $(df -h / | tail -1 | awk '{print $2}')

Installed Components:
- Python: $(python --version 2>&1)
- Docker: $(docker --version 2>&1 | head -1)
- NVIDIA Container Toolkit: $(nvidia-container-runtime --version 2>&1 | head -1 || echo "Not detected")

NuSy Environment:
- Root Directory: $NUSY_ROOT
- User: nusy
- Python Environment: $NUSY_ROOT/nusy-env

Next Steps:
1. Install NVIDIA drivers (if not auto-detected)
2. Download models: ./download_models.sh
3. Configure services: ./configure_services.sh
4. Run validation tests: ./validate_setup.sh

Log file: $LOG_FILE
EOF

    chown nusy:nusy "$report_file"
    log "Provisioning report created: $report_file"
}

# Main provisioning function
main() {
    log "Starting DGX Spark provisioning for NuSy Manolin Cluster"
    log "Script version: 1.0"
    log "Target: Ubuntu LTS with NVIDIA DGX Spark"

    preflight_checks
    update_system
    install_base_tools
    configure_firewall
    setup_nusy_environment
    install_docker_nvidia
    setup_python_env
    setup_monitoring
    create_report

    log "DGX Spark provisioning completed successfully!"
    log "Please log out and back in for group changes to take effect."
    log "Then run: su - nusy && cd $NUSY_ROOT && source nusy-env/bin/activate"
}

# Run main function
main "$@"