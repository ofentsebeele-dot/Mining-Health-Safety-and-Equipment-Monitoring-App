import streamlit as st
import pandas as pd
import os

EQUIPMENT_FILE = "equipment.csv"


def load_equipment_data():
    """Load equipment data from equipment.csv."""
    file_path = EQUIPMENT_FILE

    if not os.path.exists(file_path):
        return pd.DataFrame()

    try:
        return pd.read_csv(file_path)
    except Exception as error:
        st.error(f"Unable to read equipment.csv: {error}")
        return pd.DataFrame()


def save_equipment_data(equipment):
    """Save equipment data to equipment.csv."""
    os.makedirs(".", exist_ok=True)
    equipment.to_csv(EQUIPMENT_FILE, index=False)


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


def add_equipment_section(equipment):
    """Add new equipment record section."""
    st.subheader("Add New Equipment")

    with st.form("add_equipment_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            equipment_id = st.text_input("Equipment ID (e.g., EQ-100)")
            equipment_type = st.selectbox("Equipment Type", ["Haul Truck", "Loader", "Excavator", "Drilling Machine", "Bulldozer", "Crusher", "Conveyor"])
            manufacturer = st.text_input("Manufacturer (e.g., Caterpillar, Komatsu)")
            operating_hours = st.number_input("Operating Hours", min_value=0.0, step=100.0, value=1000.0)
            temperature = st.number_input("Temperature (°C)", min_value=0.0, step=0.1, value=75.0)
            vibration = st.number_input("Vibration (mm/s)", min_value=0.0, step=0.1, value=3.5)

        with col2:
            fuel_consumption = st.number_input("Fuel Consumption", min_value=0.0, step=0.1, value=25.0)
            brake_status = st.selectbox("Brake Status", ["Good", "Warning", "Critical"])
            tyre_status = st.selectbox("Tyre Status", ["Good", "Warning", "Critical"])
            engine_status = st.selectbox("Engine Status", ["Good", "Warning", "Critical"])
            maintenance_status = st.selectbox("Maintenance Status", ["Operational", "Under Maintenance", "Due Soon", "Overdue"])
            downtime = st.number_input("Downtime (hrs)", min_value=0.0, step=1.0, value=10.0)

        submitted = st.form_submit_button("Add Equipment")

    if submitted:
        equipment_id = equipment_id.strip()
        if equipment_id == "":
            st.error("Equipment ID is required.")
            return

        if not equipment.empty and equipment_id in equipment["Equipment ID"].astype(str).values:
            st.error(f"Equipment ID '{equipment_id}' already exists.")
            return

        new_record = {
            "Equipment ID": equipment_id,
            "Equipment type": equipment_type,
            "Manufacturer": manufacturer,
            "Operating hours": operating_hours,
            "Temperature": temperature,
            "Vibration": vibration,
            "Fuel consumption": fuel_consumption,
            "Brake status": brake_status,
            "Tyre status": tyre_status,
            "Engine status": engine_status,
            "Maintenance status": maintenance_status,
            "Downtime": downtime
        }

        new_row = pd.DataFrame([new_record])
        updated_equipment = pd.concat([equipment, new_row], ignore_index=True)
        save_equipment_data(updated_equipment)

        st.success(f"Equipment '{equipment_id}' added successfully!")
        st.rerun()


def remove_equipment_section(equipment):
    """Remove equipment record section."""
    st.subheader("Remove Equipment Record")

    if equipment.empty:
        st.info("No equipment records available to remove.")
        return

    equipment_ids = sorted(equipment["Equipment ID"].astype(str).tolist())
    selected_id = st.selectbox("Select Equipment ID to Remove", equipment_ids)

    equipment_row = equipment[equipment["Equipment ID"].astype(str) == selected_id]
    st.write("**Selected Equipment Details:**")
    st.dataframe(equipment_row, use_container_width=True, hide_index=True)

    if st.button("Permanently Remove Equipment", type="primary"):
        updated_equipment = equipment[equipment["Equipment ID"].astype(str) != selected_id]
        save_equipment_data(updated_equipment)
        st.success(f"Equipment '{selected_id}' has been removed.")
        st.rerun()


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

    # Tabs to keep original dashboard intact while adding management features
    tab_dashboard, tab_add, tab_remove = st.tabs(["Equipment Dashboard", "Add Equipment", "Remove Equipment"])

    with tab_dashboard:
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

    with tab_add:
        add_equipment_section(equipment)

    with tab_remove:
        remove_equipment_section(equipment)


# Run the page when this file is executed directly
if __name__ == "__main__":
    render_equipment_page()
