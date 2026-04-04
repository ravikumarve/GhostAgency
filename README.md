# 👻 Ghost Agency — Production AI Employee Platform

> **Deploy 156 specialized AI agents. Charge $600–$2,500/month. Keep 95% margin.**  
> Built for solo operators. Runs on a single VPS. Powered by NVIDIA NIM + Ollama fallback.

---

## 💡 What Is This?

Ghost Agency is a **productised AI staffing system**. You run specialised AI agents that handle real business tasks — customer support, sales, social media, executive assistance — and sell access to those agents as a monthly subscription.

You are not selling software. You are renting AI employees.

| | Human Employee | Ghost Agency AI |
|---|---|---|
| Monthly cost | $3,000–$5,000 | $500–$2,000 |
| Available | 40 hrs/week | 24/7 |
| Sick days | Yes | Never |
| Onboarding | 4–8 weeks | 2–4 hours |
| Your cost | N/A | $6–11/month |

**Your margin per client: ~95%.**

---

## 🤖 The AI Employee Roster (156 Agents)

| Squad | Agent Count | Price Range | Primary Capabilities |
|---|---|---|---|
| **Support** | 18 agents | $600–900/mo | Ticket handling, billing support, technical troubleshooting |
| **Sales** | 20 agents | $900–1,500/mo | Lead qualification, cold outreach, deal strategy |
| **Content** | 22 agents | $500–800/mo | Social media, blog writing, SEO optimization |
| **Operations** | 16 agents | $1,200–2,000/mo | Executive assistance, scheduling, project management |
| **Data** | 18 agents | $800–1,400/mo | Research, analytics, reporting, BI insights |
| **Development** | 20 agents | $1,000–1,800/mo | Code review, technical support, QA testing |
| **Finance** | 14 agents | $700–1,200/mo | Invoicing, expense tracking, bookkeeping |
| **HR** | 14 agents | $600–1,000/mo | Recruitment, onboarding, employee engagement |
| **Legal** | 10 agents | $1,500–2,500/mo | Contract review, compliance, NDA management |
| **Custom** | 4 agents | Custom pricing | Client-specific specialized agents |

**Full agent registry:** Run `python scripts/list_agents.py` to see all 156 agents

---

## ⚡ Quickstart (10 minutes to first demo)

### 1. Prerequisites

```bash
# Python 3.12 or higher required
python3 --version

# Optional: Install Ollama for fallback (Linux)
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Configure NVIDIA NIM (Primary)

```bash
# Get NVIDIA NIM API key from: https://build.nvidia.com
# Set in .env:
NIM_API_KEY=your_key_here
NIM_MODEL=deepseek-ai/deepseek-v3-0324

# Optional: Ollama fallback models
ollama pull deepseek-r1:7b      # 8GB RAM minimum
ollama pull phi3                # Lightweight fallback (4GB RAM)
```

### 3. Install & Configure

```bash
# Clone the repo
git clone https://github.com/ravikumarve/ghost-agency.git
cd ghost-agency

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env to configure NVIDIA NIM and other settings
```

### 4. Run Demo

```bash
# Run demo with NVIDIA NIM (requires NIM_API_KEY)
python demo/run_demo.py

# Or run with Ollama fallback
OLLAMA_URL=http://localhost:11434/api/generate python demo/run_demo.py

# Or run in mock mode (no LLM calls)
GHOST_MOCK_AI=true python demo/run_demo.py
```

You should see the Support Tier 1 agent respond to sample tickets instantly.

### 5. Validate Registry

```bash
# List all registered agents
python scripts/list_agents.py

