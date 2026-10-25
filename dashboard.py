# Dashboard

import os
import base64
from datetime import datetime

import pandas as pd
import streamlit as st

try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


# 1. Load CSV files

def find_csv_path(filename): possible_paths = [ filename, os.path.join("data", filename) ]

    for path in possible_paths:
        if os.path.isfile(path):
            return path

    return None


def load_csv(filename):
    path = find_csv_path(filename)

    if path is None:
        raise FileNotFoundError(
            f"Cannot find {filename}. "
            "Place it in the project folder or the data folder."
        )

    return pd.read_csv(path)


def load_worker_data():
    return load_csv("workers.csv")


def load_incident_data():
    return load_csv("incidents.csv")


def load_equipment_data():
    return load_csv("equipment.csv")


# 2. Helper Functions

def numeric_column(data, column_name):
    if column_name not in data.columns:
        return pd.Series(float("nan"), index=data.index)

    values = data[column_name].astype(str).str.strip()
    values = values.str.replace("%", "", regex=False)

    return pd.to_numeric(values, errors="coerce")


def category_column(data, column_name):
    if column_name not in data.columns:
        return pd.Series("Unknown", index=data.index)

    values = (
        data[column_name]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    return values.replace("", "Unknown")


def show_table(data, columns):
    available = [
        column for column in columns
        if column in data.columns
    ]

    if available:
        st.dataframe(
            data[available],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info(
            "The expected columns are not available in this CSV."
        )


# ============================================================
# 3. BACKGROUND IMAGE AND TEXT STYLING
# ============================================================

def set_background(image_file="mine_background.png"):
    path = find_csv_path(image_file)

    if path is None:
        return

    try:
        with open(path, "rb") as image:
            encoded_image = base64.b64encode(
                image.read()
            ).decode("utf-8")

        st.markdown(
            f"""
            <style>

            /* Keep the mine background and existing overlay */
            .stApp {{
                background-image:
                    linear-gradient(
                        rgba(8, 20, 31, 0.84),
                        rgba(8, 20, 31, 0.84)
                    ),
                    url("data:image/png;base64,{encoded_image}");

                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            /* Main dashboard headings */
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp h4 {{
                color: #FFFFFF !important;
                font-weight: 800 !important;
                text-shadow: 1px 1px 3px #000000;
            }}

            /* Paragraphs, labels and general text */
            .stApp p,
            .stApp label {{
                color: #FFFFFF !important;
                font-weight: 600 !important;
            }}

            /* Metric cards */
            [data-testid="stMetric"] {{
                background-color: rgba(0, 0, 0, 0.65);
                border: 1px solid rgba(255, 255, 255, 0.65);
                border-radius: 10px;
                padding: 14px;
            }}

            /* Strong white KPI numbers */
            [data-testid="stMetricValue"],
            [data-testid="stMetricValue"] * {{
                color: #FFFFFF !important;
                font-weight: 800 !important;
                opacity: 1 !important;
                text-shadow: 1px 1px 2px #000000;
            }}

            /* Strong white KPI labels */
            [data-testid="stMetricLabel"],
            [data-testid="stMetricLabel"] * {{
                color: #FFFFFF !important;
                font-weight: 700 !important;
                opacity: 1 !important;
            }}

            /* KPI delta text */
            [data-testid="stMetricDelta"],
            [data-testid="stMetricDelta"] * {{
                color: #FFFFFF !important;
                opacity: 1 !important;
            }}

            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: #101820;
            }}

            [data-testid="stSidebar"] * {{
                color: #FFFFFF !important;
            }}

            /* Expandable table sections */
            [data-testid="stExpander"] {{
                background-color: rgba(0, 0, 0, 0.60);
                border: 1px solid rgba(255, 255, 255, 0.35);
                border-radius: 8px;
            }}

            [data-testid="stExpander"] summary,
            [data-testid="stExpander"] summary p {{
                color: #FFFFFF !important;
                font-weight: 700 !important;
            }}

            /* Data table container */
            [data-testid="stDataFrame"] {{
                border: 1px solid rgba(255, 255, 255, 0.35);
                border-radius: 6px;
            }}

            /* Informational messages */
            [data-testid="stAlert"] p {{
                color: #FFFFFF !important;
                font-weight: 600 !important;
            }}

            /* Captions */
            [data-testid="stCaptionContainer"] {{
                color: #FFFFFF !important;
            }}

            /* Dividers */
            hr {{
                border-color: rgba(255, 255, 255, 0.55) !important;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    except OSError:
        pass


# ============================================================
# 4. EQUIPMENT AVAILABILITY
# ============================================================

def calculate_availability(equipment):
    operating = numeric_column(equipment, "Operating hours")
    downtime = numeric_column(equipment, "Downtime")

    total_time = operating + downtime

    availability = (
        operating / total_time.where(total_time > 0)
    ) * 100

    return availability


# ============================================================
# 5. CHART FUNCTIONS
# ============================================================

def style_plotly_chart(fig):
    """Improve Plotly chart text against the dashboard background."""

    fig.update_layout(
        font=dict(
            color="#FFFFFF",
            size=14,
            family="Arial"
        ),
        title_font=dict(
            color="#FFFFFF",
            size=19,
            family="Arial"
        ),
        paper_bgcolor="rgba(0,0,0,0.55)",
        plot_bgcolor="rgba(0,0,0,0.35)",
        legend=dict(
            font=dict(color="#FFFFFF", size=12)
        ),
        margin=dict(l=25, r=25, t=65, b=35)
    )

    fig.update_xaxes(
        title_font=dict(color="#FFFFFF", size=13),
        tickfont=dict(color="#FFFFFF", size=12),
        gridcolor="rgba(255,255,255,0.18)",
        zerolinecolor="rgba(255,255,255,0.3)"
    )

    fig.update_yaxes(
        title_font=dict(color="#FFFFFF", size=13),
        tickfont=dict(color="#FFFFFF", size=12),
        gridcolor="rgba(255,255,255,0.18)",
        zerolinecolor="rgba(255,255,255,0.3)"
    )

    return fig


def show_pie_chart(data, column, title):
    if data.empty or column not in data.columns:
        st.info(f"No data is available for {title}.")
        return

    chart_data = (
        category_column(data, column)
        .value_counts()
        .rename_axis(column)
        .reset_index(name="Count")
    )

    if PLOTLY_AVAILABLE:
        fig = px.pie(
            chart_data,
            names=column,
            values="Count",
            title=title,
            hole=0.35
        )

        fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont=dict(
                color="#FFFFFF",
                size=13,
                family="Arial"
            )
        )

        fig = style_plotly_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    else:
        st.subheader(title)
        st.bar_chart(chart_data.set_index(column))


def show_bar_chart(data, column, title):
    if data.empty or column not in data.columns:
        st.info(f"No data is available for {title}.")
        return

    chart_data = (
        category_column(data, column)
        .value_counts()
        .rename_axis(column)
        .reset_index(name="Count")
    )

    if PLOTLY_AVAILABLE:
        fig = px.bar(
            chart_data,
            x=column,
            y="Count",
            title=title,
            text="Count"
        )

        fig.update_traces(
            textfont=dict(
                color="#FFFFFF",
                size=13,
                family="Arial"
            ),
            textposition="outside"
        )

        fig = style_plotly_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    else:
        st.subheader(title)
        st.bar_chart(chart_data.set_index(column))


def show_histogram(data, column, title, x_title=None):
    if column not in data.columns:
        st.info(f"{column} is not available.")
        return

    values = numeric_column(data, column).dropna()

    if values.empty:
        st.info(f"No numeric values are available for {column}.")
        return

    if PLOTLY_AVAILABLE:
        fig = px.histogram(
            x=values,
            nbins=20,
            title=title,
            labels={
                "x": x_title or column,
                "y": "Number of records"
            }
        )

        fig = style_plotly_chart(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )
    else:
        st.subheader(title)
        st.bar_chart(values.value_counts().sort_index())


# ============================================================
# 6. MAIN DASHBOARD CONTENT
# ============================================================

def render_dashboard_content():
    set_background()

    st.title("Khwezi Mining Monitoring System")
    st.subheader("Dashboard")

    st.write(
        "Monitor worker safety, incidents, equipment conditions "
        "and maintenance performance."
    )

    if st.button("Refresh Dashboard", type="primary"):
        st.rerun()

    # Load CSV data
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
        st.error(f"Unable to load dashboard data: {error}")

        st.info(
            "Check that workers.csv, incidents.csv and equipment.csv "
            "exist in the project folder or in the data folder."
        )
        return

    # Check identifying columns
    required_columns = [
        (workers, "Worker ID", "workers.csv"),
        (incidents, "Incident ID", "incidents.csv"),
        (equipment, "Equipment ID", "equipment.csv")
    ]

    for data, column, filename in required_columns:
        if column not in data.columns:
            st.error(
                f"The column '{column}' is missing from {filename}."
            )
            return

    equipment = equipment.copy()

    equipment["Calculated Availability (%)"] = (
        calculate_availability(equipment)
    )

    # --------------------------------------------------------
    # WORKER SAFETY METRICS
    # --------------------------------------------------------

    total_workers = len(workers)

    if "Near misses" in workers.columns:
        total_near_misses = numeric_column(
            workers, "Near misses"
        ).sum()
    else:
        total_near_misses = None

    if "Safety observations" in workers.columns:
        total_observations = numeric_column(
            workers, "Safety observations"
        ).sum()
    else:
        total_observations = None

    if "PPE compliance" in workers.columns:
        average_ppe = numeric_column(
            workers, "PPE compliance"
        ).mean()
    else:
        average_ppe = float("nan")

    # --------------------------------------------------------
    # INCIDENT METRICS
    # --------------------------------------------------------

    total_incidents = len(incidents)

    if "Severity" in incidents.columns:
        severity = category_column(
            incidents, "Severity"
        ).str.lower()

        serious_incidents = severity.isin(
            ["serious", "critical", "high"]
        ).sum()
    else:
        serious_incidents = None

    # --------------------------------------------------------
    # EQUIPMENT METRICS
    # --------------------------------------------------------

    total_equipment = len(equipment)

    if "Maintenance status" in equipment.columns:
        maintenance_status = category_column(
            equipment, "Maintenance status"
        ).str.lower()

        operational_count = maintenance_status.isin(
            ["operational", "available"]
        ).sum()

        under_maintenance_count = maintenance_status.isin(
            ["under maintenance", "maintenance"]
        ).sum()
    else:
        operational_count = None
        under_maintenance_count = None

    average_availability = equipment[
        "Calculated Availability (%)"
    ].mean()

    if "Temperature" in equipment.columns:
        critical_temperature = (
            numeric_column(equipment, "Temperature") > 100
        ).fillna(False)
    else:
        critical_temperature = pd.Series(
            False, index=equipment.index
        )

    if "Vibration" in equipment.columns:
        critical_vibration = (
            numeric_column(equipment, "Vibration") > 8
        ).fillna(False)
    else:
        critical_vibration = pd.Series(
            False, index=equipment.index
        )

    critical_alerts = (
        critical_temperature | critical_vibration
    ).sum()

    # --------------------------------------------------------
    # DISPLAY KPI METRICS
    # --------------------------------------------------------

    st.divider()
    st.subheader("Key Performance Indicators")

    row1 = st.columns(4)

    row1[0].metric("Total Workers", f"{total_workers:,}")
    row1[1].metric("Total Incidents", f"{total_incidents:,}")

    row1[2].metric(
        "Near Misses",
        "N/A" if total_near_misses is None
        else f"{total_near_misses:,.0f}"
    )

    row1[3].metric(
        "Safety Observations",
        "N/A" if total_observations is None
        else f"{total_observations:,.0f}"
    )

    row2 = st.columns(4)

    row2[0].metric(
        "Average PPE Compliance",
        "N/A" if pd.isna(average_ppe)
        else f"{average_ppe:.1f}%"
    )

    row2[1].metric(
        "Serious/Critical Incidents",
        "N/A" if serious_incidents is None
        else f"{int(serious_incidents):,}"
    )

    row2[2].metric(
        "Operational Equipment",
        "N/A" if operational_count is None
        else f"{int(operational_count):,}"
    )

    row2[3].metric(
        "Under Maintenance",
        "N/A" if under_maintenance_count is None
        else f"{int(under_maintenance_count):,}"
    )

    row3 = st.columns(3)

    row3[0].metric(
        "Total Equipment",
        f"{total_equipment:,}"
    )

    row3[1].metric(
        "Average Availability",
        "N/A" if pd.isna(average_availability)
        else f"{average_availability:.1f}%"
    )

    row3[2].metric(
        "Critical Equipment Alerts",
        f"{int(critical_alerts):,}"
    )

    # --------------------------------------------------------
    # HEALTH AND SAFETY CHARTS
    # --------------------------------------------------------

    st.divider()
    st.subheader("Worker Health and Safety")

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

    left, right = st.columns(2)

    with left:
        show_histogram(
            workers,
            "PPE compliance",
            "PPE Compliance Distribution",
            "PPE compliance (%)"
        )

    with right:
        show_bar_chart(
            incidents,
            "Incident type",
            "Incidents by Type"
        )

    # --------------------------------------------------------
    # INCIDENT TREND CHART
    # --------------------------------------------------------

    if "Date" in incidents.columns:
        trend = incidents.copy()

        trend["Parsed Date"] = pd.to_datetime(
            trend["Date"],
            errors="coerce"
        )

        trend = trend.dropna(subset=["Parsed Date"])

        if not trend.empty:
            trend["Incident Date"] = (
                trend["Parsed Date"].dt.date
            )

            trend_data = (
                trend.groupby("Incident Date")
                .size()
                .reset_index(name="Number of Incidents")
                .sort_values("Incident Date")
            )

            st.subheader("Incident Trends Over Time")

            if PLOTLY_AVAILABLE:
                fig = px.line(
                    trend_data,
                    x="Incident Date",
                    y="Number of Incidents",
                    markers=True,
                    title="Incidents Recorded by Date"
                )

                fig = style_plotly_chart(fig)

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )
            else:
                st.line_chart(
                    trend_data.set_index("Incident Date")
                )

    # --------------------------------------------------------
    # EQUIPMENT CHARTS
    # --------------------------------------------------------

    st.divider()
    st.subheader("Equipment Condition and Maintenance")

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
            "Equipment by Type"
        )

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

    # --------------------------------------------------------
    # CRITICAL EQUIPMENT ALERTS
    # --------------------------------------------------------

    st.divider()
    st.subheader("Equipment Requiring Immediate Attention")

    alert_flags = pd.Series(
        False, index=equipment.index
    )

    alert_reasons = pd.Series(
        "", index=equipment.index, dtype="object"
    )

    if "Temperature" in equipment.columns:
        temperature = numeric_column(
            equipment, "Temperature"
        )

        hot = (temperature > 100).fillna(False)
        alert_flags = alert_flags | hot

        alert_reasons.loc[hot] += (
            "Temperature above 100°C; "
        )

    if "Vibration" in equipment.columns:
        vibration = numeric_column(
            equipment, "Vibration"
        )

        high_vibration = (vibration > 8).fillna(False)
        alert_flags = alert_flags | high_vibration

        alert_reasons.loc[high_vibration] += (
            "Vibration above 8 mm/s; "
        )

    if alert_flags.any():
        alert_table = equipment.loc[alert_flags].copy()

        alert_table["Alert Reason"] = (
            alert_reasons.loc[alert_flags]
        )

        alert_columns = [
            column for column in [
                "Equipment ID",
                "Equipment type",
                "Temperature",
                "Vibration",
                "Maintenance status",
                "Downtime",
                "Calculated Availability (%)",
                "Alert Reason"
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

    # --------------------------------------------------------
    # WORKER, INCIDENT AND EQUIPMENT TABLES
    # --------------------------------------------------------

    st.divider()

    with st.expander("View Worker Safety Records"):
        show_table(
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

    with st.expander("View Incident Records"):
        show_table(
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

    with st.expander("View Equipment Records"):
        show_table(
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

    # --------------------------------------------------------
    # LAST REFRESHED TIME
    # --------------------------------------------------------

    st.caption(
        "Dashboard last refreshed: "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    if not PLOTLY_AVAILABLE:
        st.info(
            "To enable interactive pie charts and histograms, "
            "add plotly to requirements.txt."
        )


# ============================================================
# 7. DASHBOARD ENTRY POINT AND AUTOMATIC REFRESH
# ============================================================

if hasattr(st, "fragment"):

    @st.fragment(run_every=30)
    def render_dashboard():
        render_dashboard_content()

else:

    def render_dashboard():
        render_dashboard_content()
