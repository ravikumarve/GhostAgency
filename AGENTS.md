### [2026-06-14 17:00] - Settings Page with SQLite Persistence
- **State**: Success ✅
- **MCP Data Used**: Direct file reads (dashboard.py, base.html, brutalist.css, existing templates)
- **Agents Deployed**: @codebase (direct execution — 3 new files, 4 modified)
- **Architectural Decision**:
  - Created `core/settings_db.py` — SQLite key-value store with `get()`, `set()`, `set_many()`, `get_effective()` (DB overrides env vars)
  - Settings page at `/settings` with 4 CSS-only tabs (LLM Provider, Agent Runtime, Notifications, Billing & License)
  - Glass Brutalism design — uses existing `.form-group`, `.form-input`, `.btn-blue` classes, no new CSS
  - Form POST writes to SQLite DB; GET reads DB with env var fallback
  - Added `python-multipart` dependency for form parsing
- **Files Created** (3):
  - `core/settings_db.py` — SQLite settings store (thread-safe, WAL mode)
  - `templates/settings.html` — Settings page with CSS tab system
  - `tests/test_settings.py` — 16 tests
- **Files Modified** (4):
  - `api/routes/dashboard.py` — added `GET /settings` and `POST /settings` routes
  - `templates/base.html` — added SETTINGS nav link
  - `requirements.txt` — added `python-multipart`
- **Quality Gate**: 91/91 tests passed (75 existing + 16 new) ✅ | flake8 clean ✅
- **Next Turn Directive**: Settings page ready. Next: wire runtime config to use settings_db overrides in provider factory and base_agent.

### [2026-06-14 16:30] - Multi-Provider LLM Support — OpenAI, Anthropic, Gemini
- **State**: Success ✅
- **MCP Data Used**: Direct file reads (existing provider clients, config, base_agent), grep (import references)
- **Agents Deployed**: @codebase (direct execution — 13 new files, 5 modified)
- **Architectural Decision**:
  - Created `integrations/providers/` package with `LLMProvider` ABC — all providers implement `complete(prompt, system, max_tokens)` and `ping()`
  - `LLM_PROVIDER` env var selects primary (default: `openai`); factory chain-falls through providers on connection failure
  - NIM demoted to testing/internal role (was primary); OpenAI is now default
  - All providers use plain `requests` — zero new pip dependencies
  - `OllamaFallbackClient` now implements `LLMProvider` interface with `system` support
- **Files Created** (7):
  - `integrations/providers/__init__.py` — package exports
  - `integrations/providers/base.py` — `LLMProvider` ABC
  - `integrations/providers/openai.py` — OpenAI provider
  - `integrations/providers/anthropic.py` — Anthropic provider
  - `integrations/providers/gemini.py` — Gemini provider
  - `integrations/llm_client.py` — provider factory + `_ChainedProvider`
  - `tests/providers/test_providers.py` — 24 tests
- **Files Modified** (6):
  - `core/config.py` — added OpenAI/Anthropic/Gemini env vars
  - `core/base_agent.py` — `_call_llm()` uses `get_llm_client()` factory
  - `integrations/nim_client.py` — inherits `LLMProvider`
  - `integrations/ollama_fallback.py` — inherits `LLMProvider`, fixed bug (unbound `model` var)
  - `.env.example` — documented all 5 providers
  - `README.md` — updated architecture table
- **Quality Gate**: 75/75 tests passed (51 existing + 24 new) ✅ | flake8 clean ✅
- **Next Turn Directive**: Ready for new feature work. Consider Gumroad product listing for revenue.

### [2026-06-14 16:00] - Glass Brutalism UI Redesign — Full Implementation
- **State**: Success ✅
- **MCP Data Used**: Direct file reads (templates, CSS, landing pages)
- **Agents Deployed**: @codebase (direct execution — 13 commits)
- **Architectural Decision**:
  - Root route `/` now serves landing page; `/dashboard` serves the dashboard
  - Created reusable Jinja2 macros in `templates/macros/cards.html` (stat_card, status_badge, glass_table)
  - Added `btn-blue`, `btn-red` CSS variants for consistent button styling
  - Moved all inline styles → CSS utility classes (zero inline styles in all templates)
  - Landing page built from Landing-2 design with ember canvas, shares design tokens with dashboard
  - Accessibility: `prefers-reduced-motion` disables all animations; `:focus-visible` keyboard states on all interactive elements
- **Files Created**:
  - `templates/macros/cards.html` — Jinja2 macro library
  - `templates/landing.html` — Glass Brutalism landing page
- **Files Modified**:
  - `static/css/brutalist.css` — btn variants, utility classes, landing components, a11y
  - `templates/index.html`, `agents.html`, `clients.html`, `stats.html`, `base.html` — macro refactor, inline style cleanup
  - `ghostagency/api/routes/dashboard.py` — added `/landing` → `/dashboard` route swap
  - `tests/test_dashboard.py`, `tests/test_dashboard_integration.py` — updated for route change, added landing page test
