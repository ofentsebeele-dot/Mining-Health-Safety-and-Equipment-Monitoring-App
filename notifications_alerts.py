
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

    temp_status = check_temperature(temperature)
    vibration_status = check_vibration(vibration)

    if "Critical" in [temp_status, vibration_status]:
        alert_level = "Critical"
        alert_message = "Urgent equipment assessment required."

    elif "Warning" in [temp_status, vibration_status]:
        alert_level = "Warning"
        alert_message = "Equipment requires attention."

    else:
        alert_level = "Normal"
        alert_message = "Equipment readings are normal."

    return {
        "equipment_id": equipment_id,
        "temperature": temperature,
        "temperature_status": temp_status,
        "vibration": vibration,
        "vibration_status": vibration_status,
        "alert_level": alert_level,
        "alert_message": alert_message,
    }


def run_demo():

    test_cases = [
        ("EQ001", 65, 3),
        ("EQ002", 85, 4),
        ("EQ003", 70, 6),
        ("EQ004", 105, 4),
        ("EQ005", 75, 9),
        ("EQ006", 90, 9),
    ]

    for equipment_id, temperature, vibration in test_cases:

        result = generate_alert(
            equipment_id,
            temperature,
            vibration
        )

        print(result)


if __name__ == "__main__":
    run_demo()
