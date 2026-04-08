"""Tests for ContentSocialMediaAgent — squad_content."""

import pytest
from unittest.mock import patch, Mock

from ghostagency.agents.squad_content.content_social_media import (
    ContentSocialMediaAgent,
)


@pytest.fixture
def agent():
    """Create a ContentSocialMediaAgent instance for testing."""
    return ContentSocialMediaAgent(client_name="TestCo", brand_voice_path=None)


@pytest.fixture
def mock_nim():
    """Patch NIMClient.complete to return a canned response."""
    with patch("ghostagency.integrations.nim_client.NIMClient.complete") as m:
        m.return_value = "Exciting news! Our new AI platform is transforming businesses. #AI #Innovation"
        yield m


class TestContentSocialMediaAgent:
    def test_primary_action_returns_string(self, agent, mock_nim):
        """Test that primary_action returns a string response."""
        result = agent.primary_action("linkedin", "AI innovation", "professional")
        assert isinstance(result, str) and len(result) > 0

    def test_agent_slug_is_registered(self):
        """Test that the agent slug is registered in the registry."""
        from ghostagency.core.agent_registry import AGENT_REGISTRY

        assert "content-social-media" in AGENT_REGISTRY

    def test_nim_timeout_falls_back_gracefully(self, agent):
        """Test that NIM timeout falls back gracefully."""
        from ghostagency.core.exceptions import LLMTimeoutError

        # Mock the entire _call_llm method to simulate timeout
        with patch.object(agent, "_call_llm", side_effect=LLMTimeoutError("timeout")):
            result = agent.primary_action("twitter", "Product launch", "engaging")
        assert isinstance(result, str)  # Must not raise

    def test_logs_written_on_interaction(self, agent, mock_nim):
        """Test that interactions are logged."""
        # Mock the logger to avoid file system operations
        with patch.object(agent.logger, "info") as mock_log:
            agent.primary_action("instagram", "Team celebration", "fun")

            # Check that logger was called
            mock_log.assert_called_once()

    def test_respond_to_comment_returns_string(self, agent, mock_nim):
        """Test that respond_to_comment returns a string."""
        comment = "This looks amazing! When will it be available?"
        response = agent.respond_to_comment(comment, "Product launch announcement")
        assert isinstance(response, str) and len(response) > 0

    def test_get_role_prompt_includes_client_name(self, agent):
        """Test that role prompt includes client name."""
        prompt = agent.get_role_prompt()
        assert "TestCo" in prompt
        assert "social media manager" in prompt

    def test_platform_guidelines_exist_for_major_platforms(self, agent):
        """Test that platform guidelines exist for major platforms."""
        platforms = [
            "twitter",
            "linkedin",
            "instagram",
            "facebook",
            "tiktok",
            "youtube",
        ]

        for platform in platforms:
            guidelines = agent._get_platform_guidelines(platform)
            assert isinstance(guidelines, str) and len(guidelines) > 0

    def test_platform_guidelines_default_for_unknown_platform(self, agent):
        """Test that unknown platforms get a default guideline."""
        guidelines = agent._get_platform_guidelines("unknown_platform")
        assert "engaging content" in guidelines

    def test_load_file_returns_empty_string_for_none_path(self, agent):
        """Test that _load_file returns empty string for None path."""
        result = agent._load_file(None)
        assert result == ""

    def test_load_file_returns_empty_string_for_invalid_path(self, agent):
        """Test that _load_file returns empty string for invalid path."""
        result = agent._load_file("/nonexistent/path.txt")
        assert result == ""
