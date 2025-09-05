# app.py
import streamlit as st
import json, os, time
from datetime import datetime
from pathlib import Path
import streamlit.components.v1 as components

# ---------------- Config & Styling ----------------
st.set_page_config(page_title="DevCatalyst | MECS Tech Club", layout="wide", page_icon="🚀")

CSS = """
<style>
:root{
  --bg:#0a0a12; --card:#07102566; --neon:#8e40ff; --accent:#00e5ff; --muted:#bfc6d1;
}
body { background: var(--bg); color: #e6eef8; }
.stButton>button { background: linear-gradient(90deg,var(--neon),var(--accent)); color: black; border-radius:10px; padding:8px 12px; font-weight:600; }
.header { display:flex; align-items:center; gap:16px; }
.club-title { font-size:30px; font-weight:800; color:var(--neon); }
.card { background: rgba(255,255,255,0.03); border:1px solid rgba(142,64,255,0.08); padding:14px; border-radius:10px; }
.small-muted { color: #9aa6b2; font-size:12px; }
.badge { padding:4px 8px; border-radius:8px; font-weight:700; color:#071025; display:inline-block;}
.status-todo { background: #ffd166; }
.status-progress { background: #5cc8ff; }
.status-done { background: #8efc9a; }
.task-card { padding:10px; border-radius:8px; margin-bottom:10px; background: rgba(255,255,255,0.02); border-left:4px solid rgba(255,255,255,0.03); }
.team-pill { padding:6px 10px; border-radius:12px; background:rgba(255,255,255,0.03); margin-right:6px; display:inline-block; }
.topbar { display:flex; justify-content:space-between; align-items:center; gap:12px; }
.logo { width:64px; height:64px; border-radius:8px; }
a { color: var(--accent); }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------------- Starfield Background (HTML) ----------------
starfield_html = """
<canvas id="s"></canvas>
<script>
const c=document.getElementById('s'); const ctx=c.getContext('2d');
function resize(){c.width=window.innerWidth; c.height=window.innerHeight;}
resize(); window.addEventListener('resize',resize);
let stars=[]; for(let i=0;i<300;i++){stars.push({x:Math.random()*c.width,y:Math.random()*c.height,r:Math.random()*1.4});}
function draw(){ctx.clearRect(0,0,c.width,c.height); ctx.fillStyle='rgba(255,255,255,0.08)'; for(let s of stars){ctx.beginPath(); ctx.arc(s.x,s.y,s.r,0,Math.PI*2); ctx.fill();}}
function anim(){ for(let s of stars){ s.x+=(Math.random()-0.5)*0.6; s.y+=(Math.random()-0.5)*0.6; if(s.x<0) s.x=c.width; if(s.x>c.width) s.x=0; if(s.y<0) s.y=c.height; if(s.y>c.height) s.y=0;} draw(); requestAnimationFrame(anim); }
anim();
</script>
<style>#s{position:fixed;top:0;left:0;z-index:-1}</style>
"""
components.html(starfield_html, height=0)

# ---------------- Data file & seed ----------------
DATA_FILE = Path("devcatalyst_data.json")

DEFAULT = {
    "club": {
        "name": "DevCatalyst | MECS Tech Club 👨‍💻🚀",
        "description": ("Welcome to DevCatalyst – the official student-led tech community at Matrusri Engineering College!\n"
                        "💡 Catalyzing Innovation, Developing Excellence\n\n"
                        "📌 What we do:\n"
                        "• Tech workshops & coding challenges\n"
                        "• Guest talks & mentorship from industry pros\n"
                        "• Startup ideation & project showcases\n"
                        "• Internship and networking opportunities\n\n"
                        "📅 Regular updates | 🎯 Skill-building | 🤝 Collaboration")
    },
    "teams": {
        "Core Team": {"lead": "core_lead", "members": ["core_lead", "core_member1"]},
        "Technical Team": {"lead": "tech_lead", "members": ["tech_lead", "tech_member1", "tech_member2"]},
        "General": {"lead": None, "members": []},
        "Representatives": {"lead": None, "members": []},
        "Event Planning": {"lead": "event_lead", "members": ["event_lead","event_member1"]},
        "Social media team": {"lead": "social_lead", "members": ["social_lead","social_member1"]},
        "Outreach Team": {"lead": "outreach_lead", "members": ["outreach_lead"]}
    },
    "users": {
        "admin": {"password": "123", "role": "Admin", "team": None},
        "core_lead": {"password": "123", "role": "Team Lead", "team": "Core Team"},
        "core_member1": {"password": "123", "role": "Member", "team": "Core Team"},
        "tech_lead": {"password": "123", "role": "Team Lead", "team": "Technical Team"},
        "tech_member1": {"password": "123", "role": "Member", "team": "Technical Team"},
        "tech_member2": {"password": "123", "role": "Member", "team": "Technical Team"},
        "event_lead": {"password": "123", "role": "Team Lead", "team": "Event Planning"},
        "event_member1": {"password": "123", "role": "Member", "team": "Event Planning"},
        "social_lead": {"password": "123", "role": "Team Lead", "team": "Social media team"},
        "social_member1": {"password": "123", "role": "Member", "team": "Social media team"},
        "outreach_lead": {"password": "123", "role": "Team Lead", "team": "Outreach Team"},
    },
    "tasks": [
        {"id": 1, "title": "Plan Hackathon", "desc": "Define tracks + rules", "status": "To Do", "team": "Event Planning", "assigned_to": "event_lead", "created_by": "admin", "created_at": time.time()},
        {"id": 2, "title": "Social Campaign", "desc": "Create reels for event", "status": "In Progress", "team": "Social media team", "assigned_to": "social_member1", "created_by": "social_lead", "created_at": time.time()},
        {"id": 3, "title": "Deploy Site Revamp", "desc": "Finish landing page", "status": "To Do", "team": "Technical Team", "assigned_to": "tech_member1", "created_by": "tech_lead", "created_at": time.time()}
    ],
    "announcements": [
        {"id":1, "title":"Welcome to DevCatalyst!", "body":"Kickoff meeting this Friday 5PM in Auditorium.", "author":"admin", "created_at": time.time()}
    ],
    "next_task_id": 4,
    "next_announcement_id": 2
}

def load_data():
    if DATA_FILE.exists():
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return DEFAULT.copy()
    return DEFAULT.copy()

def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception:
        # best-effort; permissions or ephemeral container might block.
        pass

# Initialize app data in session_state
if "data" not in st.session_state:
    st.session_state.data = load_data()
    # For interactive convenience, copy some frequently used views
    st.session_state.user = None

# ---------------- Auth (single login page) ----------------
def login(username, password):
    users = st.session_state.data["users"]
    user = users.get(username)
    if user and user["password"] == password:
        st.session_state.user = {"username": username, **user}
        return True
    return False

def logout():
    st.session_state.user = None
    st.experimental_rerun()

# Top layout: header with club description and logo if present
colL, colR = st.columns([1,3])
with colL:
    # show image if present in /mnt/data (developer uploaded earlier); else just emoji
    img_path = Path("/mnt/data/WhatsApp Image 2025-09-06 at 01.30.29_75baa112.jpg")
    if img_path.exists():
        st.image(str(img_path), width=110, caption="")
    else:
        st.markdown("<div style='font-size:48px'>🚀</div>", unsafe_allow_html=True)
with colR:
    st.markdown(f"<div class='header'><div class='club-title'>{st.session_state.data['club']['name']}</div></div>", unsafe_allow_html=True)
    st.markdown(f"<div class='small-muted'>{st.session_state.data['club']['description'].replace(chr(10),'<br>')}</div>", unsafe_allow_html=True)

st.markdown("---")

# If not logged in -> show login
if not st.session_state.user:
    st.markdown("<div class='card'><b>Login</b></div>", unsafe_allow_html=True)
    with st.form("login_form"):
        col1, col2 = st.columns([2,1])
        with col1:
            username = st.text_input("Username")
        with col2:
            password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign in")
        if submitted:
            if login(username.strip(), password.strip()):
                st.success("Signed in")
                save_data(st.session_state.data)
                st.experimental_rerun()
            else:
                st.error("Invalid credentials. (Try admin / 123 or the sample team accounts.)")
    st.stop()

# Logged in - determine role and team
user = st.session_state.user
role = user["role"]
user_team = user.get("team")

# Sidebar navigation per role
if role == "Admin":
    pages = ["Dashboard","Teams","Members","Projects","Events","Announcements","Export/Import","Settings","Sign out"]
elif role == "Team Lead":
    pages = ["Team Dashboard","Projects","Announcements","Sign out"]
else:
    pages = ["My Team","Projects","Announcements","Sign out"]

choice = st.sidebar.selectbox("Go to", pages)

st.sidebar.markdown(f"**Logged in as:** {user['username']}  \n**Role:** {role}  ")
if user_team:
    st.sidebar.markdown(f"**Team:** {user_team}")

# ---------- Helpers ----------
def new_task(title, desc, team, assigned_to, created_by):
    nid = st.session_state.data["next_task_id"]
    st.session_state.data["tasks"].append({
        "id": nid, "title": title, "desc": desc, "status": "To Do", "team": team,
        "assigned_to": assigned_to, "created_by": created_by, "created_at": time.time()
    })
    st.session_state.data["next_task_id"] += 1
    save_data(st.session_state.data)

def new_announcement(title, body, author):
    nid = st.session_state.data["next_announcement_id"]
    st.session_state.data["announcements"].insert(0, {"id": nid, "title": title, "body": body, "author": author, "created_at": time.time()})
    st.session_state.data["next_announcement_id"] += 1
    save_data(st.session_state.data)

def get_tasks_for_team(team_name):
    return [t for t in st.session_state.data["tasks"] if t["team"] == team_name]

def colored_status_html(status):
    cls = "status-todo" if status=="To Do" else ("status-progress" if status=="In Progress" else "status-done")
    return f"<span class='badge {cls}'>{status}</span>"

# ---------- Pages ----------
if choice == "Sign out":
    logout()

# Admin Dashboard
if choice == "Dashboard":
    st.header("Admin Control Deck")
    num_teams = len(st.session_state.data["teams"])
    num_users = len(st.session_state.data["users"])
    num_tasks = len(st.session_state.data["tasks"])
    col1, col2, col3 = st.columns(3)
    col1.metric("Teams", num_teams)
    col2.metric("Users", num_users)
    col3.metric("Tasks", num_tasks)

    st.subheader("Recent Announcements")
    for a in st.session_state.data["announcements"][:5]:
        st.markdown(f"**{a['title']}** — <span class='small-muted'>by {a['author']} · {datetime.fromtimestamp(a['created_at']).strftime('%Y-%m-%d %H:%M')}</span>", unsafe_allow_html=True)
        st.markdown(a['body'])

# Teams management (Admin)
if choice == "Teams":
    st.header("Teams — Manage")
    teams = st.session_state.data["teams"]
    colA, colB = st.columns([2,1])
    with colA:
        for team_name, info in teams.items():
            st.markdown(f"### {team_name}")
            st.markdown(f"Lead: **{info.get('lead') or '—'}**")
            st.markdown("Members: " + (", ".join(info.get("members",[])) or "—"))
            st.write("---")
    with colB:
        st.subheader("Create Team")
        with st.form("create_team"):
            tn = st.text_input("Team name")
            lead = st.text_input("Lead username (optional)")
            submitted = st.form_submit_button("Create")
            if submitted and tn:
                if tn in teams:
                    st.warning("Team already exists")
                else:
                    teams[tn] = {"lead": lead if lead else None, "members": [lead] if lead else []}
                    # also update users mapping if lead provided
                    if lead:
                        st.session_state.data["users"][lead] = {"password":"123", "role":"Team Lead", "team":tn}
                    save_data(st.session_state.data)
                    st.success(f"Created team {tn}")
                    st.experimental_rerun()

        st.subheader("Add Member")
        with st.form("add_member"):
            uname = st.text_input("Username")
            pwd = st.text_input("Password", value="123")
            role_sel = st.selectbox("Role", ["Member","Team Lead"])
            team_sel = st.selectbox("Team", list(teams.keys()))
            submitted2 = st.form_submit_button("Add Member")
            if submitted2 and uname:
                if uname in st.session_state.data["users"]:
                    st.warning("User exists")
                else:
                    st.session_state.data["users"][uname] = {"password":pwd, "role": role_sel if role_sel!="Member" else "Member", "team": team_sel}
                    teams[team_sel]["members"].append(uname)
                    if role_sel == "Team Lead":
                        teams[team_sel]["lead"] = uname
                    save_data(st.session_state.data)
                    st.success(f"Added {uname} to {team_sel}")
                    st.experimental_rerun()

# Members listing (Admin)
if choice == "Members":
    st.header("All Members")
    users = st.session_state.data["users"]
    rows = []
    for u, info in users.items():
        rows.append({"username": u, "role": info.get("role"), "team": info.get("team")})
    st.table(rows)

# Team Dashboard (Team Lead & Members)
if choice == "Team Dashboard" or choice == "My Team":
    # Determine which team to show
    if role == "Admin":
        team_to_show = st.selectbox("Select team", list(st.session_state.data["teams"].keys()))
    else:
        team_to_show = user_team

    st.header(f"Team Dashboard — {team_to_show}")
    team_info = st.session_state.data["teams"].get(team_to_show, {"lead":None,"members":[]})
    st.markdown(f"**Lead:** {team_info.get('lead')}")
    st.markdown(f"**Members:** {', '.join(team_info.get('members',[])) or '—'}")

    # Show tasks in Kanban columns
    statuses = ["To Do", "In Progress", "Done"]
    cols = st.columns(len(statuses))
    tasks = get_tasks_for_team(team_to_show)
    for idx, status in enumerate(statuses):
        with cols[idx]:
            st.subheader(status)
            for i, t in enumerate(tasks):
                if t["status"] == status:
                    st.markdown(f"<div class='task-card'><b>{t['title']}</b><br><span class='small-muted'>{t['desc']}</span><br>Assigned: <b>{t['assigned_to'] or '—'}</b> • {colored_status_html(t['status'])}</div>", unsafe_allow_html=True)
                    if role in ["Admin","Team Lead"]:
                        # status change control
                        new_status = st.selectbox(f"Move '{t['title']}'", statuses, index=statuses.index(status), key=f"move_{t['id']}")
                        if new_status != status:
                            # update
                            for task in st.session_state.data["tasks"]:
                                if task["id"] == t["id"]:
                                    task["status"] = new_status
                                    save_data(st.session_state.data)
                                    st.experimental_rerun()
                    if role in ["Admin","Team Lead"]:
                        # simple assign control
                        assignees = team_info.get("members", [])
                        if assignees:
                            new_assignee = st.selectbox(f"Assign '{t['title']}'", ["Unassigned"] + assignees, index=(assignees.index(t['assigned_to'])+1 if t['assigned_to'] in assignees else 0), key=f"assign_{t['id']}")
                            if new_assignee != (t['assigned_to'] or "Unassigned"):
                                for task in st.session_state.data["tasks"]:
                                    if task["id"] == t["id"]:
                                        task["assigned_to"] = (new_assignee if new_assignee != "Unassigned" else None)
                                        save_data(st.session_state.data)
                                        st.experimental_rerun()

    if role in ["Admin","Team Lead"]:
        st.subheader("Create Task for Team")
        with st.form("create_task"):
            ttitle = st.text_input("Title")
            tdesc = st.text_area("Description")
            tassign = st.selectbox("Assign to", ["Unassigned"] + team_info.get("members", []))
            submitted = st.form_submit_button("Create Task")
            if submitted and ttitle:
                new_task(ttitle, tdesc, team_to_show, (tassign if tassign!="Unassigned" else None), user["username"])
                st.success("Task created")
                st.experimental_rerun()

# Projects page (Admin & Team Lead & Member)
if choice == "Projects":
    st.header("Projects (Kanban-ish)")
    statuses = ["To Do", "In Progress", "Done"]
    cols = st.columns(len(statuses))
    projects = st.session_state.data["tasks"]  # using tasks as project tasks for demo
    for idx, status in enumerate(statuses):
        with cols[idx]:
            st.subheader(status)
            for t in projects:
                if t["status"] == status:
                    if role in ["Admin"]:
                        show_team = f" — {t.get('team')}"
                    else:
                        show_team = ""
                    st.markdown(f"- **{t['title']}**{show_team} _(assigned: {t.get('assigned_to') or '—'})_")

# Events
if choice == "Events":
    st.header("Events")
    st.table(st.session_state.data.get("events", [{"title":"Hackathon 2025","date":"2025-09-15"}]))

    if role in ["Admin","Team Lead"]:
        st.subheader("Create Event")
        with st.form("create_event"):
            et = st.text_input("Event title")
            ed = st.date_input("Date")
            sub = st.form_submit_button("Create")
            if sub and et:
                events = st.session_state.data.get("events", [])
                events.append({"title":et,"date":ed.isoformat()})
                st.session_state.data["events"] = events
                save_data(st.session_state.data)
                st.success("Event created")
                st.experimental_rerun()

# Announcements
if choice == "Announcements":
    st.header("Announcements / News")
    for a in st.session_state.data["announcements"]:
        st.markdown(f"**{a['title']}** — <span class='small-muted'>by {a['author']} • {datetime.fromtimestamp(a['created_at']).strftime('%Y-%m-%d %H:%M')}</span>", unsafe_allow_html=True)
        st.markdown(a['body'])
        st.write("---")

    if role in ["Admin","Team Lead"]:
        st.subheader("Post Announcement")
        with st.form("post_ann"):
            at = st.text_input("Title")
            ab = st.text_area("Message")
            sub = st.form_submit_button("Post")
            if sub and at:
                new_announcement(at, ab, user["username"])
                st.success("Announcement posted")
                st.experimental_rerun()

# Export/Import (Admin)
if choice == "Export/Import":
    st.header("Export / Import Data")
    if st.button("Export JSON"):
        st.download_button("Download JSON", json.dumps(st.session_state.data, indent=2), file_name="devcatalyst_data_export.json", mime="application/json")
    st.markdown("**Import (overwrite current data)**")
    uploaded = st.file_uploader("Upload JSON", type=["json"])
    if uploaded:
        try:
            newdata = json.load(uploaded)
            st.session_state.data = newdata
            save_data(st.session_state.data)
            st.success("Imported")
            st.experimental_rerun()
        except Exception as e:
            st.error("Invalid JSON")

# Settings (Admin)
if choice == "Settings":
    st.header("Settings")
    st.write("Demo settings — no external integrations configured.")
    if st.button("Reset demo data"):
        st.session_state.data = DEFAULT.copy()
        save_data(st.session_state.data)
        st.experimental_rerun()

# Save on every top-level render (best-effort)
save_data(st.session_state.data)
