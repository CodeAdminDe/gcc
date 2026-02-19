#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Running lint"
python3 -m ruff check src tests

echo "[2/3] Running tests"
python3 -m pytest -q

echo "[3/3] Syntax compile check"
python3 -m py_compile src/gcc_mcp/*.py

cat <<'EOF'

Local checks passed.

Next, run MCP Inspector manually:

  npx @modelcontextprotocol/inspector

Then configure stdio target:

  command: gcc-mcp
  args:    (none)

Run through checklist in docs/mcp-inspector-runbook.md
EOF
