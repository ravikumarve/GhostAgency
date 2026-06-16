from __future__ import annotations

from typing import Optional

from ghostagency.core.base_agent import AIAgent


class HRRecruitingAgent(AIAgent):
    """
    HR Recruiting Agent - Screens candidates, drafts job descriptions, and manages onboarding.
    Price: $900/month
    """

    agent_slug = "hr-recruiting"
    squad = "hr"
    display_name = "HR Recruiting Agent"
    price_tier = "$900/month"

    def __init__(
        self,
        client_name: str,
        knowledge_base_path: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, knowledge_base_path, model)

    def primary_action(self, hr_request: str, **kwargs) -> str:
        """Handle an HR task."""

        prompt = f"""HR Request: {hr_request}
Context: {kwargs.get('context', 'No additional context provided.')}

Provide a structured response covering:
1. Request Understanding
2. Recommended Actions
3. Timeline & Next Steps
4. Compliance Considerations

Response:"""

        try:
            response = self._call_llm(prompt)
            self._log_interaction("handle_hr_task", hr_request, response)
            return response

        except Exception as e:
            error_response = (
                "I apologize, but I'm experiencing technical difficulties "
                "processing this HR request. Please try again later."
            )
            self._log_interaction("handle_hr_task_error", hr_request, str(e))
            return error_response

    def screen_candidate(self, resume_text: str, job_requirements: str) -> str:
        """Screen a candidate against job requirements."""

        prompt = f"""Job Requirements:
{job_requirements}

Candidate Resume:
{resume_text[:2000]}

Provide a structured screening:
1. Overall Fit Score (1-10)
2. Key Strengths
3. Experience Gaps
4. Red Flags (if any)
5. Interview Recommendation (Yes/No with reasoning)

Screening Report:"""

        try:
            screening = self._call_llm(prompt)
            self._log_interaction("screen_candidate", resume_text[:100], screening)
            return screening

        except Exception as e:
            error_response = (
                "I apologize, but I'm experiencing technical difficulties "
                "screening this candidate. Please try again later."
            )
            self._log_interaction("screen_candidate_error", resume_text[:100], str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the HR Recruiting role."""
        return f"""You are an HR & Recruiting Specialist for {self.client_name}.

Your role:
- Screen candidates thoroughly against job requirements
- Draft clear and compelling job descriptions
- Manage onboarding checklists and processes
- Maintain confidentiality and professionalism
- Ensure compliance with hiring regulations"""
