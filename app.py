
import streamlit as st
import sqlite3
import hashlib
import hmac
import os
import random
import csv
import io

st.set_page_config(
    page_title="Little Minds",
    page_icon="🌈",
    layout="wide"
)

DB = "little_minds.db"

# ========== DESIGN ==========
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#f4f8ff,#fff8fb,#fffdf3);
    color: #25365f;
}
[data-testid="stSidebar"] {background:#eef2ff;}
.block-container {max-width:1350px;padding-top:1.3rem;}
h1,h2,h3 {color:#493b91;font-weight:900;}
div.stButton>button,div.stFormSubmitButton>button {
    background:#7658ed;color:white;border:0;
    border-radius:13px;min-height:42px;font-weight:800;
}
.hero {
    background:linear-gradient(110deg,#d7f2ff,#f1e5ff,#ffe4ef);
    border-radius:24px;padding:25px;text-align:center;
    border:1px solid #d9e9ff;margin-bottom:20px;
}
.hero h1 {font-size:clamp(30px,4vw,46px);margin:0;}
.tile {
    border-radius:20px;padding:18px 10px;
    min-height:150px;text-align:center;margin-bottom:12px;
}
.tile h2 {font-size:34px;margin:0 0 5px;}
.tile h3 {font-size:17px;color:#293b6d;}
.pink {background:#ffd8e9;}
.green {background:#d8f8d0;}
.yellow {background:#fff0bd;}
.purple {background:#e8ddff;}
.panel {
    background:white;border:1px solid #dce8ff;
    border-radius:18px;padding:20px;
}
.pill {
    background:#eef4ff;border-radius:13px;
    padding:13px 15px;margin:7px 0;
}
div[data-testid="stMetric"] {
    background:white;border:1px solid #dce8ff;
    border-radius:16px;padding:14px;
}
</style>
""", unsafe_allow_html=True)


# ========== DATABASE ==========
def connect():
    return sqlite3.connect(DB, timeout=10)

with connect() as con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS students(
            username TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            grade TEXT NOT NULL,
            salt TEXT NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS scores(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            game TEXT NOT NULL,
            points INTEGER DEFAULT 1
        )
    """)

def make_hash(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt.encode(), 200000
    ).hex()

def get_student(username):
    with connect() as con:
        return con.execute(
            "SELECT username,name,grade FROM students WHERE username=?",
            (username,)
        ).fetchone()

def save_score(username, game):
    with connect() as con:
        con.execute(
            "INSERT INTO scores(username,game,points) VALUES(?,?,1)",
            (username, game)
        )

def get_scores(username):
    with connect() as con:
        return con.execute("""
            SELECT game,SUM(points) FROM scores
            WHERE username=? GROUP BY game ORDER BY game
        """, (username,)).fetchall()


# ========== SESSION ==========
for key, default in {
    "user": None,
    "question": None,
    "feedback": None,
    "admin_ok": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ========== LOGIN / REGISTER ==========
# Logged out users see ONLY this page.
if not st.session_state.user:
    st.markdown("""
    <div class="hero">
        <div style="font-size:38px">🌈 🦋 🎈</div>
        <h1>Welcome to Little Minds!</h1>
        <p>A happy place to learn, play and grow.</p>
        <div style="font-size:34px">🧒🏻 👧🏻 ⭐</div>
    </div>
    """, unsafe_allow_html=True)

    login_tab, register_tab = st.tabs(
        ["🔐 Login", "✨ Create Account"]
    )

    with login_tab:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Welcome Back!")

        with st.form("login_form"):
            username = st.text_input("Username").strip().lower()
            password = st.text_input("Password", type="password")
            login = st.form_submit_button(
                "Login 🚀", use_container_width=True
            )

        if login:
            with connect() as con:
                row = con.execute(
                    "SELECT salt,password_hash FROM students WHERE username=?",
                    (username,)
                ).fetchone()

            if row and hmac.compare_digest(
                make_hash(password, row[0]), row[1]
            ):
                st.session_state.user = username
                st.session_state.question = None
                st.session_state.feedback = None
                st.rerun()
            else:
                st.error("Username ya password galat hai.")

        st.markdown("</div>", unsafe_allow_html=True)

    with register_tab:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader("Create Your Account 🌟")

        with st.form("register_form"):
            name = st.text_input("Student name")
            new_user = st.text_input("Choose username").strip().lower()
            grade = st.selectbox(
                "Choose class",
                ["Play Group", "Nursery", "LKG", "UKG"]
            )
            new_password = st.text_input(
                "Create password (8+ characters)", type="password"
            )
            confirm = st.text_input("Confirm password", type="password")
            guardian = st.checkbox(
                "My parent/guardian has approved this account."
            )
            create = st.form_submit_button(
                "Create Account 🌈", use_container_width=True
            )

        if create:
            if not name.strip() or len(new_user) < 3:
                st.error("Name aur 3+ character username enter karo.")
            elif len(new_password) < 8:
                st.error("Password kam se kam 8 characters ka hona chahiye.")
            elif new_password != confirm:
                st.error("Passwords match nahi karte.")
            elif not guardian:
                st.warning("Parent/guardian se permission lo.")
            else:
                salt = os.urandom(16).hex()
                try:
                    with connect() as con:
                        con.execute("""
                            INSERT INTO students
                            (username,name,grade,salt,password_hash)
                            VALUES(?,?,?,?,?)
                        """, (
                            new_user, name.strip(), grade, salt,
                            make_hash(new_password, salt)
                        ))
                    st.success(
                        "Account ban gaya! Ab Login tab se sign in karo."
                    )
                except sqlite3.IntegrityError:
                    st.error("Ye username pehle se use ho raha hai.")

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<center>💜 Little Minds • Learn • Play • Grow</center>",
        unsafe_allow_html=True
    )

# ========== LOGGED-IN WEBSITE ==========
else:
    with st.sidebar:
        st.markdown(
            "<h1 style='text-align:center'>🎓 Little Minds</h1>",
            unsafe_allow_html=True
        )
        st.caption("Learn • Play • Grow")

        student = get_student(st.session_state.user)
        if student:
            st.success(f"Hello, {student[1]}!")
            st.caption(f"Class: {student[2]}")

        page = st.radio("Navigate", [
            "🏠 Home",
            "🎮 Learning Games",
            "📊 My Dashboard",
            "🛡️ Admin Panel"
        ])

        st.divider()
        if st.button("Log out", use_container_width=True):
            st.session_state.user = None
            st.session_state.question = None
            st.session_state.feedback = None
            st.session_state.admin_ok = False
            st.rerun()

        st.markdown("""
        <div style="background:#e5edff;padding:16px;
        border-radius:15px;text-align:center">
        ⭐ 🌈 ⭐<br><b>Small steps today,<br>
        big dreams tomorrow!</b>
        </div>
        """, unsafe_allow_html=True)

    # ========== HOME ==========
    if page == "🏠 Home":
        student = get_student(st.session_state.user)
        name = student[1] if student else "Learner"

        st.markdown(f"""
        <div class="hero">
            <div style="font-size:36px">🌈 🦋 ☀️</div>
            <h1>Welcome back, {name}!</h1>
            <p>Your colourful learning adventure starts here.</p>
            <div style="font-size:32px">🧒🏻 👧🏻 🎈</div>
        </div>
        """, unsafe_allow_html=True)

        cards = [
            ("🔤 ABC", "Alphabet Adventure", "Discover letters!", "pink"),
            ("🔢 123", "Counting Garden", "Count and grow!", "green"),
            ("🔴 🔺", "Shapes & Colours", "Explore the world!", "yellow"),
            ("🧠 ⭐", "Memory Match", "Train your memory!", "purple")
        ]

        cols = st.columns(4)
        for col, (icon, title, desc, colour) in zip(cols, cards):
            with col:
                st.markdown(f"""
                <div class="tile {colour}">
                    <h2>{icon}</h2>
                    <h3>{title}</h3>
                    <p>{desc}</p>
                </div>
                """, unsafe_allow_html=True)

        left, right = st.columns(2)
        with left:
            st.markdown("""
            <div class="panel">
            <h3>🚀 Quick Start</h3>
            🟢 Choose a learning game<br><br>
            🔵 Answer fun questions<br><br>
            🟣 Earn points<br><br>
            🟠 Track your progress
            </div>
            """, unsafe_allow_html=True)

        with right:
            st.markdown("""
            <div class="panel">
            <h3>🏆 Learning Highlights</h3>
            ✅ Colourful learning activities<br><br>
            ✅ Personal progress dashboard<br><br>
            ✅ Fun questions for little learners<br><br>
            ✅ Celebrate every correct answer!
            </div>
            """, unsafe_allow_html=True)

    # ========== GAMES ==========
    elif page == "🎮 Learning Games":
        st.markdown("""
        <div class="hero">
            <div style="font-size:36px">🎮 🌟 🎨</div>
            <h1>Learning Adventures</h1>
            <p>Every question is a new little victory!</p>
        </div>
        """, unsafe_allow_html=True)

        game = st.selectbox("Choose your adventure", [
            "Colour Quest", "Shape Safari",
            "Counting Garden", "Alphabet Adventure"
        ])

        if (st.session_state.question is None or
            st.session_state.question.get("game") != game):

            if game == "Colour Quest":
                q = {
                    "prompt": "What colour is a ripe banana? 🍌",
                    "options": ["Blue", "Yellow", "Purple", "Green"],
                    "answer": "Yellow"
                }
            elif game == "Shape Safari":
                q = {
                    "prompt": "Which shape has three sides? 🔺",
                    "options": ["Circle", "Triangle", "Square", "Rectangle"],
                    "answer": "Triangle"
                }
            elif game == "Alphabet Adventure":
                q = {
                    "prompt": "Which letter comes after B?",
                    "options": ["A", "C", "D", "E"],
                    "answer": "C"
                }
            else:
                number = random.randint(2, 8)
                q = {
                    "prompt": f"Count the flowers: {' '.join(['🌼'] * number)}",
                    "options": [str(n) for n in range(1, 10)],
                    "answer": str(number)
                }

            q["game"] = game
            st.session_state.question = q
            st.session_state.feedback = None

        q = st.session_state.question
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader(q["prompt"])
        answer = st.radio(
            "Choose your answer:",
            q["options"],
            horizontal=True,
            key=f"answer_{game}"
        )

        if st.button("Check Answer ⭐"):
            if answer == q["answer"]:
                save_score(st.session_state.user, game)
                st.session_state.feedback = "correct"
            else:
                st.session_state.feedback = "try"

        if st.session_state.feedback == "correct":
            st.success("Correct! Amazing job! 🎉")
            if st.button("Next Question ➜"):
                st.session_state.question = None
                st.session_state.feedback = None
                st.rerun()
        elif st.session_state.feedback == "try":
            st.warning("Good try! Have another go.")

        st.markdown("</div>", unsafe_allow_html=True)

    # ========== DASHBOARD ==========
    elif page == "📊 My Dashboard":
        st.markdown("""
        <div class="hero">
            <div style="font-size:35px">📊 ⭐ 🏆</div>
            <h1>My Learning Dashboard</h1>
            <p>Look how much you have learned!</p>
        </div>
        """, unsafe_allow_html=True)

        student = get_student(st.session_state.user)
        if student:
            _, name, grade = student
            scores = get_scores(st.session_state.user)
            total = sum(points for _, points in scores)

            st.subheader(f"👋 Hello, {name}!")
            st.write(f"**Your class:** {grade}")

            a, b = st.columns(2)
            a.metric("Correct Answers ⭐", total)
            b.metric("Games With Scores 🎮", len(scores))

            st.subheader("🌱 Your Game Progress")
            if scores:
                for game_name, points in scores:
                    st.markdown(
                        f"<div class='pill'><b>🎯 {game_name}</b>"
                        f"<span style='float:right;color:#7558db;font-weight:900'>"
                        f"{points} points</span></div>",
                        unsafe_allow_html=True
                    )
            else:
                st.info("Play your first game to start earning points!")

    # ========== ADMIN ==========
    elif page == "🛡️ Admin Panel":
        st.markdown("""
        <div class="hero">
            <div style="font-size:35px">🛡️ 📋 ⭐</div>
            <h1>Admin Panel</h1>
            <p>Review student accounts and learning scores.</p>
        </div>
        """, unsafe_allow_html=True)

        admin_password = os.environ.get("LITTLE_MINDS_ADMIN_PASSWORD")

        if not admin_password:
            st.warning(
                "Admin is not configured. Ask a trusted adult to set "
                "LITTLE_MINDS_ADMIN_PASSWORD before using this panel."
            )
        else:
            with st.form("admin_login"):
                entered = st.text_input("Admin password", type="password")
                unlock = st.form_submit_button("Unlock Admin Panel")

            if unlock:
                st.session_state.admin_ok = hmac.compare_digest(
                    entered, admin_password
                )
                if not st.session_state.admin_ok:
                    st.error("Incorrect admin password.")

            if st.session_state.admin_ok:
                with connect() as con:
                    students = con.execute("""
                        SELECT username,name,grade
                        FROM students ORDER BY name
                    """).fetchall()
                    scores = con.execute("""
                        SELECT username,game,SUM(points) AS points
                        FROM scores GROUP BY username,game
                        ORDER BY username,game
                    """).fetchall()

                a, b = st.columns(2)
                a.metric("Registered Students", len(students))
                b.metric("Correct Answers Logged",
                         sum(row[2] for row in scores))

                st.subheader("👩‍🎓 Registered Students")
                st.dataframe(students, use_container_width=True)

                st.subheader("🎮 Game Scores")
                st.dataframe(scores, use_container_width=True)

                output = io.StringIO()
                writer = csv.writer(output)
                writer.writerow(["username", "game", "points"])
                writer.writerows(scores)

                st.download_button(
                    "⬇️ Download Scores CSV",
                    output.getvalue(),
                    "little_minds_scores.csv",
                    "text/csv"
                )

st.divider()
st.caption("🌈 Little Minds — Small steps, big discoveries!")
