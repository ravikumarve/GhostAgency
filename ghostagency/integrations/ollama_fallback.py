from __future__ import annotations
import os
import requests
from typing import Optional

from ghostagency.core.exceptions import LLMConnectionError
from ghostagency.core.config import OLLAMA_URL, OLLAMA_TIMEOUT


class OllamaFallbackClient:
    """Fallback to local Ollama when NIM is unavailable (CPU-only mode)."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or OLLAMA_URL

    def complete(self, prompt: str, model: str = "phi3") -> str:
        """Single-turn completion using Ollama."""
        try:
            response = requests.post(
                self.base_url,
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=OLLAMA_TIMEOUT,
            )

            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                return f"Ollama error: Status {response.status_code}"

        except requests.ConnectionError:
            raise LLMConnectionError("Ollama not running. Start with: ollama serve")
        except Exception as e:
            return f"Ollama error: {e}"
