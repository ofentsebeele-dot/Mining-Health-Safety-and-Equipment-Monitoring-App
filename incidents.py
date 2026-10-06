import streamlit as st
import pandas as pd
import os


# ==================================================
# INCIDENT CSV FILE
# ==================================================

INCIDENT_FILE = "incidents.csv"


# ==================================================
# LOAD INCIDENT DATA
# ==================================================

def load_incidents():

    # Check if the incidents CSV file exists
    if not os.path.exists(INCIDENT_FILE):

        # Create the required columns if the file does not exist
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

        # Return an empty table with the correct columns
        return pd.DataFrame(columns=columns)

    # Read the existing incidents CSV file
    return pd.read_csv(INCIDENT_FILE)


# ==================================================
# SAVE INCIDENT DATA
# ==================================================

def save_incidents(incidents):

    # Make sure the data folder exists
    os.makedirs(
        "data",
        exist_ok=True
    )

    # Save the updated incidents to the CSV file
    incidents.to_csv(
        INCIDENT_FILE,
        index=False
    )


# ==================================================
# ADD INCIDENT
# ==================================================

def add_incident(incidents):

    # Display the section heading
    st.subheader("Add Safety Incident")

    # Create the incident entry form
    with st.form(
        "add_incident_form",
        clear_on_submit=True
    ):

        # Incident identification
        incident_id = st.text_input(
            "Incident ID"
        )

        # Incident date
        date = st.date_input(
            "Date"
        )

        # Incident time
        time = st.time_input(
            "Time"
        )

        # Select the work shift
        shift = st.selectbox(
            "Shift",
            [
                "Day",
                "Night"
            ]
        )

        # Enter the incident location
        location = st.text_input(
            "Location"
        )

        # Select the department
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

        # Categorise the incident type
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

        # Select the incident severity
        severity = st.selectbox(
            "Severity",
            [
                "Minor",
                "Moderate",
                "High",
                "Critical"
            ]
        )

        # Record whether an injury occurred
        injury_status = st.selectbox(
            "Injury Status",
            [
                "No",
                "Yes"
            ]
        )

        # Record whether the injury resulted in lost time
        lost_time = st.selectbox(
            "Lost-time Injury Status",
            [
                "No",
                "Yes"
            ]
        )

        # Record the cause of the incident
        cause = st.text_area(
            "Cause"
        )

        # Record the corrective action
        corrective_action = st.text_area(
            "Corrective Action"
        )

        # Record the current incident status
        incident_status = st.selectbox(
            "Incident Status",
            [
                "Open",
                "Under Investigation",
                "Corrective Action Required",
                "Closed"
            ]
        )

        # Submit button
        submitted = st.form_submit_button(
            "Add Incident"
        )

    # Process the form after submission
    if submitted:

        # Remove unnecessary spaces from the Incident ID
        incident_id = incident_id.strip()

        # Make sure an Incident ID was entered
        if incident_id == "":

            st.error(
                "Incident ID is required."
            )

            return

        # Prevent duplicate Incident IDs
        if incident_id in incidents[
            "Incident ID"
        ].astype(str).values:

            st.error(
                "This Incident ID already exists."
            )

            return

        # Create a new incident record
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

        # Convert the new incident into a DataFrame
        new_row = pd.DataFrame(
            [new_incident]
        )

        # Add the new incident to the existing data
        incidents = pd.concat(
            [
                incidents,
                new_row
            ],
            ignore_index=True
        )

        # Save the updated data to the CSV file
        save_incidents(
            incidents
        )

        # Tell the user that the incident was successfully added
        st.success(
            "Incident added successfully."
        )

        # Refresh the application
        st.rerun()


# ==================================================
# VIEW INCIDENTS
# ==================================================

