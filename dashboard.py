import streamlit as st
import pandas as pd
import os


def load_worker_data():
    if not os.path.exists("workers.csv"):
        return pd.DataFrame(columns=["Worker ID", "Department", "Job role", "Shift", "PPE compliance", "Safety training status", "Fatigue level", "Safety observations", "Near misses", "Previous incidents"])
    return pd.read_csv("workers.csv")


def load_incident_data():
    if not os.path.exists("incidents.csv"):
        return pd.DataFrame(columns=["Incident ID", "Date", "Time", "Shift", "Location", "Department", "Incident type", "Severity", "Injury status", "Lost-time injury status", "Cause", "Corrective action", "Incident status"])
    return pd.read_csv("incidents.csv")


def load_equipment_data():
    if not os.path.exists("equipment.csv"):
        return pd.DataFrame(columns=["Equipment ID", "Equipment type", "Manufacturer", "Operating hours", "Temperature", "Vibration", "Fuel consumption", "Brake status", "Tyre status", "Engine status", "Maintenance status", "Downtime"])
    return pd.read_csv("equipment.csv")


def calculate_equipment_availability(equipment):
    total_time = equipment["Operating hours"] + equipment["Downtime"]
    availability = (equipment["Operating hours"] / total_time.replace(0, 1)) * 100
    return availability


def render_dashboard():
    st.title("Khwezi Mining Monitoring Dashboard")

    st.write("Central monitoring dashboard for health, safety and equipment information.")

    st.divider()

    # Load data from CSV files
    workers = load_worker_data()
    incidents = load_incident_data()
    equipment = load_equipment_data()

    # Worker Data
    total_workers = len(workers)
    total_near_misses = workers["Near misses"].sum() if not workers.empty else 0
    total_safety_observations = workers["Safety observations"].sum() if not workers.empty else 0
    average_ppe_compliance = workers["PPE compliance"].mean() if not workers.empty else 0.0

    # Incident Data (Fixed severity matching to include Serious, High, and Critical)
    total_incidents = len(incidents)
    if not incidents.empty:
        severity_col = incidents["Severity"].astype(str).str.strip().str.lower()
        serious_critical_incidents = len(incidents[severity_col.isin(["serious", "high", "critical"])])
    else:
        serious_critical_incidents = 0

    # Equipment Data (Account for all maintenance statuses: Operational, Under Maintenance, Due Soon, Overdue)
    total_equipment = len(equipment)
    if not equipment.empty:
        m_status = equipment["Maintenance status"].astype(str).str.strip().str.lower()
        equipment_available = len(equipment[m_status == "operational"])
        equipment_under_maintenance = len(equipment[m_status == "under maintenance"])
        equipment["Availability"] = calculate_equipment_availability(equipment)
        average_equipment_availability = equipment["Availability"].mean()
    else:
        equipment_available = 0
        equipment_under_maintenance = 0
        average_equipment_availability = 0.0

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

    st.divider()

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
    if not equipment.empty:
        st.dataframe(
            equipment[["Equipment ID", "Equipment type", "Manufacturer", "Temperature", "Vibration", "Maintenance status", "Downtime", "Availability"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No equipment data available.")

    st.divider()

    # Worker Table
    st.subheader("Worker Safety Information")
    if not workers.empty:
        st.dataframe(
            workers[["Worker ID", "Department", "Job role", "Shift", "PPE compliance", "Safety training status", "Fatigue level", "Safety observations", "Near misses", "Previous incidents"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No worker data available.")

    st.divider()

    # Incident Table
    st.subheader("Safety Incidents")
    if not incidents.empty:
        st.dataframe(
            incidents[["Incident ID", "Date", "Time", "Shift", "Location", "Department", "Incident type", "Severity", "Injury status", "Lost-time injury status", "Incident status"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No incident records available.")