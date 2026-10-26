import streamlit as st
import pandas as pd
import os


def load_equipment_data():
    """Load equipment data from equipment.csv."""
    file_path = "equipment.csv"

    if not os.path.exists(file_path):
        return pd.DataFrame()

    try:
        return pd.read_csv(file_path)
    except Exception as error:
        st.error(f"Unable to read equipment.csv: {error}")
        return pd.DataFrame()


def calculate_availability(equipment):
    """Calculate equipment availability as a percentage."""
    operating_hours = pd.to_numeric(
        equipment["Operating hours"], errors="coerce"
    ).fillna(0)

    downtime = pd.to_numeric(
        equipment["Downtime"], errors="coerce"
    ).fillna(0)

    total_time = operating_hours + downtime

    availability = (
        operating_hours / total_time.replace(0, 1)
    ) * 100

    return availability


def render_equipment_page():
    equipment = load_equipment_data()

    if equipment.empty:
        st.error(
            "Equipment data file ('equipment.csv') is missing or empty."
        )
        return

    # Check that the required CSV columns exist
    required_columns = ["Equipment ID", "Equipment type", "Manufacturer", "Operating hours", "Temperature",  "Vibration", "Fuel consumption", "Brake status", "Tyre status", "Engine status", "Maintenance status","Downtime" ]

    missing_columns = [
        column for column in required_columns
        if column not in equipment.columns]

    if missing_columns:
        st.error(
            "Missing columns in equipment.csv: "
            + ", ".join(missing_columns))
        return

    # Convert numerical columns safely
    numeric_columns = [ "Operating hours", "Temperature", "Vibration", "Fuel consumption", "Downtime" ]

    for column in numeric_columns:
        equipment[column] = pd.to_numeric(
            equipment[column], errors="coerce")

    # Calculate availability
    equipment["Availability"] = calculate_availability(equipment)

    # Page heading
    st.title("Equipment Monitoring")

    st.write(
        "Monitor mining equipment condition, operating hours, "
        "maintenance status and availability." )

    st.divider()

    # Equipment summary
    total_equipment = len(equipment)
    average_availability = equipment["Availability"].mean()
    total_downtime = equipment["Downtime"].sum()
    average_temperature = equipment["Temperature"].mean()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Equipment", total_equipment)

    with col2:
        availability_text = (
            f"{average_availability:.1f}%"
            if pd.notna(average_availability)
            else "N/A")
        st.metric("Average Availability", availability_text)

    with col3:
        downtime_text = (
            f"{total_downtime:.1f} hrs"
            if pd.notna(total_downtime)
            else "N/A")
        st.metric("Total Downtime", downtime_text)

    with col4:
        temperature_text = (
            f"{average_temperature:.1f}°C"
            if pd.notna(average_temperature)
            else "N/A")
        st.metric("Average Temperature", temperature_text)

    st.divider()

    # Equipment filters
    st.subheader("Equipment Filters")

    col1, col2, col3 = st.columns(3)

    with col1:
        equipment_types = sorted(
            equipment["Equipment type"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist() )

        selected_type = st.selectbox(
            "Equipment Type",
            ["All"] + equipment_types,
            key="equipment_type")

    with col2:
        maintenance_statuses = sorted(
            equipment["Maintenance status"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist() )

        selected_maintenance = st.selectbox(
            "Maintenance Status",
            ["All"] + maintenance_statuses,
            key="equipment_maintenance" )

    with col3:
        manufacturers = sorted(
            equipment["Manufacturer"]
            .dropna()
            .astype(str)
            .str.strip()
            .unique()
            .tolist())

        selected_manufacturer = st.selectbox(
            "Manufacturer",
            ["All"] + manufacturers,
            key="equipment_manufacturer")

    # Apply selected filters
    filtered_equipment = equipment.copy()

    if selected_type != "All":
        filtered_equipment = filtered_equipment[
            filtered_equipment["Equipment type"]
            .astype(str)
            .str.strip() == selected_type ]

    if selected_maintenance != "All":
        filtered_equipment = filtered_equipment[
            filtered_equipment["Maintenance status"]
            .astype(str)
            .str.strip() == selected_maintenance ]

    if selected_manufacturer != "All":
        filtered_equipment = filtered_equipment[
            filtered_equipment["Manufacturer"]
            .astype(str)
            .str.strip() == selected_manufacturer]

    st.divider()

    # Equipment condition records
    st.subheader("Equipment Condition Records")

    if not filtered_equipment.empty:
        condition_columns = ["Equipment ID", "Equipment type", "Manufacturer", "Operating hours", "Temperature", "Vibration", "Fuel consumption", "Brake status", "Tyre status",  "Engine status", "Maintenance status", "Downtime", "Availability"]

        condition_data = filtered_equipment[
            condition_columns
        ].copy()

        condition_data["Availability"] = (
            condition_data["Availability"].round(1))

        st.dataframe(
            condition_data,
            use_container_width=True,
            hide_index=True)
    else:
        st.info("No equipment matches the selected filters.")

    st.divider()

    # Average availability by equipment type
    st.subheader("Average Availability by Equipment Type")

    if not filtered_equipment.empty:
        availability_by_type = (
            filtered_equipment
            .groupby("Equipment type")["Availability"]
            .mean()
            .round(1))

        st.bar_chart(availability_by_type)
    else:
        st.info("No availability data available.")

    st.divider()

    # Downtime by equipment type
    st.subheader("Downtime by Equipment Type")

    if not filtered_equipment.empty:
        downtime_by_type = (
            filtered_equipment
            .groupby("Equipment type")["Downtime"]
            .sum()
            .sort_values(ascending=False))

        st.bar_chart(downtime_by_type)
    else:
        st.info("No downtime data available.")


# Run the page when this file is executed directly
if __name__ == "__main__":
    render_equipment_page()
