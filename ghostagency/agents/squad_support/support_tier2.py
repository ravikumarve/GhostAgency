from __future__ import annotations
from typing import Optional

from ghostagency.core.base_agent import AIAgent


class SupportTier2Agent(AIAgent):
    """
    Support Tier 2 Agent - Handles escalated customer issues and complex technical troubleshooting.
    Price: $900/month
    """

    agent_slug = "support-tier2"
    squad = "support"
    display_name = "Support Tier 2 Agent"
    price_tier = "$900/month"

    def __init__(
        self,
        client_name: str,
        knowledge_base_path: Optional[str] = None,
        specialist_email: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, knowledge_base_path, model)
        self.specialist_email = specialist_email

    def primary_action(
        self,
        customer_message: str,
        customer_email: Optional[str] = None,
        escalated_from: Optional[str] = None,
    ) -> str:
        """Handle escalated customer support tickets with advanced troubleshooting."""

        # Build prompt with escalation context and deeper KB access
        escalation_context = (
            f"Escalated from: {escalated_from}" if escalated_from else "Escalated ticket"
        )

        prompt = f"""Customer question: {customer_message}

{escalation_context}

Provide advanced technical troubleshooting and in-depth support.
You have access to comprehensive knowledge base information.
If this requires specialized expertise beyond your capabilities,
escalate to a human specialist with specific reasoning.

Response:"""

        try:
            response = self._call_llm(prompt)

            # Check if specialist escalation needed
            if self._needs_specialist_escalation(response):
                self._escalate_to_specialist(
                    customer_message, customer_email, response, escalated_from
                )

            # Log interaction
            self._log_interaction("handle_escalated_ticket", customer_message, response)

            return response

        except Exception as e:
            # Handle LLM errors gracefully
            error_response = (
                f"I apologize, but I'm experiencing technical difficulties. "
                f"Please contact our specialist team directly at "
                f"{self.specialist_email} for immediate assistance."
            )
            self._log_interaction("handle_ticket_error", customer_message, str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the Support Tier 2 role."""
        return f"""You are an advanced Tier 2 Support Agent for {self.client_name}.

Your role:
- Handle escalated support tickets requiring technical expertise
- Perform in-depth troubleshooting and analysis
- Access comprehensive knowledge base information
- Escalate only to specialized human experts when absolutely necessary
- Provide detailed, technical responses with clear next steps
- Maintain professional expertise while being approachable

Technical Capabilities:
- Debug complex system issues
- Analyze logs and error messages
- Provide step-by-step technical guidance
- Handle API and integration troubleshooting
- Understand system architecture and dependencies

Knowledge Base:
{self.knowledge_base[:5000]}"""

    def _needs_specialist_escalation(self, response: str) -> bool:
        """Determine if response indicates need for specialist escalation."""
        specialist_keywords = [
            "specialist required",
            "requires expert",
            "escalate to specialist",
            "beyond my capabilities",
            "specialized knowledge",
            "engineering team",
            "development team",
            "security issue",
            "legal matter",
            "account compromise",
            "critical bug",
            "system outage",
        ]

        response_lower = response.lower()
        return any(keyword in response_lower for keyword in specialist_keywords)

    def _escalate_to_specialist(
        self,
        customer_message: str,
        customer_email: Optional[str],
        ai_response: str,
        escalated_from: Optional[str],
    ) -> None:
        """Log specialist escalation with detailed context."""
        if not self.specialist_email:
            return

        escalation_data = {
            "customer_email": customer_email,
            "customer_message": customer_message,
            "ai_response": ai_response,
            "escalated_from": escalated_from,
            "escalation_level": "specialist",
            "reason": "Requires specialized technical expertise",
        }

        self.logger.info("ticket_escalated_to_specialist", **escalation_data)
