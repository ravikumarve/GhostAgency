"""OpenAI provider — GPT-4o, GPT-4, GPT-3.5, and compatible endpoints."""

from __future__ import annotations

import requests

from ghostagency.core import settings_db
from ghostagency.core.exceptions import LLMConnectionError, LLMTimeoutError
from ghostagency.core.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
    OPENAI_MODEL,
    OPENAI_TIMEOUT,
    GHOST_MAX_RETRIES,
)
from ghostagency.integrations.providers.base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI-compatible chat completions provider.

    Works with:
      - OpenAI API (api.openai.com)
      - Any OpenAI-compatible endpoint (Together AI, Groq, OpenRouter, etc.)
    Set OPENAI_BASE_URL to redirect to a compatible third-party.

    API key is read from settings DB (with env var fallback) at call time.
    """

    def __init__(self, model: str | None = None) -> None:
        self.model = model or settings_db.get("openai_model") or OPENAI_MODEL
        self.base_url = settings_db.get("openai_base_url") or OPENAI_BASE_URL
        api_key = settings_db.get("openai_api_key") or OPENAI_API_KEY
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.timeout = (
            settings_db.get_int("openai_timeout") or OPENAI_TIMEOUT
        )

    def ping(self) -> str:
        resp = self.complete("Respond with exactly: OK")
        return resp

    def complete(self, prompt: str, system: str = "", max_tokens: int = 1024) -> str:
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

                if response.status_code == 401:
                    raise LLMConnectionError(
                        "OpenAI authentication failed: Invalid API key"
                    )

                response.raise_for_status()
                return response.json()["choices"][0]["message"]["content"].strip()

            except requests.Timeout:
                if attempt == GHOST_MAX_RETRIES - 1:
                    raise LLMTimeoutError(
                        f"OpenAI timeout after {self.timeout}s on attempt {attempt + 1}"
                    )

            except (requests.ConnectionError, requests.HTTPError) as e:
                if isinstance(e, requests.HTTPError):
                    if e.response.status_code == 401:
                        raise LLMConnectionError(
                            "OpenAI authentication failed: Invalid API key"
                        )
                raise LLMConnectionError(f"OpenAI connection failed: {e}")

            except (KeyError, IndexError) as e:
                return f"ERROR: Unexpected OpenAI response format: {e}"

        return "ERROR: Max retries exceeded"
