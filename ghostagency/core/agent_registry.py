from __future__ import annotations
from typing import Type

from ghostagency.core.base_agent import AIAgent

# Import agent classes
from ghostagency.agents.squad_support.support_tier1 import SupportTier1Agent

AGENT_REGISTRY: dict[str, Type[AIAgent]] = {
    # Support Squad
    "support-tier1": SupportTier1Agent,
    # More agents will be added here as they are implemented
}

TOTAL_AGENTS = 156


def get_agent(slug: str) -> Type[AIAgent]:
    """Get agent class by slug."""
    if slug not in AGENT_REGISTRY:
        raise KeyError(
            f"Agent '{slug}' not found. Run `python scripts/list_agents.py` to see all {TOTAL_AGENTS}."
        )
    return AGENT_REGISTRY[slug]


def validate_registry() -> bool:
    """Validate registry integrity - must contain exactly 156 agents."""
    count = len(AGENT_REGISTRY)
    assert count == TOTAL_AGENTS, (
        f"Registry has {count} agents, expected {TOTAL_AGENTS}"
    )
    return True


def list_agents() -> list[dict]:
    """List all registered agents with their details."""
    agents = []
    for slug, agent_class in AGENT_REGISTRY.items():
        agents.append(
            {
                "slug": slug,
                "class_name": agent_class.__name__,
                "squad": getattr(agent_class, "squad", "unknown"),
                "display_name": getattr(agent_class, "display_name", "Unknown"),
                "price_tier": getattr(agent_class, "price_tier", "Unknown"),
            }
        )
    return agents
