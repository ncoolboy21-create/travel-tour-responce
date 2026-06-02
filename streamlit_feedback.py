import streamlit as st
import pandas as pd
st.title("Ticket Triage Review")

ticket = {
    "subject": "Unable to access account",
    "prediction": "Technical"
}

st.write("Subject:", ticket["subject"])
st.write("Prediction:", ticket["prediction"])

correct = st.radio(
    "Was prediction correct?",
    ["Yes", "No"]
)


actual = st.selectbox(
    "Actual Category",
    ["Technical", "Billing", "Feature", "Access"]
)

if st.button("Submit"):
    if st.button("Submit"):
        feedback = {
            "subject": ticket["subject"],
            "predicted_category": ticket["prediction"],
            "actual_category": actual,
            "correct": correct
        }

        feedback_df = pd.DataFrame([feedback])

        feedback_df.to_csv(
            "feedback.csv",
            mode="a",
            header=False,
            index=False
        )

    st.success("Feedback saved")