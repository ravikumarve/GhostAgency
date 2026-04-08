import pytest
from fastapi import status
from unittest.mock import patch


class TestAgentsEndpoints:
    """Test agents-related endpoints."""

    def test_list_agents_success(self, test_client, test_headers, mock_auth):
        """Test listing all agents with authentication."""
        response = test_client.get("/api/v1/agents", headers=test_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "count" in data
        assert "total" in data
        assert "agents" in data
        assert data["total"] == 156
        assert len(data["agents"]) == data["count"]

        # Verify agent structure
        agent = data["agents"][0]
        assert "slug" in agent
        assert "display_name" in agent
        assert "squad" in agent
        assert "price_tier" in agent
        assert "version" in agent

    def test_list_agents_unauthorized(self, test_client):
        """Test that listing agents requires authentication."""
        response = test_client.get("/api/v1/agents", headers={})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "detail" in response.json()

    def test_list_agents_invalid_license(self, test_client, invalid_license_key):
        """Test that invalid license key is rejected."""
        headers = {"Authorization": f"Bearer {invalid_license_key}"}

        with patch("ghostagency.api.middleware.auth.validate_license_key") as mock:
            mock.return_value = False
            response = test_client.get("/api/v1/agents", headers=headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Invalid or expired license key" in response.json()["detail"]

    def test_get_agent_info_success(
        self, test_client, test_headers, mock_auth, test_agent_data
    ):
        """Test getting specific agent information."""
        response = test_client.get("/api/v1/agents/support-tier1", headers=test_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["slug"] == "support-tier1"
        assert "display_name" in data
        assert "squad" in data
        assert "price_tier" in data
        assert "version" in data

    def test_get_agent_info_not_found(self, test_client, test_headers, mock_auth):
        """Test getting non-existent agent information."""
        response = test_client.get(
            "/api/v1/agents/nonexistent-agent", headers=test_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_execute_agent_success(
        self, test_client, test_headers, mock_auth, mock_agent_execution
    ):
        """Test executing an agent with valid input."""
        params = {
            "input": "Where is my order?",
            "client_name": "TestCo",
            "knowledge_base_path": None,
        }

        response = test_client.post(
            "/api/v1/agents/support-tier1/execute", params=params, headers=test_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["agent"] == "support-tier1"
        assert data["input"] == "Where is my order?"
        assert data["result"] == "Mocked agent response"
        assert data["client"] == "TestCo"

    def test_execute_agent_not_found(self, test_client, test_headers, mock_auth):
        """Test executing a non-existent agent."""
        params = {"input": "Test input"}

        response = test_client.post(
            "/api/v1/agents/nonexistent-agent/execute",
            params=params,
            headers=test_headers,
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["detail"]

    def test_execute_agent_missing_input(self, test_client, test_headers, mock_auth):
        """Test executing agent with missing input field."""
        params = {"client_name": "TestCo"}  # Missing 'input'

        response = test_client.post(
            "/api/v1/agents/support-tier1/execute", params=params, headers=test_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_execute_agent_rate_limited(self, test_client, test_headers, mock_auth):
        """Test rate limiting on agent execution."""
        with patch(
            "ghostagency.api.middleware.rate_limiter.RateLimiter.check_rate_limit"
        ) as mock:
            mock.side_effect = Exception("Rate limit exceeded")

            params = {"input": "Test input"}
            response = test_client.post(
                "/api/v1/agents/support-tier1/execute",
                params=params,
                headers=test_headers,
            )

        # Should handle rate limiting gracefully
        assert response.status_code >= status.HTTP_400_BAD_REQUEST

    def test_execute_agent_with_knowledge_base(
        self, test_client, test_headers, mock_auth, mock_agent_execution
    ):
        """Test executing agent with knowledge base path."""
        params = {
            "input": "What's my order status?",
            "client_name": "TestCo",
            "knowledge_base_path": "/path/to/kb",
        }

        response = test_client.post(
            "/api/v1/agents/support-tier1/execute", params=params, headers=test_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["result"] == "Mocked agent response"

    def test_execute_agent_default_client_name(
        self, test_client, test_headers, mock_auth, mock_agent_execution
    ):
        """Test executing agent with default client name."""
        params = {"input": "极Test input"}  # client_name defaults to "default-client"

        response = test_client.post(
            "/api/v1/agents/support-tier1/execute", params=params, headers=test_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["client"] == "default-client"

    def test_agent_execution_error_handling(self, test_client, test_headers, mock_auth):
        """Test error handling when agent execution fails."""
        with patch("ghostagency.core.base_agent.AIAgent.primary_action") as mock:
            mock.side_effect = Exception("Agent execution failed")

            params = {"input": "Test input"}
            response = test_client.post(
                "/api/v1/agents/support-tier1/execute",
                params=params,
                headers=test_headers,
            )

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "execution failed" in response.json()["detail"]
