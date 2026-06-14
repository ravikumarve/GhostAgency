# Ghost Agency

**AI employee platform** — deploy specialized AI agents for businesses at $500–$2,500/mo per seat. Built for solo operators and agencies.

[Business plan](GHOST_AGENCY.md) · [Developer guide](AGENTS.md) · [Demo](#quick-start)

---

## Quick Start

```bash
git clone https://github.com/ravikumarve/GhostAgency.git
cd GhostAgency
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # add your NIM API key

# Run the demo (mock mode, no AI calls needed)
PYTHONPATH=. GHOST_MOCK_AI=true python ghostagency/demo/run_demo.py
```

See all available agents:
```bash
PYTHONPATH=. python ghostagency/scripts/list_agents.py
```

---

## AI Workforce

| Department | Agents | Price/mo | Capability |
|---|---|---|---|
| Support | 3 | $600–900 | Tickets, billing, technical help |
| Sales | 1 | $900–1,500 | Lead qualification, outreach |
| Content | 1 | $500–800 | Social media, blog, SEO |
| Operations | 1 | $1,200–2,000 | EA, scheduling, projects |
| Data | — | Coming soon | Research, analytics, reporting |
| Dev | — | Coming soon | Code review, QA, technical support |
| Finance | — | Coming soon | Invoicing, expense tracking |
| HR | — | Coming soon | Recruitment, onboarding |
| Legal | — | Coming soon | Contract review, compliance |
| Custom | — | Custom | Client-specific agents |

**Current total: 6 agents** — built to scale to 156+ specialized roles.

---

## Architecture

```
Client → Agent Registry → AI Agent → Knowledge Base → LLM → Response
```

| Layer | Technology |
|---|---|
| LLM | NVIDIA NIM (GLM 5.1) primary · Ollama fallback |
| API | FastAPI · REST · async |
| Auth | License key + API key middleware |
| Rate limiting | In-memory per-key throttling |
| Logging | Structured JSON per interaction |
| Packaging | Install script · `.env.example` · LICENSE |

### Config

All via `.env`:

```env
NIM_API_KEY=your_key_here
OLLAMA_URL=http://localhost:11434/api/generate
GHOST_MOCK_AI=false
```

---

## Production

```bash
uvicorn ghostagency.api.main:app --host 0.0.0.0 --port 8000
```

---

## Testing

```bash
pytest                                # all tests
pytest --cov=ghostagency              # with coverage
pytest tests/squads/test_squad_support.py -v  # single squad
```

---

## Adding Agents

Create a new agent in the appropriate `squad_*` directory, register it in `ghostagency/core/agent_registry.py`, and validate:

```bash
python ghostagency/scripts/validate_registry.py
```

See [AGENTS.md](AGENTS.md) for full development guide.

---

## Install

```bash
# After cloning:
bash install.sh
```

---

## Status

- **6 agents** deployed across 4 squads
- **51/51 tests** passing
- **Core coverage** 100% · Overall 47%
- **Ready** for single-tenant deployment

---

*Ghost Agency — Turn AI into your invisible workforce.*
