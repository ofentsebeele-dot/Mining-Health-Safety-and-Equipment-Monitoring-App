import streamlit as st
import pandas as pd
import base64
import os
from datetime import datetime

# Plotly provides interactive charts.
# The dashboard can still work without Plotly installed.
try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


# --------------------------------------------------
# PAGE SETTINGS
# --------------------------------------------------

# Use a wide layout to make room for charts and metrics.
# If app.py already calls st.set_page_config(), keep the
# page configuration there and remove this call.
st.set_page_config(
    page_title="Khwezi Mining Monitoring Dashboard",
    page_icon="⛏️",
    layout="wide"
)


# --------------------------------------------------
# BACKGROUND IMAGE
# --------------------------------------------------

def set_background(image_file="mine_background.png"):
    """Set the background image if the image file exists."""

    # Check the project folder first.
    if not os.path.exists(image_file):

        # If it is not there, check the data folder.
        data_image = os.path.join("data", image_file)

        if os.path.exists(data_image):
            image_file = data_image
        else:
            # The dashboard can still work without a background.
            return

    try:
        # Read and encode the image for the page background.
        with open(image_file, "rb") as image:
            encoded_image = base64.b64encode(
                image.read()
            ).decode("utf-8")

        # Apply the background and style the metric cards.
        st.markdown(
            f"""
            <style>
            .stApp {{
                background:
                    linear-gradient(
                        rgba(8, 20, 31, 0.82),
                        rgba(8, 20, 31, 0.82)
                    ),
                    url("data:image/png;base64,{encoded_image}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            [data-testid="stMetric"] {{
                background: rgba(255, 255, 255, 0.08);
                border: 1px solid rgba(255, 255, 255, 0.16);
                padding: 12px 14px;
                border-radius: 12px;
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

def find_csv_path(filename):
    """Find a CSV file in the project folder or data folder."""

    possible_paths = [
        filename,
        os.path.join("data", filename)
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return None


def load_csv(filename):
    """Load the latest CSV contents without caching old data."""

    path = find_csv_path(filename)

    if path is None:
        raise FileNotFoundError(
            f"Could not find '{filename}' in the project folder "
            "or data folder."
        )

    return pd.read_csv(path)


def load_worker_data():
    """Load worker safety data."""
    return load_csv("workers.csv")


def load_incident_data():
    """Load incident data."""
    return load_csv("incidents.csv")


def load_equipment_data():
    """Load equipment monitoring data."""
    return load_csv("equipment.csv")


# --------------------------------------------------
# DATA HELPER FUNCTIONS
# --------------------------------------------------

def numeric_column(data, column_name):
    """Convert a column into numbers safely."""

    # Return an empty numeric series if the column is missing.
    if column_name not in data.columns:
        return pd.Series(index=data.index, dtype="float64")

    # Convert the values to text and remove surrounding spaces.
    values = data[column_name].astype(str).str.strip()

    # Allow values such as 95%.
    values = values.str.replace("%", "", regex=False)

    # Invalid or blank values become NaN.
    return pd.to_numeric(values, errors="coerce")


def clean_category(data, column_name, fallback="Unknown"):
    """Clean text categories for use in charts."""

    # If the column is missing, return an Unknown category.
    if column_name not in data.columns:
        return pd.Series(
            [fallback] * len(data),
            index=data.index
        )

    values = data[column_name].fillna(fallback).astype(str).str.strip()

    # Replace blank categories with Unknown.
    return values.replace("", fallback)


def display_available_columns(data, expected_columns):
    """Display columns that exist without crashing on missing columns."""

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
        st.caption(
            "Not found in this CSV: "
            + ", ".join(missing_columns)
        )

    if available_columns:
        st.dataframe(
            data[available_columns],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No expected columns are available to display.")


# --------------------------------------------------
# EQUIPMENT AVAILABILITY
# --------------------------------------------------

def calculate_equipment_availability(equipment):
    """
    Calculate availability.

    Availability = Operating hours /
                   (Operating hours + Downtime) * 100
    """

    operating_hours = numeric_column(
        equipment,
        "Operating hours"
    )

    downtime = numeric_column(
        equipment,
        "Downtime"
    )

    total_time = operating_hours + downtime

    # Avoid division by zero.
    availability = (
        operating_hours.div(
            total_time.where(total_time > 0)
        ) * 100
    )

    return availability


# --------------------------------------------------
# PIE CHARTS
# --------------------------------------------------

def show_pie_chart(data, column_name, title):
    """Display a pie chart showing category proportions."""

    if data.empty or column_name not in data.columns:
        st.info(f"No data available for {title.lower()}.")
        return

    # Count the number of records in each category.
    chart_data = (
        clean_category(data, column_name)
        .value_counts()
        .rename_axis(column_name)
        .reset_index(name="Count")
    )

    if PLOTLY_AVAILABLE:

        # Create an interactive pie chart.
        fig = px.pie(
            chart_data,
            names=column_name,
            values="Count",
            hole=0.42,
            title=title
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label"
        )

        fig.update_layout(
            margin=dict(t=55, b=10, l=10, r=10),
            legend_title_text=""
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        # Use a basic bar chart if Plotly is unavailable.
        st.bar_chart(
            chart_data.set_index(column_name)
        )


# --------------------------------------------------
# BAR CHARTS
# --------------------------------------------------

def show_bar_chart(
    data,
    category_column,
    title,
    y_title="Number of records"
):
    """Display a bar chart counting records in each category."""

    if data.empty or category_column not in data.columns:
        st.info(f"No data available for {title.lower()}.")
        return

    # Count the records in each category.
    chart_data = (
        clean_category(data, category_column)
        .value_counts()
        .rename_axis(category_column)
        .reset_index(name="Count")
    )

    if PLOTLY_AVAILABLE:

        fig = px.bar(
            chart_data,
            x=category_column,
            y="Count",
            title=title,
            text="Count"
        )

        fig.update_layout(
            xaxis_title=category_column,
            yaxis_title=y_title,
            margin=dict(t=55, b=10, l=10, r=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        st.bar_chart(
            chart_data.set_index(category_column)
        )


# --------------------------------------------------
# HISTOGRAMS
# --------------------------------------------------

def show_histogram(
    data,
    column_name,
    title,
    x_title=None
):
    """Display a histogram for a numeric column."""

    if column_name not in data.columns:
        st.info(f"{column_name} is not available in this CSV.")
        return

    # Keep only valid numeric values.
    values = numeric_column(
        data,
        column_name
    ).dropna()

    if values.empty:
        st.info(
            f"No numeric values are available for {column_name}."
        )
        return

    if PLOTLY_AVAILABLE:

        # A histogram groups values into bins.
        fig = px.histogram(
            x=values,
            nbins=20,
            title=title,
            labels={
                "x": x_title or column_name,
                "y": "Number of records"
            }
        )

        fig.update_layout(
            margin=dict(t=55, b=10, l=10, r=10)
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    else:
        # Basic fallback if Plotly is not installed.
        st.bar_chart(
            values.value_counts().sort_index()
        )


# --------------------------------------------------
# MAIN DASHBOARD
# --------------------------------------------------

def render_dashboard_content():
    """Load data and display all dashboard sections."""

    # Apply the background if an image is available.
    set_background()

    st.title("⛏️ Khwezi Mining Monitoring Dashboard")

    st.write(
        "A central overview of worker safety, incidents, "
        "equipment condition and maintenance performance."
    )

    # --------------------------------------------------
    # REFRESH BUTTON
    # --------------------------------------------------

    refresh_col, info_col = st.columns([1, 4])

    with refresh_col:
        if st.button(
            "🔄 Refresh Dashboard",
            use_container_width=True
        ):
            # Rerun the dashboard and read the CSV files again.
            st.rerun()

    with info_col:
        st.caption(
            "The dashboard reads the latest CSV contents whenever "
            "it reruns. Automatic refresh is enabled where supported."
        )

    # --------------------------------------------------
    # LOAD THE DATA
    # --------------------------------------------------

    try:
        workers = load_worker_data()
        incidents = load_incident_data()
        equipment = load_equipment_data()

    except (
        FileNotFoundError,
        pd.errors.ParserError,
        OSError,
        UnicodeDecodeError
    ) as error:

        st.error(f"Could not load dashboard data: {error}")

        st.info(
            "Check that workers.csv, incidents.csv and equipment.csv "
            "are in your project folder or data folder."
        )

        return

    # --------------------------------------------------
    # CHECK REQUIRED COLUMNS
    # --------------------------------------------------

    required_columns = {
        "workers.csv": {
            "Worker ID": workers
        },
        "incidents.csv": {
            "Incident ID": incidents
        },
        "equipment.csv": {
            "Equipment ID": equipment
        }
    }

    missing_columns = []

    for filename, columns in required_columns.items():

        for column_name, data in columns.items():

            if column_name not in data.columns:
                missing_columns.append(
                    f"{filename}: {column_name}"
                )

    if missing_columns:

        st.error(
            "The following required columns are missing: "
            + "; ".join(missing_columns)
        )

        return

    # Make a copy so the source data is not changed.
    equipment = equipment.copy()

    # Calculate availability for dashboard display.
    equipment["Calculated Availability (%)"] = (
        calculate_equipment_availability(equipment)
    )

    # --------------------------------------------------
    # CALCULATE WORKER METRICS
    # --------------------------------------------------

    total_workers = len(workers)

    if "Near misses" in workers.columns:
        total_near_misses = numeric_column(
            workers,
            "Near misses"
        ).sum()
    else:
        total_near_misses = None

    if "Safety observations" in workers.columns:
        total_safety_observations = numeric_column(
            workers,
            "Safety observations"
        ).sum()
    else:
        total_safety_observations = None

    if "PPE compliance" in workers.columns:
        average_ppe_compliance = numeric_column(
            workers,
            "PPE compliance"
        ).mean()
    else:
        average_ppe_compliance = float("nan")

    # --------------------------------------------------
    # CALCULATE INCIDENT METRICS
    # --------------------------------------------------

    total_incidents = len(incidents)

    if "Severity" in incidents.columns:

        incident_severity = clean_category(
            incidents,
            "Severity"
        ).str.lower()

        serious_critical_incidents = incident_severity.isin(
            ["serious", "critical"]
        ).sum()

    else:
        serious_critical_incidents = None

    # --------------------------------------------------
    # CALCULATE EQUIPMENT METRICS
    # --------------------------------------------------

    total_equipment = len(equipment)

    if "Maintenance status" in equipment.columns:

        maintenance_status = clean_category(
            equipment,
            "Maintenance status"
        ).str.lower()

        operational_equipment = maintenance_status.isin(
            ["operational", "available"]
        ).sum()

        equipment_under_maintenance = (
            maintenance_status == "under maintenance"
        ).sum()

    else:
        operational_equipment = None
        equipment_under_maintenance = None

    average_equipment_availability = (
        equipment["Calculated Availability (%)"].mean()
    )

    # Calculate the number of equipment records that exceed
    # the critical temperature or vibration thresholds.
    critical_temperature = (
        numeric_column(equipment, "Temperature") > 100
        if "Temperature" in equipment.columns
        else pd.Series(False, index=equipment.index)
    )

    critical_vibration = (
        numeric_column(equipment, "Vibration") > 8
        if "Vibration" in equipment.columns
        else pd.Series(False, index=equipment.index)
    )

    critical_equipment_alerts = (
        critical_temperature.fillna(False)
        | critical_vibration.fillna(False)
    ).sum()

    # --------------------------------------------------
    # KEY PERFORMANCE INDICATORS
    # --------------------------------------------------

    st.subheader("📊 Key Performance Indicators")

    # First row of metrics.
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Workers",
            f"{total_workers:,}"
        )

    with col2:
        st.metric(
            "Safety Incidents",
            f"{total_incidents:,}"
        )

    with col3:
        st.metric(
            "Near Misses",
            "N/A"
            if total_near_misses is None
            else f"{total_near_misses:,.0f}"
        )

    with col4:
        st.metric(
            "Safety Observations",
            "N/A"
            if total_safety_observations is None
            else f"{total_safety_observations:,.0f}"
        )

    # Second row of metrics.
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Average PPE Compliance",
            "N/A"
            if pd.isna(average_ppe_compliance)
            else f"{average_ppe_compliance:.1f}%"
        )

    with col2:
        st.metric(
            "Serious/Critical Incidents",
            "N/A"
            if serious_critical_incidents is None
            else f"{int(serious_critical_incidents):,}"
        )

    with col3:
        st.metric(
            "Operational Equipment",
            "N/A"
            if operational_equipment is None
            else f"{int(operational_equipment):,}"
        )

    with col4:
        st.metric(
            "Under Maintenance",
            "N/A"
            if equipment_under_maintenance is None
            else f"{int(equipment_under_maintenance):,}"
        )

    # Third row of metrics.
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Equipment",
            f"{total_equipment:,}"
        )

    with col2:
        st.metric(
            "Average Equipment Availability",
            "N/A"
            if pd.isna(average_equipment_availability)
            else f"{average_equipment_availability:.1f}%"
        )

    with col3:
        st.metric(
            "Critical Equipment Alerts",
            f"{int(critical_equipment_alerts):,}"
        )

    st.divider()

    # --------------------------------------------------
    # HEALTH AND SAFETY ANALYTICS
    # --------------------------------------------------

    st.subheader("🦺 Health and Safety Analytics")

    # Pie charts.
    left, right = st.columns(2)

    with left:
        show_pie_chart(
            incidents,
            "Severity",
            "Incidents by Severity"
        )

    with right:
        show_pie_chart(
            workers,
            "Fatigue level",
            "Worker Fatigue Distribution"
        )

    # Bar charts.
    left, right = st.columns(2)

    with left:
        show_bar_chart(
            incidents,
            "Department",
            "Incidents by Department"
        )

    with right:
        show_bar_chart(
            incidents,
            "Shift",
            "Incidents by Shift"
        )

    # Histograms and incident categories.
    left, right = st.columns(2)

    with left:
        show_histogram(
            workers,
            "PPE compliance",
            "PPE Compliance Distribution",
            "PPE Compliance (%)"
        )

    with right:
        show_bar_chart(
            incidents,
            "Incident type",
            "Most Common Incident Types"
        )

    # --------------------------------------------------
    # INCIDENT TREND OVER TIME
    # --------------------------------------------------

    if "Date" in incidents.columns:

        incident_dates = incidents.copy()

        # Convert the date column into real dates.
        incident_dates["Parsed Date"] = pd.to_datetime(
            incident_dates["Date"],
            errors="coerce"
        )

        # Ignore rows with invalid dates.
        incident_dates = incident_dates.dropna(
            subset=["Parsed Date"]
        )

        if not incident_dates.empty:

            # Group incidents by calendar date.
            incident_dates["Date Only"] = (
                incident_dates["Parsed Date"].dt.date
            )

            trend_data = (
                incident_dates
                .groupby("Date Only")
                .size()
                .reset_index(name="Incidents")
            )

            st.subheader("📈 Incident Trend Over Time")

            st.line_chart(
                trend_data.set_index("Date Only")["Incidents"],
                use_container_width=True
            )

    st.divider()

    # --------------------------------------------------
    # EQUIPMENT ANALYTICS
    # --------------------------------------------------

    st.subheader("🚜 Equipment Condition and Maintenance")

    # Maintenance status and equipment type.
    left, right = st.columns(2)

    with left:
        show_pie_chart(
            equipment,
            "Maintenance status",
            "Equipment Maintenance Status"
        )

    with right:
        show_bar_chart(
            equipment,
            "Equipment type",
            "Equipment Count by Type"
        )

    # Temperature and vibration histograms.
    left, right = st.columns(2)

    with left:
        show_histogram(
            equipment,
            "Temperature",
            "Equipment Temperature Distribution",
            "Temperature (°C)"
        )

    with right:
        show_histogram(
            equipment,
            "Vibration",
            "Equipment Vibration Distribution",
            "Vibration (mm/s)"
        )

    # Downtime and availability histograms.
    left, right = st.columns(2)

    with left:
        show_histogram(
            equipment,
            "Downtime",
            "Equipment Downtime Distribution",
            "Downtime (hours)"
        )

    with right:
        show_histogram(
            equipment,
            "Calculated Availability (%)",
            "Equipment Availability Distribution",
            "Availability (%)"
        )

    # --------------------------------------------------
    # EQUIPMENT ALERTS
    # --------------------------------------------------

    st.subheader("⚠️ Equipment Requiring Attention")

    # Start with no equipment alerts.
    alerts = pd.Series(
        False,
        index=equipment.index
    )

    alert_reasons = pd.Series(
        "",
        index=equipment.index,
        dtype="object"
    )

    # Identify temperatures above the critical threshold.
    if "Temperature" in equipment.columns:

        temperature = numeric_column(
            equipment,
            "Temperature"
        )

        hot_equipment = (
            temperature > 100
        ).fillna(False)

        alerts = alerts | hot_equipment

        alert_reasons.loc[hot_equipment] += (
            "Temperature above 100°C; "
        )

    # Identify vibration above the critical threshold.
    if "Vibration" in equipment.columns:

        vibration = numeric_column(
            equipment,
            "Vibration"
        )

        high_vibration = (
            vibration > 8
        ).fillna(False)

        alerts = alerts | high_vibration

        alert_reasons.loc[high_vibration] += (
            "Vibration above 8 mm/s; "
        )

    if alerts.any():

        # Display only equipment that triggered an alert.
        alert_table = equipment.loc[alerts].copy()

        alert_table["Alert reason"] = (
            alert_reasons.loc[alerts]
        )

        alert_columns = [
            column
            for column in [
                "Equipment ID",
                "Equipment type",
                "Temperature",
                "Vibration",
                "Maintenance status",
                "Downtime",
                "Calculated Availability (%)",
                "Alert reason"
            ]
            if column in alert_table.columns
        ]

        st.dataframe(
            alert_table[alert_columns],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success(
            "No equipment exceeds the critical temperature "
            "or vibration thresholds in the available data."
        )

    st.divider()

    # --------------------------------------------------
    # DATA TABLES
    # --------------------------------------------------

    # Expandable tables keep the dashboard tidy.
    with st.expander("👷 View Worker Safety Records"):

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

    with st.expander("📝 View Incident Records"):

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
                "Cause",
                "Corrective action",
                "Incident status"
            ]
        )

    with st.expander("🔧 View Equipment Records"):

        display_available_columns(
            equipment,
            [
                "Equipment ID",
                "Equipment type",
                "Manufacturer",
                "Operating hours",
                "Temperature",
                "Vibration",
                "Fuel consumption",
                "Brake status",
                "Tyre status",
                "Engine status",
                "Maintenance status",
                "Downtime",
                "Calculated Availability (%)"
            ]
        )

    # --------------------------------------------------
    # LAST REFRESH TIME
    # --------------------------------------------------

    st.caption(
        "Last refreshed: "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    # Explain the chart fallback if Plotly is unavailable.
    if not PLOTLY_AVAILABLE:

        st.info(
            "For interactive pie charts and histograms, add "
            "'plotly' to requirements.txt. Basic charts will "
            "still be displayed without it."
        )


# --------------------------------------------------
# AUTOMATIC REFRESH
# --------------------------------------------------

# Newer Streamlit versions support fragments that rerun periodically.
# The manual refresh button remains available as a fallback.

if hasattr(st, "fragment"):

    @st.fragment(run_every=30)
    def render_dashboard():
        render_dashboard_content()

else:

    def render_dashboard():
        render_dashboard_content()
