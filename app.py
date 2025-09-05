# techclub_demo_app.py
import streamlit as st
import pandas as pd
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

if "PROJECTS" not in st.session_state:
    st.session_state["PROJECTS"] = [
        {"title": "Smart Campus App", "status": "To Do", "tech": "Flutter + Firebase"},
        {"title": "AI Research Portal", "status": "In Progress", "tech": "Python + ML"},
        {"title": "Club Website Revamp", "status": "Completed", "tech": "Next.js + Supabase"},
    ]

EVENTS = pd.DataFrame([
    {"title": "Hackathon 2025", "date": "2025-09-15", "venue": "Main Hall", "capacity": 200, "status": "Open"},
    {"title": "AI Workshop", "date": "2025-09-20", "venue": "Lab 3", "capacity": 50, "status": "Open"},
    {"title": "Tech Talk: Future of Web", "date": "2025-09-25", "venue": "Auditorium", "capacity": 300, "status": "Closed"},
])

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
            st.rerun()
        else:
            st.error("Invalid username or password")
else:
    role = st.session_state["auth_user"]["role"]
    st.sidebar.title(f"Welcome, {role}")
    menu = st.sidebar.radio("Navigate", ["Dashboard","Events","Projects","Members","Finances","Announcements","Certificates"])
    if st.sidebar.button("Logout"):
        st.session_state["auth_user"] = None
        st.rerun()

    # ---------------- DASHBOARD ----------------
    if menu == "Dashboard":
        st.title("🌌 Club Dashboard")
        col1, col2, col3 = st.columns(3)
        col1.metric("Active Members", len(MEMBERS))
        col2.metric("Upcoming Events", EVENTS[EVENTS['status']=="Open"].shape[0])
        col3.metric("Ongoing Projects", sum(1 for p in st.session_state["PROJECTS"] if p["status"]=="In Progress"))

        st.subheader("Club Finances Overview")
        st.bar_chart(FINANCES.set_index("Category"))

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

    # ---------------- PROJECTS (Kanban) ----------------
    elif menu == "Projects":
        st.title("🛠️ Projects — Kanban Board")

        statuses = ["To Do", "In Progress", "Completed"]

        cols = st.columns(len(statuses))
        for idx, status in enumerate(statuses):
            with cols[idx]:
                st.subheader(status)
                for i, project in enumerate(st.session_state["PROJECTS"]):
                    if project["status"] == status:
                        st.markdown(f"**{project['title']}**  \n_Tech: {project['tech']}_")
                        if role in ["Admin","Team Lead"]:
                            new_status = st.selectbox(
                                f"Move '{project['title']}'",
                                statuses,
                                index=statuses.index(status),
                                key=f"{project['title']}_select"
                            )
                            if new_status != status:
                                st.session_state["PROJECTS"][i]["status"] = new_status
                                st.rerun()
                        st.divider()

        if role in ["Admin","Team Lead"]:
            st.subheader("➕ Add Project")
            with st.form("new_proj"):
                title = st.text_input("Project Title")
                tech = st.text_input("Tech Stack")
                submitted = st.form_submit_button("Add Project")
                if submitted:
                    st.session_state["PROJECTS"].append(
                        {"title": title, "status": "To Do", "tech": tech}
                    )
                    st.success(f"Project '{title}' added!")
                    st.rerun()

    # ---------------- MEMBERS ----------------
    elif menu == "Members":
        st.title("👥 Members")
        st.dataframe(MEMBERS)

    # ---------------- FINANCES ----------------
    elif menu == "Finances":
        st.title("💰 Club Finances")
        st.dataframe(FINANCES)
        st.bar_chart(FINANCES.set_index("Category"))

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
