import pandas as pd

def detect_hotspots(df):

    hotspots = df.groupby("stop_id")["delay_minutes"].mean()

    hotspots = hotspots.reset_index()

    hotspots["status"] = hotspots["delay_minutes"].apply(
        lambda x: "Hotspot" if x > 6 else "Normal"
    )

    return hotspots