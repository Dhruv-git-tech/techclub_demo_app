import streamlit as st
import pandas as pd

# -----------------------------
# Mock Login Data
# -----------------------------
USERS = {
    "admin": {"password": "dhruv", "role": "Admin"},
    "core_lead": {"password": "core123", "role": "Team Lead", "team": "Core Team"},
    "tech_lead": {"password": "tech123", "role": "Team Lead", "team": "Technical Team"},
    "event_lead": {"password": "event123", "role": "Team Lead", "team": "Event Planning"},
    "social_lead": {"password": "social123", "role": "Team Lead", "team": "Social Media Team"},
    "outreach_lead": {"password": "outreach123", "role": "Team Lead", "team": "Outreach Team"},
    "rep_lead": {"password": "rep123", "role": "Team Lead", "team": "Representatives"},
    "general_member": {"password": "member123", "role": "Member", "team": "General"},
}

TEAMS = [
    "Core Team",
    "Technical Team",
    "Event Planning",
    "Social Media Team",
    "Outreach Team",
    "Representatives",
    "General"
]

# -----------------------------
# Init Session Data
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user" not in st.session_state:
    st.session_state.user = None
if "events" not in st.session_state:
    st.session_state.events = []
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# -----------------------------
# Auth Functions
# -----------------------------
def login(username, password):
    if username in USERS and USERS[username]["password"] == password:
        st.session_state.logged_in = True
        st.session_state.user = USERS[username]
        st.rerun()
    else:
        st.error("❌ Invalid username or password")

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.rerun()

# -----------------------------
# Custom CSS Styling
# -----------------------------
st.markdown("""
    <style>
    body {
        background-color: #0e0e1f;
        color: #ffffff;
    }
    .block-container {
        padding-top: 1rem;
    }
    .stButton button {
        background: linear-gradient(45deg, #8e40ff, #4fd1c5);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.6rem 1rem;
        font-weight: 600;
    }
    .stButton button:hover {
        background: linear-gradient(45deg, #4fd1c5, #8e40ff);
        color: black;
    }
    .stDataFrame, .stTable {
        background-color: #1a1a2e;
        border-radius: 10px;
        padding: 10px;
    }
    .sidebar .sidebar-content {
        background-color: #11111f;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="DevCatalyst | MECS Tech Club", layout="wide")

st.title("👨‍💻🚀 DevCatalyst | MECS Tech Club")
st.caption("💡 Catalyzing Innovation, Developing Excellence")

# -----------------------------
# Login Screen
# -----------------------------
if not st.session_state.logged_in:
    st.subheader("🔑 Login to Continue")

    st.info("""
    ### ℹ️ About the Club  
    Welcome to **DevCatalyst – the official student-led tech community at Matrusri Engineering College!**  

    📌 What we do:  
    • Tech workshops & coding challenges  
    • Guest talks & mentorship from industry pros  
    • Startup ideation & project showcases  
    • Internship and networking opportunities  

    🎯 *Stay connected, stay ahead. Let's bridge the gap between classroom and career!*
    """)

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")
    if st.button("Login"):
        login(username, password)

# -----------------------------
# Logged-in Views
# -----------------------------
else:
    user = st.session_state.user
    role = user['role']

    # Sidebar
    st.sidebar.markdown(f"### 👋 Welcome, {role}")
    if st.sidebar.button("🚪 Logout"):
        logout()

    # -----------------------------
    # Admin Dashboard
    # -----------------------------
    if role == "Admin":
        st.subheader("📊 Admin Dashboard")
        st.write("Manage all teams and members here.")

        # Team Overview
        st.write("### 👥 Team Overview")
        team_data = pd.DataFrame({
            "Team": TEAMS,
            "Members": [8, 12, 6, 5, 7, 10, 20],
            "Active_Projects": [3, 5, 2, 4, 3, 1, 0]
        })
        st.dataframe(team_data)

        st.write("### 📊 Team Size Chart")
        st.bar_chart(team_data.set_index("Team")["Members"])

        # Show all events
        st.write("### 📅 All Club Events")
        if st.session_state.events:
            st.table(pd.DataFrame(st.session_state.events))
        else:
            st.info("No events created yet.")

        # Show all tasks
        st.write("### ✅ All Tasks Assigned")
        if st.session_state.tasks:
            st.table(pd.DataFrame(st.session_state.tasks))
        else:
            st.info("No tasks assigned yet.")

    # -----------------------------
    # Team Lead Dashboard
    # -----------------------------
    elif role == "Team Lead":
        st.subheader(f"👑 {user['team']} Dashboard (Team Lead)")

        tab1, tab2 = st.tabs(["📅 Manage Events", "✅ Assign Tasks"])

        with tab1:
            st.write("### Create Event")
            event_title = st.text_input("📝 Event Title")
            event_date = st.date_input("📆 Event Date")
            event_desc = st.text_area("🖊️ Description")
            if st.button("Add Event"):
                st.session_state.events.append({
                    "team": user["team"],
                    "title": event_title,
                    "date": str(event_date),
                    "description": event_desc
                })
                st.success("🎉 Event added!")
                st.rerun()

            st.write("### 📅 Your Team Events")
            team_events = [e for e in st.session_state.events if e["team"] == user["team"]]
            if team_events:
                st.table(pd.DataFrame(team_events))
            else:
                st.info("No events created yet.")

        with tab2:
            st.write("### Assign Task")
            member_name = st.text_input("👤 Member Name")
            task_desc = st.text_input("📝 Task")
            if st.button("Assign Task"):
                st.session_state.tasks.append({
                    "team": user["team"],
                    "member": member_name,
                    "task": task_desc,
                    "status": "Pending"
                })
                st.success(f"✅ Task assigned to {member_name}")
                st.rerun()

            st.write("### 📋 Your Team Tasks")
            team_tasks = [t for t in st.session_state.tasks if t["team"] == user["team"]]
            if team_tasks:
                st.table(pd.DataFrame(team_tasks))
            else:
                st.info("No tasks assigned yet.")

    # -----------------------------
    # Member Dashboard
    # -----------------------------
    elif role == "Member":
        st.subheader(f"🙋 {user['team']} Member Dashboard")

        st.write("### 📅 Upcoming Events (Your Team)")
        member_events = [e for e in st.session_state.events if e["team"] == user["team"]]
        if member_events:
            st.table(pd.DataFrame(member_events))
        else:
            st.info("No events yet for your team.")

        st.write("### ✅ Your Tasks")
        member_tasks = [t for t in st.session_state.tasks if t["team"] == user["team"]]
        if member_tasks:
            st.table(pd.DataFrame(member_tasks))
        else:
            st.info("No tasks assigned yet.")
