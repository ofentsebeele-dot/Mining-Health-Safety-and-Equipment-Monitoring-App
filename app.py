import streamlit as st

from login import login, logout, has_permission
from dashboard import render_dashboard
from worker_health import render_worker_health_page
from incidents import render_incidents_page
from equipment import render_equipment_page
from maintenance import render_maintenance_page
from risk_assessment import render_risk_assessment_page


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


    # --------------------------------------------------
    # WORKER HEALTH
    # --------------------------------------------------

    if has_permission("worker_health"):

        st.write("✅ Worker Health & Safety")

        render_worker_health_page()


    # --------------------------------------------------
    # INCIDENTS
    # --------------------------------------------------

    if has_permission("incidents"):

        st.write("✅ Safety Incidents")

        render_incidents_page()


    # --------------------------------------------------
    # EQUIPMENT
    # --------------------------------------------------

    if has_permission("equipment"):

       render_equipment_page()


    # --------------------------------------------------
    # MAINTENANCE
    # --------------------------------------------------
    if has_permission("maintenance"):

       render_maintenance_page()


    # --------------------------------------------------
    # RISK ASSESSMENT
    # --------------------------------------------------

   if has_permission("risk_assessment"):

      render_risk_assessment_page()


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
