#!/usr/bin/env bash
set -euo pipefail

uvicorn api.main:app --reload --port "${PORT:-8000}"
