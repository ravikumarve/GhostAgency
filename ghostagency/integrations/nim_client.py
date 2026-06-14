from __future__ import annotations

import requests

from ghostagency.core import settings_db
from ghostagency.core.exceptions import LLMConnectionError, LLMTimeoutError
from ghostagency.core.config import (
    NIM_BASE_URL,
    NIM_API_KEY,
    NIM_TIMEOUT,
    GHOST_MAX_RETRIES,
)
from ghostagency.integrations.providers.base import LLMProvider


class NIMClient(LLMProvider):
    """NVIDIA NIM API client — testing / internal provider."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or settings_db.get("nim_model") or "z-ai/glm-5.1"
        self.base_url = settings_db.get("nim_base_url") or NIM_BASE_URL
        api_key = settings_db.get("nim_api_key") or NIM_API_KEY
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.timeout = settings_db.get_int("nim_timeout") or NIM_TIMEOUT

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
                    timeout=self.timeout,
                )
                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"].strip()

            except requests.Timeout:
                if attempt == GHOST_MAX_RETRIES - 1:
                    raise LLMTimeoutError(
                        f"NIM timeout after {self.timeout}s on attempt {attempt + 1}"
                    )

            except (requests.ConnectionError, requests.HTTPError) as e:
                if hasattr(e, "response") and e.response.status_code == 403:
                    raise LLMConnectionError("NIM authentication failed: Invalid API key")
                raise LLMConnectionError(f"NIM connection failed: {e}")

            except (KeyError, IndexError) as e:
                return f"ERROR: Unexpected NIM response format: {e}"

        return "ERROR: Max retries exceeded"
