import streamlit as st


def render_user_management_page():

    st.title("User Management")

    st.write(
        "Manage system users and their assigned roles."
    )

    st.divider()

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
            "role": "Mining Manager"
        },
        "worker": {
            "password": "worker123",
            "role": "Worker"
        }
    }

    st.subheader("System Users")

    user_rows = []

    for username, details in users.items():

        user_rows.append(
            {
                "Username": username,
                "Role": details["role"]
            }
        )

    st.dataframe(
        user_rows,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------
    # ADD USER
    # --------------------------------------------------

    st.subheader("Add User")

    new_username = st.text_input(
        "Username",
        key="new_username"
    )

    new_password = st.text_input(
        "Password",
        type="password",
        key="new_password"
    )

    role_options = [
        "Administrator",
        "Safety Officer",
        "Mining Manager",
        "Worker"
    ]

    new_role = st.selectbox(
        "Role",
        role_options,
        key="new_role"
    )

    if st.button("Add User"):

        if new_username.strip() == "":
            st.error(
                "Please enter a username."
            )

        elif new_password.strip() == "":
            st.error(
                "Please enter a password."
            )

        elif new_username in users:
            st.error(
                "That username already exists."
            )

        else:

            st.success(
                f"User '{new_username}' can be added "
                f"with the role '{new_role}'."
            )

            st.info(
                "User persistence will be connected "
                "to the login system in the next step."
            )
user_rows = []

for username, details in users.items():

    user_rows.append(
        {
            "Username": username,
            "Role": details["role"]
        }
    )

st.dataframe(
    user_rows,
    use_container_width=True,
    hide_index=True
)
