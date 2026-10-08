import os
import streamlit as st
import pandas as pd


# ==================================================
# CONFIGURATION
# ==================================================

RISK_LEVELS = ["Low", "Medium", "High", "Critical"]

RISK_BANDS = {
    "Low": (1, 4),
    "Medium": (5, 9),
    "High": (10, 16),
    "Critical": (17, 25)
}


# ==================================================
# LOAD CSV FILES SAFELY
# ==================================================

def load_csv(filename):
    # Check the project root and the data folder.
    possible_paths = [
        filename,
        os.path.join("data", filename)
    ]

    for path in possible_paths:
        if os.path.exists(path):
            try:
                return pd.read_csv(path)
            except Exception as error:
                raise ValueError(
                    f"Could not read {path}: {error}"
                ) from error

    raise FileNotFoundError(
        f"{filename} was not found. "
        "Check whether it is in the project root or data folder."
    )


def load_worker_data():
    return load_csv("workers.csv")


def load_incident_data():
    return load_csv("incidents.csv")


def load_equipment_data():
    return load_csv("equipment.csv")


# ==================================================
# GENERAL HELPER FUNCTIONS
# ==================================================

def get_number(row, column, default=0):
    # Safely convert a value to a number.
    value = pd.to_numeric(
        row.get(column, default),
        errors="coerce"
    )

    if pd.isna(value):
        return default

    return value


def get_text(row, column, default=""):
    # Safely read text from a row.
    value = row.get(column, default)

    if pd.isna(value):
        return default

    return str(value).strip().lower()


def classify_risk(risk_score):
    # Apply the risk classification from the project brief.
    if pd.isna(risk_score):
        return "Not assessed"

    if risk_score < 1 or risk_score > 25:
        return "Not assessed"

    if risk_score <= 4:
        return "Low"

    elif risk_score <= 9:
        return "Medium"

    elif risk_score <= 16:
        return "High"

    return "Critical"


def calculate_risk_score(likelihood, consequence):
    # Both inputs must be between 1 and 5.
    likelihood = max(1, min(5, int(likelihood)))
    consequence = max(1, min(5, int(consequence)))

    return likelihood * consequence


def add_risk_columns(data, likelihood_function, consequence_function):
    # Calculate risk on a copy so the source CSV stays unchanged.
    data = data.copy()

    data["Likelihood"] = data.apply(
        likelihood_function,
        axis=1
    )

    data["Consequence"] = data.apply(
        consequence_function,
        axis=1
    )

    data["Risk Score"] = data.apply(
        lambda row: calculate_risk_score(
            row["Likelihood"],
            row["Consequence"]
        ),
        axis=1
    )

    data["Risk Level"] = data["Risk Score"].apply(
        classify_risk
    )

    return data


def prepare_columns(data, required_columns, optional_columns=None):
    # Report missing essential columns rather than crashing later.
    missing = [
        column for column in required_columns
        if column not in data.columns
    ]

    if missing:
        raise ValueError(
            "Missing required columns: "
            + ", ".join(missing)
        )

    # Add empty optional columns when they are not supplied.
    for column in optional_columns or []:
        if column not in data.columns:
            data[column] = pd.NA

    return data


# ==================================================
# WORKER RISK ASSESSMENT
# ==================================================

def calculate_worker_likelihood(row):
    # Start at the minimum likelihood score.
    score = 1

    ppe = get_number(row, "PPE compliance", default=100)
    fatigue = get_text(row, "Fatigue level")
    near_misses = get_number(row, "Near misses")
    previous_incidents = get_number(row, "Previous incidents")

    # Lower PPE compliance increases likelihood.
    if ppe < 80:
        score += 2
    elif ppe < 95:
        score += 1

    # Fatigue can increase the likelihood of an incident.
    if fatigue == "high":
        score += 2
    elif fatigue == "medium":
        score += 1

    # Previous near misses are warning indicators.
    if near_misses >= 3:
        score += 2
    elif near_misses >= 1:
        score += 1

    # Previous incidents indicate a need for attention.
    if previous_incidents >= 3:
        score += 2
    elif previous_incidents >= 1:
        score += 1

    return max(1, min(5, score))


def calculate_worker_consequence(row):
    # Estimate potential consequence using available worker data.
    score = 1

    previous_incidents = get_number(row, "Previous incidents")
    near_misses = get_number(row, "Near misses")
    fatigue = get_text(row, "Fatigue level")

    if previous_incidents >= 3:
        score += 2
    elif previous_incidents >= 1:
        score += 1

    if fatigue == "high":
        score += 1

    if near_misses >= 3:
        score += 1

    return max(1, min(5, score))


