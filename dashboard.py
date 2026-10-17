
import streamlit as st
import pandas as pd
import base64
import os


# --------------------------------------------------
# BACKGROUND IMAGE
# --------------------------------------------------

def set_background(image_file="mine_background.png"):
    # Check the project folder first, then the data folder.
    if not os.path.exists(image_file):
        data_image = os.path.join("data", image_file)

        if os.path.exists(data_image):
            image_file = data_image
        else:
            # The dashboard can still work without a background image.
            return

    try:
        with open(image_file, "rb") as image:
            encoded_image = base64.b64encode(
                image.read()
            ).decode("utf-8")

        st.markdown(
            f"""
            <style>
            .stApp {{
                background:
                    linear-gradient(
                        rgba(0, 0, 0, 0.65),
                        rgba(0, 0, 0, 0.65)
                    ),
                    url("data:image/png;base64,{encoded_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp p,
            .stApp label {{
                color: white;
            }}

            [data-testid="stMetricLabel"],
            [data-testid="stMetricValue"] {{
                color: white;
            }}

            [data-testid="stVerticalBlock"] {{
                border-radius: 8px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    except OSError:
        # Do not stop the dashboard if the image cannot be opened.
        pass


# --------------------------------------------------
# LOAD CSV DATA
# --------------------------------------------------

def load_csv(filename):
    # Look for the CSV in the project folder.
    if os.path.exists(filename):
        return pd.read_csv(filename)

    # If it is not there, look in the data folder.
    data_path = os.path.join("data", filename)

    if os.path.exists(data_path):
        return pd.read_csv(data_path)

    # Report which file could not be found.
    raise FileNotFoundError(
        f"Could not find '{filename}' in the project folder "
        "or the data folder."
    )


def load_worker_data():
    return load_csv("workers.csv")


def load_incident_data():
    return load_csv("incidents.csv")


def load_equipment_data():
    return load_csv("equipment.csv")


# --------------------------------------------------
# NUMERIC DATA HELPER
# --------------------------------------------------

def numeric_column(data, column_name):
    # Convert a column to numbers safely.
    # Invalid or blank values become NaN instead of causing errors.
    values = data[column_name].astype(str).str.strip()

    # Support percentage values such as "95%".
    values = values.str.replace("%", "", regex=False)

    return pd.to_numeric(values, errors="coerce")


# --------------------------------------------------
# EQUIPMENT AVAILABILITY
# --------------------------------------------------

def calculate_equipment_availability(equipment):
    # Convert operating hours and downtime to numeric values.
    operating_hours = numeric_column(
        equipment, "Operating hours"
    )

    downtime = numeric_column(
        equipment, "Downtime"
    )

    # Availability = Operating time / Total time x 100.
    total_time = operating_hours + downtime

    availability = (
        operating_hours
        .div(total_time.where(total_time > 0))
        * 100
    )

    return availability


# --------------------------------------------------
# DISPLAY TABLES SAFELY
# --------------------------------------------------

def display_available_columns(data, expected_columns):
    # Display the requested columns that actually exist.
    available_columns = [
        column
        for column in expected_columns
        if column in data.columns
    ]

    missing_columns = [
        column
        for column in expected_columns
        if column not in data.columns
    ]

    if missing_columns:
        st.warning(
            "Some columns are missing from this table: "
            + ", ".join(missing_columns)
        )

    if available_columns:
        st.dataframe(
            data[available_columns],
            use_container_width=True
        )
    else:
        st.info("No expected columns are available to display.")


# --------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------

def render_dashboard():

    # Apply the background if the image is available.
    set_background()

    st.title("Khwezi Mining Monitoring Dashboard")

    st.write(
        "Central monitoring dashboard for health, "
        "safety and equipment information."
    )

    st.divider()

    # Load the three datasets.
    try:
        workers = load_worker_data()
        incidents = load_incident_data()
        equipment = load_equipment_data()

    except (FileNotFoundError, pd.errors.ParserError, OSError) as error:
        st.error(f"Could not load dashboard data: {error}")
        st.info(
            "Check that workers.csv, incidents.csv and "
            "equipment.csv are in the project folder or data folder."
        )
        return

    # Check that essential columns exist before calculating KPIs.
    required_columns = {
        "workers.csv": ["Worker ID"],
        "incidents.csv": ["Incident ID"],
        "equipment.csv": [
            "Equipment ID",
            "Operating hours",
            "Downtime"
        ]
    }

    datasets = {
        "workers.csv": workers,
        "incidents.csv": incidents,
        "equipment.csv": equipment
    }

    missing_required = []

    for filename, columns in required_columns.items():
        for column in columns:
            if column not in datasets[filename].columns:
                missing_required.append(
                    f"{filename}: {column}"
                )

    if missing_required:
        st.error(
            "The following required columns are missing:\n\n"
            + "\n".join(
                f"- {column}" for column in missing_required
            )
        )
        return

    # Work on a copy so the original loaded data is unchanged.
    equipment = equipment.copy()

    # --------------------------------------------------
    # WORKER DATA
    # --------------------------------------------------

    total_workers = len(workers)

    if "Near misses" in workers.columns:
        total_near_misses = numeric_column(
            workers, "Near misses"
        ).sum()
    else:
        total_near_misses = None

    if "Safety observations" in workers.columns:
        total_safety_observations = numeric_column(
            workers, "Safety observations"
        ).sum()
    else:
        total_safety_observations = None

    if "PPE compliance" in workers.columns:
        ppe_values = numeric_column(
            workers, "PPE compliance"
        )
        average_ppe_compliance = ppe_values.mean()
    else:
        average_ppe_compliance = float("nan")

    # --------------------------------------------------
    # INCIDENT DATA
    # --------------------------------------------------

    total_incidents = len(incidents)

    if "Severity" in incidents.columns:
        serious_critical_incidents = incidents[
            incidents["Severity"]
            .astype(str)
            .str.strip()
            .str.lower()
            .isin(["serious", "critical"])
        ].shape[0]
    else:
        serious_critical_incidents = None

    # --------------------------------------------------
    # EQUIPMENT DATA
    # --------------------------------------------------

    total_equipment = len(equipment)

    if "Maintenance status" in equipment.columns:
        maintenance_status = (
            equipment["Maintenance status"]
            .astype(str)
            .str.strip()
            .str.lower()
        )

        equipment_available = maintenance_status.isin(
            ["operational", "available"]
        ).sum()

        equipment_under_maintenance = (
            maintenance_status == "under maintenance"
        ).sum()
    else:
        equipment_available = None
        equipment_under_maintenance = None

    # Calculate equipment availability from operating hours
    # and downtime rather than relying on existing CSV values.
    equipment["Availability"] = (
        calculate_equipment_availability(equipment)
    )

    average_equipment_availability = (
        equipment["Availability"].mean()
    )

    # --------------------------------------------------
    # HEALTH AND SAFETY KPI SECTION
    # --------------------------------------------------

    st.subheader("Health & Safety")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Workers", total_workers)

    with col2:
        st.metric("Safety Incidents", total_incidents)

    with col3:
        st.metric(
            "Near Misses",
            "N/A" if total_near_misses is None
            else f"{total_near_misses:g}"
        )

    with col4:
        st.metric(
            "Safety Observations",
            "N/A" if total_safety_observations is None
            else f"{total_safety_observations:g}"
        )

    st.divider()

    # --------------------------------------------------
    # SECOND KPI ROW
    # --------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "PPE Compliance",
            "N/A"
            if pd.isna(average_ppe_compliance)
            else f"{average_ppe_compliance:.1f}%"
        )

    with col2:
        st.metric(
            "Serious/Critical Incidents",
            "N/A"
            if serious_critical_incidents is None
            else serious_critical_incidents
        )

    with col3:
        st.metric("Total Equipment", total_equipment)

    st.divider()

    # --------------------------------------------------
    # EQUIPMENT KPI SECTION
    # --------------------------------------------------

    st.subheader("Equipment Monitoring")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Operational Equipment",
            "N/A"
            if equipment_available is None
            else int(equipment_available)
        )

    with col2:
        st.metric(
            "Under Maintenance",
            "N/A"
            if equipment_under_maintenance is None
            else int(equipment_under_maintenance)
        )

    with col3:
        st.metric(
            "Average Availability",
            "N/A"
            if pd.isna(average_equipment_availability)
            else f"{average_equipment_availability:.1f}%"
        )

    st.divider()

    # --------------------------------------------------
    # EQUIPMENT TABLE
    # --------------------------------------------------

    st.subheader("Equipment Status")

    display_available_columns(
        equipment,
        [
            "Equipment ID",
            "Equipment type",
            "Manufacturer",
            "Temperature",
            "Vibration",
            "Maintenance status",
            "Downtime",
            "Availability"
        ]
    )

    st.divider()

    # --------------------------------------------------
    # WORKER TABLE
    # --------------------------------------------------

    st.subheader("Worker Safety Information")

    display_available_columns(
        workers,
        [
            "Worker ID",
            "Department",
            "Job role",
            "Shift",
            "PPE compliance",
            "Safety training status",
            "Fatigue level",
            "Safety observations",
            "Near misses",
            "Previous incidents"
        ]
    )

    st.divider()

    # --------------------------------------------------
    # INCIDENT TABLE
    # --------------------------------------------------

    st.subheader("Safety Incidents")

    display_available_columns(
        incidents,
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
            "Incident status"
        ]
    )
