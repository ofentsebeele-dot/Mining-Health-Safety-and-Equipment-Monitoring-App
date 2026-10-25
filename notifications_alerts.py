
# --------------------------------------------------
# NOTIFICATIONS AND ALERTS
# --------------------------------------------------

elif selected_page == alerts_page_label:

    st.header("Equipment Notifications & Alerts")

    st.write(
        "Select equipment from the CSV dataset to check "
        "its recorded temperature and vibration."
    )

    st.caption(
        f"Testing dataset: {len(equipment_data)} equipment records"
    )

    st.info(
        "These are prototype thresholds for educational testing, "
        "not validated mine safety limits."
    )

    # --------------------------------------------------
    # SELECT EQUIPMENT FROM CSV
    # --------------------------------------------------

    equipment_ids = equipment_data["Equipment ID"].tolist()

    selected_equipment = st.selectbox(
        "Select Equipment ID",
        equipment_ids,
        key="selected_equipment_id"
    )

    # Retrieve the selected equipment record.
    selected_row = equipment_data.loc[
        equipment_data["Equipment ID"] == selected_equipment
    ].iloc[0]

    st.subheader("Selected Equipment")

    st.write(
        f"**Equipment ID:** {selected_row['Equipment ID']}"
    )

    st.write(
        f"**Equipment Type:** {selected_row['Equipment type']}"
    )

    # --------------------------------------------------
    # DISPLAY CSV READINGS
    # --------------------------------------------------

    csv_temperature = float(selected_row["Temperature"])
    csv_vibration = float(selected_row["Vibration"])

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Recorded Temperature",
            f"{csv_temperature:.1f} °C"
        )

    with col2:
        st.metric(
            "Recorded Vibration",
            f"{csv_vibration:.1f} mm/s"
        )

    # --------------------------------------------------
    # OPTIONAL MANUAL TESTING
    # --------------------------------------------------

    use_manual_readings = st.checkbox(
        "Enter different readings to test the alert system",
        key=f"manual_mode_{selected_equipment}"
    )

    if use_manual_readings:

        temperature = st.number_input(
            "Test Temperature (°C)",
            min_value=0.0,
            max_value=500.0,
            value=csv_temperature,
            step=1.0,
            key=f"test_temperature_{selected_equipment}"
        )

        vibration = st.number_input(
            "Test Vibration (mm/s)",
            min_value=0.0,
            max_value=100.0,
            value=csv_vibration,
            step=0.5,
            key=f"test_vibration_{selected_equipment}"
        )

    else:

        temperature = csv_temperature
        vibration = csv_vibration

    # --------------------------------------------------
    # CHECK EQUIPMENT
    # --------------------------------------------------

    if st.button(
        "Check Equipment",
        type="primary"
    ):

        result = generate_alert(
            selected_equipment,
            temperature,
            vibration
        )

        # Include the equipment type in the saved result.
        result["equipment_type"] = selected_row["Equipment type"]

        # Save the latest result for each equipment item.
        st.session_state["equipment_checks"][
            selected_equipment
        ] = result

        st.session_state["latest_equipment_alert"] = result

        # Keep warnings and critical alerts awaiting review.
        if result["alert_level"] in ["Warning", "Critical"]:

            st.session_state["pending_alerts"][
                selected_equipment
            ] = result

        else:

            st.session_state["pending_alerts"].pop(
                selected_equipment,
                None
            )

        st.rerun()

    # --------------------------------------------------
    # ALERTS AWAITING REVIEW
    # --------------------------------------------------

    st.divider()
    st.subheader("Notifications Awaiting Review")

    pending_alerts = st.session_state["pending_alerts"]

    if pending_alerts:

        st.write(
            f"{len(pending_alerts)} equipment item(s) "
            "have alerts awaiting review."
        )

        for alert_id, alert in list(pending_alerts.items()):

            with st.container(border=True):

                st.write(
                    f"**Equipment ID:** {alert_id}"
                )

                if "equipment_type" in alert:
                    st.write(
                        f"**Equipment Type:** "
                        f"{alert['equipment_type']}"
                    )

                st.write(
                    f"**Alert Level:** {alert['alert_level']}"
                )

                st.write(alert["alert_message"])

                st.write(
                    f"Temperature: {alert['temperature']:.1f} °C"
                )

                st.write(
                    f"Vibration: {alert['vibration']:.1f} mm/s"
                )

                if st.button(
                    "Mark as Reviewed",
                    key=f"review_{alert_id}"
                ):

                    st.session_state["pending_alerts"].pop(
                        alert_id,
                        None
                    )

                    st.rerun()

    else:

        st.success("No alerts are awaiting review.")

    # --------------------------------------------------
    # VIEW EQUIPMENT CHECK HISTORY
    # --------------------------------------------------

    st.divider()
    st.subheader("Latest Equipment Checks")

    all_checks = st.session_state["equipment_checks"]

    if all_checks:

        result_equipment = st.selectbox(
            "Select equipment to view its latest result",
            list(all_checks.keys()),
            key="view_equipment_results"
        )

        result = all_checks[result_equipment]

        st.write(f"**Equipment ID:** {result['equipment_id']}")

        if "equipment_type" in result:
            st.write(
                f"**Equipment Type:** {result['equipment_type']}"
            )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Temperature",
                f"{result['temperature']:.1f} °C"
            )

            st.write(
                f"Status: {result['temperature_status']}"
            )

        with col2:

            st.metric(
                "Vibration",
                f"{result['vibration']:.1f} mm/s"
            )

            st.write(
                f"Status: {result['vibration_status']}"
            )

        st.write(
            f"**Overall Alert:** {result['alert_level']}"
        )

        st.write(result["alert_message"])

        if result["alert_level"] == "Critical":
            st.error("Urgent equipment assessment required.")

        elif result["alert_level"] == "Warning":
            st.warning("Equipment requires attention.")

        else:
            st.success("Equipment readings are normal.")

    else:

        st.info(
            "Select equipment and click Check Equipment "
            "to generate the first result."
        )
