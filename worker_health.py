import streamlit as st
import pandas as pd


def load_worker_data():

    return pd.read_csv("workers.csv")


def render_worker_health_page():

    st.title("Worker Health & Safety")

    st.write(
        "Monitor worker PPE compliance, training status, "
        "fatigue, safety observations and near misses."
    )

    st.divider()

    # Load worker data
    workers = load_worker_data()


    # --------------------------------------------------
    # KEY INDICATORS
    # --------------------------------------------------

    total_workers = len(workers)

    average_ppe = workers[
        "PPE compliance"
    ].mean()

    total_observations = workers[
        "Safety observations"
    ].sum()

    total_near_misses = workers[
        "Near misses"
    ].sum()


    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Workers",
            total_workers
        )

    with col2:
        st.metric(
            "Average PPE Compliance",
            f"{average_ppe:.1f}%"
        )

    with col3:
        st.metric(
            "Safety Observations",
            total_observations
        )

    with col4:
        st.metric(
            "Near Misses",
            total_near_misses
        )


    st.divider()


    # --------------------------------------------------
    # FILTERS
    # --------------------------------------------------

    st.subheader("Worker Filters")

    col1, col2, col3 = st.columns(3)

    with col1:

        departments = [
            "All"
        ] + sorted(
            workers["Department"].unique().tolist()
        )

        selected_department = st.selectbox(
            "Department",
            departments
        )

    with col2:

        shifts = [
            "All"
        ] + sorted(
            workers["Shift"].unique().tolist()
        )

        selected_shift = st.selectbox(
            "Shift",
            shifts
        )

    with col3:

        fatigue_levels = [
            "All"
        ] + sorted(
            workers["Fatigue level"].unique().tolist()
        )

        selected_fatigue = st.selectbox(
            "Fatigue Level",
            fatigue_levels
        )


    # --------------------------------------------------
    # APPLY FILTERS
    # --------------------------------------------------

    filtered_workers = workers.copy()

    if selected_department != "All":

        filtered_workers = filtered_workers[
            filtered_workers["Department"]
            == selected_department
        ]

    if selected_shift != "All":

        filtered_workers = filtered_workers[
            filtered_workers["Shift"]
            == selected_shift
        ]

    if selected_fatigue != "All":

        filtered_workers = filtered_workers[
            filtered_workers["Fatigue level"]
            == selected_fatigue
        ]


    st.divider()


    # --------------------------------------------------
    # PPE COMPLIANCE
    # --------------------------------------------------

    st.subheader("PPE Compliance")

    filtered_ppe = filtered_workers[
        "PPE compliance"
    ].mean()

    st.metric(
        "Filtered Average PPE Compliance",
        f"{filtered_ppe:.1f}%"
    )


    # --------------------------------------------------
    # TRAINING STATUS
    # --------------------------------------------------

    st.subheader("Safety Training Status")

    training_counts = filtered_workers[
        "Safety training status"
    ].value_counts()

    st.bar_chart(training_counts)


    # --------------------------------------------------
    # FATIGUE
    # --------------------------------------------------

    st.subheader("Fatigue Levels")

    fatigue_counts = filtered_workers[
        "Fatigue level"
    ].value_counts()

    st.bar_chart(fatigue_counts)


    # --------------------------------------------------
    # SAFETY OBSERVATIONS
    # --------------------------------------------------

    st.subheader("Safety Observations")

    observation_data = (
        filtered_workers
        .groupby("Department")["Safety observations"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(observation_data)


    # --------------------------------------------------
    # NEAR MISSES
    # --------------------------------------------------

    st.subheader("Near Misses")

    near_miss_data = (
        filtered_workers
        .groupby("Department")["Near misses"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(near_miss_data)


    # --------------------------------------------------
    # WORKER DATA
    # --------------------------------------------------

    st.subheader("Worker Records")

    st.dataframe(
        filtered_workers,
        use_container_width=True
    )