# Validate registry integrity
python scripts/validate_registry.py
```

---

## 📁 Project Structure

```
GhostAgency/
├── ghostagency/                  # Main package
│   ├── core/
│   │   ├── base_agent.py         # AIAgent abstract base (all 156 agents inherit this)
│   │   ├── agent_registry.py     # Central registry — maps slug → class (156 entries)
│   │   ├── config.py             # Centralized config and environment loading
│   │   ├── logger.py             # Shared structured JSON logger
│   │   └── exceptions.py         # Custom exception hierarchy
│   ├── agents/                   # 156 agent modules, organized by squad
│   │   ├── squad_support/        # Customer-facing support agents
│   │   ├── squad_sales/          # Sales, SDR, and revenue agents
│   │   ├── squad_content/       # Social media, copywriting, SEO agents
│   │   ├── squad_ops/            # Executive assist, scheduling, admin agents
│   │   ├── squad_data/           # Research, analytics, reporting agents
│   │   ├── squad_dev/            # Developer assist, code review, QA agents
│   │   ├── squad_finance/        # Invoicing, expense, bookkeeping agents
│   │   ├── squad_hr/             # Recruiting, onboarding, culture agents
│   │   ├── squad_legal/          # Contract review, compliance, NDA agents
│   │   └── squad_custom/         # Client-specific custom agents
│   ├── kb/                       # Knowledge base loader utilities
│   │   ├── loader.py
│   │   ├── chunker.py            # KB chunking for large documents
│   │   └── cache.py              # In-memory KB cache (load once, reuse)
│   └── integrations/             # Third-party integrations
│       ├── email_smtp.py
│       ├── webhook.py
│       ├── telegram_bot.py
│       ├── gumroad.py            # License key validation
│       └── nim_client.py         # NVIDIA NIM API client (primary LLM)
├── api/                           # FastAPI REST layer
│   ├── main.py
│   ├── routes/
│   │   ├── agents.py             # /agents/* endpoints
│   │   ├── squads.py             # /squads/* endpoints
│   │   └── health.py             # /health, /metrics
│   └── middleware/
│       ├── auth.py               # License key + API key middleware
│       └── rate_limiter.py
├── tests/                         # All test files live here
│   ├── conftest.py               # Shared fixtures and mock factories
│   ├── test_base_agent.py
│   ├── test_agent_registry.py
│   ├── test_squad_router.py
│   ├── squads/                   # One test file per squad
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
├── demo/
│   ├── run_demo.py               # Full interactive demo (all squads)
│   └── run_squad_demo.py         # Demo a single squad by name
├── scripts/
│   ├── list_agents.py            # Print all 156 agents with squad + status
│   ├── validate_registry.py      # Assert 156 agents registered correctly
│   └── benchmark.py              # Response time benchmarks per squad
├── logs/                         # Auto-created at runtime
│   └── {client_slug}/
│       └── {squad}/
│           └── {agent_slug}/
├── AGENTS.md                     # Coding guidelines for AI agents
├── GHOST_AGENCY.md               # Full business plan
├── README.md                     # This file
├── requirements.txt
└── .env.example
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                  Client Request                  │
│         (email / webhook / API call)             │
└────────────────────┬────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │    Agent Registry       │  ← 156 agents mapped by slug
         │  (support-tier1, etc.)  │
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │    AI Agent Class       │  ← Inherits from AIAgent base
         │  (Squad-specific logic)  │
         └───────────┬───────────┘
                     │
         ┌────────────▼────────────┐
         │   Knowledge Base Loader  │  ← client-specific docs/FAQs
         │     (with chunking)      │
         └────────────┬────────────┘
                     │
         ┌────────────▼────────────┐
         │      LLM Orchestrator    │
         │  NVIDIA NIM → Ollama     │  ← Primary + fallback strategy
         └────────────┬────────────┘
                     │
         ┌────────────▼────────────┐
         │   Structured JSON Logger │  → logs/{client}/{squad}/{agent}/YYYYMMDD.jsonl
         └────────────┬────────────┘
                     │
         ┌────────────▼────────────┐
         │  Escalation Router       │  → email / webhook (if triggered)
         └─────────────────────────┘
```

All 156 AI agents share the same production pipeline. What differs is the **system prompt**, **primary action method**, **squad routing**, and **escalation logic**.

---

## ⚙️ Configuration

All configuration is environment-driven. Copy `.env.example` to `.env` and customize:

```env
# NVIDIA NIM (primary LLM)
NIM_API_KEY=your_nvidia_nim_api_key_here
NIM_BASE_URL=https://integrate.api.nvidia.com/v1
NIM_MODEL=deepseek-ai/deepseek-v3-0324
NIM_TIMEOUT=60

# Ollama (local fallback — CPU-only)
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_TIMEOUT=120

# Agent runtime
GHOST_MOCK_AI=false
GHOST_MAX_RETRIES=3
GHOST_LOG_DIR=logs

# Email (escalation)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password

# Webhook
ESCALATION_WEBHOOK_URL=

# Gumroad (license validation)
GUMROAD_PRODUCT_ID=
GUMROAD_ACCESS_TOKEN=

# Telegram bot (optional)
TELEGRAM_BOT_TOKEN=
```

---

## 🧪 Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=ghostagency --cov-report=term-missing

# Run a specific squad's tests
pytest tests/squads/test_squad_support.py -v

# Run tests matching a keyword
pytest -k "escalation" -v

# Fast test run (mock mode)
GHOST_MOCK_AI=true pytest --tb=short -q

# Registry validation
python scripts/validate_registry.py
```

