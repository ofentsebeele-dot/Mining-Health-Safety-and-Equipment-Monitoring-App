import streamlit as st
import pandas as pd


def load_equipment_data():
    return pd.read_csv("equipment.csv")


def calculate_availability(equipment):
    total_time = (equipment["Operating hours"] + equipment["Downtime"])
    availability = (equipment["Operating hours"] / total_time) * 100
    return availability


def evaluate_thresholds(row):
    temp = row["Temperature"]
    vib = row["Vibration"]

    # Temperature checks
    if temp > 100:
        temp_status = "CRITICAL (>100°C)"[cite: 19]
    elif temp >= 80:
        temp_status = "WARNING (80-100°C)"[cite: 19]
    else:
        temp_status = "NORMAL (<80°C)"[cite: 19]

    # Vibration checks
    if vib > 8:
        vib_status = "CRITICAL (>8 mm/s)"[cite: 19]
    elif vib >= 5:
        vib_status = "WARNING (5-8 mm/s)"[cite: 19]
    else:
        vib_status = "NORMAL (<5 mm/s)"[cite: 19]

    return temp_status, vib_status


def render_equipment_page():

    equipment = load_equipment_data()

    # Calculate availability from CSV data
    equipment["Availability"] = calculate_availability(equipment)

    st.title("Equipment Monitoring & Condition Thresholds")
    st.write("Monitor mining equipment condition, operating hours, maintenance status and availability against educational threshold limits.")

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

    # Threshold Reference Guide
    with st.expander("ℹ️ View Educational Parameter Thresholds Guide"):
        st.markdown("""
| Parameter | Normal | Warning | Critical |
|---|---|---|---|
| **Temperature** | $<80^\circ\text{C}$[cite: 19] | $80-100^\circ\text{C}$[cite: 19] | $>100^\circ\text{C}$[cite: 19] |
| **Vibration** | $<5\text{ mm/s}$[cite: 19] | $5-8\text{ mm/s}$[cite: 19] | $>8\text{ mm/s}$[cite: 19] |
""")

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

    # Apply Filters
    filtered_equipment = equipment.copy()

    if selected_type != "All":
        filtered_equipment = filtered_equipment[filtered_equipment["Equipment type"].astype(str) == selected_type]

    if selected_maintenance != "All":
        filtered_equipment = filtered_equipment[filtered_equipment["Maintenance status"].astype(str) == selected_maintenance]

    if selected_manufacturer != "All":
        filtered_equipment = filtered_equipment[filtered_equipment["Manufacturer"].astype(str) == selected_manufacturer]

    st.divider()

    # Equipment Condition & Threshold Evaluations
    st.subheader("Equipment Condition & Parameter Status")

    if not filtered_equipment.empty:
        # Add evaluated threshold columns
        display_df = filtered_equipment.copy()
        display_df["Temp Status"], display_df["Vib Status"] = zip(*display_df.apply(evaluate_thresholds, axis=1))

        condition_data = display_df[[
            "Equipment ID", "Equipment type", "Manufacturer", "Operating hours",
            "Temperature", "Temp Status", "Vibration", "Vib Status",
            "Fuel consumption", "Brake status", "Tyre status", "Engine status",
            "Maintenance status", "Downtime", "Availability"
        ]]

        st.dataframe(condition_data, use_container_width=True, hide_index=True)

    else:
        st.info("No equipment matches the selected filters.")

    st.divider()

    # Availability by Equipment Type
    st.subheader("Average Availability by Equipment Type")
    if not filtered_equipment.empty:
        availability_by_type = filtered_equipment.groupby("Equipment type")["Availability"].mean().round(1)
        st.bar_chart(availability_by_type)
    else:
        st.info("No availability data available.")

    st.divider()

    # Operating Hours
    st.subheader("Operating Hours")
    if not filtered_equipment.empty:
        operating_hours = filtered_equipment.groupby("Equipment type")["Operating hours"].sum()
        st.bar_chart(operating_hours)
    else:
        st.info("No operating-hour data available.")

    st.divider()

    # Downtime
    st.subheader("Downtime by Equipment Type")
    if not filtered_equipment.empty:
        downtime_by_type = filtered_equipment.groupby("Equipment type")["Downtime"].sum().sort_values(ascending=False)
        st.bar_chart(downtime_by_type)
    else:
        st.info("No downtime data available.")
