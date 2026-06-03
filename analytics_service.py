import pandas as pd

def calculate_metrics(df):
    override_rate = (
        (~df["correct"])
        .mean())

    accept_rate = (
        (df["confidence"] >= 0.8)
        .mean())

    accepted = df[
        df["confidence"] >= 0.8]

    accepted_accuracy = (
        accepted["correct"].mean()
        if len(accepted) > 0
        else 0)

    return {
        "override_rate": override_rate,
        "accept_rate": accept_rate,
        "accepted_accuracy": accepted_accuracy
    }

#####
def threshold_analysis(df):
    thresholds = [0.5, 0.6, 0.7, 0.8, 0.9]
    analysis = []
    for t in thresholds:
        auto = df[
            df["confidence"] >= t
        ]
        analysis.append({
            "threshold": t,
            "accept_rate":
                len(auto) / len(df),#auto_update/total

            "accuracy":
                auto["correct"].mean()
                if len(auto) > 0
                else 0
        })
    threshold_df = pd.DataFrame(analysis)
    threshold_df.to_csv(
        "threshold_analysis.csv",
        index=False
    )
    return threshold_df


#####
def generate_drift_dashboard(df):
    if "date" not in df.columns:
        df["date"] = pd.Timestamp.today()
    drift = (
        df.groupby(pd.to_datetime(df["date"]).dt.date)
        .agg(acceptance_rate=("correct", "mean"))
        .reset_index())
    drift.to_csv("drift_dashboard.csv",index=False)
    return drift


######
def validate_kpis(df):
    auto_draft_rate = (df["confidence"] >= 0.8).mean()
    accepted = df[df["confidence"] >= 0.8]
    acceptance_rate = (accepted["correct"].mean()
        if len(accepted) > 0
        else 0)
    return {
        "auto_draft_rate":auto_draft_rate,
        "acceptance_rate":acceptance_rate,
        "auto_draft_pass":auto_draft_rate >= 0.5,
        "acceptance_pass":acceptance_rate >= 0.8}
