import streamlit as st
import pandas as pd

# -----------------------------
# Mock Login Data
# -----------------------------
USERS = {
    "admin": {"password": "admin123", "role": "Admin"},
    "core_lead": {"password": "core123", "role": "Team Lead", "team": "Core Team"},
    "tech_lead": {"password": "tech123", "role": "Team Lead", "team": "Technical Team"},
    "event_lead": {"password": "event123", "role": "Team Lead", "team": "Event Planning"},
    "social_lead": {"password": "social123", "role": "Team Lead", "team": "Social Media Team"},
    "outreach_lead": {"password": "outreach123", "role": "Team Lead", "team": "Outreach Team"},
    "rep_lead": {"password": "rep123", "role": "Team Lead", "team": "Representatives"},
    "general_member": {"password": "member123", "role": "Member", "team": "General"},
}

TEAM_INFO = {
    "Core Team": {"lead": "Core Lead", "focus": "Strategy & Leadership", "color": "linear-gradient(45deg, #8e2de2, #4a00e0)"},
    "Technical Team": {"lead": "Tech Lead", "focus": "Coding & Projects", "color": "linear-gradient(45deg, #00c6ff, #0072ff)"},
    "Event Planning": {"lead": "Event Lead", "focus": "Workshops & Logistics", "color": "linear-gradient(45deg, #ff416c, #ff4b2b)"},
    "Social Media Team": {"lead": "Social Lead", "focus": "Content & Branding", "color": "linear-gradient(45deg, #ff9a9e, #fad0c4)"},
    "Outreach Team": {"lead": "Outreach Lead", "focus": "Partnerships & Sponsors", "color": "linear-gradient(45deg, #11998e, #38ef7d)"},
    "Representatives": {"lead": "Rep Lead", "focus": "Student Connect", "color": "linear-gradient(45deg, #f7971e, #ffd200)"},
    "General": {"lead": "N/A", "focus": "Learning & Growth", "color": "linear-gradient(45deg, #36d1dc, #5b86e5)"},
}

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
if "scores" not in st.session_state:
    st.session_state.scores = {"Alice": 50, "Bob": 30, "Charlie": 20}

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
st.set_page_config(page_title="DevCatalyst | MECS Tech Club", layout="wide")

