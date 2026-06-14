"""LLM provider factory — selects and chains providers by config.

Selection priority:
  1. SQLite settings DB (saved via /settings page)
  2. LLM_PROVIDER env var
  3. Default: openai

If the primary provider fails with a connection/auth error, the factory
falls through the chain to the next available provider.
"""

from __future__ import annotations

from ghostagency.core import settings_db
from ghostagency.core.config import LLM_PROVIDER
from ghostagency.core.exceptions import LLMConnectionError
from ghostagency.integrations.providers.base import LLMProvider
from ghostagency.integrations.providers.openai import OpenAIProvider
from ghostagency.integrations.providers.anthropic import AnthropicProvider
from ghostagency.integrations.providers.gemini import GeminiProvider
from ghostagency.integrations.nim_client import NIMClient
from ghostagency.integrations.ollama_fallback import OllamaFallbackClient

# Fallback chain: each provider's next option when connection fails.
# Keys are LLM_PROVIDER values; values are ordered fallback provider names.
_FALLBACK_CHAIN: dict[str, list[str]] = {
    "openai": ["anthropic", "gemini", "nim", "ollama"],
    "anthropic": ["openai", "gemini", "nim", "ollama"],
    "gemini": ["openai", "anthropic", "nim", "ollama"],
    "nim": ["ollama"],
    "ollama": [],
}

_PROVIDER_CLASSES: dict[str, type] = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "gemini": GeminiProvider,
    "nim": NIMClient,
    "ollama": OllamaFallbackClient,
}


def _instantiate(name: str, model: str | None = None) -> LLMProvider:
    """Create a provider instance by name."""
    cls = _PROVIDER_CLASSES[name]
    return cls(model=model)


def get_llm_client(model: str | None = None) -> LLMProvider:
    """Return the primary LLM client.

    Selection priority:
      1. SQLite settings DB (saved via /settings page)
      2. LLM_PROVIDER env var
      3. Default: "openai"

    The client wraps the fallback chain — if primary can't connect,
    it transparently tries the next provider.
    """
    primary = (
        settings_db.get("llm_provider")
        or LLM_PROVIDER
    ).lower().strip()

    if primary not in _PROVIDER_CLASSES:
        primary = "openai"

    chain = [primary] + _FALLBACK_CHAIN.get(primary, [])
    return _ChainedProvider(chain, model)


class _ChainedProvider(LLMProvider):
    """Wrapper that tries providers in order until one succeeds."""

    def __init__(self, chain: list[str], model: str | None = None) -> None:
        self._chain = chain
        self._model = model

    def ping(self) -> str:
        last_error = None
        for name in self._chain:
            try:
                provider = _instantiate(name, self._model)
                return provider.ping()
            except LLMConnectionError as e:
                last_error = e
                continue
        raise LLMConnectionError(
            f"All providers unavailable: {', '.join(self._chain)}"
        ) from last_error

    def complete(
        self, prompt: str, system: str = "", max_tokens: int = 1024
    ) -> str:
        last_error = None
        for name in self._chain:
            try:
                provider = _instantiate(name, self._model)
                return provider.complete(
                    prompt, system=system, max_tokens=max_tokens
                )
            except LLMConnectionError as e:
                last_error = e
                continue
        raise LLMConnectionError(
            f"All providers unavailable: {', '.join(self._chain)}"
        ) from last_error
