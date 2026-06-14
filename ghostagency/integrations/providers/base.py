"""Abstract base for all LLM providers."""

from __future__ import annotations

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Interface all LLM providers must implement.

    Each provider handles its own auth, request format, response parsing,
    and error translation into the Ghost Agency exception hierarchy.
    """

    @abstractmethod
    def complete(self, prompt: str, system: str = "", max_tokens: int = 1024) -> str:
        """Single-turn completion. Returns the response text."""
        ...

    @abstractmethod
    def ping(self) -> str:
        """Lightweight connectivity check. Should return a short OK string."""
        ...
