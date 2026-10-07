#!/usr/bin/env bash
# Wrapper que ativa o venv e roda o CLI
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec "$SCRIPT_DIR/.venv/bin/python3" -m cyber_astra "$@"
