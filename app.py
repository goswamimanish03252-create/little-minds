
import streamlit as st
import sqlite3
import hashlib
import secrets
import hmac
import os
import random
import csv
import io
from datetime import datetime

# ==========================================
# LITTLE MINDS - COMPLETE SINGLE FILE APP
# ==========================================

st.set_page_config(
    page_title="Little Minds",
    page_icon="🌈",
    layout="wide"
)

DB = "little_minds.db"

COLORS = {
    "RED": "#EF4444",
    "BLUE": "#3B82F6",
    "GREEN": "#22C55E",
    "YELLOW": "#FACC15",
    "PURPLE": "#A855F7",
    "ORANGE": "#F97316"
}

SHAPES = {
    "CIRCLE": "🔵",
    "SQUARE": "🟦",
    "TRIANGLE": "🔺",
    "STAR": "⭐"
}

ANIMALS = ["🐶", "🐱", "🐸", "🦊"]

# ==========================================
# DATABASE SETUP
# ==========================================

def database():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def setup_database():
    with database() as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            class_name TEXT NOT NULL,
            guardian_email TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)

        con.execute("""
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            game TEXT NOT NULL,
            score INTEGER NOT NULL,
            played_at TEXT NOT NULL,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
        """)


setup_database()

# ==========================================
# PASSWORD SECURITY
# ==========================================

def hash_password(password, salt=None):
    salt = salt or secrets.token_bytes(16)

    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode(),
        salt,
        200000
    )

    return hashed.hex(), salt.hex()


def verify_password(password, saved_hash, salt_hex):
    calculated, _ = hash_password(
        password,
        bytes.fromhex(salt_hex)
    )

    return hmac.compare_digest(calculated, saved_hash)


# ==========================================
# SESSION STATE
# ==========================================

defaults = {
    "student": None,
    "admin": False,
    "page": "Home",
    "colour_target": "YELLOW",
    "shape_target": "CIRCLE",
    "count_target": 3,
    "memory_cards": [],
    "memory_target": None,
    "memory_found": [],
    "memory_score_saved": False
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ==========================================
# SAVE STUDENT PROGRESS
# ==========================================

def save_score(game, points=1):
    student = st.session_state.student

    if student is None:
        return

    with database() as con:
        con.execute("""
        INSERT INTO scores
        (student_id, game, score, played_at)
        VALUES (?, ?, ?, ?)
        """, (
            student["id"],
            game,
            points,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))


# ==========================================
# WEBSITE STYLE
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg, #FFF8E8, #F1F6FF, #F0FFF4
    );
}

.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
}

.hero {
    background: linear-gradient(
        120deg, #FFE5AD, #FFD9EA, #DDEAFF
    );
    padding: 35px;
    border-radius: 25px;
    text-align: center;
}

.hero h1 {
    color: #26345A;
    font-weight: 900;
    font-size: clamp(32px, 5vw, 55px);
}

.hero p {
    color: #475569;
    font-size: 18px;
}

.game-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    text-align: center;
    border: 1px solid #E8ECF5;
    box-shadow: 0 5px 20px #0000000A;
    margin-bottom: 12px;
}

