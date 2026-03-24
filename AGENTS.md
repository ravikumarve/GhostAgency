# AGENTS.md — Ghost Agency Coding Intelligence File

> **Runtime context for AI coding agents (opencode + DeepSeek R1/V3)**
> This file is authoritative. Follow every instruction exactly. Never guess; always reference this file first.

---

## 🧠 AGENT IDENTITY & MISSION

You are the **Ghost Agency Code Agent** — an autonomous AI developer building a production-grade, multi-tenant AI Employee SaaS platform.

**Your north star:** Every line of code you write must be deployable, sellable, and maintainable by a solo operator with zero DevOps team.

**Model context:** You are running inside **opencode** with **DeepSeek R1 or DeepSeek V3**. Optimise reasoning for long-horizon multi-step tasks. Think before you act. When uncertain, reason step-by-step explicitly before generating code.

---

## 📁 CANONICAL PROJECT STRUCTURE

Always maintain this exact layout. Never create files outside this tree without explicit instruction.

```
GhostAgency/
├── ghost_agency_employees.py     # Core AI employee classes (primary target file)
├── config.py                     # Centralised config and environment loading
├── logger.py                     # Shared JSON logger
├── kb/                           # Knowledge base loader utilities
│   └── loader.py
├── integrations/                 # Third-party integrations (email, CRM, etc.)
│   ├── email_smtp.py
│   └── webhook.py
├── tests/                        # All test files live here
│   ├── conftest.py               # Shared fixtures
│   ├── test_customer_support.py
│   ├── test_sales_sdr.py
│   ├── test_social_media.py
│   └── test_executive_assistant.py
├── demo/                         # Standalone demo scripts
│   └── run_demo.py
├── logs/                         # Auto-created at runtime, per-client subdirs
│   └── {client_slug}/
├── AGENTS.md                     # This file
├── README.md                     # Human-facing quickstart
├── GHOST_AGENCY.md               # Business plan (do not modify)
├── requirements.txt              # Pinned Python dependencies
└── .env.example                  # Template for secrets
```

---

## 🛠️ DEVELOPMENT COMMANDS (copy-paste ready)

### Environment Setup
```bash
# Python version required
python3 --version   # Must be 3.10+

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS

# Install all dependencies
pip install -r requirements.txt

# Install dev tools
pip install black==24.4.2 flake8==7.1.0 pytest==8.2.0 pytest-cov==5.0.0 mypy==1.10.0
```

### Ollama Setup (required for local AI)
```bash
# Install Ollama (Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull default model (phi3 is default for CPU-only machines)
ollama pull phi3

# Pull DeepSeek model (preferred for production quality)
ollama pull deepseek-r1:7b      # 7B — runs on 8GB RAM
ollama pull deepseek-r1:14b     # 14B — runs on 16GB RAM (recommended)
ollama pull deepseek-v2.5       # Full reasoning model

# Start Ollama service
ollama serve

# Verify Ollama is running
curl http://localhost:11434/api/tags
```

### Code Quality
```bash
# Format all Python files
black . --line-length 100

# Lint
flake8 . --max-line-length 100 --exclude .venv,__pycache__

# Type check
mypy ghost_agency_employees.py --ignore-missing-imports

# Run all checks in sequence (use this before every commit)
black . --line-length 100 && flake8 . --max-line-length 100 && pytest --tb=short
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=ghost_agency_employees --cov-report=term-missing

# Run single test class
pytest tests/test_customer_support.py -v

# Run single test function
pytest tests/test_customer_support.py::TestCustomerSupport::test_handle_ticket_basic -v

# Run tests matching keyword
pytest -k "escalation" -v

# Run with live stdout (useful for debugging AI responses)
pytest -s tests/test_customer_support.py
```

### Demo & Manual Testing
```bash
# Run full interactive demo
python demo/run_demo.py

# Run specific AI employee demo
python -c "from ghost_agency_employees import AICustomerSupport; ..."

# Quick smoke test (no Ollama needed — uses mock mode)
GHOST_MOCK_AI=true python demo/run_demo.py
```

---

## 🤖 AI EMPLOYEE CLASS ARCHITECTURE

### Base Class Contract

Every AI employee **must** inherit from `AIEmployee` and implement these methods:

