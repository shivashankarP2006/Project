# ------------------------------------------------
# Import Libraries
# ------------------------------------------------
import streamlit as st
import dummy_data

# Import database setup function
from database import create_table

# Import login function
from auth import login

# Import dashboards
from dashboards.manager import manager_dashboard
from dashboards.team_lead import team_lead_dashboard
from dashboards.team_member import team_member_dashboard


# ------------------------------------------------
# Page configuration (must be first Streamlit command)
# ------------------------------------------------
st.set_page_config(
    page_title="Startup Client Manager",
    page_icon="📊",
    layout="wide"
)

# ------------------------------------------------
# Ensure database table exists
# ------------------------------------------------
create_table()

# ------------------------------------------------
# App Header
# ------------------------------------------------
st.markdown(
    "<h1 style='text-align:center;'>📊 Startup Client Management System</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center;'>Makes project management more efficient</p>",
    unsafe_allow_html=True
)

st.divider()

# ------------------------------------------------
# Initialize session state
# ------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# ------------------------------------------------
# Login Section
# ------------------------------------------------
if not st.session_state.logged_in:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        login()

# ------------------------------------------------
# After Login
# ------------------------------------------------
else:

    role = st.session_state.role
    username = st.session_state.username

    # ---------------- Sidebar ----------------
    st.sidebar.title("🚀 Startup Manager")

    st.sidebar.markdown("### 👤 User Info")
    st.sidebar.success(username)

    st.sidebar.markdown("### 🔑 Role")
    st.sidebar.info(role)

    st.sidebar.divider()

    # Logout button
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.sidebar.divider()

    # ---------------- Dashboard Routing ----------------
    if role == "Manager":
        manager_dashboard()

    elif role == "Team Lead":
        team_lead_dashboard()

    elif role == "Team Member":

        team_member_dashboard()
