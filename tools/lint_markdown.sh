#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob

# Run markdownlint using npx without installing globally.
# Exclude node_modules and .git by default.

if ! command -v npx >/dev/null 2>&1; then
  echo "npx not found. Install Node.js to run markdown lint." >&2
  exit 2
fi

# Use markdownlint-cli2 if available, fallback to markdownlint-cli
if npx --yes --quiet markdownlint-cli2 --version >/dev/null 2>&1; then
  npx --yes markdownlint-cli2 "**/*.md" "#node_modules" "#.git" || exit 1
else
  npx --yes markdownlint "**/*.md" --ignore node_modules --ignore .git || exit 1
fi

echo "Markdown lint completed."