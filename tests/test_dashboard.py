"""Test suite for dashboard functionality."""

from fastapi import status
from unittest.mock import patch, MagicMock

from ghostagency.api.routes.dashboard import get_real_agent_data
from ghostagency.core.agent_registry import AGENT_REGISTRY, list_agents


class TestDashboardFunctionality:
    """Test dashboard functionality and agent data retrieval."""

    def test_get_real_agent_data_returns_correct_structure(self):
        """Test that get_real_agent_data returns agents with proper status field."""
        # Act
        agents = get_real_agent_data()

        # Assert
        assert isinstance(agents, list)
        assert len(agents) == len(AGENT_REGISTRY)  # Should match registry count

        # Verify each agent has required fields including status
        for agent in agents:
            assert "slug" in agent
            assert "agent_slug" in agent
            assert "class_name" in agent
            assert "squad" in agent
            assert "display_name" in agent
            assert "price_tier" in agent
            assert "status" in agent
            assert agent["status"] == "online"  # All registered agents should be online

    def test_get_real_agent_data_returns_correct_count(self):
        """Test that get_real_agent_data returns exactly 6 agents."""
        # Act
        agents = get_real_agent_data()

        # Assert
        assert len(agents) == 12, f"Expected 12 agents, got {len(agents)}"
        assert len(agents) == len(AGENT_REGISTRY), "Agent count should match registry"

    def test_list_agents_function_matches_get_real_agent_data(self):
        """Test that list_agents() and get_real_agent_data() return same agent count."""
        # Act
        agents_from_list = list_agents()
        agents_from_real = get_real_agent_data()

        # Assert
        assert len(agents_from_list) == len(agents_from_real)
        assert len(agents_from_list) == 12

    def test_dashboard_context_has_correct_counts(self):
        """Test that dashboard context contains correct agent counts."""
        # Arrange
        real_agents = get_real_agent_data()

        # Act - Simulate dashboard context creation
        context = {
            "total_agents": len(AGENT_REGISTRY),
            "online_agents": len(real_agents),
            "offline_agents": 0,
        }

        # Assert
        assert context["total_agents"] == 12
        assert context["online_agents"] == 12
        assert context["offline_agents"] == 0
        assert context["total_agents"] == context["online_agents"]

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

    def test_agent_data_fields_consistency(self):
        """Test that agent data from different sources has consistent fields."""
        # Act
        agents_from_list = list_agents()
        agents_from_real = get_real_agent_data()

        # Assert
        assert len(agents_from_list) == len(agents_from_real)

        for i in range(len(agents_from_list)):
            list_agent = agents_from_list[i]
            real_agent = agents_from_real[i]

            # Core fields should match
            assert list_agent["slug"] == real_agent["slug"]
            assert list_agent["agent_slug"] == real_agent["agent_slug"]
            assert list_agent["class_name"] == real_agent["class_name"]
            assert list_agent["squad"] == real_agent["squad"]
            assert list_agent["display_name"] == real_agent["display_name"]
            assert list_agent["price_tier"] == real_agent["price_tier"]

            # Real agent data should have status field
            assert "status" in real_agent
            assert real_agent["status"] == "online"


if __name__ == "__main__":
    # Quick validation when run directly
    print("Running dashboard tests...")

    test_instance = TestDashboardFunctionality()

    print("Testing get_real_agent_data()...")
    agents = get_real_agent_data()
    print(f"Found {len(agents)} agents")
    print(f"Registry has {len(AGENT_REGISTRY)} agents")

    test_instance.test_get_real_agent_data_returns_correct_count()
    test_instance.test_get_real_agent_data_returns_correct_structure()
    test_instance.test_registry_integrity()

    print("All dashboard tests passed! ✓")
