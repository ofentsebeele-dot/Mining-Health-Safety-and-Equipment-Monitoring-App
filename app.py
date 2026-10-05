import streamlit as st
from login import login, logout

# Set default login status
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "username" not in st.session_state:
    st.session_state["username"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = ""

# Show login page if the user is not logged in
if not st.session_state["logged_in"]:

    login()

# Show application if the user is logged in
else:

    st.title("Khwezi Mining Monitoring System")

    st.success(f"Welcome, {st.session_state['username']}!")

    st.write(f"Your role: **{st.session_state['role']}**")

    st.divider()

    st.header("System Dashboard")

    st.info("The dashboard and monitoring modules will be added in the next steps.")

    logout()
