import importlib
from pathlib import Path

import pandas as pd
import streamlit as st


# --------------------------------------------------
# PAGE IMPORT HELPER
# Optional page imports prevent one missing page module from
# stopping the entire application. Login remains required.
# --------------------------------------------------
def load_page_function(module_name, function_name):
    try:
        module = importlib.import_module(module_name)
        return getattr(module, function_name, None), None
    except Exception as exc:
        return None, f"{module_name}.py: {exc}"


try:
    from login import login, logout, has_permission
except Exception as exc:
    st.error(f"Could not load login.py: {exc}")
    st.stop()


# --------------------------------------------------
# ALERT CLASSIFICATION
# Thresholds supplied for this project.
# --------------------------------------------------
def check_temperature(temperature):
    if temperature > 100:
        return "Critical"
    elif temperature >= 80:
        return "Warning"
    return "Normal"


def check_vibration(vibration):
    if vibration > 8:
        return "Critical"
    elif vibration >= 5:
        return "Warning"
    return "Normal"


def generate_alert(equipment_id, temperature, vibration):
    temperature = float(temperature)
    vibration = float(vibration)

    temperature_status = check_temperature(temperature)
    vibration_status = check_vibration(vibration)

    if temperature_status == "Critical" or vibration_status == "Critical":
        alert_level = "Critical"
        alert_message = "Urgent equipment assessment required."
    elif temperature_status == "Warning" or vibration_status == "Warning":
        alert_level = "Warning"
        alert_message = "Equipment requires attention."
    else:
        alert_level = "Normal"
        alert_message = "Equipment readings are normal."

    return {
        "equipment_id": str(equipment_id),
        "temperature": temperature,
        "temperature_status": temperature_status,
        "vibration": vibration,
        "vibration_status": vibration_status,
        "alert_level": alert_level,
        "alert_message": alert_message,
    }


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
DEFAULTS = {
    "logged_in": False,
    "username": "",
    "role": "",
    "equipment_checks": {},
    "pending_alerts": {},
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------
# LOAD EQUIPMENT CSV
# Supports either common filename.
# Put the CSV in the same folder as app.py.
# --------------------------------------------------
base_folder = Path(__file__).resolve().parent
