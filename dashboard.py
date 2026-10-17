import streamlit as st
import pandas as pd
import base64
import os


# Display a mine background image, if the image exists.
def set_background(image_file="mine_background.png"):
    if not os.path.exists(image_file):
        data_image = os.path.join("data", image_file)
        if os.path.exists(data_image):
            image_file = data_image
        else:
            st.warning(f"Background image '{image_file}' was not found. Dashboard will continue without it.")
            return

    with open(image_file, "rb") as image:
        encoded_image = base64.b64encode(image.read()).decode("utf-8")

    st.markdown(
        f"""
        <style>
        .stApp {{
            background:
                linear-gradient(rgba(0, 0, 0, 0.65), rgba(0, 0, 0, 0.65)),
                url("data:image/png;base64,{encoded_image}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label {{
            color: white;
        }}
        [data-testid="stMetricLabel"], [data-testid="stMetricValue"] {{
            color: white;
        }}
        [data-testid="stVerticalBlock"] {{
            border-radius: 8px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )


# Load a CSV from the project folder or the data folder.
def load_csv(filename):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    data_path = os.path.join("data", filename)
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    raise FileNotFoundError(
        f"Could not find '{filename}' in the project folder or data folder."
    )


def load_worker_data():
    return load_csv("workers.csv")


def load_incident_data():
    return load_csv("incidents.csv")


def load_equipment_data():
    return load_csv("equipment.csv")


# Calculate availability without dividing by zero.
def calculate_equipment_availability(equipment):
    operating_hours = pd.to_numeric(equipment["Operating hours"], errors="coerce")
    downtime = pd.to_numeric(equipment["Downtime"], errors="coerce")
    total_time = operating_hours + downtime
    return (operating_hours / total_time.where(total_time != 0)) * 100


# Main dashboard.
def render_dashboard():
    set_background("mine_background.png")
    st.title("Khwezi Mining Monitoring Dashboard")
    st.write("Central monitoring dashboard for health, safety and equipment information.")
    st.divider()

    # Load the three datasets.
    try:
        workers = load_worker_data()
        incidents = load_incident_data()
        equipment = load_equipment_data()
    except (FileNotFoundError, pd.errors.ParserError, OSError) as error:
        st.error(f"Could not load dashboard data: {error}")
        return

    # Check the columns required by this dashboard.
    required_columns = {
