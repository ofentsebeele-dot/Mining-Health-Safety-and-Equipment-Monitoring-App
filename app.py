
import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# IMPORT LOGIN AND PERMISSION FUNCTIONS
# --------------------------------------------------

from login import login, logout, has_permission

# --------------------------------------------------
# IMPORT APPLICATION PAGES
# --------------------------------------------------

from dashboard import render_dashboard
from worker_health import render_worker_health_page
from incidents import render_incidents_page
from equipment import render_equipment_page
from maintenance import render_maintenance_page
from risk_assessment import render_risk_assessment_page
from reports import render_reports_page
from user_management import render_user_management_page
from questions import render_questions_page

# --------------------------------------------------
# IMPORT NOTIFICATIONS AND ALERTS
# --------------------------------------------------

from notifications_alerts import generate_alert


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = ""

if "equipment_checks" not in st.session_state:
    st.session_state["equipment_checks"] = {}

if "pending_alerts" not in st.session_state:
    st.session_state["pending_alerts"] = {}

if "latest_equipment_alert" not in st.session_state:
    st.session_state["latest_equipment_alert"] = None


# --------------------------------------------------
# LOAD EQUIPMENT CSV FILE
# --------------------------------------------------

DATA_FILE = Path(__file__).parent / "equipment.csv"

try:
    equipment_data = pd.read_csv(DATA_FILE)

except FileNotFoundError:
    st.error(
        "Equipment data file not found. "
        "Place equipment.csv in the same folder as app.py."
    )
    st.stop()

except pd.errors.ParserError:
    st.error("The equipment CSV file could not be read.")
    st.stop()


# --------------------------------------------------
# VALIDATE CSV COLUMNS
# --------------------------------------------------

required_columns = [
    "Equipment ID",
    "Equipment type",
    "Temperature",
    "Vibration"
]

missing_columns = [
    column
    for column in required_columns
    if column not in equipment_data.columns
]

if missing_columns:
    st.error(
        "The equipment CSV is missing these columns: "
        + ", ".join(missing_columns)
    )
    st.stop()


# --------------------------------------------------
# CLEAN EQUIPMENT DATA
# --------------------------------------------------

equipment_data["Equipment ID"] = (
    equipment_data["Equipment ID"]
    .astype("string")
    .str.strip()
)

equipment_data["Temperature"] = pd.to_numeric(
    equipment_data["Temperature"],
    errors="coerce"
)

equipment_data["Vibration"] = pd.to_numeric(
    equipment_data["Vibration"],
    errors="coerce"
)

equipment_data = equipment_data.dropna(
    subset=[
        "Equipment ID",
        "Temperature",
        "Vibration"
    ]
)

equipment_data = equipment_data[
    equipment_data["Equipment ID"] != ""
]

if equipment_data.empty:
    st.error(
        "The equipment CSV does not contain valid equipment readings."
    )
    st.stop()


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

if not st.session_state["logged_in"]:
    login()
    st.stop()


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

st.title("Khwezi Mining Monitoring System")

st.success(
    f"Welcome, {st.session_state['username']}!"
)

st.write(
    f"Role: **{st.session_state['role']}**"
)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("Navigation")

pages = []

if has_permission("dashboard"):
    pages.append("Dashboard")

if has_permission("worker_health"):
    pages.append("Worker Health & Safety")

if has_permission("incidents"):
    pages.append("Safety Incidents")

if has_permission("equipment"):
    pages.append("Equipment")

if has_permission("maintenance"):
    pages.append("Maintenance")

if has_permission("risk_assessment"):
    pages.append("Risk Assessment")

if has_permission("reports"):
    pages.append("Reports")

if has_permission("questions"):
    pages.append("Questions & Answers")

# Count equipment items with pending alerts.
pending_count = len(
    st.session_state["pending_alerts"]
)

alerts_page_label = "Notifications & Alerts"

if pending_count > 0:
    alerts_page_label = (
        f"Notifications & Alerts ({pending_count})"
    )

