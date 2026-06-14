from __future__ import annotations
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from ghostagency.core.agent_registry import TOTAL_AGENTS, AGENT_REGISTRY

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy", "message": "Ghost Agency API is running"},
    )


@router.get("/metrics")
async def metrics() -> JSONResponse:
    """Basic metrics endpoint."""
    # TODO: Add real metrics
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"agents_registered": len(AGENT_REGISTRY), "agents_total": TOTAL_AGENTS, "status": "operational"},
    )
