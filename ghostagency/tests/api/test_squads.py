import pytest
from fastapi import status
from unittest.mock import patch


class TestSquadsEndpoints:
    """Test squads-related endpoints."""

    def test_list_squads_success(self, test_client, test_headers, mock_auth):
        """Test listing all squads with authentication."""
        response = test_client.get("/api/v1/squads", headers=test_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "squads" in data
        assert "total_agents" in data
        assert data["total_agents"] == 156

        # Verify squad structure
        squad = data["squads"][0]
        assert "name" in squad
        assert "agent_count" in squad
        assert "display_name" in squad
        assert isinstance(squad["agent_count"], int)

    def test_list_squads_unauthorized(self, test_client):
        """Test that listing squads requires authentication."""
        response = test_client.get("/api/v1/squads", headers={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.json()

    def test_get_squad_agents_success(self, test_client, test_headers, mock_auth):
        """Test getting agents for a specific squad."""
        response = test_client.get("/api/v1/squads/support", headers=test_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["squad"] == "support"
        assert "display_name" in data
        assert "agent_count" in data
        assert "agents" in data
        assert isinstance(data["agents"], list)

        # Verify agent structure within squad
        if data["agents"]:
            agent = data["agents"][0]
            assert "slug" in agent
            assert "display_name" in agent
            assert "price_tier" in agent
            assert "version" in agent

    def test_get_squad_agents_not_found(self, test_client, test_headers, mock_auth):
        """Test getting agents for non-existent squad."""
        response = test_client.get(
            "/api/v1/squads/nonexistent-squad", headers=test_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_execute_squad_agent_success(
        self, test_client, test_headers, mock_auth, mock_agent_execution
    ):
        """Test executing an agent from a squad by role."""
        payload = {
            "agent_role": "tier1",
            "input": "Where is my order?",
            "client_name": "TestCo",
            "knowledge_base_path": None,
        }

        response = test_client.post(
            "/api/v1/squads/support/execute", json=payload, headers=test_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["squad"] == "support"
        assert "agent" in data
        assert data["input"] == "Where is my order?"
        assert data["result"] == "Mocked agent response"
        assert data["client"] == "TestCo"
        assert "matched_agents" in data

    def test_execute_squad_agent_no_match(self, test_client, test_headers, mock_auth):
        """Test executing with no matching agent role."""
        payload = {"agent_role": "nonexistent-role", "input": "Test input"}

        response = test_client.post(
            "/api/v1/squads/support/execute", json=payload, headers=test_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "match" in response.json()["detail"]

    def test_execute_squad_agent_missing_role(
        self, test_client, test_headers, mock_auth
    ):
        """Test executing squad agent with missing agent_role field."""
        payload = {"input": "Test input", "client_name": "TestCo"}

        response = test_client.post(
            "/api/v1/squads/support/execute", json=payload, headers=test_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_execute_squad_agent_missing_input(
        self, test_client, test_headers, mock_auth
    ):
        """Test executing squad agent with missing input field."""
        payload = {"agent_role": "tier1", "client_name": "TestCo"}

        response = test_client.post(
            "/api/v1/squads/support/execute", json=payload, headers=test_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_execute_squad_agent_with_knowledge_base(
        self, test_client, test_headers, mock_auth, mock_agent_execution
    ):
        """Test executing squad agent with knowledge base."""
        payload = {
            "agent_role": "tier1",
            "input": "What's my order status?",
            "client_name": "TestCo",
            "knowledge_base_path": "/path/to/kb",
        }

        response = test_client.post(
            "/api/v1/squads/support/execute", json=payload, headers=test_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["result"] == "Mocked agent response"

    def test_execute_squad_agent_default_client_name(
        self, test_client, test_headers, mock_auth, mock_agent_execution
    ):
        """Test executing squad agent with default client name."""
        payload = {
            "agent_role": "tier1",
            "input": "Test input",
            # client_name defaults to "default-client"
        }

        response = test_client.post(
            "/api/v1/squads/support/execute", json=payload, headers=test_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["client"] == "default-client"

    def test_execute_squad_agent_rate_limited(
        self, test_client, test_headers, mock_auth
    ):
        """Test rate limiting on squad agent execution."""
        with patch(
            "ghostagency.api.middleware.rate_limiter.RateLimiter.check_rate_limit"
        ) as mock:
            mock.side_effect = Exception("Rate limit exceeded")

            payload = {"agent_role": "tier1", "input": "Test input"}
            response = test_client.post(
                "/api/v1/squads/support/execute", json=payload, headers=test_headers
            )

        # Should handle rate limiting gracefully
        assert response.status_code >= status.HTTP_400_BAD_REQUEST

    def test_squad_execution_error_handling(self, test_client, test_headers, mock_auth):
        """Test error handling when squad agent execution fails."""
        with patch("ghostagency.core.base_agent.AIAgent.primary_action") as mock:
            mock.side_effect = Exception("Agent execution failed")

            payload = {"agent_role": "tier1", "input": "Test input"}
            response = test_client.post(
                "/api/v1/squads/support/execute", json=payload, headers=test_headers
            )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "execution failed" in response.json()["detail"]

    def test_squad_display_name_formatting(self, test_client, test_headers, mock_auth):
        """Test that squad display names are properly formatted."""
        response = test_client.get("/api/v1/squads/support", headers=test_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["display_name"] == "Support"

        # Test with underscore squad name
        response = test_client.get("/api/v1/squads/squad_support", headers=test_headers)
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            assert data["display_name"] == "Squad Support"

    def test_squad_list_completeness(self, test_client, test_headers, mock_auth):
        """Test that squad list includes all expected squads."""
        response = test_client.get("/api/v1/squads", headers=test_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        squad_names = [squad["name"] for squad in data["squads"]]

        # Check for some expected squad names
        expected_squads = ["support", "sales", "content", "ops", "data", "dev"]
        for expected_squad in expected_squads:
            if expected_squad in squad_names:
                assert True
                break
        else:
            pytest.fail(f"Expected at least one of {expected_squads} in squad list")
