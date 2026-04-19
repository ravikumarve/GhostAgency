from __future__ import annotations

import argparse
import os
import sys
from typing import Any

from ghostagency.core.agent_registry import AGENT_REGISTRY


# --- Sample inputs per squad ---
SQUAD_SAMPLE_INPUTS: dict[str, dict[str, Any]] = {
    "support": {
        "method": "primary_action",
        "args": ("Where is my order? It's been 5 days.",),
        "kwargs": {"customer_email": "customer@example.com"},
    },
    "sales": {
        "method": "primary_action",
        "args": (),
        "kwargs": {
            "lead_info": {
                "name": "Jane Smith",
                "company": "Acme Corp",
                "role": "CTO",
                "budget": "$50K",
                "timeline": "Q2",
            },
        },
    },
    "content": {
        "method": "primary_action",
        "args": (),
        "kwargs": {
            "platform": "twitter",
            "topic": "AI agents for business automation",
            "style": "engaging",
        },
    },
    "ops": {
        "method": "primary_action",
        "args": (),
        "kwargs": {
            "task_type": "draft_email",
            "recipient": "partner@firm.com",
            "purpose": "Partnership proposal",
            "key_points": ["mutual growth", "Q3 launch"],
        },
    },
}


def get_available_squads(registry: dict[str, type]) -> list[str]:
    """Return a sorted list of unique squad names from the registry."""
    squads: set[str] = set()
    for cls in registry.values():
        squad = getattr(cls, "squad", "unknown")
        squads.add(squad)
    return sorted(squads)


def filter_by_squad(registry: dict[str, type], squad_name: str) -> list[tuple[str, type]]:
    """Filter registry entries matching a given squad name."""
    return [
        (slug, cls)
        for slug, cls in registry.items()
        if getattr(cls, "squad", "unknown") == squad_name
    ]


def instantiate_agent(slug: str, cls: type) -> Any:
    """Instantiate an agent with the correct constructor arguments."""
    if slug == "ops-executive-assistant":
        return cls(client_name="DemoCorp", executive_name="CEO")
    return cls(client_name="DemoCorp")


def call_agent(agent: Any, slug: str, squad: str) -> str:
    """Call the agent's primary_action with squad-appropriate sample input."""
    sample = SQUAD_SAMPLE_INPUTS.get(squad)
    if sample is None:
        return agent.primary_action("Hello, can you help me?")

    method_name = sample["method"]
    args = sample["args"]
    kwargs = sample["kwargs"]

    method = getattr(agent, method_name)
    return method(*args, **kwargs)


def run_squad_demo(squad_name: str) -> None:
    """Run the demo for a single squad's agents."""
    agents_in_squad = filter_by_squad(AGENT_REGISTRY, squad_name)

    if not agents_in_squad:
        print(f"No agents found for squad: {squad_name}")
        sys.exit(1)

    print("=" * 70)
    print(f"GHOST AGENCY - Squad Demo: {squad_name.upper()}")
    print("=" * 70)
    print(f"Agents in squad: {len(agents_in_squad)}")
    print(f"Mock AI mode: {os.getenv('GHOST_MOCK_AI', 'false')}")
    print("=" * 70)
    print()

    successes = 0
    failures = 0

    for slug, cls in agents_in_squad:
        display_name = getattr(cls, "display_name", "Unknown")
        try:
            agent = instantiate_agent(slug, cls)
            response = call_agent(agent, slug, squad_name)
            successes += 1
            print(f"  [OK] {slug} ({display_name})")
            print(f"       Response: {response[:120]}...")
        except Exception as exc:
            failures += 1
            error_msg = str(exc)
            print(f"  [FAIL] {slug} ({display_name})")
            print(f"       Error: {error_msg[:120]}")

        print()

    # --- Summary ---
    print("=" * 70)
    print(f"SUMMARY for {squad_name.upper()} squad")
    print("=" * 70)
    print(f"Total agents:  {len(agents_in_squad)}")
    print(f"Successes:     {successes}")
    print(f"Failures:      {failures}")
    print("=" * 70)

    sys.exit(1 if failures > 0 else 0)


if __name__ == "__main__":
    available = get_available_squads(AGENT_REGISTRY)

    parser = argparse.ArgumentParser(description="Run a single squad's agents in demo mode.")
    parser.add_argument(
        "--squad",
        required=True,
        choices=available,
        help=f"Squad to demo. Available: {', '.join(available)}",
    )
    args = parser.parse_args()

    run_squad_demo(args.squad)
