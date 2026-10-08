import streamlit as st
import pandas as pd
import os


# --------------------------------------------------
# LOAD EQUIPMENT DATA
# --------------------------------------------------

def load_equipment_data():

    # Load equipment data from the CSV file
    return pd.read_csv("equipment.csv")


# --------------------------------------------------
# RENDER MAINTENANCE PAGE
# --------------------------------------------------

def render_maintenance_page():

    # Load equipment information
    try:
        equipment = load_equipment_data()

    except FileNotFoundError:
        st.error(
            "Equipment file not found. "
            "Please check that equipment.csv is available."
        )
        return

    except Exception as error:
        st.error(f"Could not load equipment data: {error}")
        return

    # Check that important columns are available
    required_columns = [
        "Equipment ID",
        "Equipment type",
        "Maintenance status",
        "Operating hours",
        "Downtime"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in equipment.columns
    ]

    if missing_columns:
        st.error(
            "Missing required columns: "
            + ", ".join(missing_columns)
        )
        return

    if equipment.empty:
        st.warning("There is no equipment data to display.")
        return

    # Convert measurements to numeric values
    for column in [
        "Operating hours",
        "Downtime",
        "Temperature",
        "Vibration",
        "Availability"
    ]:
        if column in equipment.columns:
            equipment[column] = pd.to_numeric(
                equipment[column],
                errors="coerce"
            )

    # Create optional columns if they do not exist
    for column in [
        "Temperature",
        "Vibration",
        "Availability",
        "Manufacturer",
        "Engine status",
        "Brake status",
        "Tyre status"
    ]:
        if column not in equipment.columns:
            equipment[column] = pd.NA

    # Calculate availability from the available data.
    # This assumes Operating hours represents operating time
    # for the same period as Downtime.
    total_time = (
        equipment["Operating hours"] + equipment["Downtime"]
    )

    equipment["Availability"] = (
        equipment["Operating hours"]
        .div(total_time.where(total_time > 0))
        .mul(100)
    )

    # Calculate equipment condition
    def temperature_status(value):

        if pd.isna(value):
            return "Data unavailable"

        if value < 80:
            return "NORMAL"

        if value <= 100:
            return "WARNING"

        return "CRITICAL"

    def vibration_status(value):

        if pd.isna(value):
            return "Data unavailable"

        if value < 5:
            return "NORMAL"

        if value <= 8:
            return "WARNING"

        return "CRITICAL"

    equipment["Temperature Status"] = (
        equipment["Temperature"].apply(temperature_status)
    )

    equipment["Vibration Status"] = (
        equipment["Vibration"].apply(vibration_status)
    )

    # Identify equipment requiring attention
    def maintenance_reason(row):

        reasons = []

        if row["Temperature Status"] == "CRITICAL":
            reasons.append("Critical temperature")

        if row["Vibration Status"] == "CRITICAL":
            reasons.append("Critical vibration")

        if (
            pd.notna(row["Availability"])
            and row["Availability"] < 80
        ):
            reasons.append("Low availability")

        if (
            pd.notna(row["Downtime"])
            and row["Downtime"] > 24
        ):
            reasons.append("Excessive downtime")

        for column in [
            "Engine status",
            "Brake status",
            "Tyre status"
        ]:
            value = str(row[column]).strip().lower()

            if value not in [
                "good",
                "normal",
                "operational",
                "nan",
                "<na>",
                ""
            ]:
                reasons.append(f"Check {column.lower()}")

        status = str(row["Maintenance status"]).strip().lower()

        if "overdue" in status:
            reasons.append("Overdue maintenance")

        elif "due" in status:
            reasons.append("Maintenance due")

        elif "under maintenance" in status:
            reasons.append("Under maintenance")

        if reasons:
            return "; ".join(reasons)

        return "No issue identified by current rules"

    equipment["Maintenance Issue"] = equipment.apply(
        maintenance_reason,
        axis=1
    )

    # --------------------------------------------------
    # PAGE TITLE
    # --------------------------------------------------

    st.title("🔧 Maintenance Monitoring")

    st.write(
        "Search equipment, monitor its condition, filter records, "
        "and record maintenance actions."
    )

    st.caption(
        "Educational prototype thresholds: temperature below "
        "80°C is normal, 80–100°C is a warning, and above 100°C "
        "is critical. Vibration below 5 mm/s is normal, "
        "5–8 mm/s is a warning, and above 8 mm/s is critical. "
        "These are not actual manufacturer or mine safety limits."
    )

    st.divider()

    # --------------------------------------------------
    # SUMMARY CARDS
    # --------------------------------------------------

    total_equipment = len(equipment)

    status = (
        equipment["Maintenance status"]
        .fillna("")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    under_maintenance = int(
        status.str.contains(
            "under maintenance",
            regex=False
        ).sum()
    )

    operational = int(
        status.isin(["operational", "normal"]).sum()
    )

    total_downtime = equipment["Downtime"].sum()

    average_availability = equipment["Availability"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Equipment", total_equipment)
    col2.metric("Operational", operational)
    col3.metric("Under Maintenance", under_maintenance)
    col4.metric(
        "Total Downtime",
        f"{total_downtime:.1f} hrs"
    )

    col5, col6 = st.columns(2)

    if pd.notna(average_availability):
        col5.metric(
            "Average Availability",
            f"{average_availability:.1f}%"
        )
    else:
        col5.metric("Average Availability", "N/A")

    col6.metric(
        "Equipment Requiring Attention",
        int(
            (
                equipment["Maintenance Issue"]
                != "No issue identified by current rules"
            ).sum()
        )
    )

    st.divider()

    # --------------------------------------------------
    # INTERACTIVE SEARCH AND FILTERS
    # --------------------------------------------------

    st.subheader("🔎 Search and Filter Equipment")

    search_col, type_col, status_col = st.columns(3)

    with search_col:
        search_id = st.text_input(
            "Search Equipment ID",
            placeholder="e.g. HT-001"
        )

    with type_col:
        type_options = ["All"] + sorted(
            equipment["Equipment type"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_type = st.selectbox(
            "Equipment Type",
            type_options
        )

    with status_col:
        status_options = ["All"] + sorted(
            equipment["Maintenance status"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_status = st.selectbox(
            "Maintenance Status",
            status_options
        )

    filtered_equipment = equipment.copy()

    if search_id.strip():
        filtered_equipment = filtered_equipment[
            filtered_equipment["Equipment ID"]
            .astype(str)
            .str.contains(
                search_id.strip(),
                case=False,
                na=False
            )
        ]

    if selected_type != "All":
        filtered_equipment = filtered_equipment[
            filtered_equipment["Equipment type"].astype(str)
            == selected_type
        ]

    if selected_status != "All":
        filtered_equipment = filtered_equipment[
            filtered_equipment["Maintenance status"].astype(str)
            == selected_status
        ]

    st.write(
        f"**{len(filtered_equipment)} equipment record(s) found.**"
    )

    st.divider()

    # --------------------------------------------------
    # SELECT EQUIPMENT FOR DETAILED INSPECTION
    # --------------------------------------------------

    st.subheader("🛠️ Equipment Inspection")

    equipment_ids = (
        filtered_equipment["Equipment ID"]
        .dropna()
        .astype(str)
        .tolist()
    )

    if equipment_ids:

        selected_equipment_id = st.selectbox(
            "Select Equipment to Inspect",
            equipment_ids,
            key="selected_maintenance_equipment"
        )

        selected_equipment = filtered_equipment[
            filtered_equipment["Equipment ID"].astype(str)
            == selected_equipment_id
        ].iloc[0]

        st.markdown(
            f"### Equipment: {selected_equipment_id}"
        )

        detail1, detail2, detail3 = st.columns(3)

        detail1.metric(
            "Operating Hours",
            (
                f"{selected_equipment['Operating hours']:.1f}"
                if pd.notna(selected_equipment["Operating hours"])
                else "N/A"
            )
        )

        detail2.metric(
            "Temperature",
            (
                f"{selected_equipment['Temperature']:.1f} °C"
                if pd.notna(selected_equipment["Temperature"])
                else "N/A"
            )
        )

        detail3.metric(
            "Vibration",
            (
                f"{selected_equipment['Vibration']:.1f} mm/s"
                if pd.notna(selected_equipment["Vibration"])
                else "N/A"
            )
        )

        st.write(
            "**Temperature condition:** "
            + selected_equipment["Temperature Status"]
        )

        st.write(
            "**Vibration condition:** "
            + selected_equipment["Vibration Status"]
        )

        st.write(
            "**Maintenance issue:** "
            + selected_equipment["Maintenance Issue"]
        )

        st.write(
            "**Availability:** "
            + (
                f"{selected_equipment['Availability']:.1f}%"
                if pd.notna(selected_equipment["Availability"])
                else "Unavailable"
            )
        )

    else:
        st.info(
            "No equipment matches your search and filter settings."
        )

    st.divider()

    # --------------------------------------------------
    # MAINTENANCE STATUS CHART
    # --------------------------------------------------

    st.subheader("📊 Maintenance Status")

    if not filtered_equipment.empty:

        maintenance_counts = (
            filtered_equipment["Maintenance status"]
            .fillna("Unknown")
            .astype(str)
            .value_counts()
        )

        st.bar_chart(maintenance_counts)

    else:
        st.info("No maintenance records available.")

    st.divider()

    # --------------------------------------------------
    # DOWNTIME BY EQUIPMENT TYPE
    # --------------------------------------------------

    st.subheader("⏱️ Downtime by Equipment Type")

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

    st.divider()

    # --------------------------------------------------
    # MAINTENANCE ALERTS
    # --------------------------------------------------

    st.subheader("🚨 Equipment Requiring Attention")

    attention_equipment = filtered_equipment[
        filtered_equipment["Maintenance Issue"]
        != "No issue identified by current rules"
    ]

    if not attention_equipment.empty:

        st.dataframe(
            attention_equipment[
                [
                    "Equipment ID",
                    "Equipment type",
                    "Temperature",
                    "Temperature Status",
                    "Vibration",
                    "Vibration Status",
                    "Availability",
                    "Downtime",
                    "Maintenance Issue"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success(
            "No equipment has been flagged by the current rules."
        )

    st.divider()

    # --------------------------------------------------
    # RECORD MAINTENANCE ACTION
    # --------------------------------------------------

    st.subheader("📝 Record Maintenance Action")

    st.write(
        "Complete this form to prepare a maintenance record. "
        "Records are saved to a CSV file."
    )

    with st.form("maintenance_action_form"):

        action_equipment_id = st.selectbox(
            "Equipment ID",
            equipment["Equipment ID"]
            .dropna()
            .astype(str)
            .unique()
            .tolist(),
            key="action_equipment_id"
        )

        problem = st.text_input(
            "Problem Identified",
            placeholder="e.g. Excessive vibration"
        )

        action_taken = st.text_area(
            "Maintenance Action",
            placeholder="Describe the inspection or repair required."
        )

        technician = st.text_input(
            "Assigned Technician or Engineer"
        )

        action_status = st.selectbox(
            "Action Status",
            [
                "Scheduled",
                "In Progress",
                "Completed",
                "On Hold"
            ]
        )

        submitted = st.form_submit_button(
            "Save Maintenance Record"
        )

        if submitted:

            if not problem.strip() or not action_taken.strip():
                st.error(
                    "Please enter the problem and maintenance action."
                )

            else:

                new_record = pd.DataFrame([{
                    "Equipment ID": action_equipment_id,
                    "Problem Identified": problem.strip(),
                    "Maintenance Action": action_taken.strip(),
                    "Assigned Technician": technician.strip(),
                    "Action Status": action_status,
                    "Recorded At": pd.Timestamp.now()
                }])

                records_file = "maintenance_records.csv"

                try:

                    if os.path.exists(records_file):

                        old_records = pd.read_csv(records_file)

                        new_record = pd.concat(
                            [old_records, new_record],
                            ignore_index=True
                        )

                    new_record.to_csv(
                        records_file,
                        index=False
                    )

                    st.success(
                        "Maintenance action saved successfully."
                    )

                except Exception as error:

                    st.error(
                        f"Could not save maintenance record: {error}"
                    )

    # --------------------------------------------------
    # VIEW SAVED MAINTENANCE ACTIONS
    # --------------------------------------------------

    st.divider()

    st.subheader("📋 Saved Maintenance Actions")

    records_file = "maintenance_records.csv"

    if os.path.exists(records_file):

        try:

            saved_records = pd.read_csv(records_file)

            st.dataframe(
                saved_records,
                use_container_width=True,
                hide_index=True
            )

        except Exception as error:

            st.error(
                f"Could not read saved maintenance actions: {error}"
            )

    else:

        st.info(
            "No maintenance actions have been recorded yet."
        )

    # --------------------------------------------------
    # VIEW ALL EQUIPMENT RECORDS
    # --------------------------------------------------

    st.divider()

    st.subheader("📋 Equipment Records")

    display_columns = [
        "Equipment ID",
        "Equipment type",
        "Manufacturer",
        "Operating hours",
        "Temperature",
        "Temperature Status",
        "Vibration",
        "Vibration Status",
        "Maintenance status",
        "Downtime",
        "Availability",
        "Engine status",
        "Brake status",
        "Tyre status"
    ]

    st.dataframe(
        filtered_equipment[
            display_columns
        ],
        use_container_width=True,
        hide_index=True
    )
