import streamlit as st

from login import login, logout, has_permission


# Set default login status
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = ""


# Login page
if not st.session_state["logged_in"]:

    login()


# Main application
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

    # Dashboard
    if has_permission("dashboard"):
        st.write("✅ Dashboard")

    # Worker Health
    if has_permission("worker_health"):
        st.write("✅ Worker Health & Safety")

    # Incidents
    if has_permission("incidents"):
        st.write("✅ Safety Incidents")

    # Equipment
    if has_permission("equipment"):
        st.write("✅ Equipment")

    # Maintenance
    if has_permission("maintenance"):
        st.write("✅ Maintenance")

    # Risk Assessment
    if has_permission("risk_assessment"):
        st.write("✅ Risk Assessment")

    # Reports
    if has_permission("reports"):
        st.write("✅ Reports")

    # User Management
    if has_permission("manage_users"):
        st.write("✅ Manage Users")

    st.divider()

    logout()
