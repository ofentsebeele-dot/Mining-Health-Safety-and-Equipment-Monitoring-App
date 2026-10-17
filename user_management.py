
import streamlit as st

# Import the dictionaries that already exist in login.py.
from login import USERS as users
from login import ROLE_PERMISSIONS as permissions


# --------------------------------------------------
# STORE CUSTOM PERMISSIONS IN SESSION STATE
# --------------------------------------------------

# Preserve custom permissions during the current Streamlit session.
if "user_permissions" not in st.session_state:
    st.session_state["user_permissions"] = {}

user_permissions = st.session_state["user_permissions"]


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
    "manage_users": "Manage Users",
}


# --------------------------------------------------
# AVAILABLE ROLES
# --------------------------------------------------

# These roles match the intended project roles.
ROLES = [
    "Administrator",
    "Safety Officer",
    "Mining Engineer",
    "Maintenance Engineer",
    "Manager",
]


# --------------------------------------------------
# GET USER STATUS
# --------------------------------------------------

def get_user_status(username):
    """Return the user's status, supporting the existing login format."""
    user = users[username]

    # The existing login.py may use blocked=True/False.
    if user.get("blocked", False):
        return "Blocked"

    return user.get("status", "Active")


# --------------------------------------------------
# GET ORIGINAL ROLE PERMISSIONS
# --------------------------------------------------

def get_original_permissions(username):
    """Return the permissions assigned to the user's role."""
    if username not in users:
        return []

    role = users[username].get("role", "")

    # Return a copy so the original role list is not changed.
    return list(permissions.get(role, []))


# --------------------------------------------------
# GET CURRENT USER PERMISSIONS
# --------------------------------------------------

def get_current_permissions(username):
    """Return custom permissions or the user's original permissions."""
    if username not in users:
        return []

    if username in user_permissions:
        current = list(user_permissions[username])
    else:
        current = get_original_permissions(username)

    # Questions must always be available to every user.
    if "questions" not in current:
        current.append("questions")

    return current


# --------------------------------------------------
# SHOW USER INFORMATION
# --------------------------------------------------

def show_user_information(username):
    st.subheader("User Information")

    user = users[username]

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Username:** {username}")
        st.write(f"**Role:** {user.get('role', 'Not assigned')}")

    with col2:
        st.write(f"**Status:** {get_user_status(username)}")
        st.write("**Password:** Hidden")

    st.divider()
    st.write("### Original Role Permissions")

    original = get_original_permissions(username)

    for key, name in PAGE_NAMES.items():
        if key in original:
            st.success(f"✓ {name}")
        else:
            st.error(f"✗ {name}")

    st.divider()
    st.write("### Current Permissions")

    current = get_current_permissions(username)

    for key, name in PAGE_NAMES.items():
        if key in current:
            st.success(f"✓ {name}")
        else:
            st.error(f"✗ {name}")


# --------------------------------------------------
# CHANGE USER PERMISSIONS
# --------------------------------------------------

def change_permissions(username):
    st.subheader("Change User Permissions")

    st.info(
        "These changes affect the selected user's individual access, "
        "not the original permissions assigned to their role."
    )

    current = get_current_permissions(username)
    new_permissions = []

    for key, name in PAGE_NAMES.items():

        # Questions are always available.
        if key == "questions":
            st.checkbox(
                name,
                value=True,
                disabled=True,
                key=f"permission_{username}_{key}",
            )
            new_permissions.append(key)
            continue

        checked = st.checkbox(
            name,
            value=key in current,
            key=f"permission_{username}_{key}",
        )

        if checked:
            new_permissions.append(key)

    if st.button(
        "Save Permissions",
        type="primary",
        key=f"save_permissions_{username}",
    ):
        current_username = st.session_state.get("username", "")

        # Prevent an administrator from removing their own access.
        if username == current_username:
            if "manage_users" not in new_permissions:
                st.error(
                    "You cannot remove Manage Users permission "
                    "from your own account."
                )
                return

            if "dashboard" not in new_permissions:
                st.error(
                    "You cannot remove Dashboard permission "
                    "from your own account."
                )
                return

        user_permissions[username] = new_permissions

        st.success(f"Permissions for '{username}' have been saved.")
        st.rerun()


# --------------------------------------------------
# RESET USER PERMISSIONS
# --------------------------------------------------

def reset_permissions(username):
    st.subheader("Reset Permissions")

    st.write(
        "Remove the individual permission changes and restore "
        "the permissions assigned to the user's role."
    )

    if st.button(
        "Reset to Original Permissions",
        key=f"reset_permissions_{username}",
    ):
        user_permissions.pop(username, None)

        st.success(f"Permissions for '{username}' have been reset.")
        st.rerun()


# --------------------------------------------------
# CHANGE USER ROLE
# --------------------------------------------------

def change_role(username):
    st.subheader("Change User Role")

    current_role = users[username].get("role", ROLES[0])

    role_index = (
        ROLES.index(current_role)
        if current_role in ROLES
        else 0
    )

    new_role = st.selectbox(
        "Select New Role",
        ROLES,
        index=role_index,
        key=f"role_{username}",
    )

    if st.button(
        "Change Role",
        type="primary",
        key=f"change_role_{username}",
    ):
        current_username = st.session_state.get("username", "")

        # Do not allow an administrator to demote themselves.
        if username == current_username and new_role != "Administrator":
            st.error("You cannot remove your own Administrator role.")
            return

        users[username]["role"] = new_role

        # Remove custom permissions so the new role takes effect.
        user_permissions.pop(username, None)

        st.success(f"{username}'s role has been changed to {new_role}.")
        st.rerun()


