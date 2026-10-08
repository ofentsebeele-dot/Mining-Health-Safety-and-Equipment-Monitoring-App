import streamlit as st


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

    "worker": {
        "password": "worker123",
        "role": "Worker"
    }
}


# --------------------------------------------------
# EXISTING ROLE PERMISSIONS
# --------------------------------------------------
# DO NOT CHANGE THESE PERMISSIONS.
# These are the original permissions you provided.

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

    "Worker": [
        "dashboard",
        "questions",
        "worker_health"
    ]
}


# --------------------------------------------------
# USER-SPECIFIC PERMISSION CHANGES
# --------------------------------------------------
# This dictionary stores changes made by the Administrator.
#
# It starts empty, meaning everyone uses their normal
# role permissions above.

user_permissions = {}


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

def login():

    # --------------------------------------------------
    # LOGIN PAGE DESIGN
    # --------------------------------------------------
    # This CSS changes the appearance of the login page.
    # It does not change the login functionality.

    st.markdown(
        """
        <style>

        /* --------------------------------------------
           MAIN BACKGROUND
           -------------------------------------------- */

        .stApp {
            background:
                linear-gradient(
                    135deg,
                    #111827 0%,
                    #1f2937 50%,
                    #111827 100%
                );
        }


        /* --------------------------------------------
           REMOVE SOME DEFAULT TOP SPACE
           -------------------------------------------- */

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }


        /* --------------------------------------------
           LOGIN CARD
           -------------------------------------------- */

        .login-card {
            background: rgba(255, 255, 255, 0.97);
            padding: 40px 45px;
            border-radius: 20px;
            box-shadow:
                0 15px 40px rgba(0, 0, 0, 0.35);

            max-width: 480px;
            margin: 50px auto 0 auto;

            border-top: 6px solid #f59e0b;
        }


        /* --------------------------------------------
           MINING ICON
           -------------------------------------------- */

        .mining-logo {
            width: 85px;
            height: 85px;

            background: #f59e0b;

            border-radius: 50%;

            margin: 0 auto 20px auto;

            display: flex;
            align-items: center;
            justify-content: center;

            font-size: 40px;

            box-shadow:
                0 8px 20px rgba(0, 0, 0, 0.20);
        }


        /* --------------------------------------------
           LOGIN TITLE
           -------------------------------------------- */

        .login-title {
            text-align: center;

            color: #111827;

            font-size: 30px;

            font-weight: 800;

            margin-bottom: 5px;
        }


        /* --------------------------------------------
           LOGIN SUBTITLE
           -------------------------------------------- */

        .login-subtitle {
            text-align: center;

            color: #6b7280;

            font-size: 15px;

            margin-bottom: 30px;
        }


        /* --------------------------------------------
           INPUT LABELS
           -------------------------------------------- */

        label {
            color: #374151 !important;

            font-weight: 600 !important;
        }


        /* --------------------------------------------
           INPUT BOXES
           -------------------------------------------- */

        div[data-baseweb="input"] {
            border-radius: 10px;
        }


        div[data-baseweb="input"] input {
            font-size: 15px;
        }


        /* --------------------------------------------
           LOGIN BUTTON
           -------------------------------------------- */

        div.stButton > button {

            width: 100%;

            height: 48px;

            background:
                linear-gradient(
                    90deg,
                    #f59e0b,
                    #d97706
                );

            color: white;

            border: none;

            border-radius: 10px;

            font-size: 16px;

            font-weight: 700;

            transition:
                transform 0.2s ease,
                box-shadow 0.2s ease;
        }


        /* Button hover effect */

        div.stButton > button:hover {

            transform: translateY(-2px);

            box-shadow:
                0 8px 20px
                rgba(245, 158, 11, 0.35);
        }


        /* --------------------------------------------
           FOOTER
           -------------------------------------------- */

        .login-footer {

            text-align: center;

            color: #d1d5db;

            font-size: 12px;

            margin-top: 25px;
        }


        /* --------------------------------------------
           MINING WARNING STRIPE
           -------------------------------------------- */

        .mining-strip {

            height: 6px;

            background:
                repeating-linear-gradient(
                    45deg,
                    #f59e0b,
                    #f59e0b 15px,
                    #111827 15px,
                    #111827 30px
                );

            margin-top: 25px;

            border-radius: 3px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # LOGIN HEADER
    # --------------------------------------------------

    st.markdown(
        """
        <div class="login-card">

            <div class="mining-logo">
                ⛏️
            </div>

            <div class="login-title">
                Khwezi Mining
            </div>

            <div class="login-subtitle">
                Health, Safety & Equipment
                Monitoring System
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # LOGIN INPUT AREA
    # --------------------------------------------------
    # The columns keep the login form centred on the page.

    left, center, right = st.columns([1, 2, 1])

    with center:

        # Username input
        username = st.text_input(
            "Username",
            key="login_username"
        )

        # Password input
        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        # Login button
        if st.button(
            "Login",
            type="primary"
        ):

            # Check whether the username exists
            if username in users:

                # Check whether the password is correct
                if users[username]["password"] == password:

                    # Save login information
                    st.session_state["logged_in"] = True

                    st.session_state["username"] = username

                    st.session_state["role"] = users[username]["role"]


                    # Show successful login message
                    st.success(
                        "Login successful."
                    )


                    # Reload the application
                    st.rerun()

                else:

                    # Password is incorrect
                    st.error(
                        "Incorrect password."
                    )

            else:

                # Username does not exist
                st.error(
                    "Username not found."
                )


    # --------------------------------------------------
    # LOGIN FOOTER
    # --------------------------------------------------

    st.markdown(
        """
        <div class="login-footer">

            Khwezi Mining Monitoring System
            <br>

            Health • Safety • Equipment

        </div>

        <div class="mining-strip"></div>
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

def logout():

    # Display logout button in the sidebar
    if st.sidebar.button("Logout"):

        # Clear login information
        st.session_state["logged_in"] = False

        st.session_state["username"] = ""

        st.session_state["role"] = ""

        # Reload the application
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


    # If the user does not exist,
    # deny access
    if username not in users:

        return False


    # Questions are available to everyone
    if permission == "questions":

        return True


    # --------------------------------------------------
    # CHECK FOR ADMINISTRATOR CHANGES
    # --------------------------------------------------
    # If the Administrator has created
    # custom permissions for this user,
    # use those permissions.

    if username in user_permissions:

        return permission in user_permissions[username]


    # --------------------------------------------------
    # OTHERWISE USE ORIGINAL ROLE PERMISSIONS
    # --------------------------------------------------

    if role not in permissions:

        return False


    return permission in permissions[role]
