from __future__ import annotations

from typing import Optional, Dict, Any

from ghostagency.core.base_agent import AIAgent


class SalesQualificationAgent(AIAgent):
    """
    Sales Qualification Agent - Qualifies inbound leads and drafts follow-up emails.
    Price: $1,200/month
    """

    agent_slug = "sales-qualification"
    squad = "sales"
    display_name = "Sales Qualification Agent"
    price_tier = "$1,200/month"

    def __init__(
        self,
        client_name: str,
        company_info_path: Optional[str] = None,
        product_info_path: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, None, model)
        self.company_info = self._load_file(company_info_path)
        self.product_info = self._load_file(product_info_path)

    def primary_action(self, lead_info: Dict[str, Any]) -> str:
        """Qualify an inbound lead and provide analysis."""

        prompt = f"""Lead information:
{self._format_lead_info(lead_info)}

Analyze this lead and provide:
1. Qualification score (1-10, where 10 = perfect fit)
2. Key positive signals
3. Potential concerns
4. Recommended next action
5. Suggested talking points

Format as structured analysis:"""

        try:
            response = self._call_llm(prompt)
            self._log_interaction("qualify_lead", str(lead_info), response)
            return response

        except Exception as e:
            error_response = (
                "I apologize, but I'm experiencing technical difficulties "
                "analyzing this lead. Please try again later."
            )
            self._log_interaction("qualify_lead_error", str(lead_info), str(e))
            return error_response

    def draft_followup_email(self, lead_name: str, lead_company: str, context: str = "") -> str:
        """Draft a personalized follow-up email."""

        prompt = f"""Write a brief, personalized follow-up email to:
Name: {lead_name}
Company: {lead_company}
Context: {context}

Our offering:
{self.product_info}

Keep it:
- Under 100 words
- Friendly and conversational
- Focused on their potential pain point
- Include clear call-to-action (book a call)

Email:"""

        try:
            email = self._call_llm(prompt)
            self._log_interaction("draft_email", f"{lead_name}@{lead_company}", email)
            return email

        except Exception as e:
            error_response = (
                "I apologize, but I'm experiencing technical difficulties "
                "drafting the email. Please try again later."
            )
            self._log_interaction("draft_email_error", f"{lead_name}@{lead_company}", str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the Sales Qualification role."""
        return f"""You are a professional Sales Development Rep for {self.client_name}.

Your role:
- Analyze and qualify inbound leads based on company and product fit
- Provide structured lead analysis with scoring and recommendations
- Draft personalized follow-up emails that drive engagement
- Maintain a consultative and professional tone
- Focus on identifying high-potential opportunities

Company Information:
{self.company_info[:2000]}

Product Information:
{self.product_info[:2000]}"""

    def _load_file(self, path: Optional[str]) -> str:
        """Load content from a file."""
        if not path:
            return ""

        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def _format_lead_info(self, lead_info: Dict[str, Any]) -> str:
        """Format lead information for the prompt."""
        formatted = []
        for key, value in lead_info.items():
            formatted.append(f"{key.replace('_', ' ').title()}: {value}")
        return "\n".join(formatted)
