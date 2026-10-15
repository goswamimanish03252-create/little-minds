
import random
import streamlit as st
import streamlit.components.v1 as components

# ==================================================
# LITTLE MINDS - EDUCATIONAL GAMING WEBSITE
# ==================================================

st.set_page_config(
    page_title="Little Minds",
    page_icon="🌈",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------- CSS DESIGN --------------------

st.markdown("""
<style>
.stApp {
    background: #F3F1FF;
    color: #292F59;
}
h1, h2, h3, p, label {
    color: #292F59;
}
h1 { text-align: center; }

.hero {
    background: linear-gradient(130deg, #E6DCFF, #DDF3FF, #FFE6F0);
    border: 1px solid #E3DDFB;
    border-radius: 25px;
    padding: 24px 14px;
    text-align: center;
    margin: 10px 0 22px;
    animation: appear .5s ease;
}
.hero h2 { margin: 0; font-size: 29px; }
.hero p { margin-bottom: 0; }

.game-card {
    background: rgba(255,255,255,.88);
    border: 1px solid #E1DDFC;
    border-radius: 20px;
    padding: 14px;
    margin-bottom: 12px;
    animation: appear .35s ease;
}
.big-emoji {
    font-size: 45px;
    text-align: center;
    padding: 8px;
}
div.stButton > button {
    background: white;
    color: #35305F;
    border: 2px solid #DFDDFC;
    border-radius: 15px;
    min-height: 45px;
    font-weight: 600;
    transition: .2s ease;
}
div.stButton > button:hover {
    background: #E9E2FF;
    border-color: #A99AF3;
    transform: translateY(-2px);
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E1DDFC;
    padding: 12px;
    border-radius: 16px;
}
[data-testid="stProgressBar"] > div > div {
    background-color: #9276F5;
}
.small-note {
    font-size: 13px;
    color: #747999;
}
@keyframes appear {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# -------------------- GAME CATALOG --------------------

GAME_INFO = {
    "Colours": ("🎨", "Learn colours", "Art"),
    "Shapes": ("🔺", "Discover shapes", "Basics"),
    "Counting": ("🔢", "Count and learn numbers", "Math"),
    "Memory": ("🧠", "Find matching cards", "Brain"),
    "Alphabet Adventure": ("🔤", "Explore letters", "Words"),
    "Animal & Word Match": ("🐾", "Learn animals and words", "Words"),
    "Math Challenge": ("➕", "Solve number puzzles", "Math"),
    "Little Scientist": ("🌱", "Discover nature and science", "Science"),
    "World Explorer": ("🌍", "Explore our world", "Discovery"),
}

# Each quiz: question, options, correct answer
QUIZZES = {
    "Shapes": [
        ("Which shape has three sides?", ["Circle", "Triangle", "Square", "Oval"], "Triangle"),
        ("How many sides does a square have?", ["2", "3", "4", "5"], "4"),
        ("Which shape is round?", ["Circle", "Triangle", "Rectangle", "Square"], "Circle"),
        ("Which shape has four equal sides?", ["Oval", "Triangle", "Square", "Circle"], "Square"),
        ("Which shape looks like an egg?", ["Oval", "Square", "Triangle", "Star"], "Oval"),
    ],
    "Counting": [
        ("What is 2 + 3?", ["4", "5", "6", "7"], "5"),
        ("What is 5 + 1?", ["5", "6", "7", "8"], "6"),
        ("What is 4 + 4?", ["6", "7", "8", "9"], "8"),
        ("What is 9 - 3?", ["5", "6", "7", "8"], "6"),
        ("What comes after 14?", ["12", "13", "15", "16"], "15"),
    ],
    "Alphabet Adventure": [
        ("Which letter comes after A?", ["B", "C", "D", "E"], "B"),
        ("Which letter comes after D?", ["C", "E", "F", "G"], "E"),
        ("Which letter starts Apple?", ["A", "B", "C", "D"], "A"),
        ("Which letter starts Ball?", ["D", "B", "P", "G"], "B"),
        ("What comes before Z?", ["X", "Y", "W", "V"], "Y"),
    ],
    "Animal & Word Match": [
        ("Which animal says 'meow'?", ["Dog", "Cat", "Cow", "Duck"], "Cat"),
        ("Which animal gives us milk?", ["Cow", "Lion", "Fox", "Tiger"], "Cow"),
        ("Which animal has a long trunk?", ["Horse", "Elephant", "Rabbit", "Bear"], "Elephant"),
        ("Which animal can fly?", ["Fish", "Bird", "Cow", "Dog"], "Bird"),
        ("Which one is a fruit?", ["Carrot", "Apple", "Potato", "Onion"], "Apple"),
    ],
    "Math Challenge": [
        ("What is 7 + 6?", ["11", "12", "13", "14"], "13"),
        ("What is 12 - 5?", ["6", "7", "8", "9"], "7"),
        ("What is 3 × 4?", ["7", "12", "14", "16"], "12"),
        ("Which number is even?", ["3", "5", "8", "9"], "8"),
        ("What is 20 - 8?", ["10", "11", "12", "13"], "12"),
        ("What is 5 × 2?", ["7", "8", "10", "12"], "10"),
    ],
    "Little Scientist": [
        ("What helps plants grow?", ["Water and sunlight", "Plastic", "Only stones", "Darkness always"], "Water and sunlight"),
        ("Which planet do we live on?", ["Mars", "Earth", "Jupiter", "Venus"], "Earth"),
        ("What do bees collect from flowers?", ["Sand", "Nectar", "Snow", "Pebbles"], "Nectar"),
        ("What gas do humans need to breathe?", ["Oxygen", "Smoke", "Sand", "Helium"], "Oxygen"),
        ("Which is a source of light?", ["The Sun", "A rock", "A leaf", "A book"], "The Sun"),
    ],
    "World Explorer": [
        ("Which planet is known as the Red Planet?", ["Mars", "Earth", "Neptune", "Venus"], "Mars"),
        ("Which is the largest ocean?", ["Pacific", "Arctic", "Indian", "Atlantic"], "Pacific"),
        ("What helps us find directions?", ["Compass", "Pillow", "Plate", "Brush"], "Compass"),
        ("Which is a continent?", ["Africa", "Pacific", "Amazon River", "Everest"], "Africa"),
        ("Which is the highest mountain above sea level?", ["Everest", "Fuji", "Kilimanjaro", "Denali"], "Everest"),
    ],
}

COLOURS = {
    "RED": "#F04444",
    "BLUE": "#4285F4",
    "GREEN": "#36A66A",
    "YELLOW": "#F5C542",
}

# -------------------- SESSION STATE --------------------

def init_state():
    defaults = {
        "page": "Home",
        "profile_name": "Little Explorer",
        "sound_on": False,
        "scores": {g: 0 for g in GAME_INFO},
        "attempts": {g: 0 for g in GAME_INFO},
        "correct": {g: 0 for g in GAME_INFO},
        "question_no": {g: 0 for g in GAME_INFO},
        "questions": {},
        "options": {},
        "answered": {},
        "feedback": {},
        "target_colour": None,
        "colour_options": [],
        "memory_cards": [],
        "memory_revealed": [],
        "memory_matched": [],
        "memory_moves": 0,
        "memory_feedback": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_state()

# -------------------- HELPERS --------------------

def new_question(game):
    st.session_state.question_no[game] += 1
    st.session_state.answered[game] = False
    st.session_state.feedback[game] = ""

    if game == "Colours":
        st.session_state.target_colour = random.choice(list(COLOURS))
        options = list(COLOURS)
        random.shuffle(options)
        # Options are stored once per question.
        st.session_state.colour_options = options
    else:
        question = random.choice(QUIZZES[game])
        st.session_state.questions[game] = question
        options = list(question[1])
        random.shuffle(options)
        st.session_state.options[game] = options

def start_game(game):
    st.session_state.page = game
    if game == "Memory":
        reset_memory()
    else:
        new_question(game)
    st.rerun()

def next_question(game):
    new_question(game)
    st.rerun()

def reset_memory():
    cards = ["🐶", "🐱", "🐸", "🦊", "🐼", "🐰"] * 2
    random.shuffle(cards)
    st.session_state.memory_cards = cards
    st.session_state.memory_revealed = []
    st.session_state.memory_matched = []
    st.session_state.memory_moves = 0
    st.session_state.memory_feedback = ""

def total_points():
    return sum(st.session_state.scores.values())

def unlock_badges():
    total = total_points()
    badges = []
    if total >= 5:
        badges.append("🌟 First Star")
    if total >= 15:
        badges.append("🏆 Learning Hero")
    if total >= 30:
        badges.append("🚀 Super Explorer")
    return badges

def sound_effect(kind="correct"):
    if not st.session_state.sound_on:
        return

    frequency = 740 if kind == "correct" else 280
    components.html(f"""
    <script>
    try {{
        const ctx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.frequency.value = {frequency};
        gain.gain.value = 0.06;
        osc.start();
        osc.stop(ctx.currentTime + 0.18);
    }} catch(e) {{}}
    </script>
    """, height=0)

def submit_answer(game, is_correct):
    if st.session_state.answered.get(game, False):
        return

    st.session_state.answered[game] = True
    st.session_state.attempts[game] += 1

    if is_correct:
        st.session_state.scores[game] += 1
        st.session_state.correct[game] += 1
        st.session_state.feedback[game] = "correct"
        sound_effect("correct")
    else:
        st.session_state.feedback[game] = "wrong"
        sound_effect("wrong")

def back_home():
    st.session_state.page = "Home"
    st.rerun()

def render_quiz(game):
    icon = GAME_INFO[game][0]

    st.markdown(f"""
    <div class="hero">
        <div style="font-size:46px">{icon}</div>
        <h2>{game}</h2>
        <p>Learn by playing • Earn stars</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Back to Home", key=f"back_{game}"):
        back_home()

    question, original_options, correct_answer = st.session_state.questions[game]
    number = st.session_state.question_no[game]

    st.progress(((number - 1) % 5 + 1) / 5, text=f"Practice question {((number - 1) % 5) + 1} of 5")

    st.markdown('<div class="game-card">', unsafe_allow_html=True)
    st.subheader(question)

    for i, option in enumerate(st.session_state.options[game]):
        if st.button(
            option,
            key=f"opt_{game}_{number}_{i}",
            use_container_width=True,
            disabled=st.session_state.answered[game],
        ):
            submit_answer(game, option == correct_answer)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.answered[game]:
        if st.session_state.feedback[game] == "correct":
            st.success("🎉 Correct! Great job! +1 point")
            st.balloons()
        else:
            st.warning(f"😊 Good try! Correct answer: {correct_answer}")

        if st.button("➡️ Next Question", key=f"next_{game}", use_container_width=True):
            next_question(game)

    st.caption(f"⭐ {st.session_state.scores[game]} points earned")

# -------------------- HEADER --------------------

st.markdown("""
<div class="hero">
    <div style="font-size:45px">🌈</div>
    <h2>LITTLE MINDS</h2>
    <p>Play • Learn • Grow</p>
</div>
""", unsafe_allow_html=True)

# -------------------- NAVIGATION --------------------

nav_items = [
    ("🏠", "Home"),
    ("📚", "Learn"),
    ("🎮", "Games"),
    ("🏆", "Rewards"),
    ("👤", "Profile"),
]

nav_cols = st.columns(5)
for col, (icon, page) in zip(nav_cols, nav_items):
    with col:
        if st.button(f"{icon}\n{page}", key=f"nav_{page}", use_container_width=True):
            st.session_state.page = page
            st.rerun()

st.divider()

# ==================================================
# HOME
# ==================================================

if st.session_state.page == "Home":
    st.subheader(f"Hi, {st.session_state.profile_name}! 👋")
    st.write("Ready to learn something awesome today?")

    st.markdown("""
    <div class="game-card">
        <h3>⭐ Your Daily Learning Goal</h3>
        <p>Earn 5 points by playing educational games.</p>
    </div>
    """, unsafe_allow_html=True)

    st.progress(min(total_points() / 5, 1.0), text=f"{min(total_points(), 5)} / 5 points")

    st.subheader("🎮 Continue Learning")

    featured = ["Colours", "Counting", "Alphabet Adventure", "Math Challenge"]

    for start in range(0, len(featured), 2):
        cols = st.columns(2)
        for col, game in zip(cols, featured[start:start + 2]):
            icon, description, category = GAME_INFO[game]
            with col:
                st.markdown(f"""
                <div class="game-card">
                    <div class="big-emoji">{icon}</div>
                    <h3 style="text-align:center">{game}</h3>
                    <p style="text-align:center">{description}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button("Play Now ➜", key=f"home_{game}", use_container_width=True):
                    start_game(game)

    st.subheader("⭐ Your Practice Points")
    cols = st.columns(2)
    for i, game in enumerate(GAME_INFO):
        with cols[i % 2]:
            st.metric(f"{GAME_INFO[game][0]} {game}", st.session_state.scores[game])

    if st.button("🎮 See All Games", use_container_width=True):
        st.session_state.page = "Games"
        st.rerun()

# ==================================================
# LEARN
# ==================================================

elif st.session_state.page == "Learn":
    st.subheader("📚 Choose What to Learn")

    categories = {
        "🎨 Colours & Shapes": ["Colours", "Shapes"],
        "🔢 Numbers & Maths": ["Counting", "Math Challenge"],
        "🔤 Letters & Words": ["Alphabet Adventure", "Animal & Word Match"],
        "🌱 Science & Discovery": ["Little Scientist", "World Explorer"],
        "🧠 Brain Training": ["Memory"],
    }

    for category, games in categories.items():
        st.markdown(f"### {category}")
        cols = st.columns(2)

        for col, game in zip(cols, games):
            icon, description, _ = GAME_INFO[game]
            with col:
                st.markdown(f"""
                <div class="game-card">
                    <div class="big-emoji">{icon}</div>
                    <b>{game}</b>
                    <p class="small-note">{description}</p>
                </div>
                """, unsafe_allow_html=True)

                if st.button("Start ➜", key=f"learn_{game}", use_container_width=True):
                    start_game(game)

# ==================================================
# ALL GAMES
# ==================================================

elif st.session_state.page == "Games":
    st.subheader("🎮 All Learning Games")
    st.write("Choose a game and start your adventure!")

    cols = st.columns(2)

    for i, game in enumerate(GAME_INFO):
        icon, description, category = GAME_INFO[game]
        with cols[i % 2]:
            st.markdown(f"""
            <div class="game-card">
                <div class="big-emoji">{icon}</div>
                <h3 style="text-align:center">{game}</h3>
                <p style="text-align:center">{description}</p>
                <p class="small-note" style="text-align:center">{category}</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Play ➜", key=f"games_{game}", use_container_width=True):
                start_game(game)

# ==================================================
# COLOURS GAME
# ==================================================

elif st.session_state.page == "Colours":
    st.markdown("""
    <div class="hero">
        <div style="font-size:45px">🎨</div>
        <h2>Colour Quest</h2>
        <p>Find the colour and earn a star!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Back to Home", key="colour_home"):
        back_home()

    target = st.session_state.target_colour
    number = st.session_state.question_no["Colours"]

    st.subheader(f"Find the {target.title()} colour!")
    st.progress(((number - 1) % 5 + 1) / 5, text=f"Question {((number - 1) % 5) + 1} of 5")

    # The options are stored once and remain stable for this question.
    cols = st.columns(2)
    for i, colour in enumerate(st.session_state.colour_options):
        with cols[i % 2]:
            st.markdown(
                f'<div style="height:100px;background:{COLOURS[colour]};'
                'border-radius:18px;margin:5px 0;'
                'border:3px solid white;'
                'box-shadow:0 4px 10px #292F5915"></div>',
                unsafe_allow_html=True,
            )

            if st.button(
                f"Select {colour.title()}",
                key=f"colour_{number}_{colour}",
                use_container_width=True,
                disabled=st.session_state.answered["Colours"],
            ):
                submit_answer("Colours", colour == target)
                st.rerun()

    if st.session_state.answered["Colours"]:
        if st.session_state.feedback["Colours"] == "correct":
            st.success("🎉 Correct colour! +1 point")
            st.balloons()
        else:
            st.warning(f"Good try! The answer was {target.title()}.")

        if st.button("➡️ Next Question", key="colour_next", use_container_width=True):
            next_question("Colours")

    st.caption(f"⭐ Points: {st.session_state.scores['Colours']}")

# ==================================================
# QUIZ GAMES
# ==================================================

elif st.session_state.page in QUIZZES:
    render_quiz(st.session_state.page)

# ==================================================
# MEMORY GAME
# ==================================================

elif st.session_state.page == "Memory":
    st.markdown("""
    <div class="hero">
        <div style="font-size:45px">🧠</div>
        <h2>Memory Match</h2>
        <p>Find two matching animal cards!</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🏠 Back to Home", key="memory_home"):
        back_home()

    cards = st.session_state.memory_cards
    revealed = st.session_state.memory_revealed
    matched = st.session_state.memory_matched

    st.write(f"Pairs found: {len(matched) // 2} / 6")
    st.write(f"Turns: {st.session_state.memory_moves}")
    st.progress(len(matched) / len(cards) if cards else 0)

    if len(matched) == len(cards):
        st.success("🏆 Amazing! You found every pair!")
        st.balloons()

        if st.button("🔄 Play Again", use_container_width=True):
            reset_memory()
            st.rerun()
    else:
        cols = st.columns(3)

        for i, card in enumerate(cards):
            with cols[i % 3]:
                shown = i in revealed or i in matched
                label = card if shown else "❔"

                if st.button(
                    label,
                    key=f"memory_card_{i}",
                    use_container_width=True,
                    disabled=(i in matched or i in revealed),
                ):
                    # After a mismatch, the next click hides the old pair
                    # before revealing the newly selected card.
                    if len(revealed) == 2:
                        revealed.clear()

                    revealed.append(i)

                    if len(revealed) == 2:
                        first, second = revealed
                        st.session_state.memory_moves += 1

                        if cards[first] == cards[second]:
                            matched.extend(revealed)
                            revealed.clear()
                            st.session_state.scores["Memory"] += 1
                            st.session_state.memory_feedback = "correct"
                            sound_effect("correct")
                        else:
                            st.session_state.memory_feedback = "wrong"

                    st.rerun()

        if st.session_state.memory_feedback == "correct":
            st.success("🎉 Match found! +1 point")
        elif st.session_state.memory_feedback == "wrong":
            st.info("Not a match yet. Remember the cards and try again!")

        if st.button("🔀 Restart Memory
