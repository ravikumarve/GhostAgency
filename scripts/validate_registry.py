#!/usr/bin/env python3
"""
Validate agent registry integrity.
"""

import sys
from pathlib import Path

# Add the ghostagency package to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ghostagency.core.agent_registry import validate_registry, list_agents


def main():
    """Validate registry"""
    try:
        agents = list_agents()
        result = validate_registry()

        print("✅ Registry validation PASSED")
        print(f"✅ Total agents: {len(agents)} (expected: 156)")

        # Check agent attributes
        for agent in agents:
            required_attrs = ["agent_slug", "squad", "display_name", "price_tier"]
            for attr in required_attrs:
                if attr not in agent:
                    print(f"❌ Agent {agent['slug']} missing attribute: {attr}")
                    return False

        print("✅ All agents have required attributes")
        return True

    except AssertionError as e:
        print(f"❌ Registry validation FAILED: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
