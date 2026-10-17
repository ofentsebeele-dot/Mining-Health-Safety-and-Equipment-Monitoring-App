
import streamlit as st
import os
import base64


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
# Configure the browser tab and page layout.
st.set_page_config(
    page_title="Khwezi Mining Monitoring System",
    page_icon="⛏️",
    layout="wide"
)


# --------------------------------------------------
# ROLE PERMISSIONS
# --------------------------------------------------
# These permissions control which pages each role can access.
# Questions are available to every logged-in user.

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
# DEMONSTRATION USER ACCOUNTS
# --------------------------------------------------
# These accounts are for prototype testing.
# Change the passwords before using the application
# in a real environment.

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
# INITIALISE SESSION STATE
# --------------------------------------------------
# Session state keeps the user logged in while navigating
# between pages during the current Streamlit session.

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = ""


# --------------------------------------------------
# LOAD THE LOGIN BACKGROUND IMAGE
# --------------------------------------------------
def show_login_background():
    """
    Display the Khwezi Mining background image behind
    the login page.

    The image must be named khwezi_login.png and placed
    in the project root or inside the data folder.
    """

    # Look for the image in the main project folder first.
    possible_paths = [
        "khwezi_login.png",
        os.path.join("data", "khwezi_login.png")
    ]

    image_path = None

    for path in possible_paths:
        if os.path.exists(path):
            image_path = path
            break

    # Apply the background image if the file exists.
    if image_path:
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(
                image_file.read()
            ).decode()

        background_css = f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(5, 18, 35, 0.65),
                    rgba(5, 18, 35, 0.80)
                ),
                url("data:image/png;base64,{encoded_image}");

            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        /* Make the login content readable. */
        .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
        }}

        /* Style the input fields. */
        div[data-testid="stTextInput"] input {{
            background-color: white;
            color: #10243A;
            border-radius: 6px;
        }}

        /* Style the login button. */
        div[data-testid="stFormSubmitButton"] button {{
            background-color: #D6A62E;
            color: #10243A;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            width: 100%;
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
            unsafe_allow_html=True
        )

    else:
        # Use a dark background if the image is missing.
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #10243A;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.warning(
            "Background image not found. "
            "Upload khwezi_login.png to your project folder."
        )


# --------------------------------------------------
# LOGIN FUNCTION
# --------------------------------------------------
def login():

    # Show the mining background image.
    show_login_background()

    # Create space above the login form.
    st.markdown("<br>", unsafe_allow_html=True)

    # Divide the page into three columns so the login
    # form appears in the centre of the page.
    left_column, centre_column, right_column = st.columns(
        [1, 1.1, 1]
    )

    with centre_column:

        # This is the actual text displayed above the form.
        st.markdown(
            """
            <div style="
                background-color: rgba(10, 27, 48, 0.92);
                padding: 25px;
                border-radius: 12px;
                text-align: center;
                border: 1px solid rgba(214, 166, 46, 0.8);
            ">
                <h1 style="
                    color: #F0C75E;
                    margin-bottom: 5px;
                    font-size: 30px;
                ">
                    KHWEZI MINING
                </h1>

                <h3 style="
                    color: white;
                    margin-top: 0;
                ">
                    Monitoring System
                </h3>

                <p style="
                    color: #E4EAF1;
                    font-size: 14px;
                ">
                    Health, Safety and Equipment Monitoring
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        # The login fields are functional Streamlit inputs.
        # They are not part of the background picture.
        with st.form("khwezi_login_form"):

            st.subheader("Sign in")

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

                # Check that both fields have been completed.
                if not username.strip() or not password:
                    st.error(
                        "Please enter your username and password."
                    )

                # Check whether the username exists.
                elif username not in USERS:
                    st.error("Invalid username or password.")

                # Check whether the account is blocked.
                elif USERS[username].get("blocked", False):
                    st.error(
                        "This account is blocked. "
                        "Contact your system administrator."
                    )

                # Check the password.
                elif USERS[username]["password"] != password:
                    st.error("Invalid username or password.")

                else:
                    # Save the successful login details.
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["role"] = USERS[username]["role"]

                    st.success("Login successful!")

                    # Refresh the application to show the dashboard.
                    st.rerun()


# --------------------------------------------------
# PERMISSION CHECK FUNCTION
# --------------------------------------------------
def has_permission(permission):
    """
    Return True if the logged-in user's role allows
    access to the requested page.
    """

    # A user must be logged in first.
    if not st.session_state.get("logged_in", False):
        return False

    username = st.session_state.get("username", "")

    # Confirm that the account still exists.
    if username not in USERS:
        return False

    # Block access if the account has been blocked.
    if USERS[username].get("blocked", False):
        return False

    role = st.session_state.get("role", "")

    # Questions are available to all logged-in users.
    if permission == "questions":
        return True

    # Check the permissions assigned to the user's role.
    return permission in ROLE_PERMISSIONS.get(role, [])


# --------------------------------------------------
# LOGOUT FUNCTION
# --------------------------------------------------
def logout():
    """
    Log out the current user and return to the login page.
    """

    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

    # Refresh the app to display the login page.
    st.rerun()
