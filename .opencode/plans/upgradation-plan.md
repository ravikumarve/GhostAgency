# Ghost Agency Upgradation Plan

## 🔄 Current Status vs Target Architecture

### Current Implementation (Legacy)
- Single `ghost_agency_employees.py` file with 4 AI employee classes
- Basic Ollama integration only
- Simple file-based knowledge base loading
- Limited error handling and logging
- No proper testing framework

### Target Architecture (Production-Ready)
- **156 specialized agents** across 10 functional squads
- **NVIDIA NIM primary** + Ollama fallback LLM strategy
- **Structured JSON logging** with client/agent separation
- **Complete test suite** with 100% coverage requirements
- **FastAPI REST API** for multi-tenant SaaS deployment

## 📋 Upgradation Phases

### Phase 1: Core Infrastructure (COMPLETED)
✅ Created `ghostagency/` directory structure  
✅ Implemented `AIAgent` abstract base class  
✅ Set up NVIDIA NIM client integration  
✅ Added Ollama fallback client  
✅ Structured JSON logging system  
✅ Knowledge base loader with chunking  
✅ Configuration management (.env-based)  
✅ Exception hierarchy  
✅ Registry system with validation  

### Phase 2: Agent Migration (Next)
1. **Migrate existing 4 agents** to new architecture:
   - `AICustomerSupport` → `SupportTier1Agent` (DONE)
   - `AISalesDevelopmentRep` → `SalesQualificationAgent` 
   - `AISocialMediaManager` → `ContentSocialMediaAgent`
   - `AIExecutiveAssistant` → `OpsExecutiveAssistantAgent`

2. **Implement proper squad structure**:
   - Create agent files in correct squad directories
   - Add to registry with proper slugs
   - Set class attributes (squad, display_name, price_tier)

### Phase 3: Testing & Quality
1. **Write comprehensive tests** for each migrated agent
2. **Achieve 100% test coverage** on core components
3. **Implement CI/CD pipeline** with pytest, black, flake8, mypy
4. **Create integration tests** for NIM/Ollama fallback

### Phase 4: API Layer
1. **Implement FastAPI routes** for:
   - `/agents/{slug}` - Agent instantiation and interaction
   - `/squads/{squad}` - Squad-level operations
   - `/health` - System health checks
   - `/metrics` - Performance monitoring

2. **Add authentication middleware** for multi-tenancy
3. **Implement rate limiting** per client/agent

### Phase 5: Remaining 152 Agents
1. **Prioritize high-value squads** first:
   - Support (18 agents) → Sales (20 agents) → Content (22 agents)
   - Ops (16 agents) → Dev (20 agents) → Data (18 agents)
   - Finance (14 agents) → HR (14 agents) → Legal (10 agents)
   - Custom (4 agents)

2. **Batch implementation** by squad for efficiency
3. **Reuse patterns** from initial agent implementations

## 🎯 Key Upgrades Implemented

### 1. LLM Infrastructure Upgrade
```python
# OLD: Basic Ollama only
def _call_ollama(self, prompt, model="phi3"):
    # Limited error handling

# NEW: NIM primary → Ollama fallback → Mock
def _call_llm(self, prompt, model=None):
    if os.getenv("GHOST_MOCK_AI") == "true":
        return f"[MOCK] Response for: {prompt[:50]}"
    
    try:
        client = NIMClient(model=model or self.model)
        return client.complete(prompt, system=self.get_role_prompt())
    except LLMConnectionError:
        fallback = OllamaFallbackClient()
        return fallback.complete(prompt, model="phi3")
```

### 2. Structured Logging Upgrade
```python
# OLD: Simple file append
def log_interaction(self, user_input, ai_response):
    with open(log_file, 'a') as f:
        f.write(json.dumps({...}) + '\n')

# NEW: Structured JSON logging per client/agent
def _log_interaction(self, action: str, input: str, output: str):
    self.logger.info(
        "agent_interaction",
        action=action,
        input=input,
        output=output,
        agent_slug=self.agent_slug,
        squad=self.squad,
        client=self.client_name
    )
```

### 3. Knowledge Base Upgrade
```python
# OLD: Basic file loading
def _load_knowledge_base(self, path):
    if os.path.isdir(path):
        for file in Path(path).glob("*.txt"):
            # Simple concatenation

# NEW: Professional KB loader with chunking
def load_knowledge_base_dir(directory_path: str) -> str:
    # Support multiple file types
    # Automatic chunking for LLM context
    # Error handling and caching
```

## 📊 Progress Tracking

| Squad | Target | Completed | Remaining | Status |
|-------|--------|-----------|-----------|---------|
| Support | 18 | 1 | 17 | 🟡 In Progress |
| Sales | 20 | 0 | 20 | ⚪ Not Started |
| Content | 22 | 0 | 22 | ⚪ Not Started |
| Ops | 16 | 0 | 16 | ⚪ Not Started |
| Data | 18 | 0 | 18 | ⚪ Not Started |
| Dev | 20 | 0 | 20 | ⚪ Not Started |
| Finance | 14 | 0 | 14 | ⚪ Not Started |
| HR | 14 | 0 | 14 | ⚪ Not Started |
| Legal | 10 | 0 | 10 | ⚪ Not Started |
| Custom | 4 | 0 | 4 | ⚪ Not Started |
| **Total** | **156** | **1** | **155** | **1% Complete** |

## 🚀 Immediate Next Steps

1. **Migrate remaining 3 existing agents** this week
2. **Set up testing pipeline** with pytest coverage
3. **Create agent factory pattern** for dynamic instantiation
4. **Implement first FastAPI endpoint** for agent interaction

## 💡 Business Impact

This upgrade transforms Ghost Agency from a **simple script** into a **production-ready SaaS platform**:

- **Multi-tenant architecture** ready for client isolation
- **Enterprise-grade reliability** with proper error handling
- **Scalable to 156 agents** with consistent patterns
- **Professional monitoring** with structured logging
- **Commercial deployment ready** with proper configuration management

The foundation is now solid - the remaining work is primarily **pattern replication** across the other 155 agents.

---

**Last Updated:** $(date +"%Y-%m-%d %H:%M:%S")
**Current Agent Count:** 1/156
**Phase:** 1 (Core Infrastructure) Complete