import streamlit as st
import pandas as pd
from analytics_service import (
    calculate_metrics,
    threshold_analysis,
    generate_drift_dashboard,
    validate_kpis)

df = pd.read_csv("feedback.csv")
metrics = calculate_metrics(df)
threshold_df = threshold_analysis(df)
drift_df = generate_drift_dashboard(df)
kpis = validate_kpis(df)

st.title("Analytics Dashboard")

st.metric(
    "Override Rate",
    f"{metrics['override_rate']:.2%}")

st.metric(
    "Accept Rate",
    f"{metrics['accept_rate']:.2%}")

st.metric(
    "Accepted Accuracy",
    f"{metrics['accepted_accuracy']:.2%}")

st.dataframe(df)

st.subheader("Threshold Analysis")
st.dataframe(threshold_df)

st.subheader("Acceptance Rate Drift")
st.dataframe(drift_df)

st.line_chart(drift_df.set_index("date"))
st.subheader("Threshold Analysis")
st.dataframe(threshold_df)