def create_worker_risk_data(workers):
    workers = workers.copy()

    workers = add_risk_columns(
        workers,
        calculate_worker_likelihood,
        calculate_worker_consequence
    )

    return workers


# ==================================================
# INCIDENT RISK ASSESSMENT
# ==================================================

def calculate_incident_likelihood(row):
    # Estimate the likelihood that an unresolved incident
    # could recur or continue to pose a risk.
    score = 1

    status = get_text(row, "Incident status")

    if status in [
        "open",
        "active",
        "under investigation",
        "unresolved"
    ]:
        score += 2

    elif status in ["pending", "in progress"]:
        score += 1

    return max(1, min(5, score))


def calculate_incident_consequence(row):
    # Use incident severity as the starting point.
    severity = get_text(row, "Severity")
    injury = get_text(row, "Injury status")
    lost_time = get_text(row, "Lost-time injury status")

    severity_scores = {
        "critical": 5,
        "severe": 5,
        "high": 4,
        "major": 4,
        "moderate": 3,
        "medium": 3,
        "minor": 2,
        "low": 1
    }

    score = severity_scores.get(severity, 1)

    # Injury and lost-time indicators increase consequence.
    if injury in ["yes", "injury", "injured", "true"]:
        score += 1

    if lost_time in ["yes", "true", "1"]:
        score += 1

    return max(1, min(5, score))


def create_incident_risk_data(incidents):
    incidents = incidents.copy()

    incidents = add_risk_columns(
        incidents,
        calculate_incident_likelihood,
        calculate_incident_consequence
    )

    return incidents


# ==================================================
# EQUIPMENT RISK ASSESSMENT
# ==================================================

def calculate_equipment_likelihood(row):
    # Assess the likelihood of equipment failure or problems.
    score = 1

    temperature = get_number(row, "Temperature")
    vibration = get_number(row, "Vibration")
    downtime = get_number(row, "Downtime")
    maintenance = get_text(row, "Maintenance status")

    # Educational temperature thresholds.
    if temperature > 100:
        score += 3
    elif temperature >= 80:
        score += 2

    # Educational vibration thresholds.
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

    if downtime >= 100:
        score += 2
    elif downtime >= 50:
        score += 1

    return max(1, min(5, score))


def calculate_equipment_consequence(row):
    # Estimate the consequence of equipment failure.
    score = 1

    temperature = get_number(row, "Temperature")
    vibration = get_number(row, "Vibration")

    brake = get_text(row, "Brake status")
    tyre = get_text(row, "Tyre status")
    engine = get_text(row, "Engine status")

    if temperature > 100:
        score += 2
    elif temperature >= 80:
        score += 1

    if vibration > 8:
        score += 2
    elif vibration >= 5:
        score += 1

    # Treat missing component status as unknown, not as a failure.
    acceptable_statuses = [
        "good",
        "normal",
        "ok",
        "operational",
        "working",
        "healthy"
    ]

    if brake and brake not in acceptable_statuses:
        score += 1

    if tyre and tyre not in acceptable_statuses:
        score += 1

    if engine and engine not in acceptable_statuses:
        score += 1

    return max(1, min(5, score))


def create_equipment_risk_data(equipment):
    equipment = equipment.copy()

    equipment = add_risk_columns(
        equipment,
        calculate_equipment_likelihood,
        calculate_equipment_consequence
    )

    return equipment


# ==================================================
# RISK SUMMARY FUNCTIONS
# ==================================================

def get_risk_counts(data):
    # Include every category, even when its count is zero.
    return (
        data["Risk Level"]
        .value_counts()
        .reindex(RISK_LEVELS, fill_value=0)
    )


def show_risk_metrics(data, prefix):
    # Display the number of risks in each category.
    counts = get_risk_counts(data)

    columns = st.columns(4)

    for index, level in enumerate(RISK_LEVELS):
        columns[index].metric(
            level,
            int(counts[level])
        )

    high_count = int(counts["High"])
    critical_count = int(counts["Critical"])

    # Warn the user when high or critical risks exist.
    if critical_count > 0:
        st.error(
            f"{prefix}: {critical_count} critical risk(s) identified. "
            "Immediate review and appropriate action are required."
        )

    if high_count > 0:
        st.warning(
            f"{prefix}: {high_count} high risk(s) identified. "
            "Review and corrective action are required."
        )

    if high_count == 0 and critical_count == 0:
        st.success(
            f"{prefix}: no high or critical risks were identified "
            "by the current scoring rules."
        )


