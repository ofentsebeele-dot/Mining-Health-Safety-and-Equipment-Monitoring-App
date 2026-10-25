
import pandas as pd


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
        alert_message = "Urgent assessment required."

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


def load_incidents(file_path="incidents.csv"):
    data = pd.read_csv(file_path)
    data.columns = data.columns.astype(str).str.strip()
    return data.dropna(how="all")


def generate_incident_notifications(data):
    notifications = []

    for index, row in data.iterrows():
        incident_id = row.get(
            "Incident ID",
            row.get("ID", f"Incident {index + 1}")
        )

        description = row.get(
            "Description",
            row.get("Incident Type", "Safety incident")
        )

        severity = str(
            row.get("Severity", row.get("Priority", "Warning"))
        ).strip().lower()

        status = str(row.get("Status", "Open")).strip().lower()

        if status in ("closed", "resolved", "reviewed", "complete"):
            continue

        if severity in ("critical", "high", "severe", "urgent"):
            alert_level = "Critical"
        elif severity in ("low", "minor", "normal"):
            alert_level = "Normal"
        else:
            alert_level = "Warning"

        notifications.append({
            "incident_id": str(incident_id),
            "description": str(description),
            "alert_level": alert_level,
            "status": status,
        })

    return notifications
