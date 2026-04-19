from __future__ import annotations

from typing import Optional

from ghostagency.core.base_agent import AIAgent


class SupportBillingAgent(AIAgent):
    """
    Support Billing Agent - Specializes in billing and payment-related customer inquiries.
    Price: $700/month
    """

    agent_slug = "support-billing"
    squad = "support"
    display_name = "Support Billing Agent"
    price_tier = "$700/month"

    def __init__(
        self,
        client_name: str,
        knowledge_base_path: Optional[str] = None,
        escalation_email: Optional[str] = None,
        billing_contact_email: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, knowledge_base_path, model)
        self.escalation_email = escalation_email
        self.billing_contact_email = billing_contact_email

    def primary_action(self, customer_message: str, customer_email: Optional[str] = None) -> str:
        """Handle billing and payment-related customer inquiries."""

        # Build prompt with billing-specific context
        prompt = f"""Customer billing inquiry: {customer_message}

Provide a helpful, professional response focused on billing and payment matters.
Use the knowledge base for billing procedures, refund policies, and subscription management.

For complex billing disputes or refund requests that require manual review,
acknowledge the request and explain the next steps.

Response:"""

        try:
            response = self._call_llm(prompt)

            # Check if billing escalation needed
            if self._needs_billing_escalation(customer_message, response):
                self._escalate_billing_ticket(customer_message, customer_email, response)

            # Log interaction
            self._log_interaction("handle_billing_inquiry", customer_message, response)

            return response

        except Exception as e:
            # Handle LLM errors gracefully
            error_response = (
                f"I apologize, but I'm experiencing technical difficulties "
                f"with our billing system. Please try again later or contact "
                f"our billing team directly at {self.billing_contact_email}."
            )
            self._log_interaction("handle_billing_inquiry_error", customer_message, str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the Support Billing Agent role."""
        return f"""You are a specialized Billing Support Agent for {self.client_name}.

Your expertise:
- Invoice questions and payment issues
- Subscription management and changes
- Refund requests and processing
- Billing disputes and resolutions
- Payment method updates
- Failed charge investigations
- Overdue payment assistance
- Account credit applications

Your role:
- Provide accurate billing information based on knowledge base
- Explain billing procedures clearly and professionally
- Handle refund requests according to company policy
- Assist with subscription changes and cancellations
- Escalate complex billing disputes to human specialists
- Maintain confidentiality with financial information
- Never share sensitive payment details
- Follow PCI compliance guidelines

Knowledge Base:
{self.knowledge_base[:3000]}"""

    def _needs_billing_escalation(self, customer_message: str, response: str) -> bool:
        """Determine if billing inquiry requires escalation to human specialist."""
        billing_escalation_keywords = [
            # Complex billing scenarios
            "dispute",
            "chargeback",
            "fraud",
            "unauthorized",
            "legal",
            "complaint",
            "escalate",
            "manager",
            "supervisor",
            # High-value transactions
            "large refund",
            "significant amount",
            "over $1000",
            # Sensitive situations
            "threaten",
            "angry",
            "frustrated",
            "unhappy",
            # Complex technical issues
            "system error",
            "technical problem",
            "bug",
            "glitch",
            # Policy exceptions
            "exception",
            "special case",
            "make an exception",
        ]

        message_lower = customer_message.lower()
        response_lower = response.lower()

        # Check for escalation keywords in either message or response
        return any(
            keyword in message_lower or keyword in response_lower
            for keyword in billing_escalation_keywords
        )

    def _escalate_billing_ticket(
        self,
        customer_message: str,
        customer_email: Optional[str],
        ai_response: str,
    ) -> None:
        """Log billing escalation for specialist review."""
        if not self.escalation_email:
            return

        escalation_data = {
            "customer_email": customer_email,
            "customer_message": customer_message,
            "ai_response": ai_response,
            "escalation_type": "billing",
            "priority": "high",  # Billing issues typically high priority
            "reason": "Complex billing inquiry requiring specialist review",
        }

        self.logger.info("billing_ticket_escalated", **escalation_data)
