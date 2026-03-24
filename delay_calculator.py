import pandas as pd

def calculate_delay(stop_times):

    stop_times['scheduled_arrival'] = pd.to_datetime(stop_times['scheduled_arrival'], format='%H:%M')
    stop_times['actual_arrival'] = pd.to_datetime(stop_times['actual_arrival'], format='%H:%M')

    stop_times['delay_minutes'] = (
        stop_times['actual_arrival'] - stop_times['scheduled_arrival']
    ).dt.total_seconds() / 60

    stop_times['delay_minutes'] = stop_times['delay_minutes'].fillna(0)

    return stop_times