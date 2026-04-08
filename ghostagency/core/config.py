import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default configuration
DEFAULT_MODEL = os.getenv("NIM_MODEL", "deepseek-ai/deepseek-v3-0324")
LOG_DIR = Path(os.getenv("GHOST_LOG_DIR", "logs"))

# NIM Configuration
NIM_BASE_URL = os.getenv("NIM_BASE_URL", "https://integrate.api.nvidia.com/v1")
NIM_API_KEY = os.getenv("NIM_API_KEY", "")
NIM_TIMEOUT = int(os.getenv("NIM_TIMEOUT", "60"))

# Ollama Fallback
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

# Runtime
GHOST_MOCK_AI = os.getenv("GHOST_MOCK_AI", "false").lower() == "true"
GHOST_MAX_RETRIES = int(os.getenv("GHOST_MAX_RETRIES", "3"))

# API Configuration
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)
