from __future__ import annotations

from typing import Optional

from ghostagency.core.base_agent import AIAgent


class LegalContractReviewAgent(AIAgent):
    """
    Legal Contract Review Agent - Reviews contracts for risks, compliance, and key terms.
    Price: $2,000/month
    """

    agent_slug = "legal-contract-review"
    squad = "legal"
    display_name = "Legal Contract Review Agent"
    price_tier = "$2,000/month"

    def __init__(
        self,
        client_name: str,
        knowledge_base_path: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, knowledge_base_path, model)

    def primary_action(self, document_text: str, document_type: str = "contract") -> str:
        """Review a document and return legal analysis."""

        prompt = f"""Document Type: {document_type}
Document:
{document_text[:3000]}

Provide a structured legal review covering:
1. Document Summary
2. Key Terms & Clauses
3. Risk Assessment (High/Medium/Low)
4. Red Flags & Concerns
5. Recommended Changes
6. Negotiation Points

Legal Review:"""

        try:
            response = self._call_llm(prompt)
            self._log_interaction("review_document", document_text[:200], response)
            return response

        except Exception as e:
            error_response = (
                "I apologize, but I'm experiencing technical difficulties "
                "reviewing this document. Please try again later."
            )
            self._log_interaction("review_document_error", document_text[:200], str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the Legal Contract Review role."""
        return f"""You are a Legal Contract Review Specialist for {self.client_name}.

Your role:
- Review contracts and legal documents thoroughly
- Identify risks, liabilities, and unfavorable terms
- Highlight key clauses and their implications
- Suggest specific language modifications
- Flag compliance and regulatory concerns
- Maintain strict confidentiality

Note: You provide analysis and recommendations only. Final legal decisions must be made by a qualified attorney."""
