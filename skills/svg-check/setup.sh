#!/usr/bin/env bash
# Install Playwright + Chromium so overflow-check.js can run.
# Idempotent — safe to re-run. Dependencies declared in sibling package.json.
set -euo pipefail

cd "$(dirname "$0")"

# Install declared deps (playwright).
npm install --silent --no-fund --no-audit

# Install Chromium browser binary (one-time per machine).
npx playwright install chromium --with-deps 2>&1 | tail -1

echo "Setup complete. Run:"
echo "  node $(pwd)/overflow-check.js path/to/diagram.svg"
