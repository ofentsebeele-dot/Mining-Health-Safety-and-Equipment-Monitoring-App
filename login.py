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

    "worker": {
        "password": "worker123",
        "role": "Worker"
    }
}


# --------------------------------------------------
# PERMISSIONS
# --------------------------------------------------

permissions = {

    "Administrator": [
        "dashboard",
        "worker_health",
        "incidents",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports", "questions",
        "manage_users"
    ],

    "Safety Officer": [
        "dashboard",
        "worker_health",
        "incidents",
        "risk_assessment", "questions",
        "reports"
    ],

    "Mining Manager": [
        "dashboard",
        "worker_health",
        "incidents",
        "equipment",
        "maintenance",
        "risk_assessment", "questions",
        "reports"
    ],

    "Worker": [
        "dashboard", "questions",
        "worker_health"
    ]
}


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

                st.success(
                    "Login successful."
                )

                st.rerun()

            else:

                st.error(
                    "Incorrect password."
                )

        else:

            st.error(
                "Username not found."
            )


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

    role = st.session_state.get(
        "role",
        ""
    )

    if role not in permissions:

        return False

    return permission in permissions[role]
