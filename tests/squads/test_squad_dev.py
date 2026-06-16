"""Tests for Dev Squad Agents."""

import pytest
from unittest.mock import patch

from ghostagency.agents.squad_dev.dev_code_review import DevCodeReviewAgent


@pytest.fixture
def agent():
    """Create a DevCodeReviewAgent instance for testing."""
    return DevCodeReviewAgent(
        client_name="TestCo",
        knowledge_base_path=None,
    )


@pytest.fixture
def mock_nim():
    """Patch NIMClient.complete to return a canned response."""
    with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
        m.return_value = "Code review: No critical issues found."
        yield m


class TestDevCodeReviewAgent:
    def test_primary_action_returns_string(self, agent, mock_nim):
        """Test that primary_action returns a string response."""
        result = agent.primary_action("def hello(): print('hi')")
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "dev-code-review" in AGENT_REGISTRY

    def test_agent_has_correct_attributes(self):
        """Test that the agent has required class attributes."""
        assert DevCodeReviewAgent.agent_slug == "dev-code-review"
        assert DevCodeReviewAgent.squad == "dev"
        assert DevCodeReviewAgent.display_name == "Dev Code Review Agent"
        assert DevCodeReviewAgent.price_tier == "$1,500/month"

    def test_llm_failure_returns_error_message(self, agent):
        """Test that LLM failure returns a fallback error message."""
        with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
            m.side_effect = Exception("LLM connection failed")
            result = agent.primary_action("def foo(): pass")
        assert isinstance(result, str) and len(result) > 0
        assert "apologize" in result.lower() or "technical difficulties" in result.lower()

    def test_primary_action_with_language_param(self, agent, mock_nim):
        """Test primary_action with a different language."""
        result = agent.primary_action("function hello() { console.log('hi'); }", language="javascript")
        assert isinstance(result, str) and len(result) > 0

    def test_get_role_prompt_returns_string(self, agent):
        """Test that get_role_prompt returns a non-empty string."""
        prompt = agent.get_role_prompt()
        assert isinstance(prompt, str) and len(prompt) > 0
        assert "TestCo" in prompt
