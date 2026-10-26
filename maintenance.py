import streamlit as st
import pandas as pd
import os

EQUIPMENT_FILE = "equipment.csv"


def load_equipment_data():
    if not os.path.exists(EQUIPMENT_FILE):
        return pd.DataFrame(columns=[
            "Equipment ID", "Equipment type", "Manufacturer", "Operating hours",
            "Temperature", "Vibration", "Fuel consumption", "Brake status",
            "Tyre status", "Engine status", "Maintenance status", "Downtime"])
    return pd.read_csv(EQUIPMENT_FILE)


def save_equipment_data(equipment):
    os.makedirs(".", exist_ok=True)
    equipment.to_csv(EQUIPMENT_FILE, index=False)


def update_maintenance_section(equipment):
    st.subheader("Update Equipment Maintenance Status")

    if equipment.empty:
        st.info("No equipment records available to update.")
        return

    equipment_ids = sorted(equipment["Equipment ID"].astype(str).tolist())
    selected_id = st.selectbox("Select Equipment ID", equipment_ids)

    # Find current equipment status
    current_row = equipment[equipment["Equipment ID"].astype(str) == selected_id].iloc[0]
    current_status = str(current_row["Maintenance status"])
    current_downtime = float(current_row["Downtime"])

    status_choices = ["Operational", "Under Maintenance", "Due Soon", "Overdue"]
    default_index = status_choices.index(current_status) if current_status in status_choices else 0

    with st.form("update_maintenance_form"):
        new_status = st.selectbox("New Maintenance Status", status_choices, index=default_index)
        new_downtime = st.number_input("Total Downtime (hrs)", min_value=0.0, step=1.0, value=current_downtime)
        
        submitted = st.form_submit_button("Save Changes")

    if submitted:
        equipment.loc[equipment["Equipment ID"].astype(str) == selected_id, "Maintenance status"] = new_status
        equipment.loc[equipment["Equipment ID"].astype(str) == selected_id, "Downtime"] = new_downtime
        
        save_equipment_data(equipment)
        st.success(f"Equipment '{selected_id}' updated successfully!")
        st.rerun()


def render_maintenance_page():

    equipment = load_equipment_data()

    st.title("Maintenance Monitoring")

    st.write(
        "Monitor equipment maintenance status, downtime "
        "and operational condition.")

    st.divider()

    # Tabs for Dashboard & Records, and Updating Maintenance
    tab_dashboard, tab_update = st.tabs(["Maintenance Dashboard", "Update Status"])

    with tab_dashboard:
        if equipment.empty:
            st.info("No equipment records found.")
            return

        total_equipment = len(equipment)

        under_maintenance = len(
            equipment[
                equipment["Maintenance status"].astype(str).str.strip()
                == "Under Maintenance"] )

        operational = len(
            equipment[
                equipment["Maintenance status"].astype(str).str.strip()
                == "Operational"])

        total_downtime = equipment["Downtime"].sum()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Total Equipment",
                total_equipment)

        with col2:
            st.metric(
                "Operational",
                operational )

        with col3:
            st.metric(
                "Under Maintenance",
                under_maintenance)

        with col4:
            st.metric(
                "Total Downtime",
                f"{total_downtime:.1f} hrs" )

        st.divider()

        st.subheader("Maintenance Filter")

        status_options = (
            ["All"]
            + sorted(
                equipment["Maintenance status"]
                .dropna()
                .astype(str)
                .unique()
                .tolist() ) )

        selected_status = st.selectbox(
            "Maintenance Status",
            status_options,
            key="maintenance_status_filter")

        filtered_equipment = equipment.copy()

        if selected_status != "All":

            filtered_equipment = filtered_equipment[
                filtered_equipment["Maintenance status"].astype(str).str.strip()
                == selected_status ]

        st.divider()

        st.subheader("Maintenance Status Distribution")

        maintenance_counts = (
            filtered_equipment[
                "Maintenance status"]
            .astype(str)
            .value_counts())

        if not maintenance_counts.empty:

            st.bar_chart(
                maintenance_counts)

        else:

            st.info(
                "No maintenance records found.")

        st.divider()

        st.subheader(
            "Downtime by Equipment Type")

        if not filtered_equipment.empty:

            downtime_by_type = (
                filtered_equipment
                .groupby("Equipment type")["Downtime"]
                .sum()
                .sort_values(ascending=False))

            st.bar_chart(
                downtime_by_type )

        else:

            st.info(
                "No downtime data available." )

        st.divider()

        st.subheader("Maintenance Records")

        st.dataframe(
            filtered_equipment[
                [ "Equipment ID", "Equipment type", "Manufacturer", "Operating hours",  "Maintenance status", "Downtime", "Engine status", "Brake status", "Tyre status"]],
            use_container_width=True,
            hide_index=True)

    with tab_update:
        update_maintenance_section(equipment)