if has_permission("equipment"):
    pages.append(alerts_page_label)

if has_permission("manage_users"):
    pages.append("Manage Users")


# --------------------------------------------------
# CHECK AVAILABLE PAGES
# --------------------------------------------------

if not pages:
    st.error(
        "You do not have permission to access any pages."
    )
    st.stop()


# --------------------------------------------------
# SELECT PAGE
# --------------------------------------------------

selected_page = st.sidebar.radio(
    "Select a page",
    pages
)


# --------------------------------------------------
# DASHBOARD
# --------------------------------------------------

if selected_page == "Dashboard":

    render_dashboard()


# --------------------------------------------------
# WORKER HEALTH
# --------------------------------------------------

elif selected_page == "Worker Health & Safety":

    render_worker_health_page()


# --------------------------------------------------
# SAFETY INCIDENTS
# --------------------------------------------------

elif selected_page == "Safety Incidents":

    render_incidents_page()


# --------------------------------------------------
# EQUIPMENT
# --------------------------------------------------

elif selected_page == "Equipment":

    render_equipment_page()


# --------------------------------------------------
# MAINTENANCE
# --------------------------------------------------

elif selected_page == "Maintenance":

    render_maintenance_page()


# --------------------------------------------------
# RISK ASSESSMENT
# --------------------------------------------------

elif selected_page == "Risk Assessment":

    render_risk_assessment_page()


# --------------------------------------------------
# REPORTS
# --------------------------------------------------

elif selected_page == "Reports":

    render_reports_page()


# --------------------------------------------------
# QUESTIONS AND ANSWERS
# --------------------------------------------------

elif selected_page == "Questions & Answers":

    render_questions_page()


# --------------------------------------------------
# NOTIFICATIONS AND ALERTS
# --------------------------------------------------

