import streamlit as st
import pandas as pd


def render_incidents_page():

    incidents = pd.read_csv(
        "incidents.csv"
    )

    st.title("Safety Incidents")

    st.write(
        "Monitor and review reported safety incidents."
    )

    st.divider()

    total_incidents = len(incidents)

    st.metric(
        "Total Incidents",
        total_incidents
    )

    st.subheader("Incident Records")

    st.dataframe(
        incidents,
        use_container_width=True,
        hide_index=True
    )
