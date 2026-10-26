
import streamlit as st
import os
import base64


# --------------------------------------------------
# BACKGROUND IMAGE AND FONT STYLING
# --------------------------------------------------

def set_login_background():

    image_path = "khwezi_login.png"

    if os.path.exists(image_path):

        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(
                image_file.read()
            ).decode()

        background_style = f"""
        <style>

        /* Main background image with dark overlay */
        .stApp {{
            background:
                linear-gradient(
                    rgba(0, 0, 0, 0.78),
                    rgba(0, 0, 0, 0.78)
                ),
                url("data:image/png;base64,{encoded_image}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: #E6E6E6;
        }}

        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            color: #E6E6E6 !important;
        }}

        /* General text and labels */
        .stApp p,
        .stApp label,
        .stApp [data-testid="stMarkdownContainer"],
        .stApp [data-testid="stCaptionContainer"] {{
            color: #E6E6E6 !important;
        }}

        /* Login input fields */
        .stTextInput input {{
            background-color: rgba(20, 20, 20, 0.90) !important;
            color: #F0F0F0 !important;
            border: 1px solid #777777 !important;
        }}

        /* Input placeholders */
        .stTextInput input::placeholder {{
            color: #BDBDBD !important;
        }}

        /* Login button */
        .stButton button {{
            background-color: rgba(35, 35, 35, 0.95) !important;
            color: #F0F0F0 !important;
            border: 1px solid #AAAAAA !important;
            border-radius: 8px;
            font-weight: bold;
        }}

        .stButton button:hover {{
            background-color: rgba(65, 65, 65, 0.98) !important;
            border: 1px solid #FFFFFF !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: #080808 !important;
        }}

        [data-testid="stSidebar"] * {{
            color: #E6E6E6 !important;
        }}

        /* Divider */
        hr {{
            border-color: #555555 !important;
        }}

        </style>
        """

        st.markdown(
            background_style,
            unsafe_allow_html=True
        )

    else:
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #000000;
                color: #E6E6E6;
            }
            h1, h2, h3, p, label {
                color: #E6E6E6 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            "Background image not found. "
            "Please place khwezi_login.png in your project folder."
        )


# Apply styling
set_login_background()


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