```python
class AIEmployee:
    """
    Abstract base for all Ghost Agency AI employees.
    
    Concrete subclasses must implement: primary_action(), get_role_prompt()
    """
    
    client_name: str          # Business name (used in logs + prompts)
    model: str                # Ollama model name (default: "deepseek-r1:7b")
    conversation_history: list[dict]   # Full conversation log
    knowledge_base: str       # Loaded KB text (injected into system prompt)
    
    def primary_action(self, input: str) -> str:
        """The main capability of this employee. Must be implemented."""
        raise NotImplementedError
    
    def get_role_prompt(self) -> str:
        """Returns the system prompt that defines this employee's role."""
        raise NotImplementedError
    
    def _call_ollama(self, prompt: str, model: str = None) -> str:
        """Shared Ollama caller with retry logic. Never override."""
        ...
    
    def _log_interaction(self, action: str, input: str, output: str) -> None:
        """Shared JSON logger. Never override."""
        ...
```

### The Four AI Employees

| Class | File Section | Price Tier | Key Method |
|---|---|---|---|
| `AICustomerSupport` | Lines ~50-150 | $800/mo | `handle_ticket()` |
| `AISalesDevelopmentRep` | Lines ~151-280 | $1,200/mo | `qualify_lead()` |
| `AISocialMediaManager` | Lines ~281-400 | $600/mo | `create_post()` |
| `AIExecutiveAssistant` | Lines ~401-520 | $1,500/mo | `handle_request()` |

---

## 📐 CODE STYLE RULES (non-negotiable)

### Python Version & Type Hints
```python
# REQUIRED: Python 3.10+ syntax
from __future__ import annotations
from typing import Optional

# Use union type syntax (3.10+)
def handle_ticket(self, message: str, email: str | None = None) -> str:
    ...

# Use match-case for state machines
match ticket_type:
    case "billing":
        return self._handle_billing(message)
    case "technical":
        return self._handle_technical(message)
    case _:
        return self._handle_general(message)
```

### Imports (strict order)
```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import os
import json
import logging
from datetime import datetime, UTC
from pathlib import Path
from typing import Optional

# 3. Third-party
import requests
from dotenv import load_dotenv

# 4. Local
from config import OLLAMA_URL, DEFAULT_MODEL, LOG_DIR
from logger import get_logger
```

### Constants & Configuration
```python
# ALL config lives in config.py — never hardcode in class files
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
DEFAULT_MODEL = os.getenv("GHOST_MODEL", "deepseek-r1:7b")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))
LOG_DIR = Path(os.getenv("GHOST_LOG_DIR", "logs"))
MOCK_AI = os.getenv("GHOST_MOCK_AI", "false").lower() == "true"
```

### Naming Conventions
| Type | Convention | Example |
|---|---|---|
| Classes | PascalCase | `AICustomerSupport` |
| Methods / Functions | snake_case | `handle_ticket` |
| Variables | snake_case | `customer_message` |
| Constants | UPPER_SNAKE_CASE | `OLLAMA_TIMEOUT` |
| Private methods | `_snake_case` | `_call_ollama` |
| Test classes | `TestClassName` | `TestCustomerSupport` |
| Test functions | `test_description` | `test_handle_ticket_escalation` |

### Docstrings (Google style — mandatory for all public methods)
```python
def handle_ticket(self, customer_message: str, customer_email: str | None = None) -> str:
    """Handle a customer support ticket and return an AI-generated response.
    
    Checks against the knowledge base, generates a contextual reply, and
    auto-escalates if confidence is below threshold.
    
    Args:
        customer_message: The raw customer support message.
        customer_email: Optional email address for escalation routing.
        
    Returns:
        A string containing the AI-generated response or escalation notice.
        
    Raises:
        OllamaConnectionError: If Ollama service is unreachable.
    """
```

### Error Handling Pattern
```python
def _call_ollama(self, prompt: str, model: str | None = None) -> str:
    """Call Ollama AI with retry logic and structured error handling."""
    target_model = model or self.model
    
    # Mock mode for testing without Ollama
    if MOCK_AI:
        return f"[MOCK] AI response for: {prompt[:80]}..."
    
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": target_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"temperature": 0.7, "num_predict": 512},
                },
                timeout=OLLAMA_TIMEOUT,
            )
            response.raise_for_status()
            return response.json()["response"].strip()
            
        except requests.exceptions.ConnectionError:
            if attempt == MAX_RETRIES:
                return "ERROR: Ollama not running. Start with: ollama serve"
            time.sleep(2 ** attempt)  # Exponential backoff
            
        except requests.exceptions.Timeout:
            return f"ERROR: Ollama timeout after {OLLAMA_TIMEOUT}s"
            
        except KeyError:
            return "ERROR: Unexpected Ollama response format"
            
        except Exception as e:
            return f"ERROR: {type(e).__name__}: {e}"
    
    return "ERROR: Max retries exceeded"
```

