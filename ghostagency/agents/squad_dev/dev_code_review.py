from __future__ import annotations

from typing import Optional

from ghostagency.core.base_agent import AIAgent


class DevCodeReviewAgent(AIAgent):
    """
    Dev Code Review Agent - Reviews code for bugs, security issues, and best practices.
    Price: $1,500/month
    """

    agent_slug = "dev-code-review"
    squad = "dev"
    display_name = "Dev Code Review Agent"
    price_tier = "$1,500/month"

    def __init__(
        self,
        client_name: str,
        knowledge_base_path: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, knowledge_base_path, model)

    def primary_action(self, code_snippet: str, language: str = "python") -> str:
        """Review code and return analysis."""

        prompt = f"""Language: {language}
Code to review:
```{language}
{code_snippet}
```

Provide a code review covering:
1. Bugs or logic errors
2. Security vulnerabilities
3. Performance issues
4. Code style & best practices
5. Specific recommendations to fix each issue

Code Review:"""

        try:
            response = self._call_llm(prompt)
            self._log_interaction("assist_dev", code_snippet[:200], response)
            return response

        except Exception as e:
            error_response = (
                "I apologize, but I'm experiencing technical difficulties "
                "reviewing the code. Please try again later."
            )
            self._log_interaction("assist_dev_error", code_snippet[:200], str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the Dev Code Review role."""
        return f"""You are a Senior Code Reviewer for {self.client_name}.

Your role:
- Review code thoroughly for bugs, security flaws, and anti-patterns
- Provide clear, actionable fix recommendations
- Follow language-specific best practices and conventions
- Be constructive — highlight what's good too
- Never suggest changes without explaining why"""
