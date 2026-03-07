# Import required libraries
import sqlite3
import pandas as pd
from datetime import datetime

# Database file name
DB_NAME = "startup.db"


# ------------------------------
# Connect to SQLite database
# ------------------------------
def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)


# ------------------------------
# Create tasks table
# ------------------------------
def create_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client TEXT,
            team TEXT,
            assigned_to TEXT,
            status TEXT,
            deadline TEXT
        )
    """)

    conn.commit()
    conn.close()


# ------------------------------
# Add new task
# ------------------------------
def add_task(client, team, assigned_to, status, deadline):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks (client, team, assigned_to, status, deadline)
        VALUES (?, ?, ?, ?, ?)
    """, (client, team, assigned_to, status, deadline))

    conn.commit()
    conn.close()


# ------------------------------
# Get all tasks
# ------------------------------
def get_tasks():

    conn = connect()

    df = pd.read_sql_query("SELECT * FROM tasks", conn)

    conn.close()

    return df


# ------------------------------
# Update task status
# ------------------------------
def update_status(task_id, new_status):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status=? WHERE id=?",
        (new_status, task_id)
    )

    conn.commit()
    conn.close()


# ------------------------------
# Calculate hours left for deadline
# Supports BOTH formats:
# 1) YYYY-MM-DD
# 2) YYYY-MM-DD HH:MM:SS
# ------------------------------
def calculate_hours_left(deadline):

    now = datetime.now()

    try:
        # New format with time
        deadline_dt = datetime.strptime(deadline, "%Y-%m-%d %H:%M:%S")

    except ValueError:
        # Old format without time
        deadline_dt = datetime.strptime(deadline, "%Y-%m-%d")

    remaining = deadline_dt - now

    return remaining.total_seconds() / 3600