def view_incidents(incidents):

    # Display the section heading
    st.subheader(
        "View Incidents"
    )

    # Check whether there are any incidents
    if incidents.empty:

        st.info(
            "No incidents have been recorded."
        )

        return

    # Display all incidents in a table
    st.dataframe(
        incidents,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# SEARCH INCIDENTS
# ==================================================

def search_incidents(incidents):

    # Display the section heading
    st.subheader(
        "Search Incidents"
    )

    # Create a search box
    search_term = st.text_input(
        "Search incidents"
    )

    # Do not search if the search box is empty
    if search_term.strip() == "":

        st.info(
            "Enter a search term."
        )

        return

    # Convert the search text to lowercase
    search_term = search_term.lower()

    # Search across all columns
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

    # Return matching incidents
    results = incidents[
        mask
    ]

    # Display the number of results
    st.write(
        f"Search results: {len(results)}"
    )

    # Display a message when no results are found
    if results.empty:

        st.warning(
            "No matching incidents found."
        )

    else:

        # Display matching incidents
        st.dataframe(
            results,
            use_container_width=True,
            hide_index=True
        )


# ==================================================
# FILTER INCIDENTS
# ==================================================

def filter_incidents(incidents):

    # Display the section heading
    st.subheader(
        "Filter Incidents"
    )

    # Check whether incident data exists
    if incidents.empty:

        st.info(
            "No incidents available for filtering."
        )

        return

    # Create two columns for filters
    col1, col2 = st.columns(2)

    # Department filter
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

    # Shift filter
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

    # Create another two columns
    col3, col4 = st.columns(2)

    # Severity filter
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

    # Incident type filter
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

    # Incident status filter
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

    # Start with all incidents
    filtered = incidents.copy()

    # Apply department filter
    if selected_departments:

        filtered = filtered[
            filtered["Department"].isin(
                selected_departments
            )
        ]

    # Apply shift filter
    if selected_shifts:

        filtered = filtered[
            filtered["Shift"].isin(
                selected_shifts
            )
        ]

    # Apply severity filter
    if selected_severities:

        filtered = filtered[
            filtered["Severity"].isin(
                selected_severities
            )
        ]

    # Apply incident type filter
    if selected_types:

        filtered = filtered[
            filtered["Incident type"].isin(
                selected_types
            )
        ]

    # Apply status filter
    if selected_statuses:

        filtered = filtered[
            filtered["Incident status"].isin(
                selected_statuses
            )
        ]

    # Display the number of filtered incidents
    st.write(
        f"Filtered incidents: {len(filtered)}"
    )

    # Display the filtered results
    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# CATEGORIZE INCIDENTS
# ==================================================

def categorize_incidents(incidents):

    # Display the section heading
    st.subheader(
        "Incident Categories"
    )

    # Check whether incident data exists
    if incidents.empty:

        st.info(
            "No incident data available."
        )

        return

    # Count incidents by incident type
    category_counts = (
        incidents[
            "Incident type"
        ]
        .value_counts()
    )

    # Display a chart of incident categories
    st.bar_chart(
        category_counts
    )

    # Convert the category counts into a table
    category_table = (
        category_counts
        .rename("Incident Count")
        .reset_index()
    )

    # Rename the table columns
    category_table.columns = [
        "Incident Category",
        "Incident Count"
    ]

    # Display the category table
    st.dataframe(
        category_table,
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# COUNT INCIDENTS
# ==================================================

def count_incidents(incidents):

    # Display the section heading
    st.subheader(
        "Incident Counts"
    )

    # Count all incidents
    total = len(
        incidents
    )

    # Count near misses
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

    # Count incidents involving injuries
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

    # Count lost-time injuries
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

    # Create four metric columns
    col1, col2, col3, col4 = st.columns(4)

    # Display total incidents
    with col1:

        st.metric(
            "Total Incidents",
            total
        )

    # Display near misses
    with col2:

        st.metric(
            "Near Misses",
            near_misses
        )

    # Display injuries
    with col3:

        st.metric(
            "Injuries",
            injuries
        )

    # Display lost-time injuries
    with col4:

        st.metric(
            "Lost-time Injuries",
            lost_time
        )


# ==================================================
# INCIDENT TREND ANALYSIS
# ==================================================

def analyse_incident_trends(incidents):

    # Display the section heading
    st.subheader(
        "Incident Trend Analysis"
    )

    # Check whether incident data exists
    if incidents.empty:

        st.info(
            "No incident data available."
        )

        return

    # Make a copy so the original data is not changed
    trend_data = incidents.copy()

    # Convert the Date column to a proper date
    trend_data["Date"] = pd.to_datetime(
        trend_data["Date"],
        errors="coerce"
    )

    # Remove records with invalid dates
    trend_data = trend_data.dropna(
        subset=["Date"]
    )

    # Stop if no valid dates exist
    if trend_data.empty:

        st.warning(
            "Valid incident dates are required."
        )

        return

    # Create a Month column
    trend_data["Month"] = (
        trend_data["Date"]
        .dt.to_period("M")
        .astype(str)
    )

    # Count incidents for each month
    monthly_incidents = (
        trend_data[
            "Month"
        ]
        .value_counts()
        .sort_index()
    )

    # Display monthly trend
    st.write(
        "Incidents by Month"
    )

    st.line_chart(
        monthly_incidents
    )

    # Count incidents by shift
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

    # Count incidents by department
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

    # Count incidents by severity
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

    # Count incidents by incident type
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


# ==================================================
# MAIN INCIDENT PAGE
# ==================================================

def render_incidents_page():

    # Load the incidents from the CSV file
    incidents = load_incidents()

    # Display the page title
    st.title(
        "Safety Incidents"
    )

    # Explain what users can do
    st.write(
        "Record, view, search, filter, categorize "
        "and analyse safety incidents."
    )

    # Add a separator
    st.divider()

    # Create tabs for each required function
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

    # Add incidents
    with tabs[0]:

        add_incident(
            incidents
        )

    # View incidents
    with tabs[1]:

        view_incidents(
            incidents
        )

    # Search incidents
    with tabs[2]:

        search_incidents(
            incidents
        )

    # Filter incidents
    with tabs[3]:

        filter_incidents(
            incidents
        )

    # Categorize incidents
    with tabs[4]:

        categorize_incidents(
            incidents
        )

    # Count incidents
    with tabs[5]:

        count_incidents(
            incidents
        )

    # Analyse incident trends
    with tabs[6]:

        analyse_incident_trends(
            incidents
        )
