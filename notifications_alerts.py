MINN2020A: Computer Programming for Mining
Project section: Notifications, Pseudocode, Algorithms and Alerts

Purpose:
    Classify equipment temperature and vibration readings, then generate
    an alert based on the most serious condition.

Important:
    The thresholds below are educational prototype thresholds from the
    project brief. They are not actual manufacturer or mine safety limits.

Temperature rules:
    < 80 C       -> Normal
    80 to 100 C  -> Warning
    > 100 C      -> Critical

Vibration rules:
    < 5 mm/s     -> Normal
    5 to 8 mm/s  -> Warning
    > 8 mm/s     -> Critical
"""


def check_temperature(temperature):
    """Return the status for a temperature reading in degrees Celsius."""
    if temperature > 100:
        return "Critical"
    elif temperature >= 80:
        return "Warning"
    else:
        return "Normal"


def check_vibration(vibration):
    """Return the status for a vibration reading in mm/s."""
    if vibration > 8:
        return "Critical"
    elif vibration >= 5:
        return "Warning"
    else:
        return "Normal"


def generate_alert(equipment_id, temperature, vibration):
    """
    Classify both readings, display the statuses, and print the highest
    priority alert. Returns a dictionary that other application pages
    can use.
    """
    temp_status = check_temperature(temperature)
    vibration_status = check_vibration(vibration)

    print(f"Equipment ID: {equipment_id}")
    print(f"Temperature: {temperature} C -> {temp_status}")
    print(f"Vibration: {vibration} mm/s -> {vibration_status}")

    if temp_status == "Critical" or vibration_status == "Critical":
        alert_level = "Critical"
        alert_message = "CRITICAL ALERT: Urgent assessment required."
    elif temp_status == "Warning" or vibration_status == "Warning":
        alert_level = "Warning"
        alert_message = "WARNING: Equipment requires attention."
    else:
        alert_level = "Normal"
        alert_message = "NORMAL: No warning or critical alert."

    print(alert_message)

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
    """Run sample test cases for Normal, Warning, and Critical alerts."""
    test_cases = [
        ("EQ001", 65, 3),    # Normal
        ("EQ002", 85, 4),    # Warning: temperature
        ("EQ003", 70, 6),    # Warning: vibration
        ("EQ004", 105, 4),   # Critical: temperature
        ("EQ005", 75, 9),    # Critical: vibration
        ("EQ006", 90, 9),    # Critical: both readings at least Warning
    ]

    print("MINN2020A Equipment Alert System")
    print("=" * 34)

    for equipment_id, temperature, vibration in test_cases:
        print("\n" + "-" * 34)
        generate_alert(equipment_id, temperature, vibration)


if __name__ == "__main__":
    run_demo()
