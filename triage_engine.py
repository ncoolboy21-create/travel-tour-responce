import json
from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

def triage_ticket(ticket_text):
    prompt = f"""
Classify this support ticket.

Categories:
- Billing
- Technical
- Feature Request
- Account Access
- VIP
- Cancellation Intent
- Complaint Escalation
- Jurisdictional
- Legal/Refund

Return JSON:

{{
 "category":"",
 "priority":"",
 "confidence":0.0
}}

Ticket:
{ticket_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    text = response.text.strip()
    text = (
        text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )
    return json.loads(text)