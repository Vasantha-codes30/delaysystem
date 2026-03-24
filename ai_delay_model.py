import pandas as pd
from sklearn.tree import DecisionTreeClassifier

def train_model():

    data = pd.read_csv("data/stop_times.csv")

    # convert time to minutes
    data["scheduled_arrival"] = pd.to_datetime(data["scheduled_arrival"], format="%H:%M")
    data["actual_arrival"] = pd.to_datetime(data["actual_arrival"], format="%H:%M")

    data["delay_minutes"] = (
        data["actual_arrival"] - data["scheduled_arrival"]
    ).dt.total_seconds() / 60

    # label delay reason
    def label_reason(delay):
        if delay <= 2:
            return "On Time"
        elif delay <= 5:
            return "Passenger Boarding"
        elif delay <= 8:
            return "Traffic Congestion"
        else:
            return "Schedule Issue"

    data["reason"] = data["delay_minutes"].apply(label_reason)

    X = data[["delay_minutes"]]
    y = data["reason"]

    model = DecisionTreeClassifier()
    model.fit(X, y)

    return model