import streamlit as st
from feedback_service import save_feedback

st.title("Ticket Triage Review")

ticket = {
    "ticket_id": "123",
    "subject": "Unable to access account",
    "prediction": "Technical",
    "confidence": 0.87
}

st.write("Subject:", ticket["subject"])
st.write("Prediction:", ticket["prediction"])
st.write("Confidence:", ticket["confidence"])

correct = st.radio(
    "Was prediction correct?",
    ["Yes", "No"]
)

actual = st.selectbox(
    "Actual Category",
    [
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
)
if st.button("Submit"):
    feedback = {
        "ticket_id": ticket["ticket_id"],
        "predicted_category": ticket["prediction"],
        "actual_category": actual,
        "confidence": ticket["confidence"],
        "correct": correct == "Yes"
    }
    save_feedback(feedback)
    st.success("Feedback Saved")