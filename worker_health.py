
import streamlit as st
import pandas as pd


# --------------------------------------------------
# BLACK BACKGROUND AND WHITE FONT
# --------------------------------------------------

st.markdown(
    """
    <style>
    /* Main application background */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }

    /* All headings */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    /* General text */
    p, label, span, div, li {
        color: #FFFFFF;
    }

    /* Metric labels and values */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricDelta"] {
        color: #FFFFFF !important;
    }

    /* Select boxes and text inputs */
    div[data-baseweb="select"] *,
    div[data-baseweb="input"] *,
    input {
        color: #FFFFFF !important;
    }

    /* Input fields */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background-color: #171717 !important;
    }

    /* Buttons */
    .stButton button,
    .stDownloadButton button {
        background-color: #222222;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF;
    }

    .stButton button:hover,
    .stDownloadButton button:hover {
        background-color: #333333;
        color: #FFFFFF !important;
        border: 1px solid #FFFFFF;
    }

    /* Dataframe container */
    [data-testid="stDataFrame"] {
        border: 1px solid #444444;
    }

    /* Dividers */
    hr {
        border-color: #555555;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #000000;
    }

    /* Captions */
    [data-testid="stCaptionContainer"] {
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def load_worker_data():

    return pd.read_csv("workers.csv")


def render_worker_health_page():

    st.title("Worker Health & Safety")

    st.write("Monitor worker PPE compliance, training status, " "fatigue, safety observations and near misses.")

    st.divider()

    # Load worker data
    workers = load_worker_data()


    # --------------------------------------------------
    # KEY INDICATORS
    # --------------------------------------------------

    total_workers = len(workers)

    average_ppe = workers["PPE compliance"].mean()

    total_observations = workers["Safety observations"].sum()

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
