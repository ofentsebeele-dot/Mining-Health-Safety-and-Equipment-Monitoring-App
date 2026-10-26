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



if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = ""



if not st.session_state["logged_in"]:
    login()
    st.stop()




st.title("Khwezi Mining Monitoring System")

st.success(f"Welcome, {st.session_state['username']}!")

st.write(f"Role: **{st.session_state['role']}**")

# Sidebar navigation

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

if has_permission("manage_users"):
    pages.append("Manage Users")


# Check Permissions

if len(pages) == 0:

    st.error("You do not have permission to access any pages.")

    st.stop()

# Page Selection

selected_page = st.sidebar.radio("Select a page", pages)

# Page Display

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


elif selected_page == "Manage Users":

    render_user_management_page()


# Logout

st.sidebar.divider()

logout()
