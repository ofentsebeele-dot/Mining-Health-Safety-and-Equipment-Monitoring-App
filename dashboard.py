# Dashboard

import os
import base64
from datetime import datetime

import pandas as pd
import streamlit as st

try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


# 1. Load CSV files

def find_csv_path(filename):
    possible_paths = [ 
        filename, 
        os.path.join("data", filename) 
    ]

    for path in possible_paths:
        if os.path.isfile(path):
            return path

    return None


def load_csv(filename):
    path = find_csv_path(filename)

    if path is None:
        raise FileNotFoundError(
            f"Cannot find {filename}. "
            "Place it in the project folder or the data folder."
        )

    return pd.read_csv(path)


def load_worker_data():
    return load_csv("workers.csv")


def load_incident_data():
    return load_csv("incidents.csv")


def load_equipment_data():
    return load_csv("equipment.csv")


<<<<<<< HEAD
# 2. Helper Functions

def numeric_column(data, column_name):
    if column_name not in data.columns:
        return pd.Series(float("nan"), index=data.index)

    values = data[column_name].astype(str).str.strip()
    values = values.str.replace("%", "", regex=False)

    return pd.to_numeric(values, errors="coerce")


def category_column(data, column_name):
    if column_name not in data.columns:
        return pd.Series("Unknown", index=data.index)

    values = (
        data[column_name]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    return values.replace("", "Unknown")


def show_table(data, columns):
    available = [
        column for column in columns
        if column in data.columns
    ]

    if available:
        st.dataframe(
            data[available],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(
            "The expected columns are not available in this CSV."
        )


# ============================================================
# 3. BACKGROUND IMAGE AND TEXT STYLING
# ============================================================

def set_background(image_file="mine_background.png"):
    path = find_csv_path(image_file)

    if path is None:
        return

    try:
        with open(path, "rb") as image:
            encoded_image = base64.b64encode(
                image.read()
            ).decode("utf-8")

        st.markdown(
            f"""
            <style>

            /* Keep the mine background and existing overlay */
            .stApp {{
                background-image:
                    linear-gradient(
                        rgba(8, 20, 31, 0.84),
                        rgba(8, 20, 31, 0.84)
                    ),
                    url("data:image/png;base64,{encoded_image}");

                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            /* Main dashboard headings */
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp h4 {{
                color: #FFFFFF !important;
                font-weight: 800 !important;
                text-shadow: 1px 1px 3px #000000;
            }}

            /* Paragraphs, labels and general text */
            .stApp p,
            .stApp label {{
                color: #FFFFFF !important;
                font-weight: 600 !important;
            }}

            /* Metric cards */
            [data-testid="stMetric"] {{
                background-color: rgba(0, 0, 0, 0.65);
                border: 1px solid rgba(255, 255, 255, 0.65);
                border-radius: 10px;
                padding: 14px;
            }}

            /* Strong white KPI numbers */
            [data-testid="stMetricValue"],
            [data-testid="stMetricValue"] * {{
                color: #FFFFFF !important;
                font-weight: 800 !important;
                opacity: 1 !important;
                text-shadow: 1px 1px 2px #000000;
            }}

            /* Strong white KPI labels */
            [data-testid="stMetricLabel"],
            [data-testid="stMetricLabel"] * {{
                color: #FFFFFF !important;
                font-weight: 700 !important;
                opacity: 1 !important;
            }}

            /* KPI delta text */
            [data-testid="stMetricDelta"],
            [data-testid="stMetricDelta"] * {{
                color: #FFFFFF !important;
                opacity: 1 !important;
            }}

            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: #101820;
            }}

            [data-testid="stSidebar"] * {{
                color: #FFFFFF !important;
            }}

            /* Expandable table sections */
            [data-testid="stExpander"] {{
                background-color: rgba(0, 0, 0, 0.60);
                border: 1px solid rgba(255, 255, 255, 0.35);
                border-radius: 8px;
            }}

            [data-testid="stExpander"] summary,
            [data-testid="stExpander"] summary p {{
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }}

            /* Data table container */
            [data-testid="stDataFrame"] {{
                border: 1px solid rgba(255, 255, 255, 0.35);
                border-radius: 6px;
            }}

            /* Informational messages */
            [data-testid="stAlert"] p {{
                color: #FFFFFF !important;
                font-weight: 600 !important;
            }}

            /* Captions */
            [data-testid="stCaptionContainer"] {{
                color: #FFFFFF !important;
            }}

            /* Dividers */
            hr {{
                border-color: rgba(255, 255, 255, 0.55) !important;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    except OSError:
        pass


# ============================================================
# 4. EQUIPMENT AVAILABILITY
# ============================================================

def calculate_availability(equipment):
    operating = numeric_column(equipment, "Operating hours")
    downtime = numeric_column(equipment, "Downtime")

    total_time = operating + downtime

    availability = (
        operating / total_time.where(total_time > 0)
    ) * 100

=======
def calculate_equipment_availability(equipment):

    availability = (equipment["Operating hours"]/(equipment["Operating hours"] + equipment["Downtime"])) * 100

    return availability


# ============================================================
# 5. CHART FUNCTIONS
# ============================================================

<<<<<<< HEAD
def style_plotly_chart(fig):
    """Improve Plotly chart text against the dashboard background."""

    fig.update_layout(
        font=dict(
            color="#FFFFFF",
            size=14,
            family="Arial"
        ),
        title_font=dict(
            color="#FFFFFF",
            size=19,
            family="Arial"
        ),
        paper_bgcolor="rgba(0,0,0,0.55)",
        plot_bgcolor="rgba(0,0,0,0.35)",
        legend=dict(
            font=dict(color="#FFFFFF", size=12)
        ),
        margin=dict(l=25, r=25, t=65, b=35)
    )
=======
    st.title("Khwezi Mining Monitoring Dashboard")

    st.write("Central monitoring dashboard for health, " "safety and equipment information.")

    st.divider()

    # Load data from CSV files
    workers = load_worker_data()
    incidents = load_incident_data()
    equipment = load_equipment_data()

    
    # Worker Data

    total_workers = len(workers)

    total_near_misses = workers["Near misses"].sum()

    total_safety_observations = workers["Safety observations"].sum()

    average_ppe_compliance = workers["PPE compliance"].mean()

    # Incident Data

    total_incidents = len(incidents)

    serious_critical_incidents = len(incidents[incidents["Severity"].isin( ["Serious", "Critical"] )] )

    # Equipment Data

    total_equipment = len(equipment)

    equipment_available = len(equipment[equipment["Maintenance status"]== "Operational"])

    equipment_under_maintenance = len(equipment[equipment["Maintenance status"] == "Under Maintenance"])

    # Calculate availability
    equipment["Availability"] = (calculate_equipment_availability(equipment))

    average_equipment_availability = (equipment["Availability"].mean() )

    # Dashboard KPI Section

    st.subheader("Health & Safety")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Workers", total_workers)

    with col2:
        st.metric("Safety Incidents", total_incidents)

    with col3:
        st.metric("Near Misses", total_near_misses)

    with col4:
        st.metric("Safety Observations", total_safety_observations)

    st.divider()

    # Second KPI row

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("PPE Compliance", f"{average_ppe_compliance:.1f}%")

    with col2:
        st.metric("Serious/Critical Incidents", serious_critical_incidents)

    with col3:
        st.metric("Total Equipment", total_equipment)
>>>>>>> 3dc928d (updated)

    if not PLOTLY_AVAILABLE:
        st.info(
            "To enable interactive pie charts and histograms, "
            "add plotly to requirements.txt."
        )

<<<<<<< HEAD

# ============================================================
# 7. DASHBOARD ENTRY POINT AND AUTOMATIC REFRESH
# ============================================================

if hasattr(st, "fragment"):

    @st.fragment(run_every=30)
    def render_dashboard():
        render_dashboard_content()

else:

    def render_dashboard():
        render_dashboard_content()
=======
    # Equipment KPI Section

    st.subheader("Equipment Monitoring")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Available Equipment", equipment_available)

    with col2:
        st.metric("Under Maintenance", equipment_under_maintenance)

    with col3:
        st.metric("Average Availability", f"{average_equipment_availability:.1f}%")

    st.divider()

    # Equipment Table

    st.subheader("Equipment Status")

    st.dataframe(
        equipment[["Equipment ID", "Equipment type", "Manufacturer", "Temperature", "Vibration", "Maintenance status", "Downtime", "Availability"]],use_container_width=True)

    st.divider()

    # Worker Table

    st.subheader("Worker Safety Information")

    st.dataframe(workers[["Worker ID", "Department", "Job role", "Shift", "PPE compliance", "Safety training status", "Fatigue level", "Safety observations", "Near misses", "Previous incidents"]], use_container_width=True)

    st.divider()

    # Incident Tabe

    st.subheader("Safety Incidents")

    st.dataframe(incidents[["Incident ID", "Date", "Time", "Shift", "Location", "Department", "Incident type", "Severity", "Injury status", "Lost-time injury status", "Incident status"]], use_container_width=True)