def filter_risk_data(data, key_prefix):
    # Let users choose which risk categories to display.
    selected_levels = st.multiselect(
        "Filter by Risk Level",
        options=RISK_LEVELS,
        default=RISK_LEVELS,
        key=f"{key_prefix}_risk_filter"
    )

    filtered = data[
        data["Risk Level"].isin(selected_levels)
    ].copy()

    return filtered


def show_high_risk_records(data, identifier_columns, title):
    # Display only high and critical records.
    st.subheader(title)

    high_risks = data[
        data["Risk Level"].isin(["High", "Critical"])
    ].copy()

    if high_risks.empty:
        st.success("No high or critical records to display.")
        return

    # Put critical records first, then highest scores.
    high_risks["_Priority"] = high_risks["Risk Level"].map({
        "Critical": 2,
        "High": 1
    })

    high_risks = high_risks.sort_values(
        ["_Priority", "Risk Score"],
        ascending=[False, False]
    )

    display_columns = [
        column for column in identifier_columns
        if column in high_risks.columns
    ]

    display_columns += [
        "Likelihood",
        "Consequence",
        "Risk Score",
        "Risk Level"
    ]

    st.dataframe(
        high_risks[display_columns],
        use_container_width=True,
        hide_index=True
    )


# ==================================================
# RISK ASSESSMENT PAGE
# ==================================================

