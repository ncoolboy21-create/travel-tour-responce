from faker import Faker
import random

fake = Faker()

CATEGORIES = [
    "Billing",
    "Technical",
    "Feature Request",
    "Account Access",
    "VIP",
    "Cancellation Intent",
    "Complaint Escalation",
    "Jurisdictional",
    "Legal/Refund"
]

def generate_ticket():
    category = random.choice(CATEGORIES)
    return {
        "ticket_id": fake.uuid4(),
        "customer": fake.name(),
        "email": fake.email(),
        "subject": category,
        "description": fake.paragraph(nb_sentences=5),
        "actual_category": category
    }
def generate_tickets(n=100):
    return [generate_ticket() for _ in range(n)]

generate_tickets(5)