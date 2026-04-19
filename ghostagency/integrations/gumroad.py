from __future__ import annotations
import os
from typing import Dict, Any

# Gumroad configuration
GUMROAD_PRODUCT_ID = os.getenv("GUMROAD_PRODUCT_ID", "")
GUMROAD_ACCESS_TOKEN = os.getenv("GUMROAD_ACCESS_TOKEN", "")


def validate_license_key(license_key: str) -> bool:
    """
    Validate a Gumroad license key.

    In production, this would make an API call to Gumroad.
    For development, we can use a simple mock validation.
    """
    # Mock validation for development
    if os.getenv("GHOST_MOCK_AUTH", "false").lower() == "true":
        return True

    # TODO: Implement actual Gumroad API integration
    # For now, return True if we're not in production mode
    if not GUMROAD_ACCESS_TOKEN or not GUMROAD_PRODUCT_ID:
        return True

    # Placeholder for actual Gumroad validation
    # This would make an API call to Gumroad's license verification endpoint
    return True


def get_license_info(license_key: str) -> Dict[str, Any]:
    """Get information about a license key."""
    # Mock response for development
    return {
        "valid": True,
        "product_id": GUMROAD_PRODUCT_ID,
        "purchase_id": "mock_purchase_id",
        "created_at": "2024-01-01T00:00:00Z",
        "variants": "full-access",
    }
