import streamlit as st

# Hardcoded demo users (for showcase)
USERS = {
    "manager": {"password": "admin123", "role": "Manager"},

    "tl1": {"password": "tl123", "role": "Team Lead"},
    "tl2": {"password": "tl123", "role": "Team Lead"},
    "tl3": {"password": "tl123", "role": "Team Lead"},
    "tl4": {"password": "tl123", "role": "Team Lead"},
    "tl5": {"password": "tl123", "role": "Team Lead"},

    "mem1": {"password": "mem123", "role": "Team Member"},
    "mem2": {"password": "mem123", "role": "Team Member"},
    "mem3": {"password": "mem123", "role": "Team Member"},
    "mem4": {"password": "mem123", "role": "Team Member"},
    "mem5": {"password": "mem123", "role": "Team Member"},
    "memb": {"password": "mem123", "role": "Team Member"},
    "mem7": {"password": "mem123", "role": "Team Member"},
    "mem8": {"password": "mem123", "role": "Team Member"},
    "mem9": {"password": "mem123", "role": "Team Member"},
    "mem10": {"password": "mem123", "role": "Team Member"}
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
