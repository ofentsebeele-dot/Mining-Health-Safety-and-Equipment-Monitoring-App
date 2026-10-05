import streamlit as st
import pandas as pd


def load_incident_data():
    return pd.read_csv("incidents.csv")


def render_incidents_page():

    incidents = load_incident_data()

    st.title("Safety Incidents")

    st.write(
        "Monitor, filter and review reported safety incidents."
    )

    st.divider()

    # ---------------------------------------------
    # SUMMARY
    # ---------------------------------------------

    total_incidents = len(incidents)

    serious_incidents = len(
        incidents[
            incidents["Severity"] == "Serious"
        ]
    )

    critical_incidents = len(
        incidents[
            incidents["Severity"] == "Critical"
        ]
    )

    lost_time_injuries = len(
        incidents[
            incidents["Lost-time injury status"] == "Yes"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Incidents",
            total_incidents
        )

    with col2:
        st.metric(
            "Serious Incidents",
            serious_incidents
        )

    with col3:
        st.metric(
            "Critical Incidents",
            critical_incidents
        )

    with col4:
        st.metric(
            "Lost-Time Injuries",
            lost_time_injuries
        )

    st.divider()

    # ---------------------------------------------
    # FILTERS
    # ---------------------------------------------

    st.subheader("Incident Filters")

    col1, col2, col3 = st.columns(3)

    with col1:

        department_options = ["All"] + sorted(
            incidents["Department"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_department = st.selectbox(
            "Department",
            department_options
        )

    with col2:

        severity_options = ["All"] + sorted(
            incidents["Severity"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_severity = st.selectbox(
            "Severity",
            severity_options
        )

    with col3:

        status_options = ["All"] + sorted(
            incidents["Incident status"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_status = st.selectbox(
            "Incident Status",
            status_options
        )

    # ---------------------------------------------
    # APPLY FILTERS
    # ---------------------------------------------

    filtered_incidents = incidents.copy()

    if selected_department != "All":

        filtered_incidents = filtered_incidents[
            filtered_incidents["Department"]
            == selected_department
        ]

    if selected_severity != "All":

        filtered_incidents = filtered_incidents[
            filtered_incidents["Severity"]
            == selected_severity
        ]

    if selected_status != "All":

        filtered_incidents = filtered_incidents[
            filtered_incidents["Incident status"]
            == selected_status
        ]

    st.divider()

    # ---------------------------------------------
    # INCIDENT TYPE ANALYSIS
    # ---------------------------------------------

    st.subheader("Incidents by Type")

    if len(filtered_incidents) > 0:

        incident_type_counts = (
            filtered_incidents["Incident type"]
            .value_counts()
        )

        st.bar_chart(
            incident_type_counts
        )

    else:

        st.info(
            "No incidents match the selected filters."
        )

    st.divider()

    # ---------------------------------------------
    # INCIDENT SEVERITY ANALYSIS
    # ---------------------------------------------

    st.subheader("Incidents by Severity")

    if len(filtered_incidents) > 0:

        severity_counts = (
            filtered_incidents["Severity"]
            .value_counts()
        )

        st.bar_chart(
            severity_counts
        )

    else:

        st.info(
            "No severity data available."
        )

    st.divider()

    # ---------------------------------------------
    # INCIDENT STATUS
    # ---------------------------------------------

    st.subheader("Incident Status")

    if len(filtered_incidents) > 0:

        status_counts = (
            filtered_incidents["Incident status"]
            .value_counts()
        )

        st.bar_chart(
            status_counts
        )

    else:

        st.info(
            "No incident-status data available."
        )

    st.divider()

    # ---------------------------------------------
    # INCIDENT RECORDS
    # ---------------------------------------------

    st.subheader("Incident Records")

    st.dataframe(
        filtered_incidents[
            [
                "Incident ID",
                "Date",
                "Time",
                "Shift",
                "Location",
                "Department",
                "Incident type",
                "Severity",
                "Injury status",
                "Lost-time injury status",
                "Cause",
                "Corrective action",
                "Incident status"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
