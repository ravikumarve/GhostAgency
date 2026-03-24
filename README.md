# 👻 Ghost Agency — AI Employee Templates

> **Deploy AI workers. Charge $500–$2,000/month. Keep 95% margin.**  
> Built for solo operators. Runs on a single VPS. Powered by Ollama + DeepSeek.

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

## 🤖 The AI Employee Roster

| Employee | What They Do | Price |
|---|---|---|
| **AI Customer Support Agent** | Answers tickets 24/7, trained on client KB, escalates edge cases | $800/mo |
| **AI Sales Development Rep** | Qualifies leads, writes follow-up emails, books meetings | $1,200/mo |
| **AI Social Media Manager** | Creates daily posts, responds to DMs, tracks engagement | $600/mo |
| **AI Executive Assistant** | Drafts emails, summarises meetings, manages calendar tasks | $1,500/mo |

---

## ⚡ Quickstart (10 minutes to first demo)

### 1. Prerequisites

```bash
# Python 3.10 or higher required
python3 --version

# Install Ollama (Linux)
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Pull Your AI Brain

```bash
# Recommended: DeepSeek (high quality, runs on 8–16GB RAM)
ollama pull deepseek-r1:7b      # 8GB RAM minimum
ollama pull deepseek-r1:14b     # 16GB RAM — better quality

# Fallback: phi3 (lightweight, 4GB RAM)
ollama pull phi3
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
# Edit .env to set GHOST_MODEL=deepseek-r1:7b (or your preferred model)
```

### 4. Start Ollama & Run Demo

```bash
# Terminal 1: start Ollama
ollama serve

# Terminal 2: run the demo
python demo/run_demo.py
```

You should see all four AI employees respond to sample inputs within ~30 seconds.

### 5. Test Without Ollama (CI / fast iteration)

```bash
# Mock mode skips Ollama entirely — instant responses for testing
GHOST_MOCK_AI=true python demo/run_demo.py
GHOST_MOCK_AI=true pytest
```

---

## 📁 Project Structure

```
GhostAgency/
├── ghost_agency_employees.py     # Core AI employee classes
├── config.py                     # All configuration + env loading
├── logger.py                     # Shared JSON interaction logger
├── kb/
│   └── loader.py                 # Knowledge base file loader
├── integrations/
│   ├── email_smtp.py             # SMTP email for escalations
│   └── webhook.py                # Generic webhook dispatcher
├── tests/
│   ├── conftest.py               # Shared pytest fixtures
│   ├── test_customer_support.py
│   ├── test_sales_sdr.py
│   ├── test_social_media.py
│   └── test_executive_assistant.py
├── demo/
│   └── run_demo.py               # Interactive demo runner
├── logs/                         # Per-client interaction logs (auto-created)
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
         │    AI Employee Class   │
         │  (Customer Support /   │
         │   Sales / Social /     │
         │   Executive)           │
         └───────────┬───────────┘
                     │
        ┌────────────▼────────────┐
        │   Knowledge Base Loader  │  ← client-specific docs/FAQs
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │       Ollama API         │  ← local AI (DeepSeek / phi3)
        │  http://localhost:11434  │
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │   Structured Logger      │  → logs/{client}/YYYY-MM-DD.json
        └────────────┬────────────┘
                     │
        ┌────────────▼────────────┐
        │  Escalation Router       │  → email / webhook (if triggered)
        └─────────────────────────┘
```

All four AI employees share the same pipeline. What differs is the **system prompt**, **primary action method**, and **escalation logic**.

---

## ⚙️ Configuration

All configuration is environment-driven. Copy `.env.example` to `.env` and customise:

```env
# AI Model (change this to match what you've pulled in Ollama)
GHOST_MODEL=deepseek-r1:7b

# Ollama endpoint (default works for local setup)
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_TIMEOUT=120

# Logging
GHOST_LOG_DIR=logs

# Testing — set to true to skip Ollama for fast test runs
GHOST_MOCK_AI=false

# Email escalation (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASS=your_app_password
```

---

## 🧪 Testing

```bash
# Run full test suite
pytest

# With coverage report
pytest --cov=ghost_agency_employees --cov-report=term-missing

# Run a specific employee's tests
pytest tests/test_customer_support.py -v

# Fast test run (no Ollama needed)
GHOST_MOCK_AI=true pytest -q
```

Coverage target: **80% minimum** across all non-demo files.

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

**Ollama not responding:**
```bash
ollama serve              # Start the service
curl http://localhost:11434/api/tags  # Verify it's running
```

**Model not found:**
```bash
ollama list               # See installed models
ollama pull deepseek-r1:7b  # Pull your chosen model
```

**Tests failing with connection errors:**
```bash
GHOST_MOCK_AI=true pytest   # Run without Ollama
```

**Out of memory / model too slow:**
Switch to a smaller model in `.env`:
```env
GHOST_MODEL=phi3     # Runs on 4GB RAM, very fast
```

---

## 🛠️ Development Workflow

```bash
# 1. Make your changes
# 2. Format
black . --line-length 100
# 3. Lint
flake8 . --max-line-length 100
# 4. Test
pytest --tb=short
# 5. Verify demo still works
GHOST_MOCK_AI=true python demo/run_demo.py
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

1. Read `AGENTS.md` fully before writing any code
2. Write tests before implementation (TDD)
3. Every new AI employee must inherit from `AIEmployee` base class
4. All config goes in `.env` / `config.py` — nothing hardcoded
5. Keep `demo/run_demo.py` working at all times

To add a new AI employee type:
1. Add the class to `ghost_agency_employees.py`
2. Add tests to `tests/test_{employee_name}.py`
3. Add demo block to `demo/run_demo.py`
4. Update the roster table in this README

---

*Ghost Agency — Built for solo operators who want to run a high-margin AI business without a team.*
