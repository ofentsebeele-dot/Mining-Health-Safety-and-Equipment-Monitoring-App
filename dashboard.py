import streamlit as st
import pandas as pd


def load_worker_data():
    return pd.read_csv("data/workers.csv")


def load_incident_data():
    return pd.read_csv("data/incidents.csv")


def load_equipment_data():
    return pd.read_csv("data/equipment.csv")


def calculate_equipment_availability(equipment_data):

    operating_time = equipment_data["Operating hours"]

    downtime = equipment_data["Downtime"]

    availability = (
        operating_time /
        (operating_time + downtime)
    ) * 100

    return availability


def render_dashboard():

    st.title("Khwezi Mining Monitoring Dashboard")

    st.write(
        "Central monitoring view for Khwezi Mining operations."
    )

    st.divider()

    # Load CSV files
    workers = load_worker_data()
    incidents = load_incident_data()
    equipment = load_equipment_data()

    # -----------------------------
    # WORKER DATA
    # -----------------------------

    total_workers = len(workers)

    near_misses = workers["Near misses"].sum()

    safety_observations = workers[
        "Safety observations"
    ].sum()

    ppe_compliance = workers[
        "PPE compliance"
    ].mean()

    # -----------------------------
    # INCIDENT DATA
    # -----------------------------

    total_incidents = len(incidents)

    high_severity_incidents = len(
        incidents[
            incidents["Severity"].isin(
                ["Serious", "Critical"]
            )
        ]
    )

    # -----------------------------
    # EQUIPMENT DATA
    # -----------------------------

    total_equipment = len(equipment)

    available_equipment = len(
        equipment[
            equipment["Maintenance status"] == "Operational"
        ]
    )

    equipment_under_maintenance = len(
        equipment[
            equipment["Maintenance status"] == "Under Maintenance"
        ]
    )

    # Calculate availability
    equipment["Availability"] = calculate_equipment_availability(
        equipment
    )

    average_availability = equipment[
        "Availability"
    ].mean()

    # -----------------------------
    # DASHBOARD
    # -----------------------------

    st.subheader("Health & Safety")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Workers",
            total_workers
        )

    with col2:
        st.metric(
            "Safety Incidents",
            total_incidents
        )

    with col3:
        st.metric(
            "Near Misses",
            near_misses
        )

    with col4:
        st.metric(
            "Safety Observations",
            safety_observations
        )

    st.divider()

    st.subheader("Worker Safety")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Average PPE Compliance",
            f"{ppe_compliance:.1f}%"
        )

    with col2:
        st.metric(
            "Serious/Critical Incidents",
            high_severity_incidents
        )

    st.divider()

    st.subheader("Equipment Monitoring")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Equipment",
            total_equipment
        )

    with col2:
        st.metric(
            "Available Equipment",
            available_equipment
        )

    with col3:
        st.metric(
            "Under Maintenance",
            equipment_under_maintenance
        )

    with col4:
        st.metric(
            "Average Availability",
            f"{average_availability:.1f}%"
        )

    st.divider()

    st.subheader("Equipment Status")

    st.dataframe(
        equipment[
            [
                "Equipment ID",
                "Equipment type",
                "Temperature",
                "Vibration",
                "Maintenance status",
                "Downtime",
                "Availability"
            ]
        ],
        use_container_width=True
    )

    st.divider()

    st.subheader("Safety Summary")

    st.dataframe(
        workers[
            [
                "Worker ID",
                "Department",
                "Shift",
                "PPE compliance",
                "Fatigue level",
                "Near misses",
                "Previous incidents"
            ]
        ],
        use_container_width=True
    )
