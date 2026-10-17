\
import streamlit as st
import os
import base64

# --------------------------------------------------
# ROLE PERMISSIONS
# Defines which pages each role can access.
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
        "manage_users",
    ],

    "Safety Officer": [
        "dashboard",
        "worker_health",
        "incidents",
        "risk_assessment",
        "reports",
        "questions",
    ],

    "Mining Engineer": [
        "dashboard",
        "worker_health",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports",
        "questions",
    ],

    "Maintenance Engineer": [
        "dashboard",
        "equipment",
        "maintenance",
        "reports",
        "questions",
    ],

    "Manager": [
        "dashboard",
        "worker_health",
        "incidents",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports",
        "questions",
    ],
}


# --------------------------------------------------
# USER ACCOUNTS
# These are demonstration accounts for the prototype.
# Passwords are stored as plain text, so use secure
# password hashing before deploying a real system.
# --------------------------------------------------

USERS = {
    "admin": {
        "password": "admin123",
        "role": "Administrator",
        "blocked": False,
    },

    "safety": {
        "password": "safety123",
        "role": "Safety Officer",
        "blocked": False,
    },

    "mining": {
        "password": "mining123",
        "role": "Mining Engineer",
        "blocked": False,
    },

    "maintenance": {
        "password": "maintenance123",
        "role": "Maintenance Engineer",
        "blocked": False,
    },

    "manager": {
        "password": "manager123",
        "role": "Manager",
        "blocked": False,
    },
}


# --------------------------------------------------
# SESSION STATE
# Stores the current user's login information.
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = ""


# --------------------------------------------------
# LOGIN BACKGROUND IMAGE
# Looks for khwezi_login.png in the main app folder
# or in the data folder.
# --------------------------------------------------

def show_login_background():

    # Find the folder containing this Python file.
    current_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    # Check the main folder first, then the data folder.
    image_paths = [
        os.path.join(current_folder, "khwezi_login.png"),
        os.path.join(current_folder, "data", "khwezi_login.png"),
    ]

    image_path = None

    for path in image_paths:
        if os.path.isfile(path):
            image_path = path
            break

    # Apply the background image when the file exists.
    if image_path:

        try:
            with open(image_path, "rb") as image_file:
                encoded_image = base64.b64encode(
                    image_file.read()
                ).decode("utf-8")

            background_css = f"""
            <style>
            [data-testid="stAppViewContainer"] {{
                background-image:
                    linear-gradient(
                        rgba(5, 15, 30, 0.35),
                        rgba(5, 15, 30, 0.55)
                    ),
                    url("data:image/png;base64,{encoded_image}");

                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}

            [data-testid="stHeader"] {{
                background: rgba(0, 0, 0, 0);
            }}

            [data-testid="stMain"] {{
                background: transparent;
            }}

            [data-testid="stMainBlockContainer"] {{
                padding-top: 3rem;
            }}

            /* Style the login form container. */
            [data-testid="stForm"] {{
                background-color: rgba(255, 255, 255, 0.96);
                padding: 25px;
                border-radius: 12px;
                border: 1px solid #d5dce5;
            }}

            /* Style the input fields. */
            input {{
                border-radius: 5px !important;
            }}

            /* Style the login button. */
            .stForm button {{
                background-color: #17365D;
                color: white;
                border: none;
                border-radius: 5px;
                width: 100%;
            }}

            .stForm button:hover {{
                background-color: #244A78;
                color: white;
            }}
            </style>
            """

            st.markdown(
                background_css,
                unsafe_allow_html=True
            )

        except Exception as error:
            st.error(
                f"Could not load the background image: {error}"
            )

    else:
        # Use a dark background if the image is missing.
        st.markdown(
            """
            <style>
            [data-testid="stAppViewContainer"] {
                background-color: #10243A;
            }

            [data-testid="stHeader"] {
                background: transparent;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            "Background image not found. "
            "Check that khwezi_login.png is in the app folder."
        )


# --------------------------------------------------
# LOGIN FUNCTION
# Displays the login form and checks the credentials.
# --------------------------------------------------

def login():

    # Display the background image.
    show_login_background()

    # Centre the login form on the page.
    left_column, middle_column, right_column = st.columns(
        [1, 1.2, 1]
    )

    with middle_column:

        # Only the login heading is displayed.
        st.markdown(
            "<h3 style='color:white; text-align:center;'>"
            "Login"
            "</h3>",
            unsafe_allow_html=True
        )

        # Collect the username and password.
        with st.form("login_form"):

            username = st.text_input(
                "Username",
                placeholder="Enter your username"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True
            )

        # Validate the entered credentials.
        if submitted:

            username = username.strip()

            if not username or not password:
                st.error(
                    "Please enter both your username and password."
                )

            elif username not in USERS:
                st.error(
                    "Invalid username or password."
                )

            elif USERS[username]["blocked"]:
                st.error(
                    "This account has been blocked. "
                    "Please contact the administrator."
                )

            elif USERS[username]["password"] != password:
                st.error(
                    "Invalid username or password."
                )

            else:
                # Save the user's login details.
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = USERS[username]["role"]

                # Refresh the app after a successful login.
                st.rerun()


# --------------------------------------------------
# PERMISSION CHECK
# Determines whether a user can access a page.
# --------------------------------------------------

def has_permission(permission):

    # The user must be logged in first.
    if not st.session_state.get("logged_in", False):
        return False

    username = st.session_state.get("username", "")

    # Confirm that the account exists and is not blocked.
    if username not in USERS:
        return False

    if USERS[username].get("blocked", False):
        return False

    role = st.session_state.get("role", "")

    # Questions are available to all logged-in users.
    if permission == "questions":
        return True

    # Check the permissions assigned to the user's role.
    allowed_pages = ROLE_PERMISSIONS.get(role, [])

    return permission in allowed_pages


# --------------------------------------------------
# LOGOUT FUNCTION
# Clears the current user's session and returns them
# to the login page.
# --------------------------------------------------

def logout():

    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

    st.rerun()
