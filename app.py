import streamlit as st
import sqlite3
import random
import hashlib
import secrets
import hmac
import os
from datetime import datetime

# ===============================
# LITTLE MINDS - EDUCATIONAL APP
# ===============================

st.set_page_config(
    page_title="Little Minds",
    page_icon="🌈",
    layout="wide"
)

# ===============================
# DATABASE
# ===============================

conn = sqlite3.connect("little_minds.db", check_same_thread=False)
conn.row_factory = sqlite3.Row

conn.execute("""
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

conn.execute("""
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER NOT NULL,
    game TEXT NOT NULL,
    score INTEGER NOT NULL,
    played_at TEXT NOT NULL
)
""")

conn.commit()


# ===============================
# PASSWORD SECURITY
# ===============================

def make_password_hash(password, salt=None):
    if salt is None:
        salt = secrets.token_bytes(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200000
    )

    return password_hash.hex(), salt.hex()


def check_password(password, stored_hash, salt_hex):
    salt = bytes.fromhex(salt_hex)

    calculated_hash, _ = make_password_hash(
        password,
        salt
    )

    return hmac.compare_digest(
        calculated_hash,
        stored_hash
    )


# ===============================
# SAVE GAME SCORE
# ===============================

def save_score(game, score):
    student = st.session_state.get("student")

    if student:
        conn.execute("""
        INSERT INTO scores
        (student_id, game, score, played_at)
        VALUES (?, ?, ?, ?)
        """, (
            student["id"],
            game,
            score,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()


# ===============================
# SESSION STATE
# ===============================

if "student" not in st.session_state:
    st.session_state.student = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "color_target" not in st.session_state:
    st.session_state.color_target = random.choice([
        "RED", "BLUE", "GREEN", "YELLOW"
    ])

if "shape_target" not in st.session_state:
    st.session_state.shape_target = random.choice([
        "Circle", "Square", "Triangle", "Star"
    ])

if "count_target" not in st.session_state:
    st.session_state.count_target = random.randint(1, 10)


# ===============================
# WEBSITE DESIGN
# ===============================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #fff7e6,
        #f2f7ff,
        #f1fff5
    );
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.hero {
    background: linear-gradient(
        120deg,
        #ffe2a8,
        #ffd9e9,
        #dceaff
    );
    padding: 35px;
    border-radius: 25px;
    text-align: center;
}

.hero h1 {
    color: #26345a;
    font-size: 48px;
    font-weight: 900;
}

.hero p {
    font-size: 19px;
    color: #475569;
}

.game-card {
    background: white;
    padding: 22px;
    border-radius: 22px;
    text-align: center;
    box-shadow: 0 5px 20px #0000000d;
    min-height: 180px;
}

div.stButton > button {
    border-radius: 12px;
    font-weight: bold;
    min-height: 42px;
}
</style>
""", unsafe_allow_html=True)


# ===============================
# HEADER
# ===============================

st.markdown("""
<div class="hero">
    <h1>🌈 Little Minds</h1>
    <p>Little steps, big discoveries!</p>
    <p>Learn • Play • Explore • Grow</p>
</div>
""", unsafe_allow_html=True)

st.write("")


# ===============================
# SIDEBAR
# ===============================

with st.sidebar:
    st.title("🧸 Learning Menu")

    pages = [
        "Home",
        "Create Account",
        "Login",
        "Student Dashboard",
        "Colour Quest",
        "Shape Safari",
        "Counting Garden",
        "Memory Match",
        "Admin Panel"
    ]

    selected_page = st.radio(
        "Choose a page",
        pages
    )

    st.session_state.page = selected_page

    if st.session_state.student:
        st.success(
            "Welcome, "
            + st.session_state.student["name"]
        )

        if st.button("Logout"):
            st.session_state.student = None
            st.session_state.page = "Home"
            st.rerun()


# ===============================
# HOME PAGE
# ===============================

