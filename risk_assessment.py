import streamlit as st
import pandas as pd
import os
from datetime import datetime

# File locations
MANAGEMENT_FILE = "risk_management.csv"

# Risk assessment follows the brief:
# Risk Score = Likelihood × Consequence
# Both values must be between 1 and 5.


# Load CSV files

def load_data(filename):
    """Load a CSV from the project folder or the data folder."""

    possible_paths = [
        filename,
        os.path.join("data", filename)]

    for path in possible_paths:
        if os.path.exists(path):
            return pd.read_csv(path)

    raise FileNotFoundError(
        f"{filename} could not be found in the project folder or data folder.")


def load_risk_management():
    """Load saved risk assessments, statuses, notes and removed risks."""

    columns = [
        "Risk Type",
        "Record ID",
        "Status",
        "Notes",
        "Removed",
        "Updated At"]

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
                "A new one will be created when you save a change.")

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
        "Notes", "Removed", "Updated At"]

    if management.empty:
        management = pd.DataFrame(columns=columns)

    for column in columns:
        if column not in management.columns:
            management[column] = ""

    matches = (
        (management["Risk Type"].astype(str) == risk_type)
        & (management["Record ID"].astype(str) == record_id))

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
        "%Y-%m-%d %H:%M:%S")

    return management

# Risk Classification

def classify_risk(risk_score):
    """Classify a risk score using the project's specified ranges."""

    if risk_score <= 4:
        return "Low"
    elif risk_score <= 9:
        return "Medium"
    elif risk_score <= 16:
        return "High"

    return "Critical"


def calculate_risk_score(likelihood, consequence):
    """Calculate risk using likelihood multiplied by consequence."""

    likelihood = max(1, min(5, int(likelihood)))
    consequence = max(1, min(5, int(consequence)))

    score = likelihood * consequence

    return score, classify_risk(score)

# Helper Functions

def get_value(row, column, default=""):
    """Safely get a value from a CSV row."""

    if column not in row.index or pd.isna(row[column]):
        return default

    return str(row[column]).strip()


def number_value(value):
    """Convert a value to a number where possible."""

    try:
        text = str(value).replace("%", "").strip()
        return float(text)
    except (ValueError, TypeError):
        return None


def make_record_id(row, id_column, row_number):
    """Use the existing ID, or create a fallback ID for the record."""

    record_id = get_value(row, id_column)

    if record_id:
        return record_id

    return str(row_number + 1)


def add_risk(
    risks,
    risk_type,
    record_id,
    description,
    likelihood,
    consequence
):
    """Add a risk to the list with its calculated score and level."""

    score, level = calculate_risk_score(
        likelihood,
        consequence)

    risks.append({
        "Risk Type": risk_type,
        "Record ID": str(record_id),
        "Risk Description": description,
        "Likelihood": likelihood,
        "Consequence": consequence,
        "Risk Score": score,
        "Risk Level": level})


# Identfy woker Safety Risk

def identify_worker_risks(risks):
    """Identify possible safety risks from worker records."""

    try:
        workers = load_data("workers.csv")
    except FileNotFoundError:
        st.warning("workers.csv was not found. Worker risks were skipped.")
        return

    for row_number, row in workers.iterrows():

        worker_id = make_record_id(
            row, "Worker ID", row_number)

        department = get_value(row, "Department", "Unknown department")
        issues = []
        likelihood = 1
        consequence = 3

        # Check fatigue.
        fatigue = get_value(row, "Fatigue level").lower()

        if any(word in fatigue for word in ["high", "severe", "critical"]):
            issues.append("High fatigue level")
            likelihood = max(likelihood, 4)
            consequence = max(consequence, 4)

        elif fatigue in ["medium", "moderate"]:
            issues.append("Moderate fatigue level")
            likelihood = max(likelihood, 3)

        # Check PPE compliance.
        ppe = get_value(row, "PPE compliance").lower()
        ppe_number = number_value(ppe)

        if any(word in ppe for word in ["non-compliant", "noncompliant", "no", "failed"]):
            issues.append("PPE compliance concern")
            likelihood = max(likelihood, 4)
            consequence = max(consequence, 4)

        elif ppe_number is not None and ppe_number < 80:
            issues.append("Low PPE compliance")
            likelihood = max(likelihood, 4)
            consequence = max(consequence, 4)

        # Check safety training.
        training = get_value(row, "Safety training status").lower()

        if any(word in training for word in ["expired", "overdue", "incomplete", "not trained"]):
            issues.append("Safety training requires attention")
            likelihood = max(likelihood, 3)
            consequence = max(consequence, 4)

        # Check near misses.
        near_misses = number_value(get_value(row, "Near misses", "0"))

        if near_misses is not None and near_misses > 0:
            issues.append(f"{int(near_misses)} recorded near miss(es)")
            likelihood = max(likelihood, 3)

            if near_misses >= 3:
                likelihood = max(likelihood, 4)

        # Check previous incidents.
        previous_incidents = number_value(
            get_value(row, "Previous incidents", "0"))

        if previous_incidents is not None and previous_incidents > 0:
            issues.append("Previous incidents recorded")
            likelihood = max(likelihood, 3)

            if previous_incidents >= 3:
                likelihood = max(likelihood, 4)

        # Only add workers where at least one concern was identified.
        if issues:
            description = (
                f"Worker in {department}: " + "; ".join(issues))

            add_risk(
                risks,
                "Worker",
                worker_id,
                description,
                likelihood,
                consequence)


