        if not incident_dates.empty:
            incident_dates["Date"] = incident_dates["Parsed Date"].dt.date
            trend = incident_dates.groupby("Date").size().reset_index(name="Incidents")
            st.subheader("📈 Incident Trend Over Time")
            st.line_chart(trend.set_index("Date")["Incidents"], use_container_width=True)

    st.divider()

    # --------------------------------------------------
    # EQUIPMENT CHARTS
    # --------------------------------------------------
    st.subheader("🚜 Equipment Condition & Maintenance Analytics")

    left, right = st.columns(2)
    with left:
        show_pie_chart(equipment, "Maintenance status", "Equipment maintenance status")
    with right:
        show_bar_chart(equipment, "Equipment type", "Equipment count by type")

    left, right = st.columns(2)
    with left:
        show_histogram(equipment, "Temperature", "Equipment temperature distribution", "Temperature (°C)")
    with right:
        show_histogram(equipment, "Vibration", "Equipment vibration distribution", "Vibration (mm/s)")

    left, right = st.columns(2)
    with left:
        show_histogram(equipment, "Downtime", "Equipment downtime distribution", "Downtime (hours)")
    with right:
        show_histogram(
            equipment, "Calculated Availability (%)",
            "Equipment availability distribution", "Availability (%)"
        )

    # Highlight equipment outside the monitoring thresholds in the brief.
    alerts = pd.Series(False, index=equipment.index)
    alert_reasons = pd.Series("", index=equipment.index, dtype="object")

    if "Temperature" in equipment.columns:
        temperature = numeric_column(equipment, "Temperature")
        hot = temperature > 100
        alerts = alerts | hot.fillna(False)
        alert_reasons.loc[hot.fillna(False)] += "Temperature above 100°C; "

    if "Vibration" in equipment.columns:
        vibration = numeric_column(equipment, "Vibration")
        vibrating = vibration > 8
        alerts = alerts | vibrating.fillna(False)
        alert_reasons.loc[vibrating.fillna(False)] += "Vibration above 8 mm/s; "

    st.subheader("⚠️ Equipment Requiring Attention")
    if alerts.any():
        alert_table = equipment.loc[alerts].copy()
        alert_table["Alert reason"] = alert_reasons.loc[alerts]
        columns = [
            column for column in [
                "Equipment ID", "Equipment type", "Temperature", "Vibration",
                "Maintenance status", "Downtime",
                "Calculated Availability (%)", "Alert reason"
            ] if column in alert_table.columns
        ]
        st.dataframe(alert_table[columns], use_container_width=True, hide_index=True)
    else:
        st.success("No equipment exceeds the critical temperature or vibration thresholds in the available data.")

    st.divider()

    # --------------------------------------------------
    # DATA TABLES
    # --------------------------------------------------
    with st.expander("👷 View worker safety records"):
        display_available_columns(
            workers,
            [
                "Worker ID", "Department", "Job role", "Shift",
                "PPE compliance", "Safety training status", "Fatigue level",
                "Safety observations", "Near misses", "Previous incidents"
            ]
        )

    with st.expander("📝 View incident records"):
        display_available_columns(
            incidents,
            [
                "Incident ID", "Date", "Time", "Shift", "Location",
                "Department", "Incident type", "Severity", "Injury status",
                "Lost-time injury status", "Cause", "Corrective action",
                "Incident status"
            ]
        )

    with st.expander("🔧 View equipment records"):
        display_available_columns(
            equipment,
            [
                "Equipment ID", "Equipment type", "Manufacturer",
                "Operating hours", "Temperature", "Vibration",
                "Fuel consumption", "Brake status", "Tyre status",
                "Engine status", "Maintenance status", "Downtime",
                "Calculated Availability (%)"
            ]
        )

    st.caption(
        f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} "
        "| Charts and metrics are calculated from the latest CSV contents."
    )

    if not PLOTLY_AVAILABLE:
        st.info(
            "For interactive pie charts and histograms, add `plotly` to "
            "requirements.txt. Basic bar charts will still be displayed without it."
        )


# --------------------------------------------------
# AUTOMATIC REFRESH
# --------------------------------------------------

# Streamlit fragments support periodic reruns in newer Streamlit versions.
# The refresh button above remains available if fragments are not supported.
if hasattr(st, "fragment"):
    @st.fragment(run_every=30)
    def render_dashboard():
        render_dashboard_content()
else:
    def render_dashboard():
        render_dashboard_content()
