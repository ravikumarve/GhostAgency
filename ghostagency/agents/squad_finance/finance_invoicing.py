from __future__ import annotations

from typing import Optional

from ghostagency.core.base_agent import AIAgent


class FinanceInvoicingAgent(AIAgent):
    """
    Finance Invoicing Agent - Generates invoices, tracks expenses, and provides financial summaries.
    Price: $800/month
    """

    agent_slug = "finance-invoicing"
    squad = "finance"
    display_name = "Finance Invoicing Agent"
    price_tier = "$800/month"

    def __init__(
        self,
        client_name: str,
        knowledge_base_path: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, knowledge_base_path, model)

    def primary_action(self, task_description: str, **kwargs) -> str:
        """Process a financial task."""

        prompt = f"""Finance Task: {task_description}
Context: {kwargs.get('context', 'No additional context provided.')}

Provide a structured response covering:
1. Task Summary
2. Financial Analysis
3. Recommended Actions
4. Compliance Notes

Response:"""

        try:
            response = self._call_llm(prompt)
            self._log_interaction("process_task", task_description, response)
            return response

        except Exception as e:
            error_response = (
                "I apologize, but I'm experiencing technical difficulties "
                "processing this financial task. Please try again later."
            )
            self._log_interaction("process_task_error", task_description, str(e))
            return error_response

    def generate_invoice(self, client: str, items: list[dict], due_date: str) -> str:
        """Generate a professional invoice."""
        items_str = "\n".join(
            f"  - {item.get('description', 'Item')}: ${item.get('amount', 0):.2f}"
            for item in items
        )
        total = sum(item.get("amount", 0) for item in items)

        prompt = f"""Generate a professional invoice:
Client: {client}
Due Date: {due_date}
Items:
{items_str}
Total: ${total:.2f}

Include:
- Professional invoice header
- Itemized list with amounts
- Payment terms and instructions
- Thank you note"""

        try:
            invoice = self._call_llm(prompt)
            self._log_interaction("generate_invoice", f"{client}: ${total:.2f}", invoice)
            return invoice

        except Exception as e:
            error_response = (
                "I apologize, but I'm experiencing technical difficulties "
                "generating the invoice. Please try again later."
            )
            self._log_interaction("generate_invoice_error", f"{client}: ${total:.2f}", str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the Finance Invoicing role."""
        return f"""You are a Finance & Invoicing Specialist for {self.client_name}.

Your role:
- Generate professional invoices with correct formatting
- Track and categorize expenses
- Provide financial summaries and reports
- Ensure compliance with accounting standards
- Maintain accuracy and attention to detail"""