# Identify Incident risks

def identify_incident_risks(risks):
    """Identify incidents that need safety follow-up."""

    try:
        incidents = load_data("incidents.csv")
    except FileNotFoundError:
        st.warning("incidents.csv was not found. Incident risks were skipped.")
        return

    for row_number, row in incidents.iterrows():

        incident_id = make_record_id(
            row, "Incident ID", row_number)

        severity = get_value(row, "Severity").lower()
        incident_type = get_value(row, "Incident type", "Unspecified incident")
        department = get_value(row, "Department", "Unknown department")
        incident_status = get_value(row, "Incident status").lower()

        issues = []
        likelihood = 3
        consequence = 3

        # Severity values influence the initial consequence estimate.
        if any(word in severity for word in ["critical", "fatal"]):
            consequence = 5
            likelihood = 4
            issues.append(f"Critical severity: {severity}")

        elif any(word in severity for word in ["serious", "major", "high"]):
            consequence = 4
            likelihood = 3
            issues.append(f"Serious severity: {severity}")

        elif any(word in severity for word in ["moderate", "medium"]):
            consequence = 3
            likelihood = 2
            issues.append(f"Moderate severity: {severity}")

        elif any(word in severity for word in ["minor", "low"]):
            consequence = 2
            likelihood = 2
            issues.append(f"Minor severity: {severity}")

        else:
            # An incident is still recorded for assessment when severity
            # is blank or uses a different label.
            issues.append("Incident requires review")

        if any(word in incident_status for word in ["open", "pending", "investigation"]):
            issues.append("Incident is still open")
            likelihood = max(likelihood, 3)

        description = (
            f"{incident_type} in {department}: "
            + "; ".join(issues))

        add_risk(
            risks,
            "Incident",
            incident_id,
            description,
            likelihood,
            consequence)


# Identify Equipment Risks

