import streamlit as st

# --------------------------------------------------
# LOGIN
# --------------------------------------------------

def login():

    # --------------------------------------------------
    # PAGE STYLING
    # --------------------------------------------------

    st.markdown(
        """
        <style>

        /* Main application background */
        .stApp {
            background:
                linear-gradient(
                    135deg,
                    #111827 0%,
                    #1f2937 50%,
                    #111827 100%
                );
        }

        /* Remove unnecessary top spacing */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        /* Login card */
        .login-card {
            background: rgba(255, 255, 255, 0.97);
            padding: 45px 45px 40px 45px;
            border-radius: 20px;
            box-shadow:
                0 15px 40px rgba(0, 0, 0, 0.35);
            max-width: 480px;
            margin: 50px auto 0 auto;
            border-top: 6px solid #f59e0b;
        }

        /* Logo circle */
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

        /* Main title */
        .login-title {
            text-align: center;
            color: #111827;
            font-size: 30px;
            font-weight: 800;
            margin-bottom: 5px;
        }

        /* Subtitle */
        .login-subtitle {
            text-align: center;
            color: #6b7280;
            font-size: 15px;
            margin-bottom: 30px;
        }

        /* Input labels */
        label {
            color: #374151 !important;
            font-weight: 600 !important;
        }

        /* Input boxes */
        div[data-baseweb="input"] {
            border-radius: 10px;
        }

        div[data-baseweb="input"] input {
            font-size: 15px;
        }

        /* Login button */
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

        /* Login button hover effect */
        div.stButton > button:hover {
            transform: translateY(-2px);

            box-shadow:
                0 8px 20px rgba(245, 158, 11, 0.35);
        }

        /* Footer */
        .login-footer {
            text-align: center;
            color: #9ca3af;
            font-size: 12px;
            margin-top: 25px;
        }

        /* Mining strip */
        .mining-strip {
            height: 5px;

            background:
                repeating-linear-gradient(
                    45deg,
                    #f59e0b,
                    #f59e0b 15px,
                    #111827 15px,
                    #111827 30px
                );

            margin-top: 35px;
            border-radius: 3px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # LOGIN CARD
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
                Health, Safety & Equipment Monitoring System
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # LOGIN INPUTS
    # --------------------------------------------------

    # Create a centered column for the login fields
    left, center, right = st.columns(
        [1, 2, 1]
    )

    with center:

        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )

        st.write("")

        # Login button
        if st.button(
            "Login",
            type="primary"
        ):

            # Check whether the username exists
            if username in users:

                # Check whether the account is blocked
                if users[username].get(
                    "status",
                    "Active"
                ) == "Blocked":

                    st.error(
                        "This account has been blocked "
                        "by an administrator."
                    )

                    return

                # Check the password
                if users[username]["password"] == password:

                    # Save login information
                    st.session_state["logged_in"] = True

                    st.session_state["username"] = username

                    st.session_state["role"] = users[
                        username
                    ]["role"]

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
    # FOOTER
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
#
# Example:
#
# user_permissions["worker"] = [
#     "dashboard",
#     "questions",
#     "worker_health",
#     "incidents"
# ]
#
# This would give the worker an extra permission.

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

    # --------------------------------------------------
    # CHECK FOR ADMINISTRATOR CHANGES
    # --------------------------------------------------
    # If the Administrator has created custom permissions
    # for this user, use those permissions.

    if username in user_permissions:

        return permission in user_permissions[username]

    # --------------------------------------------------
    # OTHERWISE USE THE ORIGINAL ROLE PERMISSIONS
    # --------------------------------------------------

    if role not in permissions:

        return False

    return permission in permissions[role]
