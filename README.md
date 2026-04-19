# 👻 Ghost Agency — Your AI Employee Platform

> **Rent AI employees to businesses for $500–$2,500/month**  
> **Your cost: $6–$11/month per client → 95% profit margin**  
> **No coding required to get started**

---

## 🎯 For Non-Technical Users: What This Actually Does

**Ghost Agency lets you deploy specialized AI "employees" that businesses pay you for monthly.**

### 🤔 Imagine This:
- A small business pays you **$800/month** for an AI customer support agent
- The AI handles customer questions 24/7 via email and chat
- Your monthly cost to run this AI: **$8**
- Your profit: **$792/month**
- Scale to 10 clients: **$7,920/month profit**

### 🎪 You're Not Selling Software
You're renting **AI employees** that handle real business tasks:
- 🤝 Customer support tickets
- 📞 Sales calls and lead qualification  
- 📱 Social media management
- 📊 Data analysis and reporting
- 📅 Executive assistance
- And 150+ other specialized roles

### 💰 The Business Model (Simplified)
```
What you charge client: $500–$2,500/month
Your actual cost:       $6–$11/month  
Your profit margin:     95–99%
```

**This isn't a side hustle — it's a proper agency business with AI employees instead of humans.**

---

## 🚀 What You Can Do Today (No Technical Knowledge Needed)

### 1. 🎥 Watch the Demo
```bash
# Just run this one command to see it working
PYTHONPATH=. GHOST_MOCK_AI=true python ghostagency/demo/run_demo.py
```

### 2. 💰 Calculate Your Potential Income
| Clients | Monthly Revenue | Your Cost | Your Profit |
|---------|----------------|-----------|-------------|
| 5 clients | $5,000 | $40 | $4,960 |
| 10 clients | $10,000 | $80 | $9,920 |
| 20 clients | $20,000 | $160 | $19,840 |
| 50 clients | $50,000 | $400 | $49,600 |

### 3. 📋 Choose Your First AI Employee
Start with one of these easy-to-sell roles:
- **Support Agent** ($600–900/month) - Handles customer tickets
- **Social Media Manager** ($500–800/month) - Creates and schedules posts
- **Sales Development Rep** ($900–1,500/month) - Qualifies leads and makes calls

### 4. 🎯 Find Your First Client
- Local businesses needing customer support
- E-commerce stores with high ticket volume  
- Agencies that need additional capacity
- Startups that can't afford full-time staff

---

## 🏢 Meet Your AI Workforce (6 Specialized Employees - Growing Daily!)

| Department | 👥 Employee Count | 💵 Monthly Price | What They Do |
|------------|------------------|------------------|-------------|
| **🤝 Support** | 3 agents | $600–900 | Handle tickets, billing, technical help |
| **📈 Sales** | 1 agent | $900–1,500 | Qualify leads, cold outreach, deal strategy |
| **📱 Content** | 1 agent | $500–800 | Social media, blog writing, SEO optimization |
| **⚙️ Operations** | 1 agent | $1,200–2,000 | Executive assistance, scheduling, projects |
| **📊 Data** | 0 agents | Coming Soon | Research, analytics, reporting, insights |
| **💻 Development** | 0 agents | Coming Soon | Code review, technical support, QA testing |
| **💰 Finance** | 0 agents | Coming Soon | Invoicing, expense tracking, bookkeeping |
| **👥 HR** | 0 agents | Coming Soon | Recruitment, onboarding, employee engagement |
| **⚖️ Legal** | 0 agents | Coming Soon | Contract review, compliance, NDA management |
| **🎨 Custom** | 0 agents | Custom pricing | Client-specific specialized agents |

**Run this to see current employees:** `PYTHONPATH=. python ghostagency/scripts/list_agents.py`

> 🚀 **We're growing fast!** New agents added weekly based on client demand.

---

## ⚡ Quick Start Guide (10 Minutes to Your First AI Employee)

### 🎯 For Complete Beginners (No Tech Experience)
1. **Watch the demo**: `PYTHONPATH=. GHOST_MOCK_AI=true python ghostagency/demo/run_demo.py`
2. **Pick one AI employee** to start with (Support is easiest)
3. **Find one client** who needs help with customer support
4. **Charge $800/month** - they'll save thousands vs hiring humans