def identify_equipment_risks(risks):
    """Identify possible equipment risks using available sensor data."""

    try:
        equipment = load_data("equipment.csv")
    except FileNotFoundError:
        st.warning("equipment.csv was not found. Equipment risks were skipped.")
        return

    for row_number, row in equipment.iterrows():

        equipment_id = make_record_id(
            row, "Equipment ID", row_number)

        equipment_type = get_value(
            row, "Equipment type", "Unknown equipment")

        issues = []
        likelihood = 1
        consequence = 3

        # Temperature thresholds from the project brief.
        temperature = number_value(get_value(row, "Temperature"))

        if temperature is not None and temperature > 100:
            issues.append(f"Critical temperature: {temperature:g} °C")
            likelihood = max(likelihood, 5)
            consequence = max(consequence, 5)

        elif temperature is not None and temperature >= 80:
            issues.append(f"High temperature: {temperature:g} °C")
            likelihood = max(likelihood, 3)
            consequence = max(consequence, 4)

        # Vibration thresholds from the project brief.
        vibration = number_value(get_value(row, "Vibration"))

        if vibration is not None and vibration > 8:
            issues.append(f"Critical vibration: {vibration:g} mm/s")
            likelihood = max(likelihood, 5)
            consequence = max(consequence, 5)

        elif vibration is not None and vibration >= 5:
            issues.append(f"High vibration: {vibration:g} mm/s")
            likelihood = max(likelihood, 3)
            consequence = max(consequence, 4)

        # Check equipment condition fields.
        for column in ["Brake status", "Tyre status", "Engine status"]:
            condition = get_value(row, column).lower()

            if any(word in condition for word in [
                "fault", "failed", "critical", "damaged", "unsafe"
            ]):
                issues.append(f"{column}: {condition}")
                likelihood = max(likelihood, 4)
                consequence = max(consequence, 5)

        # Check maintenance status.
        maintenance = get_value(row, "Maintenance status").lower()

        if any(word in maintenance for word in ["overdue", "urgent", "overdue maintenance"]):
            issues.append("Maintenance overdue")
            likelihood = max(likelihood, 4)
            consequence = max(consequence, 4)

        elif "under maintenance" in maintenance:
            issues.append("Equipment under maintenance")
            likelihood = max(likelihood, 2)

        # Check downtime.
        downtime = number_value(get_value(row, "Downtime"))

        if downtime is not None and downtime >= 24:
            issues.append(f"High downtime: {downtime:g} hours")
            likelihood = max(likelihood, 3)
            consequence = max(consequence, 3)

        # Check availability if the column contains numeric percentages.
        availability = number_value(get_value(row, "Availability"))

        if availability is not None and availability < 70:
            issues.append(f"Low availability: {availability:g}%")
            likelihood = max(likelihood, 4)
            consequence = max(consequence, 3)

        if issues:
            description = (
                f"{equipment_type} ({equipment_id}): "
                + "; ".join(issues)
            )

            add_risk(
                risks,
                "Equipment",
                equipment_id,
                description,
                likelihood,
                consequence)

# Build risk list

def identify_risks():
    """Collect risks from worker, incident and equipment CSV files."""

    risks = []

    identify_worker_risks(risks)
    identify_incident_risks(risks)
    identify_equipment_risks(risks)

    columns = [
        "Risk Type",
        "Record ID",
        "Risk Description",
        "Likelihood",
        "Consequence",
        "Risk Score",
        "Risk Level"]

    return pd.DataFrame(risks, columns=columns)


def apply_saved_information(risks, management):
    """Add saved assessment details to each currently identified risk."""

    risks = risks.copy()

    risks["Status"] = "Open"
    risks["Notes"] = ""
    risks["Removed"] = "False"
    risks["Updated At"] = ""

    for index, risk in risks.iterrows():
        matches = management[
            (management["Risk Type"].astype(str) == str(risk["Risk Type"]))
            & (management["Record ID"].astype(str) == str(risk["Record ID"]))]

        if not matches.empty:
            saved = matches.iloc[-1]

            risks.loc[index, "Status"] = saved.get("Status", "Open") or "Open"
            risks.loc[index, "Notes"] = saved.get("Notes", "")
            risks.loc[index, "Removed"] = saved.get("Removed", "False") or "False"
            risks.loc[index, "Updated At"] = saved.get("Updated At", "")

    return risks


# Risk Assessment page

