import streamlit as st

# Users and their roles
users = {"admin": {"password": "admin123", "role": "Administrator"},
         "safety": {"password": "safety123", "role": "Safety Officer"},
         "mining": {"password": "mining123", "role": "Mining Engineer"},
         "maintenance": {"password": "maintenance123", "role": "Maintenance Engineer"},
         "manager": {"password": "manager123", "role": "Manager"}}


def login():
    st.title("Khwezi Mining")
    st.subheader("Mining Health, Safety and Equipment Monitoring System")

    st.write("Please enter your login details.")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username in users and users[username]["password"] == password:

            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = users[username]["role"]

            st.success("Login successful!")

            st.rerun()

        else:
            st.error("Invalid username or password.")


def logout():
    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.session_state["role"] = ""

        st.rerun()
