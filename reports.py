import streamlit as st
import pandas as pd


def load_worker_data():
    return pd.read_csv("workers.csv")


def load_incident_data():
    return pd.read_csv("incidents.csv")


def load_equipment_data():
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

    # --------------------------------------------------
    # OVERALL SUMMARY
    # --------------------------------------------------

    st.subheader("Overall Summary")

    total_workers = len(workers)
    total_incidents = len(incidents)
    total_equipment = len(equipment)

    total_near_misses = workers[
        "Near misses"
    ].sum()

    total_downtime = equipment[
        "Downtime"
    ].sum()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Workers",
            total_workers
        )

    with col2:
        st.metric(
            "Incidents",
            total_incidents
        )

    with col3:
        st.metric(
            "Equipment",
            total_equipment
        )

    with col4:
        st.metric(
            "Near Misses",
            total_near_misses
        )

    with col5:
        st.metric(
            "Downtime",
            f"{total_downtime:.1f} hrs"
        )

    st.divider()

    # --------------------------------------------------
    # INCIDENT REPORT
    # --------------------------------------------------

    st.subheader("Incident Report")

    incident_types = (
        incidents["Incident type"]
        .astype(str)
        .value_counts()
    )

    st.bar_chart(
        incident_types
    )

    st.divider()

    # --------------------------------------------------
    # INCIDENT SEVERITY
    # --------------------------------------------------

    st.subheader("Incident Severity")

    severity_counts = (
        incidents["Severity"]
        .astype(str)
        .value_counts()
    )

    st.bar_chart(
        severity_counts
    )

    st.divider()

    # --------------------------------------------------
    # WORKER SAFETY
    # --------------------------------------------------

    st.subheader("Worker Safety Report")

    average_ppe = workers[
        "PPE compliance"
    ].mean()

    total_observations = workers[
        "Safety observations"
    ].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Average PPE Compliance",
            f"{average_ppe:.1f}%"
        )

    with col2:
        st.metric(
            "Safety Observations",
            total_observations
        )

    with col3:
        st.metric(
            "Near Misses",
            total_near_misses
        )

    st.divider()

    # --------------------------------------------------
    # EQUIPMENT REPORT
    # --------------------------------------------------

    st.subheader("Equipment Report")

    equipment_type_count = (
        equipment["Equipment type"]
        .astype(str)
        .value_counts()
    )

    st.bar_chart(
        equipment_type_count
    )

    st.divider()

    # --------------------------------------------------
    # EQUIPMENT DOWNTIME
    # --------------------------------------------------

    st.subheader("Equipment Downtime")

    downtime_by_type = (
        equipment
        .groupby("Equipment type")["Downtime"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(
        downtime_by_type
    )

    st.divider()

    # --------------------------------------------------
    # MAINTENANCE REPORT
    # --------------------------------------------------

    st.subheader("Maintenance Status")

    maintenance_counts = (
        equipment["Maintenance status"]
        .astype(str)
        .value_counts()
    )

    st.bar_chart(
        maintenance_counts
    )

    st.divider()

    # --------------------------------------------------
    # DATA TABLES
    # --------------------------------------------------

    st.subheader("Incident Data")

    st.dataframe(
        incidents,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("Equipment Data")

    st.dataframe(
        equipment,
        use_container_width=True,
        hide_index=True
    )
