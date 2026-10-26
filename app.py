
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


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Khwezi Mining Monitoring System",
    layout="wide"
)


# --------------------------------------------------
# APPLICATION THEME
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #1E293B !important;
}

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

[data-testid="stSidebar"] {
    background-color: #172033 !important;
    min-width: 250px;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] [role="radiogroup"] label,
[data-testid="stSidebar"] [role="radiogroup"] label p {
    color: #FFFFFF !important;
}

.stTextInput input,
.stTextArea textarea,
.stNumberInput input {
    background-color: #263449 !important;
    color: #FFFFFF !important;
    border: 1px solid #64748B !important;
}

.stSelectbox div[data-baseweb="select"] > div,
.stMultiSelect div[data-baseweb="select"] > div {
    background-color: #263449 !important;
    color: #FFFFFF !important;
}

[data-baseweb="select"] span {
    color: #FFFFFF !important;
}

.stButton button,
.stDownloadButton button {
    background-color: #263449 !important;
    color: #FFFFFF !important;
    border: 1px solid #64748B !important;
}

.stButton button:hover,
.stDownloadButton button:hover {
    background-color: #334155 !important;
    color: #FFFFFF !important;
    border-color: #FFFFFF !important;
}

[data-testid="stMetric"],
[data-testid="stExpander"] {
    background-color: #263449 !important;
    border-radius: 8px;
}

[data-testid="stDataFrame"] {
    border: 1px solid #64748B !important;
}

hr {
    border-color: #64748B !important;
}

.stCheckbox label,
.stRadio label {
    color: #FFFFFF !important;
}

[data-testid="stForm"] {
    background-color: #1E293B !important;
    border-color: #64748B !important;
}

.stApp a {
    color: #93C5FD !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #CBD5E1 !important;
}
</style>
""", unsafe_allow_html=True)


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

if not st.session_state["logged_in"]:
    login()
    st.stop()


# --------------------------------------------------
# MAIN TITLE
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

# Each page is linked to its required permission.
page_permissions = {
    "Dashboard": "dashboard",
    "Worker Health & Safety": "worker_health",
    "Safety Incidents": "incidents",
    "Equipment": "equipment",
    "Maintenance": "maintenance",
    "Risk Assessment": "risk_assessment",
    "Reports": "reports",
    "Questions & Answers": "questions",
    "Notifications & Alerts": "notifications_alerts",
    "Manage Users": "manage_users"
}

# Display only pages the logged-in user can access.
pages = [
    page_name
    for page_name, permission in page_permissions.items()
    if has_permission(permission)
]

if not pages:
    st.error("You do not have permission to access any pages.")
    st.stop()

selected_page = st.sidebar.radio(
    "Select a page",
    pages,
    key="main_navigation"
)


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

elif selected_page == "Notifications & Alerts":
    render_notifications_page()

elif selected_page == "Manage Users":
    render_user_management_page()


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

st.sidebar.divider()

if st.sidebar.button("Logout", key="logout_button"):
    logout()
