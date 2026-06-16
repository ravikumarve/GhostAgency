"""Tests for Finance Squad Agents."""

import pytest
from unittest.mock import patch

from ghostagency.agents.squad_finance.finance_invoicing import FinanceInvoicingAgent


@pytest.fixture
def agent():
    """Create a FinanceInvoicingAgent instance for testing."""
    return FinanceInvoicingAgent(
        client_name="TestCo",
        knowledge_base_path=None,
    )


@pytest.fixture
def mock_nim():
    """Patch NIMClient.complete to return a canned response."""
    with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
        m.return_value = "Invoice generated successfully."
        yield m


class TestFinanceInvoicingAgent:
    def test_primary_action_returns_string(self, agent, mock_nim):
        """Test that primary_action returns a string response."""
        result = agent.primary_action("Generate monthly expense report")
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "finance-invoicing" in AGENT_REGISTRY

    def test_agent_has_correct_attributes(self):
        """Test that the agent has required class attributes."""
        assert FinanceInvoicingAgent.agent_slug == "finance-invoicing"
        assert FinanceInvoicingAgent.squad == "finance"
        assert FinanceInvoicingAgent.display_name == "Finance Invoicing Agent"
        assert FinanceInvoicingAgent.price_tier == "$800/month"

    def test_llm_failure_returns_error_message(self, agent):
        """Test that LLM failure returns a fallback error message."""
        with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
            m.side_effect = Exception("LLM connection failed")
            result = agent.primary_action("Process payroll")
        assert isinstance(result, str) and len(result) > 0
        assert "apologize" in result.lower() or "technical difficulties" in result.lower()

    def test_generate_invoice_returns_string(self, agent, mock_nim):
        """Test that generate_invoice returns a string response."""
        items = [
            {"description": "Web Development", "amount": 5000.00},
            {"description": "Hosting", "amount": 200.00},
        ]
        result = agent.generate_invoice("Acme Corp", items, "2026-07-01")
        assert isinstance(result, str) and len(result) > 0

    def test_get_role_prompt_returns_string(self, agent):
        """Test that get_role_prompt returns a non-empty string."""
        prompt = agent.get_role_prompt()
        assert isinstance(prompt, str) and len(prompt) > 0
        assert "TestCo" in prompt
