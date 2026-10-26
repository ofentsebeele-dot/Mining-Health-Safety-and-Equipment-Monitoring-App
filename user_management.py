import streamlit as st

from login import (
    users,
    permissions,
    user_permissions
)


# --------------------------------------------------
# AVAILABLE PAGE PERMISSIONS
# --------------------------------------------------

PAGE_NAMES = {
    "dashboard": "Dashboard",
    "worker_health": "Worker Health & Safety",
    "incidents": "Safety Incidents",
    "equipment": "Equipment",
    "maintenance": "Maintenance",
    "risk_assessment": "Risk Assessment",
    "reports": "Reports",
    "questions": "Questions & Answers",
    "manage_users": "Manage Users"
}


# --------------------------------------------------
# AVAILABLE ROLES
# --------------------------------------------------

ROLES = [
    "Administrator",
    "Safety Officer",
    "Mining Manager",
    "Worker"
]


# --------------------------------------------------
# GET ORIGINAL ROLE PERMISSIONS
# --------------------------------------------------

def get_original_permissions(username):

    # Get the user's role
    role = users[username]["role"]

    # Return a copy of the original role permissions
    return permissions.get(role, []).copy()


# --------------------------------------------------
# GET CURRENT USER PERMISSIONS
# --------------------------------------------------

def get_current_permissions(username):

    # If the Administrator has changed this user's
    # permissions, use those custom permissions
    if username in user_permissions:

        return user_permissions[username].copy()

    # Otherwise use the original role permissions
    return get_original_permissions(username)


# --------------------------------------------------
# SHOW USER INFORMATION
# --------------------------------------------------

def show_user_information(username):

    st.subheader("User Information")

    user = users[username]

    # Display basic account information
    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Username:** {username}"
        )

        st.write(
            f"**Role:** {user['role']}"
        )

    with col2:

        # Status may not exist for old users,
        # so Active is used by default
        status = user.get(
            "status",
            "Active"
        )

        st.write(
            f"**Status:** {status}"
        )

        st.write(
            "**Password:** ********"
        )

    st.divider()

    # --------------------------------------------------
    # ORIGINAL ROLE PERMISSIONS
    # --------------------------------------------------

    st.write("### Original Role Permissions")

    original_permissions = get_original_permissions(
        username
    )

    for permission_key, permission_name in PAGE_NAMES.items():

        if permission_key in original_permissions:

            st.success(
                f"✓ {permission_name}"
            )

        else:

            st.error(
                f"✗ {permission_name}"
            )

    st.divider()

    # --------------------------------------------------
    # CURRENT PERMISSIONS
    # --------------------------------------------------

    st.write("### Current Permissions")

    current_permissions = get_current_permissions(
        username
    )

    for permission_key, permission_name in PAGE_NAMES.items():

        if permission_key in current_permissions:

            st.success(
                f"✓ {permission_name}"
            )

        else:

            st.error(
                f"✗ {permission_name}"
            )


# --------------------------------------------------
# CHANGE USER PERMISSIONS
# --------------------------------------------------

def change_permissions(username):

    st.subheader("Change User Permissions")

    st.info(
        "The original role permissions are not changed. "
        "You are only changing this individual user's access."
    )

    # Get the user's current permissions
    current_permissions = get_current_permissions(
        username
    )

    new_permissions = []

    # Create a checkbox for every page
    for permission_key, permission_name in PAGE_NAMES.items():

        # Questions must always be available
        if permission_key == "questions":

            st.checkbox(
                permission_name,
                value=True,
                disabled=True,
                key=f"permission_{username}_{permission_key}"
            )

            new_permissions.append(
                permission_key
            )

            continue

        # Determine whether the user currently has access
        has_access = (
            permission_key in current_permissions
        )

        # Display the checkbox
        checked = st.checkbox(
            permission_name,
            value=has_access,
            key=f"permission_{username}_{permission_key}"
        )

        if checked:

            new_permissions.append(
                permission_key
            )

    # --------------------------------------------------
    # SAVE PERMISSION CHANGES
    # --------------------------------------------------

    if st.button(
        "Save Permissions",
        type="primary",
        key=f"save_permissions_{username}"
    ):

        # Prevent the Administrator from removing
        # their own Manage Users permission
        if username == st.session_state.get("username"):

            if "manage_users" not in new_permissions:

                st.error(
                    "You cannot remove Manage Users "
                    "permission from your own account."
                )

                return

        # Save the custom permissions
        user_permissions[username] = new_permissions

        st.success(
            f"Permissions for '{username}' have been changed."
        )

        st.rerun()


