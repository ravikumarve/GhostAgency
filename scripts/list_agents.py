#!/usr/bin/env python3
"""
List all registered agents with their details.
"""

import sys
from pathlib import Path

# Add the ghostagency package to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ghostagency.core.agent_registry import list_agents


def main():
    """List all agents"""
    agents = list_agents()

    print("\n" + "=" * 80)
    print("GHOST AGENCY - REGISTERED AGENTS")
    print("=" * 80)
    print(f"Total agents: {len(agents)} (target: 156)")
    print("=" * 80)

    for agent in agents:
        print(f"\n🔹 {agent['display_name']}")
        print(f"   Slug: {agent['slug']}")
        print(f"   Squad: {agent['squad']}")
        print(f"   Price: {agent['price_tier']}")
        print(f"   Class: {agent['class_name']}")
        print("   -" * 20)

    print(f"\n✅ Registry validation: {len(agents)} agents registered")

    if len(agents) < 156:
        print(f"⚠️  Missing {156 - len(agents)} agents to reach target")
    elif len(agents) > 156:
        print(f"❌ Registry has {len(agents)} agents, expected 156")
    else:
        print("🎉 Perfect! All 156 agents registered")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
