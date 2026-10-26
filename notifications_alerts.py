import streamlit as st
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# LOAD EQUIPMENT DATA
# --------------------------------------------------

def load_equipment_data():
    possible_paths = [
        Path(__file__).parent / "equipment.csv",
        Path(__file__).parent / "equipment.csv",
        Path(__file__).parent / "data" / "equipment.csv",
    ]

    equipment_file = next(
        (path for path in possible_paths if path.exists()),
        None
    )

    if equipment_file is None:
        raise FileNotFoundError(
            "Equipment data was not found. Place equipment.csv "
            "or equipment(1).csv in the same folder as this file."
        )

    data = pd.read_csv(equipment_file)

    required_columns = [
        "Equipment ID",
        "Temperature",
        "Vibration",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing_columns:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )

    data["Equipment ID"] = data["Equipment ID"].astype(str).str.strip()
    data["Temperature"] = pd.to_numeric(
        data["Temperature"], errors="coerce"
    )
    data["Vibration"] = pd.to_numeric(
        data["Vibration"], errors="coerce"
    )

    data = data.dropna(
        subset=["Equipment ID", "Temperature", "Vibration"]
    )

    data = data[data["Equipment ID"] != ""]

    if data.empty:
        raise ValueError("No valid equipment readings were found.")

    return data


# --------------------------------------------------
# CHECK TEMPERATURE
# --------------------------------------------------

def check_temperature(temperature):
    if temperature > 100:
        return "Critical"
    elif temperature >= 80:
        return "Warning"
    return "Normal"


# --------------------------------------------------
# CHECK VIBRATION
# --------------------------------------------------

def check_vibration(vibration):
    if vibration > 8:
        return "Critical"
    elif vibration >= 5:
        return "Warning"
    return "Normal"


# --------------------------------------------------
# GENERATE ALERT
# --------------------------------------------------

def generate_alert(equipment_id, temperature, vibration):
    temperature_status = check_temperature(temperature)
    vibration_status = check_vibration(vibration)

    severity_order = {
        "Normal": 1,
        "Warning": 2,
        "Critical": 3,
    }

    alert_level = max(
        [temperature_status, vibration_status],
        key=lambda status: severity_order[status]
    )

    if alert_level == "Critical":
        alert_message = (
            "Inspect equipment and initiate appropriate "
            "maintenance/safety procedures."
        )
    elif alert_level == "Warning":
        alert_message = (
            "Inspect equipment and arrange appropriate "
            "maintenance follow-up."
        )
    else:
        alert_message = (
            "Equipment readings are within the defined normal ranges."
        )

    return {
        "equipment_id": str(equipment_id),
        "temperature": float(temperature),
        "vibration": float(vibration),
        "temperature_status": temperature_status,
        "vibration_status": vibration_status,
        "alert_level": alert_level,
        "alert_message": alert_message,
    }


# --------------------------------------------------
# GENERATE NOTIFICATIONS FROM CSV
# --------------------------------------------------

def generate_notifications():
    data = load_equipment_data()
    notifications = []

    for _, row in data.iterrows():
        alert = generate_alert(
            row["Equipment ID"],
            row["Temperature"],
            row["Vibration"],
        )

        if alert["temperature_status"] != "Normal":
            notifications.append({
                "equipment_id": alert["equipment_id"],
                "parameter": "Temperature",
                "value": alert["temperature"],
                "unit": "°C",
                "status": alert["temperature_status"],
            })

        if alert["vibration_status"] != "Normal":
            notifications.append({
                "equipment_id": alert["equipment_id"],
                "parameter": "Vibration",
                "value": alert["vibration"],
                "unit": "mm/s",
                "status": alert["vibration_status"],
            })

    return notifications


# --------------------------------------------------
# DISPLAY ONE ALERT
# --------------------------------------------------

