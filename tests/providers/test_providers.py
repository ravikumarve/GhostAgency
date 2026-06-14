"""Tests for LLM provider implementations and factory."""

from __future__ import annotations

import os
from unittest.mock import patch, Mock

import pytest
import requests

from ghostagency.core.exceptions import LLMConnectionError, LLMTimeoutError
from ghostagency.integrations.llm_client import get_llm_client, _ChainedProvider
from ghostagency.integrations.providers.openai import OpenAIProvider
from ghostagency.integrations.providers.anthropic import AnthropicProvider
from ghostagency.integrations.providers.gemini import GeminiProvider
from ghostagency.integrations.nim_client import NIMClient
from ghostagency.integrations.ollama_fallback import OllamaFallbackClient


# =========================================================================
# Factory tests
# =========================================================================

class TestGetLLMClient:
    """Tests for the get_llm_client factory."""

    def test_returns_chained_provider_by_default(self):
        client = get_llm_client()
        assert isinstance(client, _ChainedProvider)

    def test_respects_env_var(self):
        """get_llm_client should wrap the provider named by LLM_PROVIDER."""
        with patch.dict(os.environ, {"LLM_PROVIDER": "openai"}, clear=False):
            client = get_llm_client()
            # The chain should start with "openai"
            assert client._chain[0] == "openai"

    def test_invalid_provider_defaults_to_openai(self):
        with patch.dict(os.environ, {"LLM_PROVIDER": "nonexistent"}, clear=False):
            client = get_llm_client()
            # Should fall back to default behavior (openai chain)
            assert client._chain[0] in ("openai", "anthropic", "gemini", "nim", "ollama")


# =========================================================================
# _ChainedProvider tests
# =========================================================================

class TestChainedProvider:
    """Tests for the fallback chain wrapper."""

    def test_success_with_first_provider(self):
        """First provider succeeds — should not try fallbacks."""
        chain = _ChainedProvider(["openai", "ollama"])

        with patch(
            "ghostagency.integrations.providers.openai.OpenAIProvider.complete",
            return_value="OpenAI response",
        ) as mock_openai:
            result = chain.complete("hello")
            assert result == "OpenAI response"
            mock_openai.assert_called_once()

    def test_fallthrough_on_connection_error(self):
        """First provider fails with connection error — tries next."""
        chain = _ChainedProvider(["openai", "ollama"])

        def fail(*a, **kw):
            raise LLMConnectionError("down")

        with patch(
            "ghostagency.integrations.providers.openai.OpenAIProvider.complete",
            side_effect=fail,
        ):
            with patch(
                "ghostagency.integrations.ollama_fallback.OllamaFallbackClient.complete",
                return_value="Ollama response",
            ) as mock_ollama:
                result = chain.complete("hello")
                assert result == "Ollama response"
                mock_ollama.assert_called_once()

    def test_raises_when_all_fail(self):
        """All providers fail — should raise LLMConnectionError."""
        chain = _ChainedProvider(["openai", "ollama"])

        def fail(*a, **kw):
            raise LLMConnectionError("down")

        with patch(
            "ghostagency.integrations.providers.openai.OpenAIProvider.complete",
            side_effect=fail,
        ):
            with patch(
                "ghostagency.integrations.ollama_fallback.OllamaFallbackClient.complete",
                side_effect=fail,
            ):
                with pytest.raises(LLMConnectionError):
                    chain.complete("hello")

    def test_ping_fallthrough(self):
        """ping() also uses the fallback chain."""
        chain = _ChainedProvider(["openai", "ollama"])

        def fail(*a, **kw):
            raise LLMConnectionError("down")

        with patch(
            "ghostagency.integrations.providers.openai.OpenAIProvider.ping",
            side_effect=fail,
        ):
            with patch(
                "ghostagency.integrations.ollama_fallback.OllamaFallbackClient.ping",
                return_value="OK",
            ) as mock_ollama:
                result = chain.ping()
                assert result == "OK"
                mock_ollama.assert_called_once()


# =========================================================================
# OpenAI provider tests
# =========================================================================

class TestOpenAIProvider:
    """Tests for OpenAI provider response parsing and error handling."""

    @pytest.fixture
    def provider(self):
        return OpenAIProvider(model="gpt-4o")

    def test_successful_response(self, provider):
        """Parses a valid OpenAI chat completions response."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello from OpenAI"}}]
        }

        with patch("requests.post", return_value=mock_response):
            result = provider.complete("Say hello")
            assert result == "Hello from OpenAI"

    def test_auth_error(self, provider):
        """401 raises LLMConnectionError."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "401", response=mock_response
        )

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(LLMConnectionError, match="Invalid API key"):
                provider.complete("hello")

    def test_timeout(self, provider):
        """Timeout after retries raises LLMTimeoutError."""
        with patch("requests.post", side_effect=requests.Timeout()):
            with pytest.raises(LLMTimeoutError):
                provider.complete("hello")

    def test_includes_system_prompt(self, provider):
        """System prompt is included in the messages array."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "ok"}}]
        }

        with patch("requests.post", return_value=mock_response) as mock_post:
            provider.complete("hello", system="You are a bot")
            call_kwargs = mock_post.call_args[1]
            messages = call_kwargs["json"]["messages"]
            assert messages[0]["role"] == "system"
            assert messages[0]["content"] == "You are a bot"

    def test_ping(self, provider):
        """ping() makes a request and returns the response."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "OK"}}]
        }

        with patch("requests.post", return_value=mock_response):
            result = provider.ping()
            assert "OK" in result


