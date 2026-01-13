#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="${ROOT_DIR}/docs/api"
OUT_FILE="${OUT_DIR}/openapi.yaml"

mkdir -p "${OUT_DIR}"

python - <<'PY'
import yaml
from backend.app.main import app
spec = app.openapi()

# Make the spec stable and reviewer-friendly
spec.setdefault("info", {})
spec["info"].setdefault("title", "Helpdesk AI Triage API")
spec["info"].setdefault("version", "1.0.0")

print(yaml.safe_dump(spec, sort_keys=False))
PY > "${OUT_FILE}"

echo "Wrote ${OUT_FILE}"
