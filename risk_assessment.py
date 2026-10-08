import streamlit as st
import pandas as pd
import os


# ----------------------------------------
# LOAD DATA
# ----------------------------------------

def load_data(filename):

    # Check the main folder and the data folder
    if os.path.exists(filename):
        return pd.read_csv(filename)

    data_path = os.path.join("data", filename)

    if os.path.exists(data_path):
        return pd.read_csv(data_path)

    raise FileNotFoundError(
        f"{filename} could not be found."
    )


# ----------------------------------------
# CLASSIFY RISK
# ----------------------------------------

def classify_risk(risk_score):

    if risk_score <= 4:
        return "Low"

    elif risk_score <= 9:
        return "Medium"

    elif risk_score <= 16:
        return "High"

    return "Critical"


# ----------------------------------------
# WORKER RISK
# ----------------------------------------

def worker_likelihood(row):

    score = 1

    ppe = pd.to_numeric(
        row["PPE compliance"], errors="coerce"
    )

    fatigue = str(row["Fatigue level"]).lower()

    near_misses = pd.to_numeric(
        row["Near misses"], errors="coerce"
    )

    previous_incidents = pd.to_numeric(
        row["Previous incidents"], errors="coerce"
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

    return min(max(score, 1), 5)


def worker_consequence(row):

    score = 1

    previous_incidents = pd.to_numeric(
        row["Previous incidents"], errors="coerce"
    )

    near_misses = pd.to_numeric(
        row["Near misses"], errors="coerce"
    )

    fatigue = str(row["Fatigue level"]).lower()

    if pd.notna(previous_incidents):
        if previous_incidents >= 3:
            score += 2
        elif previous_incidents >= 1:
            score += 1

    if fatigue == "high":
        score += 1

    if pd.notna(near_misses) and near_misses >= 3:
        score += 1

    return min(max(score, 1), 5)


# ----------------------------------------
# INCIDENT RISK
# ----------------------------------------

def incident_likelihood(row):

    score = 1

    status = str(row["Incident status"]).lower()

    if status in [
        "open",
        "active",
        "under investigation"
    ]:
        score += 2

    elif status == "pending":
        score += 1

    return min(max(score, 1), 5)


def incident_consequence(row):

    severity = str(row["Severity"]).lower()

    scores = {
        "critical": 5,
        "high": 4,
        "moderate": 3,
        "medium": 3,
        "minor": 2,
        "low": 1
    }

    score = scores.get(severity, 1)

    injury = str(row["Injury status"]).lower()
    lost_time = str(row["Lost-time injury status"]).lower()

    if injury in ["yes", "injury", "injured", "true"]:
        score += 1

    if lost_time in ["yes", "true", "1"]:
        score += 1

    return min(max(score, 1), 5)


# ----------------------------------------
# EQUIPMENT RISK
# ----------------------------------------

def equipment_likelihood(row):

    score = 1

    temperature = pd.to_numeric(
        row["Temperature"], errors="coerce"
    )

    vibration = pd.to_numeric(
        row["Vibration"], errors="coerce"
    )

    downtime = pd.to_numeric(
        row["Downtime"], errors="coerce"
    )

    maintenance = str(row["Maintenance status"]).lower()

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
    elif maintenance in [
        "under maintenance",
        "maintenance required",
        "due"
    ]:
        score += 1

    if pd.notna(downtime):
        if downtime >= 100:
            score += 2
        elif downtime >= 50:
            score += 1

    return min(max(score, 1), 5)


def equipment_consequence(row):

    score = 1

    temperature = pd.to_numeric(
        row["Temperature"], errors="coerce"
    )

    vibration = pd.to_numeric(
        row["Vibration"], errors="coerce"
    )

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

    for column in [
        "Brake status",
        "Tyre status",
        "Engine status"
    ]:

        value = str(row[column]).strip().lower()

        if value not in [
            "good",
            "normal",
            "ok",
            "operational",
            "working",
            "nan",
            "<na>",
            ""
        ]:
            score += 1

    return min(max(score, 1), 5)


# ----------------------------------------
# CALCULATE RISK
# ----------------------------------------

def calculate_risk(data, likelihood_function, consequence_function):

    data = data.copy()

    data["Likelihood"] = data.apply(
        likelihood_function, axis=1
    )

    data["Consequence"] = data.apply(
        consequence_function, axis=1
    )

    data["Risk Score"] = (
        data["Likelihood"] * data["Consequence"]
    )

    data["Risk Level"] = data["Risk Score"].apply(
        classify_risk
    )

    return data


# ----------------------------------------
# DISPLAY RISK RESULTS
# ----------------------------------------

def display_risks(data, title, columns):

    st.subheader(title)

    if data.empty:
        st.info("No records available.")
        return

    # Count the number of risks in each category
    counts = data["Risk Level"].value_counts()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Low", int(counts.get("Low", 0)))
    col2.metric("Medium", int(counts.get("Medium", 0)))
    col3.metric("High", int(counts.get("High", 0)))
    col4.metric("Critical", int(counts.get("Critical", 0)))

    # Warn users about high and critical risks
    high_risks = data[
        data["Risk Level"] == "High"
    ]

    critical_risks = data[
        data["Risk Level"] == "Critical"
    ]

    if not critical_risks.empty:
        st.error(
            f"Critical risk identified: "
            f"{len(critical_risks)} record(s) require urgent review."
        )

    if not high_risks.empty:
        st.warning(
            f"High risk identified: "
            f"{len(high_risks)} record(s) require attention."
        )

    # Show all requested records
    available_columns = [
        column for column in columns
        if column in data.columns
    ]

    st.dataframe(
        data[available_columns],
        use_container_width=True,
        hide_index=True
    )


# ----------------------------------------
# RISK ASSESSMENT PAGE
# ----------------------------------------

def render_risk_assessment_page():

    st.title("Risk Assessment")

    st.write(
        "Risk Score = Likelihood × Consequence"
    )

    st.info(
        "Low: 1–4 | Medium: 5–9 | "
        "High: 10–16 | Critical: 17–25"
    )

    try:

        workers = load_data("workers.csv")
        incidents = load_data("incidents.csv")
        equipment = load_data("equipment.csv")

        # Check that the required worker columns exist
        worker_columns = [
            "Worker ID",
            "Department",
            "Job role",
            "Shift",
            "PPE compliance",
            "Fatigue level",
            "Near misses",
            "Previous incidents"
        ]

        # Check that the required incident columns exist
        incident_columns = [
            "Incident ID",
            "Date",
            "Time",
            "Shift",
            "Location",
            "Department",
            "Incident type",
            "Severity",
            "Injury status",
            "Lost-time injury status",
            "Incident status"
        ]

        # Check that the required equipment columns exist
        equipment_columns = [
            "Equipment ID",
            "Equipment type",
            "Manufacturer",
            "Temperature",
            "Vibration",
            "Downtime",
            "Brake status",
            "Tyre status",
            "Engine status",
            "Maintenance status"
        ]

        for column in worker_columns:
            if column not in workers.columns:
                st.error(f"Missing workers.csv column: {column}")
                return

        for column in incident_columns:
            if column not in incidents.columns:
                st.error(f"Missing incidents.csv column: {column}")
                return

        for column in equipment_columns:
            if column not in equipment.columns:
                st.error(f"Missing equipment.csv column: {column}")
                return

    except (FileNotFoundError, pd.errors.ParserError) as error:

        st.error(f"Could not load risk assessment data: {error}")
        return

    # Calculate risk for each dataset
    workers = calculate_risk(
        workers,
        worker_likelihood,
        worker_consequence
    )

    incidents = calculate_risk(
        incidents,
        incident_likelihood,
        incident_consequence
    )

    equipment = calculate_risk(
        equipment,
        equipment_likelihood,
        equipment_consequence
    )

    # Display worker risks
    display_risks(
        workers,
        "Worker Safety Risk",
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
    )

    st.divider()

    # Display incident risks
    display_risks(
        incidents,
        "Incident Risk",
        [
            "Incident ID",
            "Date",
            "Department",
            "Incident type",
            "Severity",
            "Likelihood",
            "Consequence",
            "Risk Score",
            "Risk Level"
        ]
    )

    st.divider()

    # Display equipment risks
    display_risks(
        equipment,
        "Equipment Risk",
        [
            "Equipment ID",
            "Equipment type",
            "Manufacturer",
            "Temperature",
            "Vibration",
            "Maintenance status",
            "Likelihood",
            "Consequence",
            "Risk Score",
            "Risk Level"
        ]
    )
