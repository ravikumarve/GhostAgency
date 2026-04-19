from __future__ import annotations

import os
import sys
from collections import defaultdict
from typing import Any

from ghostagency.core.agent_registry import AGENT_REGISTRY, TOTAL_AGENTS


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


def group_by_squad(registry: dict[str, type]) -> dict[str, list[tuple[str, type]]]:
    """Group agent entries by their squad class attribute."""
    squads: dict[str, list[tuple[str, type]]] = defaultdict(list)
    for slug, cls in registry.items():
        squad = getattr(cls, "squad", "unknown")
        squads[squad].append((slug, cls))
    return squads


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


def run_demo() -> None:
    """Run the full interactive demo across all registered agents."""
    squads = group_by_squad(AGENT_REGISTRY)

    print("=" * 70)
    print("GHOST AGENCY - Full Interactive Demo")
    print("=" * 70)
    print(f"Total agents in registry: {TOTAL_AGENTS}")
    print(f"Mock AI mode: {os.getenv('GHOST_MOCK_AI', 'false')}")
    print("=" * 70)
    print()

    successes = 0
    failures = 0
    results: list[dict[str, str]] = []

    for squad_name in sorted(squads.keys()):
        agents_in_squad = squads[squad_name]
        print(f"--- {squad_name.upper()} SQUAD ({len(agents_in_squad)} agent(s)) ---")
        print()

        for slug, cls in agents_in_squad:
            display_name = getattr(cls, "display_name", "Unknown")
            try:
                agent = instantiate_agent(slug, cls)
                response = call_agent(agent, slug, squad_name)
                successes += 1
                status = "[OK]"
                results.append(
                    {"slug": slug, "name": display_name, "status": "OK", "response": response}
                )
                print(f"  [{status}] {slug} ({display_name})")
                print(f"         Response: {response[:120]}...")
            except Exception as exc:
                failures += 1
                status = "[FAIL]"
                error_msg = str(exc)
                results.append(
                    {
                        "slug": slug,
                        "name": display_name,
                        "status": "FAIL",
                        "response": error_msg,
                    }
                )
                print(f"  [{status}] {slug} ({display_name})")
                print(f"         Error: {error_msg[:120]}")

            print()

    # --- Summary ---
    print("=" * 70)
    print("DEMO SUMMARY")
    print("=" * 70)
    print(f"Total agents:  {TOTAL_AGENTS}")
    print(f"Successes:     {successes}")
    print(f"Failures:      {failures}")
    print("=" * 70)

    if failures > 0:
        print("\nFailed agents:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"  - {r['slug']}: {r['response'][:80]}")

    sys.exit(1 if failures > 0 else 0)


if __name__ == "__main__":
    run_demo()
