```python
import streamlit as st

from login import users, permissions


def render_user_management_page():

    st.title("User Management")

    st.write(
        "Manage system users, roles and access permissions."
    )

    st.divider()

    # --------------------------------------------------
    # CURRENT USERS
    # --------------------------------------------------

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
    # ROLE PERMISSIONS
    # --------------------------------------------------

    st.subheader("Role Permissions")

    selected_role = st.selectbox(
        "Select a role",
        list(permissions.keys()),
        key="management_role"
    )

    role_permissions = permissions[
        selected_role
    ]

    st.write(
        f"Permissions for **{selected_role}**:"
    )

    for permission in role_permissions:

        st.write(
            f"✅ {permission.replace('_', ' ').title()}"
        )

    st.divider()

    # --------------------------------------------------
    # USER DETAILS
    # --------------------------------------------------

    st.subheader("User Details")

    selected_user = st.selectbox(
        "Select a user",
        list(users.keys()),
        key="management_user"
    )

    selected_user_details = users[
        selected_user
    ]

    st.write(
        f"**Username:** {selected_user}"
    )

    st.write(
        f"**Role:** {selected_user_details['role']}"
    )

    st.divider()

    # --------------------------------------------------
    # ACCESS CHECK
    # --------------------------------------------------

    st.subheader("Access Check")

    check_permission = st.selectbox(
        "Select a system function",
        [
            "dashboard",
            "worker_health",
            "incidents",
            "equipment",
            "maintenance",
            "risk_assessment",
            "reports",
            "manage_users"
        ],
        key="permission_check"
    )

    user_role = selected_user_details["role"]

    if check_permission in permissions.get(
        user_role,
        []
    ):

        st.success(
            f"{selected_user} has permission to access "
            f"{check_permission.replace('_', ' ').title()}."
        )

    else:

        st.warning(
            f"{selected_user} does not have permission to access "
            f"{check_permission.replace('_', ' ').title()}."
        )
```
