"""Google Gemini provider — Gemini 1.5 Pro, Gemini 1.5 Flash, and other models."""

from __future__ import annotations

import requests

from ghostagency.core import settings_db
from ghostagency.core.exceptions import LLMConnectionError, LLMTimeoutError
from ghostagency.core.config import (
    GEMINI_API_KEY,
    GEMINI_BASE_URL,
    GEMINI_MODEL,
    GEMINI_TIMEOUT,
    GHOST_MAX_RETRIES,
)
from ghostagency.integrations.providers.base import LLMProvider


class GeminiProvider(LLMProvider):
    """Google Gemini API provider.

    Uses the generateContent endpoint with API key passed as query parameter.
    API key is read from settings DB (with env var fallback) at call time.
    """

    def __init__(self, model: str | None = None) -> None:
        self.model = model or settings_db.get("gemini_model") or GEMINI_MODEL
        self.base_url = settings_db.get("gemini_base_url") or GEMINI_BASE_URL
        self.api_key = settings_db.get("gemini_api_key") or GEMINI_API_KEY
        self.timeout = (
            settings_db.get_int("gemini_timeout") or GEMINI_TIMEOUT
        )

    def ping(self) -> str:
        resp = self.complete("Respond with exactly: OK")
        return resp

    def complete(self, prompt: str, system: str = "", max_tokens: int = 1024) -> str:
        url = f"{self.base_url}/v1beta/models/{self.model}:generateContent?key={self.api_key}"

        contents: list[dict] = [{"parts": [{"text": prompt}]}]

        payload: dict = {
            "contents": contents,
            "generationConfig": {
                "maxOutputTokens": max_tokens,
            },
        }

        if system:
            payload["systemInstruction"] = {
                "parts": [{"text": system}]
            }

        for attempt in range(GHOST_MAX_RETRIES):
            try:
                response = requests.post(
                    url,
                    headers={"Content-Type": "application/json"},
                    json=payload,
                    timeout=self.timeout,
                )

                if response.status_code == 403:
                    raise LLMConnectionError(
                        "Gemini authentication failed: Invalid API key"
                    )

                if response.status_code == 400:
                    body = response.json()
                    if "error" in body:
                        return f"ERROR: Gemini: {body['error'].get('message', 'bad request')}"

                response.raise_for_status()
                body = response.json()

                # Gemini returns candidates array with content parts
                candidates = body.get("candidates", [])
                if not candidates:
                    return ""
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                text_parts = [p.get("text", "") for p in parts]
                return "\n".join(text_parts).strip()

            except requests.Timeout:
                if attempt == GHOST_MAX_RETRIES - 1:
                    raise LLMTimeoutError(
                        f"Gemini timeout after {self.timeout}s on attempt {attempt + 1}"
                    )

            except (requests.ConnectionError, requests.HTTPError) as e:
                if isinstance(e, requests.HTTPError):
                    if e.response.status_code == 403:
                        raise LLMConnectionError(
                            "Gemini authentication failed: Invalid API key"
                        )
                raise LLMConnectionError(f"Gemini connection failed: {e}")

            except (KeyError, IndexError) as e:
                return f"ERROR: Unexpected Gemini response format: {e}"

        return "ERROR: Max retries exceeded"
