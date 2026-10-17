
Loading older messages…
remove this text from the code
KHWEZI MINING
MONITORING SYSTEM
Worker safety • Equipment monitoring • Risk management

Remove these lines from your login.py code:

st.markdown("**KHWEZI MINING**")
st.markdown("**MONITORING SYSTEM**")
st.markdown("Worker safety • Equipment monitoring • Risk management")

If the text is inside a multiline HTML block, remove these lines from that block instead:

<h1>KHWEZI MINING</h1>
<h2>MONITORING SYSTEM</h2>
<p>Worker safety • Equipment monitoring • Risk management</p>

Keep the background image and login form code unchanged. Save and commit the changes to GitHub, then refresh your Streamlit app.

Write the full code without them
Here is the full login.py code with the three text lines removed. It keeps the login background image, username and password fields, role permissions, login validation, and logout functionality. The image filename should be khwezi_login.png in the same folder as login.py.


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

Demo login details

Role

Username

Password

Administrator

admin

admin123

Safety Officer

safety

safety123

Mining Engineer

mining

mining123

Maintenance Engineer

maintenance

maintenance123

Manager

manager

manager123

Save the code as login.py and commit it to GitHub. The code no longer displays KHWEZI MINING, MONITORING SYSTEM, or the worker safety and equipment monitoring slogan.

ImportError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/mining-health-safety-and-equipment-monitoring-app/app.py", line 14, in <module>     from user_management import render_user_management_page
File "/mount/src/mining-health-safety-and-equipment-monitoring-app/user_management.py", line 3, in <module>     from login import (     ...<3 lines>...     )

This error is happening while app.py imports render_user_management_page from user_management.py. The traceback points to line 3 of user_management.py, where it imports functions from login.py.

A likely cause is that user_management.py is importing a function or variable that does not exist in the new login.py code. The login.py version we just used defines USERS, ROLE_PERMISSIONS, login(), logout(), and has_permission().

Fix the import error
In login.py, add the following code after both ROLE_PERMISSIONS and USERS have been defined:


# --------------------------------------------------
# COMPATIBILITY VARIABLES
# These names are used by user_management.py.
# --------------------------------------------------

# Keep the lowercase name expected by user_management.py.
users = USERS

# Provide the permissions dictionary expected by the
# user management page.
permissions = ROLE_PERMISSIONS

# Stores individual user permission overrides.
# These are temporary and reset when the app restarts.
user_permissions = {}

# Create a list of all available page permissions.
available_permissions = sorted({
    permission
    for role_pages in ROLE_PERMISSIONS.values()
    for permission in role_pages
})


Then do the following
Save login.py.

Commit the changes to GitHub.

Wait for Streamlit Cloud to redeploy the app.

Important: This should address the missing-name imports identified from your earlier code, but the complete traceback is needed to confirm the exact failing name. If the error remains, send me the first 10 lines of user_management.py, especially its import section, and I’ll match the files correctly.

write the code
Replace your entire login.py file with this code. It includes the login background, demo accounts, role permissions, compatibility variables for user_management.py, and logout functionality. It also removes the extra text from the login page.


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

Important: This should resolve the import error only if user_management.py expects these names. If the error remains, paste the import section at the top of user_management.py so I can match the exact names it requires. The user_permissions dictionary above is temporary and resets when the app restarts; it does not itself save changes made in user management.

wwrite again the code with(full code)
remove this text from the code
KHWEZI MINING
MONITORING SYSTEM
Worker safety • Equipment monitoring • Risk management

Replace your entire login.py file with this full code. The text KHWEZI MINING, MONITORING SYSTEM, and Worker safety • Equipment monitoring • Risk management has been removed. The background image and login form remain.


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

After replacing the code, save and commit login.py to GitHub and let Streamlit Cloud redeploy the application.

Note: This keeps the existing demonstration accounts. Their passwords are stored in plain text, so this version is suitable for a prototype, not a production system.


Pasted text(7).txt
Document
fix this one
I checked your uploaded login.py code. The main issue is that the old branding text is still inside the login() function, even though you wanted it removed. The code also has inconsistent indentation in a few places, which can cause Python errors.

I'll correct the full file while keeping the background image, login form, five roles, and permission checks. I'll also include the compatibility names that your user_management.py may need.

Replace everything in your login.py with this corrected full code.


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



What was fixed
Removed the KHWEZI MINING heading.

Removed the MONITORING SYSTEM heading.

Removed the slogan and other branding text.

Corrected the Python indentation and syntax.

