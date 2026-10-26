import pandas as pd
from pathlib import Path


# Find the equipment CSV file
def get_equipment_file():
    folder = Path(__file__).parent

    possible_files = [
        folder / "equipment(1).csv",
        folder / "equipment.csv",
        folder / "data" / "equipment.csv",
    ]

    for file_path in possible_files:
        if file_path.exists():
            return file_path

    raise FileNotFoundError(
        "Equipment CSV file not found. "
        "Place equipment(1).csv or equipment.csv "
        "in the same folder as this file."
    )


# Read equipment data from the CSV file
def load_equipment_data():
    file_path = get_equipment_file()
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
            "Missing CSV columns: "
            + ", ".join(missing_columns)
        )

    data["Equipment ID"] = (
        data["Equipment ID"]
        .astype("string")
        .str.strip()
    )

    data["Temperature"] = pd.to_numeric(
        data["Temperature"],
        errors="coerce"
    )

    data["Vibration"] = pd.to_numeric(
        data["Vibration"],
        errors="coerce"
    )

    data = data.dropna(
        subset=[
            "Equipment ID",
            "Temperature",
            "Vibration",
        ]
    )

    data = data[data["Equipment ID"] != ""]

    return data


# Check equipment temperature
def check_temperature(temperature):
    if temperature > 100:
        return "Critical"
    elif temperature >= 80:
        return "Warning"
    return "Normal"


# Check equipment vibration
def check_vibration(vibration):
    if vibration > 8:
        return "Critical"
    elif vibration >= 5:
        return "Warning"
    return "Normal"


# Generate an alert for one equipment item
def generate_alert(equipment_id, temperature, vibration):
    temp_status = check_temperature(temperature)
    vibration_status = check_vibration(vibration)

    if "Critical" in [temp_status, vibration_status]:
        alert_level = "Critical"
        alert_message = (
            "Urgent equipment assessment required."
        )

    elif "Warning" in [temp_status, vibration_status]:
        alert_level = "Warning"
        alert_message = "Equipment requires attention."

    else:
        alert_level = "Normal"
        alert_message = "Equipment readings are normal."

    return {
        "equipment_id": str(equipment_id),
        "temperature": float(temperature),
        "temperature_status": temp_status,
        "vibration": float(vibration),
        "vibration_status": vibration_status,
        "alert_level": alert_level,
        "alert_message": alert_message,
    }


# Check every equipment item and create notifications
def generate_notifications():
    equipment_data = load_equipment_data()
    notifications = []

    for _, row in equipment_data.iterrows():
        result = generate_alert(
            row["Equipment ID"],
            row["Temperature"],
            row["Vibration"],
        )

        if "Equipment type" in equipment_data.columns:
            result["equipment_type"] = row["Equipment type"]

        if result["alert_level"] in ["Warning", "Critical"]:
            notifications.append(result)

    return notifications


# Run a test of the notification system
def run_demo():
    try:
        equipment_data = load_equipment_data()
        notifications = generate_notifications()

        print(
            "Equipment records checked:",
            len(equipment_data)
        )

        print(
            "Notifications generated:",
            len(notifications)
        )

        if notifications:
            for notification in notifications:
                print("------------------------------")
                print(
                    "Equipment ID:",
                    notification["equipment_id"]
                )

                if "equipment_type" in notification:
                    print(
                        "Equipment Type:",
                        notification["equipment_type"]
                    )

                print(
                    "Temperature:",
                    notification["temperature"],
                    "°C"
                )

                print(
                    "Temperature Status:",
                    notification["temperature_status"]
                )

                print(
                    "Vibration:",
                    notification["vibration"],
                    "mm/s"
                )

                print(
                    "Vibration Status:",
                    notification["vibration_status"]
                )

                print(
                    "Alert Level:",
                    notification["alert_level"]
                )

                print(
                    "Notification:",
                    notification["alert_message"]
                )
        else:
            print(
                "There are no warnings or critical alerts."
            )

    except (
        FileNotFoundError,
        ValueError,
        pd.errors.ParserError,
    ) as error:
        print("Error:", error)


if __name__ == "__main__":
    run_demo()
