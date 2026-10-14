import streamlit as st
import sqlite3
import hashlib
import hmac
import os
import random
import csv
import io
import html
from pathlib import Path

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Little Minds",
    page_icon="🌈",
    layout="wide"
)

DB = str(Path(_file_).resolve().parent / "little_minds.db")


# =====================================================
# DESIGN
# =====================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(
        135deg, #f4f8ff, #fff8fb, #fffdf3
    );
    color: #25365f;
}

[data-testid="stSidebar"] {
    background: #eef2ff;
}

.block-container {
    max-width: 1350px;
    padding-top: 1.3rem;
}

h1, h2, h3 {
    color: #493b91;
    font-weight: 900;
}

div.stButton > button,
div.stFormSubmitButton > button {
    background: #7658ed;
    color: white;
    border: 0;
    border-radius: 13px;
    min-height: 42px;
    font-weight: 800;
}

.hero {
    background: linear-gradient(
        110deg, #d7f2ff, #f1e5ff, #ffe4ef
    );
    border-radius: 24px;
    padding: 25px;
    text-align: center;
    border: 1px solid #d9e9ff;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: clamp(30px, 4vw, 46px);
    margin: 0;
}

.tile {
    border-radius: 20px;
    padding: 18px 10px;
    min-height: 150px;
    text-align: center;
    margin-bottom: 12px;
}

.tile h2 {
    font-size: 34px;
    margin: 0 0 5px;
}

.tile h3 {
    font-size: 17px;
    color: #293b6d;
}

.pink {
    background: #ffd8e9;
}

.green {
    background: #d8f8d0;
}

.yellow {
    background: #fff0bd;
}

.purple {
    background: #e8ddff;
}

.panel {
    background: white;
    border: 1px solid #dce8ff;
    border-radius: 18px;
    padding: 20px;
}

.pill {
    background: #eef4ff;
    border-radius: 13px;
    padding: 13px 15px;
    margin: 7px 0;
}

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #dce8ff;
    border-radius: 16px;
    padding: 14px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# DATABASE CONNECTION
# =====================================================

def connect():
    con = sqlite3.connect(
        DB,
        timeout=15
    )
    con.execute("PRAGMA busy_timeout = 15000")
    return con


# =====================================================
# DATABASE SETUP AND MIGRATION
# =====================================================

