import streamlit as st
import pandas as pd
import os


INCIDENT_FILE = "incidents.csv"


def load_incidents():

    if not os.path.exists(INCIDENT_FILE):

        columns = [
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

        return pd.DataFrame(columns=columns)

    return pd.read_csv(INCIDENT_FILE)


def save_incidents(incidents):

    os.makedirs(
        "data",
        exist_ok=True
    )

    incidents.to_csv(
        INCIDENT_FILE,
        index=False
    )


def add_incident(incidents):

    st.subheader("Add Safety Incident")

    with st.form(
        "add_incident_form",
        clear_on_submit=True
    ):

        incident_id = st.text_input(
            "Incident ID"
        )

        date = st.date_input(
            "Date"
        )

        time = st.time_input(
            "Time"
        )

        shift = st.selectbox(
            "Shift",
            [
                "Day",
                "Night"
            ]
        )

        location = st.text_input(
            "Location"
        )

        department = st.selectbox(
            "Department",
            [
                "Mining",
                "Processing",
                "Engineering",
                "Maintenance",
                "Health and Safety",
                "Logistics",
                "Administration"
            ]
        )

        incident_type = st.selectbox(
            "Incident Type",
            [
                "Injury",
                "Near Miss",
                "Equipment Failure",
                "Unsafe Condition",
                "Unsafe Act",
                "Environmental Incident",
                "Fire",
                "Vehicle Incident",
                "Other"
            ]
        )

        severity = st.selectbox(
            "Severity",
            [
                "Minor",
                "Moderate",
                "High",
                "Critical"
            ]
        )

        injury_status = st.selectbox(
            "Injury Status",
            [
                "No",
                "Yes"
            ]
        )

        lost_time = st.selectbox(
            "Lost-time Injury Status",
            [
                "No",
                "Yes"
            ]
        )

        cause = st.text_area(
            "Cause"
        )

        corrective_action = st.text_area(
            "Corrective Action"
        )

        incident_status = st.selectbox(
            "Incident Status",
            [
                "Open",
                "Under Investigation",
                "Corrective Action Required",
                "Closed"
            ]
        )

        submitted = st.form_submit_button(
            "Add Incident"
        )

    if submitted:

        incident_id = incident_id.strip()

        if incident_id == "":

            st.error(
                "Incident ID is required."
            )

            return

        if incident_id in incidents[
            "Incident ID"
        ].astype(str).values:

            st.error(
                "This Incident ID already exists."
            )

            return

        new_incident = {
            "Incident ID": incident_id,
            "Date": date.strftime("%Y-%m-%d"),
            "Time": time.strftime("%H:%M"),
            "Shift": shift,
            "Location": location,
            "Department": department,
            "Incident type": incident_type,
            "Severity": severity,
            "Injury status": injury_status,
            "Lost-time injury status": lost_time,
            "Cause": cause,
            "Corrective action": corrective_action,
            "Incident status": incident_status
        }

        new_row = pd.DataFrame(
            [new_incident]
        )

        incidents = pd.concat(
            [
                incidents,
                new_row
            ],
            ignore_index=True
        )

        save_incidents(
            incidents
        )

        st.success(
            "Incident added successfully."
        )

        st.rerun()


def view_incidents(incidents):

    st.subheader(
        "View Incidents"
    )

    if incidents.empty:

        st.info(
            "No incidents have been recorded."
        )

        return

    st.dataframe(
        incidents,
        use_container_width=True,
        hide_index=True
    )


def search_incidents(incidents):

    st.subheader(
        "Search Incidents"
    )

    search_term = st.text_input(
        "Search incidents"
    )

    if search_term.strip() == "":

        st.info(
            "Enter a search term."
        )

        return

    search_term = search_term.lower()

    mask = (
        incidents.astype(str)
        .apply(
            lambda column:
            column.str.lower().str.contains(
                search_term,
                na=False
            )
        )
        .any(axis=1)
    )

    results = incidents[
        mask
    ]

    st.write(
        f"Search results: {len(results)}"
    )

    if results.empty:

        st.warning(
            "No matching incidents found."
        )

    else:

        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )


