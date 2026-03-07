import sqlite3
import random
from datetime import datetime, timedelta

# Connect database
conn = sqlite3.connect("startup.db")
cursor = conn.cursor()

# Create table if not exists
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

clients = [
    "Amazon","Google","Meta","Netflix","Tesla",
    "Microsoft","Adobe","IBM","Oracle","Samsung",
    "Sony","Intel","Uber","Spotify","Airbnb",
    "Dropbox","PayPal","Zoom","Nvidia","OpenAI"
]

teams = {
    "Team A": ["mem1", "mem2"],
    "Team B": ["mem3", "mem4"],
    "Team C": ["mem5", "mem6"],
    "Team D": ["mem7", "mem8"],
    "Team E": ["mem9", "mem10"]
}

statuses = ["New", "In Progress", "Completed"]

tasks = []

base_date = datetime.now()

# Generate 150 tasks
for i in range(150):

    team = random.choice(list(teams.keys()))
    member = random.choice(teams[team])

    client = random.choice(clients)
    status = random.choice(statuses)

    random_days = random.randint(0, 10)
    random_hours = random.randint(0, 23)

    deadline = base_date + timedelta(days=random_days, hours=random_hours)

    deadline_str = deadline.strftime("%Y-%m-%d %H:%M:%S")

    tasks.append((client, team, member, status, deadline_str))

# Insert tasks
cursor.executemany(
"""
INSERT INTO tasks (client, team, assigned_to, status, deadline)
VALUES (?, ?, ?, ?, ?)
""",
tasks
)

conn.commit()
conn.close()

print("✅ 150 dummy tasks inserted successfully!")