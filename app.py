
import streamlit as st

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

# Import equipment notification and alert functions.
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


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

# Show the login page if the user is not logged in.
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

# Add pages according to the user's permissions.
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

# Only users with equipment permission can access alerts.
if has_permission("equipment"):
    pages.append("Notifications & Alerts")

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
# SELECT APPLICATION PAGE
# --------------------------------------------------

selected_page = st.sidebar.radio(
    "Select a page",
    pages
)


# --------------------------------------------------
# DISPLAY SELECTED PAGE
# --------------------------------------------------

if selected_page == "Dashboard":

    render_dashboard()


elif selected_page == "Worker Health & Safety":

    render_worker_health_page()


elif selected_page == "Safety Incidents":

    render_incidents_page()


elif selected_page == "Equipment":

    render_equipment_page()


elif selected_page == "Maintenance":

    render_maintenance_page()


elif selected_page == "Risk Assessment":

    render_risk_assessment_page()


elif selected_page == "Reports":

    render_reports_page()


elif selected_page == "Questions & Answers":

    render_questions_page()


# --------------------------------------------------
# NOTIFICATIONS AND ALERTS PAGE
# --------------------------------------------------

elif selected_page == "Notifications & Alerts":

    st.header("Equipment Notifications & Alerts")

    st.write(
        "Enter equipment temperature and vibration readings "
        "to determine the equipment condition and alert level."
    )


    # --------------------------------------------------
    # EQUIPMENT INPUTS
    # --------------------------------------------------

    equipment_id = st.text_input(
        "Equipment ID",
        value="EQ001"
    )

    temperature = st.number_input(
        "Temperature (°C)",
        min_value=0.0,
        max_value=500.0,
        value=65.0,
        step=1.0
    )

    vibration = st.number_input(
        "Vibration (mm/s)",
        min_value=0.0,
        max_value=100.0,
        value=3.0,
        step=0.5
    )

    # --------------------------------------------------
    # CHECK EQUIPMENT
    # --------------------------------------------------

    if st.button(
        "Check Equipment",
        type="primary"
    ):

        if not equipment_id.strip():

            st.error(
                "Please enter an equipment ID."
            )

        else:

            # Generate the equipment alert.
            result = generate_alert(
                equipment_id.strip(),
                temperature,
                vibration
            )

            # Save the latest result for this session.
            st.session_state["latest_equipment_alert"] = result

    # --------------------------------------------------
    # DISPLAY EQUIPMENT RESULTS
    # --------------------------------------------------

    result = st.session_state.get(
        "latest_equipment_alert"
    )

    if result:

        st.divider()

        st.subheader("Equipment Reading Results")

        st.write(
            f"**Equipment ID:** {result['equipment_id']}"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Temperature",
                f"{result['temperature']:.1f} °C"
            )

            st.write(
                f"**Temperature Status:** "
                f"{result['temperature_status']}"
            )

        with col2:

            st.metric(
                "Vibration",
                f"{result['vibration']:.1f} mm/s"
            )

            st.write(
                f"**Vibration Status:** "
                f"{result['vibration_status']}"
            )

        st.divider()

        st.subheader("Overall Alert")

        if result["alert_level"] == "Critical":

            st.error(
                f"Alert Level: {result['alert_level']}\n\n"
                f"{result['alert_message']}"
            )

        elif result["alert_level"] == "Warning":

            st.warning(
                f"Alert Level: {result['alert_level']}\n\n"
                f"{result['alert_message']}"
            )

        else:

            st.success(
                f"Alert Level: {result['alert_level']}\n\n"
                f"{result['alert_message']}"
            )


# --------------------------------------------------
# USER MANAGEMENT PAGE
# --------------------------------------------------

elif selected_page == "Manage Users":

    render_user_management_page()


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

st.sidebar.divider()

if st.sidebar.button("Logout"):

    logout()
