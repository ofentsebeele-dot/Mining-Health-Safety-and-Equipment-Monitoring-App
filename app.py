import streamlit as st

from login import login, logout, has_permission
from dashboard import render_dashboard
from worker_health import render_worker_health_page
from incidents import render_incidents_page
from equipment import render_equipment_page
from maintenance import render_maintenance_page
from risk_assessment import render_risk_assessment_page
from reports import render_reports_page
from user_management import render_user_management_page
from questions import render_questions_page

from notifications_alerts import (
    load_equipment_data,
    generate_alert,
    generate_notifications,
)


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


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

if not st.session_state["logged_in"]:
    login()
    st.stop()


# --------------------------------------------------
# LOAD EQUIPMENT DATA
# --------------------------------------------------

try:
    equipment_data = load_equipment_data()

except (FileNotFoundError, ValueError, OSError) as error:
    st.error(f"Could not load equipment data: {error}")
    st.stop()

except Exception as error:
    st.error(f"An error occurred while reading equipment data: {error}")
    st.stop()


# --------------------------------------------------
# AUTOMATICALLY GENERATE NOTIFICATIONS
# --------------------------------------------------

try:
    notifications = generate_notifications()

    for notification in notifications:
        equipment_id = notification["equipment_id"]

        if equipment_id not in st.session_state["equipment_checks"]:
            st.session_state["equipment_checks"][equipment_id] = (
                notification
            )

        # Keep an alert pending until it is reviewed.
        if equipment_id not in st.session_state["pending_alerts"]:
            st.session_state["pending_alerts"][equipment_id] = (
                notification
            )

except (FileNotFoundError, ValueError, OSError) as error:
    st.error(f"Could not generate equipment notifications: {error}")
    st.stop()

except Exception as error:
    st.error(f"An error occurred while generating notifications: {error}")
    st.stop()


# --------------------------------------------------
# MAIN TITLE
# --------------------------------------------------

st.title("Khwezi Mining Monitoring System")

st.success(f"Welcome, {st.session_state['username']}!")

st.write(f"Role: **{st.session_state['role']}**")


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


# Show the number of alerts awaiting review.
pending_count = len(st.session_state["pending_alerts"])

alerts_page_label = "Notifications & Alerts"

if pending_count > 0:
    alerts_page_label = f"Notifications & Alerts ({pending_count})"

if has_permission("equipment"):
    pages.append(alerts_page_label)

if has_permission("manage_users"):
    pages.append("Manage Users")


# --------------------------------------------------
# CHECK PERMISSIONS
# --------------------------------------------------

if not pages:
    st.error("You do not have permission to access any pages.")
    st.stop()


# --------------------------------------------------
# PAGE SELECTION
# --------------------------------------------------

selected_page = st.sidebar.radio("Select a page", pages)


# --------------------------------------------------
# PAGE DISPLAY
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
# NOTIFICATIONS AND ALERTS
# --------------------------------------------------

elif selected_page == alerts_page_label:

    st.header("Notifications & Alerts")

    equipment_ids = equipment_data["Equipment ID"].drop_duplicates().tolist()

    selected_equipment = st.selectbox(
        "Select Equipment ID",
        equipment_ids
    )

    selected_rows = equipment_data[
        equipment_data["Equipment ID"] == selected_equipment
    ]

    if not selected_rows.empty:

        selected_row = selected_rows.iloc[0]

        st.subheader("Equipment Readings")

        st.write(f"**Equipment ID:** {selected_equipment}")

        if "Equipment type" in equipment_data.columns:
            st.write(
                f"**Equipment Type:** {selected_row['Equipment type']}"
            )

        temperature = float(selected_row["Temperature"])
        vibration = float(selected_row["Vibration"])

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Temperature", f"{temperature:.1f} °C")

        with col2:
            st.metric("Vibration", f"{vibration:.1f} mm/s")

        if st.button("Check Equipment"):

            result = generate_alert(
                selected_equipment,
                temperature,
                vibration
            )

            if "Equipment type" in equipment_data.columns:
                result["equipment_type"] = selected_row["Equipment type"]

            st.session_state["equipment_checks"][selected_equipment] = result

            if result["alert_level"] in ["Warning", "Critical"]:
                st.session_state["pending_alerts"][selected_equipment] = result
            else:
                st.session_state["pending_alerts"].pop(
                    selected_equipment, None
                )

            st.rerun()

    # Show the selected equipment's latest check.
    st.divider()
    st.subheader("Latest Equipment Check")

    latest_check = st.session_state["equipment_checks"].get(
        selected_equipment
    )

    if latest_check:

        st.write(f"**Alert Level:** {latest_check['alert_level']}")
        st.write(latest_check["alert_message"])

        st.write(
            f"Temperature Status: {latest_check['temperature_status']}"
        )

        st.write(
            f"Vibration Status: {latest_check['vibration_status']}"
        )

        if latest_check["alert_level"] == "Critical":
            st.error("Urgent equipment assessment required.")

        elif latest_check["alert_level"] == "Warning":
            st.warning("Equipment requires attention.")

        else:
            st.success("Equipment readings are normal.")

    else:
        st.info("Click Check Equipment to check the selected equipment.")

    # Show notifications that still need review.
    st.divider()
    st.subheader("Notifications Awaiting Review")

    pending_alerts = st.session_state["pending_alerts"]

    if pending_alerts:

        for alert_id, alert in list(pending_alerts.items()):

            with st.container(border=True):

                st.write(f"**Equipment ID:** {alert_id}")

                if "equipment_type" in alert:
                    st.write(
                        f"**Equipment Type:** {alert['equipment_type']}"
                    )

                st.write(f"**Alert Level:** {alert['alert_level']}")
                st.write(alert["alert_message"])

                st.write(
                    f"Temperature: {alert['temperature']:.1f} °C"
                )

                st.write(
                    f"Vibration: {alert['vibration']:.1f} mm/s"
                )

                if st.button(
                    "Mark as Reviewed",
                    key=f"review_{alert_id}"
                ):
                    st.session_state["pending_alerts"].pop(
                        alert_id, None
                    )
                    st.rerun()

    else:
        st.success("There are no alerts awaiting review.")


elif selected_page == "Manage Users":

    render_user_management_page()


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

st.sidebar.divider()

if st.sidebar.button("Logout"):
    logout()
    st.rerun()