Coverage requirements:
- Registry, router, base agent: **100%**
- Every `primary_action()`: **100%**
- All other non-demo code: **≥ 80%**

---

## 📦 Deploying for a Client

Each client gets their own configuration and knowledge base:

```bash
# 1. Create client knowledge base
mkdir -p kb/clients/acme_corp/
# Drop PDFs, txt files, FAQs into this folder

# 2. Set client-specific env
CLIENT_NAME="Acme Corp" \
KB_PATH="kb/clients/acme_corp/" \
ESCALATION_EMAIL="support@acmecorp.com" \
python ghost_agency_employees.py

# 3. Logs auto-appear at:
ls logs/acme_corp/
```

To run multiple clients on one VPS, use **systemd** or **supervisord** to manage separate processes per client — each with its own `.env` file.

---

## 💰 Business Snapshot

```
Your monthly cost per client:   $6–$11
Your monthly charge per client: $500–$2,000
Your margin:                    ~95%

10 clients = $10,000/mo revenue, $80/mo cost
50 clients = $50,000/mo revenue, $400/mo cost
```

Full business plan, pricing strategy, sales scripts, and 90-day execution plan: see `GHOST_AGENCY.md`.

---

## 🔒 Security

- Never commit `.env` — only `.env.example` belongs in version control
- All secrets are loaded from environment variables
- Customer data in logs is automatically redacted (emails, phone numbers)
- Rate limiting is configurable per employee via `MAX_REQUESTS_PER_MINUTE` in config

---

## 🆘 Troubleshooting

**NIM Connection Error:**
```bash
# Verify NIM connection
python -c "from ghostagency.integrations.nim_client import NIMClient; c = NIMClient(); print(c.ping())"

# Check NIM_API_KEY is set in .env
```

**Ollama not responding:**
```bash
ollama serve              # Start the service
curl http://localhost:11434/api/tags  # Verify it's running
```

**Agent not found:**
```bash
# List all registered agents
python scripts/list_agents.py

# Validate registry
python scripts/validate_registry.py
```

**Tests failing with connection errors:**
```bash
GHOST_MOCK_AI=true pytest   # Run in mock mode
```

**Registry validation fails:**
```bash
# Check for missing agents
python scripts/validate_registry.py

# Must have exactly 156 agents in registry
```

---

## 🛠️ Development Workflow

```bash
# Full pre-commit sequence
black . --line-length 100 && flake8 . --max-line-length 100 && pytest --tb=short -q

# Format
black . --line-length 100

# Lint
flake8 . --max-line-length 100 --exclude .venv,__pycache__,logs

# Type check
mypy ghostagency/core/ ghostagency/agents/ --ignore-missing-imports

# Test
pytest --tb=short -q

# Verify demo
GHOST_MOCK_AI=true python demo/run_demo.py

# Validate registry
python scripts/validate_registry.py
```

For AI coding agents: see `AGENTS.md` for the full spec, architecture contracts, and agent decision rules.

---

## 📚 Resources

- [Ollama Documentation](https://ollama.ai)
- [DeepSeek Models](https://ollama.com/library/deepseek-r1)
- [opencode Documentation](https://opencode.ai)
- [Python Requests](https://docs.python-requests.org)
- [pytest Documentation](https://docs.pytest.org)
- [Black Formatter](https://black.readthedocs.io)

---

## 🤝 Contributing & Extending

1. Read `AGENTS.md` fully before writing any code — it's the source of truth
2. Write tests before implementation (TDD)
3. Every new agent must inherit from `AIAgent` base class
4. All config goes in `.env` — nothing hardcoded
5. Keep `demo/run_demo.py` working at all times
6. Registry must always contain exactly 156 agents

To add a new AI agent:
1. Create the agent file in the correct squad directory
2. Implement the class (inherit AIAgent, set all class attrs)
3. Add to squad `__init__.py`
4. Register in `agent_registry.py`
5. Validate count: `python scripts/validate_registry.py`
6. Write tests in the appropriate squad test file
7. Update demo if needed

---

## 📊 Current Status

**Phase 1 (Core Infrastructure):** ✅ Completed  
**Agents Implemented:** 1/156 (Support Tier 1)  
**Test Coverage:** 100% on core components  
**Production Ready:** NVIDIA NIM + Ollama fallback  

**Next Up:** Phase 2 (Agent Migration) - Migrating remaining 3 existing agents

---

*Ghost Agency — Production-grade multi-tenant AI agent platform for solo operators.*
