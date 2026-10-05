import streamlit as st
import pandas as pd


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


def calculate_worker_risk(row):

    score = 0

    # PPE compliance
    if row["PPE compliance"] < 80:
        score += 3
    elif row["PPE compliance"] < 90:
        score += 2
    elif row["PPE compliance"] < 95:
        score += 1

    # Safety training
    if str(
        row["Safety training status"]
    ).lower() not in [
        "completed",
        "complete",
        "up to date"
    ]:
        score += 2

    # Fatigue
    fatigue = str(
        row["Fatigue level"]
    ).lower()

    if fatigue == "high":
        score += 3
    elif fatigue == "medium":
        score += 2
    elif fatigue == "low":
        score += 1

    # Near misses
    near_misses = row["Near misses"]

    if near_misses >= 3:
        score += 3
    elif near_misses >= 1:
        score += 1

    # Previous incidents
    previous_incidents = row[
        "Previous incidents"
    ]

    if previous_incidents >= 3:
        score += 3
    elif previous_incidents >= 1:
        score += 1

    return score


def get_risk_level(score):

    if score >= 9:
        return "High"

    elif score >= 5:
        return "Medium"

    else:
        return "Low"


def calculate_incident_risk(row):

    score = 0

    severity = str(
        row["Severity"]
    ).lower()

    if severity == "critical":
        score += 5

    elif severity == "serious":
        score += 4

    elif severity == "moderate":
        score += 2

    elif severity == "minor":
        score += 1

    injury = str(
        row["Injury status"]
    ).lower()

    if injury in ["yes", "injury"]:

        score += 2

    lost_time = str(
        row["Lost-time injury status"]
    ).lower()

    if lost_time == "yes":

        score += 3

    return score


def calculate_equipment_risk(row):

    score = 0

    # Temperature
    temperature = row["Temperature"]

    if temperature >= 100:
        score += 3

    elif temperature >= 80:
        score += 2

    # Vibration
    vibration = row["Vibration"]

    if vibration >= 8:
        score += 3

    elif vibration >= 5:
        score += 2

    # Brake status
    brake = str(
        row["Brake status"]
    ).lower()

    if brake not in [
        "good",
        "normal",
        "ok",
        "operational"
    ]:
        score += 2

    # Tyre status
    tyre = str(
        row["Tyre status"]
    ).lower()

    if tyre not in [
        "good",
        "normal",
        "ok",
        "operational"
    ]:
        score += 2

    # Engine status
    engine = str(
        row["Engine status"]
    ).lower()

    if engine not in [
        "good",
        "normal",
        "ok",
        "operational"
    ]:
        score += 2

    # Maintenance status
    maintenance = str(
        row["Maintenance status"]
    ).lower()

    if maintenance in [
        "overdue",
        "critical",
        "under maintenance"
    ]:
        score += 2

    return score


def render_risk_assessment_page():

    workers = load_worker_data()

    incidents = load_incident_data()

    equipment = load_equipment_data()

    st.title("Risk Assessment")

    st.write(
        "Risk is calculated from worker, incident "
        "and equipment information."
    )

    st.divider()

    # --------------------------------------------------
    # WORKER RISK
    # --------------------------------------------------

    workers["Risk Score"] = workers.apply(
        calculate_worker_risk,
        axis=1
    )

    workers["Risk Level"] = workers[
        "Risk Score"
    ].apply(
        get_risk_level
    )

    st.subheader("Worker Risk Assessment")

    high_worker_risk = len(
        workers[
            workers["Risk Level"] == "High"
        ]
    )

    medium_worker_risk = len(
        workers[
            workers["Risk Level"] == "Medium"
        ]
    )

    low_worker_risk = len(
        workers[
            workers["Risk Level"] == "Low"
        ]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "High Risk Workers",
            high_worker_risk
        )

    with col2:
        st.metric(
            "Medium Risk Workers",
            medium_worker_risk
        )

    with col3:
        st.metric(
            "Low Risk Workers",
            low_worker_risk
        )

    st.dataframe(
        workers[
            [
                "Worker ID",
                "Department",
                "Job role",
                "Shift",
                "PPE compliance",
                "Fatigue level",
                "Near misses",
                "Previous incidents",
                "Risk Score",
                "Risk Level"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------
    # INCIDENT RISK
    # --------------------------------------------------

    incidents["Risk Score"] = incidents.apply(
        calculate_incident_risk,
        axis=1
    )

    incidents["Risk Level"] = incidents[
        "Risk Score"
    ].apply(
        get_risk_level
    )

    st.subheader("Incident Risk Assessment")

    incident_risk_counts = (
        incidents["Risk Level"]
        .value_counts()
    )

    st.bar_chart(
        incident_risk_counts
    )

    st.dataframe(
        incidents[
            [
                "Incident ID",
                "Date",
                "Department",
                "Incident type",
                "Severity",
                "Injury status",
                "Lost-time injury status",
                "Risk Score",
                "Risk Level"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------------------------
    # EQUIPMENT RISK
    # --------------------------------------------------

    equipment["Risk Score"] = equipment.apply(
        calculate_equipment_risk,
        axis=1
    )

    equipment["Risk Level"] = equipment[
        "Risk Score"
    ].apply(
        get_risk_level
    )

    st.subheader("Equipment Risk Assessment")

    equipment_risk_counts = (
        equipment["Risk Level"]
        .value_counts()
    )

    st.bar_chart(
        equipment_risk_counts
    )

    st.dataframe(
        equipment[
            [
                "Equipment ID",
                "Equipment type",
                "Manufacturer",
                "Temperature",
                "Vibration",
                "Brake status",
                "Tyre status",
                "Engine status",
                "Maintenance status",
                "Risk Score",
                "Risk Level"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )
