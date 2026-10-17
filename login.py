
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
        "incidents",
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
# DEMONSTRATION USER ACCOUNTS
# These accounts are for prototype testing.
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
# These names may be imported by user_management.py.
# --------------------------------------------------

users = USERS
permissions = ROLE_PERMISSIONS

# Temporary individual permission overrides.
user_permissions = {}

# List of available page permissions.
available_permissions = sorted({
    permission
    for role_pages in ROLE_PERMISSIONS.values()
    for permission in role_pages
})


# --------------------------------------------------
# SESSION STATE
# Stores the user's login information.
# --------------------------------------------------

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = ""


# --------------------------------------------------
# LOGIN BACKGROUND IMAGE
# Looks for khwezi_login.png beside login.py
# or inside the data folder.
# --------------------------------------------------

def show_login_background():

    # Find the folder containing this Python file.
    project_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    # Check both possible image locations.
    image_paths = [
        os.path.join(project_folder, "khwezi_login.png"),
        os.path.join(project_folder, "data", "khwezi_login.png"),
    ]

    image_path = None

    # Find the first existing image.
    for path in image_paths:
        if os.path.isfile(path):
            image_path = path
            break

    # Display a fallback background if the image is missing.
    if image_path is None:

        st.markdown(
            """
            <style>
            [data-testid="stAppViewContainer"] {
                background-color: #10243A;
            }

            [data-testid="stHeader"] {
                background: transparent;
            }

            [data-testid="stMain"] {
                background: transparent;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        st.warning(
            "Background image not found. "
            "Upload khwezi_login.png beside app.py and login.py."
        )

        return

    # Read the image and convert it to Base64.
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        encoded_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

    except OSError as error:
        st.error(f"Could not read the background image: {error}")
        return

    # Apply the background image and login styling.
    background_css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image:
            linear-gradient(
                rgba(5, 18, 35, 0.25),
                rgba(5, 18, 35, 0.45)
            ),
            url("data:image/png;base64,{encoded_image}");

        background-size: cover;
        background-position: center center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stHeader"] {{
        background: transparent;
    }}

    [data-testid="stMain"] {{
        background: transparent;
    }}

    .block-container {{
        padding-top: 2rem;
        padding-bottom: 2rem;
    }}

    /* Make login inputs readable. */
    div[data-testid="stTextInput"] input {{
        background-color: white;
        color: #10243A;
        border-radius: 6px;
    }}

    /* Style the login button. */
    div[data-testid="stFormSubmitButton"] button {{
        background-color: #D6A62E;
        color: #10243A;
        font-weight: bold;
        border: none;
        border-radius: 6px;
        min-height: 45px;
    }}

    div[data-testid="stFormSubmitButton"] button:hover {{
        background-color: #F0C75E;
        color: #10243A;
    }}
    </style>
    """

    st.markdown(
        background_css,
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# LOGIN FUNCTION
# The requested branding text has been removed.
# --------------------------------------------------

def login():

    # Display the background image.
    show_login_background()

    # Centre the login form.
    left_column, centre_column, right_column = st.columns(
        [1, 1.1, 1]
    )

    with centre_column:

        # Display only the login heading.
        st.markdown(
            """
            <h2 style="color:white; text-align:center;">
                Login
            </h2>
            """,
            unsafe_allow_html=True,
        )

        # Create the username and password form.
        with st.form("khwezi_login_form"):

            st.subheader("Sign in to your account")

            username = st.text_input(
                "Username",
                placeholder="Enter your username",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
            )

            submitted = st.form_submit_button(
                "Login",
                use_container_width=True,
            )

        # Check the credentials after the form is submitted.
        if submitted:

            username = username.strip()

            if not username or not password:
                st.error(
                    "Please enter your username and password."
                )

            elif username not in USERS:
                st.error("Invalid username or password.")

            elif USERS[username].get("blocked", False):
                st.error(
                    "This account is blocked. "
                    "Contact the administrator."
                )

            elif USERS[username]["password"] != password:
                st.error("Invalid username or password.")

            else:
                # Save the successful login information.
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = USERS[username]["role"]

                # Refresh the app after successful login.
                st.rerun()


# --------------------------------------------------
# PERMISSION CHECKING
# --------------------------------------------------

def has_permission(permission):

    # The user must be logged in.
    if not st.session_state.get("logged_in", False):
        return False

    username = st.session_state.get("username", "")

    # Check that the account exists.
    if username not in USERS:
        return False

    # Block access for blocked accounts.
    if USERS[username].get("blocked", False):
        return False

    role = st.session_state.get("role", "")

    # All logged-in users can access Questions.
    if permission == "questions":
        return True

    # Check the permissions assigned to the user's role.
    allowed_pages = ROLE_PERMISSIONS.get(role, [])

    # Check optional individual permission overrides.
    individual_permissions = user_permissions.get(
        username,
        {},
    )

    return (
        permission in allowed_pages
        or individual_permissions.get(permission, False)
    )


# --------------------------------------------------
# LOGOUT FUNCTION
# --------------------------------------------------

def logout():

    # Clear the current user's session information.
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

    # Return the user to the login page.
    st.rerun()
