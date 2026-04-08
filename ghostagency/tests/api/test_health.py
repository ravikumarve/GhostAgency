import pytest
from fastapi import status


class TestHealthEndpoints:
    """Test health check and metrics endpoints."""

    def test_health_check_success(self, test_client):
        """Test that health check endpoint returns healthy status."""
        response = test_client.get("/api/v1/health")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {
            "status": "healthy",
            "message": "Ghost Agency API is running",
        }

    def test_health_check_no_auth_required(self, test_client):
        """Test that health endpoint doesn't require authentication."""
        response = test_client.get("/api/v1/health", headers={})

        assert response.status_code == status.HTTP_200_OK
        assert "healthy" in response.json()["status"]

    def test_metrics_endpoint_success(self, test_client):
        """Test that metrics endpoint returns basic metrics."""
        response = test_client.get("/api/v1/metrics")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "agents_registered" in data
        assert "agents_total" in data
        assert "status" in data
        assert data["agents_total"] == 156

    def test_metrics_endpoint_no_auth_required(self, test_client):
        """Test that metrics endpoint doesn't require authentication."""
        response = test_client.get("/api/v1/metrics", headers={})

        assert response.status_code == status.HTTP_200_OK
        assert "agents_registered" in response.json()

    def test_health_endpoints_cors_enabled(self, test_client):
        """Test that CORS is enabled for health endpoints."""
        response = test_client.options(
            "/api/v1/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
                "Access-Control-Request-Headers": "Content-Type",
            },
        )

        assert response.status_code == status.HTTP_200_OK
        assert "access-control-allow-origin" in response.headers

    def test_metrics_endpoint_structure(self, test_client):
        """Test that metrics endpoint has expected structure."""
        response = test_client.get("/api/v1/metrics")
        data = response.json()

        assert isinstance(data["agents_registered"], int)
        assert isinstance(data["agents_total"], int)
        assert isinstance(data["status"], str)
        assert data["agents_total"] >= data["agents_registered"]