### 🛠️ For Technical Users (Ready to Deploy)

#### 1. Prerequisites
```bash
# Python 3.12 or higher
python3 --version

# Optional: Install Ollama for free local AI
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 2. Get Your AI Keys (Free Options)
- **Option A (Recommended)**: NVIDIA NIM - [Get free API key](https://build.nvidia.com)
- **Option B (Free)**: Ollama - runs locally on your computer

#### 3. Install & Configure
```bash
# Clone the repository
git clone https://github.com/ravikumarve/ghost-agency.git
cd ghost-agency

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env to add your NVIDIA NIM key or configure Ollama
```

#### 4. Run Your First AI Employee
```bash
# With NVIDIA NIM (best performance)
PYTHONPATH=. python ghostagency/demo/run_demo.py

# With Ollama (free, runs locally)
OLLAMA_URL=http://localhost:11434/api/generate PYTHONPATH=. python ghostagency/demo/run_demo.py

# Mock mode (see how it works without AI calls)
PYTHONPATH=. GHOST_MOCK_AI=true python ghostagency/demo/run_demo.py
```

#### 5. Validate Everything Works
```bash
# List all AI employees
PYTHONPATH=. python ghostagency/scripts/list_agents.py

# Check system health
PYTHONPATH=. python ghostagency/scripts/validate_registry.py
```

---

## ⚡ Quick Install

```bash
# After purchasing on Gumroad, clone the repo and run:
bash install.sh
```

> **Note:** The one-liner `curl -sSL https://raw.githubusercontent.com/ravikumarve/GhostAgency/main/install.sh | bash` will work once the repo is made public. For private/Gumroad distribution, clone first then run `bash install.sh`.

---

## 💰 Pricing & ROI Calculator

### 📈 Monthly Business Model
| Metric | Amount | Notes |
|--------|--------|-------|
| **Your charge per client** | $500–$2,500 | Based on AI employee type |
| **Your cost per client** | $6–$11 | Hosting + API costs |
| **Your profit margin** | 95–99% | Industry-best margins |
| **Setup fee** | $1,000–$3,000 | One-time per client |

### 🧮 Profit Calculator
```python
# Example: 10 clients with Support agents
clients = 10
monthly_charge = 800  # per client
monthly_cost = 8      # per client

monthly_revenue = clients * monthly_charge      # $8,000
monthly_expenses = clients * monthly_cost       # $80  
monthly_profit = monthly_revenue - monthly_expenses  # $7,920
```

### 🎯 Who Should Buy This?
- **Agencies** looking to scale without hiring
- **Business owners** tired of customer support costs
- **Freelancers** wanting retainers instead of project work
- **Tech-savvy entrepreneurs** building the future of work

---

## 🏗️ Technical Overview (For Developers)

### 📁 Project Structure
```
GhostAgency/
├── ghostagency/                 # Main package
│   ├── core/                    # Core infrastructure
│   ├── agents/                  # AI employee modules (6+ and growing)
│   ├── kb/                      # Knowledge base system
│   └── integrations/            # Third-party integrations
├── api/                         # REST API layer
├── tests/                       # Comprehensive test suite
├── demo/                        # Live demos
├── scripts/                     # Management utilities
└── logs/                        # Automatic logging
```

### ⚙️ System Architecture

```
Client Request → Agent Registry → AI Employee → Knowledge Base → LLM → Response
```

**Key Components:**
- **Agent Registry**: Maps employees to their capabilities (scales to 156+)
- **Knowledge Base Loader**: Client-specific information and training
- **LLM Orchestrator**: NVIDIA NIM (primary) + Ollama (fallback)
- **Structured Logger**: Automatic logging for every interaction
- **Escalation Router**: Handles complex issues that need human attention

### 🔧 Configuration

All configuration via environment variables (`.env` file):

```env
# NVIDIA NIM (recommended for production)
NIM_API_KEY=your_nvidia_nim_key_here

# Ollama (free local option)
OLLAMA_URL=http://localhost:11434/api/generate

# Client-specific settings
CLIENT_NAME="Client Business Name"
KB_PATH="kb/clients/client_name/"
```

---

## 🧪 Testing & Quality Assurance

