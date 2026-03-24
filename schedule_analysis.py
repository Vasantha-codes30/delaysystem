import pandas as pd

def analyze_schedule(df):

    df["scheduled_arrival"] = pd.to_datetime(df["scheduled_arrival"])
    df["actual_arrival"] = pd.to_datetime(df["actual_arrival"])

    df["schedule_delay"] = (
        df["actual_arrival"] - df["scheduled_arrival"]
    ).dt.total_seconds()/60

    df["schedule_status"] = df["schedule_delay"].apply(
        lambda x: "Unrealistic" if x > 5 else "Feasible"
    )

    return df