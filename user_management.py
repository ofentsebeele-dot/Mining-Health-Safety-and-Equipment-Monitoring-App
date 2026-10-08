import streamlit as st
import pandas as pd
import os


# ============================================================
# FILE USED TO STORE USER INFORMATION
# ============================================================

USER_FILE = "data/users.csv"


# ============================================================
# ALL AVAILABLE PERMISSIONS
# ============================================================

PERMISSIONS = {
    "dashboard": "Dashboard",
    "worker_health": "Worker Health & Safety",
    "incidents": "Safety Incidents",
    "equipment": "Equipment",
    "maintenance": "Maintenance",
    "risk_assessment": "Risk Assessment",
    "reports": "Reports",
    "manage_users": "Manage Users",
    "questions": "Questions & Answers"
}


# ============================================================
# LOAD USERS
# ============================================================

def load_users():

    # Check if the data folder exists
    os.makedirs("data", exist_ok=True)

    # If the users file does not exist, create an empty table
    if not os.path.exists(USER_FILE):

        columns = [
            "Username",
            "Password",
            "Role",
            "Status",
            "Permissions"
        ]

        return pd.DataFrame(columns=columns)

    # Load the users from the CSV file
    return pd.read_csv(USER_FILE)


# ============================================================
# SAVE USERS
# ============================================================

def save_users(users):

    # Make sure the data folder exists
    os.makedirs("data", exist_ok=True)

    # Save all user information
    users.to_csv(USER_FILE, index=False)


# ============================================================
# CONVERT PERMISSIONS INTO TEXT
# ============================================================

def permissions_to_text(permissions):

    return ";".join(permissions)


# ============================================================
# CONVERT PERMISSION TEXT BACK INTO A LIST
# ============================================================

def text_to_permissions(permission_text):

    if pd.isna(permission_text) or permission_text == "":
        return []

    return permission_text.split(";")


# ============================================================
# ADD NEW USER
# ============================================================

def add_user(users):

    st.subheader("Add New User")

    username = st.text_input(
        "Username",
        key="new_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="new_password"
    )

    role = st.selectbox(
        "Role",
        [
            "Administrator",
            "Safety Officer",
            "Mining Engineer",
            "Maintenance Engineer",
            "Manager"
        ],
        key="new_role"
    )

    st.write("Select what this user is allowed to access:")

    selected_permissions = []

    for permission_key, permission_name in PERMISSIONS.items():

        # Questions must always be available to everyone
        if permission_key == "questions":

            st.checkbox(
                permission_name,
                value=True,
                disabled=True,
                key=f"new_{permission_key}"
            )

            selected_permissions.append(permission_key)

        else:

            allowed = st.checkbox(
                permission_name,
                key=f"new_{permission_key}"
            )

            if allowed:
                selected_permissions.append(permission_key)

    if st.button("Create User", type="primary"):

        if username.strip() == "":
            st.error("Please enter a username.")
            return

        if password.strip() == "":
            st.error("Please enter a password.")
            return

        # Check if the username already exists
        if username in users["Username"].astype(str).values:
            st.error("That username already exists.")
            return

        new_user = {
            "Username": username,
            "Password": password,
            "Role": role,
            "Status": "Active",
            "Permissions": permissions_to_text(
                selected_permissions
            )
        }

        users = pd.concat(
            [users, pd.DataFrame([new_user])],
            ignore_index=True
        )

        save_users(users)

        st.success(
            f"User '{username}' has been created successfully."
        )

        st.rerun()


# ============================================================
# MANAGE EXISTING USER
# ============================================================

