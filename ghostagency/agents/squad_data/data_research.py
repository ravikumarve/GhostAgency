from __future__ import annotations

from typing import Optional

from ghostagency.core.base_agent import AIAgent


class DataResearchAgent(AIAgent):
    """
    Data Research Agent - Researches topics, analyzes data, and generates reports.
    Price: $1,000/month
    """

    agent_slug = "data-research"
    squad = "data"
    display_name = "Data Research Agent"
    price_tier = "$1,000/month"

    def __init__(
        self,
        client_name: str,
        knowledge_base_path: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, knowledge_base_path, model)

    def primary_action(self, research_query: str, depth: str = "standard") -> str:
        """Research a topic and return structured findings."""

        prompt = f"""Research Query: {research_query}
Depth: {depth}

Provide a structured research report covering:
1. Executive Summary
2. Key Findings
3. Supporting Data & Sources
4. Implications & Recommendations

Research Report:"""

        try:
            response = self._call_llm(prompt)
            self._log_interaction("run_analysis", research_query, response)
            return response

        except Exception as e:
            error_response = (
                "I apologize, but I'm experiencing technical difficulties "
                "running the research analysis. Please try again later."
            )
            self._log_interaction("run_analysis_error", research_query, str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the Data Research role."""
        return f"""You are a Senior Data Research Analyst for {self.client_name}.

Your role:
- Conduct thorough research on any given topic
- Provide structured, data-backed reports
- Identify trends, patterns, and actionable insights
- Cite sources and quantify findings where possible
- Maintain objectivity and analytical rigor"""