### 🎯 Testing Commands
```bash
# Run all tests
pytest

# Test specific department (e.g., Support)
pytest tests/squads/test_squad_support.py -v

# Run in mock mode (fast)
GHOST_MOCK_AI=true pytest --tb=short -q

# Check test coverage
pytest --cov=ghostagency --cov-report=term-missing
```

### ✅ Quality Standards
- **100% test coverage** on core components
- **≥80% coverage** on all other code (currently 47% - improving daily)
- **Zero hardcoded secrets** - everything in `.env`
- **Automatic logging** of every AI interaction
- **Regular registry validation** (ensures agent integrity)

---

## 🚀 Deployment Guide

### 📦 Production Deployment
```bash
# Start the FastAPI server
uvicorn ghostagency.api.main:app --host 0.0.0.0 --port 8000
```

For multi-client setups, run one instance per client with separate `.env` files, or use a reverse proxy (nginx/caddy) to route by domain.

---

## 🛠️ Development & Customization

### 🔧 Adding New AI Employees

```python
# 1. Create employee file in correct department
# ghostagency/agents/squad_support/support_new_role.py

from ghostagency.core.base_agent import AIAgent

class SupportNewRoleAgent(AIAgent):
    """New support employee description"""
    agent_slug = "support-new-role"
    squad = "support"
    display_name = "Support New Role"
    price_tier = "$700/mo"
    
    def primary_action(self, input: str) -> str:
        """Main capability of this employee"""
        return self._call_llm(f"Handle this support request: {input}")
```

### 📋 Registry Management

The system is designed to scale to **156+ AI employees** and currently has 6:

```bash
# List all employees
PYTHONPATH=. python ghostagency/scripts/list_agents.py

# Validate registry integrity
PYTHONPATH=. python ghostagency/scripts/validate_registry.py

# Expected output: "Registry validated: 6 agents found"
```

---

## 🆘 Troubleshooting & Support

### ❓ Common Issues

**"NIM Connection Error"**
```bash
# Check your NVIDIA NIM API key
PYTHONPATH=. python -c "from ghostagency.integrations.nim_client import NIMClient; c = NIMClient(); print(c.ping())"
```

**"Ollama not working"**
```bash
# Start Ollama service
ollama serve

# Verify it's running
curl http://localhost:11434/api/tags
```

**"Employee not found"**
```bash
# List all registered employees
PYTHONPATH=. python ghostagency/scripts/list_agents.py

# Validate registry
PYTHONPATH=. python ghostagency/scripts/validate_registry.py
```

### 📞 Getting Help

1. **Check the demo**: `PYTHONPATH=. GHOST_MOCK_AI=true python ghostagency/demo/run_demo.py`
2. **Validate registry**: `PYTHONPATH=. python ghostagency/scripts/validate_registry.py`
3. **Check logs**: Look in `logs/{client_name}/` for detailed error information
4. **Run tests**: `pytest --tb=short -q` to identify issues

---

## 📚 Learning Resources

- **[Ollama Documentation](https://ollama.ai)** - Free local AI setup
- **[NVIDIA NIM](https://build.nvidia.com)** - Production-grade AI API
- **[Full Business Plan](GHOST_AGENCY.md)** - Detailed pricing, marketing, sales strategies
- **[Developer Guide](AGENTS.md)** - Technical architecture and coding standards

---

## 🎯 Current Status

**✅ Phase 1 (Core Infrastructure)**: Completed  
**🤖 AI Employees Ready**: 6/156 (Multiple squads) - **New agents added weekly!**  
**🧪 Test Coverage**: 100% on core components + 47% overall (improving daily)  
**🚀 Production Ready**: NVIDIA NIM + Ollama fallback

**🔜 Next Phase**: Expanding based on client demand - tell us what you need!

---

## 💡 Why This Works

### 🏆 Competitive Advantages
1. **95% Profit Margins** - Unbeatable economics
2. **24/7 Availability** - AI never sleeps or takes breaks
3. **Instant Scaling** - Add clients without hiring
4. **Zero Overhead** - No office, equipment, or benefits
5. **Happy Clients** - Professional service at fraction of human cost

### 🎯 Perfect For
- **Digital agencies** looking to productize services
- **Freelancers** transitioning to recurring revenue
- **Tech entrepreneurs** building AI-first businesses
- **Business consultants** with existing client networks

---

**Ghost Agency** — Turn AI into your invisible workforce. Start with 6 proven agents, expand as you grow.