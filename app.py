import streamlit as st
import pandas as pd
import random

st.set_page_config(page_title="DevCatalyst Club Manager", layout="wide")

# -----------------------
# Custom Styling (Dark Neon)
# -----------------------
st.markdown("""
<style>
body {
    background-color: #0d0d0d;
    color: #f0f0f0;
    font-family: 'Inter', sans-serif;
}
h1, h2, h3, h4 {
    color: #8e40ff;
}
.stButton>button {
    background: linear-gradient(90deg, #8e40ff, #00e6ff);
    color: white;
    border-radius: 12px;
    border: none;
    padding: 0.6em 1.2em;
    font-weight: bold;
    transition: 0.3s;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #00e6ff, #8e40ff);
    transform: scale(1.05);
}
.stProgress > div > div > div {
    background-color: #8e40ff !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# Mock Users & Teams
# -----------------------
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "lead_ai": {"password": "lead123", "role": "Team Lead", "team": "AI/ML Team"},
    "lead_web": {"password": "lead123", "role": "Team Lead", "team": "Web Dev Team"},
    "member1": {"password": "mem123", "role": "Member", "team": "AI/ML Team"},
    "member2": {"password": "mem123", "role": "Member", "team": "Web Dev Team"},
    "guest": {"password": "guest", "role": "Guest"},
}

TEAM_INFO = {
    "AI/ML Team": {"lead": "lead_ai", "focus": "Artificial Intelligence & Machine Learning"},
    "Web Dev Team": {"lead": "lead_web", "focus": "Full Stack Web Development"},
    "Cloud Team": {"lead": None, "focus": "Cloud & DevOps"},
    "Cybersecurity Team": {"lead": None, "focus": "Security Research"},
}

# -----------------------
# Session State Defaults
# -----------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.role = None
    st.session_state.username = None
    st.session_state.events = []
    st.session_state.tasks = []

# -----------------------
# Login
# -----------------------
def login():
    st.title("🔐 DevCatalyst Club Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state.logged_in = True
            st.session_state.role = USERS[username]["role"]
            st.session_state.username = username
            st.success(f"✅ Logged in as {st.session_state.role}")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

# -----------------------
# Admin Dashboard
# -----------------------
def admin_dashboard():
    st.title("🛠️ Admin Dashboard – DevCatalyst | MECS Tech Club")
    st.write("👨‍💻 Manage teams, members, events, and tasks in one place.")

    # Club Description
    st.info(
        "📌 **DevCatalyst | MECS Tech Club** 👨‍💻🚀\n\n"
        "Welcome to DevCatalyst – the official student-led tech community at Matrusri Engineering College!\n\n"
        "💡 Catalyzing Innovation, Developing Excellence\n\n"
        "### What we do:\n"
        "- Tech workshops & coding challenges\n"
        "- Guest talks & mentorship from industry pros\n"
        "- Startup ideation & project showcases\n"
        "- Internship and networking opportunities\n\n"
        "📅 Regular updates | 🎯 Skill-building | 🤝 Collaboration"
    )

    # Teams
    st.subheader("👥 Teams Overview")
    for team, info in TEAM_INFO.items():
        with st.expander(f"🔹 {team} — Lead: {info['lead']}"):
            members = [f"{team} Member {i+1}" for i in range(5)]
            st.write(f"**Total Members:** {len(members)}")
            st.write(f"**Focus:** {info['focus']}")

            # Team tasks
            team_tasks = [t for t in st.session_state.tasks if t["team"] == team]
            if team_tasks:
                df = pd.DataFrame(team_tasks)
                st.write("📋 Task Status")
                st.table(df)
                completed = sum(1 for t in team_tasks if t["status"] == "Completed")
                total = len(team_tasks)
                progress = int((completed / total) * 100) if total > 0 else 0
                st.progress(progress / 100)
                st.caption(f"{progress}% tasks completed")
            else:
                st.info("No tasks assigned yet.")

            # Lead activity
            if info["lead"]:
                events_by_lead = [e for e in st.session_state.events if e["team"] == team]
                tasks_by_lead = [t for t in st.session_state.tasks if t["team"] == team]
                st.write("📊 **Team Lead Activity**")
                st.write(f"- Events Created: {len(events_by_lead)}")
                st.write(f"- Tasks Assigned: {len(tasks_by_lead)}")
            else:
                st.warning("No lead assigned for this team.")

            # Drill-down member view
            st.divider()
            st.write("🔎 **Member Insights**")
            selected_member = st.selectbox(
                f"View member details in {team}:", ["-- Select --"] + members, key=f"member_{team}"
            )
            if selected_member != "-- Select --":
                st.subheader(f"👤 {selected_member}")
                personal_tasks = [
                    {"Task": f"Task {i+1}", "Status": "Completed" if i % 2 == 0 else "Pending"}
                    for i in range(4)
                ]
                df_member = pd.DataFrame(personal_tasks)
                st.table(df_member)
                completed = sum(1 for t in personal_tasks if t["Status"] == "Completed")
                total = len(personal_tasks)
                progress = int((completed / total) * 100)
                st.progress(progress / 100)
                st.caption(f"{progress}% tasks completed by {selected_member}")
                st.info(f"🏆 Contribution Points: {completed * 10}")
                st.write("📅 Last Active: Yesterday")

    # Leaderboard
    st.subheader("🏆 Global Leaderboard")
    leaderboard_data = []
    for team in TEAM_INFO:
        for i in range(5):
            name = f"{team} Member {i+1}"
            points = random.randint(20, 100)
            leaderboard_data.append({"Member": name, "Team": team, "Points": points})
    df_leader = pd.DataFrame(leaderboard_data).sort_values("Points", ascending=False)
    st.table(df_leader.head(10))

# -----------------------
# Team Lead Dashboard
# -----------------------
def team_lead_dashboard():
    team = USERS[st.session_state.username]["team"]
    st.title(f"👨‍🏫 Team Lead Dashboard – {team}")
    task_title = st.text_input("New Task Title")
    if st.button("Assign Task"):
        st.session_state.tasks.append({"task": task_title, "team": team, "status": "Pending"})
        st.success("✅ Task Assigned!")
    if st.session_state.tasks:
        df = pd.DataFrame(st.session_state.tasks)
        st.table(df[df["team"] == team])

# -----------------------
# Member Dashboard
# -----------------------
def member_dashboard():
    team = USERS[st.session_state.username]["team"]
    st.title(f"🙋 Member Dashboard – {team}")
    personal_tasks = [
        {"Task": f"Task {i+1}", "Status": "Completed" if i % 2 == 0 else "Pending"}
        for i in range(5)
    ]
    st.table(pd.DataFrame(personal_tasks))
    st.progress(0.6)
    st.caption("60% tasks completed")

# -----------------------
# Guest View
# -----------------------
def guest_view():
    st.title("👋 Welcome Guest")
    st.write("You can explore upcoming events and public posts here.")
    if not st.session_state.events:
        st.info("No upcoming events. Stay tuned!")

# -----------------------
# Main
# -----------------------
if not st.session_state.get("logged_in", False):
    login()
else:
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.role = None
        st.session_state.username = None
        st.rerun()

    role = st.session_state.get("role", None)

    if role == "Admin":
        admin_dashboard()
    elif role == "Team Lead":
        team_lead_dashboard()
    elif role == "Member":
        member_dashboard()
    else:
        guest_view()
