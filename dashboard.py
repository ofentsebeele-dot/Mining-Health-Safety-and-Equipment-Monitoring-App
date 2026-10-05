import streamlit as st
import pandas as pd


def load_worker_data():
    return pd.read_csv("workers.csv")


def load_incident_data():
    return pd.read_csv("incidents.csv")


def load_equipment_data():
    return pd.read_csv("equipment.csv")


def calculate_equipment_availability(equipment):

    availability = (equipment["Operating hours"]/(equipment["Operating hours"] + equipment["Downtime"])) * 100

    return availability


def render_dashboard():

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
