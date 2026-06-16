"""Tests for Legal Squad Agents."""

import pytest
from unittest.mock import patch

from ghostagency.agents.squad_legal.legal_contract_review import LegalContractReviewAgent


@pytest.fixture
def agent():
    """Create a LegalContractReviewAgent instance for testing."""
    return LegalContractReviewAgent(
        client_name="TestCo",
        knowledge_base_path=None,
    )


@pytest.fixture
def mock_nim():
    """Patch NIMClient.complete to return a canned response."""
    with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
        m.return_value = "Legal review: Contract terms are standard."
        yield m


class TestLegalContractReviewAgent:
    def test_primary_action_returns_string(self, agent, mock_nim):
        """Test that primary_action returns a string response."""
        result = agent.primary_action(
            "This agreement is entered into by and between Party A and Party B...",
            document_type="contract"
        )
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "legal-contract-review" in AGENT_REGISTRY

    def test_agent_has_correct_attributes(self):
        """Test that the agent has required class attributes."""
        assert LegalContractReviewAgent.agent_slug == "legal-contract-review"
        assert LegalContractReviewAgent.squad == "legal"
        assert LegalContractReviewAgent.display_name == "Legal Contract Review Agent"
        assert LegalContractReviewAgent.price_tier == "$2,000/month"

    def test_llm_failure_returns_error_message(self, agent):
        """Test that LLM failure returns a fallback error message."""
        with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
            m.side_effect = Exception("LLM connection failed")
            result = agent.primary_action("NDA Agreement")
        assert isinstance(result, str) and len(result) > 0
        assert "apologize" in result.lower() or "technical difficulties" in result.lower()

    def test_primary_action_defaults_contract_type(self, agent, mock_nim):
        """Test primary_action with default document type."""
        result = agent.primary_action("Service agreement terms...")
        assert isinstance(result, str) and len(result) > 0

    def test_get_role_prompt_returns_string(self, agent):
        """Test that get_role_prompt returns a non-empty string."""
        prompt = agent.get_role_prompt()
        assert isinstance(prompt, str) and len(prompt) > 0
        assert "TestCo" in prompt
