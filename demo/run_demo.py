#!/usr/bin/env python3
"""
Ghost Agency Demo - Test the AI Agent Platform
"""

import os
import sys
from pathlib import Path

# Add the ghostagency package to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ghostagency.core.agent_registry import get_agent
from ghostagency.core.config import GHOST_MOCK_AI


def demo_support_tier1():
    """Demo Support Tier 1 Agent"""
    print("\n" + "=" * 60)
    print("DEMO: SUPPORT TIER 1 AGENT")
    print("=" * 60)

    # Create knowledge base directory
    kb_dir = Path("demo_kb/support")
    kb_dir.mkdir(parents=True, exist_ok=True)

    # Create sample knowledge base
    faq_content = """
SHIPPING POLICY:
- Free shipping on orders over $50
- Standard shipping: 5-7 business days
- Express shipping: 2-3 business days (additional $15)

RETURN POLICY:
- 30-day return window
- Items must be unused and in original packaging
- Refund processed within 5-7 business days

PRODUCT WARRANTY:
- All products come with 1-year warranty
- Covers manufacturing defects
- Does not cover normal wear and tear
"""

    with open(kb_dir / "faqs.txt", "w") as f:
        f.write(faq_content)

    # Initialize agent
    SupportAgent = get_agent("support-tier1")
    agent = SupportAgent(
        client_name="Demo E-commerce Store",
        knowledge_base_path=str(kb_dir),
        escalation_email="support@demo.com",
    )

    print(f"🤖 Agent: {agent.display_name}")
    print(f"💰 Price: {agent.price_tier}")
    print(f"🏢 Squad: {agent.squad}")
    print("=" * 60)

    # Test tickets
    test_tickets = [
        "How long does shipping take?",
        "Can I return a product after 45 days?",
        "My product broke after 2 months, is it covered under warranty?",
        "I need help with a very complex technical integration issue",
    ]

    for i, ticket in enumerate(test_tickets, 1):
        print(f"\n📝 Ticket #{i}: {ticket}")
        print("-" * 40)

        response = agent.primary_action(ticket, "customer@example.com")
        print(f"🤖 Response: {response}")

        if i < len(test_tickets):
            print("\n" + "-" * 60)


def main():
    """Main demo function"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║            GHOST AGENCY - AI AGENT PLATFORM              ║
║         Production-Grade Multi-Tenant SaaS               ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)

    if GHOST_MOCK_AI:
        print("🔧 Running in MOCK MODE (no real LLM calls)")
    else:
        print("⚠️  Running with REAL LLM calls - ensure NVIDIA NIM/Ollama is configured")

    from ghostagency.core.agent_registry import AGENT_REGISTRY, TOTAL_AGENTS

    print(
        f"\nTotal agents registered: {len(AGENT_REGISTRY)} (of {TOTAL_AGENTS} target)"
    )

    try:
        demo_support_tier1()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        if "NIM_API_KEY" in str(e):
            print(
                "\n💡 Tip: Set NIM_API_KEY in your .env file or use GHOST_MOCK_AI=true"
            )

    print("\n" + "=" * 60)
    print("DEMO COMPLETED")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback

        traceback.print_exc()
