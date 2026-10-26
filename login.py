
import streamlit as st
import os
import base64


# --------------------------------------------------
# BACKGROUND IMAGE AND TEXT STYLING
# --------------------------------------------------

def find_image_path(filename):

    possible_paths = [
        filename,
        os.path.join("data", filename)
    ]

    for path in possible_paths:
        if os.path.isfile(path):
            return path

    return None


def set_login_background(image_file="khwezi_login.png"):

    path = find_image_path(image_file)

    if path is None:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #000000 !important;
            }

            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp p,
            .stApp label {
                color: #E6E6E6 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            "Background image not found. "
            "Save khwezi_login.png in the project folder "
            "or inside the data folder."
        )
        return

    try:
        with open(path, "rb") as image:
            encoded_image = base64.b64encode(
                image.read()
            ).decode("utf-8")

        st.markdown(
            f"""
            <style>

            /* Background image with dark overlay */
            .stApp {{
                background-image:
                    linear-gradient(
                        rgba(0, 0, 0, 0.78),
                        rgba(0, 0, 0, 0.78)
                    ),
                    url("data:image/png;base64,{encoded_image}");

                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: #E6E6E6 !important;
            }}

            /* Headings */
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp h4 {{
                color: #E6E6E6 !important;
                font-weight: 800 !important;
                text-shadow: 1px 1px 3px #000000;
            }}

            /* General text and labels */
            .stApp p,
            .stApp label,
            .stApp [data-testid="stMarkdownContainer"] {{
                color: #E6E6E6 !important;
                font-weight: 600 !important;
            }}

            /* Login input fields */
            .stTextInput input {{
                background-color: rgba(15, 15, 15, 0.90) !important;
                color: #E6E6E6 !important;
                border: 1px solid #888888 !important;
                border-radius: 6px;
            }}

            /* Input placeholder text */
            .stTextInput input::placeholder {{
                color: #BBBBBB !important;
            }}

            /* Login and other buttons */
            .stButton button {{
                background-color: rgba(25, 25, 25, 0.95) !important;
                color: #E6E6E6 !important;
                border: 1px solid #888888 !important;
                border-radius: 8px;
                font-weight: 700 !important;
            }}

            .stButton button:hover {{
                background-color: rgba(55, 55, 55, 0.98) !important;
                border: 1px solid #FFFFFF !important;
            }}

            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: #101010 !important;
            }}

            [data-testid="stSidebar"] * {{
                color: #E6E6E6 !important;
            }}

            /* Alerts */
            [data-testid="stAlert"] p {{
                color: #E6E6E6 !important;
            }}

            /* Dividers */
            hr {{
                border-color: rgba(230, 230, 230, 0.45) !important;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    except OSError as error:
        st.error(f"Could not load the login background image: {error}")


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

    "maintenance": {
        "password": "maintenance123",
        "role": "Maintenance Engineer"
    },

    "worker": {
        "password": "worker123",
        "role": "Worker"
    }
}


# --------------------------------------------------
# EXISTING ROLE PERMISSIONS
# DO NOT CHANGE THESE PERMISSIONS
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

    # Apply background when the login page is displayed
    set_login_background()

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

    # Check for administrator changes
    if username in user_permissions:
        return permission in user_permissions[username]

    # Otherwise use the original role permissions
    if role not in permissions:
        return False

    return permission in permissions[role]
