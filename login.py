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

    "mining": {
        "password": "mining123",
        "role": "Mining Engineer"
    },

    "maintenance": {
        "password": "maintenance123",
        "role": "Maintenance Engineer"
    },

    "manager": {
        "password": "manager123",
        "role": "Manager"
    },

    "worker": {
        "password": "worker123",
        "role": "Worker"
    }
}


# --------------------------------------------------
# ROLE PERMISSIONS
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
        "reports",
        "questions"
    ],

    "Mining Engineer": [
        "dashboard",
        "worker_health",
        "maintenance",
        "risk_assessment",
        "questions"
    ],

    "Maintenance Engineer": [
        "dashboard",
        "worker_health",
        "incidents",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports",
        "questions"
    ],

    "Manager": [
        "dashboard",
        "worker_health",
        "incidents",
        "maintenance",
        "reports",
        "questions"
    ],

    "Worker": [
        "dashboard",
        "worker_health",
        "questions"
    ]
}


# --------------------------------------------------
# USER-SPECIFIC PERMISSIONS
# --------------------------------------------------
# This stores permission changes made by
# the Administrator.

user_permissions = {}


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

def login():

    st.title("Khwezi Mining Monitoring System")

    st.subheader("Login")

    # Username
    username = st.text_input(
        "Username",
        key="login_username"
    )

    # Password
    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    # Login button
    if st.button("Login"):

        # Check if username exists
        if username in users:

            # Check password
            if users[username]["password"] == password:

                # Save login information
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = users[username]["role"]

                st.success("Login successful.")

                # Reload the application
                st.rerun()

            else:

                st.error("Incorrect password.")

        else:

            st.error("Username not found.")


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

def logout():

    # Display logout button in the sidebar
    if st.sidebar.button("Logout"):

        # Clear login information
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["role"] = ""

        # Reload the application
        st.rerun()


# --------------------------------------------------
# PERMISSION CHECK
# --------------------------------------------------

def has_permission(permission):

    # Get the current username
    username = st.session_state.get(
        "username",
        ""
    )

    # Get the current role
    role = st.session_state.get(
        "role",
        ""
    )

    # If the user does not exist,
    # deny access
    if username not in users:
        return False

    # Questions are available to everyone
    if permission == "questions":
        return True

    # --------------------------------------------------
    # CHECK CUSTOM USER PERMISSIONS
    # --------------------------------------------------

    # If the Administrator has changed
    # this user's permissions, use them.
    if username in user_permissions:

        return permission in user_permissions[username]

    # --------------------------------------------------
    # USE NORMAL ROLE PERMISSIONS
    # --------------------------------------------------

    if role not in permissions:
        return False

    return permission in permissions[role]