def setup_database():
    with connect() as con:

        # Create the students table if it does not exist.
        con.execute("""
            CREATE TABLE IF NOT EXISTS students (
                username TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                grade TEXT NOT NULL,
                salt TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        # Read the existing columns.
        columns = {
            row[1]
            for row in con.execute(
                "PRAGMA table_info(students)"
            ).fetchall()
        }

        # Support the older version of the project.
        # Missing columns are added without dropping the table.
        optional_columns = {
            "name": "TEXT",
            "grade": "TEXT",
            "salt": "TEXT",
            "password_hash": "TEXT",
            "email": "TEXT",
            "guardian_email": "TEXT",
            "created_at": "TEXT"
        }

        for column, data_type in optional_columns.items():
            if column not in columns:
                con.execute(
                    f"ALTER TABLE students "
                    f"ADD COLUMN {column} {data_type}"
                )

        # Scores table.
        con.execute("""
            CREATE TABLE IF NOT EXISTS scores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                game TEXT NOT NULL,
                points INTEGER DEFAULT 1,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        score_columns = {
            row[1]
            for row in con.execute(
                "PRAGMA table_info(scores)"
            ).fetchall()
        }

        if "created_at" not in score_columns:
            con.execute("""
                ALTER TABLE scores
                ADD COLUMN created_at TEXT
            """)

        con.execute("""
            CREATE INDEX IF NOT EXISTS idx_scores_username
            ON scores(username)
        """)


try:
    setup_database()
except sqlite3.Error:
    st.error(
        "Database setup nahi ho saka. "
        "Database file aur permissions check karo."
    )
    st.stop()


# =====================================================
# PASSWORD SECURITY
# =====================================================

def make_hash(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        200000
    ).hex()


# =====================================================
# STUDENT FUNCTIONS
# =====================================================

def get_student(username):
    with connect() as con:
        return con.execute("""
            SELECT username, name, grade
            FROM students
            WHERE username = ?
        """, (username,)).fetchone()


def register_student(username, name, grade, password):
    salt = os.urandom(16).hex()
    password_hash = make_hash(password, salt)

    with connect() as con:
        con.execute("""
            INSERT INTO students
            (username, name, grade, salt, password_hash)
            VALUES (?, ?, ?, ?, ?)
        """, (
            username,
            name,
            grade,
            salt,
            password_hash
        ))


def verify_login(username, password):
    with connect() as con:
        row = con.execute("""
            SELECT salt, password_hash
            FROM students
            WHERE username = ?
        """, (username,)).fetchone()

    if not row:
        return False

    salt, saved_hash = row
    entered_hash = make_hash(password, salt)

    return hmac.compare_digest(
        entered_hash,
        saved_hash
    )


# =====================================================
# SCORE FUNCTIONS
# =====================================================

def save_score(username, game):
    with connect() as con:
        con.execute("""
            INSERT INTO scores
            (username, game, points)
            VALUES (?, ?, 1)
        """, (username, game))


def get_scores(username):
    with connect() as con:
        return con.execute("""
            SELECT game, SUM(points)
            FROM scores
            WHERE username = ?
            GROUP BY game
            ORDER BY game
        """, (username,)).fetchall()


def get_total_points(username):
    with connect() as con:
        result = con.execute("""
            SELECT COALESCE(SUM(points), 0)
            FROM scores
            WHERE username = ?
        """, (username,)).fetchone()

    return result[0]


# =====================================================
# SESSION STATE
# =====================================================

defaults = {
    "user": None,
    "question": None,
    "feedback": None,
    "answered": False,
    "admin_ok": False,
    "admin_password_checked": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =====================================================
# LOGOUT-SAFE HELPER
# =====================================================

def reset_game():
    st.session_state.question = None
    st.session_state.feedback = None
    st.session_state.answered = False


# =====================================================
# LOGIN AND REGISTRATION
# =====================================================

if not st.session_state.user:

    st.markdown("""
    <div class="hero">
        <div style="font-size:38px">🌈 🦋 🎈</div>
        <h1>Welcome to Little Minds!</h1>
        <p>A happy place to learn, play and grow.</p>
        <div style="font-size:34px">🧒🏻 👧🏻 ⭐</div>
    </div>
    """, unsafe_allow_html=True)

    login_tab, register_tab = st.tabs([
        "🔐 Login",
        "✨ Create Account"
    ])

    # ---------------- LOGIN ----------------

    with login_tab:

        st.subheader("Welcome Back!")

        with st.form("login_form"):

            username = st.text_input(
                "Username"
            ).strip().lower()

            password = st.text_input(
                "Password",
                type="password"
            )

            login = st.form_submit_button(
                "Login 🚀",
                use_container_width=True
            )

        if login:

            if not username or not password:
                st.error("Username aur password enter karo.")

            elif verify_login(username, password):

                st.session_state.user = username
                st.session_state.admin_ok = False
                reset_game()
                st.rerun()

            else:
                st.error("Username ya password galat hai.")

    # ---------------- REGISTRATION ----------------

    with register_tab:

        st.subheader("Create Your Account 🌟")

        st.info(
            "Bachchon ke account ke liye parent/guardian "
            "ki permission zaroori hai."
        )

        with st.form("register_form"):

            name = st.text_input(
                "Student name"
            )

            new_user = st.text_input(
                "Choose username"
            ).strip().lower()

            grade = st.selectbox(
                "Choose class",
                [
                    "Play Group",
                    "Nursery",
                    "LKG",
                    "UKG"
                ]
            )

            new_password = st.text_input(
                "Create password (8+ characters)",
                type="password"
            )

            confirm = st.text_input(
                "Confirm password",
                type="password"
            )

            guardian = st.checkbox(
                "My parent/guardian has approved this account."
            )

            create = st.form_submit_button(
                "Create Account 🌈",
                use_container_width=True
            )

        if create:

            if not name.strip():
                st.error("Student name enter karo.")

            elif len(new_user) < 3:
                st.error(
                    "Username kam se kam 3 characters ka hona chahiye."
                )

            elif not all(
                char.isalnum() or char in "_-."
                for char in new_user
            ):
                st.error(
                    "Username mein letters, numbers, _, - ya . use karo."
                )

            elif len(new_password) < 8:
                st.error(
                    "Password kam se kam 8 characters ka hona chahiye."
                )

            elif new_password != confirm:
                st.error("Passwords match nahi karte.")

            elif not guardian:
                st.warning(
                    "Parent/guardian se permission lo."
                )

            else:
                try:
                    register_student(
                        new_user,
                        name.strip(),
                        grade,
                        new_password
                    )

                    st.success(
                        "Account ban gaya! Ab Login tab se sign in karo."
                    )

                except sqlite3.IntegrityError:
                    st.error(
                        "Ye username pehle se use ho raha hai."
                    )

                except sqlite3.Error:
                    st.error(
                        "Account create nahi ho saka. "
                        "Database configuration check karo."
                    )

    st.markdown(
        "<center>💜 Little Minds • Learn • Play • Grow</center>",
        unsafe_allow_html=True
    )


# =====================================================
# LOGGED-IN WEBSITE
# =====================================================

else:

    student = get_student(st.session_state.user)

    # If the account no longer exists, log out safely.
    if student is None:
        st.session_state.user = None
        st.rerun()

    with st.sidebar:

        st.markdown(
            "<h1 style='text-align:center'>🎓 Little Minds</h1>",
            unsafe_allow_html=True
        )

        st.caption("Learn • Play • Grow")

        st.success(f"Hello, {student[1]}!")
        st.caption(f"Class: {student[2]}")

        page = st.radio(
            "Navigate",
            [
                "🏠 Home",
                "🎮 Learning Games",
                "📊 My Dashboard",
                "🛡️ Admin Panel"
            ]
        )

        st.divider()

        if st.button(
            "Log out",
            use_container_width=True
        ):
            st.session_state.user = None
            st.session_state.admin_ok = False
            st.session_state.admin_password_checked = False
            reset_game()
            st.rerun()

        st.markdown("""
        <div style="
            background:#e5edff;
            padding:16px;
            border-radius:15px;
            text-align:center">
            ⭐ 🌈 ⭐<br>
            <b>Small steps today,<br>
            big dreams tomorrow!</b>
        </div>
        """, unsafe_allow_html=True)

    # =================================================
    # HOME
    # =================================================

    if page == "🏠 Home":

        safe_name = html.escape(student[1])

        st.markdown(f"""
        <div class="hero">
            <div style="font-size:36px">🌈 🦋 ☀️</div>
            <h1>Welcome back, {safe_name}!</h1>
            <p>Your colourful learning adventure starts here.</p>
            <div style="font-size:32px">🧒🏻 👧🏻 🎈</div>
        </div>
        """, unsafe_allow_html=True)

        cards = [
            (
                "🔤 ABC",
                "Alphabet Adventure",
                "Discover letters!",
                "pink"
            ),
            (
                "🔢 123",
                "Counting Garden",
                "Count and grow!",
                "green"
            ),
            (
                "🔴 🔺",
                "Shapes & Colours",
                "Explore the world!",
                "yellow"
            ),
            (
                "🧠 ⭐",
                "Memory Match",
                "Train your memory!",
                "purple"
            )
        ]

        cols = st.columns(4)

        for col, (icon, title, desc, colour) in zip(
            cols, cards
        ):
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

    # =================================================
    # LEARNING GAMES
    # =================================================

    elif page == "🎮 Learning Games":

        st.markdown("""
        <div class="hero">
            <div style="font-size:36px">🎮 🌟 🎨</div>
            <h1>Learning Adventures</h1>
            <p>Every question is a new little victory!</p>
        </div>
        """, unsafe_allow_html=True)

        game = st.selectbox(
            "Choose your adventure",
            [
                "Colour Quest",
                "Shape Safari",
                "Counting Garden",
                "Alphabet Adventure"
            ],
            key="selected_game"
        )

        # Generate a question only when the game changes
        # or the student requests the next question.
        if (
            st.session_state.question is None
            or st.session_state.question.get("game") != game
        ):

            if game == "Colour Quest":

                q = {
                    "prompt": "What colour is a ripe banana? 🍌",
                    "options": [
                        "Blue",
                        "Yellow",
                        "Purple",
                        "Green"
                    ],
                    "answer": "Yellow"
                }

            elif game == "Shape Safari":

                q = {
                    "prompt": "Which shape has three sides? 🔺",
                    "options": [
                        "Circle",
                        "Triangle",
                        "Square",
                        "Rectangle"
                    ],
                    "answer": "Triangle"
                }

            elif game == "Alphabet Adventure":

                q = {
                    "prompt": "Which letter comes after B?",
                    "options": [
                        "A",
                        "C",
                        "D",
                        "E"
                    ],
                    "answer": "C"
                }

            else:

                number = random.randint(2, 8)

                q = {
                    "prompt": (
                        f"Count the flowers: "
                        f"{' '.join(['🌼'] * number)}"
                    ),
                    "options": [
                        str(n) for n in range(1, 10)
                    ],
                    "answer": str(number)
                }

            q["game"] = game

            st.session_state.question = q
            st.session_state.feedback = None
            st.session_state.answered = False

        q = st.session_state.question

        st.markdown('<div class="panel">', unsafe_allow_html=True)

        st.subheader(q["prompt"])

        answer = st.radio(
            "Choose your answer:",
            q["options"],
            horizontal=True,
            key=f"answer_{game}_{q['prompt']}"
        )

        # Award a point only once per question.
        if st.button(
            "Check Answer ⭐",
            disabled=st.session_state.answered
        ):

            st.session_state.answered = True

            if answer == q["answer"]:

                try:
                    save_score(
                        st.session_state.user,
                        game
                    )
                    st.session_state.feedback = "correct"

                except sqlite3.Error:
                    st.session_state.feedback = "database_error"

            else:
                st.session_state.feedback = "try"

            st.rerun()

        if st.session_state.feedback == "correct":

            st.success("Correct! Amazing job! 🎉")

            if st.button("Next Question ➜"):
                reset_game()
                st.rerun()

        elif st.session_state.feedback == "try":

            st.warning(
                "Good try! Click Next Questio
