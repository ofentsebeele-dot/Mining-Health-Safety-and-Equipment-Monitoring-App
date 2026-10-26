import streamlit as st


# --------------------------------------------------
# USERS
# --------------------------------------------------

users = {
    "admin": {
        "password": "admin123",
        "role": "Administrator"
    },

    "safety": {
        "password": "safety123",
        "role": "Safety Officer"
    },

    "manager": {
        "password": "manager123",
        "role": "Mining Manager"
    },

    "engineer": {
        "password": "engineer123",
        "role": "Maintenance Engineer"
    },

    "worker": {
        "password": "worker123",
        "role": "Worker"
>>>>>>> 3dc928d (updated)
    }


<<<<<<< HEAD
def load_incidents(file_path="incidents.csv"):
    data = pd.read_csv(file_path)
    data.columns = data.columns.astype(str).str.strip()
    return data.dropna(how="all")


def generate_incident_notifications(data):
    notifications = []
=======
# --------------------------------------------------
# EXISTING ROLE PERMISSIONS (Aligned with Table 1 of Project Brief)
# --------------------------------------------------

permissions = {

    "Administrator": [
        "dashboard",
        "worker_health",
        "incidents",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports",
        "questions",
        "manage_users"
    ],

    "Safety Officer": [
        "dashboard",
        "worker_health",
        "incidents",
        "risk_assessment",
        "questions",
        "reports"
    ],

    "Mining Manager": [
        "dashboard",
        "worker_health",
        "incidents",
        "equipment",
        "maintenance",
        "risk_assessment",
        "questions",
        "reports"
    ],

    "Maintenance Engineer": [
        "dashboard",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports",
        "questions"
    ],

    "Worker": [
        "dashboard",
        "questions",
        "worker_health"
    ]
}


# --------------------------------------------------
# USER-SPECIFIC PERMISSION CHANGES
# --------------------------------------------------

user_permissions = {}


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

def login():

    st.title("Khwezi Mining Monitoring System")

    st.subheader("Login")

    username = st.text_input(
        "Username",
        key="login_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    if st.button("Login"):

        if username in users:

            if users[username]["password"] == password:

                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = users[username]["role"]

                st.success("Login successful.")
                st.rerun()

            else:
                st.error("Incorrect password.")

        if severity in ("critical", "high", "severe", "urgent"):
            alert_level = "Critical"
        elif severity in ("low", "minor", "normal"):
            alert_level = "Normal"
        else:
            st.error("Username not found.")


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

def logout():

    if st.sidebar.button("Logout"):

        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["role"] = ""

        st.rerun()


# --------------------------------------------------
# PERMISSION CHECK
# --------------------------------------------------

def has_permission(permission):

    username = st.session_state.get("username", "")
    role = st.session_state.get("role", "")

    if username not in users:
        return False

    if permission == "questions":
        return True

    if username in user_permissions:
        return permission in user_permissions[username]

    if role not in permissions:
        return False

    return permission in permissions[role]