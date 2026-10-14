
import streamlit as st
import sqlite3
import hashlib
import hmac
import os
import random

st.set_page_config(
    page_title="Little Minds",
    page_icon="🌈",
    layout="wide"
)

DB = "little_minds.db"

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#f4f8ff,#fff8fb);
    color: #25365f;
}
[data-testid="stSidebar"] {
    background: #eef2ff;
}
h1,h2,h3 {color:#493b91;}
.block-container {padding-top:1.5rem;max-width:1300px;}
div.stButton>button, div.stFormSubmitButton>button {
    background:#7658ed;color:white;border:0;
    border-radius:12px;min-height:42px;font-weight:800;
}
.hero {
    background:linear-gradient(110deg,#d7f2ff,#f1e5ff,#ffe4ef);
    border-radius:22px;padding:25px;text-align:center;
    border:1px solid #d9e9ff;margin-bottom:18px;
}
.hero h1 {font-size:42px;margin:0;}
.tile {
    border-radius:18px;padding:18px 10px;
    text-align:center;min-height:150px;margin-bottom:12px;
}
.pink {background:#ffd8e9;}
.green {background:#d8f8d0;}
.yellow {background:#fff0bd;}
.purple {background:#e8ddff;}
.panel {
    background:white;border:1px solid #dce8ff;
    border-radius:18px;padding:20px;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATABASE ----------
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

def save_score(game):
    with connect() as con:
        con.execute(
            "INSERT INTO scores(username,game) VALUES(?,?)",
            (st.session_state.user, game)
        )

if "user" not in st.session_state:
    st.session_state.user = None
if "question" not in st.session_state:
    st.session_state.question = None
if "feedback" not in st.session_state:
    st.session_state.feedback = None
if "admin_ok" not in st.session_state:
    st.session_state.admin_ok = False

# ---------- SIDEBAR ----------
with st.sidebar:
    st.markdown("<h1 style='text-align:center'>🎓 Little Minds</h1>",
                unsafe_allow_html=True)
    st.caption("Learn • Play • Grow")
    page = st.radio("Navigate", [
        "🏠 Home", "📝 Register", "🔐 Login",
        "🎮 Learning Games", "📊 My Dashboard",
        "🛡️ Admin Panel"
    ])
    st.divider()
    if st.session_state.user:
        st.success("Logged in")
        if st.button("Log out"):
            st.session_state.user = None
            st.rerun()
    else:
        st.info("👤 Guest")
    st.markdown("""
    <div style="background:#e5edff;padding:18px;
    border-radius:15px;text-align:center">
    ⭐ 🌈 ⭐<br><b>Small steps today,<br>
    big dreams tomorrow!</b>
    </div>
    """, unsafe_allow_html=True)

# ---------- HOME ----------
if page == "🏠 Home":
    st.markdown("""
    <div class="hero">
      <div style="font-size:35px">🌈 🦋 ☀️</div>
      <h1>Welcome to Little Minds!</h1>
      <h3>A fun learning platform for Nursery, LKG & UKG</h3>
      <div style="font-size:35px">🧒🏻 👧🏻 🎈</div>
    </div>
    """, unsafe_allow_html=True)

    cols = st.columns(4)
    cards = [
        ("🔤 ABC","Alphabet Adventure","Learn letters","pink"),
        ("🔢 123","Counting Garden","Count and grow","green"),
        ("🔴 🔺","Shapes & Colours","Explore the world","yellow"),
        ("🧠 ⭐","Memory Match","Train your memory","purple")
    ]
    for col, card in zip(cols, cards):
        with col:
            icon, title, desc, colour = card
            st.markdown(f"""
            <div class="tile {colour}">
            <h1>{icon}</h1><h3>{title}</h3><p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    a, b = st.columns(2)
    with a:
        st.markdown("""
        <div class="panel">
        <h3>🚀 Quick Start</h3>
        🟢 Create your student account<br><br>
        🔵 Choose your class<br><br>
        🟣 Play fun learning games<br><br>
        🟠 Track your progress ⭐
        </div>
        """, unsafe_allow_html=True)
    with b:
        st.markdown("""
        <div class="panel">
        <h3>🏆 Latest Highlights</h3>
        ✅ Colourful learning games<br><br>
        ✅ Personal progress dashboard<br><br>
        ✅ Fun questions for little learners<br><br>
        ✅ Celebrate every correct answer!
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        "<center>💜 Little Minds • Learn • Play • Grow</center>",
        unsafe_allow_html=True
    )

# ---------- REGISTER ----------
elif page == "📝 Register":
    st.markdown("""
    <div class="hero"><h1>🌟 Create Your Account</h1>
    <p>Ask a parent or guardian to help with registration.</p></div>
    """, unsafe_allow_html=True)

    with st.form("register"):
        name = st.text_input("Student name")
        username = st.text_input("Choose username").strip().lower()
        grade = st.selectbox(
            "Class", ["Play Group","Nursery","LKG","UKG"]
        )
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm password", type="password")
        approved = st.checkbox(
            "My parent/guardian has approved this account."
        )
        submit = st.form_submit_button("Create Account 🌈")

    if submit:
        if not name.strip() or len(username) < 3:
            st.error("Enter a name and username of at least 3 characters.")
        elif len(password) < 8:
            st.error("Password must have at least 8 characters.")
        elif password != confirm:
            st.error("Passwords do not match.")
        elif not approved:
            st.warning("Please ask your parent/guardian for approval.")
        else:
            salt = os.urandom(16).hex()
            try:
                with connect() as con:
                    con.execute("""
                        INSERT INTO students
                        VALUES(?,?,?,?,?)
                    """, (username, name.strip(), grade, salt,
                          make_hash(password, salt)))
                st.success("Account created! Now open Login.")
            except sqlite3.IntegrityError:
                st.error("That username is already taken.")

# ---------- LOGIN ----------
elif page == "🔐 Login":
    st.markdown("""
    <div class="hero"><h1>🐻 Welcome Back!</h1>
    <p>Continue your learning journey.</p></div>
    """, unsafe_allow_html=True)

    with st.form("login"):
        username = st.text_input("Username").strip().lower()
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login 🚀")

    if submit:
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
            st.rerun()
        else:
            st.error("Incorrect username or password.")

# ---------- GAMES ----------
elif page == "🎮 Learning Games":
    st.markdown("""
    <div class="hero"><h1>🎮 Learning Adventures</h1>
    <p>Every question is a new little victory!</p></div>
    """, unsafe_allow_html=True)

    if not st.session_state.user:
        st.info("Please login first to save your scores.")
    else:
        game = st.selectbox("Choose a game", [
            "Colour Quest", "Shape Safari",
            "Counting Garden", "Alphabet Adventure"
        ])

        if (st.session_state.question is None or
            st.session_state.question["game"] != game):
            if game == "Colour Quest":
                q = ("What colour is a ripe banana? 🍌",
                     ["Blue","Yellow","Purple","Green"], "Yellow")
            elif game == "Shape Safari":
                q = ("Which shape has three sides? 🔺",
                     ["Circle","Triangle","Square"], "Triangle")
            elif game == "Alphabet Adventure":
                q = ("Which letter comes after B?",
                     ["A","C","D","E"], "C")
            else:
                n = random.randint(2,8)
                q = (f"Count the flowers: {'🌼 ' * n}",
                     [str(i) for i in range(1,10)], str(n))

            st.session_state.question = {
                "game": game, "prompt": q[0],
                "options": q[1], "answer": q[2]
            }
            st.session_state.feedback = None

        q = st.session_state.question
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.subheader(q["prompt"])
        answer = st.radio("Choose your answer:", q["options"])

        if st.button("Check Answer ⭐"):
            if answer == q["answer"]:
                save_score(game)
                st.session_state.feedback = "correct"
            else:
                st.session_state.feedback = "try"

        if st.session_state.feedback == "correct":
            st.success("Correct! Great job! 🎉")
            if st.button("Next Question ➜"):
                st.session_state.question = None
                st.session_state.feedback = None
                st.rerun()
        elif st.session_state.feedback == "try":
            st.warning("Good try! Have another go.")

        st.markdown("</div>", unsafe_allow_html=True)

# ---------- DASHBOARD ----------
elif page == "📊 My Dashboard":
    st.markdown("""
    <div class="hero"><h1>📊 My Learning Dashboard</h1>
    <p>Look how much you have learned!</p></div>
    """, unsafe_allow_html=True)

    if not st.session_state.user:
        st.info("Login to see your progress.")
    else:
        with connect() as con:
            student = con.execute(
                "SELECT name,grade FROM students WHERE username=?",
                (st.session_state.user,)
            ).fetchone()
            scores = con.execute("""
                SELECT game,SUM(points) FROM scores
                WHERE username=? GROUP BY game
            """, (st.session_state.user,)).fetchall()

        if student:
            st.subheader(f"👋 Hello, {student[0]}!")
            st.write("Class:", student[1])
            total = sum(points for _, points in scores)
            a, b = st.columns(2)
            a.metric("Correct Answers ⭐", total)
            b.metric("Games Played 🎮", len(scores))

            st.subheader("🌱 Your Game Progress")
            if scores:
                for game, points in scores:
                    st.info(f"🎯 {game}: {points} points")
            else:
                st.write("Play a game to start earning points!")

# ---------- ADMIN ----------
elif page == "🛡️ Admin Panel":
    st.markdown("""
    <div class="hero"><h1>🛡️ Admin Panel</h1>
    <p>Review student accounts and game scores.</p></div>
    """, unsafe_allow_html=True)

    admin_password = os.environ.get("LITTLE_MINDS_ADMIN_PASSWORD")
    if not admin_password:
        st.warning(
            "Admin is not configured. Ask a trusted adult to set "
            "LITTLE_MINDS_ADMIN_PASSWORD before using this panel."
        )
    else:
        entered = st.text_input("Admin password", type="password")
        if st.button("Unlock Admin Panel"):
            st.session_state.admin_ok = hmac.compare_digest(
                entered, admin_password
            )
            if not st.session_state.admin_ok:
                st.error("Incorrect admin password.")

        if st.session_state.admin_ok:
            with connect() as con:
                students = con.execute(
                    "SELECT username,name,grade FROM students"
                ).fetchall()
                scores = con.execute("""
                    SELECT username,game,SUM(points)
                    FROM scores GROUP BY username,game
                """).fetchall()

            st.subheader("👩‍🎓 Registered Students")
            st.dataframe(students, use_container_width=True)
            st.subheader("🎮 Game Scores")
            st.dataframe(scores, use_container_width=True)

            csv_text = "username,game,points\n"
            csv_text += "\n".join(
                f"{u},{g},{p}" for u,g,p in scores
            )
            st.download_button(
                "⬇️ Download Scores CSV",
                csv_text,
                "little_minds_scores.csv",
                "text/csv"
            )

st.divider()
st.caption("🌈 Little Minds — Small steps, big discoveries!")
