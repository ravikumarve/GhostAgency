"""Tests for Data Squad Agents."""

import pytest
from unittest.mock import patch

from ghostagency.agents.squad_data.data_research import DataResearchAgent


@pytest.fixture
def agent():
    """Create a DataResearchAgent instance for testing."""
    return DataResearchAgent(
        client_name="TestCo",
        knowledge_base_path=None,
    )


@pytest.fixture
def mock_nim():
    """Patch NIMClient.complete to return a canned response."""
    with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
        m.return_value = "Research report: Key findings include..."
        yield m


class TestDataResearchAgent:
    def test_primary_action_returns_string(self, agent, mock_nim):
        """Test that primary_action returns a string response."""
        result = agent.primary_action("What are the latest AI trends?")
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "data-research" in AGENT_REGISTRY

    def test_agent_has_correct_attributes(self):
        """Test that the agent has required class attributes."""
        assert DataResearchAgent.agent_slug == "data-research"
        assert DataResearchAgent.squad == "data"
        assert DataResearchAgent.display_name == "Data Research Agent"
        assert DataResearchAgent.price_tier == "$1,000/month"

    def test_llm_failure_returns_error_message(self, agent):
        """Test that LLM failure returns a fallback error message."""
        with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
            m.side_effect = Exception("LLM connection failed")
            result = agent.primary_action("Test query")
        assert isinstance(result, str) and len(result) > 0
        assert "apologize" in result.lower() or "technical difficulties" in result.lower()

    def test_primary_action_with_different_depth(self, agent, mock_nim):
        """Test primary_action with depth parameter."""
        result = agent.primary_action("Market analysis", depth="deep")
        assert isinstance(result, str) and len(result) > 0

    def test_get_role_prompt_returns_string(self, agent):
        """Test that get_role_prompt returns a non-empty string."""
        prompt = agent.get_role_prompt()
        assert isinstance(prompt, str) and len(prompt) > 0
        assert "TestCo" in prompt
