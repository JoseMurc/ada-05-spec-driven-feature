#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Running tests"
pytest -v

echo "[2/3] Running lint"
ruff check .

echo "[3/3] Repository checks"
python scripts/check_repo_contract.py

echo "VERIFY_REPO: PASS"
