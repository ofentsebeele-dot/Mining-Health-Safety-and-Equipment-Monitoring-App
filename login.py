
import streamlit as st


# --------------------------------------------------
# USERS
# --------------------------------------------------

users = {

    # Administrator
    "admin": {
        "password": "admin123",
        "role": "Administrator"
    },

    # Safety Officer
    "safety": {
        "password": "safety123",
        "role": "Safety Officer"
    },

    # Mining Engineer
    "mining": {
        "password": "mining123",
        "role": "Mining Engineer"
    },

    # Maintenance Engineer
    "maintenance": {
        "password": "maintenance123",
        "role": "Maintenance Engineer"
    },

    # Manager
    "manager": {
        "password": "manager123",
        "role": "Manager"
    },

    # Worker
    "worker": {
        "password": "worker123",
        "role": "Worker"
    }
}


# --------------------------------------------------
# ROLE PERMISSIONS
# --------------------------------------------------
# These permissions control which pages each role
# can access.
#
# Questions are available to everyone.
# --------------------------------------------------

permissions = {

    # --------------------------------------------------
    # ADMINISTRATOR
    # --------------------------------------------------

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


    # --------------------------------------------------
    # SAFETY OFFICER
    # --------------------------------------------------

    "Safety Officer": [
        "dashboard",
        "worker_health",
        "incidents",
        "risk_assessment",
        "reports",
        "questions"
    ],


    # --------------------------------------------------
    # MINING ENGINEER
    # --------------------------------------------------

    "Mining Engineer": [
        "dashboard",
        "worker_health",
        "maintenance",
        "risk_assessment",
        "questions"
    ],


    # --------------------------------------------------
    # MAINTENANCE ENGINEER
    # --------------------------------------------------

    "Maintenance Engineer": [
        "dashboard",
        "worker_health",
        "incidents",
        "equipment",
        "maintenance",
        "risk_assessment",
        "reports",
        "questions"
    ],


    # --------------------------------------------------
    # MANAGER
    # --------------------------------------------------

    "Manager": [
        "dashboard",
        "worker_health",
        "incidents",
        "maintenance",
        "reports",
        "questions"
    ],


    # --------------------------------------------------
    # WORKER
    # --------------------------------------------------

    "Worker": [
        "dashboard",
        "worker_health",
        "questions"
    ]
}


# --------------------------------------------------
# USER-SPECIFIC PERMISSION CHANGES
# --------------------------------------------------
# The Administrator can use the User Management page
# to give a specific user additional permissions.
#
# This starts empty, so users use their normal
# role permissions above.

user_permissions = {}


# --------------------------------------------------
# LOGIN
# --------------------------------------------------

def login():

    # --------------------------------------------------
    # LOGIN PAGE DESIGN
    # --------------------------------------------------

    st.markdown(
        """
        <style>

        .stApp {
            background:
                linear-gradient(
                    135deg,
                    #111827 0%,
                    #1f2937 50%,
                    #111827 100%
                );
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

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

        .login-title {
            text-align: center;
            color: #111827;
            font-size: 30px;
            font-weight: 800;
            margin-bottom: 5px;
        }

        .login-subtitle {
            text-align: center;
            color: #6b7280;
            font-size: 15px;
            margin-bottom: 30px;
        }

        label {
            color: #374151 !important;
            font-weight: 600 !important;
        }

        div[data-baseweb="input"] {
            border-radius: 10px;
        }

        div[data-baseweb="input"] input {
            font-size: 15px;
        }

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

        div.stButton > button:hover {
            transform: translateY(-2px);
            box-shadow:
                0 8px 20px
                rgba(245, 158, 11, 0.35);
        }

        .login-footer {
            text-align: center;
            color: #d1d5db;
            font-size: 12px;
            margin-top: 25px;
        }

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
    # LOGIN FORM
    # --------------------------------------------------

    left, center, right = st.columns([1, 2, 1])

    with center:

        # Username
        username = st.text_input(
            "Username",
            key="login_username"
        )

        # Password
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

            # Check if username exists
            if username in users:

                # Check password
                if users[username]["password"] == password:

                    # Save login status
                    st.session_state["logged_in"] = True

                    # Save username
                    st.session_state["username"] = username

                    # Save role
                    st.session_state["role"] = users[username]["role"]

                    # Display success message
                    st.success(
                        "Login successful."
                    )

                    # Reload the application
                    st.rerun()

                else:

                    # Incorrect password
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

    # Display logout button
    if st.sidebar.button("Logout"):

        # Clear login information
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["role"] = ""

        # Reload application
        st.rerun()


# --------------------------------------------------
# PERMISSION CHECK
# --------------------------------------------------

def has_permission(permission):

    # Get current username
    username = st.session_state.get(
        "username",
        ""
    )

    # Get current role
    role = st.session_state.get(
        "role",
        ""
    )


    # User must exist
    if username not in users:
        return False


    # Questions are available to everyone
    if permission == "questions":
        return True


    # --------------------------------------------------
    # CHECK CUSTOM USER PERMISSIONS
    # --------------------------------------------------
    # If the Administrator changed the permissions
    # for this specific user, use those permissions.

    if username in user_permissions:

        return permission in user_permissions[username]


    # --------------------------------------------------
    # USE ROLE PERMISSIONS
    # --------------------------------------------------

    if role not in permissions:
        return False


    return permission in permissions[role]
