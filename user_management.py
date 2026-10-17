
import streamlit as st
import os
import base64


# --------------------------------------------------
# ROLE PERMISSIONS
# --------------------------------------------------

ROLE_PERMISSIONS = {
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
        "incidents",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports",
        "questions"
    ],

    "Maintenance Engineer": [
        "dashboard",
        "equipment",
        "maintenance",
        "reports",
        "questions"
    ],

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
# USERS
# --------------------------------------------------

USERS = {
    "admin": {
        "password": "admin123",
        "role": "Administrator",
        "blocked": False
    },

    "safety": {
        "password": "safety123",
        "role": "Safety Officer",
        "blocked": False
    },

    "mining": {
        "password": "mining123",
        "role": "Mining Engineer",
        "blocked": False
    },

    "maintenance": {
        "password": "maintenance123",
        "role": "Maintenance Engineer",
        "blocked": False
    },

    "manager": {
        "password": "manager123",
        "role": "Manager",
        "blocked": False
    }
}


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = ""


# --------------------------------------------------
# LOGIN BACKGROUND IMAGE
# --------------------------------------------------

def show_login_background():

    # Look for the login image in the project folder
    # or in the data folder.
    image_paths = [
        "khwezi_login.png",
        os.path.join("data", "khwezi_login.png")
    ]

    image_path = None

    for path in image_paths:
        if os.path.exists(path):
            image_path = path
            break

    # Display the background image when available.
    if image_path:

        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(
                image_file.read()
            ).decode()

        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image:
                    url("data:image/png;base64,{encoded_image}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}

            .login-container {{
                background-color: rgba(255, 255, 255, 0.96);
                padding: 30px;
                border-radius: 10px;
                max-width: 450px;
                margin: auto;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    else:

        # Use a plain background if the image is missing.
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #0B1F33;
            }
            </style>
            """,
            unsafe_allow_html=True
        )


# --------------------------------------------------
# LOGIN FUNCTION
# --------------------------------------------------

def login():

    show_login_background()

    # Centre the login form on the page.
    left, middle, right = st.columns([1, 1.5, 1])

    with middle:

        with st.form("login_form"):

            username = st.text_input("Username")

            password = st.text_input(
                "Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        if submitted:

            # Check whether the username exists.
            if username in USERS:

                user = USERS[username]

                # Prevent blocked accounts from logging in.
                if user.get("blocked", False):

                    st.error(
                        "Your account has been blocked. "
                        "Please contact the Administrator."
                    )

                # Verify the password.
                elif password == user["password"]:

                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["role"] = user["role"]

                    st.success("Login successful!")

                    st.rerun()

                else:

                    st.error("Incorrect password.")

            else:

                st.error("Username does not exist.")


# --------------------------------------------------
# CHECK USER PERMISSIONS
# --------------------------------------------------

def has_permission(permission):

    # The user must be logged in.
    if not st.session_state.get("logged_in", False):
        return False

    username = st.session_state.get("username", "")

    # Check that the account exists.
    if username not in USERS:
        return False

    user = USERS[username]

    # Blocked users cannot access pages.
    if user.get("blocked", False):
        return False

    # Questions are available to every logged-in user.
    if permission == "questions":
        return True

    # Get the user's role.
    role = user.get("role", "")

    # Check whether the role has permission for the page.
    return permission in ROLE_PERMISSIONS.get(role, [])


# --------------------------------------------------
# LOGOUT FUNCTION
# --------------------------------------------------

def logout():

    # Clear the current user's login information.
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

    st.rerun()
