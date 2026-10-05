import streamlit as st
import pandas as pd


# ==================================================
# LOAD DATA
# ==================================================

def load_worker_data():
    return pd.read_csv("data/workers.csv")


def load_incident_data():
    return pd.read_csv("data/incidents.csv")


def load_equipment_data():
    return pd.read_csv("data/equipment.csv")


# ==================================================
# RISK CLASSIFICATION
# ==================================================

def classify_risk(risk_score):

    if risk_score <= 4:
        return "Low"

    elif risk_score <= 9:
        return "Medium"

    elif risk_score <= 16:
        return "High"

    return "Critical"


# ==================================================
# WORKER RISK
# ==================================================

def calculate_worker_likelihood(row):

    score = 1

    ppe = pd.to_numeric(
        row["PPE compliance"],
        errors="coerce"
    )

    fatigue = str(
        row["Fatigue level"]
    ).strip().lower()

    near_misses = pd.to_numeric(
        row["Near misses"],
        errors="coerce"
    )

    previous_incidents = pd.to_numeric(
        row["Previous incidents"],
        errors="coerce"
    )

    if pd.notna(ppe):

        if ppe < 80:
            score += 2

        elif ppe < 95:
            score += 1

    if fatigue == "high":
        score += 2

    elif fatigue == "medium":
        score += 1

    if pd.notna(near_misses):

        if near_misses >= 3:
            score += 2

        elif near_misses >= 1:
            score += 1

    if pd.notna(previous_incidents):

        if previous_incidents >= 3:
            score += 2

        elif previous_incidents >= 1:
            score += 1

    return min(score, 5)


def calculate_worker_consequence(row):

    score = 1

    previous_incidents = pd.to_numeric(
        row["Previous incidents"],
        errors="coerce"
    )

    near_misses = pd.to_numeric(
        row["Near misses"],
        errors="coerce"
    )

    fatigue = str(
        row["Fatigue level"]
    ).strip().lower()

    if pd.notna(previous_incidents):

        if previous_incidents >= 3:
            score += 2

        elif previous_incidents >= 1:
            score += 1

    if fatigue == "high":
        score += 1

    if pd.notna(near_misses):

        if near_misses >= 3:
            score += 1

    return min(score, 5)


# ==================================================
# INCIDENT RISK
# ==================================================

def calculate_incident_likelihood(row):

    score = 1

    status = str(
        row["Incident status"]
    ).strip().lower()

    if status in [
        "open",
        "active",
        "under investigation"
    ]:
        score += 2

    elif status == "pending":
        score += 1

    return min(score, 5)


def calculate_incident_consequence(row):

    severity = str(
        row["Severity"]
    ).strip().lower()

    injury = str(
        row["Injury status"]
    ).strip().lower()

    lost_time = str(
        row["Lost-time injury status"]
    ).strip().lower()

    if severity == "critical":
        score = 5

    elif severity == "high":
        score = 4

    elif severity == "moderate":
        score = 3

    elif severity == "minor":
        score = 2

    else:
        score = 1

    if injury in [
        "yes",
        "injury",
        "injured"
    ]:
        score += 1

    if lost_time in [
        "yes",
        "true"
    ]:
        score += 1

    return min(score, 5)


# ==================================================
# EQUIPMENT RISK
# ==================================================

def calculate_equipment_likelihood(row):

    score = 1

    temperature = pd.to_numeric(
        row["Temperature"],
        errors="coerce"
    )

    vibration = pd.to_numeric(
        row["Vibration"],
        errors="coerce"
    )

    downtime = pd.to_numeric(
        row["Downtime"],
        errors="coerce"
    )

    maintenance = str(
        row["Maintenance status"]
    ).strip().lower()

    if pd.notna(temperature):

        if temperature > 100:
            score += 3

        elif temperature >= 80:
            score += 2

    if pd.notna(vibration):

        if vibration > 8:
            score += 2

        elif vibration >= 5:
            score += 1

    if maintenance in [
        "overdue",
        "critical"
    ]:
        score += 2

    elif maintenance in [
        "under maintenance",
        "maintenance required"
    ]:
        score += 1

    if pd.notna(downtime):

        if downtime >= 100:
            score += 2

        elif downtime >= 50:
            score += 1

    return min(score, 5)


def calculate_equipment_consequence(row):

    score = 1

    temperature = pd.to_numeric(
        row["Temperature"],
        errors="coerce"
    )

    vibration = pd.to_numeric(
        row["Vibration"],
        errors="coerce"
    )

    brake = str(
        row["Brake status"]
    ).strip().lower()

    tyre = str(
        row["Tyre status"]
    ).strip().lower()

    engine = str(
        row["Engine status"]
    ).strip().lower()

    if pd.notna(temperature):

        if temperature > 100:
            score += 2

        elif temperature >= 80:
            score += 1

    if pd.notna(vibration):

        if vibration > 8:
            score += 2

        elif vibration >= 5:
            score += 1

    if brake not in [
        "good",
        "normal",
        "ok",
        "operational"
    ]:
        score += 1

    if tyre not in [
        "good",
        "normal",
        "ok",
        "operational"
    ]:
        score += 1

    if engine not in [
        "good",
        "normal",
        "ok",
        "operational"
    ]:
        score += 1

    return min(score, 5)


# ==================================================
# CREATE RISK DATA
# ==================================================

