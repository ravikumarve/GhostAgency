from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from ghostagency.api.routes import agents, squads, health, dashboard
from ghostagency.core.config import API_PREFIX


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Ghost Agency API",
        description="REST API and Dashboard for Ghost Agency's AI agents",
        version="1.0.0",
        docs_url=f"{API_PREFIX}/docs",
        redoc_url=f"{API_PREFIX}/redoc",
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routers (under API_PREFIX)
    app.include_router(agents.router, prefix=API_PREFIX)
    app.include_router(squads.router, prefix=API_PREFIX)
    app.include_router(health.router, prefix=API_PREFIX)

    # Include dashboard routes (at root level)
    app.include_router(dashboard.router)

    # Mount static files
    static_dir = Path(__file__).parent.parent.parent / "static"
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
