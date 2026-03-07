import streamlit as st

# Hardcoded demo users (for showcase)
USERS = {
    "manager": {"password": "admin123", "role": "Manager"},

    "tl1": {"password": "tl123", "role": "Team Lead"},
    "tl2": {"password": "tl123", "role": "Team Lead"},
    "tl3": {"password": "tl123", "role": "Team Lead"},
    "tl4": {"password": "tl123", "role": "Team Lead"},
    "tl5": {"password": "tl123", "role": "Team Lead"},

    "member1": {"password": "mem123", "role": "Team Member"},
    "member2": {"password": "mem123", "role": "Team Member"},
    "member3": {"password": "mem123", "role": "Team Member"},
    "member4": {"password": "mem123", "role": "Team Member"},
    "member5": {"password": "mem123", "role": "Team Member"},
    "member6": {"password": "mem123", "role": "Team Member"},
    "member7": {"password": "mem123", "role": "Team Member"},
    "member8": {"password": "mem123", "role": "Team Member"},
    "member9": {"password": "mem123", "role": "Team Member"},
    "member10": {"password": "mem123", "role": "Team Member"}
}

def login():
    st.subheader("Login")

    # Input fields
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # When login button is pressed
    if st.button("Login"):

        # Validate credentials
        if username in USERS and USERS[username]["password"] == password:

            # Store login state
            st.session_state.logged_in = True
            st.session_state.role = USERS[username]["role"]
            st.session_state.username = username

            st.success("Login successful")
            st.rerun()

        else:
            st.error("Invalid credentials")