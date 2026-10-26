
import streamlit as st
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# LOAD EQUIPMENT DATA
# --------------------------------------------------

def load_equipment_data():
    possible_paths = [
        Path(__file__).parent / "equipment(1).csv",
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
        raise ValueError(
            "No valid equipment readings were found in the CSV file."
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
# GENERATE COMBINED EQUIPMENT ALERT
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
# GENERATE NOTIFICATIONS FROM EQUIPMENT DATA
# --------------------------------------------------

def generate_notifications():
    data = load_equipment_data()
    notifications = []

    for _, row in data.iterrows():
        equipment_id = str(row["Equipment ID"])
        temperature = float(row["Temperature"])
        vibration = float(row["Vibration"])

        equipment_type = row.get(
            "Equipment type", "Not specified"
        )

        temperature_status = check_temperature(temperature)
        vibration_status = check_vibration(vibration)

        if temperature_status != "Normal":
            notifications.append({
                "equipment_id": equipment_id,
                "equipment_type": equipment_type,
                "parameter": "Temperature",
                "value": temperature,
                "unit": "°C",
                "status": temperature_status,
                "threshold_status": (
                    "Above Critical Threshold"
                    if temperature_status == "Critical"
                    else "Above Warning Threshold"
                ),
                "recommended_action": (
                    "Inspect equipment and initiate appropriate "
                    "maintenance/safety procedures."
                    if temperature_status == "Critical"
                    else
                    "Inspect equipment and arrange appropriate "
                    "maintenance follow-up."
                ),
            })

        if vibration_status != "Normal":
            notifications.append({
                "equipment_id": equipment_id,
                "equipment_type": equipment_type,
                "parameter": "Vibration",
                "value": vibration,
                "unit": "mm/s",
                "status": vibration_status,
                "threshold_status": (
                    "Above Critical Threshold"
                    if vibration_status == "Critical"
                    else "Above Warning Threshold"
                ),
                "recommended_action": (
                    "Inspect equipment and initiate appropriate "
                    "maintenance/safety procedures."
                    if vibration_status == "Critical"
                    else
                    "Inspect equipment and arrange appropriate "
                    "maintenance follow-up."
                ),
            })

    # Show Critical alerts before Warning alerts when navigating.
    notifications.sort(
        key=lambda item: (
            0 if item["status"] == "Critical" else 1,
            item["equipment_id"],
            item["parameter"],
        )
    )

    return notifications


# --------------------------------------------------
# DISPLAY ONE ALERT
# --------------------------------------------------

def display_mining_alert(alert):
    st.write("=====================================================")
    st.markdown("### MINING MONITORING ALERT")

    if alert["status"] == "Critical":
        st.error("[CRITICAL]")
    else:
        st.warning("[WARNING]")

    st.write(f"**Equipment ID:** {alert['equipment_id']}")
    st.write(f"**Parameter:** {alert['parameter']}")
    st.write(
        f"**Value:** {alert['value']:.1f} {alert['unit']}"
    )
    st.write(f"**Status:** {alert['threshold_status']}")

    st.write("**Recommended Action:**")
    st.write(alert["recommended_action"])

    st.write("=====================================================")
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

    if equipment_data.empty:
        st.warning("No equipment records are available.")
        return

    # One entry per equipment ID.
    equipment_ids = (
        equipment_data["Equipment ID"]
        .drop_duplicates()
        .tolist()
    )

    if not equipment_ids:
        st.warning("No equipment IDs were found.")
        return

    # Initialise equipment navigation.
    if "notification_equipment_index" not in st.session_state:
        st.session_state["notification_equipment_index"] = 0

    index = st.session_state["notification_equipment_index"]
    index = max(0, min(index, len(equipment_ids) - 1))

    st.session_state["notification_equipment_index"] = index

    # Navigate between equipment.
    previous_col, selector_col, next_col = st.columns([1, 2, 1])

    with previous_col:
        if st.button(
            "Previous Equipment",
            disabled=(index == 0),
            use_container_width=True,
            key="notification_previous_equipment",
        ):
            st.session_state["notification_equipment_index"] = index - 1
            st.session_state["notification_alert_index"] = 0
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
            "Next Equipment",
            disabled=(index >= len(equipment_ids) - 1),
            use_container_width=True,
            key="notification_next_equipment",
        ):
            st.session_state["notification_equipment_index"] = index + 1
            st.session_state["notification_alert_index"] = 0
            st.rerun()

    selected_index = equipment_ids.index(selected_equipment)

    if selected_index != index:
        st.session_state["notification_equipment_index"] = selected_index
        st.session_state["notification_alert_index"] = 0
        st.rerun()

    st.caption(
        f"Equipment {selected_index + 1} of {len(equipment_ids)}"
    )

    # Get the selected equipment's readings only.
    selected_rows = equipment_data[
        equipment_data["Equipment ID"] == selected_equipment
    ]

    if selected_rows.empty:
        st.warning("No readings found for the selected equipment.")
        return

    equipment = selected_rows.iloc[0]

    temperature = float(equipment["Temperature"])
    vibration = float(equipment["Vibration"])
    equipment_type = equipment.get(
        "Equipment type", "Not specified"
    )

    # Show selected equipment details.
    st.divider()
    st.subheader("Selected Equipment")

    st.write(f"**Equipment ID:** {selected_equipment}")
    st.write(f"**Equipment Type:** {equipment_type}")

    temperature_col, vibration_col = st.columns(2)

    with temperature_col:
        st.metric("Temperature", f"{temperature:.1f} °C")

    with vibration_col:
        st.metric("Vibration", f"{vibration:.1f} mm/s")

    # Generate individual alerts for this equipment.
    equipment_alerts = []

    temperature_status = check_temperature(temperature)
    vibration_status = check_vibration(vibration)

    if temperature_status != "Normal":
        equipment_alerts.append({
            "equipment_id": selected_equipment,
            "parameter": "Temperature",
            "value": temperature,
            "unit": "°C",
            "status": temperature_status,
            "threshold_status": (
                "Above Critical Threshold"
                if temperature_status == "Critical"
                else "Above Warning Threshold"
            ),
            "recommended_action": (
                "Inspect equipment and initiate appropriate "
                "maintenance/safety procedures."
                if temperature_status == "Critical"
                else
                "Inspect equipment and arrange appropriate "
                "maintenance follow-up."
            ),
        })

    if vibration_status != "Normal":
        equipment_alerts.append({
            "equipment_id": selected_equipment,
            "parameter": "Vibration",
            "value": vibration,
            "unit": "mm/s",
            "status": vibration_status,
            "threshold_status": (
                "Above Critical Threshold"
                if vibration_status == "Critical"
                else "Above Warning Threshold"
            ),
            "recommended_action": (
                "Inspect equipment and initiate appropriate "
                "maintenance/safety procedures."
                if vibration_status == "Critical"
                else
                "Inspect equipment and arrange appropriate "
                "maintenance follow-up."
            ),
        })

    # Display a normal status if no alerts exist.
    if not equipment_alerts:
        st.divider()
        st.subheader("Equipment Status")
        st.success("NORMAL")
        st.write(
            "No temperature or vibration alerts for this equipment."
        )
        st.write(
            "**Recommended Action:** Continue routine monitoring."
        )
        return

    # Initialise navigation between this equipment's alerts.
    if "notification_alert_index" not in st.session_state:
        st.session_state["notification_alert_index"] = 0

    alert_index = st.session_state["notification_alert_index"]
    alert_index = max(0, min(alert_index, len(equipment_alerts) - 1))

    st.session_state["notification_alert_index"] = alert_index

    # Display different subheadings for each alert type.
    st.divider()

    if len(equipment_alerts) > 1:
        alert_previous_col, alert_count_col, alert_next_col = st.columns(
            [1, 1, 1]
        )

        with alert_previous_col:
            if st.button(
                "Previous Alert",
                disabled=(alert_index == 0),
                use_container_width=True,
                key="notification_previous_alert",
            ):
                st.session_state["notification_alert_index"] = alert_index - 1
                st.rerun()

        with alert_count_col:
            st.write(
                f"Alert {alert_index + 1} of {len(equipment_alerts)}"
            )

        with alert_next_col:
            if st.button(
                "Next Alert",
                disabled=(alert_index >= len(equipment_alerts) - 1),
                use_container_width=True,
                key="notification_next_alert",
            ):
                st.session_state["notification_alert_index"] = alert_index + 1
                st.rerun()

    selected_alert = equipment_alerts[alert_index]

    if selected_alert["parameter"] == "Temperature":
        st.subheader("Temperature Alert")
    else:
        st.subheader("Vibration Alert")

    display_mining_alert(selected_alert)


# --------------------------------------------------
# RUN PAGE DIRECTLY IF NEEDED
# --------------------------------------------------

if __name__ == "__main__":
    render_notifications_page()