def create_worker_risk_data(workers):

    workers = workers.copy()

    workers["Likelihood"] = workers.apply(
        calculate_worker_likelihood,
        axis=1
    )

    workers["Consequence"] = workers.apply(
        calculate_worker_consequence,
        axis=1
    )

    workers["Risk Score"] = (
        workers["Likelihood"]
        * workers["Consequence"]
    )

    workers["Risk Level"] = workers[
        "Risk Score"
    ].apply(
        classify_risk
    )

    return workers


def create_incident_risk_data(incidents):

    incidents = incidents.copy()

    incidents["Likelihood"] = incidents.apply(
        calculate_incident_likelihood,
        axis=1
    )

    incidents["Consequence"] = incidents.apply(
        calculate_incident_consequence,
        axis=1
    )

    incidents["Risk Score"] = (
        incidents["Likelihood"]
        * incidents["Consequence"]
    )

    incidents["Risk Level"] = incidents[
        "Risk Score"
    ].apply(
        classify_risk
    )

    return incidents


def create_equipment_risk_data(equipment):

    equipment = equipment.copy()

    equipment["Likelihood"] = equipment.apply(
        calculate_equipment_likelihood,
        axis=1
    )

    equipment["Consequence"] = equipment.apply(
        calculate_equipment_consequence,
        axis=1
    )

    equipment["Risk Score"] = (
        equipment["Likelihood"]
        * equipment["Consequence"]
    )

    equipment["Risk Level"] = equipment[
        "Risk Score"
    ].apply(
        classify_risk
    )

    return equipment


# ==================================================
# RISK ASSESSMENT PAGE
# ==================================================

def render_risk_assessment_page():

    workers = load_worker_data()
    incidents = load_incident_data()
    equipment = load_equipment_data()

    workers = create_worker_risk_data(workers)
    incidents = create_incident_risk_data(incidents)
    equipment = create_equipment_risk_data(equipment)

    st.title("Risk Assessment")

    st.write(
        "Risk Score = Likelihood × Consequence"
    )

    st.info(
        "Low: 1–4 | Medium: 5–9 | "
        "High: 10–16 | Critical: 17–25"
    )

    st.divider()

    # ==================================================
    # WORKER RISK
    # ==================================================

    st.header("Worker Safety Risk")

    worker_counts = (
        workers["Risk Level"]
        .value_counts()
        .reindex(
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ],
            fill_value=0
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Low",
            worker_counts["Low"]
        )

    with col2:
        st.metric(
            "Medium",
            worker_counts["Medium"]
        )

    with col3:
        st.metric(
            "High",
            worker_counts["High"]
        )

    with col4:
        st.metric(
            "Critical",
            worker_counts["Critical"]
        )

    if (
        worker_counts["High"] > 0
        or worker_counts["Critical"] > 0
    ):
        st.warning(
            "High or critical worker risks require attention."
        )

    st.dataframe(
        workers[
            [
                "Worker ID",
                "Department",
                "Job role",
                "Shift",
                "Likelihood",
                "Consequence",
                "Risk Score",
                "Risk Level"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================================
    # INCIDENT RISK
    # ==================================================

    st.header("Incident Risk")

    incident_counts = (
        incidents["Risk Level"]
        .value_counts()
        .reindex(
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ],
            fill_value=0
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Low",
            incident_counts["Low"]
        )

    with col2:
        st.metric(
            "Medium",
            incident_counts["Medium"]
        )

    with col3:
        st.metric(
            "High",
            incident_counts["High"]
        )

    with col4:
        st.metric(
            "Critical",
            incident_counts["Critical"]
        )

    if (
        incident_counts["High"] > 0
        or incident_counts["Critical"] > 0
    ):
        st.warning(
            "High or critical incident risks require attention."
        )

    st.dataframe(
        incidents[
            [
                "Incident ID",
                "Date",
                "Time",
                "Shift",
                "Location",
                "Department",
                "Incident type",
                "Severity",
                "Likelihood",
                "Consequence",
                "Risk Score",
                "Risk Level"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================================
    # EQUIPMENT RISK
    # ==================================================

    st.header("Equipment Risk")

    equipment_counts = (
        equipment["Risk Level"]
        .value_counts()
        .reindex(
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ],
            fill_value=0
        )
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Low",
            equipment_counts["Low"]
        )

    with col2:
        st.metric(
            "Medium",
            equipment_counts["Medium"]
        )

    with col3:
        st.metric(
            "High",
            equipment_counts["High"]
        )

    with col4:
        st.metric(
            "Critical",
            equipment_counts["Critical"]
        )

    if (
        equipment_counts["High"] > 0
        or equipment_counts["Critical"] > 0
    ):
        st.warning(
            "High or critical equipment risks require attention."
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
                "Likelihood",
                "Consequence",
                "Risk Score",
                "Risk Level"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # ==================================================
    # OVERALL RISK
    # ==================================================

    st.header("Overall Risk Summary")

    all_risks = pd.concat(
        [
            workers[["Risk Level"]],
            incidents[["Risk Level"]],
            equipment[["Risk Level"]]
        ],
        ignore_index=True
    )

    overall_counts = (
        all_risks["Risk Level"]
        .value_counts()
        .reindex(
            [
                "Low",
                "Medium",
                "High",
                "Critical"
            ],
            fill_value=0
        )
    )

    st.bar_chart(
        overall_counts
    )

    if (
        overall_counts["Critical"] > 0
    ):
        st.error(
            "Critical risks are currently present."
        )

    elif (
        overall_counts["High"] > 0
    ):
        st.warning(
            "High risks are currently present."
        )
    else:
        st.success(
            "No high or critical risks are currently present."
        )
