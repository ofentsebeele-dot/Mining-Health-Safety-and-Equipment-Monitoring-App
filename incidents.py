```python
import streamlit as st
import pandas as pd


def load_incident_data():

    return pd.read_csv(
        "incidents.csv"
    )


def render_incidents_page():

    incidents = load_incident_data()

    st.title("Safety Incidents")

    st.write(
        "Monitor, filter and review reported safety incidents."
    )

    st.divider()

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    total_incidents = len(incidents)

    serious_incidents = len(
        incidents[
            incidents["Severity"].astype(str)
            == "Serious"
        ]
    )

    critical_incidents = len(
        incidents[
            incidents["Severity"].astype(str)
            == "Critical"
        ]
    )

    lost_time_injuries = len(
        incidents[
            incidents[
                "Lost-time injury status"
            ].astype(str) == "Yes"
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

    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------

    st.subheader("Incident Filters")

    col1, col2, col3 = st.columns(3)

    # Department filter
    with col1:

        department_values = (
            incidents["Department"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        department_values.sort()

        department_options = [
            "All"
        ] + department_values

        selected_department = st.selectbox(
            "Department",
            options=department_options,
            key="incident_department"
        )

    # Severity filter
    with col2:

        severity_values = (
            incidents["Severity"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        severity_values.sort()

        severity_options = [
            "All"
        ] + severity_values

        selected_severity = st.selectbox(
            "Severity",
            options=severity_options,
            key="incident_severity"
        )

    # Status filter
    with col3:

        status_values = (
            incidents["Incident status"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        status_values.sort()

        status_options = [
            "All"
        ] + status_values

        selected_status = st.selectbox(
            "Incident Status",
            options=status_options,
            key="incident_status"
        )

    # --------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------

    filtered_incidents = incidents.copy()

    if selected_department != "All":

        filtered_incidents = filtered_incidents[
            filtered_incidents["Department"]
            .astype(str)
            == selected_department
        ]

    if selected_severity != "All":

        filtered_incidents = filtered_incidents[
            filtered_incidents["Severity"]
            .astype(str)
            == selected_severity
        ]

    if selected_status != "All":

        filtered_incidents = filtered_incidents[
            filtered_incidents["Incident status"]
            .astype(str)
            == selected_status
        ]

    st.divider()

    # --------------------------------------------------
    # FILTERED RESULTS
    # --------------------------------------------------

    st.subheader("Filtered Incidents")

    st.metric(
        "Matching Incidents",
        len(filtered_incidents)
    )

    # --------------------------------------------------
    # INCIDENT TYPE ANALYSIS
    # --------------------------------------------------

    st.subheader("Incidents by Type")

    if not filtered_incidents.empty:

        incident_type_counts = (
            filtered_incidents[
                "Incident type"
            ]
            .astype(str)
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

    # --------------------------------------------------
    # INCIDENT SEVERITY ANALYSIS
    # --------------------------------------------------

    st.subheader("Incidents by Severity")

    if not filtered_incidents.empty:

        severity_counts = (
            filtered_incidents[
                "Severity"
            ]
            .astype(str)
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

    # --------------------------------------------------
    # INCIDENT STATUS
    # --------------------------------------------------

    st.subheader("Incident Status")

    if not filtered_incidents.empty:

        status_counts = (
            filtered_incidents[
                "Incident status"
            ]
            .astype(str)
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

    # --------------------------------------------------
    # INCIDENT RECORDS
    # --------------------------------------------------

    st.subheader("Incident Records")

    display_columns = [
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

    st.dataframe(
        filtered_incidents[display_columns],
        use_container_width=True,
        hide_index=True
    )
```
