"""Custom exception hierarchy for Ghost Agency."""


class GhostAgencyError(Exception):
    """Base exception for all Ghost Agency errors."""

    pass


class LLMError(GhostAgencyError):
    """Base exception for LLM-related errors."""

    pass


class LLMConnectionError(LLMError):
    """Raised when unable to connect to LLM service."""

    pass


class LLMTimeoutError(LLMError):
    """Raised when LLM request times out."""

    pass


class AgentNotFoundError(GhostAgencyError):
    """Raised when agent slug is not found in registry."""

    pass


class KnowledgeBaseError(GhostAgencyError):
    """Raised when knowledge base operations fail."""

    pass


class ConfigurationError(GhostAgencyError):
    """Raised when configuration is invalid or missing."""

    pass