def display_mining_alert(alert):
    st.subheader("MINING MONITORING ALERT")

    if alert["status"] == "Critical":
        st.error("[CRITICAL]")
    else:
        st.warning("[WARNING]")

    st.write(f"**Equipment ID:** {alert['equipment_id']}")
    st.write(f"**Parameter:** {alert['parameter']}")
    st.write(f"**Value:** {alert['value']:.1f} {alert['unit']}")
    st.write(f"**Status:** {alert['threshold_status']}")

    st.write("**Recommended Action:**")
    st.write(alert["recommended_action"])

    st.caption("Figure 1: Mining monitoring alert.")


# --------------------------------------------------
# NOTIFICATIONS PAGE
# --------------------------------------------------

def render_notifications_page():
    st.header("Notifications & Alerts")

    try:
        equipment_data = load_equipment_data()
    except (FileNotFoundError, ValueError, OSError) as error:
        st.error(f"Could not load equipment data: {error}")
        return

    equipment_ids = (
        equipment_data["Equipment ID"]
        .drop_duplicates()
        .tolist()
    )

    if not equipment_ids:
        st.warning("No equipment records are available.")
        return

    selected_equipment = st.selectbox(
        "Select Equipment ID",
        equipment_ids,
        key="notification_equipment_selector",
    )

    selected_rows = equipment_data[
        equipment_data["Equipment ID"] == selected_equipment
    ]

    if selected_rows.empty:
        st.warning("No readings found for this equipment.")
        return

    equipment = selected_rows.iloc[0]

    temperature = float(equipment["Temperature"])
    vibration = float(equipment["Vibration"])
    equipment_type = equipment.get(
        "Equipment type", "Not specified"
    )

    st.subheader("Equipment Details")
    st.write(f"**Equipment ID:** {selected_equipment}")
    st.write(f"**Equipment Type:** {equipment_type}")

    temperature_col, vibration_col = st.columns(2)

    with temperature_col:
        st.metric("Temperature", f"{temperature:.1f} °C")

    with vibration_col:
        st.metric("Vibration", f"{vibration:.1f} mm/s")

    temperature_status = check_temperature(temperature)
    vibration_status = check_vibration(vibration)

    # Show only the most serious abnormal parameter.
    severity_order = {
        "Normal": 1,
        "Warning": 2,
        "Critical": 3,
    }

    statuses = {
        "Temperature": temperature_status,
        "Vibration": vibration_status,
    }

    most_serious_parameter = max(
        statuses,
        key=lambda parameter: severity_order[statuses[parameter]]
    )

    most_serious_status = statuses[most_serious_parameter]

    if most_serious_status == "Normal":
        st.subheader("Equipment Status")
        st.success("NORMAL")
        st.write(
            "No temperature or vibration alerts for this equipment."
        )
        st.write(
            "**Recommended Action:** Continue routine monitoring."
        )
        return

    if most_serious_parameter == "Temperature":
        value = temperature
        unit = "°C"
        subheading = "Temperature Alert"
    else:
        value = vibration
        unit = "mm/s"
        subheading = "Vibration Alert"

    threshold_status = (
        "Above Critical Threshold"
        if most_serious_status == "Critical"
        else "Above Warning Threshold"
    )

    recommended_action = (
        "Inspect equipment and initiate appropriate "
        "maintenance/safety procedures."
        if most_serious_status == "Critical"
        else
        "Inspect equipment and arrange appropriate "
        "maintenance follow-up."
    )

    alert = {
        "equipment_id": selected_equipment,
        "parameter": most_serious_parameter,
        "value": value,
        "unit": unit,
        "status": most_serious_status,
        "threshold_status": threshold_status,
        "recommended_action": recommended_action,
    }

    st.subheader(subheading)
    display_mining_alert(alert)


# --------------------------------------------------
# RUN PAGE DIRECTLY IF NEEDED
# --------------------------------------------------

if __name__ == "__main__":
    render_notifications_page()
