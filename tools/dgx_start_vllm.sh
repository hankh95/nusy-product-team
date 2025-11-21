#!/usr/bin/env bash
set -euo pipefail

# Simple wrapper to enforce DGX runtime etiquette when starting the vLLM server.
# Assumes you are already on the DGX, inside the project repo, with the venv activated.
#
# Usage:
#   export KANBAN_CARD_ID=exp-XXX-some-slug   # optional but recommended
#   ./tools/dgx_start_vllm.sh [additional args...]
#
# This script will:
#   - check/acquire a DGX runtime lock for the 'vllm' service
#   - start the vLLM server via the standard deploy script
#   - release the lock when the process exits

ROOT_DIR=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/..\" && pwd)\"
cd \"${ROOT_DIR}\"

SERVICE=\"vllm\"
LOCK_HELPER=\"${ROOT_DIR}/tools/dgx_runtime_lock.py\"
DEPLOY_SCRIPT=\"${ROOT_DIR}/expeditions/dgx-deployment-scripts/deploy_mistral_dgx.sh\"

if [[ ! -x \"${DEPLOY_SCRIPT}\" ]]; then
  echo \"❌ DGX vLLM deploy script not found or not executable: ${DEPLOY_SCRIPT}\"
  exit 1
fi

if [[ ! -x \"${LOCK_HELPER}\" ]]; then
  echo \"❌ Missing tools/dgx_runtime_lock.py; ensure it is present and executable.\"
  exit 1
fi

echo \"🔐 Requesting DGX runtime lock for service '${SERVICE}'...\"
python \"${LOCK_HELPER}\" --service \"${SERVICE}\" --action acquire

trap 'echo \"Releasing DGX runtime lock for ${SERVICE}...\"; python \"${LOCK_HELPER}\" --service \"${SERVICE}\" --action release' EXIT

echo \"🚀 Starting vLLM server for service '${SERVICE}' via ${DEPLOY_SCRIPT}...\"
\"${DEPLOY_SCRIPT}\" \"$@\"


