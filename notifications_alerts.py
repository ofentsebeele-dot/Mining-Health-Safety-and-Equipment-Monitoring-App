
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

    if temp_status == "Critical" or vibration_status == "Critical":
        alert_level = "Critical"
        alert_message = "Urgent equipment assessment required."

    elif temp_status == "Warning" or vibration_status == "Warning":
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
