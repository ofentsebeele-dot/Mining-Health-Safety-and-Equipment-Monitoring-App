
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
# Demonstration accounts for the prototype.
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
# COMPATIBILITY VARIABLES
# These names may be used by user_management.py.
# --------------------------------------------------

# Lowercase alias for code expecting "users".
users = USERS

# Lowercase alias for code expecting "permissions".
permissions = ROLE_PERMISSIONS

# Stores optional per-user permission overrides.
user_permissions = {}

# List of available page permissions.
available_permissions = sorted({
    permission
    for role_pages in ROLE_PERMISSIONS.values()
    for permission in role_pages
})


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
# Looks for khwezi_login.png beside this file or
# inside the data folder.
# --------------------------------------------------

def show_login_background():

    current_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    image_paths = [
        os.path.join(
            current_folder,
            "khwezi_login.png"
        ),
        os.path.join(
            current_folder,
            "data",
            "khwezi_login.png"
        ),
    ]

    image_path = None

    for path in image_paths:
        if os.path.isfile(path):
            image_path = path
            break

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
                background: transparent;
            }}

            [data-testid="stMain"] {{
                background: transparent;
            }}

            [data-testid="stMainBlockContainer"] {{
                padding-top: 3rem;
            }}

            [data-testid="stForm"] {{
                background-color: rgba(255, 255, 255, 0.96);
                padding: 25px;
                border-radius: 12px;
                border: 1px solid #d5dce5;
            }}

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
# --------------------------------------------------

def login():

    show_login_background()

    # Centre the login form.
    left_column, middle_column, right_column = st.columns(
        [1, 1.2, 1]
    )

    with middle_column:

        # Login heading only; removed the requested text.
        st.markdown(
            "<h3 style='color:white; text-align:center;'>"
            "Login"
            "</h3>",
            unsafe_allow_html=True
        )

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

            elif USERS[username].get("blocked", False):
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

                # Refresh the app after login.
                st.rerun()


# --------------------------------------------------
# PERMISSION CHECK
# --------------------------------------------------

def has_permission(permission):

    if not st.session_state.get("logged_in", False):
        return False

    username = st.session_state.get("username", "")

    if username not in USERS:
        return False

    if USERS[username].get("blocked", False):
        return False

    role = st.session_state.get("role", "")

    # Questions are available to every logged-in user.
    if permission == "questions":
        return True

    allowed_pages = ROLE_PERMISSIONS.get(role, [])

    # Check role-based page access.
    if permission in allowed_pages:
        return True

    # Check optional individual permission overrides.
    individual_permissions = user_permissions.get(
        username,
        {}
    )

    return individual_permissions.get(permission, False)


# --------------------------------------------------
# LOGOUT FUNCTION
# --------------------------------------------------

def logout():

    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

    st.rerun()