st.markdown("""
    <style>
    body { background-color: #0d0d1f; color: #ffffff; }
    .banner {
        background: linear-gradient(90deg, #8e2de2, #4a00e0);
        color: white;
        text-align: center;
        padding: 3rem 1rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 0 25px rgba(142,64,255,0.6);
    }
    .section {
        padding: 2rem;
        margin: 1rem 0;
        border-radius: 16px;
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
    }
    .team-card {
        padding: 1rem;
        border-radius: 16px;
        color: white;
        margin: 0.7rem;
        text-align: center;
        font-weight: 600;
        box-shadow: 0px 4px 25px rgba(0,0,0,0.4);
        transition: transform 0.3s;
    }
    .team-card:hover {
        transform: scale(1.05);
    }
    .stButton button {
        background: linear-gradient(45deg, #00eaff, #8e40ff);
        color: white; border-radius: 12px; border: none;
        padding: 0.7rem 1.2rem; font-weight: 600;
        box-shadow: 0px 0px 10px rgba(0,234,255,0.7);
    }
    .stButton button:hover {
        background: linear-gradient(45deg, #8e40ff, #00eaff);
        color: black;
    }
    .badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        color: white;
    }
    .gold { background: linear-gradient(45deg, #FFD700, #FFA500); }
    .silver { background: linear-gradient(45deg, #C0C0C0, #808080); }
    .bronze { background: linear-gradient(45deg, #cd7f32, #8b4513); }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Landing Page
# -----------------------------
if not st.session_state.logged_in:
    # Banner
    st.markdown("""
        <div class="banner">
            <h1>👨‍💻🚀 DevCatalyst | MECS Tech Club</h1>
            <h3>💡 Catalyzing Innovation, Developing Excellence</h3>
        </div>
    """, unsafe_allow_html=True)

    # About Section
    st.markdown("""
    <div class="section">
    <h2>📌 What We Do</h2>
    <ul>
        <li>⚡ Tech workshops & coding challenges</li>
        <li>🎤 Guest talks & mentorship from industry pros</li>
        <li>🚀 Startup ideation & project showcases</li>
        <li>🌐 Internship and networking opportunities</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    # Team Cards Section
    st.markdown("<h2 style='text-align:center;'>👥 Our Teams</h2>", unsafe_allow_html=True)
    cols = st.columns(3)
    i = 0
    for team, info in TEAM_INFO.items():
        with cols[i % 3]:
            st.markdown(
                f"""
                <div class="team-card" style="background:{info['color']}">
                    <h3>{team}</h3>
                    <p>👑 Lead: {info['lead']}</p>
                    <p>🎯 Focus: {info['focus']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        i += 1

    # Opportunities Section
    st.markdown("""
    <div class="section">
    <h2>🎯 Opportunities</h2>
    <p>Stay connected, stay ahead. Let's bridge the gap between <b>classroom and career</b>!  
    ✨ Skill-building | 🤝 Collaboration | 📅 Regular updates</p>
    </div>
    """, unsafe_allow_html=True)

    # Login Form
    st.subheader("🔑 Login to Continue")
    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")
    if st.button("Login ➝"):
        login(username, password)

# -----------------------------
# Logged-in Dashboards
# -----------------------------
else:
    user = st.session_state.user
    role = user['role']
    st.sidebar.markdown("### ⚡ Navigation")
    st.sidebar.success(f"✅ Logged in as {role}")
    if st.sidebar.button("🚪 Logout"):
        logout()

    if role == "Admin":
        st.header("📊 Admin Dashboard")
        col1, col2, col3 = st.columns(3)
        col1.metric("👥 Total Members", "68")
        col2.metric("📅 Events", str(len(st.session_state.events)))
        col3.metric("✅ Tasks", str(len(st.session_state.tasks)))

        st.subheader("👥 Team Overview")
        team_data = pd.DataFrame({
            "Team": list(TEAM_INFO.keys()),
            "Members": [8, 12, 6, 5, 7, 10, 20],
            "Active Projects": [3, 5, 2, 4, 3, 1, 0]
        })
        st.bar_chart(team_data.set_index("Team")["Members"])

        st.subheader("🏆 Leaderboard")
        leaderboard = pd.DataFrame.from_dict(st.session_state.scores, orient="index", columns=["Points"])
        leaderboard = leaderboard.sort_values("Points", ascending=False)

        for i, (name, row) in enumerate(leaderboard.iterrows()):
            badge_class = "gold" if i == 0 else "silver" if i == 1 else "bronze" if i == 2 else ""
            st.markdown(
                f"<div class='badge {badge_class}'>{i+1}️⃣ {name} - {row['Points']} pts</div>",
                unsafe_allow_html=True
            )

    elif role == "Team Lead":
        st.header(f"👑 {user['team']} Lead Dashboard")
        tab1, tab2 = st.tabs(["📅 Manage Events", "✅ Assign Tasks"])

        with tab1:
            st.subheader("Create Event")
            title = st.text_input("📝 Event Title")
            date = st.date_input("📆 Date")
            desc = st.text_area("🖊️ Description")
            if st.button("Add Event 🎉"):
                st.session_state.events.append({"team": user["team"], "title": title, "date": str(date), "desc": desc})
                st.balloons()
                st.success("Event added!")
                st.rerun()
            st.write("### Your Events")
            df = [e for e in st.session_state.events if e["team"] == user["team"]]
            if df: st.table(pd.DataFrame(df))
            else: st.info("No events yet.")

        with tab2:
            st.subheader("Assign Task")
            member = st.text_input("👤 Member Name")
            task = st.text_input("📝 Task")
            if st.button("Assign Task ✅"):
                st.session_state.tasks.append({"team": user["team"], "member": member, "task": task, "status": "Pending"})
                st.session_state.scores[member] = st.session_state.scores.get(member, 0) + 10
                st.snow()
                st.success(f"Task assigned to {member}")
                st.rerun()
            st.write("### Your Tasks")
            df = [t for t in st.session_state.tasks if t["team"] == user["team"]]
            if df: st.table(pd.DataFrame(df))
            else: st.info("No tasks yet.")

    elif role == "Member":
        st.header(f"🙋 {user['team']} Member Dashboard")
        st.subheader("📅 Events")
        events = [e for e in st.session_state.events if e["team"] == user["team"]]
        if events: st.table(pd.DataFrame(events))
        else: st.info("No events for your team yet.")
        
        st.subheader("✅ Your Tasks")
        tasks = [t for t in st.session_state.tasks if t["team"] == user["team"]]
        if tasks: st.table(pd.DataFrame(tasks))
        else: st.info("No tasks yet.")
