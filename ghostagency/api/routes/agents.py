from __future__ import annotations
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from ghostagency.core.agent_registry import get_agent, AGENT_REGISTRY
from ghostagency.core.base_agent import AIAgent
from ghostagency.api.middleware.auth import auth_scheme

router = APIRouter(tags=["agents"])


@router.get("/agents")
async def list_agents(_: str = Depends(auth_scheme)) -> JSONResponse:
    """List all available agents."""
    agents_list = []
    for slug, agent_class in AGENT_REGISTRY.items():
        agents_list.append(
            {
                "slug": slug,
                "display_name": agent_class.display_name,
                "squad": agent_class.squad,
                "price_tier": agent_class.price_tier,
                "version": getattr(agent_class, "version", "1.0.0"),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"count": len(agents_list), "total": 156, "agents": agents_list},
    )


@router.get("/agents/{agent_slug}")
async def get_agent_info(
    agent_slug: str, _: str = Depends(auth_scheme)
) -> JSONResponse:
    """Get detailed information about a specific agent."""
    try:
        agent_class = get_agent(agent_slug)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "slug": agent_slug,
                "display_name": agent_class.display_name,
                "squad": agent_class.squad,
                "price_tier": agent_class.price_tier,
                "version": getattr(agent_class, "version", "1.0.0"),
            },
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_slug}' not found",
        )


@router.post("/agents/{agent_slug}/execute")
async def execute_agent(
    agent_slug: str,
    input: str,
    client_name: str = "default-client",
    knowledge_base_path: str | None = None,
    _: str = Depends(auth_scheme),
) -> JSONResponse:
    """Execute an agent with the given input."""
    try:
        agent_class = get_agent(agent_slug)
        agent_instance = agent_class(
            client_name=client_name,
            knowledge_base_path=knowledge_base_path,
        )

        result = agent_instance.primary_action(input)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "agent": agent_slug,
                "input": input,
                "result": result,
                "client": client_name,
            },
        )
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{agent_slug}' not found",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Agent execution failed: {str(e)}",
        )
