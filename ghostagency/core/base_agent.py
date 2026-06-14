from __future__ import annotations

from abc import ABC, abstractmethod
import os

from ghostagency.core.config import DEFAULT_MODEL
from ghostagency.core.logger import get_logger
from ghostagency.integrations.llm_client import get_llm_client


class AIAgent(ABC):
    """
    Abstract base for all Ghost Agency AI agents.
    Concrete subclasses must implement: primary_action(), get_role_prompt(), agent_slug
    """

    # --- Required class-level attributes (define in every subclass) ---
    agent_slug: str  # e.g. "support-tier1", "sdr-cold-outreach"
    squad: str  # e.g. "support", "sales", "content"
    display_name: str  # Human-readable name shown in UI
    price_tier: str  # e.g. "$800/mo" — used in Gumroad listing
    version: str = "1.0.0"

    def __init__(
        self,
        client_name: str,
        knowledge_base_path: str | None = None,
        model: str | None = None,
    ) -> None:
        self.client_name = client_name
        self.model = model or DEFAULT_MODEL
        self.conversation_history: list[dict] = []
        self.knowledge_base: str = self._load_kb(knowledge_base_path)
        self.logger = get_logger(self.agent_slug, client_name)

    @abstractmethod
    def primary_action(self, input: str, **kwargs) -> str:
        """The main capability of this agent. Must be implemented."""
        ...

    @abstractmethod
    def get_role_prompt(self) -> str:
        """Returns the system prompt defining this agent's role."""
        ...

    def _call_llm(self, prompt: str, model: str | None = None) -> str:
        """Provider-agnostic LLM call with automatic chain fallback.

        Uses the provider factory which chains through available providers
        (OpenAI → Anthropic → Gemini → NIM → Ollama) on connection failure.
        """
        if os.getenv("GHOST_MOCK_AI") == "true":
            return f"[MOCK] Response for: {prompt[:50]}"

        client = get_llm_client(model=model or self.model)
        return client.complete(prompt, system=self.get_role_prompt())

    def _log_interaction(self, action: str, input: str, output: str) -> None:
        """Shared structured JSON logger. Never override."""
        self.logger.info(
            "agent_interaction",
            action=action,
            input=input,
            output=output,
            agent_slug=self.agent_slug,
            squad=self.squad,
            client=self.client_name,
        )

    def _load_kb(self, path: str | None) -> str:
        """Load and cache knowledge base. Returns empty string if no path."""
        if not path:
            return ""

        try:
            if os.path.isdir(path):
                from ghostagency.kb.loader import load_knowledge_base_dir

                return load_knowledge_base_dir(path)
            else:
                from ghostagency.kb.loader import load_knowledge_base_file

                return load_knowledge_base_file(path)
        except Exception as e:
            self.logger.error("kb_load_failed", error=str(e), path=path)
            return f"Error loading knowledge base: {e}"

    def reset_history(self) -> None:
        """Clear conversation history. Call between client sessions."""
        self.conversation_history = []
