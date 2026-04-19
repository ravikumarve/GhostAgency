from __future__ import annotations

from ghostagency.core.agent_registry import AGENT_REGISTRY, TOTAL_AGENTS


def list_agents() -> None:
    """Print a formatted table of all registered agents."""
    slug_width = 28
    squad_width = 12
    name_width = 30
    price_width = 14
    status_width = 12

    header = (
        f"{'Slug':<{slug_width}} | "
        f"{'Squad':<{squad_width}} | "
        f"{'Display Name':<{name_width}} | "
        f"{'Price Tier':<{price_width}} | "
        f"{'Status':<{status_width}}"
    )
    separator = "-" * len(header)

    print(separator)
    print(header)
    print(separator)

    for slug, cls in AGENT_REGISTRY.items():
        squad = getattr(cls, "squad", "unknown")
        display_name = getattr(cls, "display_name", "Unknown")
        price_tier = getattr(cls, "price_tier", "Unknown")
        status = "registered"

        print(
            f"{slug:<{slug_width}} | "
            f"{squad:<{squad_width}} | "
            f"{display_name:<{name_width}} | "
            f"{price_tier:<{price_width}} | "
            f"{status:<{status_width}}"
        )

    print(separator)
    print(f"Total: {len(AGENT_REGISTRY)} / {TOTAL_AGENTS} agents")
    print(separator)


if __name__ == "__main__":
    list_agents()
