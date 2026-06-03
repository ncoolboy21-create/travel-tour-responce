import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

AUTO_ACCEPT_THRESHOLD = 0.80

NEVER_AUTO_RESPOND = {
    "VIP",
    "Cancellation Intent",
    "Complaint Escalation",
    "Jurisdictional",
    "Legal/Refund"
}

ESCALATION_TEAM = {
    "VIP": "Senior Support Manager",
    "Cancellation Intent": "Retention Team",
    "Complaint Escalation": "Customer Success Lead",
    "Jurisdictional": "Compliance Team",
    "Legal/Refund": "Legal & Finance Team"
}