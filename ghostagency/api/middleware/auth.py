from typing import Optional
from fastapi import HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ghostagency.integrations.gumroad import validate_license_key


class LicenseKeyAuth(HTTPBearer):
    """Middleware for Gumroad license key authentication."""

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)

        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme",
                )

            license_key = credentials.credentials

            # Validate license key with Gumroad
            is_valid = validate_license_key(license_key)

            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid or expired license key",
                )

            return license_key

        return None


# Create auth instance
auth_scheme = LicenseKeyAuth()
