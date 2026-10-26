import streamlit as st
import pandas as pd


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

def load_worker_data():

    return pd.read_csv(
        "workers.csv"
    )


def load_incident_data():

    return pd.read_csv(
        "incidents.csv"
    )


def load_equipment_data():

    return pd.read_csv(
        "equipment.csv"
    )


# --------------------------------------------------
# CALCULATE EQUIPMENT AVAILABILITY
# --------------------------------------------------

def calculate_availability(equipment):

    total_time = (
        equipment["Operating hours"]
        + equipment["Downtime"]
    )

    equipment["Availability"] = (
        equipment["Operating hours"]
        / total_time
    ) * 100

    return equipment


# --------------------------------------------------
# RENDER QUESTIONS PAGE
# --------------------------------------------------

def render_questions_page():

    workers = load_worker_data()

    incidents = load_incident_data()

    equipment = load_equipment_data()

    equipment = calculate_availability(
        equipment
    )

    st.title("Safety & Equipment Questions")

    st.write(
        "Select a question from the project brief "
        "to view the answer based on the monitoring data."
    )

    st.divider()

    # --------------------------------------------------
    # QUESTION CATEGORIES
    # --------------------------------------------------

    categories = [
        "Health and Safety",
        "Equipment",
        "Integrated Safety and Equipment Analysis"
    ]

    selected_category = st.selectbox(
        "Question Category",
        categories
    )

    # --------------------------------------------------
    # HEALTH AND SAFETY QUESTIONS
    # --------------------------------------------------

    if selected_category == "Health and Safety":

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
            "Select a question",
            questions
        )

        st.divider()

        # --------------------------------------------------
        # QUESTION 1
        # --------------------------------------------------

        if selected_question == questions[0]:

            st.metric(
                "Safety Incidents",
                len(incidents)
            )

        # --------------------------------------------------
        # QUESTION 2
        # --------------------------------------------------

        elif selected_question == questions[1]:

            department_counts = (
                incidents[
                    "Department"
                ]
                .value_counts()
            )

            if not department_counts.empty:

                department = (
                    department_counts
                    .idxmax()
                )

                count = (
                    department_counts
                    .max()
                )

                st.success(
                    f"{department} has the highest "
                    f"number of incidents with {count} incidents."
                )

                st.bar_chart(
                    department_counts
                )

        # --------------------------------------------------
        # QUESTION 3
        # --------------------------------------------------

        elif selected_question == questions[2]:

            shift_counts = (
                incidents[
                    "Shift"
                ]
                .value_counts()
            )

            if not shift_counts.empty:

                shift = (
                    shift_counts
                    .idxmax()
                )

                count = (
                    shift_counts
                    .max()
                )

                st.success(
                    f"The {shift} shift records the most "
                    f"incidents with {count} incidents."
                )

                st.bar_chart(
                    shift_counts
                )

        # --------------------------------------------------
        # QUESTION 4
        # --------------------------------------------------

        elif selected_question == questions[3]:

            compliant_workers = workers[
                workers["PPE compliance"] >= 95
            ]

            percentage = (
                len(compliant_workers)
                / len(workers)
            ) * 100

            st.metric(
                "PPE Compliance",
                f"{percentage:.1f}%"
            )

        # --------------------------------------------------
        # QUESTION 5
        # --------------------------------------------------

        elif selected_question == questions[4]:

            near_misses = workers[
                "Near misses"
            ].sum()

            st.metric(
                "Near Misses",
                int(near_misses)
            )

        # --------------------------------------------------
        # QUESTION 6
        # --------------------------------------------------

        elif selected_question == questions[5]:

            incident_types = (
                incidents[
                    "Incident type"
                ]
                .value_counts()
            )

            st.write(
                "Most frequent incident types:"
            )

            st.bar_chart(
                incident_types
            )

        # --------------------------------------------------
        # QUESTION 7
        # --------------------------------------------------

        elif selected_question == questions[6]:

            severity = (
                incidents[
                    "Severity"
                ]
                .astype(str)
                .str.lower()
            )

            high_critical = incidents[
                severity.isin(
                    [
                        "high",
                        "critical"
                    ]
                )
            ]

            st.metric(
                "High or Critical Incidents",
                len(high_critical)
            )

        # --------------------------------------------------
        # QUESTION 8
        # --------------------------------------------------

        elif selected_question == questions[7]:

            department_risk = (
                workers
                .groupby("Department")[
                    [
                        "Near misses",
                        "Previous incidents",
                        "Fatigue level"
                    ]
                ]
                .sum(
                    numeric_only=True
                )
            )

            st.write(
                "Departments with the highest "
                "safety indicators:"
            )

            st.dataframe(
                department_risk,
                use_container_width=True
            )

        # --------------------------------------------------
        # QUESTION 9
        # --------------------------------------------------

        elif selected_question == questions[8]:

            shift_counts = (
                incidents[
                    "Shift"
                ]
                .value_counts()
            )

            st.write(
                "Incident distribution by shift:"
            )

            st.bar_chart(
                shift_counts
            )

            if len(shift_counts) >= 2:

                highest = shift_counts.max()

                lowest = shift_counts.min()

                difference = highest - lowest

                st.info(
                    f"The difference between the highest "
                    f"and lowest incident counts is "
                    f"{difference}."
                )

        # --------------------------------------------------
        # QUESTION 10
        # --------------------------------------------------

        elif selected_question == questions[9]:

            st.write(
                "Safety conditions requiring attention "
                "are identified using PPE compliance, "
                "fatigue, near misses and previous incidents."
            )

            attention = workers[
                (
                    workers["PPE compliance"] < 95
                )
                |
                (
                    workers["Near misses"] >= 2
                )
                |
                (
                    workers["Previous incidents"] >= 2
                )
            ]

            st.dataframe(
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
                ],
                use_container_width=True,
                hide_index=True
            )


    # --------------------------------------------------
    # EQUIPMENT QUESTIONS
    # --------------------------------------------------

    elif selected_category == "Equipment":

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
            "Select a question",
            questions
        )

        st.divider()

        # --------------------------------------------------
        # QUESTION 1
        # --------------------------------------------------

        if selected_question == questions[0]:

            equipment_row = equipment.loc[
                equipment["Downtime"].idxmax()
            ]

            st.success(
                f"{equipment_row['Equipment ID']} "
                f"has the highest downtime: "
                f"{equipment_row['Downtime']} hours."
            )

        # --------------------------------------------------
        # QUESTION 2
        # --------------------------------------------------

        elif selected_question == questions[1]:

            equipment_row = equipment.loc[
                equipment["Availability"].idxmin()
            ]

            st.success(
                f"{equipment_row['Equipment ID']} "
                f"has the lowest availability: "
                f"{equipment_row['Availability']:.1f}%."
            )

        # --------------------------------------------------
        # QUESTION 3
        # --------------------------------------------------

        elif selected_question == questions[2]:

            equipment_row = equipment.loc[
                equipment["Vibration"].idxmax()
            ]

            st.success(
                f"{equipment_row['Equipment ID']} "
                f"has the highest vibration: "
                f"{equipment_row['Vibration']}."
            )

        # --------------------------------------------------
        # QUESTION 4
        # --------------------------------------------------

        elif selected_question == questions[3]:

            equipment_row = equipment.loc[
                equipment["Temperature"].idxmax()
            ]

            st.success(
                f"{equipment_row['Equipment ID']} "
                f"has the highest operating temperature: "
                f"{equipment_row['Temperature']}."
            )

        # --------------------------------------------------
        # QUESTION 5
        # --------------------------------------------------

        elif selected_question == questions[4]:

            st.info(
                "Alert generation will be based on abnormal "
                "equipment conditions such as high temperature, "
                "high vibration and equipment status."
            )

            alerts = equipment[
                (
                    equipment["Temperature"] >= 80
                )
                |
                (
                    equipment["Vibration"] >= 5
                )
                |
                (
                    equipment["Maintenance status"]
                    .astype(str)
                    .str.lower()
                    .isin(
                        [
                            "overdue",
                            "critical"
                        ]
                    )
                )
            ]

            st.dataframe(
                alerts,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------------------
        # QUESTION 6
        # --------------------------------------------------

        elif selected_question == questions[5]:

            maintenance = equipment[
                equipment["Maintenance status"]
                .astype(str)
                .str.lower()
                .isin(
                    [
                        "under maintenance",
                        "maintenance required",
                        "overdue"
                    ]
                )
            ]

            st.dataframe(
                maintenance,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------------------
        # QUESTION 7
        # --------------------------------------------------

        elif selected_question == questions[6]:

            overdue = equipment[
                equipment["Maintenance status"]
                .astype(str)
                .str.lower()
                == "overdue"
            ]

            if overdue.empty:

                st.success(
                    "No equipment is currently marked overdue."
                )

            else:

                st.dataframe(
                    overdue,
                    use_container_width=True,
                    hide_index=True
                )

        # --------------------------------------------------
        # QUESTION 8
        # --------------------------------------------------

        elif selected_question == questions[7]:

            average_availability = (
                equipment["Availability"]
                .mean()
            )

            st.metric(
                "Average Equipment Availability",
                f"{average_availability:.1f}%"
            )

        # --------------------------------------------------
        # QUESTION 9
        # --------------------------------------------------

        elif selected_question == questions[8]:

            downtime = (
                equipment
                .groupby("Equipment type")[
                    "Downtime"
                ]
                .sum()
                .sort_values(
                    ascending=False
                )
            )

            st.bar_chart(
                downtime
            )

            if not downtime.empty:

                st.success(
                    f"{downtime.idxmax()} has the "
                    f"highest total downtime."
                )

        # --------------------------------------------------
        # QUESTION 10
        # --------------------------------------------------

        elif selected_question == questions[9]:

            inspection = equipment[
                (
                    equipment["Temperature"] >= 80
                )
                |
                (
                    equipment["Vibration"] >= 5
                )
                |
                (
                    equipment["Brake status"]
                    .astype(str)
                    .str.lower()
                    != "good"
                )
                |
                (
                    equipment["Engine status"]
                    .astype(str)
                    .str.lower()
                    != "good"
                )
            ]

            st.dataframe(
                inspection,
                use_container_width=True,
                hide_index=True
            )


    # --------------------------------------------------
    # INTEGRATED QUESTIONS
    # --------------------------------------------------

    else:

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
            "Select a question",
            questions
        )

        st.divider()

        # --------------------------------------------------
        # QUESTION 1
        # --------------------------------------------------

        if selected_question == questions[0]:

            shift_counts = (
                incidents[
                    "Shift"
                ]
                .value_counts()
            )

            st.bar_chart(
                shift_counts
            )

            st.write(
                "This shows the distribution of "
                "incidents across shifts."
            )

        # --------------------------------------------------
        # QUESTION 2
        # --------------------------------------------------

        elif selected_question == questions[1]:

            department_incidents = (
                incidents[
                    "Department"
                ]
                .value_counts()
            )

            department_downtime = (
                equipment
                .groupby("Equipment type")[
                    "Downtime"
                ]
                .sum()
            )

            st.write(
                "Incident levels by department:"
            )

            st.bar_chart(
                department_incidents
            )

            st.write(
                "Equipment downtime by equipment type:"
            )

            st.bar_chart(
                department_downtime
            )

        # --------------------------------------------------
        # QUESTION 3
        # --------------------------------------------------

        elif selected_question == questions[2]:

            alerts = equipment[
                (
                    equipment["Temperature"] >= 80
                )
                |
                (
                    equipment["Vibration"] >= 5
                )
                |
                (
                    equipment["Maintenance status"]
                    .astype(str)
                    .str.lower()
                    .isin(
                        [
                            "overdue",
                            "critical"
                        ]
                    )
                )
            ]

            st.dataframe(
                alerts,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------------------
        # QUESTION 4
        # --------------------------------------------------

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

            st.dataframe(
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
                ],
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------------------
        # QUESTION 5
        # --------------------------------------------------

        elif selected_question == questions[4]:

            causes = (
                incidents[
                    "Cause"
                ]
                .astype(str)
                .value_counts()
            )

            st.bar_chart(
                causes
            )

        # --------------------------------------------------
        # QUESTION 6
        # --------------------------------------------------

        elif selected_question == questions[5]:

            st.write(
                "Indicators requiring management attention "
                "include repeated incidents, near misses, "
                "poor PPE compliance and abnormal equipment "
                "conditions."
            )

            management_attention = workers[
                (
                    workers["PPE compliance"] < 95
                )
                |
                (
                    workers["Near misses"] >= 2
                )
                |
                (
                    workers["Previous incidents"] >= 2
                )
            ]

            st.dataframe(
                management_attention,
                use_container_width=True,
                hide_index=True
            )

        # --------------------------------------------------
        # QUESTION 7
        # --------------------------------------------------

        elif selected_question == questions[6]:

            normal = equipment[
                (
                    equipment["Temperature"] < 80
                )
                &
                (
                    equipment["Vibration"] < 5
                )
                &
                (
                    equipment["Maintenance status"]
                    .astype(str)
                    .str.lower()
                    == "operational"
                )
            ]

            percentage = (
                len(normal)
                / len(equipment)
            ) * 100

            st.metric(
                "Operating Normally",
                f"{percentage:.1f}%"
            )

        # --------------------------------------------------
        # QUESTION 8
        # --------------------------------------------------

        elif selected_question == questions[7]:

            critical_alerts = equipment[
                (
                    equipment["Temperature"] >= 100
                )
                |
                (
                    equipment["Vibration"] >= 8
                )
                |
                (
                    equipment["Maintenance status"]
                    .astype(str)
                    .str.lower()
                    == "critical"
                )
            ]

            st.metric(
                "Critical Alerts",
                len(critical_alerts)
            )

        # --------------------------------------------------
        # QUESTION 9
        # --------------------------------------------------

        elif selected_question == questions[8]:

            st.write(
                "Areas requiring attention are identified "
                "from incident frequency, worker safety "
                "indicators and equipment condition."
            )

            st.subheader(
                "Incident Areas"
            )

            st.bar_chart(
                incidents[
                    "Department"
                ].value_counts()
            )

            st.subheader(
                "Equipment Areas"
            )

            st.bar_chart(
                equipment
                .groupby("Equipment type")[
                    "Downtime"
                ]
                .sum()
            )

        # --------------------------------------------------
        # QUESTION 10
        # --------------------------------------------------

        elif selected_question == questions[9]:

            st.subheader(
                "Recommended Actions"
            )

            st.write(
                "• Investigate departments with repeated incidents."
            )

            st.write(
                "• Review workers with poor PPE compliance."
            )

            st.write(
                "• Investigate repeated near misses."
            )

            st.write(
                "• Prioritise equipment with high downtime."
            )

            st.write(
                "• Inspect equipment with abnormal vibration "
                "or temperature."
            )

            st.write(
                "• Review overdue maintenance."
            )

            st.write(
                "• Investigate recurring incident causes."
            )
