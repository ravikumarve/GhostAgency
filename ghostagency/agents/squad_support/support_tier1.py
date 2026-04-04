from __future__ import annotations
from typing import Optional

from ghostagency.core.base_agent import AIAgent


class SupportTier1Agent(AIAgent):
    """
    Support Tier 1 Agent - Handles common customer inquiries and basic troubleshooting.
    Price: $800/month
    """

    agent_slug = "support-tier1"
    squad = "support"
    display_name = "Support Tier 1 Agent"
    price_tier = "$800/month"

    def __init__(
        self,
        client_name: str,
        knowledge_base_path: Optional[str] = None,
        escalation_email: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, knowledge_base_path, model)
        self.escalation_email = escalation_email

    def primary_action(
        self, customer_message: str, customer_email: Optional[str] = None
    ) -> str:
        """Handle a customer support ticket."""

        # Build prompt with knowledge base context
        prompt = f"""Customer question: {customer_message}

Provide a helpful, professional response based on our knowledge base. 
If you don't know the answer based on the available information, 
be honest and offer to escalate to a human specialist.

Response:"""

        try:
            response = self._call_llm(prompt)

            # Check if escalation needed
            if self._needs_escalation(response):
                self._escalate_ticket(customer_message, customer_email, response)

            # Log interaction
            self._log_interaction("handle_ticket", customer_message, response)

            return response

        except Exception as e:
            # Handle LLM errors gracefully
            error_response = f"I apologize, but I'm experiencing technical difficulties. Please try again later or contact support directly at {self.escalation_email}."
            self._log_interaction("handle_ticket_error", customer_message, str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the Support Tier 1 role."""
        return f"""You are a friendly and professional Tier 1 Support Agent for {self.client_name}.

Your role:
- Answer common customer questions based on the knowledge base
- Provide clear, concise, and helpful responses
- Escalate complex issues to human specialists when needed
- Maintain a positive and professional tone
- Never make up information - if you don't know, say so

Knowledge Base:
{self.knowledge_base[:3000]}"""

    def _needs_escalation(self, response: str) -> bool:
        """Determine if response indicates need for escalation."""
        escalation_keywords = [
            "escalate",
            "don't know",
            "not sure",
            "complex",
            "speak to human",
            "contact support",
            "specialist",
        ]

        response_lower = response.lower()
        return any(keyword in response_lower for keyword in escalation_keywords)

    def _escalate_ticket(
        self, customer_message: str, customer_email: Optional[str], ai_response: str
    ) -> None:
        """Log escalation for human review."""
        if not self.escalation_email:
            return

        escalation_data = {
            "customer_email": customer_email,
            "customer_message": customer_message,
            "ai_response": ai_response,
            "reason": "Complex query requiring human intervention",
        }

        self.logger.info("ticket_escalated", **escalation_data)
