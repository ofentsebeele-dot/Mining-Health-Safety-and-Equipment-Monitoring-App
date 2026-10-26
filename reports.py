import streamlit as st
import pandas as pd
import os


def load_worker_data():
    if not os.path.exists("workers.csv"):
        return pd.DataFrame()
    return pd.read_csv("workers.csv")


def load_incident_data():
    if not os.path.exists("incidents.csv"):
        return pd.DataFrame()
    return pd.read_csv("incidents.csv")


def load_equipment_data():
    if not os.path.exists("equipment.csv"):
        return pd.DataFrame()
    return pd.read_csv("equipment.csv")


def render_reports_page():
    workers = load_worker_data()
    incidents = load_incident_data()
    equipment = load_equipment_data()

    st.title("Reports")

    st.write(
        "Summary reports for worker safety, incidents and equipment."
    )

    st.divider()

    # Overall Summary
    st.subheader("Overall Summary")

    total_workers = len(workers)
    total_incidents = len(incidents)
    total_equipment = len(equipment)

    total_near_misses = workers["Near misses"].sum() if not workers.empty and "Near misses" in workers.columns else 0
    total_downtime = equipment["Downtime"].sum() if not equipment.empty and "Downtime" in equipment.columns else 0.0

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Workers", total_workers)

    with col2:
        st.metric("Incidents", total_incidents)

    with col3:
        st.metric("Equipment", total_equipment)

    with col4:
        st.metric("Near Misses", total_near_misses)

    with col5:
        st.metric("Downtime", f"{total_downtime:.1f} hrs")

    st.divider()

    # Incident Report
    st.subheader("Incident Report")
    if not incidents.empty and "Incident type" in incidents.columns:
        st.bar_chart(incidents["Incident type"].astype(str).value_counts())
    else:
        st.info("No incident data for reports.")

    st.divider()

    # Incident Severity
    st.subheader("Incident Severity")
    if not incidents.empty and "Severity" in incidents.columns:
        st.bar_chart(incidents["Severity"].astype(str).value_counts())
    else:
        st.info("No severity data available.")

    st.divider()

    # Worker Safety
    st.subheader("Worker Safety Report")
    if not workers.empty:
        average_ppe = workers["PPE compliance"].mean() if "PPE compliance" in workers.columns else 0.0
        total_observations = workers["Safety observations"].sum() if "Safety observations" in workers.columns else 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average PPE Compliance", f"{average_ppe:.1f}%")
        with col2:
            st.metric("Safety Observations", total_observations)
        with col3:
            st.metric("Near Misses", total_near_misses)
    else:
        st.info("No worker data available.")

    st.divider()

    # Equipment Report
    st.subheader("Equipment Report")
    if not equipment.empty and "Equipment type" in equipment.columns:
        st.bar_chart(equipment["Equipment type"].astype(str).value_counts())
    else:
        st.info("No equipment data available.")

    st.divider()

    # Equipment Downtime
    st.subheader("Equipment Downtime")
    if not equipment.empty and "Equipment type" in equipment.columns and "Downtime" in equipment.columns:
        downtime_by_type = equipment.groupby("Equipment type")["Downtime"].sum().sort_values(ascending=False)
        st.bar_chart(downtime_by_type)
    else:
        st.info("No downtime data available.")

    st.divider()

    # Maintenance Status
    st.subheader("Maintenance Status")
    if not equipment.empty and "Maintenance status" in equipment.columns:
        st.bar_chart(equipment["Maintenance status"].astype(str).value_counts())
    else:
        st.info("No maintenance status data available.")

    st.divider()

    # Data Tables
    st.subheader("Incident Data")
    if not incidents.empty:
        st.dataframe(incidents, use_container_width=True, hide_index=True)

    st.subheader("Equipment Data")
    if not equipment.empty:
        st.dataframe(equipment, use_container_width=True, hide_index=True)