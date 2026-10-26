
import streamlit as st


def apply_dark_theme():

    st.markdown(
        """
        <style>

        /* Main page background */
        .stApp {
            background-color: #000000 !important;
            color: #F0F0F0 !important;
        }

        /* Main content area */
        [data-testid="stMain"],
        [data-testid="stMainBlockContainer"] {
            background-color: #000000 !important;
            color: #F0F0F0 !important;
        }

        /* All headings */
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }

        /* Paragraphs, labels and normal text */
        p, label, li,
        [data-testid="stMarkdownContainer"],
        [data-testid="stCaptionContainer"] {
            color: #F0F0F0 !important;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #101010 !important;
        }

        [data-testid="stSidebar"] * {
            color: #F0F0F0 !important;
        }

        /* Text input fields */
        .stTextInput input,
        .stNumberInput input,
        .stTextArea textarea {
            background-color: #181818 !important;
            color: #FFFFFF !important;
            border: 1px solid #666666 !important;
        }

        /* Dropdowns and select boxes */
        [data-baseweb="select"] > div {
            background-color: #181818 !important;
            color: #FFFFFF !important;
            border-color: #666666 !important;
        }

        /* Buttons */
        .stButton button {
            background-color: #222222 !important;
            color: #FFFFFF !important;
            border: 1px solid #777777 !important;
            border-radius: 6px !important;
        }

        .stButton button:hover {
            background-color: #383838 !important;
            border-color: #FFFFFF !important;
        }

        /* Tables and dataframes */
        [data-testid="stDataFrame"],
        [data-testid="stTable"] {
            color: #FFFFFF !important;
        }

        /* Checkboxes and radio buttons */
        [data-testid="stCheckbox"],
        [data-testid="stRadio"] {
            color: #F0F0F0 !important;
        }

        /* Metrics */
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"],
        [data-testid="stMetricDelta"] {
            color: #FFFFFF !important;
        }

        /* Alerts */
        [data-testid="stAlert"] {
            color: #FFFFFF !important;
        }

        /* Horizontal lines */
        hr {
            border-color: #555555 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
