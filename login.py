import streamlit as st


# Users and their roles
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


# Permissions for each role
permissions = {
    "Administrator": [
        "dashboard",
        "worker_health",
        "incidents",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports",
        "manage_users"
    ],

    "Safety Officer": [
        "dashboard",
        "worker_health",
        "incidents",
        "risk_assessment"
    ],

    "Mining Engineer": [
        "dashboard",
        "worker_health",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports"
    ],

    "Maintenance Engineer": [
        "dashboard",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports"
    ],

    "Manager": [
        "dashboard",
        "worker_health",
        "incidents",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports"
    ]
}


def login():

    st.title("Khwezi Mining")

    st.subheader(
        "Mining Health, Safety and Equipment Monitoring System"
    )

    st.write("Please enter your login details.")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username in users and users[username]["password"] == password:

            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = users[username]["role"]

            st.success("Login successful!")

            st.rerun()

        else:

            st.error("Invalid username or password.")


def logout():

    if st.button("Logout"):

        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["role"] = ""

        st.rerun()


def has_permission(permission):

    role = st.session_state.get("role")

    if role in permissions:

        return permission in permissions[role]

    return False
