import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from streamlit_autorefresh import st_autorefresh
import random
from fpdf import FPDF

# ----------------------------
# Login System
# ----------------------------
users = {
    "admin": "admin123",
    "viewer": "viewer123"
}

st.sidebar.title("Login")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

login_button = st.sidebar.button("Login")

if login_button:
    if username in users and users[username] == password:
        st.session_state["logged_in"] = True
        st.session_state["role"] = username
    else:
        st.sidebar.error("Invalid login")

if "logged_in" not in st.session_state:
    st.warning("Please login to access dashboard")
    st.stop()

# ----------------------------
# Dashboard Title
# ----------------------------
st.title("Offline Public Transport Delay Attribution System")
st.subheader("Shivamogga Smart Transport Analytics Dashboard")

st.write(
"This dashboard analyzes bus delays and identifies congestion patterns, delay causes and route performance."
)

# ----------------------------
# Load Data
# ----------------------------
route_report = pd.read_csv("output/route_delay_report.csv")
stop_report = pd.read_csv("output/stop_delay_report.csv")
hotspots = pd.read_csv("output/congestion_hotspots.csv")

# ----------------------------
# Route Delay Report
# ----------------------------
st.header("Route Delay Report")
st.dataframe(route_report)

# ----------------------------
# Stop Delay Report
# ----------------------------
st.header("Stop Delay Report")
st.dataframe(stop_report)

# ----------------------------
# Congestion Hotspots
# ----------------------------
st.header("Congestion Hotspots")
st.dataframe(hotspots)

# ----------------------------
# Route Congestion Graph
# ----------------------------
st.header("Route Congestion Graph")

fig1, ax1 = plt.subplots()
ax1.bar(route_report["route_id"], route_report["avg_delay"])
ax1.set_xlabel("Route ID")
ax1.set_ylabel("Average Delay (minutes)")
ax1.set_title("Average Delay by Route")

st.pyplot(fig1)

# ----------------------------
# Stop Delay Bar Chart
# ----------------------------
st.header("Stop Delay Bar Chart")

fig2, ax2 = plt.subplots()
ax2.bar(stop_report["stop_id"], stop_report["avg_delay"])
ax2.set_xlabel("Stop ID")
ax2.set_ylabel("Average Delay (minutes)")
ax2.set_title("Average Delay by Stop")

st.pyplot(fig2)

# ----------------------------
# Delay Heatmap
# ----------------------------
st.header("Delay Heatmap")

heatmap_data = stop_report.pivot_table(
    values="avg_delay",
    index="stop_id"
)

fig3, ax3 = plt.subplots()
sns.heatmap(heatmap_data, annot=True, cmap="Reds", ax=ax3)

st.pyplot(fig3)

# ----------------------------
# Delay Reason Detection
# ----------------------------
st.header("Delay Reason Detection")

reason_data = stop_report.copy()

reason_data["reason"] = reason_data["avg_delay"].apply(
    lambda x: "Passenger Boarding Delay" if x <= 5
    else "Traffic Congestion" if x <= 8
    else "Unrealistic Schedule"
)

st.dataframe(reason_data)

# ----------------------------
# Interactive Delay Simulator
# ----------------------------
st.header("Interactive Delay Simulator")

delay_input = st.slider(
    "Select delay minutes",
    min_value=0,
    max_value=20,
    value=5
)

def predict_reason(delay):
    if delay <= 2:
        return "On Time"
    elif delay <= 5:
        return "Passenger Boarding Delay"
    elif delay <= 8:
        return "Traffic Congestion"
    else:
        return "Unrealistic Schedule"

st.success(predict_reason(delay_input))

# ----------------------------
# Real-Time Simulation
# ----------------------------
st.header("Real-Time Bus Delay Simulation")

st_autorefresh(interval=5000, key="simulation")

routes = ["R1","R2","R3","R4","R5"]

simulation_data = []

for route in routes:
    delay = random.randint(0,15)

    if delay <= 2:
        reason="On Time"
    elif delay <= 5:
        reason="Passenger Boarding"
    elif delay <= 8:
        reason="Traffic Congestion"
    else:
        reason="Schedule Issue"

    simulation_data.append({
        "route":route,
        "delay_minutes":delay,
        "predicted_reason":reason
    })

st.dataframe(pd.DataFrame(simulation_data))

# ----------------------------
# Admin Control Panel
# ----------------------------
if st.session_state["role"] == "admin":

    st.header("Admin Control Panel")

    uploaded_file = st.file_uploader(
        "Upload new stop_times dataset",
        type=["csv"]
    )

    if uploaded_file:

        new_data = pd.read_csv(uploaded_file)

        st.subheader("Uploaded Data Preview")
        st.dataframe(new_data)

# ----------------------------
# Download Reports
# ----------------------------
st.header("Download Analytics Reports")

excel_file = "output/transport_report.xlsx"

with pd.ExcelWriter(excel_file) as writer:
    route_report.to_excel(writer, sheet_name="Route Delay", index=False)
    stop_report.to_excel(writer, sheet_name="Stop Delay", index=False)
    hotspots.to_excel(writer, sheet_name="Hotspots", index=False)

with open(excel_file,"rb") as f:
    st.download_button(
        "Download Excel Report",
        f,
        "transport_delay_report.xlsx"
    )

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

pdf.cell(200,10,"Shivamogga Bus Delay Analysis",ln=True)

for i,row in route_report.iterrows():
    pdf.cell(
        200,8,
        f"Route {row['route_id']} Avg Delay {row['avg_delay']} min",
        ln=True
    )

pdf_file="output/transport_report.pdf"
pdf.output(pdf_file)

with open(pdf_file,"rb") as f:
    st.download_button(
        "Download PDF Report",
        f,
        "transport_delay_report.pdf"
    )