from __future__ import annotations
from typing import Optional, List

from ghostagency.core.base_agent import AIAgent


class OpsExecutiveAssistantAgent(AIAgent):
    """
    Executive Assistant Agent - Handles executive support tasks.
    Price: $1,500/month
    """

    agent_slug = "ops-executive-assistant"
    squad = "ops"
    display_name = "Executive Assistant Agent"
    price_tier = "$1,500/month"

    def __init__(
        self,
        client_name: str,
        executive_name: str,
        preferences_path: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, None, model)
        self.executive_name = executive_name
        self.preferences = self._load_file(preferences_path) if preferences_path else ""

    def primary_action(self, task_type: str, **kwargs) -> str:
        """Handle various executive assistant tasks."""

        if task_type == "draft_email":
            return self.draft_email(
                kwargs.get("recipient", ""),
                kwargs.get("purpose", ""),
                kwargs.get("key_points", []),
            )
        elif task_type == "summarize_meeting":
            return self.summarize_meeting(kwargs.get("meeting_notes", ""))
        elif task_type == "research_topic":
            return self.research_topic(
                kwargs.get("topic", ""), kwargs.get("depth", "brief")
            )
        else:
            return f"I'm sorry, I don't support the task type '{task_type}' yet."

    def draft_email(
        self, recipient: str, purpose: str, key_points: List[str] = []
    ) -> str:
        """Draft a professional email."""

        prompt = f"""Draft an email to: {recipient}
Purpose: {purpose}
Key points to include: {", ".join(key_points)}

The email should be:
- Professional yet warm
- Clear and concise
- Action-oriented
- Signed by {self.executive_name}

Email:"""

        try:
            email = self._call_llm(prompt)
            self._log_interaction("draft_email", f"{recipient}: {purpose}", email)
            return email

        except Exception as e:
            error_response = f"I apologize, but I'm experiencing technical difficulties drafting the email. Please try again later."
            self._log_interaction(
                "draft_email_error", f"{recipient}: {purpose}", str(e)
            )
            return error_response

    def summarize_meeting(self, meeting_notes: str) -> str:
        """Summarize meeting notes."""

        prompt = f"""Summarize these meeting notes into:
1. Key decisions made
2. Action items (with owners if mentioned)
3. Important takeaways
4. Follow-up needed

Meeting notes:
{meeting_notes}

Summary:"""

        try:
            summary = self._call_llm(prompt)
            self._log_interaction("summarize_meeting", meeting_notes[:100], summary)
            return summary

        except Exception as e:
            error_response = f"I apologize, but I'm experiencing technical difficulties summarizing the meeting notes. Please try again later."
            self._log_interaction(
                "summarize_meeting_error", meeting_notes[:100], str(e)
            )
            return error_response

    def research_topic(self, topic: str, depth: str = "brief") -> str:
        """Research a topic and provide summary."""

        prompt = f"""Topic: {topic}
Depth: {depth}

Provide a {depth} overview that includes:
- Key facts and statistics
- Main players/companies
- Recent developments
- Potential implications for our business

Research summary:"""

        try:
            research = self._call_llm(prompt)
            self._log_interaction("research_topic", topic, research)
            return research

        except Exception as e:
            error_response = f"I apologize, but I'm experiencing technical difficulties researching the topic. Please try again later."
            self._log_interaction("research_topic_error", topic, str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the Executive Assistant role."""
        return f"""You are the executive assistant for {self.executive_name} at {self.client_name}.

Your role:
- Draft professional emails and communications
- Summarize meetings and extract action items
- Research topics and provide concise overviews
- Maintain confidentiality and professionalism
- Adapt to the executive's preferences and style

Executive Preferences:
{self.preferences[:2000]}"""

    def _load_file(self, path: Optional[str]) -> str:
        """Load content from a file."""
        if not path:
            return ""

        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
