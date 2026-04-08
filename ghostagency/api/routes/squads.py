from __future__ import annotations
from typing import Dict, List
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from ghostagency.core.agent_registry import AGENT_REGISTRY
from ghostagency.api.middleware.auth import auth_scheme

router = APIRouter(tags=["squads"])


@router.get("/squads")
async def list_squads(_: str = Depends(auth_scheme)) -> JSONResponse:
    """List all squads and their agent counts."""
    squad_counts: Dict[str, int] = {}

    for agent_class in AGENT_REGISTRY.values():
        squad = agent_class.squad
        squad_counts[squad] = squad_counts.get(squad, 0) + 1

    squads_list = []
    for squad, count in squad_counts.items():
        squads_list.append(
            {
                "name": squad,
                "agent_count": count,
                "display_name": squad.replace("_", " ").title(),
            }
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "squads": squads_list,
            "total_agents": sum(squad_counts.values()),
        },
    )


@router.get("/squads/{squad_name}")
async def get_squad_agents(
    squad_name: str, _: str = Depends(auth_scheme)
) -> JSONResponse:
    """Get all agents in a specific squad."""
    squad_agents = []

    for slug, agent_class in AGENT_REGISTRY.items():
        if agent_class.squad == squad_name:
            squad_agents.append(
                {
                    "slug": slug,
                    "display_name": agent_class.display_name,
                    "price_tier": agent_class.price_tier,
                    "version": getattr(agent_class, "version", "1.0.0"),
                }
            )

    if not squad_agents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Squad '{squad_name}' not found or has no agents",
        )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "squad": squad_name,
            "display_name": squad_name.replace("_", " ").title(),
            "agent_count": len(squad_agents),
            "agents": squad_agents,
        },
    )


@router.post("/squads/{squad_name}/execute")
async def execute_squad_agent(
    squad_name: str,
    agent_role: str,
    input: str,
    client_name: str = "default-client",
    knowledge_base_path: str | None = None,
    _: str = Depends(auth_scheme),
) -> JSONResponse:
    """Execute the first agent found in a squad that matches a role pattern."""
    matching_agents = []

    for slug, agent_class in AGENT_REGISTRY.items():
        if (
            agent_class.squad == squad_name
            and agent_role.lower() in agent_class.display_name.lower()
        ):
            matching_agents.append((slug, agent_class))

    if not matching_agents:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No agents in squad '{squad_name}' match role '{agent_role}'",
        )

    # Use the first matching agent
    agent_slug, agent_class = matching_agents[0]
    agent_instance = agent_class(
        client_name=client_name,
        knowledge_base_path=knowledge_base_path,
    )

    result = agent_instance.primary_action(input)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "squad": squad_name,
            "agent": agent_slug,
            "input": input,
            "result": result,
            "client": client_name,
            "matched_agents": len(matching_agents),
        },
    )
