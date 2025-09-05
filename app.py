# techclub_demo_app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Tech Club Hub", page_icon="🚀", layout="wide")
st.markdown("""
    <style>
        body { background-color: #0a0a0f; color: white; }
        .stApp { background: linear-gradient(135deg,#0a0a0f,#1b0034); }
        h1, h2, h3, h4 { color: #8e40ff; }
        .stButton>button {
            background: linear-gradient(90deg,#8e40ff,#00e5ff);
            color: white; border: none; border-radius: 12px;
            padding: 0.6em 1.2em; font-weight: bold;
        }
        .stButton>button:hover { opacity: 0.9; transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

# ---------------- MOCK DATA ----------------
USERS = {
    "admin": {"password": "123", "role": "Admin"},
    "core": {"password": "123", "role": "Core Team"},
    "lead": {"password": "123", "role": "Team Lead"},
    "member": {"password": "123", "role": "Member"},
    "guest": {"password": "123", "role": "Guest/Sponsor"},
}

EVENTS = pd.DataFrame([
    {"title": "Hackathon 2025", "date": "2025-09-15", "venue": "Main Hall", "capacity": 200, "status": "Open"},
    {"title": "AI Workshop", "date": "2025-09-20", "venue": "Lab 3", "capacity": 50, "status": "Open"},
    {"title": "Tech Talk: Future of Web", "date": "2025-09-25", "venue": "Auditorium", "capacity": 300, "status": "Closed"},
])

PROJECTS = [
    {"title": "Smart Campus App", "status": "In Progress", "tech": "Flutter + Firebase"},
    {"title": "AI Research Portal", "status": "Planning", "tech": "Python + ML"},
    {"title": "Club Website Revamp", "status": "Completed", "tech": "Next.js + Supabase"},
]

MEMBERS = pd.DataFrame([
    {"name": "Alice", "year": "3rd", "skills": "Python, ML"},
    {"name": "Bob", "year": "2nd", "skills": "Web, React"},
    {"name": "Charlie", "year": "4th", "skills": "AI, Cloud"},
])

FINANCES = pd.DataFrame({
    "Category": ["Sponsorships", "Tickets", "Expenses"],
    "Amount": [50000, 10000, 30000]
})

# ---------------- LOGIN ----------------
if "auth_user" not in st.session_state:
    st.session_state["auth_user"] = None

if not st.session_state["auth_user"]:
    st.title("🚀 Tech Club Hub")
    st.subheader("Login to continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["auth_user"] = USERS[username]
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")
else:
    role = st.session_state["auth_user"]["role"]
    st.sidebar.title(f"Welcome, {role}")
    menu = st.sidebar.radio("Navigate", ["Dashboard","Events","Projects","Members","Finances","Announcements","Certificates"])
    if st.sidebar.button("Logout"):
        st.session_state["auth_user"] = None
        st.experimental_rerun()

    # ---------------- DASHBOARD ----------------
    if menu == "Dashboard":
        st.title("🌌 Club Dashboard")
        col1, col2, col3 = st.columns(3)
        col1.metric("Active Members", len(MEMBERS))
        col2.metric("Upcoming Events", EVENTS[EVENTS['status']=="Open"].shape[0])
        col3.metric("Ongoing Projects", sum(1 for p in PROJECTS if p["status"]=="In Progress"))

        fig = px.pie(FINANCES, names="Category", values="Amount", title="Club Finances")
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- EVENTS ----------------
    elif menu == "Events":
        st.title("📅 Events")
        st.dataframe(EVENTS)
        if role in ["Admin","Core Team"]:
            st.subheader("➕ Create Event")
            with st.form("new_event"):
                title = st.text_input("Event Title")
                date = st.date_input("Date")
                venue = st.text_input("Venue")
                cap = st.number_input("Capacity",1,500)
                submitted = st.form_submit_button("Add Event")
                if submitted:
                    st.success(f"Event '{title}' created!")

    # ---------------- PROJECTS ----------------
    elif menu == "Projects":
        st.title("🛠️ Projects")
        for p in PROJECTS:
            st.markdown(f"**{p['title']}** — {p['status']} *(Tech: {p['tech']})*")
        if role in ["Admin","Team Lead"]:
            st.info("You can assign tasks and manage Kanban (future feature).")

    # ---------------- MEMBERS ----------------
    elif menu == "Members":
        st.title("👥 Members")
        st.dataframe(MEMBERS)

    # ---------------- FINANCES ----------------
    elif menu == "Finances":
        st.title("💰 Club Finances")
        st.dataframe(FINANCES)
        fig = px.bar(FINANCES, x="Category", y="Amount", color="Category")
        st.plotly_chart(fig)

    # ---------------- ANNOUNCEMENTS ----------------
    elif menu == "Announcements":
        st.title("📢 Announcements")
        st.success("Hackathon registrations open!")
        st.info("Next Core Team meeting: Monday 5pm")

    # ---------------- CERTIFICATES ----------------
    elif menu == "Certificates":
        st.title("🏅 Certificates")
        st.write("Generate PDF certificates (demo)")
        name = st.text_input("Member Name")
        if st.button("Generate Certificate"):
            st.success(f"Certificate for {name} generated! (demo only)")
