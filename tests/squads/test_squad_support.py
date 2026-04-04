"""Tests for SupportTier1Agent — squad_support."""

import pytest
from unittest.mock import patch, Mock
from pathlib import Path

from ghostagency.agents.squad_support.support_tier1 import SupportTier1Agent


@pytest.fixture
def agent():
    """Create a SupportTier1Agent instance for testing."""
    return SupportTier1Agent(
        client_name="TestCo",
        knowledge_base_path=None,
        escalation_email="support@testco.com",
    )


@pytest.fixture
def mock_nim():
    """Patch NIMClient.complete to return a canned response."""
    with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
        m.return_value = "Your order ships in 3-5 business days."
        yield m


class TestSupportTier1Agent:
    def test_primary_action_returns_string(self, agent, mock_nim):
        """Test that primary_action returns a string response."""
        result = agent.primary_action("Where is my order?")
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "support-tier1" in AGENT_REGISTRY

    def test_nim_timeout_falls_back_gracefully(self, agent):
        """Test that NIM timeout falls back gracefully."""
        from ghostagency.core.exceptions import LLMTimeoutError

        # Mock the entire _call_llm method to simulate timeout
        with patch.object(agent, "_call_llm", side_effect=LLMTimeoutError("timeout")):
            result = agent.primary_action("Hello")
        assert isinstance(result, str)  # Must not raise

    def test_logs_written_on_interaction(self, agent, mock_nim):
        """Test that interactions are logged."""
        # Mock the logger to avoid file system operations
        with patch.object(agent.logger, "info") as mock_log:
            agent.primary_action("Test message")

            # Check that logger was called
            mock_log.assert_called_once()

    def test_escalation_detection(self, agent):
        """Test that escalation is detected correctly."""
        # Should detect escalation
        assert agent._needs_escalation("I don't know the answer")
        assert agent._needs_escalation("This is complex, needs specialist")

        # Should not detect escalation
        assert not agent._needs_escalation("Shipping takes 3-5 days")
        assert not agent._needs_escalation("Yes, that's covered under warranty")

    def test_get_role_prompt_includes_client_name(self, agent):
        """Test that role prompt includes client name."""
        prompt = agent.get_role_prompt()
        assert "TestCo" in prompt
        assert "Tier 1 Support Agent" in prompt
