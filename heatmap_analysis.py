import pandas as pd

def generate_delay_heatmap(df):

    df["hour"] = pd.to_datetime(df["scheduled_arrival"]).dt.hour

    heatmap = df.pivot_table(
        values="delay_minutes",
        index="stop_id",
        columns="hour",
        aggfunc="mean"
    )

    return heatmap