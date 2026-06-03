from config import (
    NEVER_AUTO_RESPOND,
    ESCALATION_TEAM,
    AUTO_ACCEPT_THRESHOLD
)

def route_ticket(category, confidence):

    if category in NEVER_AUTO_RESPOND:

        return {
            "action": "ESCALATE",
            "team": ESCALATION_TEAM[category],
            "auto_response": False
        }

    if confidence >= AUTO_ACCEPT_THRESHOLD:

        return {
            "action": "AUTO_ROUTE",
            "team": "Auto",
            "auto_response": True
        }

    return {
        "action": "HUMAN_REVIEW",
        "team": "Support Analyst",
        "auto_response": False
    }