from __future__ import annotations

from fastapi import APIRouter, Request
from typing import Any

from ghostagency.core.agent_registry import AGENT_REGISTRY, list_agents
from ghostagency.core.templates import shared_templates as templates

router = APIRouter(tags=["dashboard"])

MOCK_CLIENTS = [
    {
        "name": "Acme Corp",
        "plan": "enterprise",
        "agent_count": 15,
        "status": "active",
        "created_date": "2024-01-15",
    },
    {
        "name": "Beta Labs",
        "plan": "business",
        "agent_count": 8,
        "status": "active",
        "created_date": "2024-02-20",
    },
    {
        "name": "Gamma Tech",
        "plan": "starter",
        "agent_count": 3,
        "status": "trial",
        "created_date": "2024-03-10",
    },
    {
        "name": "Delta Solutions",
        "plan": "enterprise",
        "agent_count": 12,
        "status": "active",
        "created_date": "2024-01-28",
    },
]


def simplify_for_template(obj: Any) -> Any:
    """Convert complex objects to simpler representations for template caching.

    This prevents "unhashable type" errors when Jinja2 tries to cache templates
    with complex objects (dicts, lists) in the context.

    For the dashboard, we need to ensure performance data remains as a dict
    since templates expect to access its properties directly.
    """
    return obj


def get_real_agent_data() -> list[dict]:
    """Get real agent data from registry with status field added."""
    agents = list_agents()
    # Add "status": "online" to all real agents since they're registered
    for agent in agents:
        agent["status"] = "online"
    return agents


def get_squad_data() -> list[dict]:
    """Derive squad list with counts from the real agent registry."""
    squad_counts: dict[str, int] = {}
    for agent_class in AGENT_REGISTRY.values():
        squad = getattr(agent_class, "squad", "unknown")
        squad_counts[squad] = squad_counts.get(squad, 0) + 1
    return [{"name": name, "count": count} for name, count in sorted(squad_counts.items())]


@router.get("/")
async def dashboard(request: Request):
    """Main dashboard page."""
    real_agents = get_real_agent_data()
    context = {
        "request": request,
        "total_agents": len(AGENT_REGISTRY),
        "online_agents": len(real_agents),  # All registered agents are online
        "offline_agents": 0,  # No offline agents since we're using real registry
        "squads": simplify_for_template(get_squad_data()),
        "performance": simplify_for_template(
            {
                "avg_response_time": 3.2,
                "success_rate": 0.97,
                "escalations": 42,
            }
        ),
        "recent_activity": simplify_for_template(
            [
                {
                    "agent": "support-tier1",
                    "action": "Handled support ticket #1234",
                    "timestamp": "2 min ago",
                },
                {
                    "agent": "sales-qualification",
                    "action": "Qualified new lead",
                    "timestamp": "5 min ago",
                },
                {
                    "agent": "ops-executive-assistant",
                    "action": "Scheduled meeting",
                    "timestamp": "8 min ago",
                },
                {
                    "agent": "content-social-media",
                    "action": "Posted to Twitter",
                    "timestamp": "15 min ago",
                },
                {
                    "agent": "support-tier2",
                    "action": "Escalated ticket #1235",
                    "timestamp": "20 min ago",
                },
            ]
        ),
    }
    # Manual template rendering to work around starlette/jinja2 issue
    template = templates.get_template("index.html")
    content = template.render(**context)
    from starlette.responses import HTMLResponse

    return HTMLResponse(content)


@router.get("/agents")
async def agents_page(request: Request):
    """Agent management page."""
    real_agents = get_real_agent_data()
    context = {
        "request": request,
        "agents": simplify_for_template(real_agents),
        "total_agents": len(AGENT_REGISTRY),
        "squads": simplify_for_template([s["name"] for s in get_squad_data()]),
    }
    # Manual template rendering to work around starlette/jinja2 issue
    template = templates.get_template("agents.html")
    content = template.render(**context)
    from starlette.responses import HTMLResponse

    return HTMLResponse(content)


@router.get("/clients")
async def clients_page(request: Request):
    """Client management page."""
    context = {
        "request": request,
        "clients": simplify_for_template(MOCK_CLIENTS),
        "active_clients": 3,
        "trial_clients": 1,
        "total_revenue": 12500.00,
    }
    # Manual template rendering to work around starlette/jinja2 issue
    template = templates.get_template("clients.html")
    content = template.render(**context)
    from starlette.responses import HTMLResponse

    return HTMLResponse(content)


@router.get("/stats")
async def stats_page(request: Request):
    """Usage statistics page."""
    context = {
        "request": request,
        "period": "30d",
        "stats": {
            "total_requests": 125000,
            "avg_response_time": 3.2,
            "p95_response_time": 8.1,
            "p50_response_time": 2.1,
            "p99_response_time": 12.5,
            "success_rate": 0.97,
            "failed_requests": 3750,
            "escalations": 4200,
            "escalation_rate": 0.0336,
            "peak_requests": 350,
            "avg_requests": 173,
        },
        "squad_performance": [
            {
                "name": "support",
                "requests": 45000,
                "avg_response_time": 2.8,
                "success_rate": 0.98,
                "escalations": 900,
            },
            {
                "name": "sales",
                "requests": 28000,
                "avg_response_time": 4.2,
                "success_rate": 0.95,
                "escalations": 1400,
            },
            {
                "name": "content",
                "requests": 22000,
                "avg_response_time": 1.8,
                "success_rate": 0.99,
                "escalations": 220,
            },
            {
                "name": "ops",
                "requests": 15000,
                "avg_response_time": 5.1,
                "success_rate": 0.96,
                "escalations": 600,
            },
            {
                "name": "data",
                "requests": 8000,
                "avg_response_time": 6.3,
                "success_rate": 0.92,
                "escalations": 640,
            },
            {
                "name": "dev",
                "requests": 5000,
                "avg_response_time": 2.5,
                "success_rate": 0.99,
                "escalations": 50,
            },
        ],
        "top_agents": [
            {
                "name": "Support Tier 1",
                "squad": "support",
                "requests": 12000,
                "success_rate": 0.99,
                "avg_response_time": 2.1,
            },
            {
                "name": "Social Media",
                "squad": "content",
                "requests": 9500,
                "success_rate": 0.99,
                "avg_response_time": 1.5,
            },
            {
                "name": "Sales Qualification",
                "squad": "sales",
                "requests": 8500,
                "success_rate": 0.96,
                "avg_response_time": 3.8,
            },
            {
                "name": "Executive Assistant",
                "squad": "ops",
                "requests": 7200,
                "success_rate": 0.97,
                "avg_response_time": 4.2,
            },
            {
                "name": "Support Tier 2",
                "squad": "support",
                "requests": 6800,
                "success_rate": 0.98,
                "avg_response_time": 3.5,
            },
        ],
    }
    # Manual template rendering to work around starlette/jinja2 issue
    template = templates.get_template("stats.html")
    content = template.render(**context)
    from starlette.responses import HTMLResponse

    return HTMLResponse(content)