elif selected_page == alerts_page_label:

    st.header("Equipment Notifications & Alerts")

    st.write(
        "Select equipment from the CSV dataset to check "
        "its recorded temperature and vibration."
    )

    st.caption(
        f"Equipment records available: {len(equipment_data)}"
    )

    # --------------------------------------------------
    # SELECT EQUIPMENT
    # --------------------------------------------------

    equipment_ids = (
        equipment_data["Equipment ID"]
        .drop_duplicates()
        .tolist()
    )

    selected_equipment = st.selectbox(
        "Select Equipment ID",
        equipment_ids,
        key="selected_equipment_id"
    )

    # Get the selected equipment record.
    selected_row = equipment_data.loc[
        equipment_data["Equipment ID"]
        == selected_equipment
    ].iloc[0]

    st.subheader("Selected Equipment")

    st.write(
        f"**Equipment ID:** {selected_row['Equipment ID']}"
    )

    st.write(
        f"**Equipment Type:** {selected_row['Equipment type']}"
    )

    # --------------------------------------------------
    # DISPLAY RECORDED READINGS
    # --------------------------------------------------

    csv_temperature = float(
        selected_row["Temperature"]
    )

    csv_vibration = float(
        selected_row["Vibration"]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Recorded Temperature",
            f"{csv_temperature:.1f} °C"
        )

    with col2:

        st.metric(
            "Recorded Vibration",
            f"{csv_vibration:.1f} mm/s"
        )

    # --------------------------------------------------
    # MANUAL TESTING OPTION
    # --------------------------------------------------

    use_manual_readings = st.checkbox(
        "Enter different readings to test alerts",
        key=f"manual_mode_{selected_equipment}"
    )

    if use_manual_readings:

        temperature = st.number_input(
            "Test Temperature (°C)",
            min_value=0.0,
            max_value=500.0,
            value=csv_temperature,
            step=1.0,
            key=f"test_temperature_{selected_equipment}"
        )

        vibration = st.number_input(
            "Test Vibration (mm/s)",
            min_value=0.0,
            max_value=100.0,
            value=csv_vibration,
            step=0.5,
            key=f"test_vibration_{selected_equipment}"
        )

    else:

        temperature = csv_temperature
        vibration = csv_vibration

    # --------------------------------------------------
    # CHECK EQUIPMENT
    # --------------------------------------------------

    if st.button(
        "Check Equipment",
        type="primary"
    ):

        result = generate_alert(
            selected_equipment,
            temperature,
            vibration
        )

        result["equipment_type"] = (
            selected_row["Equipment type"]
        )

        # Store the latest result for this equipment.
        st.session_state["equipment_checks"][
            selected_equipment
        ] = result

        st.session_state["latest_equipment_alert"] = result

        # Add or update pending warnings and critical alerts.
        if result["alert_level"] in [
            "Warning",
            "Critical"
        ]:

            st.session_state["pending_alerts"][
                selected_equipment
            ] = result

        else:

            # Normal readings clear the pending alert.
            st.session_state["pending_alerts"].pop(
                selected_equipment,
                None
            )

        st.rerun()

    # --------------------------------------------------
    # PENDING NOTIFICATIONS
    # --------------------------------------------------

    st.divider()

    st.subheader("Notifications Awaiting Review")

    pending_alerts = st.session_state["pending_alerts"]

    if pending_alerts:

        st.write(
            f"{len(pending_alerts)} equipment item(s) "
            "have alerts awaiting review."
        )

        for alert_id, alert in list(
            pending_alerts.items()
        ):

            with st.container(border=True):

                st.write(
                    f"**Equipment ID:** {alert_id}"
                )

                if "equipment_type" in alert:

                    st.write(
                        f"**Equipment Type:** "
                        f"{alert['equipment_type']}"
                    )

                st.write(
                    f"**Alert Level:** "
                    f"{alert['alert_level']}"
                )

                st.write(alert["alert_message"])

                st.write(
                    f"Temperature: "
                    f"{alert['temperature']:.1f} °C"
                )

                st.write(
                    f"Vibration: "
                    f"{alert['vibration']:.1f} mm/s"
                )

                if st.button(
                    "Mark as Reviewed",
                    key=f"review_{alert_id}"
                ):

                    st.session_state["pending_alerts"].pop(
                        alert_id,
                        None
                    )

                    st.rerun()

    else:

        st.success(
            "There are no alerts awaiting review."
        )

    # --------------------------------------------------
    # LATEST EQUIPMENT CHECKS
    # --------------------------------------------------

    st.divider()

    st.subheader("Latest Equipment Checks")

    all_checks = st.session_state["equipment_checks"]

    if all_checks:

        result_equipment = st.selectbox(
            "Select equipment to view its latest result",
            list(all_checks.keys()),
            key="view_equipment_results"
        )

        result = all_checks[result_equipment]

        st.write(
            f"**Equipment ID:** {result['equipment_id']}"
        )

        if "equipment_type" in result:

            st.write(
                f"**Equipment Type:** "
                f"{result['equipment_type']}"
            )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Temperature",
                f"{result['temperature']:.1f} °C"
            )

            st.write(
                f"Temperature Status: "
                f"{result['temperature_status']}"
            )

        with col2:

            st.metric(
                "Vibration",
                f"{result['vibration']:.1f} mm/s"
            )

            st.write(
                f"Vibration Status: "
                f"{result['vibration_status']}"
            )

        st.write(
            f"**Overall Alert:** {result['alert_level']}"
        )

        st.write(result["alert_message"])

        if result["alert_level"] == "Critical":

            st.error(
                "Urgent equipment assessment required."
            )

        elif result["alert_level"] == "Warning":

            st.warning(
                "Equipment requires attention."
            )

        else:

            st.success(
                "Equipment readings are normal."
            )

    else:

        st.info(
            "Select equipment and click Check Equipment "
            "to generate the first result."
        )


# --------------------------------------------------
# USER MANAGEMENT
# --------------------------------------------------

elif selected_page == "Manage Users":

    render_user_management_page()


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

st.sidebar.divider()

if st.sidebar.button("Logout"):

    logout()
    st.rerun()