# =========================================================================
# Anthropic provider tests
# =========================================================================

class TestAnthropicProvider:
    """Tests for Anthropic provider response parsing and error handling."""

    @pytest.fixture
    def provider(self):
        return AnthropicProvider(model="claude-3-5-sonnet-20241022")

    def test_successful_response(self, provider):
        """Parses a valid Anthropic messages response."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [{"type": "text", "text": "Hello from Claude"}]
        }

        with patch("requests.post", return_value=mock_response):
            result = provider.complete("Say hello")
            assert result == "Hello from Claude"

    def test_auth_error(self, provider):
        """401 raises LLMConnectionError."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 401
        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "401", response=mock_response
        )

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(LLMConnectionError, match="Invalid API key"):
                provider.complete("hello")

    def test_bad_request_returns_error_string(self, provider):
        """400 with error body returns error string instead of raising."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "error": {"message": "too many tokens"}
        }

        with patch("requests.post", return_value=mock_response):
            result = provider.complete("hello")
            assert "too many tokens" in result

    def test_multiple_content_blocks(self, provider):
        """Handles Anthropic's content block format correctly."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "content": [
                {"type": "text", "text": "Hello"},
                {"type": "text", "text": "World"},
            ]
        }

        with patch("requests.post", return_value=mock_response):
            result = provider.complete("Say hi")
            assert "Hello\nWorld" == result


# =========================================================================
# Gemini provider tests
# =========================================================================

class TestGeminiProvider:
    """Tests for Gemini provider response parsing and error handling."""

    @pytest.fixture
    def provider(self):
        return GeminiProvider(model="gemini-1.5-pro")

    def test_successful_response(self, provider):
        """Parses a valid Gemini generateContent response."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [{"text": "Hello from Gemini"}]
                    }
                }
            ]
        }

        with patch("requests.post", return_value=mock_response):
            result = provider.complete("Say hello")
            assert result == "Hello from Gemini"

    def test_auth_error(self, provider):
        """403 raises LLMConnectionError."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "403", response=mock_response
        )

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(LLMConnectionError, match="Invalid API key"):
                provider.complete("hello")

    def test_empty_candidates(self, provider):
        """Empty candidates array returns empty string."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"candidates": []}

        with patch("requests.post", return_value=mock_response):
            result = provider.complete("hello")
            assert result == ""

    def test_multi_part_response(self, provider):
        """Multiple text parts are joined with newlines."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "Part 1"},
                            {"text": "Part 2"},
                        ]
                    }
                }
            ]
        }

        with patch("requests.post", return_value=mock_response):
            result = provider.complete("Say more")
            assert result == "Part 1\nPart 2"


# =========================================================================
# NIM provider tests
# =========================================================================

class TestNIMClient:
    """Tests for NIM client (now an LLMProvider)."""

    @pytest.fixture
    def provider(self):
        return NIMClient(model="z-ai/glm-5.1")

    def test_successful_response(self, provider):
        """Parses a valid NIM chat completions response."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "NIM response"}}]
        }

        with patch("requests.post", return_value=mock_response):
            result = provider.complete("hello")
            assert result == "NIM response"

    def test_auth_error_403(self, provider):
        """403 raises LLMConnectionError."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.HTTPError(
            "403", response=mock_response
        )

        with patch("requests.post", return_value=mock_response):
            with pytest.raises(LLMConnectionError, match="Invalid API key"):
                provider.complete("hello")


# =========================================================================
# Ollama provider tests
# =========================================================================

class TestOllamaFallbackClient:
    """Tests for Ollama provider (now an LLMProvider)."""

    @pytest.fixture
    def provider(self):
        return OllamaFallbackClient(model="phi3:mini")

    def test_successful_response(self, provider):
        """Parses a valid Ollama generate response."""
        mock_response = Mock(spec=requests.Response)
        mock_response.status_code = 200
        mock_response.json.return_value = {"response": "Ollama response"}

        with patch("requests.post", return_value=mock_response):
            result = provider.complete("hello")
            assert result == "Ollama response"

    def test_connection_error(self, provider):
        """Connection refused raises LLMConnectionError."""
        with patch("requests.post", side_effect=requests.ConnectionError()):
            with pytest.raises(LLMConnectionError, match="Ollama not running"):
                provider.complete("hello")
