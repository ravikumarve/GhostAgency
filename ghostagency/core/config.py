import os
from pathlib import Path

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

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)
