import pandas as pd

def generate_stop_report(df):

    report = df.groupby("stop_id").agg(
        avg_delay=("delay_minutes","mean"),
        trips=("trip_id","count")
    ).reset_index()

    return report


def generate_route_report(df, trips):

    merged = pd.merge(df, trips, on="trip_id")

    report = merged.groupby("route_id").agg(
        avg_delay=("delay_minutes","mean"),
        trips=("trip_id","count")
    ).reset_index()

    return report