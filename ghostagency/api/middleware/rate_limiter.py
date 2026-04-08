from __future__ import annotations
import os
from typing import Dict, List
from datetime import datetime, timedelta
from fastapi import HTTPException, Request, status


class RateLimiter:
    """Simple in-memory rate limiter."""

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, List[datetime]] = {}

    async def check_rate_limit(self, request: Request, identifier: str) -> None:
        """Check if the request exceeds the rate limit."""
        current_time = datetime.now()

        # Clean up old requests
        one_minute_ago = current_time - timedelta(minutes=1)
        if identifier in self.requests:
            self.requests[identifier] = [
                req_time
                for req_time in self.requests[identifier]
                if req_time > one_minute_ago
            ]
        else:
            self.requests[identifier] = []

        # Check if limit exceeded
        if len(self.requests[identifier]) >= self.requests_per_minute:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )

        # Add current request
        self.requests[identifier].append(current_time)


# Global rate limiter instance
rate_limiter = RateLimiter(
    requests_per_minute=int(os.getenv("RATE_LIMIT_REQUESTS_PER_MINUTE", "60"))
)


def get_client_identifier(request: Request) -> str:
    """Get a unique identifier for the client."""
    # Use license key if available, otherwise use IP
    license_key = request.headers.get("Authorization", "")
    if license_key and license_key.startswith("Bearer "):
        return license_key[7:]  # Remove "Bearer " prefix

    # Fallback to IP address
    return request.client.host if request.client else "unknown"
