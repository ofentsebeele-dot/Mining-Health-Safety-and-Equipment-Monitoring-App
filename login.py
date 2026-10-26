import streamlit as st
import os
import base64


def find_image_path(filename):
    possible_paths = [
        filename,
        os.path.join("data", filename)]

    for path in possible_paths:
        if os.path.isfile(path):
            return path

    return None


def set_login_background(image_file="khwezi_login.png"):
    path = find_image_path(image_file)

    if path is None:
        st.markdown("""
        <style>
        .stApp {
            background-color: #000000 !important;
        }

        .stApp h1,
        .stApp h2,
        .stApp h3,
        .stApp h4,
        .stApp p,
        .stApp label {
            color: #FFFFFF !important;
        }
        </style>
        """, unsafe_allow_html=True)
        return

    try:
        with open(path, "rb") as image:
            encoded_image = base64.b64encode(
                image.read()
            ).decode("utf-8")

        st.markdown(
            f"""
            <style>

            /* Background image with a lighter dark overlay */
            .stApp {{
                background-image:
                    linear-gradient(
                        rgba(0, 0, 0, 0.40),
                        rgba(0, 0, 0, 0.40)
                    ),
                    url("data:image/png;base64,{encoded_image}");

                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                color: #FFFFFF !important;
            }}

            /* Move the login content down */
            .block-container {{
                padding-top: 150px !important;
                padding-bottom: 40px !important;
            }}

            /* Login title and headings */
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp h4 {{
                color: #FFFFFF !important;
                font-weight: 800 !important;
                text-shadow: 2px 2px 5px #000000;
            }}

            /* General text and labels */
            .stApp p,
            .stApp label,
            .stApp [data-testid="stMarkdownContainer"] {{
                color: #FFFFFF !important;
                font-weight: 600 !important;
                text-shadow: 1px 1px 3px #000000;
            }}

            /* Login input fields */
            .stTextInput input {{
                background-color: rgba(15, 15, 15, 0.80) !important;
                color: #FFFFFF !important;
                border: 1px solid #CCCCCC !important;
                border-radius: 6px;
            }}

            .stTextInput input::placeholder {{
                color: #DDDDDD !important;
            }}

            /* Login buttons */
            .stButton button {{
                background-color: rgba(25, 25, 25, 0.85) !important;
                color: #FFFFFF !important;
                border: 1px solid #CCCCCC !important;
                border-radius: 8px;
                font-weight: 700 !important;
            }}

            .stButton button:hover {{
                background-color: rgba(55, 55, 55, 0.95) !important;
                border: 1px solid #FFFFFF !important;
            }}

            /* Sidebar */
            [data-testid="stSidebar"] {{
                background-color: #101010 !important;
            }}

            [data-testid="stSidebar"] * {{
                color: #FFFFFF !important;
            }}

            /* Alerts */
            [data-testid="stAlert"] p {{
                color: #FFFFFF !important;
                text-shadow: none !important;
            }}

            /* Dividers */
            hr {{
                border-color: rgba(255, 255, 255, 0.45) !important;
            }}

            </style>
            """,
            unsafe_allow_html=True
        )

    except OSError as error:
        st.error(f"Could not load the login background image: {error}")


# Users

users = {"admin": { "password": "admin1", "role": "Administrator"},
         "safety": {"password": "safety1", "role": "Safety Officer"},
         "manager": {"password": "manager1","role": "Mining Manager"},
         "maintenance": {"password": "maintenance1","role": "Maintenance Engineer"},
         "worker": { "password": "worker1", "role": "Worker"}}


# Default role permissions

permissions = {"Administrator": ["dashboard", "worker_health", "incidents", "equipment", "maintenance", "risk_assessment","reports", "questions", "manage_users", "notifications_alerts"],
               "Safety Officer": ["dashboard","worker_health", "incidents", "risk_assessment", "questions", "reports", "notifications_alerts"],
               "Mining Manager": ["dashboard", "worker_health", "incidents", "equipment", "maintenance",  "risk_assessment", "questions", "reports", "notifications_alerts" ],
               "Maintenance Engineer": [ "dashboard","equipment", "maintenance", "risk_assessment", "reports", "questions", "notifications_alerts"],
               "Worker": ["dashboard", "questions","worker_health", "notifications_alerts"]}


user_permissions = {}

# Login Function

def login():
    set_login_background()

    # Add space above the login title
    st.markdown(
        '<div style="height: 20px;"></div>',
        unsafe_allow_html=True)

    st.title("Monitoring System")
    st.subheader("Login")

    username = st.text_input(
        "Username",
        key="login_username")

    password = st.text_input(
        "Password",
        type="password",
        key="login_password" )

    if st.button("Login"):
        if username in users:
            if users[username]["password"] == password:
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.session_state["role"] = users[username]["role"]

                st.success("Login successful.")
                st.rerun()
            else:
                st.error("Incorrect password.")
        else:
            st.error("Username not found.")

# Logout Functions

def logout():
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""
    st.rerun()


# Permission

def has_permission(permission):
    username = st.session_state.get("username", "")
    role = st.session_state.get("role", "")

    if username not in users:
        return False

    # Questions and Notifications & Alerts are available to everyone
    if permission in ["questions", "notifications_alerts"]:
        return True

    # Use administrator-customised permissions if available
    if username in user_permissions:
        return permission in user_permissions[username]

    # Otherwise use default role permissions
    if role not in permissions:
        return False

    return permission in permissions[role]
