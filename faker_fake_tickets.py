from faker import Faker
import random
from dotenv import load_dotenv
import os
fake = Faker()
categories = [
    "billing issue",
    "technical bug",
    "feature request",
    "account access",
    "performance issue"
]
# #GENERATING FAKER TICKETS
def generate_ticket():
    category = random.choice(categories)
    return {
        "ticket_id": fake.uuid4(),
        "customer": fake.name(),
        "email": fake.email(),
        "subject": f"{category.title()}",
        "description": fake.paragraph(nb_sentences=5),
        "actual_category": category
    }
tickets = [generate_ticket() for _ in range(100)]
print(tickets[0])



#GENERATING TICKETS USING GEMINI-2.5-FLASH
import google.generativeai as genai
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
prompt = """
Generate a realistic SaaS support ticket.

Category: Billing Issue

Return:
Subject:
Description:
"""
response = model.generate_content(prompt)
print(response.text)



# #TRIAGING TICKETS USING GEMINI-2.5-FLASH
def triage_ticket(ticket_text):
    prompt = f"""
    Classify this support ticket.

    Categories:
    - Billing
    - Technical
    - Feature Request
    - Account Access

    Also assign priority:
    Low, Medium, High

    Ticket:
    {ticket_text}

    Return JSON only.
    """
    response = model.generate_content(prompt)
    return response.text



# #TRIAGING TICKETS USING GEMINI-2.5-FLASH
import pandas as pd
results = []
for ticket in tickets:
    prediction = triage_ticket(ticket["description"])
    results.append({
        "ticket_id": ticket["ticket_id"],
        "prediction": prediction
    })
df = pd.DataFrame(results)
df.to_csv("triage_results.csv", index=False)


# #CREATING FEEDBACK TABLE
feedback = {
    "ticket_id": "123",
    "predicted_category": "Technical",
    "human_category": "Billing",
    "correct": False,
    "comments": "Misclassified invoice issue"
}

feedback_db = []
feedback_db.append(feedback)

feedback_df = pd.DataFrame(feedback_db)

override_rate = (
    feedback_df["correct"] == False
).mean()

print(
    f"Override Rate: {override_rate}"
)
