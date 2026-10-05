import streamlit as st

from login import login, logout, has_permission
from dashboard import render_dashboard
from worker_health import render_worker_health_page
from incidents import render_incidents

# Set default login status
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = ""


# --------------------------------------------------
# LOGIN PAGE
# --------------------------------------------------

if not st.session_state["logged_in"]:

    login()


# --------------------------------------------------
# MAIN APPLICATION
# --------------------------------------------------

else:

    st.title("Khwezi Mining Monitoring System")

    st.success(
        f"Welcome, {st.session_state['username']}!"
    )

    st.write(
        f"Role: **{st.session_state['role']}**"
    )

    st.divider()

    st.header("Navigation")


    # --------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------

    if has_permission("dashboard"):

        st.write("✅ Dashboard")

        render_dashboard()

    else:

        st.error(
            "You do not have permission to access the dashboard."
        )


    # --------------------------------------------------
    # WORKER HEALTH
    # --------------------------------------------------

    if has_permission("worker_health"):

       render_worker_health_page()


    # --------------------------------------------------
    # INCIDENTS
    # --------------------------------------------------

    if has_permission("incidents"):
        
        render_incidents_page()


    # --------------------------------------------------
    # EQUIPMENT
    # --------------------------------------------------

    if has_permission("equipment"):

        st.write("✅ Equipment")


    # --------------------------------------------------
    # MAINTENANCE
    # --------------------------------------------------

    if has_permission("maintenance"):

        st.write("✅ Maintenance")


    # --------------------------------------------------
    # RISK ASSESSMENT
    # --------------------------------------------------

    if has_permission("risk_assessment"):

        st.write("✅ Risk Assessment")


    # --------------------------------------------------
    # REPORTS
    # --------------------------------------------------

    if has_permission("reports"):

        st.write("✅ Reports")


    # --------------------------------------------------
    # USER MANAGEMENT
    # --------------------------------------------------

    if has_permission("manage_users"):

        st.write("✅ Manage Users")


    st.divider()


    # --------------------------------------------------
    # LOGOUT
    # --------------------------------------------------

    logout()
