import streamlit as st

# Users
users = {"admin": {"password": "admin123", "role": "Administrator"},
         "safety": {"password": "safety123", "role": "Safety Officer"},
         "mining": {"password": "mining123", "role": "Mining Engineer"},
         "maintenance": {"password": "maintenance123", "role": "Maintenance Engineer"},
         "manager": {"password": "manager123","role": "Manager"}}

user_permissions = {}

# Role Permissions

permissions = {"Administrator": ["dashboard", "worker_health", "incidents", "equipment", "maintenance", "risk_assessment", "reports", "questions", "manage_users"],
               "Safety Officer": ["dashboard", "worker_health", "incidents", "risk_assessment", "reports", "questions"],
               "Mining Engineer":["dashboard", "worker_health", "incidents","equipment", "maintenance", "risk_assessment", "reports", "questions"],
               "Maintenance Engineer": ["dashboard", "equipment", "maintenance",  "reports", "questions"],
               "Manager": ["dashboard", "worker_health", "incidents","equipment", "maintenance", "risk_assessment", "reports", "questions"]}

# Login

def login():

    # Display the application title
    st.title("Khwezi Mining Monitoring System")

    # Display login heading
    st.subheader("Login")

    # Ask for username
    username = st.text_input("Username", key="login_username")

    # Ask for password
    password = st.text_input("Password", type="password", key="login_password")

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

# Logout

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

# Permission check

def has_permission(permission):

    # Get the current username
    username = st.session_state.get("username", "")

    # Get the current role
    role = st.session_state.get("role", "")

    # Check User
    if username not in users:

        return False

    # Questions are available to everyone.

    if permission == "questions":

        return True


    # Custom user permissions
    # If the Administrator has changed the permissions
    # for this specific user, use those permissions.

    if username in user_permissions:

        return permission in user_permissions[username]

    # Role permissions
    # If there are no custom permissions,
    # use the user's normal role permissions.

    if role not in permissions:

        return False


    return permission in permissions[role]
