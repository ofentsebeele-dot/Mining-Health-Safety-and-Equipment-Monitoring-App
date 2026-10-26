import streamlit as st
import pandas as pd
from pathlib import Path


# --------------------------------------------------
# LOAD EQUIPMENT DATA
# --------------------------------------------------

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
            "The CSV file contains no valid equipment readings."
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
# GENERATE AN ALERT
# --------------------------------------------------

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


# --------------------------------------------------
# GENERATE NOTIFICATIONS FROM CSV DATA
# --------------------------------------------------

def generate_notifications():
    data = load_equipment_data()
    notifications = []

    for _, row in data.iterrows():
        result = generate_alert(
            row["Equipment ID"],
            row["Temperature"],
            row["Vibration"],
        )

        if "Equipment type" in data.columns:
            result["equipment_type"] = row["Equipment type"]

        if result["alert_level"] in ["Warning", "Critical"]:
            notifications.append(result)

    return notifications


# --------------------------------------------------
# INTERACTIVE NOTIFICATIONS PAGE
# --------------------------------------------------

def render_notifications_page():
    st.title("Notifications & Alerts")

    try:
        data = load_equipment_data()

    except (FileNotFoundError, ValueError, OSError) as error:
        st.error(str(error))
        return

    # Initialise session state
    if "equipment_checks" not in st.session_state:
        st.session_state["equipment_checks"] = {}

    if "pending_alerts" not in st.session_state:
        st.session_state["pending_alerts"] = {}

    # Generate notifications from current CSV readings
    current_alerts = generate_notifications()

    current_alert_ids = {
        alert["equipment_id"] for alert in current_alerts
    }

    # Update alerts automatically
    for alert in current_alerts:
        equipment_id = alert["equipment_id"]

        st.session_state["pending_alerts"][equipment_id] = alert

    # Remove alerts that are no longer Warning or Critical
    for equipment_id in list(
        st.session_state["pending_alerts"].keys()
    ):
        if equipment_id not in current_alert_ids:
            st.session_state["pending_alerts"].pop(
                equipment_id, None
            )

    # Summary
    critical_count = sum(
        1 for alert in current_alerts
        if alert["alert_level"] == "Critical"
    )

    warning_count = sum(
        1 for alert in current_alerts
        if alert["alert_level"] == "Warning"
    )

    pending_count = len(st.session_state["pending_alerts"])

    col1, col2, col3 = st.columns(3)

    col1.metric("Critical Alerts", critical_count)
    col2.metric("Warnings", warning_count)
    col3.metric("Active Notifications", pending_count)

    st.divider()

    # Equipment selection
    equipment_ids = sorted(
        data["Equipment ID"].drop_duplicates().tolist()
    )

    selected_equipment = st.selectbox(
        "Select Equipment",
        equipment_ids,
        key="notification_equipment",
    )

    selected_rows = data[
        data["Equipment ID"] == selected_equipment
    ]

    if selected_rows.empty:
        st.warning("No data found for this equipment.")
        return

    row = selected_rows.iloc[0]

    st.subheader("Equipment Information")

    st.write("Equipment ID:", selected_equipment)

    if "Equipment type" in data.columns:
        st.write("Equipment Type:", row["Equipment type"])

    csv_temperature = float(row["Temperature"])
    csv_vibration = float(row["Vibration"])

    col1, col2 = st.columns(2)

    col1.metric(
        "Recorded Temperature",
        f"{csv_temperature:.1f} °C",
    )

    col2.metric(
        "Recorded Vibration",
        f"{csv_vibration:.1f} mm/s",
    )

    # Test readings
    test_mode = st.checkbox(
        "Enter test readings",
        key=f"test_mode_{selected_equipment}",
    )

    if test_mode:
        temperature = st.number_input(
            "Test Temperature (°C)",
            min_value=0.0,
            max_value=500.0,
            value=csv_temperature,
            step=1.0,
            key=f"test_temperature_{selected_equipment}",
        )

        vibration = st.number_input(
            "Test Vibration (mm/s)",
            min_value=0.0,
            max_value=100.0,
            value=csv_vibration,
            step=0.5,
            key=f"test_vibration_{selected_equipment}",
        )
    else:
        temperature = csv_temperature
        vibration = csv_vibration

    # Check selected equipment
    if st.button(
        "Check Equipment",
        type="primary",
        key="check_notification_equipment",
    ):
        result = generate_alert(
            selected_equipment,
            temperature,
            vibration,
        )

        if "Equipment type" in data.columns:
            result["equipment_type"] = row["Equipment type"]

        st.session_state["equipment_checks"][
            selected_equipment
        ] = result

        if result["alert_level"] in ["Warning", "Critical"]:
            st.session_state["pending_alerts"][
                selected_equipment
            ] = result
        else:
            st.session_state["pending_alerts"].pop(
                selected_equipment, None
            )

        st.rerun()

    # Latest check
    st.divider()
    st.subheader("Latest Equipment Check")

    latest_result = st.session_state["equipment_checks"].get(
        selected_equipment
    )

    if latest_result:
        st.write("Alert Level:", latest_result["alert_level"])
        st.write(latest_result["alert_message"])

        col1, col2 = st.columns(2)

        col1.metric(
            "Temperature Status",
            latest_result["temperature_status"],
        )

        col2.metric(
            "Vibration Status",
            latest_result["vibration_status"],
        )

        if latest_result["alert_level"] == "Critical":
            st.error("Urgent equipment assessment required.")

        elif latest_result["alert_level"] == "Warning":
            st.warning("Equipment requires attention.")

        else:
            st.success("Equipment readings are normal.")

    else:
        st.info(
            "Select equipment and click Check Equipment "
            "to generate a result."
        )

    # Notifications without review buttons
    st.divider()
    st.subheader("Active Notifications")

    pending_alerts = st.session_state["pending_alerts"]

    if pending_alerts:
        for equipment_id, alert in pending_alerts.items():
            with st.container(border=True):
                st.write("Equipment ID:", equipment_id)

                if "equipment_type" in alert:
                    st.write(
                        "Equipment Type:",
                        alert["equipment_type"],
                    )

                st.write("Alert Level:", alert["alert_level"])
                st.write(alert["alert_message"])

                st.write(
                    f"Temperature: {alert['temperature']:.1f} °C"
                )

                st.write(
                    f"Vibration: {alert['vibration']:.1f} mm/s"
                )

    else:
        st.success("There are no active warnings or critical alerts.")

    # Search and filter equipment readings
    st.divider()
    st.subheader("All Equipment Readings")

    display_data = data.copy()

    display_data["Temperature Status"] = display_data[
        "Temperature"
    ].apply(check_temperature)

    display_data["Vibration Status"] = display_data[
        "Vibration"
    ].apply(check_vibration)

    display_data["Alert Level"] = display_data.apply(
        lambda item: generate_alert(
            item["Equipment ID"],
            item["Temperature"],
            item["Vibration"],
        )["alert_level"],
        axis=1,
    )

    search_id = st.text_input(
        "Search Equipment ID",
        placeholder="Enter equipment ID",
    )

    if search_id.strip():
        display_data = display_data[
            display_data["Equipment ID"].str.contains(
                search_id.strip(),
                case=False,
                na=False,
            )
        ]

    alert_filter = st.selectbox(
        "Filter by Alert Level",
        ["All", "Normal", "Warning", "Critical"],
    )

    if alert_filter != "All":
        display_data = display_data[
            display_data["Alert Level"] == alert_filter
        ]

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True,
    )


# --------------------------------------------------
# RUN AS A STREAMLIT PAGE
# --------------------------------------------------

if __name__ == "__main__":
    render_notifications_page()
