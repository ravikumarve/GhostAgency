"""LLM provider factory — selects and chains providers by config.

Selection is driven by the LLM_PROVIDER env var:

  LLM_PROVIDER=openai     → OpenAI (GPT-4o, etc.) — default
  LLM_PROVIDER=anthropic  → Anthropic (Claude 3.5)
  LLM_PROVIDER=gemini     → Google Gemini 1.5
  LLM_PROVIDER=nim        → NVIDIA NIM (testing/internal)
  LLM_PROVIDER=ollama     → Local Ollama (fallback)

If the primary provider fails with a connection/auth error, the factory
falls through the chain to the next available provider.
"""

from __future__ import annotations

import os

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
    """Return the primary LLM client based on LLM_PROVIDER env var.

    The client wraps the fallback chain internally — if the primary
    provider can't connect, it transparently tries the next in the chain.
    """
    primary = (os.getenv("LLM_PROVIDER") or LLM_PROVIDER).lower().strip()

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
