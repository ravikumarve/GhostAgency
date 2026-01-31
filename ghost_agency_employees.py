#!/usr/bin/env python3
"""
GHOST AGENCY - AI Employee Templates
Ready-to-deploy AI workers that you can sell for $500-2000/month

Each AI employee costs you $5-10/month to run but you charge $500-2000/month
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class AIEmployee:
    """Base class for all AI employees"""
    
    def __init__(self, client_name, role, knowledge_base_path=None):
        self.client_name = client_name
        self.role = role
        self.knowledge_base = []
        self.conversation_history = []
        
        if knowledge_base_path and os.path.exists(knowledge_base_path):
            self._load_knowledge_base(knowledge_base_path)
    
    def _load_knowledge_base(self, path):
        """Load client's knowledge base (FAQs, docs, etc.)"""
        print(f"📚 Loading knowledge base for {self.client_name}...")
        
        if os.path.isdir(path):
            for file in Path(path).glob("*.txt"):
                with open(file, 'r', encoding='utf-8') as f:
                    self.knowledge_base.append(f.read())
        else:
            with open(path, 'r', encoding='utf-8') as f:
                self.knowledge_base.append(f.read())
        
        print(f"✓ Loaded {len(self.knowledge_base)} knowledge documents")
    
    def _call_ollama(self, prompt, model="phi3"):
        """Call Ollama AI"""
        try:
            response = requests.post(
                'http://localhost:11434/api/generate',
                json={'model': model, 'prompt': prompt, 'stream': False},
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()['response'].strip()
            else:
                return f"Error: Status {response.status_code}"
        
        except requests.exceptions.ConnectionError:
            return "ERROR: Ollama not running. Start with: ollama serve"
        except Exception as e:
            return f"ERROR: {e}"
    
    def log_interaction(self, user_input, ai_response):
        """Log all interactions for analysis"""
        self.conversation_history.append({
            'timestamp': datetime.now().isoformat(),
            'user': user_input,
            'ai': ai_response,
            'role': self.role
        })
        
        # Save to file
        log_dir = Path(f"logs/{self.client_name}")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"{datetime.now().strftime('%Y%m')}_interactions.json"
        
        with open(log_file, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)


class AICustomerSupport(AIEmployee):
    """
    AI Customer Support Agent
    
    Sell for: $800/month
    Your cost: $8/month
    Profit: $792/month per client
    """
    
    def __init__(self, client_name, knowledge_base_path, escalation_email=None):
        super().__init__(client_name, "Customer Support", knowledge_base_path)
        self.escalation_email = escalation_email
        self.confidence_threshold = 0.7
    
    def handle_ticket(self, customer_message, customer_email=None):
        """Handle a customer support ticket"""
        
        print(f"\n{'='*60}")
        print(f"📧 NEW TICKET from {customer_email or 'Customer'}")
        print(f"{'='*60}")
        print(f"Message: {customer_message}")
        print(f"{'='*60}")
        
        # Build context from knowledge base
        context = "\n\n".join(self.knowledge_base)
        
        # Create prompt
        prompt = f"""You are a customer support agent for {self.client_name}.

Company knowledge base:
{context}

Customer question: {customer_message}

Provide a helpful, professional response. If you don't know the answer based on the knowledge base, say so and offer to escalate.

Response:"""

        # Get AI response
        response = self._call_ollama(prompt)
        
        print(f"\n🤖 AI Response:\n{response}")
        
        # Check if escalation needed (simple keyword detection)
        escalation_keywords = ['escalate', "don't know", 'not sure', 'complex', 'speak to human']
        needs_escalation = any(keyword in response.lower() for keyword in escalation_keywords)
        
        if needs_escalation and self.escalation_email:
            self._escalate_ticket(customer_message, customer_email, response)
        
        # Log interaction
        self.log_interaction(customer_message, response)
        
        return response
    
    def _escalate_ticket(self, customer_message, customer_email, ai_response):
        """Escalate complex tickets to human"""
        print(f"\n⚠️  ESCALATING to {self.escalation_email}")
        
        # In production, send email to client's support team
        # For now, just log it
        escalation = {
            'timestamp': datetime.now().isoformat(),
            'customer_email': customer_email,
            'message': customer_message,
            'ai_attempted_response': ai_response,
            'reason': 'Low confidence / Complex query'
        }
        
        log_dir = Path(f"logs/{self.client_name}/escalations")
        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_file = log_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(log_file, 'w') as f:
            json.dump(escalation, f, indent=2)


class AISalesDevelopmentRep(AIEmployee):
    """
    AI Sales Development Rep (SDR)
    
    Sell for: $1,200/month
    Your cost: $10/month  
    Profit: $1,190/month per client
    """
    
    def __init__(self, client_name, company_info_path, product_info_path):
        super().__init__(client_name, "Sales Development Rep")
        self.company_info = self._load_file(company_info_path)
        self.product_info = self._load_file(product_info_path)
    
    def _load_file(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()
        return ""
    
    def qualify_lead(self, lead_info):
        """Qualify an inbound lead"""
        
        print(f"\n{'='*60}")
        print(f"🎯 QUALIFYING LEAD")
        print(f"{'='*60}")
        
        prompt = f"""You are a sales development rep for {self.client_name}.

Company info:
{self.company_info}

Products/services:
{self.product_info}

Lead information:
{json.dumps(lead_info, indent=2)}

Analyze this lead and provide:
1. Qualification score (1-10, where 10 = perfect fit)
2. Key signals (positive and negative)
3. Recommended next action
4. Suggested talking points

Format as JSON:
{{
  "score": X,
  "positive_signals": [...],
  "concerns": [...],
  "next_action": "...",
  "talking_points": [...]
}}

Analysis:"""

        response = self._call_ollama(prompt)
        
        print(f"\n🤖 Lead Qualification:\n{response}")
        
        self.log_interaction(str(lead_info), response)
        
        return response
    
    def draft_followup_email(self, lead_name, lead_company, context=""):
        """Draft personalized follow-up email"""
        
        prompt = f"""You are a sales development rep for {self.client_name}.

Write a brief, personalized follow-up email to:
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

        email = self._call_ollama(prompt)
        
        print(f"\n📧 Draft Email:\n{email}")
        
        return email


class AISocialMediaManager(AIEmployee):
    """
    AI Social Media Manager
    
    Sell for: $600/month
    Your cost: $8/month
    Profit: $592/month per client
    """
    
    def __init__(self, client_name, brand_voice_path):
        super().__init__(client_name, "Social Media Manager")
        self.brand_voice = self._load_file(brand_voice_path) if brand_voice_path else ""
    
    def _load_file(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()
        return ""
    
    def create_post(self, platform, topic, style="engaging"):
        """Create a social media post"""
        
        print(f"\n{'='*60}")
        print(f"📱 CREATING {platform.upper()} POST")
        print(f"{'='*60}")
        
        platform_guidelines = {
            'twitter': 'Max 280 characters. Punchy and concise. Use 1-2 relevant hashtags.',
            'linkedin': '150-300 words. Professional yet engaging. Tell a story. No hashtags unless very relevant.',
            'instagram': 'Visual-focused caption. 100-200 words. Use 5-10 hashtags. Include call-to-action.',
            'facebook': '100-200 words. Conversational. Ask questions to drive engagement.'
        }
        
        prompt = f"""You are the social media manager for {self.client_name}.

Brand voice:
{self.brand_voice}

Platform: {platform}
Platform guidelines: {platform_guidelines.get(platform, '')}

Topic: {topic}
Style: {style}

Create an {style} post that:
1. Captures attention immediately
2. Provides value
3. Matches our brand voice
4. Encourages engagement

Post:"""

        post = self._call_ollama(prompt)
        
        print(f"\n📝 Generated Post:\n{post}")
        
        self.log_interaction(f"{platform} - {topic}", post)
        
        return post
    
    def respond_to_comment(self, comment_text, post_context=""):
        """Generate response to a comment"""
        
        prompt = f"""You are the social media manager for {self.client_name}.

Brand voice:
{self.brand_voice}

Someone commented on our post:
Comment: "{comment_text}"
Post context: {post_context}

Write a brief, friendly response that:
- Acknowledges their comment
- Adds value if possible
- Encourages continued engagement
- Stays on-brand

Keep it under 50 words.

Response:"""

        response = self._call_ollama(prompt)
        
        print(f"\n💬 Comment Response:\n{response}")
        
        return response


class AIExecutiveAssistant(AIEmployee):
    """
    AI Executive Assistant
    
    Sell for: $1,500/month
    Your cost: $10/month
    Profit: $1,490/month per client
    """
    
    def __init__(self, client_name, executive_name, preferences_path=None):
        super().__init__(client_name, "Executive Assistant")
        self.executive_name = executive_name
        self.preferences = self._load_file(preferences_path) if preferences_path else ""
    
    def _load_file(self, path):
        if os.path.exists(path):
            with open(path, 'r') as f:
                return f.read()
        return ""
    
    def draft_email(self, recipient, purpose, key_points=[]):
        """Draft an email"""
        
        print(f"\n{'='*60}")
        print(f"✉️  DRAFTING EMAIL")
        print(f"{'='*60}")
        
        prompt = f"""You are the executive assistant for {self.executive_name}.

Executive preferences:
{self.preferences}

Draft an email to: {recipient}
Purpose: {purpose}
Key points to include: {', '.join(key_points)}

The email should be:
- Professional yet warm
- Clear and concise
- Action-oriented
- Signed by {self.executive_name}

Email:"""

        email = self._call_ollama(prompt)
        
        print(f"\n📧 Draft:\n{email}")
        
        self.log_interaction(f"Email to {recipient}: {purpose}", email)
        
        return email
    
    def summarize_meeting(self, meeting_notes):
        """Summarize meeting notes"""
        
        prompt = f"""You are the executive assistant for {self.executive_name}.

Summarize these meeting notes into:
1. Key decisions made
2. Action items (with owners if mentioned)
3. Important takeaways
4. Follow-up needed

Meeting notes:
{meeting_notes}

Summary:"""

        summary = self._call_ollama(prompt)
        
        print(f"\n📋 Meeting Summary:\n{summary}")
        
        return summary
    
    def research_topic(self, topic, depth="brief"):
        """Research a topic and provide summary"""
        
        prompt = f"""You are researching on behalf of {self.executive_name}.

Topic: {topic}
Depth: {depth}

Provide a {depth} overview that includes:
- Key facts and statistics
- Main players/companies
- Recent developments
- Potential implications for our business

Research summary:"""

        research = self._call_ollama(prompt)
        
        print(f"\n🔍 Research:\n{research}")
        
        return research


def demo_customer_support():
    """Demo of AI Customer Support"""
    print("\n" + "="*60)
    print("DEMO: AI CUSTOMER SUPPORT AGENT")
    print("="*60)
    
    # Create knowledge base
    kb_dir = Path("demo_kb/support")
    kb_dir.mkdir(parents=True, exist_ok=True)
    
    with open(kb_dir / "faqs.txt", 'w') as f:
        f.write("""
SHIPPING POLICY:
- Free shipping on orders over $50
- Standard shipping: 5-7 business days
- Express shipping: 2-3 business days (additional $15)

RETURN POLICY:
- 30-day return window
- Items must be unused and in original packaging
- Refund processed within 5-7 business days

PRODUCT WARRANTY:
- All products come with 1-year warranty
- Covers manufacturing defects
- Does not cover normal wear and tear
""")
    
    # Initialize AI
    support_ai = AICustomerSupport(
        client_name="Demo E-commerce Store",
        knowledge_base_path=kb_dir,
        escalation_email="support@client.com"
    )
    
    # Test tickets
    test_tickets = [
        "How long does shipping take?",
        "Can I return a product after 45 days?",
        "My product broke after 2 months, is it covered?",
        "I need help with a very complex technical integration issue with your API"
    ]
    
    for ticket in test_tickets:
        support_ai.handle_ticket(ticket, "customer@example.com")
        print("\n" + "-"*60 + "\n")


def demo_sales_sdr():
    """Demo of AI Sales Development Rep"""
    print("\n" + "="*60)
    print("DEMO: AI SALES DEVELOPMENT REP")
    print("="*60)
    
    # Create company info
    info_dir = Path("demo_kb/sales")
    info_dir.mkdir(parents=True, exist_ok=True)
    
    with open(info_dir / "company.txt", 'w') as f:
        f.write("We help B2B SaaS companies reduce customer churn through AI-powered engagement.")
    
    with open(info_dir / "product.txt", 'w') as f:
        f.write("Our platform identifies at-risk customers and automatically initiates retention campaigns.")
    
    # Initialize AI
    sales_ai = AISalesDevelopmentRep(
        client_name="ChurnFix AI",
        company_info_path=info_dir / "company.txt",
        product_info_path=info_dir / "product.txt"
    )
    
    # Test lead
    lead = {
        "name": "Sarah Johnson",
        "title": "VP of Customer Success",
        "company": "TechStart SaaS",
        "employees": "50-100",
        "current_churn": "8% monthly",
        "pain_point": "Struggling to identify churn signals early"
    }
    
    sales_ai.qualify_lead(lead)
    print("\n" + "-"*60 + "\n")
    
    sales_ai.draft_followup_email("Sarah Johnson", "TechStart SaaS", "Interested in reducing churn")


def main():
    """Main demo"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║            GHOST AGENCY - AI EMPLOYEES                    ║
║         Ready-to-Deploy AI Workers                        ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # Check Ollama
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code != 200:
            print("❌ Ollama not running. Start with: ollama serve")
            return
    except:
        print("❌ Ollama not running. Start with: ollama serve")
        return
    
    print("✓ Ollama connected\n")
    
    while True:
        print("\n" + "="*60)
        print("SELECT DEMO:")
        print("="*60)
        print("1. AI Customer Support Agent ($800/month)")
        print("2. AI Sales Development Rep ($1,200/month)")
        print("3. AI Social Media Manager ($600/month)")
        print("4. AI Executive Assistant ($1,500/month)")
        print("5. Exit")
        print("="*60)
        
        choice = input("\nSelect (1-5): ").strip()
        
        if choice == "1":
            demo_customer_support()
        
        elif choice == "2":
            demo_sales_sdr()
        
        elif choice == "3":
            smm_ai = AISocialMediaManager("Demo Company", None)
            smm_ai.create_post("linkedin", "AI automation in business", "thought leadership")
        
        elif choice == "4":
            ea_ai = AIExecutiveAssistant("Demo Corp", "John Smith", None)
            ea_ai.draft_email(
                recipient="jane@partner.com",
                purpose="Schedule quarterly business review",
                key_points=["Q4 results", "2025 planning", "Partnership expansion"]
            )
        
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("Invalid choice")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