if st.session_state.page == "Home":

    st.title("Welcome to Little Minds! 🎉")

    st.write("""
    A fun educational website for young learners.

    Explore colourful activities designed for
    PG, Nursery, LKG and UKG.
    """)

    st.subheader("🌟 Explore Our Games")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class="game-card">
        <h1>🎨</h1>
        <h3>Colour Quest</h3>
        <p>Discover colours through play.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="game-card">
        <h1>🔷</h1>
        <h3>Shape Safari</h3>
        <p>Explore different shapes.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="game-card">
        <h1>🔢</h1>
        <h3>Counting Garden</h3>
        <p>Learn to count objects.</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="game-card">
        <h1>🧠</h1>
        <h3>Memory Match</h3>
        <p>Practise remembering symbols.</p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.subheader("📚 Learning Classes")

    st.info("🧸 PG  |  🌱 Nursery  |  ✏️ LKG  |  🚀 UKG")

    st.caption(
        "Activities are introductory learning exercises, "
        "not an official school syllabus."
    )


# ===============================
# CREATE ACCOUNT
# ===============================

elif st.session_state.page == "Create Account":

    st.title("🧸 Create Student Account")

    st.warning(
        "A parent or guardian should complete registration "
        "for a young child."
    )

    with st.form("register_form"):

        name = st.text_input(
            "Child's first name or nickname"
        )

        email = st.text_input(
            "Account email"
        )

        guardian_email = st.text_input(
            "Parent/guardian email"
        )

        class_name = st.selectbox(
            "Select Class",
            ["PG", "Nursery", "LKG", "UKG"]
        )

        password = st.text_input(
            "Create Password",
            type="password"
        )

        consent = st.checkbox(
            "I am the parent/guardian and consent "
            "to creating this account."
        )

        submitted = st.form_submit_button(
            "Create Account"
        )

    if submitted:

        if not name.strip():
            st.error("Please enter the child's name.")

        elif "@" not in email:
            st.error("Enter a valid account email.")

        elif "@" not in guardian_email:
            st.error("Enter a valid guardian email.")

        elif len(password) < 10:
            st.error(
                "Password must contain at least 10 characters."
            )

        elif not consent:
            st.error("Parent/guardian consent is required.")

        else:
            password_hash, salt = make_password_hash(
                password
            )

            try:
                conn.execute("""
                INSERT INTO students
                (name, email, password_hash, salt,
                 class_name, guardian_email, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    name.strip(),
                    email.strip().lower(),
                    password_hash,
                    salt,
                    class_name,
                    guardian_email.strip().lower(),
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                ))

                conn.commit()

                st.success(
                    "Account created successfully! "
                    "Now go to Login."
                )

            except sqlite3.IntegrityError:
                st.error(
                    "This email is already registered."
                )


# ===============================
# LOGIN
# ===============================

elif st.session_state.page == "Login":

    st.title("🔐 Student Login")

    with st.form("login_form"):

        email = st.text_input("Account email")

        password = st.text_input(
            "Password",
            type="password"
        )

        submitted = st.form_submit_button("Login")

    if submitted:

        student = conn.execute("""
        SELECT * FROM students
        WHERE email = ?
        """, (
            email.strip().lower(),
        )).fetchone()

        if student and check_password(
            password,
            student["password_hash"],
            student["salt"]
        ):

            st.session_state.student = dict(student)

            st.success("Login successful!")

            st.session_state.page = "Student Dashboard"

            st.rerun()

        else:
            st.error("Incorrect email or password.")


# ===============================
# STUDENT DASHBOARD
# ===============================

elif st.session_state.page == "Student Dashboard":

    if not st.session_state.student:

        st.warning("Please login first.")

    else:

        student = st.session_state.student

        st.title(
            "Hello, "
            + student["name"]
            + "! 👋"
        )

        st.write(
            "Your class: "
            + student["class_name"]
        )

        rows = conn.execute("""
        SELECT game, score, played_at
        FROM scores
        WHERE student_id = ?
        ORDER BY id DESC
        """, (
            student["id"],
        )).fetchall()

        total_points = sum(
            row["score"] for row in rows
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Games Played",
            len(rows)
        )

        col2.metric(
            "Total Points",
            total_points
        )

        col3.metric(
            "Best Score",
            max(
                [row["score"] for row in rows],
                default=0
            )
        )

        st.subheader("📊 Recent Progress")

        if rows:

            st.dataframe(
                [
                    {
                        "Game": row["game"],
                        "Score": row["score"],
                        "Date": row["played_at"]
                    }
                    for row in rows
                ],
                use_container_width=True,
                hide_index=True
            )

        else:
            st.info(
                "Play a game to start tracking progress!"
            )


# ===============================
# COLOUR QUEST
# ===============================

elif st.session_state.page == "Colour Quest":

    st.title("🎨 Colour Quest")

    if not st.session_state.student:

        st.warning("Please login first.")

    else:

        colours = {
            "RED": "#ef4444",
            "BLUE": "#3b82f6",
            "GREEN": "#22c55e",
            "YELLOW": "#facc15",
            "PURPLE": "#a855f7",
            "ORANGE": "#f97316"
        }

        target = st.session_state.color_target

        st.subheader(
            f"Find the {target} colour!"
        )

        st.write("Choose the box with the matching colour.")

        options = random.sample(
            list(colours.keys()),
            len(colours)
        )

        cols = st.columns(3)

        for i, colour in enumerate(options):

            with cols[i % 3]:

                st.markdown(
                    f"""
                    <div style="
                        height:100px;
                        background:{colours[colour]};
                        border-radius:18px;
                        margin-bottom:8px;
                        border:2px solid white;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    "Choose",
                    key=f"colour_{i}_{target}"
                ):

                    if colour == target:

                        save_score("Colour Quest", 1)

                        st.success(
                            "Correct! Great job! 🌟"
                        )

                    else:

                        st.error(
                            "Try again! You can do it."
                        )

        if st.button("Next Colour"):

            st.session_state.color_target = random.choice(
                list(colours.keys())
            )

            st.rerun()


