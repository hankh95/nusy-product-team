#!/usr/bin/env bash
set -euo pipefail

TOPIC_ID="${1:-example-topic}"

echo "Comparing BMJ pipeline vs Santiago-Doctor-BMJ for topic: ${TOPIC_ID}"

# TODO: implement actual comparison logic here.
# Expected responsibilities:
# - Ensure outputs/bmj/${TOPIC_ID}/ and outputs/santiago-doctor-bmj/${TOPIC_ID}/ exist
# - Compare framed files, logic completeness, BDD results, and timing
# - Emit a summary report

echo "[stub] Comparing outputs/bmj/${TOPIC_ID}/ with outputs/santiago-doctor-bmj/${TOPIC_ID}/ ..."
echo "[stub] (Implement diffing and scoring here.)"
