
import streamlit as st
import os
import base64

# ============================================================
# KHWEZI MINING MONITORING SYSTEM
# LOGIN AND PERMISSIONS
# ============================================================

# Demo users for the project.
# For a real production system, use secure password hashing
# and store accounts in a protected database.
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

# Stores permission overrides for individual users during
# the current application session.
user_permissions = {}

# Default permissions for each role.
permissions = {
    "Administrator": [
        "dashboard", "worker_health", "incidents",
        "equipment", "maintenance", "risk_assessment",
        "reports", "questions", "manage_users"
    ],

    "Safety Officer": [
        "dashboard", "worker_health", "incidents",
        "risk_assessment", "reports", "questions"
    ],

    "Mining Engineer": [
        "dashboard", "worker_health", "incidents",
        "equipment", "maintenance", "risk_assessment",
        "reports", "questions"
    ],

    "Maintenance Engineer": [
        "dashboard", "equipment", "maintenance",
        "reports", "questions"
    ],

    "Manager": [
        "dashboard", "worker_health", "incidents",
        "equipment", "maintenance", "risk_assessment",
        "reports", "questions"
    ]
}


# ============================================================
# BACKGROUND IMAGE
# ============================================================

def show_login_background():
    """
    Display the uploaded mining picture behind the login page.

    Upload the image to the main GitHub repository folder
    and name it khwezi_login.png.
    """

    image_path = "khwezi_login.png"

    # Also support an image stored inside the data folder.
    if not os.path.isfile(image_path):
        image_path = os.path.join("data", "khwezi_login.png")

    # Use a plain dark background if the image is missing.
    if not os.path.isfile(image_path):
        st.markdown(
            """
            <style>
            .stApp {
                background: linear-gradient(
                    135deg, #071525, #132a40
                );
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        return

    # Read the image and convert it to a format usable by CSS.
    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    # Apply the image as the page background.
    # A dark overlay helps keep the actual login form readable.
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image:
                linear-gradient(
                    rgba(4, 13, 26, 0.48),
                    rgba(4, 13, 26, 0.70)
                ),
                url("data:image/png;base64,{image_data}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}

        [data-testid="stMainBlockContainer"] {{
            max-width: 850px;
            padding-top: 2rem;
        }}

        [data-testid="stHeader"] {{
            background: transparent;
        }}

        .login-heading {{
            text-align: center;
            color: white;
            font-size: 36px;
            font-weight: 800;
            margin-bottom: 5px;
        }}

        .login-subheading {{
            text-align: center;
            color: #ffc107;
            font-size: 16px;
            letter-spacing: 3px;
            font-weight: 700;
            margin-bottom: 24px;
        }}

        .login-description {{
            text-align: center;
            color: #e0e8f4;
            font-size: 15px;
            margin-bottom: 25px;
        }}

        [data-testid="stForm"],
        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background: rgba(5, 18, 33, 0.91);
            border: 1px solid rgba(255, 193, 7, 0.35);
            border-radius: 16px;
            padding: 22px;
        }}

        [data-testid="stWidgetLabel"] p {{
            color: #f1f5f9;
            font-weight: 600;
        }}

        div[data-baseweb="input"] {{
            background-color: #15283d;
            border: 1px solid #53657b;
            border-radius: 8px;
        }}

        div[data-baseweb="input"] input {{
            color: white;
        }}

        div[data-testid="stFormSubmitButton"] button,
        div.stButton > button {{
            background: #ffb800;
            color: #101820;
            border: none;
            border-radius: 8px;
            min-height: 45px;
            font-weight: 700;
            width: 100%;
        }}

        div[data-testid="stFormSubmitButton"] button:hover,
        div.stButton > button:hover {{
            background: #ffd04a;
            color: #101820;
            border: none;
        }}

        .login-footer {{
            color: #e0e8f4;
            text-align: center;
            font-size: 13px;
            margin-top: 25px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# LOGIN FUNCTION
# ============================================================

def login():

    # Apply the background before displaying the login controls.
    show_login_background()

    # Application heading.
    st.markdown(
        '<div class="login-heading">KHWEZI MINING</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-subheading">'
        'MONITORING SYSTEM</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="login-description">'
        'Worker safety • Equipment monitoring • Risk management'
        '</div>',
        unsafe_allow_html=True
    )

    # Center the login form on the page.
    left, centre, right = st.columns([1, 2, 1])

    with centre:

        st.markdown("### Welcome Back")

        st.write(
            "Sign in with your account to access the "
            "Khwezi Mining Monitoring System."
        )

        # A form allows the user to submit both fields together.
        with st.form("khwezi_login_form"):

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

        # Check the credentials only after the form is submitted.
        if submitted:

            username = username.strip()

            if not username or not password:
                st.error("Please enter your username and password.")

            elif username in users and users[username]["password"] == password:

                # Save the authenticated user's details.
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = users[username]["role"]

                st.success("Login successful.")

                # Return to app.py so the dashboard can load.
                st.rerun()

            else:
                st.error("Incorrect username or password.")

    # Footer text.
    st.markdown(
        '<div class="login-footer">'
        'Safer People • Smarter Equipment • Better Decisions'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# LOGOUT FUNCTION
# ============================================================

def logout():

    if st.sidebar.button("Logout"):

        # Clear the active user's session.
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["role"] = ""

        # Remove login form values when logging out.
        st.session_state.pop("login_username", None)
        st.session_state.pop("login_password", None)

        st.rerun()


# ============================================================
# PERMISSION CHECK
# ============================================================

def has_permission(permission):

    # Read the current user's session information.
    username = st.session_state.get("username", "")
    role = st.session_state.get("role", "")

    # Unauthenticated users cannot access protected pages.
    if not st.session_state.get("logged_in", False):
        return False

    # Questions are available to every logged-in role.
    if permission == "questions":
        return True

    # Apply individual permission overrides if they exist.
    if username in user_permissions:
        return permission in user_permissions[username]

    # Otherwise, use the normal role permissions.
    if role not in permissions:
        return False

    return permission in permissions[role]
