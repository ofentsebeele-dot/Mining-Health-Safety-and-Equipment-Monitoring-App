import streamlit as st
import pandas as pd


def load_equipment_data():

    return pd.read_csv("equipment.csv")


def calculate_availability(equipment):

    total_time = (equipment["Operating hours"]+ equipment["Downtime"])

    availability = (equipment["Operating hours"]/ total_time) * 100

    return availability


def render_equipment_page():

    equipment = load_equipment_data()

    # Calculate availability from the CSV data.
    equipment["Availability"] = calculate_availability(equipment)

    st.title("Equipment Monitoring")

    st.write("Monitor mining equipment condition, operating hours, " "maintenance status and availability.")

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
        st.metric( "Total Downtime", f"{total_downtime:.1f} hrs")

    with col4:
        st.metric("Average Temperature", f"{average_temperature:.1f}")

    st.divider()

    # Filters

    st.subheader("Equipment Filters")

    col1, col2, col3 = st.columns(3)

    with col1:

        equipment_types = (equipment["Equipment type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist())

        equipment_types.sort()

        equipment_type_options = (["All"] + equipment_types)

        selected_type = st.selectbox("Equipment Type", equipment_type_options, key="equipment_type")

    with col2:

        maintenance_statuses = (equipment["Maintenance status"]
            .dropna()
            .astype(str)
            .unique()
            .tolist())

        maintenance_statuses.sort()

        maintenance_options = (["All"] + maintenance_statuses)

        selected_maintenance = st.selectbox("Maintenance Status", maintenance_options, key="equipment_maintenance")

    with col3:

        manufacturers = (equipment["Manufacturer"]
            .dropna()
            .astype(str)
            .unique()
            .tolist())

        manufacturers.sort()

        manufacturer_options = (["All"] + manufacturers)

        selected_manufacturer = st.selectbox("Manufacturer", manufacturer_options, key="equipment_manufacturer")

    # Apply Filters

    filtered_equipment = equipment.copy()

    if selected_type != "All":

        filtered_equipment = filtered_equipment[
            filtered_equipment["Equipment type"]
            .astype(str)
            == selected_type
        ]

    if selected_maintenance != "All":

        filtered_equipment = filtered_equipment[
            filtered_equipment["Maintenance status"]
            .astype(str)
            == selected_maintenance
        ]

    if selected_manufacturer != "All":

        filtered_equipment = filtered_equipment[
            filtered_equipment["Manufacturer"]
            .astype(str)
            == selected_manufacturer
        ]

    st.divider()

    # Equipment Condition

    st.subheader("Equipment Condition")

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

        st.info(
            "No equipment matches the selected filters."
        )

    st.divider()

    # Availability by Equipment Type

    st.subheader(
        "Average Availability by Equipment Type"
    )

    if not filtered_equipment.empty:

        availability_by_type = (
            filtered_equipment
            .groupby("Equipment type")["Availability"]
            .mean()
            .round(1)
        )

        st.bar_chart(
            availability_by_type
        )

    else:

        st.info(
            "No availability data available."
        )

    st.divider()

    # Operating Hours

    st.subheader("Operating Hours")

    if not filtered_equipment.empty:

        operating_hours = (
            filtered_equipment
            .groupby("Equipment type")["Operating hours"]
            .sum()
        )

        st.bar_chart(
            operating_hours
        )

    else:

        st.info(
            "No operating-hour data available."
        )

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

        st.bar_chart(
            downtime_by_type
        )

    else:

        st.info(
            "No downtime data available."
        )
