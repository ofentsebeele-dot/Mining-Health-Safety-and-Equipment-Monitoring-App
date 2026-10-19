
import os
import streamlit as st
import pandas as pd

# ==========================================================
# KHWEZI MINING MONITORING SYSTEM
# SAFETY, EQUIPMENT & INTEGRATED ANALYSIS
# ==========================================================

IMAGE_DIR = "images"


def show_image(filename, caption=None, width=None):
    """Display an optional local image without breaking the page."""
    path = os.path.join(IMAGE_DIR, filename)

    if os.path.isfile(path):
        st.image(path, caption=caption, use_container_width=True)
        return True

    return False


# ==========================================================
# MINING DASHBOARD DESIGN
# ==========================================================

def apply_mining_theme():

    st.markdown("""
    <style>
    .stApp {
        background-color: #101820;
        color: #F1F5F9;
    }

    [data-testid="stHeader"] {
        background-color: rgba(16, 24, 32, 0.95);
    }

    [data-testid="stSidebar"] {
        background-color: #192630;
    }

    [data-testid="stSidebar"] * {
        color: #F1F5F9;
    }

    h1, h2, h3 {
        color: #F5A623 !important;
        font-weight: 750 !important;
    }

    p, label, .stMarkdown {
        color: #E2E8F0;
    }

    [data-testid="stMetric"] {
        background-color: #202F3A;
        border: 1px solid #394B58;
        padding: 18px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: #CBD5E1 !important;
    }

    [data-testid="stMetricValue"] {
        color: #F5A623 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #202F3A;
        border-color: #536675;
    }

    .stSelectbox label {
        color: #F5A623 !important;
        font-weight: bold;
    }

    .stButton button {
        background-color: #F5A623;
        color: #101820;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }

    .stButton button:hover {
        background-color: #FFD078;
        color: #101820;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #394B58;
        border-radius: 10px;
    }

    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    hr {
        border-color: #394B58;
    }

    .mine-subtitle {
        color: #CBD5E1;
        font-size: 16px;
        margin-top: -8px;
    }

    .mine-tag {
        display: inline-block;
        background-color: #293945;
        border: 1px solid #F5A623;
        color: #F5A623;
        padding: 5px 11px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    .mine-card {
        background-color: #202F3A;
        padding: 17px;
        border-radius: 12px;
        border: 1px solid #394B58;
        min-height: 110px;
    }

    .mine-card-title {
        color: #F5A623;
        font-weight: bold;
        font-size: 17px;
    }

    .mine-card-text {
        color: #CBD5E1;
        font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)


# ==========================================================
# LOAD DATA
# ==========================================================

def load_worker_data():
    return pd.read_csv("workers.csv")


def load_incident_data():
    return pd.read_csv("incidents.csv")


def load_equipment_data():
    return pd.read_csv("equipment.csv")


# ==========================================================
# CALCULATE EQUIPMENT AVAILABILITY
# ==========================================================

def calculate_availability(equipment):

    equipment = equipment.copy()

    total_time = (
        equipment["Operating hours"]
        + equipment["Downtime"]
    )

    equipment["Availability"] = (
        equipment["Operating hours"]
        .div(total_time.where(total_time != 0))
        * 100
    )

    return equipment


# ==========================================================
# SHARED DISPLAY HELPERS
# ==========================================================

def show_result_table(data):
    if data.empty:
        st.info("No records match these conditions.")
    else:
        st.dataframe(
            data,
            use_container_width=True,
            hide_index=True
        )


def show_bar_chart(data, title):
    st.subheader(title)

    if data.empty:
        st.info("There is no data available to display.")
    else:
        st.bar_chart(data)


def get_top_row(data, column):
    if data.empty or data[column].dropna().empty:
        st.info("There is no valid data available for this question.")
        return None

    return data.loc[data[column].idxmax()]


# ==========================================================
# RENDER QUESTIONS PAGE
# ==========================================================

def render_questions_page():

    apply_mining_theme()

    # Load monitoring information
    try:
        workers = load_worker_data()
        incidents = load_incident_data()
        equipment = load_equipment_data()
        equipment = calculate_availability(equipment)

    except FileNotFoundError as error:
        st.error(
            f"Required CSV file was not found: {error.filename}. "
            "Check that workers.csv, incidents.csv and equipment.csv "
            "are saved in your project folder."
        )
        return

    except Exception as error:
        st.error(f"Could not load the monitoring data: {error}")
        return

    # ------------------------------------------------------
    # MINING HERO BANNER
    # ------------------------------------------------------

    hero_path = os.path.join(IMAGE_DIR, "mine_hero.jpg")

    if os.path.isfile(hero_path):
        st.image(hero_path, use_container_width=True)

    st.markdown(
        '<span class="mine-tag">KHWEZI MINING OPERATIONS</span>',
        unsafe_allow_html=True
    )

    st.title("Safety & Equipment Intelligence")

    st.markdown(
        '<p class="mine-subtitle">'
        'Mining monitoring, operational insights and data-driven '
        'decision support for safer and more efficient mining.'
        '</p>',
        unsafe_allow_html=True
    )

    st.divider()

    # ------------------------------------------------------
    # TOP-LEVEL METRICS
    # ------------------------------------------------------

    total_workers = len(workers)
    total_incidents = len(incidents)
    total_equipment = len(equipment)

    average_availability = (
        equipment["Availability"].mean()
        if not equipment.empty
        else 0
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Workers Monitored", total_workers)
    col2.metric("Safety Incidents", total_incidents)
    col3.metric("Equipment Units", total_equipment)
    col4.metric(
        "Average Availability",
        f"{average_availability:.1f}%"
    )

    st.divider()

    # ------------------------------------------------------
    # VISUAL CATEGORY CARDS
    # ------------------------------------------------------

    st.subheader("Monitoring Centre")
    st.write(
        "Choose a monitoring category to investigate the mine data."
    )

    card1, card2, card3 = st.columns(3)

    with card1:
        show_image("mine_safety.jpg", "Worker safety")

        st.markdown("""
        <div class="mine-card">
            <div class="mine-card-title">Worker Safety</div>
            <div class="mine-card-text">
                Incidents, PPE compliance, near misses and
                workforce risk indicators.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with card2:
        show_image("mining_truck.jpg", "Mining fleet")

        st.markdown("""
        <div class="mine-card">
            <div class="mine-card-title">Equipment Monitoring</div>
            <div class="mine-card-text">
                Equipment availability, downtime, temperature,
                vibration and maintenance.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with card3:
        show_image("mine_equipment.jpg", "Mine machinery")

        st.markdown("""
        <div class="mine-card">
            <div class="mine-card-title">Integrated Analysis</div>
            <div class="mine-card-text">
                Combine worker safety indicators and equipment
                performance to support decisions.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ------------------------------------------------------
    # QUESTION CATEGORIES
    # ------------------------------------------------------

    categories = [
        "Health and Safety",
        "Equipment",
        "Integrated Safety and Equipment Analysis"
    ]

    selected_category = st.selectbox(
        "Select Monitoring Category",
        categories
    )

    st.divider()

    # ======================================================
    # HEALTH AND SAFETY QUESTIONS
    # ======================================================

    if selected_category == "Health and Safety":

        st.subheader("Worker Health & Safety")
        st.caption(
            "Analyse incident patterns and worker safety indicators."
        )

        questions = [
            "How many safety incidents occurred during the selected period?",
            "Which department has the highest number of incidents?",
            "Which shift records the most incidents?",
            "What percentage of workers comply with PPE requirements?",
            "How many near misses have been recorded?",
            "Which incident types occur most frequently?",
            "How many incidents are classified as high or critical?",
            "Which departments have the highest safety risk?",
            "Is there an observable difference in incidents between day and night shifts?",
            "Which safety conditions require immediate attention?"
        ]

        selected_question = st.selectbox(
            "Select a safety question",
            questions,
            key="safety_question"
        )

        st.divider()

        # QUESTION 1
        if selected_question == questions[0]:

            st.subheader("Safety Incident Overview")

            st.metric("Total Safety Incidents", len(incidents))

            show_bar_chart(
                incidents["Severity"].value_counts(),
                "Incidents by Severity"
            )

        # QUESTION 2
        elif selected_question == questions[1]:

            department_counts = incidents["Department"].value_counts()

            if not department_counts.empty:
                department = department_counts.idxmax()
                count = department_counts.max()

                st.success(
                    f"{department} has the highest number of "
                    f"incidents, with {count} incidents."
                )

                show_bar_chart(
                    department_counts,
                    "Safety Incidents by Department"
                )
            else:
                st.info("No department incident data is available.")

        # QUESTION 3
        elif selected_question == questions[2]:

            shift_counts = incidents["Shift"].value_counts()

            if not shift_counts.empty:
                shift = shift_counts.idxmax()
                count = shift_counts.max()

                st.success(
                    f"The {shift} shift records the most incidents, "
                    f"with {count} incidents."
                )

                show_bar_chart(
                    shift_counts,
                    "Safety Incidents by Shift"
                )
            else:
                st.info("No shift incident data is available.")

        # QUESTION 4
        elif selected_question == questions[3]:

            if workers.empty:
                st.info("No worker records are available.")
            else:
                compliant_workers = workers[
                    workers["PPE compliance"] >= 95
                ]

                percentage = (
                    len(compliant_workers) / len(workers)
                ) * 100

                st.metric(
                    "Workers Meeting PPE Threshold",
                    f"{percentage:.1f}%"
                )

                st.caption(
                    "Workers with PPE compliance of 95% or higher "
                    "are counted as meeting the threshold."
                )

                show_bar_chart(
                    workers["PPE compliance"],
                    "PPE Compliance by Worker"
                )

        # QUESTION 5
        elif selected_question == questions[4]:

            near_misses = workers["Near misses"].sum()

            st.metric("Recorded Near Misses", int(near_misses))

            show_bar_chart(
                workers.groupby("Department")["Near misses"].sum(),
                "Near Misses by Department"
            )

        # QUESTION 6
        elif selected_question == questions[5]:

            incident_types = incidents["Incident type"].value_counts()

            show_bar_chart(
                incident_types,
                "Most Frequent Incident Types"
            )

            if not incident_types.empty:
                st.info(
                    f"The most frequently recorded incident type is "
                    f"{incident_types.index[0]} "
                    f"({incident_types.iloc[0]} incidents)."
                )

        # QUESTION 7
        elif selected_question == questions[6]:

            severity = (
                incidents["Severity"]
                .astype(str)
                .str.strip()
                .str.lower()
            )

            high_critical = incidents[
                severity.isin(["high", "critical"])
            ]

            st.metric(
                "High or Critical Incidents",
                len(high_critical)
            )

            show_result_table(high_critical)

        # QUESTION 8
        elif selected_question == questions[7]:

            department_risk = (
                workers.groupby("Department")[
                    [
                        "Near misses",
                        "Previous incidents"
                    ]
                ]
                .sum()
            )

            st.write(
                "The table summarises recorded near misses and "
                "previous incidents by department. These indicators "
                "can help identify areas for further investigation."
            )

            show_result_table(department_risk.reset_index())

        # QUESTION 9
        elif selected_question == questions[8]:

            shift_counts = incidents["Shift"].value_counts()

            show_bar_chart(
                shift_counts,
                "Incident Distribution by Shift"
            )

            if len(shift_counts) >= 2:
                difference = (
                    shift_counts.max() - shift_counts.min()
                )

                st.info(
                    f"The difference between the highest and lowest "
                    f"shift incident counts is {difference}."
                )

            st.caption(
                "Incident counts alone do not prove that a shift "
                "is less safe. Worker numbers and hours worked may "
                "also affect the comparison."
            )

        # QUESTION 10
        elif selected_question == questions[9]:

            st.write(
                "Workers are listed for review when their PPE "
                "compliance is below 95%, near misses are at least 2, "
                "or previous incidents are at least 2."
            )

            attention = workers[
                (workers["PPE compliance"] < 95)
                | (workers["Near misses"] >= 2)
                | (workers["Previous incidents"] >= 2)
            ]

            show_result_table(
                attention[
                    [
                        "Worker ID",
                        "Department",
                        "Job role",
                        "PPE compliance",
                        "Fatigue level",
                        "Near misses",
                        "Previous incidents"
                    ]
                ]
            )

    # ======================================================
    # EQUIPMENT QUESTIONS
    # ======================================================

    elif selected_category == "Equipment":

        st.subheader("Equipment Performance Centre")
        st.caption(
            "Investigate fleet condition, reliability and maintenance."
        )

        questions = [
            "Which equipment has the highest downtime?",
            "Which equipment has the lowest availability?",
            "Which equipment has the highest vibration?",
            "Which equipment has the highest operating temperature?",
            "Which equipment has generated the most alerts?",
            "Which equipment requires maintenance?",
            "Which equipment is overdue for maintenance?",
            "What is the average equipment availability?",
            "Which equipment type has the highest downtime?",
            "Which equipment requires immediate inspection?"
        ]

        selected_question = st.selectbox(
            "Select an equipment question",
            questions,
            key="equipment_question"
        )

        st.divider()

        # QUESTION 1
        if selected_question == questions[0]:

            equipment_row = get_top_row(equipment, "Downtime")

            if equipment_row is not None:
                st.metric(
                    "Highest Downtime",
                    f"{equipment_row['Downtime']} hours"
                )

                st.success(
                    f"{equipment_row['Equipment ID']} has the "
                    f"highest downtime."
                )

                show_bar_chart(
                    equipment.set_index("Equipment ID")["Downtime"],
                    "Downtime by Equipment"
                )

        # QUESTION 2
        elif selected_question == questions[1]:

            valid = equipment.dropna(subset=["Availability"])

            if not valid.empty:
                equipment_row = valid.loc[
                    valid["Availability"].idxmin()
                ]

                st.metric(
                    "Lowest Availability",
                    f"{equipment_row['Availability']:.1f}%"
                )

                st.warning(
                    f"{equipment_row['Equipment ID']} has the "
                    f"lowest calculated availability."
                )

                show_bar_chart(
                    valid.set_index("Equipment ID")["Availability"],
                    "Availability by Equipment (%)"
                )
            else:
                st.info("Availability cannot be calculated from the data.")

        # QUESTION 3
        elif selected_question == questions[2]:

            equipment_row = get_top_row(equipment, "Vibration")

            if equipment_row is not None:
                st.metric(
                    "Highest Vibration",
                    equipment_row["Vibration"]
                )

                st.warning(
                    f"{equipment_row['Equipment ID']} has the "
                    f"highest recorded vibration."
                )

                show_bar_chart(
                    equipment.set_index("Equipment ID")["Vibration"],
                    "Vibration by Equipment"
                )

        # QUESTION 4
        elif selected_question == questions[3]:

            equipment_row = get_top_row(equipment, "Temperature")

            if equipment_row is not None:
                st.metric(
                    "Highest Temperature",
                    equipment_row["Temperature"]
                )

                st.warning(
                    f"{equipment_row['Equipment ID']} has the "
                    f"highest recorded operating temperature."
                )

                show_bar_chart(
                    equipment.set_index("Equipment ID")["Temperature"],
                    "Operating Temperature by Equipment"
                )

        # QUESTION 5
        elif selected_question == questions[4]:

            st.info(
                "Potential alerts are flagged using the project's "
                "rules: temperature of at least 80, vibration of at "
                "least 5, or maintenance status marked overdue or critical."
            )

            alerts = equipment[
                (equipment["Temperature"] >= 80)
                | (equipment["Vibration"] >= 5)
                | (
                    equipment["Maintenance status"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .isin(["overdue", "critical"])
                )
            ]

            st.metric("Equipment with Potential Alerts", len(alerts))
            show_result_table(alerts)

        # QUESTION 6
        elif selected_question == questions[5]:

            maintenance = equipment[
                equipment["Maintenance status"]
                .astype(str)
                .str.strip()
                .str.lower()
                .isin([
                    "under maintenance",
                    "maintenance required",
                    "overdue"
                ])
            ]

            st.metric("Equipment Requiring Maintenance", len(maintenance))
            show_result_table(maintenance)

        # QUESTION 7
        elif selected_question == questions[6]:

            overdue = equipment[
                equipment["Maintenance status"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "overdue"
            ]

            if overdue.empty:
                st.success(
                    "No equipment is currently marked overdue."
                )
            else:
                st.warning(
                    f"{len(overdue)} equipment item(s) are marked overdue."
                )
                show_result_table(overdue)

        # QUESTION 8
        elif selected_question == questions[7]:

            average_availability = equipment["Availability"].mean()

            if pd.isna(average_availability):
                st.info("Average availability cannot be calculated.")
            else:
                st.metric(
                    "Average Equipment Availability",
                    f"{average_availability:.1f}%"
                )

                show_bar_chart(
                    equipment.set_index("Equipment ID")["Availability"],
                    "Equipment Availability (%)"
                )

        # QUESTION 9
        elif selected_question == questions[8]:

            downtime = (
                equipment.groupby("Equipment type")["Downtime"]
                .sum()
                .sort_values(ascending=False)
            )

            show_bar_chart(
                downtime,
                "Total Downtime by Equipment Type"
            )

            if not downtime.empty:
                st.success(
                    f"{downtime.idxmax()} has the highest total downtime."
                )

        # QUESTION 10
        elif selected_question == questions[9]:

            inspection = equipment[
                (equipment["Temperature"] >= 80)
                | (equipment["Vibration"] >= 5)
                | (
                    equipment["Brake status"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    != "good"
                )
                | (
                    equipment["Engine status"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    != "good"
                )
            ]

            st.write(
                "These equipment units meet one or more of the "
                "project's inspection rules. Confirm actual operating "
                "limits and inspect equipment according to site procedures."
            )

            st.metric("Equipment Flagged for Inspection", len(inspection))
            show_result_table(inspection)

    # ======================================================
    # INTEGRATED SAFETY AND EQUIPMENT QUESTIONS
    # ======================================================

    else:

        st.subheader("Integrated Mining Intelligence")
        st.caption(
            "Combine worker safety and equipment data to support "
            "operational decisions."
        )

        questions = [
            "Are safety incidents associated with particular shifts?",
            "Which departments have both high safety risk and high equipment downtime?",
            "Which equipment contributes to the greatest number of alerts?",
            "Which equipment should receive maintenance priority?",
            "What are the most common causes of safety incidents?",
            "Which safety indicators require management intervention?",
            "What percentage of monitored equipment is operating normally?",
            "How many critical alerts are currently active?",
            "Which areas of the operation require the greatest attention?",
            "What recommendations can be generated from the monitoring results?"
        ]

        selected_question = st.selectbox(
            "Select an integrated question",
            questions,
            key="integrated_question"
        )

        st.divider()

        # QUESTION 1
        if selected_question == questions[0]:

            shift_counts = incidents["Shift"].value_counts()

            show_bar_chart(
                shift_counts,
                "Safety Incidents by Shift"
            )

            st.write(
                "Use this chart to compare recorded incident counts "
                "between shifts. The results show patterns, not proof "
                "that a shift caused the incidents."
            )

        # QUESTION 2
        elif selected_question == questions[1]:

            st.write("Incident levels by department")

            department_incidents = incidents[
                "Department"
            ].value_counts()

            show_bar_chart(
                department_incidents,
                "Safety Incidents by Department"
            )

            st.write("Equipment downtime by equipment type")

            department_downtime = (
                equipment.groupby("Equipment type")["Downtime"]
                .sum()
                .sort_values(ascending=False)
            )

            show_bar_chart(
                department_downtime,
                "Downtime by Equipment Type"
            )

            st.caption(
                "The current equipment dataset groups downtime by "
                "equipment type, not department. A direct department-to-"
                "equipment comparison requires a shared department field."
            )

        # QUESTION 3
        elif selected_question == questions[2]:

            alerts = equipment[
                (equipment["Temperature"] >= 80)
                | (equipment["Vibration"] >= 5)
                | (
                    equipment["Maintenance status"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    .isin(["overdue", "critical"])
                )
            ]

            st.metric("Equipment with Potential Alerts", len(alerts))
            show_result_table(alerts)

            st.caption(
                "This counts equipment units meeting at least one "
                "alert rule. It does not count individual alert events."
            )

        # QUESTION 4
        elif selected_question == questions[3]:

            priority = equipment.copy()

            priority["Priority Score"] = (
                priority["Downtime"] * 0.4
                + priority["Vibration"] * 10
                + priority["Temperature"] * 0.2
            )

            priority = priority.sort_values(
                "Priority Score",
                ascending=False
            )

            st.write(
                "Equipment is ranked using the original project's "
                "priority formula. The score is a preliminary ranking, "
                "not a validated engineering risk assessment."
            )

            show_result_table(
                priority[
                    [
                        "Equipment ID",
                        "Equipment type",
                        "Downtime",
                        "Vibration",
                        "Temperature",
                        "Maintenance status",
                        "Priority Score"
                    ]
                ]
            )

        # QUESTION 5
        elif selected_question == questions[4]:

            causes = (
                incidents["Cause"]
                .astype(str)
                .value_counts()
            )

            show_bar_chart(
                causes,
                "Most Common Causes of Safety Incidents"
            )

        # QUESTION 6
        elif selected_question == questions[5]:

            st.write(
                "The following worker records meet at least one "
                "management review criterion: PPE compliance below "
                "95%, at least two near misses, or at least two "
                "previous incidents."
            )

            management_attention = workers[
                (workers["PPE compliance"] < 95)
                | (workers["Near misses"] >= 2)
                | (workers["Previous incidents"] >= 2)
            ]

            st.metric(
                "Worker Records Flagged for Review",
                len(management_attention)
            )

            show_result_table(management_attention)

        # QUESTION 7
        elif selected_question == questions[6]:

            normal = equipment[
                (equipment["Temperature"] < 80)
                & (equipment["Vibration"] < 5)
                & (
                    equipment["Maintenance status"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    == "operational"
                )
            ]

            percentage = (
                len(normal) / len(equipment) * 100
                if len(equipment) > 0
                else 0
            )

            st.metric(
                "Equipment Meeting Normal-Operation Rules",
                f"{percentage:.1f}%"
            )

            show_result_table(normal)

            st.caption(
                "Normal operation is defined here using the project's "
                "temperature, vibration and maintenance-status rules."
            )

        # QUESTION 8
        elif selected_question == questions[7]:

            critical_alerts = equipment[
                (equipment["Temperature"] >= 100)
                | (equipment["Vibration"] >= 8)
                | (
                    equipment["Maintenance status"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    == "critical"
                )
            ]

            st.metric(
                "Equipment Units with Critical Alerts",
                len(critical_alerts)
            )

            show_result_table(critical_alerts)

            st.caption(
                "These are rule-based flags. Verify alert thresholds "
                "against the manufacturer's limits and site procedures."
            )

        # QUESTION 9
        elif selected_question == questions[8]:

            st.write(
                "Review incident frequency and equipment downtime "
                "to identify areas that may need further investigation."
            )

            st.subheader("Safety by Department")

            show_bar_chart(
                incidents["Department"].value_counts(),
                "Recorded Incidents"
            )

            st.subheader("Downtime by Equipment Type")

            show_bar_chart(
                equipment.groupby("Equipment type")["Downtime"]
                .sum()
                .sort_values(ascending=False),
                "Recorded Downtime"
            )

        # QUESTION 10
        elif selected_question == questions[9]:

            st.subheader("Recommended Actions")

            recommendations = [
                (
                    "Worker safety",
                    "Investigate departments with repeated incidents "
                    "and review incident causes."
                ),
                (
                    "PPE compliance",
                    "Review workers whose recorded PPE compliance "
                    "is below the 95% project threshold."
                ),
                (
                    "Near misses",
                    "Investigate repeated near misses and use findings "
                    "to improve preventive controls."
                ),
                (
                    "Equipment downtime",
                    "Investigate equipment with high downtime and "
                    "identify recurring causes."
                ),
                (
                    "Abnormal conditions",
                    "Inspect equipment with abnormal vibration or "
                    "temperature using approved site procedures."
                ),
                (
                    "Maintenance",
                    "Review overdue maintenance and confirm outstanding "
                    "work orders."
                ),
                (
                    "Management review",
                    "Track trends over time and verify that corrective "
                    "actions are completed."
                )
            ]

            for title, description in recommendations:
                st.markdown(
                    f"""
                    <div class="mine-card">
                        <div class="mine-card-title">
                            &#9679; {title}
                        </div>
                        <div class="mine-card-text">
                            {description}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.write("")

    # ------------------------------------------------------
    # FOOTER
    # ------------------------------------------------------

    st.divider()

    st.markdown("""
    <div style="text-align:center; padding:12px;">
        <div style="color:#F5A623; font-weight:bold; font-size:16px;">
            KHWEZI MINING MONITORING SYSTEM
        </div>
        <div style="color:#94A3B8; font-size:12px;">
            Worker Safety | Equipment Performance | Mine Data Analytics
        </div>
        <div style="color:#64748B; font-size:11px; margin-top:6px;">
            Decision-support prototype — verify alerts and findings
            against site procedures.
        </div>
    </div>
    """, unsafe_allow_html=True)
