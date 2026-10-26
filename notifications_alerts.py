import streamlit as st
import pandas as pd
from pathlib import Path



def load_equipment_data():
    folder = Path(__file__).parent

    possible_files = [
        folder / "equipment(1).csv",
        folder / "equipment.csv",
        folder / "data" / "equipment.csv",
    ]

    file_path = None

    for path in possible_files:
        if path.exists():
            file_path = path
            break

    if file_path is None:
        raise FileNotFoundError(
            "Equipment CSV file not found. "
            "Place equipment(1).csv in the same folder as app.py."
        )

    data = pd.read_csv(file_path)

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
            "Missing CSV columns: " + ", ".join(missing_columns)
        )

    data["Equipment ID"] = (
        data["Equipment ID"].astype("string").str.strip()
    )

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
            "No valid equipment readings were found in the CSV."
        )

    return data




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
    temperature_status = check_temperature(temperature)
    vibration_status = check_vibration(vibration)

    if (
        temperature_status == "Critical"
        or vibration_status == "Critical"
    ):
        alert_level = "Critical"
        alert_message = "Urgent equipment assessment required."

    elif (
        temperature_status == "Warning"
        or vibration_status == "Warning"
    ):
        alert_level = "Warning"
        alert_message = "Equipment requires attention."

    else:
        alert_level = "Normal"
        alert_message = "Equipment readings are normal."

    return {
        "equipment_id": str(equipment_id),
        "temperature": float(temperature),
        "temperature_status": temperature_status,
        "vibration": float(vibration),
        "vibration_status": vibration_status,
        "alert_level": alert_level,
        "alert_message": alert_message,
    }



def generate_notifications():
    data = load_equipment_data()
    notifications = []

    for _, row in data.iterrows():
        equipment_id = str(row["Equipment ID"])
        equipment_type = row.get("Equipment type", "Not specified")

        temperature = float(row["Temperature"])
        vibration = float(row["Vibration"])

        # Create a separate alert for abnormal temperature.
        temperature_status = check_temperature(temperature)

        if temperature_status != "Normal":
            if temperature_status == "Critical":
                action = (
                    "Inspect equipment immediately and initiate "
                    "appropriate maintenance and safety procedures."
                )
            else:
                action = (
                    "Inspect the cooling system and monitor "
                    "equipment temperature."
                )

            notifications.append({
                "equipment_id": equipment_id,
                "equipment_type": equipment_type,
                "parameter": "Temperature",
                "value": temperature,
                "unit": "°C",
                "status": temperature_status,
                "threshold": (
                    "Above Critical Threshold"
                    if temperature_status == "Critical"
                    else "At or Above Warning Threshold"
                ),
                "recommended_action": action,
            })

        # Create a separate alert for abnormal vibration.
        vibration_status = check_vibration(vibration)

        if vibration_status != "Normal":
            if vibration_status == "Critical":
                action = (
                    "Inspect equipment and initiate appropriate "
                    "maintenance and safety procedures."
                )
            else:
                action = (
                    "Inspect equipment for excessive vibration "
                    "and arrange maintenance if necessary."
                )

            notifications.append({
                "equipment_id": equipment_id,
                "equipment_type": equipment_type,
                "parameter": "Vibration",
                "value": vibration,
                "unit": "mm/s",
                "status": vibration_status,
                "threshold": (
                    "Above Critical Threshold"
                    if vibration_status == "Critical"
                    else "At or Above Warning Threshold"
                ),
                "recommended_action": action,
            })

    # Display Critical alerts before Warning alerts.
    priority = {
        "Critical": 0,
        "Warning": 1,
    }

    notifications.sort(
        key=lambda alert: (
            priority[alert["status"]],
            alert["equipment_id"],
        )
    )

    return notifications




def display_mining_alert(alert):
    separator = "=" * 65

    st.markdown(f"**{separator}**")
    st.markdown("## MINING MONITORING ALERT")
    st.markdown(f"**{separator}**")

    st.markdown(f"### [{alert['status']}]")

    st.write(f"**Equipment ID:** {alert['equipment_id']}")
    st.write(f"**Equipment Type:** {alert['equipment_type']}")
    st.write(f"**Parameter:** {alert['parameter']}")
    st.write(
        f"**Value:** {alert['value']:.1f} {alert['unit']}"
    )
    st.write(f"**Status:** {alert['threshold']}")

    st.write("**Recommended Action:**")
    st.write(alert["recommended_action"])

    st.markdown(f"**{separator}**")
    st.caption("Figure 1: Mining monitoring alert.")



