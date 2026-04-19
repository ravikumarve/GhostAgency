#!/usr/bin/env bash
set -euo pipefail

# ──────────────────────────────────────────────
# Ghost Agency — One-Click Install Script
# Idempotent: safe to re-run at any time.
# ──────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ── 1. Check Python 3.10+ ─────────────────────
echo "🔍 Checking Python version..."

if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 not found. Install Python 3.10+ and re-run."
    exit 1
fi

PY_MAJOR=$(python3 -c 'import sys; print(sys.version_info.major)')
PY_MINOR=$(python3 -c 'import sys; print(sys.version_info.minor)')

if [[ "$PY_MAJOR" -lt 3 ]] || [[ "$PY_MAJOR" -eq 3 && "$PY_MINOR" -lt 10 ]]; then
    echo "❌ Python 3.10+ required (found 3.${PY_MINOR}). Upgrade and re-run."
    exit 1
fi

echo "✅ Python 3.${PY_MINOR} detected"

# ── 2. Create virtual environment ──────────────
if [[ ! -d ".venv" ]]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "📦 Virtual environment already exists — reusing"
fi

# ── 3. Install deps using venv pip explicitly ──
PIP=".venv/bin/pip"
PYTHON=".venv/bin/python"

echo "📥 Installing dependencies..."
$PIP install --quiet --upgrade pip
$PIP install --quiet -r requirements.txt

# ── 4. Copy .env.example → .env if missing ────
if [[ ! -f ".env" ]]; then
    echo "⚙️  Creating .env from .env.example"
    cp .env.example .env
    echo "   → Edit .env to add your NIM_API_KEY or Ollama config"
else
    echo "⚙️  .env already exists — preserving"
fi

# ── 5. Validate agent registry ─────────────────
echo "🤖 Validating agent registry..."
PYTHONPATH=. $PYTHON ghostagency/scripts/validate_registry.py

# ── 6. Done ────────────────────────────────────
echo ""
echo "✅ Ghost Agency installed!"
echo "   Run:  PYTHONPATH=. GHOST_MOCK_AI=true python ghostagency/demo/run_demo.py"
echo ""
exit 0
