import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --------------------------------------------------
# FILE LOCATIONS
# --------------------------------------------------

MANAGEMENT_FILE = "risk_management.csv"


def load_data(filename):
    """Load a CSV from the project folder or the data folder."""
    if os.path.exists(filename):
        return pd.read_csv(filename)

    data_path = os.path.join("data", filename)
    if os.path.exists(data_path):
        return pd.read_csv(data_path)

    raise FileNotFoundError(f"{filename} could not be found in the project folder or data folder.")


def load_risk_management():
    """Load saved assessments and removed-risk records."""
    columns = [
        "Risk Type", "Record ID", "Status", "Notes",
        "Removed", "Updated At"
    ]

    if os.path.exists(MANAGEMENT_FILE):
        try:
            saved = pd.read_csv(MANAGEMENT_FILE, dtype=str).fillna("")
            for column in columns:
                if column not in saved.columns:
                    saved[column] = ""
            return saved[columns]
        except (pd.errors.ParserError, OSError):
            st.warning("The saved risk-management file could not be read. A new one will be created.")
    return pd.DataFrame(columns=columns)


def save_risk_management(management):
    """Save assessments separately from the original worker/incident/equipment data."""
    management.to_csv(MANAGEMENT_FILE, index=False)


def update_risk_record(management, risk_type, record_id, status=None, notes=None, removed=None):
    """Add or update one risk-management record without duplicating it."""
    risk_type = str(risk_type)
    record_id = str(record_id)

    if management.empty:
        management = pd.DataFrame(columns=[
            "Risk Type", "Record ID", "Status", "Notes", "Removed", "Updated At"
        ])

    matches = (
        (management["Risk Type"].astype(str) == risk_type)
        & (management["Record ID"].astype(str) == record_id)
    )

    if matches.any():
        index = management.index[matches][0]
    else:
        index = len(management)
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

    management.loc[index, "Updated At"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
