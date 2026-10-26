
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

    equipment_file = None

    for path in possible_paths:
        if path.exists():
            equipment_file = path
            break

    if equipment_file is None:
        raise FileNotFoundError(
            "Equipment data was not found. Place equipment.csv "
            "or equipment(1).csv in the same folder as app.py."
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
        raise ValueError(
            "The equipment file contains no valid equipment readings."
        )

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
# GENERATE EQUIPMENT ALERT
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
            "Urgent equipment inspection and appropriate "
            "maintenance or safety action are required."
        )

    elif alert_level == "Warning":
        alert_message = (
            "Equipment requires inspection and appropriate "
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
# GENERATE NOTIFICATIONS FROM CSV DATA
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

        equipment_type = row.get("Equipment type", "Not specified")

        if alert["alert_level"] == "Normal":
            continue

        if alert["temperature_status"] != "Normal":
            notifications.append({
                "equipment_id": alert["equipment_id"],
                "equipment_type": equipment_type,
                "parameter": "Temperature",
                "value": alert["temperature"],
                "unit": "°C",
                "status": alert["temperature_status"],
                "recommended_action": alert["alert_message"],
            })

        if alert["vibration_status"] != "Normal":
            notifications.append({
                "equipment_id": alert["equipment_id"],
                "equipment_type": equipment_type,
                "parameter": "Vibration",
                "value": alert["vibration"],
                "unit": "mm/s",
                "status": alert["vibration_status"],
                "recommended_action": alert["alert_message"],
            })

    notifications.sort(
        key=lambda item: (
            0 if item["status"] == "Critical" else 1,
            item["equipment_id"],
        )
    )

    return notifications


# --------------------------------------------------
# DISPLAY ONE EQUIPMENT AT A TIME
# --------------------------------------------------

def render_notifications_page():
    st.header("Notifications & Alerts")

    try:
        equipment_data = load_equipment_data()

    except (FileNotFoundError, ValueError, OSError) as error:
        st.error(f"Could not load equipment data: {error}")
        return

    if equipment_data.empty:
        st.warning("No equipment records are available.")
        return

    equipment_ids = (
        equipment_data["Equipment ID"]
        .drop_duplicates()
        .tolist()
    )

    if not equipment_ids:
        st.warning("No equipment IDs were found.")
        return

    # Initialise the selected equipment position.
    if "notification_equipment_index" not in st.session_state:
        st.session_state["notification_equipment_index"] = 0

    index = st.session_state["notification_equipment_index"]
    index = max(0, min(index, len(equipment_ids) - 1))

    st.session_state["notification_equipment_index"] = index

    # Equipment navigation.
    previous_col, selector_col, next_col = st.columns([1, 2, 1])

    with previous_col:
        if st.button(
            "Previous",
            disabled=(index == 0),
            use_container_width=True,
            key="notification_previous",
        ):
            st.session_state["notification_equipment_index"] = index - 1
            st.rerun()

    with selector_col:
        selected_equipment = st.selectbox(
            "Select Equipment ID",
            equipment_ids,
            index=index,
            key="notification_equipment_selector",
        )

    with next_col:
        if st.button(
            "Next",
            disabled=(index == len(equipment_ids) - 1),
            use_container_width=True,
            key="notification_next",
        ):
            st.session_state["notification_equipment_index"] = index + 1
            st.rerun()

    selected_index = equipment_ids.index(selected_equipment)

    if selected_index != index:
        st.session_state["notification_equipment_index"] = selected_index
        st.rerun()

    st.caption(
        f"Equipment {selected_index + 1} of {len(equipment_ids)}"
    )

    # Read only the selected equipment's record.
    selected_rows = equipment_data[
        equipment_data["Equipment ID"] == selected_equipment
    ]

    if selected_rows.empty:
        st.warning("No readings found for the selected equipment.")
        return

    equipment = selected_rows.iloc[0]

    temperature = float(equipment["Temperature"])
    vibration = float(equipment["Vibration"])
    equipment_type = equipment.get("Equipment type", "Not specified")

    # Equipment information.
    st.divider()
    st.subheader("Equipment Details")

    st.write(f"**Equipment ID:** {selected_equipment}")
    st.write(f"**Equipment Type:** {equipment_type}")

    temperature_col, vibration_col = st.columns(2)

    with temperature_col:
        st.metric(
            "Temperature",
            f"{temperature:.1f} °C",
        )

    with vibration_col:
        st.metric(
            "Vibration",
            f"{vibration:.1f} mm/s",
        )

    # Generate an alert for the selected equipment.
    alert = generate_alert(
        selected_equipment,
        temperature,
        vibration,
    )

    # Display the selected equipment's alert only.
    st.divider()
    st.subheader("Equipment Alert")

    if alert["alert_level"] == "Critical":
        st.error("CRITICAL ALERT")

    elif alert["alert_level"] == "Warning":
        st.warning("WARNING")

    else:
        st.success("NORMAL")

    st.write(f"**Alert Level:** {alert['alert_level']}")
    st.write(
        f"**Temperature Status:** {alert['temperature_status']}"
    )
    st.write(
        f"**Vibration Status:** {alert['vibration_status']}"
    )

    if alert["alert_level"] == "Critical":
        st.write(
            "**Recommended Action:** Inspect equipment urgently "
            "and initiate appropriate maintenance and safety procedures."
        )

    elif alert["alert_level"] == "Warning":
        st.write(
            "**Recommended Action:** Inspect equipment and arrange "
            "appropriate maintenance."
        )

    else:
        st.write(
            "**Recommended Action:** Continue routine monitoring."
        )


# --------------------------------------------------
# RUN PAGE DIRECTLY IF NEEDED
# --------------------------------------------------

if __name__ == "__main__":
    render_notifications_page()