Kept the login form, background image, roles, and permission checks.

Added compatibility variables that may be required by user_management.py.

Important: The exact ImportError may still depend on which names user_management.py imports. If it persists, share that file's first 15 lines so the imports can be matched precisely.


import streamlit as st
import os
import base64


# --------------------------------------------------
# ROLE PERMISSIONS
# --------------------------------------------------
# Define the pages that each role is allowed to access.
# All logged-in users can access the Questions page.

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
# Do not use plain-text passwords for a production system.

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
# SESSION STATE
# --------------------------------------------------
# Preserve the login details while the user navigates
# around the Streamlit application.

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = ""


# --------------------------------------------------
# LOGIN BACKGROUND IMAGE
# --------------------------------------------------
def show_login_background():
    # Find the folder containing this login.py file.
    project_folder = os.path.dirname(
        os.path.abspath(__file__)
    )

    # Check the main folder and the data folder.
    image_paths = [
        os.path.join(project_folder, "khwezi_login.png"),
        os.path.join(
            project_folder,
            "data",
            "khwezi_login.png"
        )
    ]

    image_path = None

    # Find the first available image.
    for path in image_paths:
        if os.path.isfile(path):
            image_path = path
            break

    # Show an error if the image is missing.
    if image_path is None:
        st.error(
            "The login background image could not be found."
        )

        st.write(
            "Expected filename: khwezi_login.png"
        )

        st.write(
            "Upload the image beside app.py and login.py "
            "in your GitHub repository."
        )

        # Use a navy background if no image is available.
        st.markdown(
            """
            <style>
            [data-testid="stAppViewContainer"] {
                background-color: #10243A;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        return

    # Read the image and convert it to Base64.
    # This embeds the image in the page styling.
    try:
        with open(image_path, "rb") as image_file:
            image_bytes = image_file.read()

        encoded_image = base64.b64encode(
            image_bytes
        ).decode("utf-8")

    except OSError as error:
        st.error(f"Could not read the background image: {error}")
        return

    # Apply the image to the Streamlit application.
    # The overlay keeps the login form readable.
    st.markdown(
        f"""
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

        /* Style the login input fields. */
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
        """,
        unsafe_allow_html=True
    )


# --------------------------------------------------
# LOGIN FUNCTION
# --------------------------------------------------
def login():
    # Display the background before the login form.
    show_login_background()

    # Create a centred login area.
    left_column, centre_column, right_column = st.columns(
        [1, 1.1, 1]
    )

    with centre_column:

        # Display the system heading.
        st.markdown(
            """
            <div style="
                background-color: rgba(10, 27, 48, 0.90);
                padding: 22px;
                border-radius: 12px;
                text-align: center;
                border: 1px solid #D6A62E;
            ">
                <h1 style="
                    color: #F0C75E;
                    margin-bottom: 6px;
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

        # Create the functional login form.
        with st.form("khwezi_login_form"):

            st.subheader("Sign in to your account")

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

                # Check that both fields are completed.
                if not username.strip() or not password:
                    st.error(
                        "Please enter your username and password."
                    )

                # Check that the username exists.
                elif username not in USERS:
                    st.error("Invalid username or password.")

                # Check whether the account is blocked.
                elif USERS[username].get("blocked", False):
                    st.error(
                        "This account is blocked. "
                        "Contact the administrator."
                    )

                # Check whether the password is correct.
                elif USERS[username]["password"] != password:
                    st.error("Invalid username or password.")

                else:
                    # Store the successful login information.
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = username
                    st.session_state["role"] = USERS[username]["role"]

                    # Refresh the page to open the application.
                    st.rerun()


# --------------------------------------------------
# PERMISSION CHECKING
# --------------------------------------------------
def has_permission(permission):
    # Deny access if the user is not logged in.
    if not st.session_state.get("logged_in", False):
        return False

    username = st.session_state.get("username", "")

    # Confirm that the user account exists.
    if username not in USERS:
        return False

    # Deny access to blocked accounts.
    if USERS[username].get("blocked", False):
        return False

    role = st.session_state.get("role", "")

    # Every logged-in role can use the Questions page.
    if permission == "questions":
        return True

    # Check the permissions for the current role.
    return permission in ROLE_PERMISSIONS.get(role, [])


# --------------------------------------------------
# LOGOUT FUNCTION
# --------------------------------------------------
def logout():
    # Clear the current user's login details.
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""
    st.session_state["role"] = ""

    # Return the application to the login page.
    st.rerun()


