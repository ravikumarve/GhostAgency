from __future__ import annotations

from typing import Optional

from ghostagency.core.base_agent import AIAgent


class CustomGenericAgent(AIAgent):
    """
    Custom Generic Agent - A flexible agent for client-specific custom tasks.
    Price: Custom pricing — configured per client.
    """

    agent_slug = "custom-generic"
    squad = "custom"
    display_name = "Custom Generic Agent"
    price_tier = "Custom"

    def __init__(
        self,
        client_name: str,
        knowledge_base_path: Optional[str] = None,
        custom_instructions: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, knowledge_base_path, model)
        self.custom_instructions = custom_instructions or ""

    def primary_action(self, task_input: str, **kwargs) -> str:
        """Execute a custom task based on client-specific instructions."""

        prompt = f"""Task: {task_input}
Context: {kwargs.get('context', 'No additional context provided.')}

Execute this task according to the custom instructions provided.
Provide a clear, actionable response.

Response:"""

        try:
            response = self._call_llm(prompt)
            self._log_interaction("custom_action", task_input, response)
            return response

        except Exception as e:
            error_response = (
                "I apologize, but I'm experiencing technical difficulties "
                "executing this custom task. Please try again later."
            )
            self._log_interaction("custom_action_error", task_input, str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the Custom Generic role."""
        base_prompt = f"""You are a Custom AI Agent configured for {self.client_name}.

Your role:
- Execute client-specific tasks according to custom instructions
- Adapt your communication style to client preferences
- Handle a wide variety of task types flexibly
- Provide clear, actionable outputs
- Ask clarifying questions when instructions are ambiguous
"""

        if self.custom_instructions:
            base_prompt += f"\nCustom Instructions:\n{self.custom_instructions[:2000]}"

        return base_prompt
