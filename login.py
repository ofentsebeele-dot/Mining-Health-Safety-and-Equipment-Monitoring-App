
import pandas as pd


def check_temperature(temperature):
    if temperature > 100:
        return "Critical"
    elif temperature >= 80:
        return "Warning"
    return "Normal"


def check_vibration(vibration):
    if vibration > 8:
        return "Critical"
    elif vibration >= 5:
        return "Warning"
    return "Normal"


<<<<<<< HEAD
def generate_alert(equipment_id, temperature, vibration):
    temperature_status = check_temperature(temperature)
    vibration_status = check_vibration(vibration)

    if (
        temperature_status == "Critical"
        or vibration_status == "Critical"
    ):
        alert_level = "Critical"
        alert_message = "Urgent assessment required."

    elif (
        temperature_status == "Warning"
        or vibration_status == "Warning"
    ):
        alert_level = "Warning"
        alert_message = "Equipment requires attention."

    else:
        alert_level = "Normal"
        alert_message = "Equipment readings are normal."

    return {
        "equipment_id": str(equipment_id),
        "temperature": float(temperature),
        "temperature_status": temperature_status,
        "vibration": float(vibration),
        "vibration_status": vibration_status,
        "alert_level": alert_level,
        "alert_message": alert_message,
=======
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
>>>>>>> 3dc928d (updated)

    for index, row in data.iterrows():
        incident_id = row.get(
            "Incident ID",
            row.get("ID", f"Incident {index + 1}")
        )

        description = row.get(
            "Description",
            row.get("Incident Type", "Safety incident")
        )

        severity = str(
            row.get("Severity", row.get("Priority", "Warning"))
        ).strip().lower()

        status = str(row.get("Status", "Open")).strip().lower()

<<<<<<< HEAD
        if status in ("closed", "resolved", "reviewed", "complete"):
            continue
=======
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
>>>>>>> 3dc928d (updated)

        if severity in ("critical", "high", "severe", "urgent"):
            alert_level = "Critical"
        elif severity in ("low", "minor", "normal"):
            alert_level = "Normal"
        else:
<<<<<<< HEAD
            alert_level = "Warning"

        notifications.append({
            "incident_id": str(incident_id),
            "description": str(description),
            "alert_level": alert_level,
            "status": status,
        })

    return notifications
=======
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
>>>>>>> 3dc928d (updated)