# --------------------------------------------------
# RESET USER PERMISSIONS
# --------------------------------------------------

def reset_permissions(username):

    st.subheader("Reset Permissions")

    st.write(
        "This will remove the custom permissions and "
        "return the user to their original role permissions."
    )

    if st.button(
        "Reset to Original Permissions",
        key=f"reset_permissions_{username}"
    ):

        # Remove custom permissions
        if username in user_permissions:

            del user_permissions[username]

        st.success(
            f"{username} has been returned to their "
            f"original role permissions."
        )

        st.rerun()


# --------------------------------------------------
# CHANGE USER ROLE
# --------------------------------------------------

def change_role(username):

    st.subheader("Change User Role")

    current_role = users[username]["role"]

    # Find the current role in the list
    if current_role in ROLES:

        role_index = ROLES.index(
            current_role
        )

    else:

        role_index = 0

    new_role = st.selectbox(
        "Select New Role",
        ROLES,
        index=role_index,
        key=f"role_{username}"
    )

    if st.button(
        "Change Role",
        type="primary",
        key=f"change_role_{username}"
    ):

        # Prevent the administrator from changing
        # their own Administrator role
        if username == st.session_state.get("username"):

            if new_role != "Administrator":

                st.error(
                    "You cannot remove your own Administrator role."
                )

                return

        # Change the user's role
        users[username]["role"] = new_role

        st.success(
            f"{username}'s role has been changed to "
            f"{new_role}."
        )

        st.rerun()


# --------------------------------------------------
# CHANGE PASSWORD
# --------------------------------------------------

def change_password(username):

    st.subheader("Change Password")

    new_password = st.text_input(
        "New Password",
        type="password",
        key=f"new_password_{username}"
    )

    confirm_password = st.text_input(
        "Confirm New Password",
        type="password",
        key=f"confirm_password_{username}"
    )

    if st.button(
        "Change Password",
        type="primary",
        key=f"change_password_{username}"
    ):

        if new_password.strip() == "":

            st.error(
                "Password cannot be empty."
            )

            return

        if new_password != confirm_password:

            st.error(
                "The passwords do not match."
            )

            return

        # Update the password
        users[username]["password"] = new_password

        st.success(
            f"Password for '{username}' has been changed."
        )

        st.rerun()


# --------------------------------------------------
# BLOCK / UNBLOCK USER
# --------------------------------------------------

def block_unblock_user(username):

    st.subheader("Block / Unblock User")

    # Get current status
    current_status = users[username].get(
        "status",
        "Active"
    )

    st.write(
        f"Current Status: **{current_status}**"
    )

    # --------------------------------------------------
    # BLOCK USER
    # --------------------------------------------------

    if current_status == "Active":

        if st.button(
            "Block User",
            key=f"block_{username}"
        ):

            # Prevent admin from blocking themselves
            if username == st.session_state.get("username"):

                st.error(
                    "You cannot block your own account."
                )

                return

            users[username]["status"] = "Blocked"

            st.success(
                f"'{username}' has been blocked."
            )

            st.rerun()

    # --------------------------------------------------
    # UNBLOCK USER
    # --------------------------------------------------

    else:

        if st.button(
            "Unblock User",
            type="primary",
            key=f"unblock_{username}"
        ):

            users[username]["status"] = "Active"

            st.success(
                f"'{username}' has been unblocked."
            )

            st.rerun()


# --------------------------------------------------
# ADD USER
# --------------------------------------------------

def add_user():

    st.subheader("Add New User")

    username = st.text_input(
        "Username",
        key="new_user_username"
    )

    password = st.text_input(
        "Password",
        type="password",
        key="new_user_password"
    )

    role = st.selectbox(
        "Role",
        ROLES,
        key="new_user_role"
    )

    if st.button(
        "Add User",
        type="primary"
    ):

        # Check username
        if username.strip() == "":

            st.error(
                "Please enter a username."
            )

            return

        # Check password
        if password.strip() == "":

            st.error(
                "Please enter a password."
            )

            return

        # Check if username already exists
        if username in users:

            st.error(
                "That username already exists."
            )

            return

        # Create the new user
        users[username] = {
            "password": password,
            "role": role,
            "status": "Active"
        }

        st.success(
            f"User '{username}' has been added."
        )

        st.rerun()


