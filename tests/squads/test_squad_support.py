"""Tests for Support Squad Agents."""

import pytest
from unittest.mock import patch

from ghostagency.agents.squad_support.support_tier1 import SupportTier1Agent
from ghostagency.agents.squad_support.support_tier2 import SupportTier2Agent
from ghostagency.agents.squad_support.support_billing import SupportBillingAgent


@pytest.fixture
def tier1_agent():
    """Create a SupportTier1Agent instance for testing."""
    return SupportTier1Agent(
        client_name="TestCo",
        knowledge_base_path=None,
        escalation_email="support@testco.com",
    )


@pytest.fixture
def tier2_agent():
    """Create a SupportTier2Agent instance for testing."""
    return SupportTier2Agent(
        client_name="TestCo",
        knowledge_base_path=None,
        specialist_email="specialist@testco.com",
    )


@pytest.fixture
def billing_agent():
    """Create a SupportBillingAgent instance for testing."""
    return SupportBillingAgent(
        client_name="TestCo",
        knowledge_base_path=None,
        billing_contact_email="billing@testco.com",
    )


@pytest.fixture
def mock_nim():
    """Patch NIMClient.complete to return a canned response."""
    with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
        m.return_value = "Your issue has been resolved."
        yield m


class TestSupportTier1Agent:
    def test_primary_action_returns_string(self, tier1_agent, mock_nim):
        """Test that primary_action returns a string response."""
        result = tier1_agent.primary_action("Where is my order?")
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "support-tier1" in AGENT_REGISTRY

    def test_nim_timeout_falls_back_gracefully(self, tier1_agent):
        """Test that NIM timeout falls back gracefully."""
        from ghostagency.core.exceptions import LLMTimeoutError

        # Mock the entire _call_llm method to simulate timeout
        with patch.object(tier1_agent, "_call_llm", side_effect=LLMTimeoutError("timeout")):
            result = tier1_agent.primary_action("Hello")
        assert isinstance(result, str)  # Must not raise

    def test_logs_written_on_interaction(self, tier1_agent, mock_nim):
        """Test that interactions are logged."""
        # Mock the logger to avoid file system operations
        with patch.object(tier1_agent.logger, "info") as mock_log:
            tier1_agent.primary_action("Test message")

            # Check that logger was called
            mock_log.assert_called_once()

    def test_escalation_detection(self, tier1_agent):
        """Test that escalation is detected correctly."""
        # Should detect escalation
        assert tier1_agent._needs_escalation("I don't know the answer")
        assert tier1_agent._needs_escalation("This is complex, needs specialist")

        # Should not detect escalation
        assert not tier1_agent._needs_escalation("Shipping takes 3-5 days")
        assert not tier1_agent._needs_escalation("Yes, that's covered under warranty")

    def test_get_role_prompt_includes_client_name(self, tier1_agent):
        """Test that role prompt includes client name."""
        prompt = tier1_agent.get_role_prompt()
        assert "TestCo" in prompt
        assert "Tier 1 Support Agent" in prompt


class TestSupportTier2Agent:
    def test_primary_action_returns_string(self, tier2_agent, mock_nim):
        """Test that primary_action returns a string response."""
        result = tier2_agent.primary_action(
            "Complex technical issue", escalated_from="support-tier1"
        )
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "support-tier2" in AGENT_REGISTRY

    def test_nim_timeout_falls_back_gracefully(self, tier2_agent):
        """Test that NIM timeout falls back gracefully."""
        from ghostagency.core.exceptions import LLMTimeoutError

        # Mock the entire _call_llm method to simulate timeout
        with patch.object(tier2_agent, "_call_llm", side_effect=LLMTimeoutError("timeout")):
            result = tier2_agent.primary_action("Hello")
        assert isinstance(result, str)  # Must not raise

    def test_specialist_escalation_detection(self, tier2_agent):
        """Test that specialist escalation is detected correctly."""
        # Should detect specialist escalation
        assert tier2_agent._needs_specialist_escalation("specialist required for this issue")
        assert tier2_agent._needs_specialist_escalation("Please escalate to engineering team")
        assert tier2_agent._needs_specialist_escalation("This is a security issue")

        # Should not detect specialist escalation
        assert not tier2_agent._needs_specialist_escalation("Here's how to fix this common issue")
        assert not tier2_agent._needs_specialist_escalation(
            "This can be resolved by clearing cache"
        )

    def test_get_role_prompt_includes_client_name(self, tier2_agent):
        """Test that role prompt includes client name."""
        prompt = tier2_agent.get_role_prompt()
        assert "TestCo" in prompt
        assert "Tier 2 Support Agent" in prompt

    def test_escalation_with_context(self, tier2_agent, mock_nim):
        """Test that escalation context is handled properly."""
        result = tier2_agent.primary_action(
            "Critical system bug",
            customer_email="user@test.com",
            escalated_from="support-tier1",
        )
        assert isinstance(result, str)


class TestSupportBillingAgent:
    def test_primary_action_returns_string(self, billing_agent, mock_nim):
        """Test that primary_action returns a string response."""
        result = billing_agent.primary_action("I need help with my invoice")
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "support-billing" in AGENT_REGISTRY
        assert AGENT_REGISTRY["support-billing"] == SupportBillingAgent

    def test_nim_timeout_falls_back_gracefully(self, billing_agent):
        """Test that NIM timeout falls back gracefully."""
        from ghostagency.core.exceptions import LLMTimeoutError

        # Mock the entire _call_llm method to simulate timeout
        with patch.object(billing_agent, "_call_llm", side_effect=LLMTimeoutError("timeout")):
            result = billing_agent.primary_action("Billing question")
        assert isinstance(result, str)  # Must not raise

    def test_billing_escalation_detection(self, billing_agent):
        """Test that billing escalation is detected correctly."""
        # Should detect billing escalation
        assert billing_agent._needs_billing_escalation(
            "I want to dispute a charge", "test response"
        )
        assert billing_agent._needs_billing_escalation("This is fraud!", "test response")
        assert billing_agent._needs_billing_escalation("I need a large refund", "test response")
        assert billing_agent._needs_billing_escalation(
            "I'm very angry about my bill", "test response"
        )

        # Should not detect billing escalation
        assert not billing_agent._needs_billing_escalation("Where is my invoice?", "test response")
        assert not billing_agent._needs_billing_escalation(
            "Can I update my payment method?", "test response"
        )

    def test_get_role_prompt_includes_billing_keywords(self, billing_agent):
        """Test that role prompt includes billing-specific content."""
        prompt = billing_agent.get_role_prompt()
        assert "billing" in prompt.lower()
        assert "payment" in prompt.lower()
        assert "invoice" in prompt.lower()
        assert "refund" in prompt.lower()
        assert "subscription" in prompt.lower()

    def test_agent_attributes_correct(self, billing_agent):
        """Test that agent attributes are set correctly."""
        assert billing_agent.agent_slug == "support-billing"
        assert billing_agent.squad == "support"
        assert billing_agent.display_name == "Support Billing Agent"
        assert billing_agent.price_tier == "$700/month"

    def test_escalation_with_billing_contact(self, billing_agent, mock_nim):
        """Test that billing escalation works with contact email."""
        billing_agent.billing_contact_email = "specialist@testco.com"
        result = billing_agent.primary_action("I need to dispute a fraudulent charge")
        assert isinstance(result, str)
        # Should not raise even with escalation logic