def render_notifications_page():
    st.title("Notifications & Alerts")

    try:
        data = load_equipment_data()
        notifications = generate_notifications()

    except (FileNotFoundError, ValueError, OSError) as error:
        st.error(str(error))
        return

    except pd.errors.ParserError:
        st.error("The equipment CSV file could not be read.")
        return

    # Summary counts
    critical_count = sum(
        1 for alert in notifications
        if alert["status"] == "Critical"
    )

    warning_count = sum(
        1 for alert in notifications
        if alert["status"] == "Warning"
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Critical Alerts", critical_count)
    col2.metric("Warnings", warning_count)
    col3.metric("Equipment Records", len(data))

    st.divider()

    # Equipment selection
    st.subheader("Check Equipment")

    equipment_ids = sorted(
        data["Equipment ID"].drop_duplicates().tolist()
    )

    selected_equipment = st.selectbox(
        "Select Equipment ID",
        equipment_ids,
        key="alert_equipment_selector",
    )

    selected_rows = data[
        data["Equipment ID"] == selected_equipment
    ]

    if selected_rows.empty:
        st.warning("No equipment data was found.")
        return

    row = selected_rows.iloc[0]

    equipment_type = row.get("Equipment type", "Not specified")
    csv_temperature = float(row["Temperature"])
    csv_vibration = float(row["Vibration"])

    st.write(f"**Equipment ID:** {selected_equipment}")
    st.write(f"**Equipment Type:** {equipment_type}")

    col1, col2 = st.columns(2)

    col1.metric(
        "Recorded Temperature",
        f"{csv_temperature:.1f} °C",
    )

    col2.metric(
        "Recorded Vibration",
        f"{csv_vibration:.1f} mm/s",
    )

    # Optional interactive test readings
    test_mode = st.checkbox(
        "Enter test readings",
        key=f"alert_test_mode_{selected_equipment}",
    )

    if test_mode:
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.0,
            max_value=500.0,
            value=csv_temperature,
            step=1.0,
            key=f"alert_test_temperature_{selected_equipment}",
        )

        vibration = st.number_input(
            "Vibration (mm/s)",
            min_value=0.0,
            max_value=100.0,
            value=csv_vibration,
            step=0.1,
            key=f"alert_test_vibration_{selected_equipment}",
        )
    else:
        temperature = csv_temperature
        vibration = csv_vibration

    # Check selected equipment
    if st.button(
        "Generate Equipment Alert",
        type="primary",
        key="generate_equipment_alert",
    ):
        result = generate_alert(
            selected_equipment,
            temperature,
            vibration,
        )

        st.session_state["latest_mining_alert"] = result
        st.session_state["latest_mining_alert"]["equipment_type"] = (
            equipment_type
        )

    # Display the result of the selected equipment check
    latest_alert = st.session_state.get("latest_mining_alert")

    if (
        latest_alert
        and latest_alert["equipment_id"] == selected_equipment
    ):
        st.divider()
        st.subheader("Selected Equipment Alert")

        temperature_status = check_temperature(
            latest_alert["temperature"]
        )

        vibration_status = check_vibration(
            latest_alert["vibration"]
        )

        # Display an alert for each abnormal parameter.
        parameter_alerts = []

        if temperature_status != "Normal":
            parameter_alerts.append({
                "equipment_id": selected_equipment,
                "equipment_type": equipment_type,
                "parameter": "Temperature",
                "value": latest_alert["temperature"],
                "unit": "°C",
                "status": temperature_status,
                "threshold": (
                    "Above Critical Threshold"
                    if temperature_status == "Critical"
                    else "At or Above Warning Threshold"
                ),
                "recommended_action": (
                    "Inspect equipment immediately and initiate "
                    "appropriate maintenance and safety procedures."
                    if temperature_status == "Critical"
                    else
                    "Inspect the cooling system and monitor "
                    "equipment temperature."
                ),
            })

        if vibration_status != "Normal":
            parameter_alerts.append({
                "equipment_id": selected_equipment,
                "equipment_type": equipment_type,
                "parameter": "Vibration",
                "value": latest_alert["vibration"],
                "unit": "mm/s",
                "status": vibration_status,
                "threshold": (
                    "Above Critical Threshold"
                    if vibration_status == "Critical"
                    else "At or Above Warning Threshold"
                ),
                "recommended_action": (
                    "Inspect equipment and initiate appropriate "
                    "maintenance and safety procedures."
                    if vibration_status == "Critical"
                    else
                    "Inspect equipment for excessive vibration "
                    "and arrange maintenance if necessary."
                ),
            })

        if parameter_alerts:
            for alert in parameter_alerts:
                display_mining_alert(alert)
        else:
            st.success(
                "Equipment readings are normal. "
                "No warning or critical alert was generated."
            )

    # Search and filter all equipment alerts
    st.divider()
    st.subheader("Equipment Alert Search")

    search_id = st.text_input(
        "Search Equipment ID",
        placeholder="Enter equipment ID",
        key="alert_search_id",
    )

    alert_filter = st.selectbox(
        "Filter Alerts",
        ["All", "Critical", "Warning"],
        key="alert_filter_level",
    )

    filtered_alerts = notifications

    if search_id.strip():
        filtered_alerts = [
            alert for alert in filtered_alerts
            if search_id.strip().lower()
            in alert["equipment_id"].lower()
        ]

    if alert_filter != "All":
        filtered_alerts = [
            alert for alert in filtered_alerts
            if alert["status"] == alert_filter
        ]

    if filtered_alerts:
        for alert in filtered_alerts:
            display_mining_alert(alert)
    else:
        st.success("No matching warning or critical alerts were found.")



if __name__ == "__main__":
    render_notifications_page()
