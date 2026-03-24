def assign_delay_cause(row):

    delay = row["delay_minutes"]

    if delay <= 2:
        return "On Time"

    elif delay > 2 and delay <= 5:
        return "Passenger Boarding / Stop Dwell Time"

    elif delay > 5 and delay <= 8:
        return "Traffic Congestion on Route"

    elif delay > 8:
        return "Unrealistic Schedule / Route Delay"

    else:
        return "Operational Delay"