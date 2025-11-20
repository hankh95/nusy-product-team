#!/usr/bin/env bash
set -euo pipefail

TOPIC_ID="${1:-example-topic}"

echo "Running BMJ pipeline on DGX for topic: ${TOPIC_ID}"

# TODO: implement real BMJ pipeline invocation here.
# Expected responsibilities:
# - Start or connect to DGX LLM
# - Set environment for BMJ pipeline
# - Run BMJ extraction/graph/framed-file generation for ${TOPIC_ID}
# - Run BDD tests
# - Store outputs under outputs/bmj/${TOPIC_ID}/

echo "[stub] Starting DGX LLM for BMJ pipeline ..."
echo "[stub] Running BMJ pipeline for topic ${TOPIC_ID} ..."
echo "[stub] Writing outputs to outputs/bmj/${TOPIC_ID}/ ..."
