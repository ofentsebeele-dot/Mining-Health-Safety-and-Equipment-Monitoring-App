
import streamlit as st


# --------------------------------------------------
# USERS
# --------------------------------------------------
# These are the users who can log into the system.

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
    }
}


# --------------------------------------------------
# ROLE PERMISSIONS
# --------------------------------------------------
# These are the permissions for each role.
#
# Questions are available to all users.
#
# The permissions can also be changed for an
# individual user by the Administrator.

permissions = {

    # --------------------------------------------------
    # ADMINISTRATOR
    # --------------------------------------------------

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


    # --------------------------------------------------
    # SAFETY OFFICER
    # --------------------------------------------------

    "Safety Officer": [
        "dashboard",
        "worker_health",
        "incidents",
        "risk_assessment",
        "reports",
        "questions"
    ],


    # --------------------------------------------------
    # MINING ENGINEER
    # --------------------------------------------------

    "Mining Engineer": [
        "dashboard",
        "worker_health",
        "maintenance",
        "risk_assessment",
        "questions"
    ],


    # --------------------------------------------------
    # MAINTENANCE ENGINEER
    # --------------------------------------------------

    "Maintenance Engineer": [
        "dashboard",
        "worker_health",
        "equipment",
        "maintenance",
        "risk_assessment",
        "questions"
    ],


    # --------------------------------------------------
    # MANAGER
    # --------------------------------------------------

    "Manager": [
        "dashboard",
        "worker_health",
        "incidents",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports",
        "questions"
    ]
}


# --------------------------------------------------
# USER-SPECIFIC PERMISSIONS
# --------------------------------------------------
# This dictionary stores permission changes made
# by the Administrator for individual users.
#
# It starts empty.
#
# Example:
#
# user_permissions["mining"] = [
#     "dashboard",
#     "worker_health",
#     "equipment",
#     "maintenance",
#     "risk_assessment",
#     "questions"
# ]
#
# This would give the mining engineer exactly
# those permissions.

user_permissions = {}


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

def login():

    # Display the application title
    st.title("Khwezi Mining Monitoring System")

    # Display login heading
    st.subheader("Login")

    # Ask for username
    username = st.text_input(
        "Username",
        key="login_username"
    )

    # Ask for password
    password = st.text_input(
        "Password",
        type="password",
        key="login_password"
    )

    # Login button
    if st.button("Login"):

        # Check whether the username exists
        if username in users:

            # Check whether the password is correct
            if users[username]["password"] == password:

                # Store login status
                st.session_state["logged_in"] = True

                # Store username
                st.session_state["username"] = username

                # Store user's role
                st.session_state["role"] = users[username]["role"]

                # Display success message
                st.success("Login successful.")

                # Reload the application
                st.rerun()

            else:

                # Password is incorrect
                st.error("Incorrect password.")

        else:

            # Username does not exist
            st.error("Username not found.")


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

def logout():

    # Display logout button in the sidebar
    if st.sidebar.button("Logout"):

        # Clear login status
        st.session_state["logged_in"] = False

        # Clear username
        st.session_state["username"] = ""

        # Clear role
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

    # --------------------------------------------------
    # CHECK USER
    # --------------------------------------------------
    # If the username does not exist,
    # access is denied.

    if username not in users:

        return False


    # --------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------
    # Questions are available to everyone.

    if permission == "questions":

        return True


    # --------------------------------------------------
    # CUSTOM USER PERMISSIONS
    # --------------------------------------------------
    # If the Administrator has changed the permissions
    # for this specific user, use those permissions.

    if username in user_permissions:

        return permission in user_permissions[username]


    # --------------------------------------------------
    # ROLE PERMISSIONS
    # --------------------------------------------------
    # If there are no custom permissions,
    # use the user's normal role permissions.

    if role not in permissions:

        return False


    return permission in permissions[role]
```