def render_risk_assessment_page():
    """Main page called by app.py."""

    st.title("Risk Assessment")

    st.write(
        "Identify possible worker safety, incident and equipment risks. "
        "Review each risk, update its status, add assessment notes, "
        "or remove it from the active list."
    )

    # Load the saved management information and identify current risks.
    management = load_risk_management()
    risks = identify_risks()
    risks = apply_saved_information(risks, management)

    if risks.empty:
        st.info(
            "No risks were identified from the available data. "
            "Check that your CSV files contain the expected columns and records.")
        return

    # Separate active and removed risks.
    removed_mask = risks["Removed"].astype(str).str.lower().isin(
        ["true", "1", "yes"] )

    active_risks = risks[~removed_mask].copy()
    removed_risks = risks[removed_mask].copy()

    # Summary counts.
    st.subheader("Risk Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Active Risks", len(active_risks))
    col2.metric(
        "High Risks",
        int((active_risks["Risk Level"] == "High").sum()))
    col3.metric(
        "Critical Risks",
        int((active_risks["Risk Level"] == "Critical").sum()))
    col4.metric("Removed Risks", len(removed_risks))

    # Show high and critical warnings.
    serious_risks = active_risks[
        active_risks["Risk Level"].isin(["High", "Critical"]) ]

    if not serious_risks.empty:
        st.warning(
            f"{len(serious_risks)} active risk(s) are classified as High "
            "or Critical and should be reviewed promptly.")

    # Display active risks.
    st.subheader("Identified Risks")

    if active_risks.empty:
        st.info("There are no active risks. You can restore removed risks below.")
    else:
        display_columns = [
            "Risk Type",
            "Record ID",
            "Risk Description",
            "Likelihood",
            "Consequence",
            "Risk Score",
            "Risk Level",
            "Status"]

        # Allow the user to filter the displayed risks.
        selected_type = st.selectbox(
            "Filter by risk type",
            ["All"] + sorted(active_risks["Risk Type"].unique().tolist()) )

        filtered_risks = active_risks.copy()

        if selected_type != "All":
            filtered_risks = filtered_risks[
                filtered_risks["Risk Type"] == selected_type]

        st.dataframe(
            filtered_risks[display_columns],
            use_container_width=True,
            hide_index=True )

    # Assess, Update or remove risk

    st.subheader("Assess or Manage a Risk")

    if not active_risks.empty:

        # Create labels that help the user select the correct risk.
        risk_options = {}

        for index, risk in active_risks.iterrows():
            label = (
                f"{risk['Risk Type']} | ID: {risk['Record ID']} | "
                f"{risk['Risk Level']} | Score: {risk['Risk Score']}" )

            # Include the row index to avoid duplicate option labels.
            risk_options[f"{label} | Item {index}"] = index

        selected_label = st.selectbox(
            "Select a risk to assess",
            list(risk_options.keys()) )

        selected_index = risk_options[selected_label]
        selected_risk = active_risks.loc[selected_index]

        st.write("**Risk description:**", selected_risk["Risk Description"])
        st.write(
            f"**Risk score:** {selected_risk['Likelihood']} × "
            f"{selected_risk['Consequence']} = {selected_risk['Risk Score']}")
        st.write("**Risk level:**", selected_risk["Risk Level"])

        status_options = [
            "Open",
            "Under review",
            "Controls applied",
            "Resolved",
            "Dismissed" ]

        current_status = selected_risk["Status"]

        if current_status not in status_options:
            current_status = "Open"

        selected_status = st.selectbox(
            "Assessment status",
            status_options,
            index=status_options.index(current_status))

        selected_notes = st.text_area(
            "Assessment notes or control measures",
            value=str(selected_risk["Notes"]),
            placeholder="Record findings, actions taken or control measures.")

        col_save, col_remove = st.columns(2)

        with col_save:
            if st.button("Save Assessment", use_container_width=True):
                management = update_risk_record(
                    management,
                    selected_risk["Risk Type"],
                    selected_risk["Record ID"],
                    status=selected_status,
                    notes=selected_notes,
                    removed=False )

                save_risk_management(management)
                st.success("Risk assessment saved.")
                st.rerun()

        with col_remove:
            if st.button(
                "Remove from Active Risks",
                use_container_width=True
            ):
                management = update_risk_record(
                    management,
                    selected_risk["Risk Type"],
                    selected_risk["Record ID"],
                    removed=True)

                save_risk_management(management)
                st.success(
                    "Risk removed from the active list. "
                    "The original source CSV data has not been deleted."
                )
                st.rerun()

    # Restore removed risk

    st.subheader("Removed Risks")

    if removed_risks.empty:
        st.info("There are no removed risks to restore.")
    else:
        st.dataframe(
            removed_risks[
                [
                    "Risk Type",
                    "Record ID",
                    "Risk Description",
                    "Risk Score",
                    "Risk Level",
                    "Status"]],
            use_container_width=True,
            hide_index=True)

        restore_options = {}

        for index, risk in removed_risks.iterrows():
            label = (
                f"{risk['Risk Type']} | ID: {risk['Record ID']} | "
                f"{risk['Risk Level']} | Item {index}"
            )
            restore_options[label] = index

        restore_label = st.selectbox(
            "Select a risk to restore",
            list(restore_options.keys()))

        restore_index = restore_options[restore_label]
        restore_risk = removed_risks.loc[restore_index]

        if st.button("Restore Risk"):
            management = update_risk_record(
                management,
                restore_risk["Risk Type"],
                restore_risk["Record ID"],
                removed=False)

            save_risk_management(management)
            st.success("Risk restored to the active list.")
            st.rerun()
