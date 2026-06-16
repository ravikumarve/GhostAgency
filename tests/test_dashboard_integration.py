"""
Integration tests for dashboard functionality.
Tests the actual dashboard routes with proper fixtures.
"""

from fastapi import status
from unittest.mock import patch, MagicMock

from ghostagency.core.agent_registry import AGENT_REGISTRY


class TestDashboardIntegration:
    """Integration tests for dashboard routes."""

    def test_dashboard_route_returns_correct_counts(self, test_client, test_headers, mock_auth):
        """Test that dashboard route returns correct agent counts in context."""
        # Mock template rendering to avoid Jinja2 issues
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>test</html>"

        with patch("ghostagency.api.routes.dashboard.templates.get_template") as mock_get_template:
            mock_get_template.return_value = mock_template

            # Act
            response = test_client.get("/dashboard", headers=test_headers)

        # Assert
        assert response.status_code == status.HTTP_200_OK

        # Verify template was called with correct context
        mock_get_template.assert_called_once_with("index.html")
        call_args = mock_template.render.call_args
        context = call_args[1]  # kwargs passed to render

        assert context["total_agents"] == 12
        assert context["online_agents"] == 12
        assert context["offline_agents"] == 0

    def test_landing_page_route_returns_correct_context(self, test_client, test_headers, mock_auth):
        """Test that landing page route returns correct agent data."""
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>test</html>"

        with patch("ghostagency.api.routes.dashboard.templates.get_template") as mock_get_template:
            mock_get_template.return_value = mock_template

            response = test_client.get("/", headers=test_headers)

        assert response.status_code == status.HTTP_200_OK
        mock_get_template.assert_called_once_with("landing.html")
        call_args = mock_template.render.call_args
        context = call_args[1]

        assert context["total_agents"] == 12
        assert len(context["agents"]) == 12

    def test_agents_page_route_returns_correct_data(self, test_client, test_headers, mock_auth):
        """Test that agents page route returns correct agent data."""
        # Mock template rendering
        mock_template = MagicMock()
        mock_template.render.return_value = "<html>test</html>"

        with patch("ghostagency.api.routes.dashboard.templates.get_template") as mock_get_template:
            mock_get_template.return_value = mock_template

            # Act
            response = test_client.get("/agents", headers=test_headers)

        # Assert
        assert response.status_code == status.HTTP_200_OK

        # Verify template was called with correct context
        mock_get_template.assert_called_once_with("agents.html")
        call_args = mock_template.render.call_args
        context = call_args[1]  # kwargs passed to render

        assert context["total_agents"] == 12
        assert len(context["agents"]) == 12

        # Verify all agents have status field
        for agent in context["agents"]:
            assert agent["status"] == "online"

    def test_registry_integrity(self):
        """Test that agent registry contains exactly 12 agents."""
        # Act
        agent_count = len(AGENT_REGISTRY)

        # Assert
        assert agent_count == 12, f"Expected 12 agents in registry, found {agent_count}"

        # Verify specific agents exist
        expected_agents = [
            "support-tier1",
            "support-tier2",
            "support-billing",
            "sales-qualification",
            "content-social-media",
            "ops-executive-assistant",
            "data-research",
            "dev-code-review",
            "finance-invoicing",
            "hr-recruiting",
            "legal-contract-review",
            "custom-generic",
        ]

        for agent_slug in expected_agents:
            assert agent_slug in AGENT_REGISTRY, f"Agent {agent_slug} not found in registry"
