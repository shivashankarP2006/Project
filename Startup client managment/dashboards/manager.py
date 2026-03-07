import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from database import get_tasks


def manager_dashboard():

    # -------- Title --------
    st.markdown(
        "<h2 style='text-align:center;'>👨‍💼 Manager Dashboard</h2>",
        unsafe_allow_html=True
    )

    # -------- Get tasks from database --------
    tasks = get_tasks()

    # ---------------- Search Feature ----------------
    search = st.text_input("🔍 Search Client")

    if search:
        tasks = tasks[tasks["client"].str.contains(search, case=False)]

    st.divider()

    # ---------------- Near Deadline Alerts ----------------
    st.subheader("⏰ Tasks Near Deadline")

    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    for _, row in tasks.iterrows():

        try:
            deadline_dt = datetime.strptime(row["deadline"], "%Y-%m-%d %H:%M:%S")
        except:
            deadline_dt = datetime.strptime(row["deadline"], "%Y-%m-%d")

        deadline_date = deadline_dt.date()
        deadline_display = deadline_dt.strftime("%d %b %Y %I:%M %p")

        if deadline_date == today:
            st.error(
                f"🔴 TODAY DEADLINE → Team {row['team']} | "
                f"{row['client']} | {deadline_display}"
            )

        elif deadline_date == tomorrow:
            st.warning(
                f"🟠 TOMORROW DEADLINE → Team {row['team']} | "
                f"{row['client']} | {deadline_display}"
            )

    st.divider()

    # ---------------- Dashboard Data ----------------
    if not tasks.empty:

        # -------- Team Summary --------
        team_summary = tasks.groupby("team").agg(
            total_tasks=("id", "count"),
            new_tasks=("status", lambda x: (x == "New").sum()),
            progress_tasks=("status", lambda x: (x == "In Progress").sum()),
            completed_tasks=("status", lambda x: (x == "Completed").sum())
        ).reset_index()

        def overall_status(row):

            if row["completed_tasks"] == row["total_tasks"]:
                return "Completed"

            elif row["progress_tasks"] > 0:
                return "In Progress"

            else:
                return "New"

        team_summary["overall_status"] = team_summary.apply(
            overall_status,
            axis=1
        )

        st.subheader("📊 Team Summary")

        st.dataframe(
            team_summary[["team", "overall_status", "total_tasks"]]
        )

        st.divider()

        # -------- Task Metrics --------
        new = len(tasks[tasks["status"] == "New"])
        progress = len(tasks[tasks["status"] == "In Progress"])
        completed = len(tasks[tasks["status"] == "Completed"])

        st.subheader("📈 Task Overview")

        col1, col2, col3 = st.columns(3)

        col1.metric("🆕 New Tasks", new)
        col2.metric("🔄 In Progress", progress)
        col3.metric("✅ Completed", completed)

        st.divider()

        # -------- Chart --------
        st.subheader("📊 Task Status Chart")

        chart_data = pd.DataFrame({
            "Status": ["New", "In Progress", "Completed"],
            "Count": [new, progress, completed]
        })

        st.bar_chart(chart_data.set_index("Status"))

    else:
        st.info("No tasks available yet.")

    st.divider()

    # ---------------- Individual Task Status ----------------
    st.subheader("📋 Task Status Details")

    # New Tasks
    st.markdown("### 🆕 New Tasks")

    new_tasks = tasks[tasks["status"] == "New"]

    if not new_tasks.empty:
        st.dataframe(new_tasks[["client", "team", "assigned_to", "deadline"]])
    else:
        st.info("No new tasks.")

    # In Progress Tasks
    st.markdown("### 🔄 In Progress Tasks")

    progress_tasks = tasks[tasks["status"] == "In Progress"]

    if not progress_tasks.empty:
        st.dataframe(progress_tasks[["client", "team", "assigned_to", "deadline"]])
    else:
        st.info("No tasks in progress.")

    # Completed Tasks
    st.markdown("### ✅ Completed Tasks")

    completed_tasks = tasks[tasks["status"] == "Completed"]

    if not completed_tasks.empty:
        st.dataframe(completed_tasks[["client", "team", "assigned_to", "deadline"]])
    else:
        st.info("No completed tasks.")