import pandas as pd

# Existing modules
from delay_calculator import calculate_delay
from delay_rules import assign_delay_cause
from report_generator import generate_stop_report, generate_route_report

# Advanced feature modules
from heatmap_analysis import generate_delay_heatmap
from congestion_detector import detect_hotspots
from schedule_analysis import analyze_schedule
from pdf_report import generate_pdf


def main():

    print("Loading datasets...")

    # Load datasets
    stop_times = pd.read_csv("data/stop_times.csv")
    trips = pd.read_csv("data/trips.csv")

    print("Calculating delays...")

    # Calculate delay
    stop_times = calculate_delay(stop_times)

    print("Assigning delay causes...")

    # Assign delay cause
    stop_times["cause"] = stop_times.apply(assign_delay_cause, axis=1)

    print("Generating stop-wise report...")

    # Generate stop report
    stop_report = generate_stop_report(stop_times)

    print("Generating route-wise report...")

    # Generate route report
    route_report = generate_route_report(stop_times, trips)

    # Save reports
    stop_report.to_csv("output/stop_delay_report.csv", index=False)
    route_report.to_csv("output/route_delay_report.csv", index=False)

    print("Running advanced analysis...")

    # 1️⃣ Delay Heatmap
    heatmap = generate_delay_heatmap(stop_times)
    heatmap.to_csv("output/delay_heatmap.csv")

    # 2️⃣ Congestion Hotspot Detection
    hotspots = detect_hotspots(stop_times)
    hotspots.to_csv("output/congestion_hotspots.csv", index=False)

    # 3️⃣ Schedule Feasibility Analysis
    schedule_report = analyze_schedule(stop_times)
    schedule_report.to_csv("output/schedule_analysis.csv", index=False)

    # 4️⃣ Generate Automated PDF Report
    generate_pdf(route_report)

    print("All analysis completed successfully.")
    print("Check the 'output' folder for results.")


if __name__ == "__main__":
    main()