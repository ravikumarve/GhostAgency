"""Anthropic provider — Claude 3.5 Sonnet, Claude 3 Haiku, and other models."""

from __future__ import annotations

import requests

from ghostagency.core import settings_db
from ghostagency.core.exceptions import LLMConnectionError, LLMTimeoutError
from ghostagency.core.config import (
    ANTHROPIC_API_KEY,
    ANTHROPIC_BASE_URL,
    ANTHROPIC_MODEL,
    ANTHROPIC_TIMEOUT,
    GHOST_MAX_RETRIES,
)
from ghostagency.integrations.providers.base import LLMProvider


class AnthropicProvider(LLMProvider):
    """Anthropic Messages API provider.

    Uses the /v1/messages endpoint with the Anthropic API format.
    API key is read from settings DB (with env var fallback) at call time.
    """

    def __init__(self, model: str | None = None) -> None:
        self.model = model or settings_db.get("anthropic_model") or ANTHROPIC_MODEL
        self.base_url = settings_db.get("anthropic_base_url") or ANTHROPIC_BASE_URL
        api_key = settings_db.get("anthropic_api_key") or ANTHROPIC_API_KEY
        self.headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        self.timeout = (
            settings_db.get_int("anthropic_timeout") or ANTHROPIC_TIMEOUT
        )

    def ping(self) -> str:
        resp = self.complete("Respond with exactly: OK")
        return resp

    def complete(self, prompt: str, system: str = "", max_tokens: int = 1024) -> str:
        payload: dict = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system

        for attempt in range(GHOST_MAX_RETRIES):
            try:
                response = requests.post(
                    f"{self.base_url}/v1/messages",
                    headers=self.headers,
                    json=payload,
                    timeout=self.timeout,
                )

                if response.status_code == 401:
                    raise LLMConnectionError(
                        "Anthropic authentication failed: Invalid API key"
                    )

                if response.status_code == 400:
                    body = response.json()
                    if "error" in body:
                        return f"ERROR: Anthropic: {body['error'].get('message', 'bad request')}"

                response.raise_for_status()
                body = response.json()

                # Anthropic returns content as a list of content blocks
                content_blocks = body.get("content", [])
                text_parts = [
                    b.get("text", "")
                    for b in content_blocks
                    if b.get("type") == "text"
                ]
                return "\n".join(text_parts).strip()

            except requests.Timeout:
                if attempt == GHOST_MAX_RETRIES - 1:
                    raise LLMTimeoutError(
                        f"Anthropic timeout after {self.timeout}s on attempt {attempt + 1}"
                    )

            except (requests.ConnectionError, requests.HTTPError) as e:
                if isinstance(e, requests.HTTPError):
                    if e.response.status_code == 401:
                        raise LLMConnectionError(
                            "Anthropic authentication failed: Invalid API key"
                        )
                raise LLMConnectionError(f"Anthropic connection failed: {e}")

            except (KeyError, IndexError) as e:
                return f"ERROR: Unexpected Anthropic response format: {e}"

        return "ERROR: Max retries exceeded"
