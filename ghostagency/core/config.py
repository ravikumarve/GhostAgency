import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower().strip()
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gpt-4o")
LOG_DIR = Path(os.getenv("GHOST_LOG_DIR", "logs"))

# ---------------------------------------------------------------------------
# Provider: OpenAI (default — also works with OpenAI-compatible endpoints)
# ---------------------------------------------------------------------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")
OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", "60"))

# ---------------------------------------------------------------------------
# Provider: Anthropic (Claude)
# ---------------------------------------------------------------------------
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
ANTHROPIC_TIMEOUT = int(os.getenv("ANTHROPIC_TIMEOUT", "60"))

# ---------------------------------------------------------------------------
# Provider: Google Gemini
# ---------------------------------------------------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
GEMINI_TIMEOUT = int(os.getenv("GEMINI_TIMEOUT", "60"))

# ---------------------------------------------------------------------------
# Provider: NVIDIA NIM (testing / internal)
# ---------------------------------------------------------------------------
NIM_BASE_URL = os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
NIM_API_KEY = os.getenv("NIM_API_KEY", "")
NIM_MODEL = os.getenv("NIM_MODEL", "z-ai/glm-5.1")
NIM_TIMEOUT = int(os.getenv("NIM_TIMEOUT", "60"))

# ---------------------------------------------------------------------------
# Provider: Ollama (local CPU fallback)
# ---------------------------------------------------------------------------
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434/api/generate")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

# ---------------------------------------------------------------------------
# Runtime
# ---------------------------------------------------------------------------
GHOST_MOCK_AI = os.getenv("GHOST_MOCK_AI", "false").lower() == "true"
GHOST_MAX_RETRIES = int(os.getenv("GHOST_MAX_RETRIES", "3"))

# API Configuration
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)
