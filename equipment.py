import streamlit as st
import pandas as pd
import os
from notifications_alerts import generate_alert


def load_equipment_data():
    if not os.path.exists("equipment.csv"):
        return pd.DataFrame(columns=[
            "Equipment ID", "Equipment type", "Manufacturer", "Operating hours",
            "Temperature", "Vibration", "Fuel consumption", "Brake status",
            "Tyre status", "Engine status", "Maintenance status", "Downtime"
        ])
    return pd.read_csv("equipment.csv")


def calculate_availability(equipment):
    total_time = equipment["Operating hours"] + equipment["Downtime"]
    availability = (equipment["Operating hours"] / total_time.replace(0, 1)) * 100
    return availability


def render_equipment_page():
    equipment = load_equipment_data()

    if equipment.empty:
        st.error("Equipment data file ('equipment.csv') is missing or empty.")
        return

    equipment["Availability"] = calculate_availability(equipment)

    st.title("Equipment Monitoring")

    st.write("Monitor mining equipment condition, operating hours, maintenance status and availability.")

    st.divider()

    # Summary
    total_equipment = len(equipment)
    average_availability = equipment["Availability"].mean()
    total_downtime = equipment["Downtime"].sum()
    average_temperature = equipment["Temperature"].mean()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Equipment", total_equipment)

    with col2:
        st.metric("Average Availability", f"{average_availability:.1f}%")

    with col3:
        st.metric("Total Downtime", f"{total_downtime:.1f} hrs")

    with col4:
        st.metric("Average Temperature", f"{average_temperature:.1f}°C")

    st.divider()

    # Filters
    st.subheader("Equipment Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        equipment_types = sorted(equipment["Equipment type"].dropna().astype(str).unique().tolist())
        selected_type = st.selectbox("Equipment Type", ["All"] + equipment_types, key="equipment_type")

    with col2:
        maintenance_statuses = sorted(equipment["Maintenance status"].dropna().astype(str).unique().tolist())
        selected_maintenance = st.selectbox("Maintenance Status", ["All"] + maintenance_statuses, key="equipment_maintenance")

    with col3:
        manufacturers = sorted(equipment["Manufacturer"].dropna().astype(str).unique().tolist())
        selected_manufacturer = st.selectbox("Manufacturer", ["All"] + manufacturers, key="equipment_manufacturer")

    # Apply Filters (Robust String Matching)
    filtered_equipment = equipment.copy()

    if selected_type != "All":
        filtered_equipment = filtered_equipment[
            filtered_equipment["Equipment type"].astype(str).str.strip() == selected_type
        ]

    if selected_maintenance != "All":
        filtered_equipment = filtered_equipment[
            filtered_equipment["Maintenance status"].astype(str).str.strip() == selected_maintenance
        ]

    if selected_manufacturer != "All":
        filtered_equipment = filtered_equipment[
            filtered_equipment["Manufacturer"].astype(str).str.strip() == selected_manufacturer
        ]

    st.divider()

    # Automated Alerts Integration (Section 3h)
    st.subheader("Automated Equipment Alerts")
    alert_triggered = False
    for _, row in filtered_equipment.iterrows():
        alert_info = generate_alert(row["Equipment ID"], row["Temperature"], row["Vibration"])
        if alert_info["alert_level"] == "Critical":
            alert_triggered = True
            st.error(f"**[CRITICAL] Equipment ID:** {alert_info['equipment_id']} | Temp: {alert_info['temperature']}°C ({alert_info['temperature_status']}) | Vib: {alert_info['vibration']} mm/s ({alert_info['vibration_status']}) — {alert_info['alert_message']}")
        elif alert_info["alert_level"] == "Warning":
            alert_triggered = True
            st.warning(f"**[WARNING] Equipment ID:** {alert_info['equipment_id']} | Temp: {alert_info['temperature']}°C ({alert_info['temperature_status']}) | Vib: {alert_info['vibration']} mm/s ({alert_info['vibration_status']}) — {alert_info['alert_message']}")

    if not alert_triggered:
        st.success("NORMAL: All filtered equipment operating within defined monitoring limits.")

    st.divider()

    # Equipment Condition
    st.subheader("Equipment Condition Records")

    if not filtered_equipment.empty:
        condition_data = filtered_equipment[
            [
                "Equipment ID",
                "Equipment type",
                "Manufacturer",
                "Operating hours",
                "Temperature",
                "Vibration",
                "Fuel consumption",
                "Brake status",
                "Tyre status",
                "Engine status",
                "Maintenance status",
                "Downtime",
                "Availability"
            ]
        ]

        st.dataframe(
            condition_data,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No equipment matches the selected filters.")

    st.divider()

    # Availability by Equipment Type
    st.subheader("Average Availability by Equipment Type")

    if not filtered_equipment.empty:
        availability_by_type = (
            filtered_equipment
            .groupby("Equipment type")["Availability"]
            .mean()
            .round(1)
        )
        st.bar_chart(availability_by_type)
    else:
        st.info("No availability data available.")

    st.divider()

    # Downtime
    st.subheader("Downtime by Equipment Type")

    if not filtered_equipment.empty:
        downtime_by_type = (
            filtered_equipment
            .groupby("Equipment type")["Downtime"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(downtime_by_type)
    else:
        st.info("No downtime data available.")