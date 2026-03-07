import streamlit as st
from datetime import date, datetime
from database import add_task, get_tasks, calculate_hours_left


def team_lead_dashboard():

    st.markdown("<h2 style='text-align:center;'>👨‍💻 Team Lead Dashboard</h2>", unsafe_allow_html=True)
    # ---------------- Assign Task ----------------
    st.subheader("➕ Assign New Task")

    with st.container():

        st.markdown(
            """
            <div style="border:1px solid #ddd;padding:20px;border-radius:12px;background:#f9f9f9">
            </div>
            """,
            unsafe_allow_html=True
        )

        client = st.text_input("Client Name")

        # Team → Members mapping
        team_members = {
            "Team A": ["mem1", "mem2"],
            "Team B": ["mem3", "mem4"],
            "Team C": ["mem5", "mem6"],
            "Team D": ["mem7", "mem8"],
            "Team E": ["mem9", "mem10"]
        }

        col1, col2 = st.columns(2)

        with col1:
            team = st.selectbox("Select Team", list(team_members.keys()))

        with col2:
            assigned_to = st.selectbox(
                "Assign To Member",
                team_members[team]
            )

        status = st.selectbox(
            "Task Status",
            ["New", "In Progress"]
        )

        col3, col4 = st.columns(2)

        with col3:
            deadline_date = st.date_input("Deadline Date", date.today())

        with col4:
            deadline_time = st.time_input("Deadline Time")

        if st.button("Assign Task"):

            deadline = datetime.combine(deadline_date, deadline_time)

            add_task(
                client,
                team,
                assigned_to,
                status,
                deadline.strftime("%Y-%m-%d %H:%M:%S")
            )

            st.success("Task Assigned Successfully")
            st.rerun()

    st.divider()

    # ---------------- Deadline Alerts ----------------
    st.subheader("⏰ Upcoming Deadlines (Next 5 Days)")

    tasks = get_tasks()

    for _, row in tasks.iterrows():

        hours_left = calculate_hours_left(row["deadline"])

        if 0 <= hours_left <= 120:

            st.warning(
                f"⚠ {row['client']} → {row['assigned_to']} "
                f"({round(hours_left)} hours left)"
            )

    st.divider()

    # ---------------- Task Table ----------------
    st.subheader("📋 All Tasks")

    if tasks.empty:
        st.info("No tasks available.")
    else:
        st.dataframe(tasks)