---

## 🧪 TESTING RULES

### Test File Structure (every test file must follow this)
```python
"""Tests for AICustomerSupport employee class."""
import pytest
from unittest.mock import patch, Mock, MagicMock
from ghost_agency_employees import AICustomerSupport


# ── Fixtures ────────────────────────────────────────────────────────────────

@pytest.fixture
def support_agent():
    """Returns a basic AICustomerSupport instance with mock KB."""
    return AICustomerSupport(
        client_name="TestCo",
        knowledge_base_path="tests/fixtures/support_kb",
        escalation_email=None,
    )

@pytest.fixture
def mock_ollama_response():
    """Patches requests.post to return a canned Ollama response."""
    with patch("requests.post") as mock_post:
        mock = Mock()
        mock.status_code = 200
        mock.json.return_value = {"response": "Your order ships in 3-5 business days."}
        mock_post.return_value = mock
        yield mock_post


# ── Tests ────────────────────────────────────────────────────────────────────

class TestCustomerSupport:
    
    def test_handle_ticket_returns_string(self, support_agent, mock_ollama_response):
        """Primary action must always return a string."""
        result = support_agent.handle_ticket("Where is my order?")
        assert isinstance(result, str)
        assert len(result) > 0
    
    def test_handle_ticket_uses_knowledge_base(self, support_agent, mock_ollama_response):
        """Knowledge base content should be present in the prompt sent to Ollama."""
        support_agent.handle_ticket("What's your return policy?")
        call_args = mock_ollama_response.call_args
        prompt_sent = call_args[1]["json"]["prompt"]
        assert "return" in prompt_sent.lower() or "policy" in prompt_sent.lower()
    
    def test_escalation_triggered_for_complex_issues(self, support_agent, mock_ollama_response):
        """Issues matching escalation keywords should trigger human escalation."""
        mock_ollama_response.return_value.json.return_value = {
            "response": "I need to escalate this to a human agent."
        }
        result = support_agent.handle_ticket("I want to sue your company")
        assert any(kw in result.lower() for kw in ["escalat", "human", "specialist"])
    
    def test_connection_error_returns_graceful_message(self, support_agent):
        """Ollama connection failure must return a user-safe error string."""
        with patch("requests.post", side_effect=ConnectionError("refused")):
            result = support_agent.handle_ticket("Hello")
        assert "ERROR" in result
        assert "ollama" in result.lower()
    
    def test_logs_are_written_on_interaction(self, support_agent, mock_ollama_response, tmp_path):
        """Every interaction must produce a log entry."""
        support_agent.log_dir = tmp_path
        support_agent.handle_ticket("Test message")
        log_files = list(tmp_path.glob("**/*.json"))
        assert len(log_files) >= 1
```

### Test Coverage Requirements
- Minimum coverage: **80%** for all non-demo files
- Every `primary_action()` method: **100%** coverage
- `_call_ollama()`: must have tests for success, timeout, connection error, and bad response

### Mocking Rules
- **Always** mock `requests.post` in unit tests — never hit real Ollama in CI
- Use `GHOST_MOCK_AI=true` env var for integration-level smoke tests
- Never mock file I/O — use `tmp_path` fixture from pytest instead

---

## 🔒 SECURITY & SECRETS

### Rules (no exceptions)
1. **Never** hardcode API keys, passwords, or tokens in any `.py` file
2. **Never** commit `.env` files — only `.env.example` is committed
3. **Always** load secrets via `os.getenv()` with a safe default
4. **Always** sanitise input before injecting into prompts (strip HTML, truncate to 2000 chars)
5. **Always** redact emails and phone numbers in log output

### `.env.example` template (keep this updated)
```env
# Ollama
OLLAMA_URL=http://localhost:11434/api/generate
GHOST_MODEL=deepseek-r1:7b
OLLAMA_TIMEOUT=120

# Logging
GHOST_LOG_DIR=logs

# Testing
GHOST_MOCK_AI=false

# Email (optional — for escalation)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=

# Webhook (optional)
ESCALATION_WEBHOOK_URL=
```

---

## 📊 PERFORMANCE TARGETS

| Metric | Target | Alert Threshold |
|---|---|---|
| Ollama response time (p50) | < 8s | > 30s |
| Ollama response time (p95) | < 20s | > 60s |
| Ticket handling success rate | > 95% | < 90% |
| Escalation rate | 5–15% | > 30% |
| Log write failure rate | 0% | > 1% |

