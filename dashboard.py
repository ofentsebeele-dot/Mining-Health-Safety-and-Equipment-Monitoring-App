
# ============================================================
# KHWEZI MINING MONITORING SYSTEM
# Dashboard: Worker Safety, Incidents and Equipment
# ============================================================

import os
import base64
from datetime import datetime

import pandas as pd
import streamlit as st

try:
    import plotly.express as px
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False


# ============================================================
# 1. LOAD CSV FILES
# ============================================================

def find_csv_path(filename):
    possible_paths = [
        filename,
        os.path.join("data", filename)
    ]

    for path in possible_paths:
        if os.path.isfile(path):
            return path

    return None


def load_csv(filename):
    path = find_csv_path(filename)

    if path is None:
        raise FileNotFoundError(
            f"Cannot find {filename}. "
            "Place it in the project folder or the data folder."
        )

    return pd.read_csv(path)


def load_worker_data():
    return load_csv("workers.csv")


def load_incident_data():
    return load_csv("incidents.csv")


def load_equipment_data():
    return load_csv("equipment.csv")


# ============================================================
# 2. HELPER FUNCTIONS
# ============================================================

def numeric_column(data, column_name):
    if column_name not in data.columns:
        return pd.Series(float("nan"), index=data.index)

    values = data[column_name].astype(str).str.strip()
    values = values.str.replace("%", "", regex=False)

    return pd.to_numeric(values, errors="coerce")


def category_column(data, column_name):
    if column_name not in data.columns:
        return pd.Series("Unknown