div.stButton > button {
    border-radius: 13px;
    font-weight: 800;
    min-height: 42px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

left, right = st.columns([4, 1])

with left:
    st.markdown("## 🌈 Little Minds")

with right:
    if st.session_state.student:
        st.write("👋 " + st.session_state.student["name"])

        if st.button("Logout"):
            st.session_state.student = None
            st.session_state.page = "Home"
            st.rerun()


# ==========================================
# NAVIGATION
# ==========================================

PAGES = [
    "Home",
    "Create Account",
    "Student Login",
    "Student Dashboard",
    "Colour Quest",
    "Shape Safari",
    "Counting Garden",
    "Memory Match",
    "Admin Panel"
]

with st.sidebar:
    st.title("🧸 Learning Menu")

    page = st.radio(
        "Choose a section",
        PAGES,
        index=PAGES.index(st.session_state.page)
        if st.session_state.page in PAGES else 0
    )

    st.session_state.page = page

    st.divider()

    st.caption("PG • Nursery • LKG • UKG")


# ==========================================
# HOME PAGE
# ==========================================

if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>Curious Minds. Happy Discoveries! 🌈</h1>
        <p>Learn • Play • Explore • Grow</p>
        <p>Fun learning for PG, Nursery, LKG and UKG.</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    columns = st.columns(4)

    games = [
        ("🎨", "Colour Quest", "Learn colours"),
        ("🔷", "Shape Safari", "Explore shapes"),
        ("🔢", "Counting Garden", "Learn numbers"),
        ("🧠", "Memory Match", "Train your memory")
    ]

    for col, game in zip(columns, games):
        with col:
            st.markdown(f"""
            <div class="game-card">
                <h1>{game[0]}</h1>
                <h3>{game[1]}</h3>
                <p>{game[2]}</p>
            </div>
            """, unsafe_allow_html=True)

    st.subheader("📚 Choose Your Learning Level")

    c1, c2, c3, c4 = st.columns(4)

    for col, level, emoji in zip(
        [c1, c2, c3, c4],
        ["PG", "Nursery", "LKG", "UKG"],
        ["🧸", "🌱", "✏️", "🚀"]
    ):
        with col:
            st.info(f"{emoji} **{level}**")

    st.caption(
        "These are starter activities, not a complete official syllabus."
    )


# ==========================================
# REGISTRATION
# ==========================================

elif page == "Create Account":

    st.title("🧸 Create Student Account")

    st.info(
        "A parent or guardian should complete registration "
        "and provide consent for a young child."
    )

    with st.form("registration"):

        name = st.text_input("Student name or nickname")
        email = st.text_input("Account email")
        guardian = st.text_input("Parent/guardian email")

        level = st.selectbox(
            "Choose class",
            ["PG", "Nursery", "LKG", "UKG"]
        )

        password = st.text_input(
            "Password (minimum 10 characters)",
            type="password"
        )

        consent = st.checkbox(
            "I am the parent/guardian and consent to creating this account."
        )

        submit = st.form_submit_button("Create Account")

    if submit:

        if not name.strip():
            st.error("Enter the student's name.")

        elif "@" not in email or "." not in email.split("@")[-1]:
            st.error("Enter a valid account email.")

        elif "@" not in guardian or "." not in guardian.split("@")[-1]:
            st.error("Enter a valid guardian email.")

        elif len(password) < 10:
            st.error("Password must be at least 10 characters.")

        elif not consent:
            st.error("Guardian consent is required.")

        else:
            password_hash, salt = hash_password(password)

            try:
                with database() as con:
                    con.execute("""
                    INSERT INTO students
                    (name, email, password_hash, salt,
                     class_name, guardian_email, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        name.strip(),
                        email.strip().lower(),
                        password_hash,
                        salt,
                        level,
                        guardian.strip().lower(),
                        datetime.now().isoformat(timespec="seconds")
                    ))

                st.success(
                    "Account created! Open Student Login to continue."
                )

            except sqlite3.IntegrityError:
                st.error("This account email is already registered.")


# ==========================================
# STUDENT LOGIN
# ==========================================

elif page == "Student Login":

    st.title("🔐 Student Login")

    with st.form("login"):

        email = st.text_input("Account email")

        password = st.text_input(
            "Password",
            type="password"
        )

        submit = st.form_submit_button("Sign In")

    if submit:

        with database() as con:
            student = con.execute("""
            SELECT * FROM students WHERE email = ?
            """, (email.strip().lower(),)).fetchone()

        if student and verify_password(
            password,
            student["password_hash"],
            student["salt"]
        ):

            st.session_state.student = dict(student)
            st.session_state.page = "Student Dashboard"

            st.success("Login successful!")
            st.rerun()

        else:
            st.error("Incorrect email or password.")


# ==========================================
# STUDENT DASHBOARD
# ==========================================

elif page == "Student Dashboard":

    if not st.session_state.student:

        st.warning("Please sign in first.")

    else:

        student = st.session_state.student

        st.title(f"Hello, {student['name']}! 👋")

        st.write(f"**Your class:** {student['class_name']}")

        with database() as con:
            records = con.execute("""
            SELECT game, score, played_at
            FROM scores
            WHERE student_id = ?
            ORDER BY id DESC
            """, (student["id"],)).fetchall()

        total = sum(record["score"] for record in records)

        a, b, c = st.columns(3)

        a.metric("Activities completed", len(records))
        b.metric("Total points", total)
        c.metric(
            "Best points",
            max([r["score"] for r in records], default=0)
        )

        st.subheader("📊 Recent Learning Activity")

        if records:
            st.dataframe(
                [
                    {
                        "Game": r["game"],
                        "Points": r["score"],
                        "Date": r["played_at"]
                    }
                    for r in records
                ],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Play a game to start tracking your progress!")


# ==========================================
# COLOUR QUEST
# ==========================================

elif page == "Colour Quest":

    st.title("🎨 Colour Quest")

    if not st.session_state.student:
        st.warning("Please sign in first.")

    else:

        target = st.session_state.colour_target

        st.subheader(f"Find the {target} colour!")

        st.write("Tap the correct coloured box.")

        names = list(COLORS.keys())
        cols = st.columns(3)

        for i, name in enumerate(names):

            with cols[i % 3]:

                st.markdown(
                    f"""
                    <div style="
                        height:95px;
                        border-radius:18px;
                        background:{COLORS[name]};
                        border:3px solid white;
                        margin-bottom:8px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "Choose this colour",
                    key=f"color_{i}_{target}",
                    use_container_width=True
                ):

                    if name == target:
                        save_score("Colour Quest")
                        st.success("Correct! Great job! 🎉")
                    else:
                        st.error("Try again!")

        if st.button("Next Colour"):
            st.session_state.colour_target = random.choice(names)
            st.rerun()


# ==========================================
# SHAPE SAFARI
# ==========================================

elif page == "Shape Safari":

    st.title("🔷 Shape Safari")

    if not st.session_state.student:
        st.warning("Please sign in first.")

    else:

        target = st.session_state.shape_target

        st.subheader(f"Find the {target}!")

        cols = st.columns(4)

        for i, (shape, emoji) in enumerate(SHAPES.items()):

            with cols[i]:

                st.markdown(
                    f"<h1 style='text-align:center'>{emoji}</h1>",
                    unsafe_allow_html=True
                )

                if st.button(shape, key=f"shape_{i}"):

                    if shape == target:
                        save_score("Shape Safari")
                        st.success("Correct shape! ⭐")
                    else:
                        st.error("Try again!")

        if st.button("Next Shape"):
            st.session_state.shape_target = random.choice(
                list(SHAPES.keys())
            )
            st.rerun()


# ==========================================
# COUNTING GARDEN
# ==========================================

elif page == "Counting Garden":

    st.title("🔢 Counting Garden")

    if not st.session_state.student:
        st.warning("Please sign in first.")

    else:

        target = st.session_state.count_target

        st.subheader("Count the apples!")

        st.markdown(
            f"<h1>{'🍎 ' * target}</h1>",
            unsafe_allow_html=True
        )

        options = sorted(set([
            target,
            max(1, target - 1),
            min(10, target + 1),
            random.randint(1, 10)
        ]))

        cols = st.columns(len(options))

        for i, number in enumerate(options):

            with cols[i]:

                if st.button(
                    str(number),
                    key=f"count_{target}_{i}_{number}"
                ):

                    if number == target:
                        save_score("Counting Garden")
                        st.success("Correct counting! 🎉")
                    else:
                        st.error("Count the apples again.")

        if st.button("Next Counting Round"):
            st.session_state.count_target = random.randint(1, 10)
            st.rerun()


# ==========================================
# MEMORY MATCH
# ==========================================

elif page == "Memory Match":

    st.title("🧠 Memory Match")

    if not st.session_state.student:
        st.warning("Please sign in first.")

    else:

        if not st.session_state.memory_cards:
            cards = random.sample(ANIMALS, 4)
            st.session_state.memory_cards = cards
            st.session_state.memory_target = random.choice(cards)

        target = st.session_state.memory_target

        st.subheader(f"Find this animal: {target}")

        cols = st.columns(4)

        for i, animal in enumerate(st.session_state.memory_cards):

            with cols[i]:

                st.markdown(
                    f"<h1 style='text-align:center'>{animal}</h1>",
                    unsafe_allow_html=True
                )

                if st.button("Choose", key=f"animal_{i}"):

                    if animal == target:
                        save_score("Memory Match")
                        st.success("You remembered it! 🧠")
                    else:
                        st.error("Try another animal.")

        if st.button("New Memory Round"):
            cards = random.sample(ANIMALS, 4)
            st.session_state.memory_cards = cards
            st.session_state.memory_target = random.choice(cards)
            st.rerun()


# ==========================================
# ADMIN PANEL
# ==========================================

elif page == "Admin Panel":

    st.title("🛡️ Admin Dashboard")

    admin_password = os.environ.get(
        "LITTLE_MINDS_ADMIN_PASSWORD", ""
    )

    if not admin_password:

        st.warning(
            "Admin login is disabled. Set the "
            "LITTLE_MINDS_ADMIN_PASSWORD environment variable."
        )

    elif not st.session_state.admin:

        entered = st.text_input(
            "Admin password",
            type="password"
        )

        if st.button("Admin Login"):

            if hmac.compare_digest(entered, admin_password):
                st.session_state.admin = True
                st.rerun()
            else:
                st.error("Incorrect admin password.")

    else:

        if st.button("Admin Logout"):
            st.session_state.admin = False
            st.rerun()

        with database() as con:

            students = con.execute("""
            SELECT name, email, class_name,
                   guardian_email, created_at
            FROM students ORDER BY id DESC
            """).fetchall()

            scores = con.execute("""
            SELECT students.name, students.class_name,
                   scores.game, scores.score, scores.played_at
            FROM scores
            JOIN students ON students.id = scores.student_id
            ORDER BY scores.id DESC
            """).fetchall()

        st.metric("Registered students", len(students))

        st.subheader("👩‍🎓 Student Records")

        st.dataframe(
            [
                {
                    "Name": s["name"],
                    "Class": s["class_name"],
                    "Account Email": s["email"],
                    "Guardian Email": s["guardian_email"],
                    "Registered": s["created_at"]
                }
                for s in students
            ],
            use_container_width=True,
            hide_index=True
        )

        st.subheader("📈 Game Progress")

        st.dataframe(
            [
                {
                    "Student": s["name"],
                    "Class": s["class_name"],
                    "Game": s["game"],
                    "Score": s["score"],
                    "Played": s["played_at"]
                }
                for s in scores
            ],
            use_container_width=True,
            hide_index=True
        )

        if students:

            output = io.StringIO()

            writer = csv.writer(output)

            writer.writerow([
                "Name", "Class", "Account Email",
                "Guardian Email", "Registered"
            ])

            for s in students:
                writer.writerow([
                    s["name"],
                    s["class_name"],
                    s["email"],
                    s["guardian_email"],
                    s["created_at"]
                ])

            st.download_button(
                "Download student CSV",
                data=output.getvalue(),
                file_name="little_minds_students.csv",
                mime="text/csv"
            )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "🌈 Little Minds — Learn through play!"
)

st.caption(
    "Starter prototype: records are stored in a local database. "
    "Before public use with children, arrange a privacy and security "
    "review, guardian-consent process, secure hosting and backups. "
    "Never publish the local database file."
)
