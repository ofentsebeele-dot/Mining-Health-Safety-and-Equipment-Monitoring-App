
import streamlit as st


# --------------------------------------------------
# USER MANAGEMENT PAGE
# --------------------------------------------------

def render_user_management_page():

    st.title("User Management")

    st.write(
        "Administrator page for managing system users."
    )

    # --------------------------------------------------
    # EXISTING USERS
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
            "role": "Manager"
        },
        "worker": {
            "password": "worker123",
            "role": "Worker"
        }
    }

    # --------------------------------------------------
    # DISPLAY USERS
    # --------------------------------------------------

    st.subheader("Existing Users")

    for username, details in users.items():

        st.write(
            f"**Username:** {username}"
        )

        st.write(
            f"**Role:** {details['role']}"
        )

        st.divider()

    # --------------------------------------------------
    # ADD NEW USER
    # --------------------------------------------------

    st.subheader("Add New User")

    new_username = st.text_input(
        "New Username"
    )

    new_password = st.text_input(
        "New Password",
        type="password"
    )

    available_roles = [
        "Administrator",
        "Safety Officer",
        "Manager",
        "Worker"
    ]

    new_role = st.selectbox(
        "Select Role",
        available_roles
    )

    if st.button("Add User"):

        # Check that the username was entered.
        if new_username.strip() == "":

            st.error(
                "Please enter a username."
            )

        # Check that the password was entered.
        elif new_password.strip() == "":

            st.error(
                "Please enter a password."
            )

        # Check for duplicate usernames.
        elif new_username in users:

            st.error(
                "This username already exists."
            )

        else:

            # Add the new account to the users dictionary.
            users[new_username] = {
                "password": new_password,
                "role": new_role
            }

            st.success(
                f"User '{new_username}' added successfully."
            )
