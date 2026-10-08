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
# EXISTING ROLE PERMISSIONS
# --------------------------------------------------
# DO NOT CHANGE THESE PERMISSIONS.
# These are the original permissions you provided.

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

    "Worker": [
        "dashboard",
        "questions",
        "worker_health"
    ]
}


# --------------------------------------------------
# USER-SPECIFIC PERMISSION CHANGES
# --------------------------------------------------
# This dictionary stores changes made by the Administrator.
#
# It starts empty, meaning everyone uses their normal
# role permissions above.
#
# Example:
#
# user_permissions["worker"] = [
#     "dashboard",
#     "questions",
#     "worker_health",
#     "incidents"
# ]
#
# This would give the worker an extra permission.

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

        # Check whether the username exists
        if username in users:

            # Check the password
            if users[username]["password"] == password:

                # Save login information
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

    # Get the logged-in username
    username = st.session_state.get(
        "username",
        ""
    )

    # Get the logged-in user's role
    role = st.session_state.get(
        "role",
        ""
    )

    # If the user does not exist, deny access
    if username not in users:

        return False

    # Questions are available to everyone
    if permission == "questions":

        return True

    # --------------------------------------------------
    # CHECK FOR ADMINISTRATOR CHANGES
    # --------------------------------------------------
    # If the Administrator has created custom permissions
    # for this user, use those permissions.

    if username in user_permissions:

        return permission in user_permissions[username]

    # --------------------------------------------------
    # OTHERWISE USE THE ORIGINAL ROLE PERMISSIONS
    # --------------------------------------------------

    if role not in permissions:

        return False

    return permission in permissions[role]
