import pandas as pd
import os
FEEDBACK_FILE = "feedback.csv"
def save_feedback(record):
    df = pd.DataFrame([record])
    header = not os.path.exists(FEEDBACK_FILE)
    df.to_csv(
        FEEDBACK_FILE,
        mode="a",
        header=header,
        index=False
    )