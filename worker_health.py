import streamlit as st
import pandas as pd
import os

WORKER_FILE = "workers.csv"


def load_worker_data():
    if not os.path.exists(WORKER_FILE):
        columns = [
            "Worker ID", "Department", "Job role", "Shift", 
            "PPE compliance", "Safety training status", "Fatigue level", 
            "Safety observations", "Near misses", "Previous incidents"
        ]
        return pd.DataFrame(columns=columns)
    return pd.read_csv(WORKER_FILE)


def save_worker_data(workers):
    os.makedirs(".", exist_ok=True)
    workers.to_csv(WORKER_FILE, index=False)


def add_worker_section(workers):
    st.subheader("Add New Worker")

    with st.form("add_worker_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            worker_id = st.text_input("Worker ID (e.g., WRK-100)")
            department = st.selectbox("Department", ["Mining", "Processing", "Engineering", "Maintenance", "Health & Safety", "Logistics", "Administration"])
            job_role = st.text_input("Job Role (e.g., Miner, Operator)")
            shift = st.selectbox("Shift", ["Day", "Night"])
            ppe_compliance = st.slider("PPE Compliance (%)", 0, 100, 90)

        with col2:
            training_status = st.selectbox("Safety Training Status", ["Current", "Expired", "Pending"])
            fatigue_level = st.selectbox("Fatigue Level", ["Low", "Medium", "High"])
            safety_observations = st.number_input("Safety Observations", min_value=0, step=1, value=0)
            near_misses = st.number_input("Near Misses", min_value=0, step=1, value=0)
            previous_incidents = st.number_input("Previous Incidents", min_value=0, step=1, value=0)

        submitted = st.form_submit_button("Add Worker")

    if submitted:
        worker_id = worker_id.strip()
        if worker_id == "":
            st.error("Worker ID is required.")
            return

        if not workers.empty and worker_id in workers["Worker ID"].astype(str).values:
            st.error(f"Worker ID '{worker_id}' already exists.")
            return

        new_worker = {
            "Worker ID": worker_id,
            "Department": department,
            "Job role": job_role,
            "Shift": shift,
            "PPE compliance": ppe_compliance,
            "Safety training status": training_status,
            "Fatigue level": fatigue_level,
            "Safety observations": safety_observations,
            "Near misses": near_misses,
            "Previous incidents": previous_incidents
        }

        new_row = pd.DataFrame([new_worker])
        updated_workers = pd.concat([workers, new_row], ignore_index=True)
        save_worker_data(updated_workers)

        st.success(f"Worker '{worker_id}' added successfully!")
        st.rerun()


def remove_worker_section(workers):
    st.subheader("Remove Worker Record")

    if workers.empty:
        st.info("No worker records available to remove.")
        return

    worker_ids = sorted(workers["Worker ID"].astype(str).tolist())
    selected_worker_id = st.selectbox("Select Worker ID to Remove", worker_ids)

    # Show details of selected worker
    worker_row = workers[workers["Worker ID"].astype(str) == selected_worker_id]
    st.write("**Selected Worker Details:**")
    st.dataframe(worker_row, use_container_width=True, hide_index=True)

    if st.button("Permanently Remove Worker", type="primary"):
        updated_workers = workers[workers["Worker ID"].astype(str) != selected_worker_id]
        save_worker_data(updated_workers)
        st.success(f"Worker '{selected_worker_id}' has been removed.")
        st.rerun()


def render_worker_health_page():

    st.title("Worker Health & Safety")

    st.write("Monitor worker PPE compliance, training status, fatigue, safety observations and near misses.")

    st.divider()

    # Load worker data
    workers = load_worker_data()

    # Create tabs for viewing dashboard, adding, or removing
    tab_dashboard, tab_add, tab_remove = st.tabs(["Dashboard & Records", "Add Worker", "Remove Worker"])

    with tab_dashboard:
        if workers.empty:
            st.info("No worker records found. Please add a worker using the 'Add Worker' tab.")
            return

        # --------------------------------------------------
        # KEY INDICATORS
        # --------------------------------------------------

        total_workers = len(workers)
        average_ppe = workers["PPE compliance"].mean()
        total_observations = workers["Safety observations"].sum()
        total_near_misses = workers["Near misses"].sum()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Workers", total_workers)

        with col2:
            st.metric("Average PPE Compliance", f"{average_ppe:.1f}%")

        with col3:
            st.metric("Safety Observations", total_observations)

        with col4:
            st.metric("Near Misses", total_near_misses)

        st.divider()

        # --------------------------------------------------
        # FILTERS
        # --------------------------------------------------

        st.subheader("Worker Filters")

        col1, col2, col3 = st.columns(3)

        with col1:
            departments = ["All"] + sorted(workers["Department"].dropna().astype(str).unique().tolist())
            selected_department = st.selectbox("Department", departments)

        with col2:
            shifts = ["All"] + sorted(workers["Shift"].dropna().astype(str).unique().tolist())
            selected_shift = st.selectbox("Shift", shifts)

        with col3:
            fatigue_levels = ["All"] + sorted(workers["Fatigue level"].dropna().astype(str).unique().tolist())
            selected_fatigue = st.selectbox("Fatigue Level", fatigue_levels)

        # --------------------------------------------------
        # APPLY FILTERS
        # --------------------------------------------------

        filtered_workers = workers.copy()

        if selected_department != "All":
            filtered_workers = filtered_workers[
                filtered_workers["Department"].astype(str) == selected_department
            ]

        if selected_shift != "All":
            filtered_workers = filtered_workers[
                filtered_workers["Shift"].astype(str) == selected_shift
            ]

        if selected_fatigue != "All":
            filtered_workers = filtered_workers[
                filtered_workers["Fatigue level"].astype(str) == selected_fatigue
            ]

        st.divider()

        # --------------------------------------------------
        # PPE COMPLIANCE
        # --------------------------------------------------

        st.subheader("PPE Compliance")
        filtered_ppe = filtered_workers["PPE compliance"].mean() if not filtered_workers.empty else 0.0
        st.metric("Filtered Average PPE Compliance", f"{filtered_ppe:.1f}%")

        # --------------------------------------------------
        # TRAINING STATUS
        # --------------------------------------------------

        st.subheader("Safety Training Status")
        if not filtered_workers.empty:
            training_counts = filtered_workers["Safety training status"].value_counts()
            st.bar_chart(training_counts)

        # --------------------------------------------------
        # FATIGUE
        # --------------------------------------------------

        st.subheader("Fatigue Levels")
        if not filtered_workers.empty:
            fatigue_counts = filtered_workers["Fatigue level"].value_counts()
            st.bar_chart(fatigue_counts)

        # --------------------------------------------------
        # SAFETY OBSERVATIONS
        # --------------------------------------------------

        st.subheader("Safety Observations")
        if not filtered_workers.empty:
            observation_data = (
                filtered_workers
                .groupby("Department")["Safety observations"]
                .sum()
                .sort_values(ascending=False)
            )
            st.bar_chart(observation_data)

        # --------------------------------------------------
        # NEAR MISSES
        # --------------------------------------------------

        st.subheader("Near Misses")
        if not filtered_workers.empty:
            near_miss_data = (
                filtered_workers
                .groupby("Department")["Near misses"]
                .sum()
                .sort_values(ascending=False)
            )
            st.bar_chart(near_miss_data)

        # --------------------------------------------------
        # WORKER DATA
        # --------------------------------------------------

        st.subheader("Worker Records")
        st.dataframe(
            filtered_workers,
            use_container_width=True,
            hide_index=True
        )

    with tab_add:
        add_worker_section(workers)

    with tab_remove:
        remove_worker_section(workers)
