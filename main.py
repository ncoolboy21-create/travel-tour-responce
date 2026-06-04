import pandas as pd
from ticket_generator import generate_tickets
from triage_engine import triage_ticket
from escalation_service import route_ticket
from analytics_service import (
    calculate_metrics,
    threshold_analysis,
    generate_drift_dashboard,
    validate_kpis
)


print("Generating tickets...")
tickets = generate_tickets(3)
print(f"{len(tickets)} tickets generated")



print("Running Gemini triage...")
triage_results = []
for ticket in tickets:
    prediction = triage_ticket(
        f"""
        Subject:
        {ticket['subject']}

        Description:
        {ticket['description']}
        """
    )
    triage_results.append({
        "ticket_id": ticket["ticket_id"],
        "subject": ticket["subject"],
        "actual_category": ticket["actual_category"],
        "predicted_category":prediction["category"],
        "priority":prediction["priority"],
        "confidence":prediction["confidence"]
    })
triage_df = pd.DataFrame(triage_results)
triage_df.to_csv(
    "triage_results.csv",
    index=False
)
print("Triage results saved")



print("Running routing engine...")
routing_results = []
for _, row in triage_df.iterrows():
    route = route_ticket(
        row["predicted_category"],
        row["confidence"]
    )

    routing_results.append({
        "ticket_id":row["ticket_id"],
        "category":row["predicted_category"],
        "confidence":row["confidence"],
        "action":route["action"],
        "team":route["team"],
        "auto_response":route["auto_response"]
    })
routing_df = pd.DataFrame(routing_results)
routing_df.to_csv(
    "routing_decisions.csv",
    index=False
)
print("Routing decisions saved")



print("Creating feedback records...")
feedback_records = []
for _, row in triage_df.iterrows():
    predicted = (str(row["predicted_category"]).lower())
    actual = (str(row["actual_category"]).lower())
    correct = (predicted == actual)
    feedback_records.append({
        "ticket_id":row["ticket_id"],
        "predicted_category":row["predicted_category"],
        "actual_category":row["actual_category"],
        "confidence":row["confidence"],
        "correct":correct
    })
feedback_df = pd.DataFrame(feedback_records)
feedback_df.to_csv(
    "feedback.csv",
    index=False
)

print("Feedback dataset saved")




metrics = calculate_metrics(feedback_df)
print("\nMetrics")
print("-" * 40)
print(
    f"Override Rate: "
    f"{metrics['override_rate']:.2%}"
)
print(
    f"Accept Rate: "
    f"{metrics['accept_rate']:.2%}"
)
print(
    f"Accepted Accuracy: "
    f"{metrics['accepted_accuracy']:.2%}"
)




print("\nRunning threshold analysis...")
threshold_df = threshold_analysis(feedback_df)
print(threshold_df)


print("\nGenerating drift dashboard...")
feedback_df["date"] = pd.Timestamp.today()
drift_df = generate_drift_dashboard(
    feedback_df)
print(drift_df)



print("\nValidating KPIs...")
kpis = validate_kpis(feedback_df)
print(
    f"Auto Draft Rate: "
    f"{kpis['auto_draft_rate']:.2%}"
)
print(
    f"Acceptance Rate: "
    f"{kpis['acceptance_rate']:.2%}"
)
if kpis["auto_draft_pass"]:
    print("PASS: >= 50% Auto Draft")
else:
    print("FAIL: < 50% Auto Draft")

if kpis["acceptance_pass"]:
    print("PASS: >= 80% Acceptance")
else:
    print("FAIL: < 80% Acceptance")

print("\nPipeline completed successfully")