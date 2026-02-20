#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
KEY_FILE="$ROOT_DIR/secrets/audit-signing.key"
ENV_FILE="$ROOT_DIR/.env"

failed=0

if [[ ! -f "$KEY_FILE" ]]; then
  echo "[ERROR] Missing required secret file: $KEY_FILE"
  echo "        Create it with: openssl rand -hex 32 > secrets/audit-signing.key"
  echo "        Then secure it with: chmod 600 secrets/audit-signing.key"
  failed=1
elif [[ ! -s "$KEY_FILE" ]]; then
  echo "[ERROR] Secret file exists but is empty: $KEY_FILE"
  failed=1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "[ERROR] Missing environment file: $ENV_FILE"
  echo "        Create it with: cp .env.example .env"
  failed=1
fi

if [[ "$failed" -ne 0 ]]; then
  exit 1
fi

echo "[OK] Container production prerequisites are present."
