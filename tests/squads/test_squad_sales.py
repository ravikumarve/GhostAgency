"""Tests for SalesQualificationAgent — squad_sales."""

import pytest
from unittest.mock import patch

from ghostagency.agents.squad_sales.sales_qualification import SalesQualificationAgent


@pytest.fixture
def agent():
    """Create a SalesQualificationAgent instance for testing."""
    return SalesQualificationAgent(
        client_name="TestCo", company_info_path=None, product_info_path=None
    )


@pytest.fixture
def mock_nim():
    """Patch NIMClient.complete to return a canned response."""
    with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
        m.return_value = (
            "Qualification score: 8/10. "
            "Positive: Strong interest in AI. Next action: Schedule demo."
        )
        yield m


class TestSalesQualificationAgent:
    def test_primary_action_returns_string(self, agent, mock_nim):
        """Test that primary_action returns a string response."""
        lead_info = {"name": "John", "company": "TestCo", "interest": "AI solutions"}
        result = agent.primary_action(lead_info)
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "sales-qualification" in AGENT_REGISTRY

    def test_nim_timeout_falls_back_gracefully(self, agent):
        """Test that NIM timeout falls back gracefully."""
        from ghostagency.core.exceptions import LLMTimeoutError

        # Mock the entire _call_llm method to simulate timeout
        with patch.object(agent, "_call_llm", side_effect=LLMTimeoutError("timeout")):
            lead_info = {"name": "John", "company": "TestCo"}
            result = agent.primary_action(lead_info)
        assert isinstance(result, str)  # Must not raise

    def test_logs_written_on_interaction(self, agent, mock_nim):
        """Test that interactions are logged."""
        # Mock the logger to avoid file system operations
        with patch.object(agent.logger, "info") as mock_log:
            lead_info = {"name": "John", "company": "TestCo"}
            agent.primary_action(lead_info)

            # Check that logger was called
            mock_log.assert_called_once()

    def test_draft_followup_email_returns_string(self, agent, mock_nim):
        """Test that draft_followup_email returns a string."""
        email = agent.draft_followup_email("John", "TestCo", "Interested in AI")
        assert isinstance(email, str) and len(email) > 0

    def test_get_role_prompt_includes_client_name(self, agent):
        """Test that role prompt includes client name."""
        prompt = agent.get_role_prompt()
        assert "TestCo" in prompt
        assert "Sales Development Rep" in prompt

    def test_format_lead_info_correctly(self, agent):
        """Test that lead information is formatted correctly."""
        lead_info = {
            "name": "John Doe",
            "company": "Tech Solutions Inc.",
            "title": "CTO",
            "interest_level": "high",
        }

        formatted = agent._format_lead_info(lead_info)

        # Should contain all keys in title case
        assert "John Doe" in formatted
        assert "Tech Solutions Inc." in formatted
        assert "Cto" in formatted or "CTO" in formatted
        assert "high" in formatted

    def test_load_file_returns_empty_string_for_none_path(self, agent):
        """Test that _load_file returns empty string for None path."""
        result = agent._load_file(None)
        assert result == ""

    def test_load_file_returns_empty_string_for_invalid_path(self, agent):
        """Test that _load_file returns empty string for invalid path."""
        result = agent._load_file("/nonexistent/path.txt")
        assert result == ""
