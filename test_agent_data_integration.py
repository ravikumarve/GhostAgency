#!/usr/bin/env python3
"""
Test Script for Ghost Agency Dashboard Agent Data Integration

This script tests the real agent data integration to ensure:
1. get_real_agent_data() function works correctly
2. All required fields are present (slug, display_name, squad, price_tier, status)
3. Status is "online" for all agents
4. Data structure is suitable for dashboard templates
"""

import sys
from pathlib import Path

# 1. Import necessary modules
sys.path.insert(0, str(Path(__file__).parent))
from ghostagency.api.routes.dashboard import get_real_agent_data
from ghostagency.core.agent_registry import AGENT_REGISTRY


def main():
    """Run the integration test."""

    print("=" * 70)
    print("GHOST AGENCY - AGENT DATA INTEGRATION TEST")
    print("=" * 70)

    # 2. Call get_real_agent_data()
    print("\n📋 Calling get_real_agent_data()...")
    agents = get_real_agent_data()

    # 3. Print results to verify data structure
    print(f"✅ Retrieved {len(agents)} agents")
    print(f"✅ Registry contains {len(AGENT_REGISTRY)} agents")

    # Print sample data
    print(f"\n🔍 Sample agent data:")
    sample_agent = agents[0]
    for key, value in sample_agent.items():
        print(f"   {key}: {value}")

    # 4. Check required fields
    print(f"\n🔍 Checking required fields...")
    required_fields = {"slug", "display_name", "squad", "price_tier", "status"}

    all_fields_present = True
    for agent in agents:
        missing_fields = required_fields - set(agent.keys())
        if missing_fields:
            print(f"❌ Missing fields {missing_fields} for agent {agent['slug']}")
            all_fields_present = False

    if all_fields_present:
        print("✅ All required fields present")

    # 5. Verify status is "online" for all agents
    print(f"\n🔍 Checking agent statuses...")

    all_status_online = True
    for agent in agents:
        if agent["status"] != "online":
            print(
                f"❌ Agent {agent['slug']} has status '{agent['status']}', expected 'online'"
            )
            all_status_online = False

    if all_status_online:
        print("✅ All agents have status 'online'")

    # Additional validation
    print(f"\n🔍 Additional validation...")

    # Check field types
    type_issues = []
    for agent in agents:
        if not isinstance(agent.get("slug"), str):
            type_issues.append(f"slug not string: {agent.get('slug')}")
        if not isinstance(agent.get("display_name"), str):
            type_issues.append(f"display_name not string: {agent.get('display_name')}")
        if not isinstance(agent.get("squad"), str):
            type_issues.append(f"squad not string: {agent.get('squad')}")
        if not isinstance(agent.get("price_tier"), str):
            type_issues.append(f"price_tier not string: {agent.get('price_tier')}")
        if not isinstance(agent.get("status"), str):
            type_issues.append(f"status not string: {agent.get('status')}")

    if not type_issues:
        print("✅ All field types are correct")
    else:
        for issue in type_issues:
            print(f"❌ {issue}")

    # Check slug uniqueness
    slugs = [agent["slug"] for agent in agents]
    if len(slugs) == len(set(slugs)):
        print("✅ All slugs are unique")
    else:
        duplicates = {slug for slug in slugs if slugs.count(slug) > 1}
        print(f"❌ Duplicate slugs found: {duplicates}")

    # Summary
    print(f"\n" + "=" * 70)
    print("TEST RESULTS SUMMARY:")
    print(f"   Agents retrieved: {len(agents)}/{len(AGENT_REGISTRY)}")
    print(f"   All required fields present: {all_fields_present}")
    print(f"   All agents status 'online': {all_status_online}")
    print(f"   Field types correct: {not type_issues}")
    print(f"   Slugs unique: {len(slugs) == len(set(slugs))}")

    success = all(
        [
            len(agents) == len(AGENT_REGISTRY),
            all_fields_present,
            all_status_online,
            not type_issues,
            len(slugs) == len(set(slugs)),
        ]
    )

    if success:
        print(f"\n🎉 SUCCESS: All tests passed!")
        print("The get_real_agent_data() function works correctly.")
        print("Dashboard integration is ready for production.")
        print("You can safely update the todo status.")
        return 0
    else:
        print(f"\n❌ FAILURE: Some tests failed.")
        print("Please fix the implementation before updating todo status.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