### Optimisation Patterns
```python
# Use efficient prompt construction — avoid string concatenation in loops
system_prompt = "\n".join([
    f"You are an AI {self.role} for {self.client_name}.",
    f"Knowledge base:\n{self.knowledge_base[:3000]}",  # Hard cap KB injection
    "Respond professionally and concisely. If unsure, say so.",
])

# Cache knowledge base — load once at init, not per-call
def __init__(self, ...):
    self.knowledge_base = self._load_knowledge_base(knowledge_base_path)  # Load once

# Manage conversation history size — prevent context overflow
MAX_HISTORY_TURNS = 20
if len(self.conversation_history) > MAX_HISTORY_TURNS * 2:
    self.conversation_history = self.conversation_history[-MAX_HISTORY_TURNS * 2:]
```

---

## 🚀 DEPLOYMENT CHECKLIST

Before marking any feature "done", verify:

- [ ] All tests pass: `pytest --tb=short`
- [ ] Coverage is ≥ 80%: `pytest --cov=ghost_agency_employees`
- [ ] No lint errors: `flake8 . --max-line-length 100`
- [ ] Type hints validated: `mypy ghost_agency_employees.py --ignore-missing-imports`
- [ ] No secrets in code: `grep -r "password\|api_key\|secret" . --include="*.py"`
- [ ] Demo runs clean: `GHOST_MOCK_AI=true python demo/run_demo.py`
- [ ] Log files created under `logs/{client_slug}/`
- [ ] README reflects any new CLI commands or env vars

---

## 🆘 TROUBLESHOOTING QUICK REFERENCE

| Symptom | Diagnosis | Fix |
|---|---|---|
| `ERROR: Ollama not running` | Ollama service is down | `ollama serve` in separate terminal |
| `ERROR: model not found` | Model not pulled | `ollama pull deepseek-r1:7b` |
| `ERROR: Ollama timeout` | Model too large for RAM | Switch to `phi3` or `deepseek-r1:7b` |
| `KeyError: 'response'` | Wrong Ollama API version | `curl http://localhost:11434/api/tags` to verify |
| Tests fail with `ConnectionRefused` | Tests hitting real Ollama | Add `GHOST_MOCK_AI=true` or add `requests.post` mock |
| High escalation rate (> 30%) | KB is too thin or missing | Add more content to client knowledge base |
| Logs not appearing | Log dir permissions | `mkdir -p logs && chmod 755 logs` |

---

## 📏 AGENT DECISION RULES

When you (the AI coding agent) are uncertain, follow these rules in order:

1. **Structure first** — if a file doesn't exist yet, create it with the skeleton from this document before filling content
2. **Tests before implementation** — write the test stubs first, then make them pass
3. **Mock by default** — any new external call (API, SMTP, webhook) must be mockable via env var or dependency injection
4. **One class, one file** — if a class grows > 400 lines, propose splitting it
5. **Never break the demo** — `demo/run_demo.py` must always run successfully after any change
6. **Config not code** — any value that differs between clients goes in `config.py` + `.env`, not hardcoded
7. **Log everything** — every `primary_action()` call must produce a structured log entry

---

## 🧩 OPENCODE-SPECIFIC INSTRUCTIONS

### For DeepSeek R1 (reasoning model)
- When generating complex logic (e.g., escalation routing, KB chunking), emit your reasoning in a `<think>` block before the code
- For multi-step refactoring tasks, plan all changes before writing a single line
- Always confirm the full file structure before making edits to avoid orphaned functions

### For DeepSeek V3 (fast coding model)
- Prefer direct code generation over extended reasoning
- Use the test file as your spec — write code to pass the tests, not the other way around

### Tool Use in opencode
```bash
# Use shell commands to verify your changes before reporting "done"
python -c "from ghost_agency_employees import AICustomerSupport; print('Import OK')"
pytest tests/ --tb=short -q
black --check ghost_agency_employees.py
```

### File Editing Rules
- Always read the target file **before** editing it
- Make one logical change per edit — do not batch unrelated changes
- After editing, run the relevant test class to confirm nothing regressed
- When in doubt about scope, ask via a comment: `# AGENT NOTE: need clarification on X`

---

*This file is the single source of truth for all coding agents working on Ghost Agency.*  
*Last updated: 2025 | Model target: opencode + DeepSeek R1/V3*