def manage_existing_user(users):

    st.subheader("Manage Existing User")

    if users.empty:
        st.info("There are no users to manage.")
        return

    usernames = users["Username"].astype(str).tolist()

    selected_username = st.selectbox(
        "Select User",
        usernames
    )

    # Find the selected user
    user_index = users[
        users["Username"].astype(str) == selected_username
    ].index[0]

    selected_user = users.loc[user_index]

    # --------------------------------------------------------
    # USER INFORMATION
    # --------------------------------------------------------

    st.write("### User Information")

    st.write(
        f"**Username:** {selected_user['Username']}"
    )

    current_role = selected_user["Role"]

    current_status = selected_user["Status"]

    # --------------------------------------------------------
    # CHANGE ROLE
    # --------------------------------------------------------

    roles = [
        "Administrator",
        "Safety Officer",
        "Mining Engineer",
        "Maintenance Engineer",
        "Manager"
    ]

    role_index = roles.index(current_role) if current_role in roles else 0

    new_role = st.selectbox(
        "Change Role",
        roles,
        index=role_index,
        key=f"role_{selected_username}"
    )

    # --------------------------------------------------------
    # BLOCK / UNBLOCK USER
    # --------------------------------------------------------

    st.write("### Account Status")

    if current_status == "Active":

        if st.button(
            "Block User",
            key=f"block_{selected_username}"
        ):

            # Do not allow admin to block their own account
            if selected_username == st.session_state.get("username"):
                st.error(
                    "You cannot block your own account."
                )
            else:

                users.loc[
                    user_index,
                    "Status"
                ] = "Blocked"

                save_users(users)

                st.success(
                    f"{selected_username} has been blocked."
                )

                st.rerun()

    else:

        if st.button(
            "Unblock User",
            key=f"unblock_{selected_username}"
        ):

            users.loc[
                user_index,
                "Status"
            ] = "Active"

            save_users(users)

            st.success(
                f"{selected_username} has been unblocked."
            )

            st.rerun()

    # --------------------------------------------------------
    # CHANGE PASSWORD
    # --------------------------------------------------------

    st.write("### Change Password")

    new_password = st.text_input(
        "New Password",
        type="password",
        key=f"password_{selected_username}"
    )

    # --------------------------------------------------------
    # USER PERMISSIONS
    # --------------------------------------------------------

    st.write("### Page Permissions")

    st.caption(
        "The administrator can decide exactly what this user "
        "can see and access."
    )

    existing_permissions = text_to_permissions(
        selected_user["Permissions"]
    )

    selected_permissions = []

    for permission_key, permission_name in PERMISSIONS.items():

        # Questions are available to everyone
        if permission_key == "questions":

            st.checkbox(
                permission_name,
                value=True,
                disabled=True,
                key=f"permission_{selected_username}_{permission_key}"
            )

            selected_permissions.append(permission_key)

        else:

            is_allowed = permission_key in existing_permissions

            permission_checked = st.checkbox(
                permission_name,
                value=is_allowed,
                key=f"permission_{selected_username}_{permission_key}"
            )

            if permission_checked:
                selected_permissions.append(permission_key)

    # --------------------------------------------------------
    # SAVE CHANGES
    # --------------------------------------------------------

    if st.button(
        "Save Changes",
        type="primary",
        key=f"save_{selected_username}"
    ):

        # Make sure the current administrator cannot remove
        # their own Manage Users permission
        if selected_username == st.session_state.get("username"):

            if "manage_users" not in selected_permissions:

                st.error(
                    "You cannot remove Manage Users permission "
                    "from your own account."
                )

                return

        # Update role
        users.loc[
            user_index,
            "Role"
        ] = new_role

        # Update password if a new password was entered
        if new_password.strip() != "":

            users.loc[
                user_index,
                "Password"
            ] = new_password

        # Update permissions
        users.loc[
            user_index,
            "Permissions"
        ] = permissions_to_text(
            selected_permissions
        )

        save_users(users)

        st.success(
            f"{selected_username}'s settings have been updated."
        )

        st.rerun()


# ============================================================
# DELETE USER
# ============================================================

def delete_user(users):

    st.subheader("Delete User")

    if users.empty:
        return

    usernames = users["Username"].astype(str).tolist()

    selected_username = st.selectbox(
        "Select User to Delete",
        usernames,
        key="delete_user_select"
    )

    # Prevent administrator from deleting themselves
    if selected_username == st.session_state.get("username"):

        st.warning(
            "You cannot delete your own account."
        )

        return

    if st.button(
        "Delete User",
        type="secondary"
    ):

        users = users[
            users["Username"].astype(str)
            != selected_username
        ]

        save_users(users)

        st.success(
            f"User '{selected_username}' has been deleted."
        )

        st.rerun()


# ============================================================
# VIEW ALL USERS
# ============================================================

def view_all_users(users):

    st.subheader("All Users")

    if users.empty:

        st.info("No users have been created yet.")

        return

    display_users = users.copy()

    # Make the permissions easier to read
    display_users["Permissions"] = display_users[
        "Permissions"
    ].apply(
        lambda x: ", ".join(
            [
                PERMISSIONS.get(permission, permission)
                for permission in text_to_permissions(x)
            ]
        )
    )

    # Do not display passwords on screen
    display_users = display_users.drop(
        columns=["Password"]
    )

    st.dataframe(
        display_users,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MAIN USER MANAGEMENT PAGE
# ============================================================

def render_user_management_page():

    st.title("User Management")

    st.write(
        "Administrators can control user accounts, roles, "
        "permissions and access."
    )

    # Only administrators should be able to use this page
    if st.session_state.get("role") != "Administrator":

        st.error(
            "Only Administrators can manage users."
        )

        return

    # Load current users
    users = load_users()

    # Create tabs for the different management functions
    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Add User",
            "Manage User",
            "Delete User",
            "View Users"
        ]
    )

    with tab1:
        add_user(users)

    with tab2:
        manage_existing_user(users)

    with tab3:
        delete_user(users)

    with tab4:
        view_all_users(users)
