import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --------------------------------------------------
# FILE LOCATIONS
# --------------------------------------------------

MANAGEMENT_FILE = "risk_management.csv"

# Risk assessment follows the brief:
# Risk Score = Likelihood × Consequence
# Both values must be between 1 and 5.


# --------------------------------------------------
# LOAD CSV FILES
# --------------------------------------------------

def load_data(filename):
    """Load a CSV from the project folder or the data folder."""

    possible_paths = [
        filename,
        os.path.join("data", filename)
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return pd.read_csv(path)

    raise FileNotFoundError(
        f"{filename} could not be found in the project folder or data folder."
    )


def load_risk_management():
    """Load saved risk assessments, statuses, notes and removed risks."""

    columns = [
        "Risk Type",
        "Record ID",
        "Status",
        "Notes",
        "Removed",
        "Updated At"
    ]

    if os.path.exists(MANAGEMENT_FILE):
        try:
            saved = pd.read_csv(
                MANAGEMENT_FILE,
                dtype=str
            ).fillna("")

            # Add any missing columns so older files remain usable.
            for column in columns:
                if column not in saved.columns:
                    saved[column] = ""

            return saved[columns]

        except (pd.errors.ParserError, OSError, UnicodeDecodeError):
            st.warning(
                "The saved risk-management file could not be read. "
                "A new one will be created when you save a change."
            )

    return pd.DataFrame(columns=columns)


def save_risk_management(management):
    """Save risk assessments separately from the original CSV files."""

    management.to_csv(MANAGEMENT_FILE, index=False)


def update_risk_record(
    management,
    risk_type,
    record_id,
    status=None,
    notes=None,
    removed=None
):
    """Add or update one saved risk record without duplicating it."""

    risk_type = str(risk_type)
    record_id = str(record_id)

    # Make sure the management table has the required columns.
    columns = [
        "Risk Type", "Record ID", "Status",
        "Notes", "Removed", "Updated At"
    ]

    if management.empty:
        management = pd.DataFrame(columns=columns)

    for column in columns:
        if column not in management.columns:
            management[column] = ""

    matches = (
        (management["Risk Type"].astype(str) == risk_type)
        & (management["Record ID"].astype(str) == record_id)
    )

    if matches.any():
        index = management.index[matches][0]
    else:
        # Use a new index so existing records are not overwritten.
        index = max(management.index, default=-1) + 1

        management.loc[index, "Risk Type"] = risk_type
        management.loc[index, "Record ID"] = record_id
        management.loc[index, "Status"] = "Open"
        management.loc[index, "Notes"] = ""
        management.loc[index, "Removed"] = "False"

    if status is not None:
        management.loc[index, "Status"] = status

    if notes is not None:
        management.loc[index, "Notes"] = notes

    if removed is not None:
        management.loc[index, "Removed"] = str(removed)

    management.loc[index, "Updated At"] = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return management


# --------------------------------------------------
# RISK CLASSIFICATION
# --------------------------------------------------

def classify_risk(risk_score):
    if risk_score <= 4:
        return "Low"
    elif risk_score <= 9:
        return "Medium"
    elif risk_score <= 16:
        return "High"
    return "Critical"


# Worker Risk

def calculate_worker_likelihood(row):
    score = 1
    ppe = pd.to_numeric(row["PPE compliance"], errors="coerce")
    fatigue = str(row["Fatigue level"]).strip().lower()
    near_misses = pd.to_numeric(row["Near misses"], errors="coerce")
    previous_incidents = pd.to_numeric(row["Previous incidents"], errors="coerce")

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
    previous_incidents = pd.to_numeric(row["Previous incidents"], errors="coerce")
    near_misses = pd.to_numeric(row["Near misses"], errors="coerce")
    fatigue = str(row["Fatigue level"]).strip().lower()

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


# Incident Risk

def calculate_incident_likelihood(row):
    score = 1
    status = str(row["Incident status"]).strip().lower()

    # Matches CSV values: "open", "under investigation", "corrective action pending"
    if status in ["open", "active", "under investigation", "corrective action pending"]:
        score += 2
    elif "pending" in status:
        score += 1

    return min(score, 5)


def calculate_incident_consequence(row):
    severity = str(row["Severity"]).strip().lower()
    injury = str(row["Injury status"]).strip().lower()
    lost_time = str(row["Lost-time injury status"]).strip().lower()

    # Fixed to match CSV values: "minor", "moderate", "serious", "critical"
    if severity == "critical":
        score = 5
    elif severity == "serious":
        score = 4
    elif severity == "moderate":
        score = 3
    elif severity == "minor":
        score = 2
    else:
        score = 1

    # Fixed to match CSV injury values: "medical treatment", "first aid", "lost time injury"
    if injury in ["yes", "injury", "injured", "medical treatment", "first aid", "lost time injury"]:
        score += 1

    if lost_time in ["yes", "true"]:
        score += 1

    return min(score, 5)


# Equipment Risk

def calculate_equipment_likelihood(row):
    score = 1
    temperature = pd.to_numeric(row["Temperature"], errors="coerce")
    vibration = pd.to_numeric(row["Vibration"], errors="coerce")
    downtime = pd.to_numeric(row["Downtime"], errors="coerce")
    maintenance = str(row["Maintenance status"]).strip().lower()

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

    if maintenance in ["overdue", "critical"]:
        score += 2
    elif maintenance in ["under maintenance", "due soon", "maintenance required"]:
        score += 1

    if pd.notna(downtime):
        if downtime >= 100:
            score += 2
        elif downtime >= 50:
            score += 1

    return min(score, 5)


def calculate_equipment_consequence(row):
    score = 1
    temperature = pd.to_numeric(row["Temperature"], errors="coerce")
    vibration = pd.to_numeric(row["Vibration"], errors="coerce")
    brake = str(row["Brake status"]).strip().lower()
    tyre = str(row["Tyre status"]).strip().lower()
    engine = str(row["Engine status"]).strip().lower()

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

    if brake not in ["good", "normal", "ok", "operational"]:
        score += 1

    if tyre not in ["good", "normal", "ok", "operational"]:
        score += 1

    if engine not in ["good", "normal", "ok", "operational"]:
        score += 1

    return min(score, 5)


# Create Risk Data

def create_worker_risk_data(workers):
    workers = workers.copy()
    workers["Likelihood"] = workers.apply(calculate_worker_likelihood, axis=1)
    workers["Consequence"] = workers.apply(calculate_worker_consequence, axis=1)
    workers["Risk Score"] = workers["Likelihood"] * workers["Consequence"]
    workers["Risk Level"] = workers["Risk Score"].apply(classify_risk)
    return workers


def create_incident_risk_data(incidents):
    incidents = incidents.copy()
    incidents["Likelihood"] = incidents.apply(calculate_incident_likelihood, axis=1)
    incidents["Consequence"] = incidents.apply(calculate_incident_consequence, axis=1)
    incidents["Risk Score"] = incidents["Likelihood"] * incidents["Consequence"]
    incidents["Risk Level"] = incidents["Risk Score"].apply(classify_risk)
    return incidents


def create_equipment_risk_data(equipment):
    equipment = equipment.copy()
    equipment["Likelihood"] = equipment.apply(calculate_equipment_likelihood, axis=1)
    equipment["Consequence"] = equipment.apply(calculate_equipment_consequence, axis=1)
    equipment["Risk Score"] = equipment["Likelihood"] * equipment["Consequence"]
    equipment["Risk Level"] = equipment["Risk Score"].apply(classify_risk)
    return equipment


# Risk Assessment Page

def render_risk_assessment_page():
    workers = load_worker_data()
    incidents = load_incident_data()
    equipment = load_equipment_data()

    workers = create_worker_risk_data(workers)
    incidents = create_incident_risk_data(incidents)
    equipment = create_equipment_risk_data(equipment)

    st.title("Risk Assessment")
    st.write("Risk Score = Likelihood × Consequence")
    st.info("Low: 1–4 | Medium: 5–9 | High: 10–16 | Critical: 17–25")
    st.divider()

    # Worker Risk
    st.header("Worker Safety Risk")
    worker_counts = workers["Risk Level"].value_counts().reindex(["Low", "Medium", "High", "Critical"], fill_value=0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Low", worker_counts["Low"])
    with col2:
        st.metric("Medium", worker_counts["Medium"])
    with col3:
        st.metric("High", worker_counts["High"])
    with col4:
        st.metric("Critical", worker_counts["Critical"])

    if worker_counts["High"] > 0 or worker_counts["Critical"] > 0:
        st.warning("High or critical worker risks require attention.")

    st.dataframe(
        workers[[
            "Worker ID", "Department", "Job role", "Shift", 
            "Likelihood", "Consequence", "Risk Score", "Risk Level"
        ]],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Incident Risk
    st.header("Incident Risk")
    incident_counts = incidents["Risk Level"].value_counts().reindex(["Low", "Medium", "High", "Critical"], fill_value=0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Low", incident_counts["Low"])
    with col2:
        st.metric("Medium", incident_counts["Medium"])
    with col3:
        st.metric("High", incident_counts["High"])
    with col4:
        st.metric("Critical", incident_counts["Critical"])

    if incident_counts["High"] > 0 or incident_counts["Critical"] > 0:
        st.warning("High or critical incident risks require attention.")

    st.dataframe(
        incidents[[
            "Incident ID", "Date", "Time", "Shift", "Location", "Department", 
            "Incident type", "Severity", "Likelihood", "Consequence", "Risk Score", "Risk Level"
        ]],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Equipment Risk
    st.header("Equipment Risk")
    equipment_counts = equipment["Risk Level"].value_counts().reindex(["Low", "Medium", "High", "Critical"], fill_value=0)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Low", equipment_counts["Low"])
    with col2:
        st.metric("Medium", equipment_counts["Medium"])
    with col3:
        st.metric("High", equipment_counts["High"])
    with col4:
        st.metric("Critical", equipment_counts["Critical"])

    if equipment_counts["High"] > 0 or equipment_counts["Critical"] > 0:
        st.warning("High or critical equipment risks require attention.")

    st.dataframe(
        equipment[[
            "Equipment ID", "Equipment type", "Manufacturer", "Temperature", "Vibration", 
            "Brake status", "Tyre status", "Engine status", "Maintenance status", 
            "Likelihood", "Consequence", "Risk Score", "Risk Level"
        ]],
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # Overall Risk 
    st.header("Overall Risk Summary")
    all_risks = pd.concat(
        [workers[["Risk Level"]], incidents[["Risk Level"]], equipment[["Risk Level"]]],
        ignore_index=True
    )

    overall_counts = all_risks["Risk Level"].value_counts().reindex(["Low", "Medium", "High", "Critical"], fill_value=0)
    st.bar_chart(overall_counts)

    if overall_counts["Critical"] > 0:
        st.error("Critical risks are currently present.")
    elif overall_counts["High"] > 0:
        st.warning("High risks are currently present.")
    else:
        st.success("No high or critical risks are currently present.")