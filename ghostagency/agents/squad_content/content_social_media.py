from __future__ import annotations
from typing import Optional

from ghostagency.core.base_agent import AIAgent


class ContentSocialMediaAgent(AIAgent):
    """
    Social Media Content Agent - Creates posts and responds to comments.
    Price: $600/month
    """

    agent_slug = "content-social-media"
    squad = "content"
    display_name = "Social Media Content Agent"
    price_tier = "$600/month"

    def __init__(
        self,
        client_name: str,
        brand_voice_path: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        super().__init__(client_name, None, model)
        self.brand_voice = self._load_file(brand_voice_path) if brand_voice_path else ""

    def primary_action(self, platform: str, topic: str, style: str = "engaging") -> str:
        """Create a social media post for the specified platform."""

        platform_guidelines = self._get_platform_guidelines(platform)

        prompt = f"""Platform: {platform}
Platform guidelines: {platform_guidelines}
Topic: {topic}
Style: {style}

Create an {style} post that:
1. Captures attention immediately
2. Provides value
3. Matches our brand voice
4. Encourages engagement

Post:"""

        try:
            post = self._call_llm(prompt)
            self._log_interaction("create_post", f"{platform} - {topic}", post)
            return post

        except Exception as e:
            error_response = (
                "I apologize, but I'm experiencing technical difficulties "
                "creating the post. Please try again later."
            )
            self._log_interaction("create_post_error", f"{platform} - {topic}", str(e))
            return error_response

    def respond_to_comment(self, comment_text: str, post_context: str = "") -> str:
        """Generate a response to a social media comment."""

        prompt = f"""Comment: "{comment_text}"
Post context: {post_context}

Write a brief, friendly response that:
- Acknowledges their comment
- Adds value if possible
- Encourages continued engagement
- Stays on-brand

Keep it under 50 words.

Response:"""

        try:
            response = self._call_llm(prompt)
            self._log_interaction("respond_comment", comment_text[:50], response)
            return response

        except Exception as e:
            error_response = "I appreciate your comment! I'll get back to you shortly."
            self._log_interaction("respond_comment_error", comment_text[:50], str(e))
            return error_response

    def get_role_prompt(self) -> str:
        """System prompt defining the Social Media Content role."""
        return f"""You are the social media manager for {self.client_name}.

Your role:
- Create engaging social media posts across multiple platforms
- Respond to comments in a friendly, brand-appropriate manner
- Maintain consistent brand voice and tone
- Drive engagement and build community
- Adapt content style to different platform requirements

Brand Voice:
{self.brand_voice[:2000]}"""

    def _load_file(self, path: Optional[str]) -> str:
        """Load content from a file."""
        if not path:
            return ""

        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""

    def _get_platform_guidelines(self, platform: str) -> str:
        """Get platform-specific guidelines."""
        guidelines = {
            "twitter": ("Max 280 characters. Punchy and concise. Use 1-2 relevant hashtags."),
            "linkedin": (
                "150-300 words. Professional yet engaging. "
                "Tell a story. No hashtags unless very relevant."
            ),
            "instagram": (
                "Visual-focused caption. 100-200 words. "
                "Use 5-10 hashtags. Include call-to-action."
            ),
            "facebook": ("100-200 words. Conversational. Ask questions to drive engagement."),
            "tiktok": (
                "Short, engaging videos. 15-60 seconds. " "Trend-focused. Music and effects."
            ),
            "youtube": (
                "Longer form content. 5-15 minutes. "
                "Educational or entertaining. Clear structure."
            ),
        }
        return guidelines.get(
            platform.lower(), "Create engaging content appropriate for the platform"
        )
