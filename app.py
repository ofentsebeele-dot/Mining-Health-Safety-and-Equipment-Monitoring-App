
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
from notifications_alerts import render_notifications_page


# App background: black and white font

st.markdown("""
<style>

/* Main application background */
.stApp {
    background-color: #1E293B !important;
}

/* Main application text */
.stApp p,
.stApp h1,
.stApp h2,
.stApp h3,
.stApp h4,
.stApp h5,
.stApp h6,
.stApp label,
.stApp li,
.stApp span,
.stApp [data-testid="stMarkdownContainer"],
.stApp [data-testid="stMetricLabel"],
.stApp [data-testid="stMetricValue"],
.stApp [data-testid="stCaptionContainer"] {
    color: #FFFFFF !important;
}

/* Sidebar background */
[data-testid="stSidebar"] {
    background-color: #172033 !important;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #FFFFFF !important;
}

/* Sidebar navigation radio labels */
[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [role="radiogroup"] label p {
    color: #FFFFFF !important;
}

/* Text inputs */
.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #263449 !important;
    color: #FFFFFF !important;
    border: 1px solid #64748B !important;
}

/* Dropdowns */
.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    background-color: #263449 !important;
    color: #FFFFFF !important;
}

/* Dropdown selected text */
[data-baseweb="select"] span {
    color: #FFFFFF !important;
}

/* Buttons */
.stButton button,
.stDownloadButton button {
    background-color: #263449 !important;
    color: #FFFFFF !important;
    border: 1px solid #64748B !important;
}

/* Button hover */
.stButton button:hover,
.stDownloadButton button:hover {
    background-color: #334155 !important;
    color: #FFFFFF !important;
    border-color: #FFFFFF !important;
}

/* Metrics and containers */
[data-testid="stMetric"],
[data-testid="stExpander"] {
    background-color: #263449 !important;
    border-radius: 8px;
}

/* Dataframe container */
[data-testid="stDataFrame"] {
    border: 1px solid #64748B !important;
}

/* Dividers */
hr {
    border-color: #64748B !important;
}

/* Checkbox and radio text */
.stCheckbox label,
.stRadio label {
    color: #FFFFFF !important;
}

/* Form backgrounds */
[data-testid="stForm"] {
    background-color: #1E293B !important;
    border-color: #64748B !important;
}

/* Links */
.stApp a {
    color: #93C5FD !important;
}

/* Placeholder text */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #CBD5E1 !important;
}

</style>
""", unsafe_allow_html=True)

# Session date

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = ""

# Login

if not st.session_state["logged_in"]:
    login()
    st.stop()


# Main tittle

st.title("Monitoring System")

st.success(f"Welcome, {st.session_state['username']}!")

st.write(f"Role: **{st.session_state['role']}**")


# Sidebar Navigation

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

if has_permission("equipment"):
    pages.append("Notifications & Alerts")

if has_permission("manage_users"):
    pages.append("Manage Users")


# Check permissions

if not pages:
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

elif selected_page == "Notifications & Alerts":
    render_notifications_page()

elif selected_page == "Manage Users":
    render_user_management_page()

# Logout

st.sidebar.divider()

if st.sidebar.button("Logout", key="logout_button"):
    logout()
    st.rerun()
