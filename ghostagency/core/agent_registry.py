from __future__ import annotations
from typing import Type

from ghostagency.core.base_agent import AIAgent

# Import agent classes
from ghostagency.agents.squad_support.support_tier1 import SupportTier1Agent
from ghostagency.agents.squad_support.support_tier2 import SupportTier2Agent
from ghostagency.agents.squad_support.support_billing import SupportBillingAgent
from ghostagency.agents.squad_sales.sales_qualification import SalesQualificationAgent
from ghostagency.agents.squad_content.content_social_media import (
    ContentSocialMediaAgent,
)
from ghostagency.agents.squad_ops.ops_executive_assistant import (
    OpsExecutiveAssistantAgent,
)
from ghostagency.agents.squad_data.data_research import DataResearchAgent
from ghostagency.agents.squad_dev.dev_code_review import DevCodeReviewAgent
from ghostagency.agents.squad_finance.finance_invoicing import FinanceInvoicingAgent
from ghostagency.agents.squad_hr.hr_recruiting import HRRecruitingAgent
from ghostagency.agents.squad_legal.legal_contract_review import LegalContractReviewAgent
from ghostagency.agents.squad_custom.custom_generic import CustomGenericAgent

AGENT_REGISTRY: dict[str, Type[AIAgent]] = {
    # Support Squad
    "support-tier1": SupportTier1Agent,
    "support-tier2": SupportTier2Agent,
    "support-billing": SupportBillingAgent,
    # Sales Squad
    "sales-qualification": SalesQualificationAgent,
    # Content Squad
    "content-social-media": ContentSocialMediaAgent,
    # Operations Squad
    "ops-executive-assistant": OpsExecutiveAssistantAgent,
    # Data Squad
    "data-research": DataResearchAgent,
    # Dev Squad
    "dev-code-review": DevCodeReviewAgent,
    # Finance Squad
    "finance-invoicing": FinanceInvoicingAgent,
    # HR Squad
    "hr-recruiting": HRRecruitingAgent,
    # Legal Squad
    "legal-contract-review": LegalContractReviewAgent,
    # Custom Squad
    "custom-generic": CustomGenericAgent,
}

TOTAL_AGENTS = 12


def get_agent(slug: str) -> Type[AIAgent]:
    """Get agent class by slug."""
    if slug not in AGENT_REGISTRY:
        raise KeyError(
            f"Agent '{slug}' not found. "
            f"Run `python scripts/list_agents.py` to see all {TOTAL_AGENTS}."
        )
    return AGENT_REGISTRY[slug]


def validate_registry() -> bool:
    """Validate registry integrity - must contain exactly TOTAL_AGENTS agents."""
    count = len(AGENT_REGISTRY)
    assert count == TOTAL_AGENTS, f"Registry has {count} agents, expected {TOTAL_AGENTS}"
    return True


def list_agents() -> list[dict]:
    """List all registered agents with their details."""
    agents = []
    for slug, agent_class in AGENT_REGISTRY.items():
        agents.append(
            {
                "slug": slug,
                "agent_slug": getattr(agent_class, "agent_slug", "unknown"),
                "class_name": agent_class.__name__,
                "squad": getattr(agent_class, "squad", "unknown"),
                "display_name": getattr(agent_class, "display_name", "Unknown"),
                "price_tier": getattr(agent_class, "price_tier", "Unknown"),
            }
        )
    return agents