- **Quality Gate**: 51/51 tests passed ✅ | All routes return 200 ✅
- **Next Turn Directive**: No remaining debt from this sprint. Ready for new feature work.

### [2026-06-13 20:30] - Sprint UI-Redesign-Analysis (Landing Page Evaluation)
- **State**: Analysis Complete — Handoff Ready
- **MCP Data Used**: Direct file reads (webpages/GA landing-1.html, GA landing-2.html), code_tree for dashboard template structure
- **Agents Deployed**: @orchestrator (direct analysis)
- **Architectural Decision**: Selected **Landing-2 (Glass/Interactive)** as foundation for "Glass Brutalism" design system. Its component library (`.role-card`, `.math-card`, `.table-wrapper`, `.terminal-box`) maps 1:1 to dashboard needs. Landing-1 (Cinematic/Editorial) relegated to pitch deck use.
- **Key Findings**:
  - Both pages use identical Void + Gold/Amber/Flame palette
  - Landing-2 adds `--accent-success` (#10b981) matching dashboard profit semantics
  - Landing-2's card system = reusable Jinja2 macros for index/agents/stats/clients
  - Landing-2's terminal demo proves product works (critical for technical buyers)
  - Landing-2 follows proven SaaS conversion funnel (Hero → Economics → Quick Start → Workforce → Advantages → ROI → CTA)
- **Implementation Plan**: 5 phases (Design Tokens → Jinja2 Macros → Dashboard Refactor → Landing Template → Polish) = ~7.5 hrs
- **Handoff Created**: New session with full plan for @codebase agent
- **Next Turn Directive**: @codebase to execute Phase 1-2 (design tokens + macros), then Phase 3 (dashboard template refactor)

### [2026-04-20 21:30] - Sprint Gumroad-Packaging (Git Push + Finalize)
- **State**: Success ✅ (all changes pushed to GitHub main, quality gates green)
- **MCP Data Used**: envsitter (key blanking + verification), grep (path sweep), git (push + verify)
- **Agents Deployed**: @orchestrator (direct execution)
- **Architectural Decision**:
  - Committed 75 files across 3 sprints: `feat: Gumroad-ready packaging — LICENSE, install.sh, README polish, credential remediation` (6e6702f)
  - Follow-up fix: corrected curl URL from `ghost-agency` → `GhostAgency` to match actual repo name (cdc209d)
  - Follow-up fix: updated Quick Install section — repo is **private**, so curl one-liner deferred; replaced with `clone + bash install.sh` instructions (70f7aec)
  - Key discovery: GitHub repo `ravikumarve/GhostAgency` is private — raw.githubusercontent.com URLs return 404 for unauthenticated access. The curl one-liner will only work after making the repo public or using a GitHub release with a public asset
  - All 3 commits pushed to `origin/main` successfully
- **Files Modified in this session**: README.md (2 follow-up commits)
- **Quality Gate Results**:
  - `black . --line-length 100` → ✅ 45 files unchanged
  - `flake8 . --max-line-length 100 --exclude .venv,__pycache__` → ✅ zero errors
  - `pytest --tb=short -q` → ✅ 49 passed, 0 failed
  - `bash install.sh` (clean venv) → ✅ all steps pass
  - `bash install.sh` (idempotent re-run) → ✅ all steps pass
  - `git push origin main` → ✅ 3 commits pushed (6e6702f, cdc209d, 70f7aec)
- **Remaining Debt**:
  - D1: LICENSE ✅ | D2: README ✅ | D3: install.sh ✅ | D4: .gitignore ✅ | D5: .env.example ✅
  - D6: Gumroad product listing — not yet created
  - D7: Gumroad packaging (zip/tar) — not yet created
  - D8: Repo visibility — currently private; curl one-liner requires public repo or GitHub release asset
- **Next Turn Directive**: Create Gumroad product listing. Decide on repo visibility (public for curl install, or private with zip distribution via Gumroad). Build release zip/tar for Gumroad upload.

### [2026-04-20 16:00] - Sprint Cleanup-Demo-Scripts
- **State**: Success ✅ (all quality gates green)
- **MCP Data Used**: code_tree (AST scan), grep (import verification), envsitter (key check)
- **Agents Deployed**: @orchestrator (direct execution), @backend-architect (lint fixes)
- **Architectural Decision**:
  - Fixed missing `list_agents` import in `tests/test_dashboard.py` (used on L45, L145 but never imported)
  - Removed `pytest_plugins` from `tests/test_dashboard_integration.py` (E402 violation) → created `tests/conftest.py` with inline fixtures instead of cross-package plugin reference
  - Fixed dashboard route URLs in tests: `/dashboard/` → `/`, `/dashboard/agents` → `/agents` (router mounted at root, no prefix)
  - Deleted 3 root debris files: `test_brutalist.html`, `api.log`, `server.log`
  - Created `pyproject.toml` with `pythonpath = ["."]`, `testpaths = ["tests"]`, `asyncio_mode = "auto"` — eliminates need for `PYTHONPATH=.` hack
  - Installed `pytest-timeout` in venv for per-test timeout support
- **Files Modified**: tests/test_dashboard.py, tests/test_dashboard_integration.py, tests/conftest.py (new), pyproject.toml (new)
- **Files Deleted**: test_brutalist.html, api.log, server.log
- **Quality Gate Results**:
  - `black . --line-length 100` → ✅ 45 files unchanged
  - `flake8 . --max-line-length 100 --exclude .venv,__pycache__` → ✅ zero errors
  - `pytest --tb=short -q` → ✅ 49 passed, 0 failed (0.58s)
- **Smoke Test Results**:
  - `GHOST_MOCK_AI=true python ghostagency/demo/run_demo.py` → ✅ 6/6 agents, 0 failures
  - `python ghostagency/scripts/validate_registry.py` → ✅ Registry valid: 6 agents
  - `python ghostagency/scripts/list_agents.py` → ✅ 6/6 agents listed with correct squad/price
- **Remaining Debt**: D1-D7 from CPO briefing (LICENSE, README polish, install script, Gumroad packaging)
- **Next Turn Directive**: If quality gate passes (it does ✅), the project is ready for Gumroad packaging — create LICENSE, polish README with install instructions, and build a one-click install script.

### [2026-04-19 14:30] - Sprint Model-Swap-GLM5.1
- **State**: Success
- **MCP Data Used**: envsitter (key read/set), grep (verification sweep)
- **Agents Deployed**: @orchestrator (direct execution)
- **Architectural Decision**: Migrated all NIM model references from deepseek-ai/deepseek-v3-0324 to z-ai/glm-5.1 across 5 files. Ollama fallback (deepseek-r1:7b) left untouched — it is the local CPU fallback, not NIM.
- **Files Modified**: ghostagency/core/config.py (L9), opencode.json (L3), .env.example (L4), config.py (L16), .env (NIM_MODEL key)
- **Verification**: grep -r "deepseek" --include="*.py" --include="*.json" --include="*.env*" returned zero hits. python3 DEFAULT_MODEL check returned z-ai/glm-5.1
- **Next Turn Directive**: Run pytest --tb=short -q to confirm no regressions from model swap. Then test NIM connectivity with python3 -c "from ghostagency.integrations.nim_client import NIMClient; c = NIMClient(); print(c.ping())"

# AGENTS.md — Ghost Agency Coding Intelligence File

> **Runtime context for AI coding agents (opencode + GLM 5.1 via NVIDIA NIM)**
> This file is authoritative. Follow every instruction exactly. Never guess; always reference this file first.
> **Scale:** 6 installed agents (scaling to 156) across `ghostagency/` directory.

---

## 🧠 AGENT IDENTITY & MISSION

You are the **Ghost Agency Code Agent** — an autonomous AI developer building a production-grade, multi-tenant AI Employee SaaS platform with **6 specialised AI agents (scaling to 156)** organised into functional squads.

**Your north star:** Every line of code you write must be deployable, sellable, and maintainable by a solo operator with zero DevOps team.

**Model context:** You are running inside **opencode** with **GLM 5.1 via NVIDIA NIM** (primary). Optimise for long-horizon multi-step tasks. Think before you act. When uncertain, reason step-by-step explicitly before generating code.

**Scale context:** This codebase manages 6 agents (scaling to 156). Every design decision must account for horizontal scale — naming conventions, registry lookups, and squad routing must work for agent #1 and agent #156 identically.

---

## 📁 CANONICAL PROJECT STRUCTURE

Always maintain this exact layout. Never create files outside this tree without explicit instruction.

```
ghostagency/
├── core/
│   ├── base_agent.py              # AIAgent abstract base (all agents inherit this)
│   ├── agent_registry.py          # Central registry — maps slug → class (scales to 156 entries)
│   ├── squad_router.py            # Routes tasks to correct squad
│   ├── config.py                  # Centralised config and environment loading
│   ├── logger.py                  # Shared structured JSON logger
│   └── exceptions.py              # Custom exception hierarchy
│
├── agents/                        # Agent modules, organised by squad (6+ and growing)
│   ├── squad_support/             # Customer-facing support agents
│   ├── squad_sales/               # Sales, SDR, and revenue agents
│   ├── squad_content/             # Social media, copywriting, SEO agents
│   ├── squad_ops/                 # Executive assist, scheduling, admin agents
│   ├── squad_data/                # Research, analytics, reporting agents
│   ├── squad_dev/                 # Developer assist, code review, QA agents
│   ├── squad_finance/             # Invoicing, expense, bookkeeping agents
│   ├── squad_hr/                  # Recruiting, onboarding, culture agents
│   ├── squad_legal/               # Contract review, compliance, NDA agents
│   └── squad_custom/              # Client-specific custom agents
│
├── kb/                            # Knowledge base loader utilities
│   ├── loader.py
│   ├── chunker.py                 # KB chunking for large documents
│   └── cache.py                   # In-memory KB cache (load once, reuse)
│
├── integrations/                  # Third-party integrations
│   ├── email_smtp.py
│   ├── webhook.py
│   ├── telegram_bot.py
│   ├── gumroad.py                 # License key validation
│   └── nim_client.py              # NVIDIA NIM API client (primary LLM)
│
├── api/                           # FastAPI REST layer
│   ├── main.py
│   ├── routes/
│   │   ├── agents.py              # /agents/* endpoints
│   │   ├── squads.py              # /squads/* endpoints
│   │   └── health.py              # /health, /metrics
│   └── middleware/
│       ├── auth.py                # License key + API key middleware
│       └── rate_limiter.py
│
├── tests/                         # All test files live here
│   ├── conftest.py                # Shared fixtures and mock factories
│   ├── test_base_agent.py
│   ├── test_agent_registry.py
│   ├── test_squad_router.py
│   ├── squads/                    # One test file per squad
│   │   ├── test_squad_support.py
│   │   ├── test_squad_sales.py
│   │   ├── test_squad_content.py
│   │   ├── test_squad_ops.py
│   │   ├── test_squad_data.py
│   │   ├── test_squad_dev.py
│   │   ├── test_squad_finance.py
│   │   ├── test_squad_hr.py
│   │   ├── test_squad_legal.py
│   │   └── test_squad_custom.py
│   └── integration/
│       └── test_nim_client.py
│
├── demo/
│   ├── run_demo.py                # Full interactive demo (all squads)
│   └── run_squad_demo.py          # Demo a single squad by name
│
├── scripts/
│   ├── list_agents.py             # Print all agents with squad + status
│   ├── validate_registry.py       # Assert agents registered correctly
│   └── benchmark.py              # Response time benchmarks per squad
│
├── logs/                          # Auto-created at runtime
│   └── {client_slug}/
│       └── {squad}/
│           └── {agent_slug}/
│
├── AGENTS.md                      # This file
├── README.md
├── GHOST_AGENCY.md                # Business plan (do not modify)
├── requirements.txt
└── .env.example
```

---

## 🛠️ DEVELOPMENT COMMANDS (copy-paste ready)

### Environment Setup
```bash
python3 --version   # Must be 3.10+

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
pip install black==24.4.2 flake8==7.1.0 pytest==8.2.0 pytest-cov==5.0.0 mypy==1.10.0
```

### NVIDIA NIM Setup (primary LLM — cloud, no GPU required)
```bash
# NIM uses GLM 5.1 via API — no local GPU needed
# Set in .env:
# NIM_API_KEY=your_key_here
# NIM_BASE_URL=https://integrate.api.nvidia.com/v1
# NIM_MODEL=z-ai/glm-5.1

# Verify NIM connection
python -c "from ghostagency.integrations.nim_client import NIMClient; c = NIMClient(); print(c.ping())"
```

### Ollama Setup (fallback for offline/CPU-only use)
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull deepseek-r1:7b
ollama pull phi3            # Lightweight fallback
ollama serve
curl http://localhost:11434/api/tags
```

### Agent Registry
```bash
# List all 156 agents with squad and status
python scripts/list_agents.py

# Validate registry integrity (count must equal 156)
python scripts/validate_registry.py

# Add a new agent to registry (interactive)
python scripts/list_agents.py --add
```

### Code Quality
```bash
# Format
black . --line-length 100

# Lint
flake8 . --max-line-length 100 --exclude .venv,__pycache__,logs

# Type check
mypy ghostagency/core/ ghostagency/agents/ --ignore-missing-imports

# Full pre-commit sequence
black . --line-length 100 && flake8 . --max-line-length 100 && pytest --tb=short -q
```

### Testing
```bash
# Run all tests
pytest

# With coverage
pytest --cov=ghostagency --cov-report=term-missing

# Run a specific squad's tests
pytest tests/squads/test_squad_support.py -v

# Run tests matching a keyword
pytest -k "escalation" -v

# Run with live stdout (debug AI responses)
pytest -s tests/squads/test_squad_support.py

# Benchmark response times across all squads
python scripts/benchmark.py
```

### Demo & Manual Testing
```bash
# Full demo — all squads
python demo/run_demo.py

# Single squad demo
python demo/run_squad_demo.py --squad support
python demo/run_squad_demo.py --squad sales

# Mock mode (no LLM calls)
GHOST_MOCK_AI=true python demo/run_demo.py
```

---

## 🤖 AGENT ARCHITECTURE

### Base Class Contract

Every agent **must** inherit from `AIAgent` and implement these methods:

```python
# ghostagency/core/base_agent.py
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Optional
from ghostagency.core.config import DEFAULT_MODEL, LOG_DIR
from ghostagency.core.logger import get_logger


class AIAgent(ABC):
    """
    Abstract base for all Ghost Agency AI agents.
    Concrete subclasses must implement: primary_action(), get_role_prompt(), agent_slug
    """

    # --- Required class-level attributes (define in every subclass) ---
    agent_slug: str        # e.g. "support-tier1", "sdr-cold-outreach"
    squad: str             # e.g. "support", "sales", "content"
    display_name: str      # Human-readable name shown in UI
    price_tier: str        # e.g. "$800/mo" — used in Gumroad listing
    version: str = "1.0.0"

    def __init__(
        self,
        client_name: str,
        knowledge_base_path: str | None = None,
        model: str | None = None,
    ) -> None:
        self.client_name = client_name
        self.model = model or DEFAULT_MODEL
        self.conversation_history: list[dict] = []
        self.knowledge_base: str = self._load_kb(knowledge_base_path)
        self.logger = get_logger(self.agent_slug, client_name)

    @abstractmethod
    def primary_action(self, input: str, **kwargs) -> str:
        """The main capability of this agent. Must be implemented."""
        ...

    @abstractmethod
    def get_role_prompt(self) -> str:
        """Returns the system prompt defining this agent's role."""
        ...

    def _call_llm(self, prompt: str, model: str | None = None) -> str:
        """Shared LLM caller (NIM primary, Ollama fallback). Never override."""
        ...

    def _log_interaction(self, action: str, input: str, output: str) -> None:
        """Shared structured JSON logger. Never override."""
        ...

    def _load_kb(self, path: str | None) -> str:
        """Load and cache knowledge base. Returns empty string if no path."""
        ...

    def reset_history(self) -> None:
        """Clear conversation history. Call between client sessions."""
        self.conversation_history = []
```

### Agent Registry Pattern

The registry maps every agent slug to its class. It currently contains **6 entries** (scaling to 156).

```python
# ghostagency/core/agent_registry.py
from __future__ import annotations
from typing import Type
from ghostagency.core.base_agent import AIAgent

# Import agent classes (6 currently, scaling to 156)
from ghostagency.agents.squad_support import *
from ghostagency.agents.squad_sales import *
from ghostagency.agents.squad_content import *
from ghostagency.agents.squad_ops import *
from ghostagency.agents.squad_data import *
from ghostagency.agents.squad_dev import *
from ghostagency.agents.squad_finance import *
from ghostagency.agents.squad_hr import *
from ghostagency.agents.squad_legal import *
from ghostagency.agents.squad_custom import *

AGENT_REGISTRY: dict[str, Type[AIAgent]] = {
    # support squad (example entries)
    "support-tier1":             SupportTier1Agent,
    "support-tier2":             SupportTier2Agent,
    "support-billing":           SupportBillingAgent,
    # ... all entries ...
}

TOTAL_AGENTS = 6

def get_agent(slug: str) -> Type[AIAgent]:
    if slug not in AGENT_REGISTRY:
        raise KeyError(f"Agent '{slug}' not found. Run `python scripts/list_agents.py` to see all {TOTAL_AGENTS}.")
    return AGENT_REGISTRY[slug]

def validate_registry() -> bool:
    """Called at startup. Fails loudly if count != TOTAL_AGENTS."""
    count = len(AGENT_REGISTRY)
    assert count == TOTAL_AGENTS, f"Registry has {count} agents, expected {TOTAL_AGENTS}"
    return True
```

### Squad Overview (6 Agents Total - Scaling to 156)

| Squad | Dir | Agent Count | Price Range | Primary Method |
|---|---|---|---|---|
| Support | `squad_support/` | 18 | $600–900/mo | `handle_ticket()` |
| Sales | `squad_sales/` | 20 | $900–1,500/mo | `qualify_lead()` |
| Content | `squad_content/` | 22 | $500–800/mo | `create_content()` |
| Ops | `squad_ops/` | 16 | $1,200–2,000/mo | `handle_request()` |
| Data | `squad_data/` | 18 | $800–1,400/mo | `run_analysis()` |
| Dev | `squad_dev/` | 20 | $1,000–1,800/mo | `assist_dev()` |
| Finance | `squad_finance/` | 14 | $700–1,200/mo | `process_task()` |
| HR | `squad_hr/` | 14 | $600–1,000/mo | `handle_hr_task()` |
| Legal | `squad_legal/` | 10 | $1,500–2,500/mo | `review_document()` |
| Custom | `squad_custom/` | 4 | Custom pricing | `custom_action()` |
| **Total** | | **156** | | |

---

## 🔌 LLM CLIENT — NVIDIA NIM (Primary)

```python
# ghostagency/integrations/nim_client.py
from __future__ import annotations
import os
import requests
from typing import Optional
from ghostagency.core.exceptions import LLMConnectionError, LLMTimeoutError

NIM_BASE_URL = os.getenv("NIM_BASE_URL", "[https://integrate.api.nvidia.com/v1](https://integrate.api.nvidia.com/v1)")
NIM_MODEL = os.getenv("NIM_MODEL", "z-ai/glm-5.1")
NIM_API_KEY = os.getenv("NIM_API_KEY", "")
NIM_TIMEOUT = int(os.getenv("NIM_TIMEOUT", "60"))
MAX_RETRIES = int(os.getenv("GHOST_MAX_RETRIES", "3"))


class NIMClient:
    """NVIDIA NIM API client — primary LLM backend for all agents."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or NIM_MODEL
        self.base_url = NIM_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {NIM_API_KEY}",
            "Content-Type": "application/json",
        }

    def ping(self) -> str:
        """Verify NIM connectivity."""
        resp = self.complete("Say: NIM OK")
        return resp

    def complete(self, prompt: str, system: str = "", max_tokens: int = 1024) -> str:
        """Single-turn completion. Retries up to MAX_RETRIES."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(MAX_RETRIES):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={"model": self.model, "messages": messages, "max_tokens": max_tokens},
                    timeout=NIM_TIMEOUT,
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"].strip()

            except requests.Timeout:
                if attempt == MAX_RETRIES - 1:
                    raise LLMTimeoutError(f"NIM timeout after {NIM_TIMEOUT}s on attempt {attempt + 1}")

            except requests.ConnectionError as e:
                raise LLMConnectionError(f"NIM connection failed: {e}")

            except (KeyError, IndexError) as e:
                return f"ERROR: Unexpected NIM response format: {e}"

        return "ERROR: Max retries exceeded"


class OllamaFallbackClient:
    """Fallback to local Ollama when NIM is unavailable (CPU-only mode)."""

    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

    def complete(self, prompt: str, model: str = "deepseek-r1:7b") -> str:
        ...
```

### LLM Selection Logic (in `base_agent.py`)

```python
def _call_llm(self, prompt: str, model: str | None = None) -> str:
    """NIM primary → Ollama fallback → Mock."""
    if os.getenv("GHOST_MOCK_AI") == "true":
        return f"[MOCK] Response for: {prompt[:50]}"

    try:
        client = NIMClient(model=model or self.model)
        return client.complete(prompt, system=self.get_role_prompt())
    except LLMConnectionError:
        # Fallback to Ollama (CPU-only machines)
        fallback = OllamaFallbackClient()
        return fallback.complete(prompt, model="phi3")
```

---

## 📐 CODE STYLE RULES (non-negotiable)

### Python Version & Type Hints
```python
from __future__ import annotations
from typing import Optional

# Use union type syntax (3.10+)
def primary_action(self, input: str, context: dict | None = None) -> str: ...

# Use match-case for routing
match squad:
    case "support":   return SupportRouter(task)
    case "sales":     return SalesRouter(task)
    case "content":   return ContentRouter(task)
    case _:           raise ValueError(f"Unknown squad: {squad}")
```

### Naming Conventions (critical for agent scale)
```python
# Agent slugs: {squad}-{role}  (kebab-case, max 40 chars)
"support-tier1"           ✅
"sales-cold-outreach-sdr" ✅
"SupportTier1"            ❌ (not a slug)

# Agent class names: {Squad}{Role}Agent  (PascalCase)
class SupportTier1Agent(AIAgent): ...        ✅
class SalesColdOutreachSDRAgent(AIAgent): ... ✅

# Squad directory names: squad_{name}  (snake_case)
squad_support/  ✅
support/        ❌

# Module files: {agent_slug_underscored}.py
squad_support/support_tier1.py         ✅
squad_support/SupportTier1.py          ❌
```

### Imports (strict order)
```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import os, json, logging
from datetime import datetime, UTC
from pathlib import Path
from typing import Optional
from abc import ABC, abstractmethod

# 3. Third-party
import requests
from dotenv import load_dotenv

# 4. Local — core first, then integrations
from ghostagency.core.config import DEFAULT_MODEL, LOG_DIR
from ghostagency.core.logger import get_logger
from ghostagency.core.exceptions import LLMConnectionError
from ghostagency.integrations.nim_client import NIMClient
```

---

## 🧪 TESTING RULES

### Test File Structure
```python
"""Tests for SupportTier1Agent — squad_support."""
import pytest
from unittest.mock import patch, Mock
from ghostagency.agents.squad_support.support_tier1 import SupportTier1Agent


@pytest.fixture
def agent():
    return SupportTier1Agent(client_name="TestCo", knowledge_base_path=None)

@pytest.fixture
def mock_nim():
    """Patches NIMClient.complete to return a canned response."""
    with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
        m.return_value = "Your order ships in 3-5 business days."
        yield m


class TestSupportTier1Agent:

    def test_primary_action_returns_string(self, agent, mock_nim):
        result = agent.primary_action("Where is my order?")
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        from ghostagency.core.agent_registry import AGENT_REGISTRY
        assert "support-tier1" in AGENT_REGISTRY

    def test_nim_timeout_falls_back_gracefully(self, agent):
        from ghostagency.core.exceptions import LLMTimeoutError
        with patch("ghostagency.integrations.nim_client.NIMClient.complete",
                   side_effect=LLMTimeoutError("timeout")):
            result = agent.primary_action("Hello")
        assert isinstance(result, str)  # Must not raise

    def test_logs_written_on_interaction(self, agent, mock_nim, tmp_path):
        agent.logger.log_dir = tmp_path
        agent.primary_action("Test")
        assert len(list(tmp_path.glob("**/*.json"))) >= 1
```

### Registry Integrity Test (run this always)
```python
# tests/test_agent_registry.py
from ghostagency.core.agent_registry import AGENT_REGISTRY, TOTAL_AGENTS

def test_registry_count():
    assert len(AGENT_REGISTRY) == TOTAL_AGENTS, \
        f"Expected {TOTAL_AGENTS} agents, got {len(AGENT_REGISTRY)}"

def test_all_agents_inherit_base():
    from ghostagency.core.base_agent import AIAgent
    for slug, cls in AGENT_REGISTRY.items():
        assert issubclass(cls, AIAgent), f"{slug} does not inherit AIAgent"

def test_all_agents_have_required_attributes():
    required = ["agent_slug", "squad", "display_name", "price_tier"]
    for slug, cls in AGENT_REGISTRY.items():
        for attr in required:
            assert hasattr(cls, attr), f"{slug} missing class attribute: {attr}"
```

### Coverage Requirements
- Registry, router, base agent: **100%**
- Every `primary_action()`: **100%**
- `_call_llm()`: must test NIM success, NIM timeout, Ollama fallback, mock mode
- All other non-demo code: **≥ 80%**

### Mocking Rules
- **Always** mock `NIMClient.complete` in unit tests — never hit real NIM in CI
- **Always** mock `OllamaFallbackClient.complete` as secondary
- Use `GHOST_MOCK_AI=true` for integration smoke tests
- Never mock file I/O — use `tmp_path` pytest fixture

---

## 🔒 SECURITY & SECRETS

### Rules (no exceptions)
1. **Never** hardcode API keys, NIM keys, passwords, or tokens in any `.py` file
2. **Never** commit `.env` — only `.env.example`
3. **Always** load secrets via `os.getenv()` with a safe default
4. **Always** sanitise input before injecting into prompts (strip HTML, truncate at 2000 chars)
5. **Always** redact emails and phone numbers in log output
6. **Never** log NIM API keys or full request headers

### `.env.example` Template
```env
# NVIDIA NIM (primary LLM)
NIM_API_KEY=
NIM_BASE_URL=https://integrate.api.nvidia.com/v1
NIM_MODEL=z-ai/glm-5.1
NIM_TIMEOUT=60

# Ollama (local fallback — CPU-only)
OLLAMA_URL=http://localhost:11434/api/generate
GHOST_MODEL=deepseek-r1:7b
OLLAMA_TIMEOUT=120

# Agent runtime
GHOST_MOCK_AI=false
GHOST_MAX_RETRIES=3
GHOST_LOG_DIR=logs

# Email (escalation)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=

# Webhook
ESCALATION_WEBHOOK_URL=

# Gumroad (license validation)
GUMROAD_PRODUCT_ID=
GUMROAD_ACCESS_TOKEN=

# Telegram bot (optional)
TELEGRAM_BOT_TOKEN=
```

---

## 📊 PERFORMANCE TARGETS

| Metric | Target | Alert Threshold |
|---|---|---|
| NIM response time (p50) | < 4s | > 15s |
| NIM response time (p95) | < 10s | > 30s |
| Ollama fallback (p50) | < 12s | > 45s |
| primary_action success rate | > 97% | < 92% |
| Escalation rate | 5–15% | > 30% |
| Registry load time | < 200ms | > 1s |
| Log write failure rate | 0% | > 1% |

### Optimisation Patterns (for agent scale)
```python
# ✅ Cache KB at init, not per-call
def __init__(self, ...):
    self.knowledge_base = self._load_kb(knowledge_base_path)  # Once

# ✅ Hard-cap KB injection
system_prompt = "\n".join([
    f"You are {self.display_name} for {self.client_name}.",
    f"KB:\n{self.knowledge_base[:3000]}",
    "Respond concisely. If unsure, say so.",
])

# ✅ Trim conversation history to prevent context overflow
MAX_HISTORY_TURNS = 20
if len(self.conversation_history) > MAX_HISTORY_TURNS * 2:
    self.conversation_history = self.conversation_history[-MAX_HISTORY_TURNS * 2:]

# ✅ Registry is loaded once at import time — never rebuild per request
# ❌ Don't scan agent dirs at runtime — the registry dict is the source of truth
```

---

## 🚀 DEPLOYMENT CHECKLIST

Before marking any feature "done":

- [ ] `pytest --tb=short -q` — all tests pass
- [ ] `pytest --cov=ghostagency` — coverage ≥ 80% globally, 100% on registry + base
- [ ] `python scripts/validate_registry.py` — confirms agents registered correctly
- [ ] `flake8 . --max-line-length 100` — no lint errors
- [ ] `mypy ghostagency/core/ ghostagency/agents/ --ignore-missing-imports` — no type errors
- [ ] `grep -r "api_key\|password\|secret\|NIM_API_KEY" . --include="*.py"` — no hardcoded secrets
- [ ] `GHOST_MOCK_AI=true python demo/run_demo.py` — demo runs clean
- [ ] `python scripts/list_agents.py` — all agents listed with correct squad
- [ ] Log files created under `logs/{client_slug}/{squad}/{agent_slug}/`
- [ ] README reflects any new CLI commands or env vars

---

## 🆘 TROUBLESHOOTING QUICK REFERENCE

| Symptom | Diagnosis | Fix |
|---|---|---|
| `LLMConnectionError: NIM` | NIM API key missing or wrong | Check `NIM_API_KEY` in `.env` |
| `LLMTimeoutError` | Prompt too long or NIM overloaded | Reduce KB injection size; retry |
| `KeyError: agent not found` | Agent slug not in registry | Run `python scripts/validate_registry.py` |
| `AssertionError: 4 agents, expected 6` | Agents not registered | Add missing slugs to `AGENT_REGISTRY` |
| `ImportError` on squad module | Agent file not created yet | Create the agent file first, then register |
| `ERROR: Ollama not running` | Ollama fallback not started | `ollama serve` in separate terminal |
| `ERROR: model not found` | Model not pulled | `ollama pull deepseek-r1:7b` |
| Tests fail `ConnectionRefused` | Tests hitting real NIM/Ollama | Add `GHOST_MOCK_AI=true` or mock `NIMClient.complete` |
| High escalation rate > 30% | KB too thin | Add content to client knowledge base |
| Registry load > 1s | Too many dynamic imports | Convert squad `__init__.py` to explicit imports |
| Logs not appearing | Log dir permissions | `mkdir -p logs && chmod 755 logs` |

---

## 📏 AGENT DECISION RULES

When you (the AI coding agent) are uncertain, follow these in order:

1. **Registry first** — if an agent slug isn't in `AGENT_REGISTRY`, it doesn't exist. Check the registry before writing new code.
2. **Validate count** — after any add/remove, run `validate_registry.py`. Count must match TOTAL_AGENTS.
3. **Structure first** — create the file skeleton before filling content.
4. **Tests before implementation** — write test stubs first, then make them pass.
5. **Mock by default** — any external call (NIM, Ollama, SMTP, webhook) must be mockable via env var or dependency injection.
6. **One class, one file** — if a class grows > 400 lines, propose splitting it.
7. **Never break the demo** — `demo/run_demo.py` must always run after any change.
8. **Config not code** — any value that differs between clients goes in `config.py` + `.env`.
9. **Log everything** — every `primary_action()` call must produce a structured log entry.
10. **Squad routing** — new agents must declare `squad` class attribute matching their `squad_*` directory name exactly.

---

## 🧩 OPENCODE-SPECIFIC INSTRUCTIONS

### Model Selection
- **z-ai/glm-5.1(NIM)** — default for all coding tasks (fast, accurate)
- **DeepSeek R1** — use for complex multi-step reasoning: architecture decisions, escalation routing design, registry refactoring

### For GLM 5.1 (fast coding)
- Prefer direct code generation
- Use the test file as your spec — write code to pass the tests, not the other way around
- Generate complete, runnable files — no placeholders like `# TODO: implement`

### For DeepSeek R1 (reasoning tasks)
- Emit reasoning in a `<think>` block before any code
- For multi-step refactoring (e.g. migrating agents to a new base class), plan all changes before writing a single line
- Confirm the full file structure before editing to avoid orphaned functions

### Tool Use in opencode
```bash
# Verify imports before reporting done
python -c "from ghostagency.core.agent_registry import AGENT_REGISTRY; print(len(AGENT_REGISTRY), 'agents loaded')"

# Run registry validation
python scripts/validate_registry.py

# Run squad-specific tests
pytest tests/squads/test_squad_support.py --tb=short -q

# Full quality gate
black . --line-length 100 && flake8 . --max-line-length 100 && pytest --tb=short -q
```

### File Editing Rules
- Always **read** the target file before editing it
- Make **one logical change** per edit — do not batch unrelated changes
- After editing an agent file, run its squad test class to confirm no regression
- After editing `agent_registry.py`, always run `validate_registry.py`
- When in doubt about scope, leave: `# AGENT NOTE: need clarification on X`

### Adding a New Agent (step-by-step)
```bash
# 1. Create the agent file
touch ghostagency/agents/squad_support/support_new_role.py

# 2. Implement the class (inherit AIAgent, set all class attrs)

# 3. Add to squad __init__.py
echo "from .support_new_role import SupportNewRoleAgent" >> ghostagency/agents/squad_support/__init__.py

# 4. Register in agent_registry.py
# "support-new-role": SupportNewRoleAgent,

# 5. Validate count
python scripts/validate_registry.py

# 6. Write tests
touch tests/squads/test_squad_support.py  # Add test class for new agent

# 7. Run tests
pytest tests/squads/test_squad_support.py -v
```

---

*This file is the single source of truth for all coding agents working on Ghost Agency.*
*Last updated: 2025 | Scale: 6 agents (scaling to 156) | Model: opencode + GLM 5.1 via NVIDIA NIM*
