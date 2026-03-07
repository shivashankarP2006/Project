import streamlit as st
from database import get_tasks, update_status, calculate_hours_left


def team_member_dashboard():

    st.markdown("<h2 style='text-align:center;'>👨‍💻 Team Member Dashboard</h2>", unsafe_allow_html=True)

    # Get logged-in username
    username = st.session_state.username

    # Get all tasks
    tasks = get_tasks()

    # Filter tasks for this member
    member_tasks = tasks[tasks["assigned_to"] == username]

    # ---------------- Deadline Alerts ----------------
    st.subheader("⏰ Deadline Alerts (5 Days)")

    for _, row in member_tasks.iterrows():

        hours_left = calculate_hours_left(row["deadline"])

        if 0 <= hours_left <= 120:
            st.warning(
                f"⚠ {row['client']} deadline in {round(hours_left)} hours"
            )

    st.divider()

    # ---------------- Task List ----------------
    st.subheader("📋 Your Tasks")

    if member_tasks.empty:
        st.info("No tasks assigned to you yet.")
        return

    for _, row in member_tasks.iterrows():

        with st.container():

            st.markdown(
                f"""
                <div style="
                border:1px solid #ddd;
                padding:15px;
                border-radius:10px;
                margin-bottom:10px;
                ">
                <h4>Client: {row['client']}</h4>
                <p><b>Deadline:</b> {row['deadline']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Status Badge
            if row["status"] == "Completed":
                st.success("✅ Status: Completed")

            elif row["status"] == "In Progress":
                st.warning("🔄 Status: In Progress")

            else:
                st.info("🆕 Status: New")

            # Update Status
            new_status = st.selectbox(
                "Update Status",
                ["New", "In Progress", "Completed"],
                key=row["id"]
            )

            if st.button("Update Task Status", key=f"btn{row['id']}"):

                update_status(row["id"], new_status)

                st.success("Status Updated Successfully")

                st.rerun()

            st.divider()