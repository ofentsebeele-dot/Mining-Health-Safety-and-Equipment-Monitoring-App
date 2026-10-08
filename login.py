```python
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


# --------------------------------------------------
# ROLE PERMISSIONS
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
# USER-SPECIFIC PERMISSIONS
# --------------------------------------------------
# This dictionary stores permission changes made
# by the Administrator.

user_permissions = {}


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

        /* ------------------------------------------
           MAIN APPLICATION BACKGROUND
           ------------------------------------------ */

        .stApp {
            background:
                linear-gradient(
                    135deg,
                    #eef5ff 0%,
                    #ffffff 50%,
                    #e8f1ff 100%
                );
        }


        /* ------------------------------------------
           REMOVE EXCESS TOP SPACE
           ------------------------------------------ */

        .block-container {
            padding-top: 3rem;
            padding-bottom: 2rem;
        }


        /* ------------------------------------------
           MAIN LOGIN CARD
           ------------------------------------------ */

        .login-card {
            background: #ffffff;

            border-radius: 20px;

            padding: 35px 40px 30px 40px;

            box-shadow:
                0 12px 35px
                rgba(30, 64, 175, 0.15);

            border: 1px solid #dbeafe;

            text-align: center;

            margin-bottom: 20px;
        }


        /* ------------------------------------------
           BLUE TOP LINE
           ------------------------------------------ */

        .blue-line {
            height: 5px;

            width: 100%;

            background:
                linear-gradient(
                    90deg,
                    #1d4ed8,
                    #3b82f6,
                    #60a5fa
                );

            border-radius: 10px;

            margin-bottom: 25px;
        }


        /* ------------------------------------------
           LOGO CIRCLE
           ------------------------------------------ */

        .logo-circle {

            width: 75px;
            height: 75px;

            margin: 0 auto 18px auto;

            border-radius: 50%;

            background:
                linear-gradient(
                    135deg,
                    #1d4ed8,
                    #2563eb
                );

            display: flex;

            align-items: center;

            justify-content: center;

            color: white;

            font-size: 30px;

            font-weight: 700;

            box-shadow:
                0 8px 20px
                rgba(37, 99, 235, 0.25);
        }


        /* ------------------------------------------
           MAIN TITLE
           ------------------------------------------ */

        .login-title {

            color: #0f172a;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 30px;

            font-weight: 700;

            letter-spacing: -0.5px;

            margin-bottom: 6px;
        }


        /* ------------------------------------------
           SUBTITLE
           ------------------------------------------ */

        .login-subtitle {

            color: #475569;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 14px;

            line-height: 1.5;

            margin-bottom: 5px;
        }


        /* ------------------------------------------
           FORM LABELS
           ------------------------------------------ */

        label {

            color: #1e293b !important;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 14px !important;

            font-weight: 600 !important;
        }


        /* ------------------------------------------
           INPUT BOXES
           ------------------------------------------ */

        div[data-baseweb="input"] {

            background: #ffffff;

            border: 1px solid #cbd5e1;

            border-radius: 10px;
        }


        div[data-baseweb="input"]:focus-within {

            border-color: #2563eb;

            box-shadow:
                0 0 0 2px
                rgba(37, 99, 235, 0.12);
        }


        div[data-baseweb="input"] input {

            color: #0f172a !important;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 15px;

            font-weight: 500;
        }


        /* ------------------------------------------
           LOGIN BUTTON
           ------------------------------------------ */

        div.stButton > button {

            width: 100%;

            height: 48px;

            background:
                linear-gradient(
                    90deg,
                    #1d4ed8,
                    #2563eb
                );

            color: #ffffff !important;

            border: none;

            border-radius: 10px;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 16px;

            font-weight: 700;

            margin-top: 10px;

            transition:
                0.2s ease;
        }


        /* ------------------------------------------
           BUTTON HOVER
           ------------------------------------------ */

        div.stButton > button:hover {

            background:
                linear-gradient(
                    90deg,
                    #1e40af,
                    #1d4ed8
                );

            transform: translateY(-1px);

            box-shadow:
                0 8px 18px
                rgba(37, 99, 235, 0.25);
        }


        /* ------------------------------------------
           FOOTER
           ------------------------------------------ */

        .login-footer {

            text-align: center;

            color: #64748b;

            font-family:
                "Segoe UI",
                Arial,
                sans-serif;

            font-size: 12px;

            margin-top: 20px;

            line-height: 1.6;
        }


        /* ------------------------------------------
           WELCOME TEXT
           ------------------------------------------ */

        .welcome-text {

            text-align: center;

            color: #2563eb;

            font-size: 13px;

            font-weight: 600;

            margin-top: 5px;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------
    # LOGIN LAYOUT
    # --------------------------------------------------

    left, center, right = st.columns(
        [1, 1.6, 1]
    )


    with center:

        # --------------------------------------------------
        # LOGIN CARD HEADER
        # --------------------------------------------------

        st.markdown(
            """
            <div class="login-card">

                <div class="blue-line"></div>

                <div class="logo-circle">
                    K
                </div>

                <div class="login-title">
                    Khwezi Mining
                </div>

                <div class="login-subtitle">
                    Health, Safety & Equipment
                    Monitoring System
                </div>

                <div class="welcome-text">
                    Secure System Login
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        # --------------------------------------------------
        # USERNAME
        # --------------------------------------------------

        username = st.text_input(
            "Username",
            key="login_username"
        )


        # --------------------------------------------------
        # PASSWORD
        # --------------------------------------------------

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        # --------------------------------------------------
        # LOGIN BUTTON
        # --------------------------------------------------

        if st.button(
            "Sign In",
            type="primary"
        ):

            # Check whether username exists
            if username in users:

                # Check password
                if users[username]["password"] == password:

                    # Store login status
                    st.session_state["logged_in"] = True

                    # Store username
                    st.session_state["username"] = username

                    # Store role
                    st.session_state["role"] = users[username]["role"]

                    # Show success message
                    st.success(
                        "Login successful."
                    )

                    # Reload application
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
        # FOOTER
        # --------------------------------------------------

        st.markdown(
            """
            <div class="login-footer">

                Khwezi Mining Monitoring System
                <br>

                Authorised users only

            </div>
            """,
            unsafe_allow_html=True
        )


# --------------------------------------------------
# LOGOUT
# --------------------------------------------------

def logout():

    # Display logout button in sidebar
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


    # --------------------------------------------------
    # CHECK USER
    # --------------------------------------------------

    if username not in users:

        return False


    # --------------------------------------------------
    # QUESTIONS
    # --------------------------------------------------
    # Questions are available to everyone.

    if permission == "questions":

        return True


    # --------------------------------------------------
    # CUSTOM USER PERMISSIONS
    # --------------------------------------------------
    # If the Administrator has changed
    # permissions for a specific user,
    # use those permissions.

    if username in user_permissions:

        return permission in user_permissions[username]


    # --------------------------------------------------
    # ROLE PERMISSIONS
    # --------------------------------------------------

    if role not in permissions:

        return False


    return permission in permissions[role]
```
