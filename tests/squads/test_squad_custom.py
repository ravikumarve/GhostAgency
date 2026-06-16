"""Tests for Custom Squad Agents."""

import pytest
from unittest.mock import patch

from ghostagency.agents.squad_custom.custom_generic import CustomGenericAgent


@pytest.fixture
def agent():
    """Create a CustomGenericAgent instance for testing."""
    return CustomGenericAgent(
        client_name="TestCo",
        knowledge_base_path=None,
    )


@pytest.fixture
def agent_with_instructions():
    """Create a CustomGenericAgent with custom instructions."""
    return CustomGenericAgent(
        client_name="TestCo",
        knowledge_base_path=None,
        custom_instructions="Always respond in Spanish.",
    )


@pytest.fixture
def mock_nim():
    """Patch NIMClient.complete to return a canned response."""
    with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
        m.return_value = "Custom task completed successfully."
        yield m


class TestCustomGenericAgent:
    def test_primary_action_returns_string(self, agent, mock_nim):
        """Test that primary_action returns a string response."""
        result = agent.primary_action("Summarize this document")
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "custom-generic" in AGENT_REGISTRY

    def test_agent_has_correct_attributes(self):
        """Test that the agent has required class attributes."""
        assert CustomGenericAgent.agent_slug == "custom-generic"
        assert CustomGenericAgent.squad == "custom"
        assert CustomGenericAgent.display_name == "Custom Generic Agent"
        assert CustomGenericAgent.price_tier == "Custom"

    def test_llm_failure_returns_error_message(self, agent):
        """Test that LLM failure returns a fallback error message."""
        with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
            m.side_effect = Exception("LLM connection failed")
            result = agent.primary_action("Do something")
        assert isinstance(result, str) and len(result) > 0
        assert "apologize" in result.lower() or "technical difficulties" in result.lower()

    def test_custom_instructions_in_role_prompt(self, agent_with_instructions):
        """Test that custom instructions appear in the role prompt."""
        prompt = agent_with_instructions.get_role_prompt()
        assert "Spanish" in prompt

    def test_get_role_prompt_returns_string(self, agent):
        """Test that get_role_prompt returns a non-empty string."""
        prompt = agent.get_role_prompt()
        assert isinstance(prompt, str) and len(prompt) > 0
        assert "TestCo" in prompt
