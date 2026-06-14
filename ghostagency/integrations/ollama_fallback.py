"""Ollama provider — local LLM fallback for CPU-only mode."""

from __future__ import annotations

import requests

from ghostagency.core.exceptions import LLMConnectionError
from ghostagency.core.config import OLLAMA_URL, OLLAMA_TIMEOUT
from ghostagency.integrations.providers.base import LLMProvider


class OllamaFallbackClient(LLMProvider):
    """Local Ollama provider (CPU-friendly fallback)."""

    def __init__(self, model: str | None = None) -> None:
        self.base_url = OLLAMA_URL
        self.default_model = model or "phi3:mini"

    def ping(self) -> str:
        resp = self.complete("Respond with exactly: OK")
        return resp

    def complete(
        self, prompt: str, system: str = "", max_tokens: int = 1024
    ) -> str:
        """Single-turn completion using Ollama generate endpoint."""
        try:
            full_prompt = f"{system}\n\n{prompt}" if system else prompt

            response = requests.post(
                self.base_url,
                json={
                    "model": self.default_model,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {"num_predict": max_tokens},
                },
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