# ===============================
# SHAPE SAFARI
# ===============================

elif st.session_state.page == "Shape Safari":

    st.title("🔷 Shape Safari")

    if not st.session_state.student:

        st.warning("Please login first.")

    else:

        shapes = {
            "Circle": "🔵",
            "Square": "🟦",
            "Triangle": "🔺",
            "Star": "⭐"
        }

        target = st.session_state.shape_target

        st.subheader(
            f"Find the {target}!"
        )

        cols = st.columns(4)

        for i, shape in enumerate(shapes):

            with cols[i]:

                st.markdown(
                    f"<h1 style='text-align:center'>"
                    f"{shapes[shape]}</h1>",
                    unsafe_allow_html=True
                )

                if st.button(
                    shape,
                    key=f"shape_{i}"
                ):

                    if shape == target:

                        save_score("Shape Safari", 1)

                        st.success(
                            "Excellent! You found the shape! ⭐"
                        )

                    else:

                        st.error("Try another shape.")

        if st.button("Next Shape"):

            st.session_state.shape_target = random.choice(
                list(shapes.keys())
            )

            st.rerun()


# ===============================
# COUNTING GARDEN
# ===============================

elif st.session_state.page == "Counting Garden":

    st.title("🔢 Counting Garden")

    if not st.session_state.student:

        st.warning("Please login first.")

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

        for i, answer in enumerate(options):

            with cols[i]:

                if st.button(
                    str(answer),
                    key=f"count_{i}_{target}"
                ):

                    if answer == target:

                        save_score(
                            "Counting Garden",
                            1
                        )

                        st.success(
                            "Correct counting! 🎉"
                        )

                    else:

                        st.error(
                            "Count the apples again."
                        )

        if st.button("Next Counting Round"):

            st.session_state.count_target = random.randint(
                1, 10
            )

            st.rerun()


