import streamlit as st
import pandas as pd

# -------------------------------
# Sample Users and Roles
# -------------------------------
users = {
    "admin": {"password": "admin123", "role": "Admin"},
    "core_lead": {"password": "core123", "role": "Lead", "team": "Core Team"},
    "core_member1": {"password": "member123", "role": "Member", "team": "Core Team"},
    "tech_lead": {"password": "tech123", "role": "Lead", "team": "Technical Team"},
    "tech_member1": {"password": "member123", "role": "Member", "team": "Technical Team"},
    "general_lead": {"password": "general123", "role": "Lead", "team": "General"},
    "general_member1": {"password": "member123", "role": "Member", "team": "General"},
    "rep_lead": {"password": "rep123", "role": "Lead", "team": "Representatives"},
    "rep_member1": {"password": "member123", "role": "Member", "team": "Representatives"},
    "event_lead": {"password": "event123", "role": "Lead", "team": "Event Planning"},
    "event_member1": {"password": "member123", "role": "Member", "team": "Event Planning"},
    "smedia_lead": {"password": "smedia123", "role": "Lead", "team": "Social Media Team"},
    "smedia_member1": {"password": "member123", "role": "Member", "team": "Social Media Team"},
    "outreach_lead": {"password": "outreach123", "role": "Lead", "team": "Outreach Team"},
    "outreach_member1": {"password": "member123", "role": "Member", "team": "Outreach Team"},
}

# -------------------------------
# Sample Teams and Tasks
# -------------------------------
teams = {
    "Core Team": {
        "lead": "core_lead",
        "members": ["core_member1"],
        "tasks": {"Plan semester roadmap": 80, "Host orientation event": 50}
    },
    "Technical Team": {
        "lead": "tech_lead",
        "members": ["tech_member1"],
        "tasks": {"Hackathon planning": 40, "Workshop on AI": 70}
    },
    "General": {
        "lead": "general_lead",
        "members": ["general_member1"],
        "tasks": {"Maintain WhatsApp updates": 90}
    },
    "Representatives": {
        "lead": "rep_lead",
        "members": ["rep_member1"],
        "tasks": {"Collect feedback from classes": 60}
    },
    "Event Planning": {
        "lead": "event_lead",
        "members": ["event_member1"],
        "tasks": {"Annual Tech Fest": 30, "Weekly meetups": 50}
    },
    "Social Media Team": {
        "lead": "smedia_lead",
        "members": ["smedia_member1"],
        "tasks": {"Instagram campaign": 75, "Event posters": 65}
    },
    "Outreach Team": {
        "lead": "outreach_lead",
        "members": ["outreach_member1"],
        "tasks": {"Industry connections": 20, "Guest talks": 40}
    }
}

# -------------------------------
# Session State Init
# -------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.team = ""

# -------------------------------
# Futuristic Theme Styling
# -------------------------------
st.markdown("""
    <style>
    body { background-color: #0e1117; color: #fff; }
    .stProgress > div > div > div > div { background-image: linear-gradient(to right, #8e40ff , #00e6ff); }
    .big-font { font-size:24px !important; font-weight:700; color:#00e6ff; }
    .card {
        background-color: #161a23;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 0 15px rgba(142,64,255,0.4);
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💻🚀 DevCatalyst | MECS Tech Club Management")

# -------------------------------
# Login Page
# -------------------------------
if not st.session_state.logged_in:
    st.subheader("🔑 Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login", use_container_width=True):
        if username in users and users[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = users[username]["role"]
            st.session_state.team = users[username].get("team", "")
            st.success(f"✅ Welcome {username} ({st.session_state.role})")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# -------------------------------
# Logged-in Views
# -------------------------------
else:
    role = st.session_state.role
    username = st.session_state.username

    st.sidebar.title("📌 Navigation")
    st.sidebar.write(f"👤 Logged in as: **{username} ({role})**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # -------------------------------
    # Admin Dashboard
    # -------------------------------
    if role == "Admin":
        st.header("🛠️ Admin Dashboard")

        # Team Summary Chart
        st.subheader("📊 Team Progress Overview")
        summary = {team: int(sum(details["tasks"].values())/len(details["tasks"])) for team, details in teams.items()}
        df = pd.DataFrame.from_dict(summary, orient="index", columns=["Progress %"])
        st.bar_chart(df)

        st.markdown("---")
        # Detailed Team Cards
        for team, details in teams.items():
            st.markdown(f"<div class='card'><span class='big-font'>👥 {team}</span>", unsafe_allow_html=True)
            st.write(f"**Team Lead:** {details['lead']}")
            st.write(f"**Members:** {', '.join(details['members'])}")
            st.write("📌 **Tasks & Progress**")
            for task, progress in details["tasks"].items():
                st.progress(progress / 100)
                st.write(f"{task}: {progress}% complete")
            st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------
    # Team Lead Dashboard
    # -------------------------------
    elif role == "Lead":
        team = st.session_state.team
        st.header(f"👑 Team Lead Dashboard - {team}")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write(f"**Members:** {', '.join(teams[team]['members'])}")
        st.write("📌 **Tasks & Progress** (Update below)")
        for task, progress in teams[team]["tasks"].items():
            new_val = st.slider(f"{task}", 0, 100, progress)
            teams[team]["tasks"][task] = new_val
            st.progress(new_val / 100)
        st.markdown("</div>", unsafe_allow_html=True)

    # -------------------------------
    # Member Dashboard
    # -------------------------------
    elif role == "Member":
        team = st.session_state.team
        st.header(f"🙋 Member Dashboard - {team}")
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.write("📌 **Your Tasks**")
        for task, progress in teams[team]["tasks"].items():
            st.progress(progress / 100)
            st.write(f"- {task}: {progress}% complete")
        st.markdown("</div>", unsafe_allow_html=True)
