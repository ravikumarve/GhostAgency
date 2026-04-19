from __future__ import annotations

import sys

from ghostagency.core.agent_registry import AGENT_REGISTRY, TOTAL_AGENTS
from ghostagency.core.base_agent import AIAgent


REQUIRED_CLASS_ATTRS = ("agent_slug", "squad", "display_name", "price_tier")


def validate_registry() -> None:
    """Validate the agent registry and exit with appropriate code."""
    count = len(AGENT_REGISTRY)
    errors: list[str] = []

    # Check count
    if count != TOTAL_AGENTS:
        errors.append(f"Registry has {count} agents, expected {TOTAL_AGENTS}")

    # Check each entry
    for slug, cls in AGENT_REGISTRY.items():
        # Must inherit AIAgent
        if not issubclass(cls, AIAgent):
            errors.append(f"'{slug}' does not inherit AIAgent")

        # Must have all required class attributes
        for attr in REQUIRED_CLASS_ATTRS:
            if not hasattr(cls, attr):
                errors.append(f"'{slug}' missing required class attribute: {attr}")

    if errors:
        print("[FAIL] Registry validation failed:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print(f"[OK] Registry valid: {count} agents, all inherit AIAgent")


if __name__ == "__main__":
    validate_registry()