def filter_incidents(incidents):

    st.subheader(
        "Filter Incidents"
    )

    if incidents.empty:

        st.info(
            "No incidents available for filtering."
        )

        return

    col1, col2 = st.columns(2)

    with col1:

        departments = sorted(
            incidents[
                "Department"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_departments = st.multiselect(
            "Department",
            departments
        )

    with col2:

        shifts = sorted(
            incidents[
                "Shift"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_shifts = st.multiselect(
            "Shift",
            shifts
        )

    col3, col4 = st.columns(2)

    with col3:

        severities = sorted(
            incidents[
                "Severity"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_severities = st.multiselect(
            "Severity",
            severities
        )

    with col4:

        incident_types = sorted(
            incidents[
                "Incident type"
            ]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_types = st.multiselect(
            "Incident Type",
            incident_types
        )

    statuses = sorted(
        incidents[
            "Incident status"
        ]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    selected_statuses = st.multiselect(
        "Incident Status",
        statuses
    )

    filtered = incidents.copy()

    if selected_departments:

        filtered = filtered[
            filtered["Department"].isin(
                selected_departments
            )
        ]

    if selected_shifts:

        filtered = filtered[
            filtered["Shift"].isin(
                selected_shifts
            )
        ]

    if selected_severities:

        filtered = filtered[
            filtered["Severity"].isin(
                selected_severities
            )
        ]

    if selected_types:

        filtered = filtered[
            filtered["Incident type"].isin(
                selected_types
            )
        ]

    if selected_statuses:

        filtered = filtered[
            filtered["Incident status"].isin(
                selected_statuses
            )
        ]

    st.write(
        f"Filtered incidents: {len(filtered)}"
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )


def categorize_incidents(incidents):

    st.subheader(
        "Incident Categories"
    )

    if incidents.empty:

        st.info(
            "No incident data available."
        )

        return

    category_counts = (
        incidents[
            "Incident type"
        ]
        .value_counts()
    )

    st.bar_chart(
        category_counts
    )

    category_table = (
        category_counts
        .rename("Incident Count")
        .reset_index()
    )

    category_table.columns = [
        "Incident Category",
        "Incident Count"
    ]

    st.dataframe(
        category_table,
        use_container_width=True,
        hide_index=True
    )


def count_incidents(incidents):

    st.subheader(
        "Incident Counts"
    )

    total = len(
        incidents
    )

    near_misses = len(
        incidents[
            incidents[
                "Incident type"
            ]
            .astype(str)
            .str.lower()
            == "near miss"
        ]
    )

    injuries = len(
        incidents[
            incidents[
                "Injury status"
            ]
            .astype(str)
            .str.lower()
            == "yes"
        ]
    )

    lost_time = len(
        incidents[
            incidents[
                "Lost-time injury status"
            ]
            .astype(str)
            .str.lower()
            == "yes"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Incidents",
            total
        )

    with col2:

        st.metric(
            "Near Misses",
            near_misses
        )

    with col3:

        st.metric(
            "Injuries",
            injuries
        )

    with col4:

        st.metric(
            "Lost-time Injuries",
            lost_time
        )


def analyse_incident_trends(incidents):

    st.subheader(
        "Incident Trend Analysis"
    )

    if incidents.empty:

        st.info(
            "No incident data available."
        )

        return

    trend_data = incidents.copy()

    trend_data["Date"] = pd.to_datetime(
        trend_data["Date"],
        errors="coerce"
    )

    trend_data = trend_data.dropna(
        subset=["Date"]
    )

    if trend_data.empty:

        st.warning(
            "Valid incident dates are required."
        )

        return

    trend_data["Month"] = (
        trend_data["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    monthly_incidents = (
        trend_data[
            "Month"
        ]
        .value_counts()
        .sort_index()
    )

    st.write(
        "Incidents by Month"
    )

    st.line_chart(
        monthly_incidents
    )

    st.write(
        "Incidents by Shift"
    )

    shift_counts = (
        incidents[
            "Shift"
        ]
        .value_counts()
    )

    st.bar_chart(
        shift_counts
    )

    st.write(
        "Incidents by Department"
    )

    department_counts = (
        incidents[
            "Department"
        ]
        .value_counts()
    )

    st.bar_chart(
        department_counts
    )

    st.write(
        "Incidents by Severity"
    )

    severity_counts = (
        incidents[
            "Severity"
        ]
        .value_counts()
    )

    st.bar_chart(
        severity_counts
    )

    st.write(
        "Incidents by Type"
    )

    type_counts = (
        incidents[
            "Incident type"
        ]
        .value_counts()
    )

    st.bar_chart(
        type_counts
    )


def render_incidents_page():

    incidents = load_incidents()

    st.title(
        "Safety Incidents"
    )

    st.write(
        "Record, view, search, filter, categorize "
        "and analyse safety incidents."
    )

    st.divider()

    tabs = st.tabs(
        [
            "Add Incident",
            "View Incidents",
            "Search",
            "Filter",
            "Categories",
            "Counts",
            "Trend Analysis"
        ]
    )

    with tabs[0]:

        add_incident(
            incidents
        )

    with tabs[1]:

        view_incidents(
            incidents
        )

    with tabs[2]:

        search_incidents(
            incidents
        )

    with tabs[3]:

        filter_incidents(
            incidents
        )

    with tabs[4]:

        categorize_incidents(
            incidents
        )

    with tabs[5]:

        count_incidents(
            incidents
        )

    with tabs[6]:

        analyse_incident_trends(
            incidents
        )