# --------------------------------------------------
# DELETE USER
# --------------------------------------------------

def delete_user(username):

    st.subheader("Delete User")

    st.warning(
        f"You are about to permanently delete "
        f"the user '{username}'."
    )

    # Prevent deleting yourself
    if username == st.session_state.get("username"):

        st.error(
            "You cannot delete your own account."
        )

        return

    confirmation = st.checkbox(
        "I confirm that I want to permanently delete this user.",
        key=f"confirm_delete_{username}"
    )

    if st.button(
        "Delete User",
        type="secondary",
        key=f"delete_{username}"
    ):

        if not confirmation:

            st.error(
                "Please confirm the deletion."
            )

            return

        # Delete the user
        del users[username]

        # Delete their custom permissions if they have any
        if username in user_permissions:

            del user_permissions[username]

        st.success(
            f"User '{username}' has been deleted."
        )

        st.rerun()


# --------------------------------------------------
# VIEW ALL USERS
# --------------------------------------------------

def view_all_users():

    st.subheader("All Existing Users")

    if not users:

        st.info(
            "There are no users."
        )

        return

    # Create a table for displaying users
    user_data = []

    for username, user in users.items():

        current_permissions = get_current_permissions(
            username
        )

        user_data.append(
            {
                "Username": username,
                "Role": user["role"],
                "Status": user.get(
                    "status",
                    "Active"
                ),
                "Number of Permissions": len(
                    current_permissions
                )
            }
        )

    st.dataframe(
        user_data,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# MAIN USER MANAGEMENT PAGE
# --------------------------------------------------

def render_user_management_page():

    st.title("User Management")

    st.write(
        "Administrator control panel for managing "
        "users and their access."
    )

    # Only administrators can access this page
    if st.session_state.get("role") != "Administrator":

        st.error(
            "Only Administrators can access User Management."
        )

        return

    # --------------------------------------------------
    # TABS
    # --------------------------------------------------

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
        [
            "Add User",
            "Manage User",
            "Permissions",
            "Block / Unblock",
            "Delete User",
            "All Users"
        ]
    )

    # --------------------------------------------------
    # ADD USER
    # --------------------------------------------------

    with tab1:

        add_user()

    # --------------------------------------------------
    # MANAGE USER
    # --------------------------------------------------

    with tab2:

        if users:

            selected_user = st.selectbox(
                "Select User",
                list(users.keys()),
                key="manage_user"
            )

            st.divider()

            show_user_information(
                selected_user
            )

            st.divider()

            change_role(
                selected_user
            )

            st.divider()

            change_password(
                selected_user
            )

        else:

            st.info(
                "No users available."
            )

    # --------------------------------------------------
    # PERMISSIONS
    # --------------------------------------------------

    with tab3:

        if users:

            selected_user = st.selectbox(
                "Select User",
                list(users.keys()),
                key="permission_user"
            )

            st.divider()

            change_permissions(
                selected_user
            )

            st.divider()

            reset_permissions(
                selected_user
            )

        else:

            st.info(
                "No users available."
            )

    # --------------------------------------------------
    # BLOCK / UNBLOCK
    # --------------------------------------------------

    with tab4:

        if users:

            selected_user = st.selectbox(
                "Select User",
                list(users.keys()),
                key="block_user"
            )

            st.divider()

            block_unblock_user(
                selected_user
            )

        else:

            st.info(
                "No users available."
            )

    # --------------------------------------------------
    # DELETE USER
    # --------------------------------------------------

    with tab5:

        if users:

            selected_user = st.selectbox(
                "Select User",
                list(users.keys()),
                key="delete_user"
            )

            st.divider()

            delete_user(
                selected_user
            )

        else:

            st.info(
                "No users available."
            )

    # --------------------------------------------------
    # ALL USERS
    # --------------------------------------------------

    with tab6:

        view_all_users()