# ===============================
# MEMORY MATCH
# ===============================

elif st.session_state.page == "Memory Match":

    st.title("🧠 Memory Match")

    if not st.session_state.student:

        st.warning("Please login first.")

    else:

        if "memory_cards" not in st.session_state:
            st.session_state.memory_cards = random.sample(
                ["🍎", "🐻", "🚗", "🌟", "🐸", "🦋"],
                4
            )

        if "memory_target" not in st.session_state:
            st.session_state.memory_target = random.choice(
                st.session_state.memory_cards
            )

        target = st.session_state.memory_target

        st.subheader(
            f"Find this symbol: {target}"
        )

        cols = st.columns(4)

        for i, symbol in enumerate(
            st.session_state.memory_cards
        ):

            with cols[i]:

                st.markdown(
                    f"<h1 style='text-align:center'>"
                    f"{symbol}</h1>",
                    unsafe_allow_html=True
                )

                if st.button(
                    "Choose",
                    key=f"memory_{i}"
                ):

                    if symbol == target:

                        save_score("Memory Match", 1)

                        st.success(
                            "Well remembered! 🧠"
                        )

                    else:

                        st.error("Try again!")

        if st.button("New Memory Round"):

            st.session_state.memory_cards = random.sample(
                ["🍎", "🐻", "🚗", "🌟", "🐸", "🦋"],
                4
            )

            st.session_state.memory_target = random.choice(
                st.session_state.memory_cards
            )

            st.rerun()


# ===============================
# ADMIN PANEL
# ===============================

elif st.session_state.page == "Admin Panel":

    st.title("🛡️ Admin Dashboard")

    admin_password = os.environ.get(
        "LITTLE_MINDS_ADMIN_PASSWORD",
        ""
    )

    if not admin_password:

        st.warning(
            "Admin login is disabled. Set the "
            "LITTLE_MINDS_ADMIN_PASSWORD environment variable."
        )

    elif not st.session_state.admin_logged_in:

        entered_password = st.text_input(
            "Admin Password",
            type="password"
        )

        if st.button("Admin Login"):

            if hmac.compare_digest(
                entered_password,
                admin_password
            ):

                st.session_state.admin_logged_in = True

                st.rerun()

            else:

                st.error("Incorrect admin password.")

    else:

        if st.button("Admin Logout"):

            st.session_state.admin_logged_in = False

            st.rerun()

        students = conn.execute("""
        SELECT id, name, email, class_name,
               guardian_email, created_at
        FROM students
        ORDER BY id DESC
        """).fetchall()

        scores = conn.execute("""
        SELECT students.name,
               students.class_name,
               scores.game,
               scores.score,
               scores.played_at
        FROM scores
        JOIN students
        ON students.id = scores.student_id
        ORDER BY scores.id DESC
        """).fetchall()

        st.metric(
            "Registered Students",
            len(students)
        )

        st.subheader("👩‍🎓 Student Accounts")

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
                    "Played At": s["played_at"]
                }
                for s in scores
            ],
            use_container_width=True,
            hide_index=True
        )

        if students:

            csv_data = (
                "Name,Class,Account Email,Guardian Email,Registered\n"
                + "\n".join(
                    ",".join(
                        '"' + str(value).replace('"', '""') + '"'
                        for value in [
                            s["name"],
                            s["class_name"],
                            s["email"],
                            s["guardian_email"],
                            s["created_at"]
                        ]
                    )
                    for s in students
                )
            )

            st.download_button(
                "Download Student List CSV",
                data=csv_data,
                file_name="little_minds_students.csv",
                mime="text/csv"
            )


# ===============================
# FOOTER
# ===============================

st.divider()

st.caption(
    "Little Minds | Learn through play 🌈"
)

st.caption(
    "Prototype notice: account details and game scores are "
    "stored in a local database. Before public launch, have an "
    "adult review child privacy, guardian consent, hosting security, "
    "and applicable laws. Never expose the database publicly."
)
