from __future__ import annotations

import requests

from ghostagency.core.exceptions import LLMConnectionError, LLMTimeoutError
from ghostagency.core.config import (
    NIM_BASE_URL,
    DEFAULT_MODEL,
    NIM_API_KEY,
    NIM_TIMEOUT,
    GHOST_MAX_RETRIES,
)


class NIMClient:
    """NVIDIA NIM API client — primary LLM backend for all 156 agents."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or DEFAULT_MODEL
        self.base_url = NIM_BASE_URL
        self.headers = {
            "Authorization": f"Bearer {NIM_API_KEY}",
            "Content-Type": "application/json",
        }

    def ping(self) -> str:
        """Verify NIM connectivity."""
        resp = self.complete("Say: NIM OK")
        return resp

    def complete(self, prompt: str, system: str = "", max_tokens: int = 1024) -> str:
        """Single-turn completion. Retries up to MAX_RETRIES."""
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        for attempt in range(GHOST_MAX_RETRIES):
            try:
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=self.headers,
                    json={
                        "model": self.model,
                        "messages": messages,
                        "max_tokens": max_tokens,
                    },
                    timeout=NIM_TIMEOUT,
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"].strip()

            except requests.Timeout:
                if attempt == GHOST_MAX_RETRIES - 1:
                    raise LLMTimeoutError(
                        f"NIM timeout after {NIM_TIMEOUT}s on attempt {attempt + 1}"
                    )

            except (requests.ConnectionError, requests.HTTPError) as e:
                if hasattr(e, "response") and e.response.status_code == 403:
                    raise LLMConnectionError("NIM authentication failed: Invalid API key")
                raise LLMConnectionError(f"NIM connection failed: {e}")

            except (KeyError, IndexError) as e:
                return f"ERROR: Unexpected NIM response format: {e}"

        return "ERROR: Max retries exceeded"