def render_risk_assessment_page():

    st.title("Risk Assessment")

    st.write(
        "Assess worker safety, safety incidents and equipment "
        "using a basic likelihood and consequence scoring model."
    )

    st.info(
        "**Risk Score = Likelihood × Consequence**\n\n"
        "Both values use a scale from 1 to 5."
    )

    # Show the required classification bands.
    st.subheader("Risk Classification")

    risk_table = pd.DataFrame({
        "Risk Score": ["1–4", "5–9", "10–16", "17–25"],
        "Classification": [
            "Low",
            "Medium",
            "High",
            "Critical"
        ],
        "Required response": [
            "Monitor and maintain controls",
            "Review controls and monitor",
            "Prompt review and corrective action",
            "Urgent review and appropriate action"
        ]
    })

    st.dataframe(
        risk_table,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "This is a basic prototype scoring model. "
        "The likelihood and consequence rules are estimates based "
        "on the available CSV fields. Follow approved mine safety "
        "procedures and site-specific risk criteria."
    )

    st.divider()

    # --------------------------------------------------
    # LOAD AND VALIDATE DATA
    # --------------------------------------------------

    try:
        workers = load_worker_data()
        incidents = load_incident_data()
        equipment = load_equipment_data()

        workers = prepare_columns(
            workers,
            required_columns=[
                "Worker ID",
                "Department",
                "Job role",
                "Shift",
                "PPE compliance",
                "Fatigue level",
                "Near misses",
                "Previous incidents"
            ],
            optional_columns=[]
        )

        incidents = prepare_columns(
            incidents,
            required_columns=[
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
            ],
            optional_columns=[]
        )

        equipment = prepare_columns(
            equipment,
            required_columns=[
                "Equipment ID",
                "Equipment type",
                "Maintenance status"
            ],
            optional_columns=[
                "Manufacturer",
                "Temperature",
                "Vibration",
                "Downtime",
                "Brake status",
                "Tyre status",
                "Engine status"
            ]
        )

    except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
        st.error(f"Risk assessment could not load the data: {error}")
        st.info(
            "Check your CSV filenames, column headings and file locations."
        )
        return

    if workers.empty and incidents.empty and equipment.empty:
        st.warning("All three datasets are empty.")
        return

    # --------------------------------------------------
    # CALCULATE RISKS
    # --------------------------------------------------

    workers = create_worker_risk_data(workers)
    incidents = create_incident_risk_data(incidents)
    equipment = create_equipment_risk_data(equipment)

    # --------------------------------------------------
    # OVERALL SUMMARY
    # --------------------------------------------------

    st.header("Overall Risk Summary")

    all_risks = pd.concat(
        [
            workers[["Risk Score", "Risk Level"]].assign(
                Category="Worker"
            ),
            incidents[["Risk Score", "Risk Level"]].assign(
                Category="Incident"
            ),
            equipment[["Risk Score", "Risk Level"]].assign(
                Category="Equipment"
            )
        ],
        ignore_index=True
    )

    overall_counts = get_risk_counts(all_risks)

    total_high = int(overall_counts["High"])
    total_critical = int(overall_counts["Critical"])

    summary1, summary2, summary3 = st.columns(3)

    summary1.metric("Total Records Assessed", len(all_risks))
    summary2.metric("High Risks", total_high)
    summary3.metric("Critical Risks", total_critical)

    if total_critical > 0:
        st.error(
            f"URGENT ATTENTION: {total_critical} critical risk(s) "
            "were identified across the application."
        )

    elif total_high > 0:
        st.warning(
            f"ATTENTION REQUIRED: {total_high} high risk(s) "
            "were identified across the application."
        )

    else:
        st.success(
            "No high or critical risks were identified by the "
            "current scoring rules."
        )

    st.bar_chart(overall_counts)

    st.subheader("Risk Categories by Data Source")

    category_summary = pd.crosstab(
        all_risks["Category"],
        all_risks["Risk Level"]
    )

    category_summary = category_summary.reindex(
        columns=RISK_LEVELS,
        fill_value=0
    )

    st.dataframe(
        category_summary,
        use_container_width=True
    )

    st.divider()

    # --------------------------------------------------
    # WORKER SAFETY RISK
    # --------------------------------------------------

    st.header("Worker Safety Risk")

    if workers.empty:
        st.info("No worker records are available.")
    else:
        show_risk_metrics(workers, "Worker safety")

        worker_filter = filter_risk_data(
            workers,
            "worker"
        )

        worker_columns = [
            "Worker ID",
            "Department",
            "Job role",
            "Shift",
            "Likelihood",
            "Consequence",
            "Risk Score",
            "Risk Level"
        ]

        st.subheader("Worker Risk Records")

        st.dataframe(
            worker_filter[worker_columns],
            use_container_width=True,
            hide_index=True
        )

        show_high_risk_records(
            workers,
            [
                "Worker ID",
                "Department",
                "Job role",
                "Shift"
            ],
            "Workers Requiring Attention"
        )

    st.divider()

    # --------------------------------------------------
    # INCIDENT RISK
    # --------------------------------------------------

    st.header("Incident Risk")

    if incidents.empty:
        st.info("No incident records are available.")
    else:
        show_risk_metrics(incidents, "Incident safety")

        incident_filter = filter_risk_data(
            incidents,
            "incident"
        )

        incident_columns = [
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

        st.subheader("Incident Risk Records")

        st.dataframe(
            incident_filter[incident_columns],
            use_container_width=True,
            hide_index=True
        )

        show_high_risk_records(
            incidents,
            [
                "Incident ID",
                "Date",
                "Department",
                "Incident type",
                "Severity"
            ],
            "Incidents Requiring Attention"
        )

    st.divider()

    # --------------------------------------------------
    # EQUIPMENT RISK
    # --------------------------------------------------

    st.header("Equipment Risk")

    if equipment.empty:
        st.info("No equipment records are available.")
    else:
        show_risk_metrics(equipment, "Equipment safety")

        equipment_filter = filter_risk_data(
            equipment,
            "equipment"
        )

        equipment_columns = [
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

        st.subheader("Equipment Risk Records")

        st.dataframe(
            equipment_filter[equipment_columns],
            use_container_width=True,
            hide_index=True
        )

        show_high_risk_records(
            equipment,
            [
                "Equipment ID",
                "Equipment type",
                "Manufacturer",
                "Maintenance status"
            ],
            "Equipment Requiring Attention"
        )

    st.divider()

    # --------------------------------------------------
    # RISK SCORING EXPLANATION
    # --------------------------------------------------

    with st.expander("How are risks calculated?"):

        st.write(
            "**Likelihood:** Estimates how likely an incident "
            "or equipment problem may occur, based on the available "
            "worker, incident or equipment information."
        )

        st.write(
            "**Consequence:** Estimates the potential seriousness "
            "of the outcome using the available data."
        )

        st.write(
            "**Risk Score:** Likelihood multiplied by consequence. "
            "The result ranges from 1 to 25."
        )

        st.write(
            "The scoring rules are simple estimates for this "
            "prototype. They should be reviewed against your mine's "
            "approved risk matrix before operational use."
        )
