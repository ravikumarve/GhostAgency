"""Shared test fixtures for Ghost Agency tests."""

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient

from ghostagency.api.main import create_app


@pytest.fixture
def test_client():
    """Create a test client for the FastAPI app."""
    return TestClient(create_app())


@pytest.fixture
def mock_auth():
    """Mock authentication to bypass license key validation."""
    with patch("ghostagency.api.middleware.auth.validate_license_key") as mock:
        mock.return_value = True
        yield mock


@pytest.fixture
def mock_agent_execution():
    """Mock agent execution to avoid actual LLM calls."""
    with patch("ghostagency.core.base_agent.AIAgent.primary_action") as mock:
        mock.return_value = "Mocked agent response"
        yield mock


@pytest.fixture
def mock_rate_limiter():
    """Mock rate limiter to disable rate limiting in tests."""
    with patch("ghostagency.api.middleware.rate_limiter.RateLimiter.check_rate_limit") as mock:
        yield mock


@pytest.fixture
def valid_license_key():
    """Return a valid license key for testing."""
    return "valid-license-key-123"


@pytest.fixture
def invalid_license_key():
    """Return an invalid license key for testing."""
    return "invalid-license-key"


@pytest.fixture
def test_headers(valid_license_key):
    """Return headers with valid authentication."""
    return {"Authorization": f"Bearer {valid_license_key}"}


@pytest.fixture
def test_agent_data():
    """Return sample agent data for testing."""
    return {
        "slug": "support-tier1",
        "display_name": "Support Tier 1 Agent",
        "squad": "support",
        "price_tier": "$800/mo",
        "version": "1.0.0",
    }


@pytest.fixture
def test_squad_data():
    """Return sample squad data for testing."""
    return {
        "name": "support",
        "display_name": "Support",
        "agent_count": 18,
        "agents": [],
    }
