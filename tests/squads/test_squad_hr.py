"""Tests for HR Squad Agents."""

import pytest
from unittest.mock import patch

from ghostagency.agents.squad_hr.hr_recruiting import HRRecruitingAgent


@pytest.fixture
def agent():
    """Create an HRRecruitingAgent instance for testing."""
    return HRRecruitingAgent(
        client_name="TestCo",
        knowledge_base_path=None,
    )


@pytest.fixture
def mock_nim():
    """Patch NIMClient.complete to return a canned response."""
    with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
        m.return_value = "Candidate screened: Strong fit."
        yield m


class TestHRRecruitingAgent:
    def test_primary_action_returns_string(self, agent, mock_nim):
        """Test that primary_action returns a string response."""
        result = agent.primary_action("Create onboarding plan for new engineer")
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "hr-recruiting" in AGENT_REGISTRY

    def test_agent_has_correct_attributes(self):
        """Test that the agent has required class attributes."""
        assert HRRecruitingAgent.agent_slug == "hr-recruiting"
        assert HRRecruitingAgent.squad == "hr"
        assert HRRecruitingAgent.display_name == "HR Recruiting Agent"
        assert HRRecruitingAgent.price_tier == "$900/month"

    def test_llm_failure_returns_error_message(self, agent):
        """Test that LLM failure returns a fallback error message."""
        with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
            m.side_effect = Exception("LLM connection failed")
            result = agent.primary_action("Review job posting")
        assert isinstance(result, str) and len(result) > 0
        assert "apologize" in result.lower() or "technical difficulties" in result.lower()

    def test_screen_candidate_returns_string(self, agent, mock_nim):
        """Test that screen_candidate returns a string response."""
        result = agent.screen_candidate(
            resume_text="5 years Python experience, MIT graduate",
            job_requirements="Senior Python developer, 3+ years experience",
        )
        assert isinstance(result, str) and len(result) > 0

    def test_screen_candidate_with_empty_resume(self, agent, mock_nim):
        """Test screen_candidate with minimal input."""
        result = agent.screen_candidate(resume_text="", job_requirements="Any position")
        assert isinstance(result, str) and len(result) > 0

    def test_get_role_prompt_returns_string(self, agent):
        """Test that get_role_prompt returns a non-empty string."""
        prompt = agent.get_role_prompt()
        assert isinstance(prompt, str) and len(prompt) > 0
        assert "TestCo" in prompt