# --------------------------------------------------
# CHANGE PASSWORD
# --------------------------------------------------

def change_password(username):
    st.subheader("Change Password")

    new_password = st.text_input(
        "New Password",
        type="password",
        key=f"new_password_{username}",
    )

    confirm_password = st.text_input(
        "Confirm New Password",
        type="password",
        key=f"confirm_password_{username}",
    )

    if st.button(
        "Change Password",
        type="primary",
        key=f"change_password_{username}",
    ):
        if not new_password.strip():
            st.error("Password cannot be empty.")
            return

        if new_password != confirm_password:
            st.error("The passwords do not match.")
            return

        users[username]["password"] = new_password

        st.success(f"Password for '{username}' has been changed.")
        st.rerun()


# --------------------------------------------------
# BLOCK / UNBLOCK USER
# --------------------------------------------------

def block_unblock_user(username):
    st.subheader("Block / Unblock User")

    current_status = get_user_status(username)
    st.write(f"Current Status: **{current_status}**")

    if current_status == "Active":
        if st.button("Block User", key=f"block_{username}"):
            if username == st.session_state.get("username", ""):
                st.error("You cannot block your own account.")
                return

            # Keep both fields updated for compatibility with login.py.
            users[username]["status"] = "Blocked"
            users[username]["blocked"] = True

            st.success(f"'{username}' has been blocked.")
            st.rerun()

    else:
        if st.button(
            "Unblock User",
            type="primary",
            key=f"unblock_{username}",
        ):
            users[username]["status"] = "Active"
            users[username]["blocked"] = False

            st.success(f"'{username}' has been unblocked.")
            st.rerun()


# --------------------------------------------------
# ADD USER
# --------------------------------------------------

def add_user():
    st.subheader("Add New User")

    username = st.text_input("Username", key="new_user_username").strip()

    password = st.text_input(
        "Password",
        type="password",
        key="new_user_password",
    )

    role = st.selectbox("Role", ROLES, key="new_user_role")

    if st.button("Add User", type="primary", key="add_user_button"):
        if not username:
            st.error("Please enter a username.")
            return

        if not password.strip():
            st.error("Please enter a password.")
            return

        if username in users:
            st.error("That username already exists.")
            return

        # Add the account in the same format used by login.py.
        users[username] = {
            "password": password,
            "role": role,
            "blocked": False,
            "status": "Active",
        }

        # The new user starts with the selected role's permissions.
        user_permissions.pop(username, None)

        st.success(f"User '{username}' has been added.")
        st.rerun()


# --------------------------------------------------
# DELETE USER
# --------------------------------------------------

def delete_user(username):
    st.subheader("Delete User")

    st.warning(
        f"You are about to permanently delete the user '{username}'."
    )

    if username == st.session_state.get("username", ""):
        st.error("You cannot delete your own account.")
        return

    confirmation = st.checkbox(
        "I confirm that I want to permanently delete this user.",
        key=f"confirm_delete_{username}",
    )

    if st.button(
        "Delete User",
        key=f"delete_{username}",
    ):
        if not confirmation:
            st.error("Please confirm the deletion.")
            return

        del users[username]
        user_permissions.pop(username, None)

        st.success(f"User '{username}' has been deleted.")
        st.rerun()


# --------------------------------------------------
# VIEW ALL USERS
# --------------------------------------------------

def view_all_users():
    st.subheader("All Existing Users")

    if not users:
        st.info("There are no users.")
        return

    user_data = []

    for username, user in users.items():
        user_data.append({
            "Username": username,
            "Role": user.get("role", ""),
            "Status": get_user_status(username),
            "Number of Permissions": len(
                get_current_permissions(username)
            ),
        })

    st.dataframe(
        user_data,
        use_container_width=True,
        hide_index=True,
    )


# --------------------------------------------------
# MAIN USER MANAGEMENT PAGE
# --------------------------------------------------

def render_user_management_page():
    st.title("User Management")

    st.write(
        "Administrator control panel for managing users "
        "and their access."
    )

    # Only administrators may access this page.
    if st.session_state.get("role") != "Administrator":
        st.error("Only Administrators can access User Management.")
        return

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Add User",
        "Manage User",
        "Permissions",
        "Block / Unblock",
        "Delete User",
        "All Users",
    ])

    with tab1:
        add_user()

    with tab2:
        if users:
            selected_user = st.selectbox(
                "Select User",
                list(users.keys()),
                key="manage_user",
            )

            st.divider()
            show_user_information(selected_user)

            st.divider()
            change_role(selected_user)

            st.divider()
            change_password(selected_user)
        else:
            st.info("No users available.")

    with tab3:
        if users:
            selected_user = st.selectbox(
                "Select User",
                list(users.keys()),
                key="permission_user",
            )

            st.divider()
            change_permissions(selected_user)

            st.divider()
            reset_permissions(selected_user)
        else:
            st.info("No users available.")

    with tab4:
        if users:
            selected_user = st.selectbox(
                "Select User",
                list(users.keys()),
                key="block_user",
            )

            st.divider()
            block_unblock_user(selected_user)
        else:
            st.info("No users available.")

    with tab5:
        if users:
            selected_user = st.selectbox(
                "Select User",
                list(users.keys()),
                key="delete_user",
            )

            st.divider()
            delete_user(selected_user)
        else:
            st.info("No users available.")

    with tab6:
        view_all_users()
