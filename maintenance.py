import streamlit as st
import pandas as pd


def load_equipment_data():

    return pd.read_csv(
        "equipment.csv"
    )


def render_maintenance_page():

    equipment = load_equipment_data()

    st.title("Maintenance Monitoring")

    st.write(
        "Monitor equipment maintenance status, downtime "
        "and operational condition."
    )

    st.divider()

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    total_equipment = len(equipment)

    under_maintenance = len(
        equipment[
            equipment["Maintenance status"].astype(str)
            == "Under Maintenance"
        ]
    )

    operational = len(
        equipment[
            equipment["Maintenance status"].astype(str)
            == "Operational"
        ]
    )

    total_downtime = equipment["Downtime"].sum()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Equipment",
            total_equipment
        )

    with col2:
        st.metric(
            "Operational",
            operational
        )

    with col3:
        st.metric(
            "Under Maintenance",
            under_maintenance
        )

    with col4:
        st.metric(
            "Total Downtime",
            f"{total_downtime:.1f} hrs"
        )

    st.divider()

    # --------------------------------------------------
    # FILTER
    # --------------------------------------------------

    st.subheader("Maintenance Filter")

    status_options = (
        ["All"]
        + sorted(
            equipment["Maintenance status"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

    selected_status = st.selectbox(
        "Maintenance Status",
        status_options,
        key="maintenance_status"
    )

    filtered_equipment = equipment.copy()

    if selected_status != "All":

        filtered_equipment = filtered_equipment[
            filtered_equipment["Maintenance status"]
            .astype(str)
            == selected_status
        ]

    st.divider()

    # --------------------------------------------------
    # MAINTENANCE STATUS
    # --------------------------------------------------

    st.subheader("Maintenance Status")

    maintenance_counts = (
        filtered_equipment[
            "Maintenance status"
        ]
        .astype(str)
        .value_counts()
    )

    if not maintenance_counts.empty:

        st.bar_chart(
            maintenance_counts
        )

    else:

        st.info(
            "No maintenance records found."
        )

    st.divider()

    # --------------------------------------------------
    # DOWNTIME BY EQUIPMENT TYPE
    # --------------------------------------------------

    st.subheader(
        "Downtime by Equipment Type"
    )

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

    st.divider()

    # --------------------------------------------------
    # MAINTENANCE RECORDS
    # --------------------------------------------------

    st.subheader("Maintenance Records")

    st.dataframe(
        filtered_equipment[
            [
                "Equipment ID",
                "Equipment type",
                "Manufacturer",
                "Operating hours",
                "Maintenance status",
                "Downtime",
                "Engine status",
                "Brake status",
                "Tyre status"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
