
import random
import streamlit as st

st.set_page_config(
    page_title="Little Minds",
    page_icon="🌈",
    layout="centered"
)

# ================= CARTOON DESIGN =================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #FFF8E8 0%, #F0F4FF 100%);
    color: #30345B;
}

[data-testid="stHeader"] {
    background: transparent;
}

h1, h2, h3, p, label {
    color: #30345B;
}

h1 {
    text-align: center;
    font-weight: 900;
}

div.stButton > button {
    background: white;
    color: #30345B;
    border: 2px solid #D8DDFC;
    border-radius: 18px;
    min-height: 48px;
    font-weight: 800;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    background: #E9EFFF;
    border-color: #8798F5;
    transform: translateY(-2px);
}

div[data-testid="stMetric"] {
    background: white;
    border: 2px solid #E2E6FF;
    padding: 15px;
    border-radius: 18px;
}

.game-card {
    background: white;
    border: 3px solid #E2E6FF;
    border-radius: 22px;
    padding: 18px;
    text-align: center;
    margin: 5px 0 12px 0;
    box-shadow: 0 4px 10px #30345B10;
}

.big-emoji {
    font-size: 54px;
    text-align: center;
    padding: 12px;
}

.question-box {
    background: white;
    border: 3px solid #D8DDFC;
    border-radius: 22px;
    padding: 20px;
    text-align: center;
    margin: 12px 0;
}

.badge-card {
    background: #FFF0B8;
    border: 2px solid #F3CE60;
    border-radius: 16px;
    padding: 12px;
    text-align: center;
}

div.st-key-colour_RED button {
    background: #F04444 !important;
    border: 4px solid #FFFFFF !important;
    height: 105px !important;
    color: transparent !important;
    font-size: 0 !important;
}
div.st-key-colour_BLUE button {
    background: #4285F4 !important;
    border: 4px solid #FFFFFF !important;
    height: 105px !important;
    color: transparent !important;
    font-size: 0 !important;
}
div.st-key-colour_GREEN button {
    background: #36A66A !important;
    border: 4px solid #FFFFFF !important;
    height: 105px !important;
    color: transparent !important;
    font-size: 0 !important;
}
div.st-key-colour_YELLOW button {
    background: #F5C542 !important;
    border: 4px solid #FFFFFF !important;
    height: 105px !important;
    color: transparent !important;
    font-size: 0 !important;
}

div.st-key-colour_RED button:hover,
div.st-key-colour_BLUE button:hover,
div.st-key-colour_GREEN button:hover,
div.st-key-colour_YELLOW button:hover {
    filter: brightness(0.92);
    transform: scale(1.02);
}

div.st-key-colour_RED button:focus,
div.st-key-colour_BLUE button:focus,
div.st-key-colour_GREEN button:focus,
div.st-key-colour_YELLOW button:focus {
    border: 5px solid #30345B !important;
    outline: 3px solid #FFFFFF !important;
}

.stProgress > div > div > div {
    background: #8A83F7;
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


# ================= GAME DATA =================

COLOURS = {
    "RED": "#F04444",
    "BLUE": "#4285F4",
    "GREEN": "#36A66A",
    "YELLOW": "#F5C542"
}

SHAPES = {
    "CIRCLE": "🔵",
    "SQUARE": "🟦",
    "TRIANGLE": "🔺",
    "STAR": "⭐"
}

ALPHABET = {
    "A": ("🍎", "Apple"),
    "B": ("⚽", "Ball"),
    "C": ("🐱", "Cat"),
    "D": ("🐶", "Dog"),
    "E": ("🥚", "Egg"),
    "F": ("🐟", "Fish"),
    "G": ("🍇", "Grapes"),
    "H": ("🏠", "House"),
    "I": ("🍦", "Ice cream"),
    "J": ("🧃", "Juice"),
    "K": ("🪁", "Kite"),
    "L": ("🦁", "Lion"),
    "M": ("🥭", "Mango"),
    "N": ("🥜", "Nuts"),
    "O": ("🍊", "Orange"),
    "P": ("🍍", "Pineapple"),
    "Q": ("👸", "Queen"),
    "R": ("🌈", "Rainbow"),
    "S": ("☀️", "Sun"),
    "T": ("🐯", "Tiger"),
    "U": ("☂️", "Umbrella"),
    "V": ("🚐", "Van"),
    "W": ("⌚", "Watch"),
    "X": ("🎼", "Xylophone"),
    "Y": ("🪀", "Yo-yo"),
    "Z": ("🦓", "Zebra")
}

WORDS = {
    "Apple": "🍎",
    "Ball": "⚽",
    "Cat": "🐱",
    "Dog": "🐶",
    "Fish": "🐟",
    "Lion": "🦁",
    "Mango": "🥭",
    "Sun": "☀️",
    "Tiger": "🐯",
    "Star": "⭐"
}

GAMES = ["Colours", "Shapes", "Counting", "Memory",
         "ABC", "Maths", "Word Matching"]

# ================= SESSION STATE =================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "scores" not in st.session_state:
    st.session_state.scores = {game: 0 for game in GAMES}

if "stars" not in st.session_state:
    st.session_state.stars = 0

if "answered" not in st.session_state:
    st.session_state.answered = False

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "selected_colour" not in st.session_state:
    st.session_state.selected_colour = None

if "last_celebration" not in st.session_state:
    st.session_state.last_celebration = False


# ================= BADGES =================

def get_badge(stars):
    if stars >= 50:
        return "🏆 Gold Champion"
    elif stars >= 25:
        return "🥈 Silver Star"
    elif stars >= 10:
        return "🥉 Bronze Star"
    elif stars >= 5:
        return "🌟 Rising Star"
    return "🌱 Beginner"


def show_progress():
    stars = st.session_state.stars

    st.subheader("⭐ Your Achievements")

    a, b = st.columns(2)
    a.metric("Total Stars", f"⭐ {stars}")
    b.metric("Current Badge", get_badge(stars))

    if stars < 5:
        next_goal = 5
    elif stars < 10:
        next_goal = 10
    elif stars < 25:
        next_goal = 25
    elif stars < 50:
        next_goal = 50
    else:
        next_goal = 50

    if stars < 50:
        st.progress(min(stars / next_goal, 1.0))
        st.caption(
            f"{max(0, next_goal - stars)} more stars "
            "to unlock the next badge!"
        )
    else:
        st.success("🏆 You unlocked the Gold Champion badge!")


# ================= QUESTION SETUP =================

def setup_question(game):
    st.session_state.answered = False
    st.session_state.feedback = ""
    st.session_state.last_celebration = False

    if game == "Colours":
        st.session_state.target = random.choice(list(COLOURS))
        st.session_state.selected_colour = None

    elif game == "Shapes":
        st.session_state.shape_target = random.choice(list(SHAPES))

    elif game == "Counting":
        st.session_state.count_target = random.randint(1, 5)
        st.session_state.count_item = random.choice(
            ["🍎", "⭐", "🐻", "🍓", "🦋"]
        )

    elif game == "ABC":
        st.session_state.abc_target = random.choice(list(ALPHABET))
        options = [st.session_state.abc_target]
        options += random.sample(
            [letter for letter in ALPHABET
             if letter != st.session_state.abc_target],
            3
        )
        random.shuffle(options)
        st.session_state.abc_options = options

    elif game == "Maths":
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        operator = random.choice(["+", "-"])

        if operator == "-" and y > x:
            x, y = y, x

        correct = x + y if operator == "+" else x - y

        choices = {correct}
        while len(choices) < 4:
            choices.add(max(0, correct + random.randint(-5, 5)))

        st.session_state.math_x = x
        st.session_state.math_y = y
        st.session_state.math_operator = operator
        st.session_state.math_target = correct
        st.session_state.math_options = list(choices)
        random.shuffle(st.session_state.math_options)

    elif game == "Word Matching":
        word = random.choice(list(WORDS))
        st.session_state.word_target = word

        other_words = [w for w in WORDS if w != word]
        options = [word] + random.sample(other_words, 3)
        random.shuffle(options)
        st.session_state.word_options = options

    elif game == "Memory":
        st.session_state.memory_cards = (
            ["🐶", "🐱", "🐸", "🦊"] * 2
        )
        random.shuffle(st.session_state.memory_cards)
        st.session_state.memory_revealed = []
        st.session_state.memory_matched = []
        st.session_state.memory_moves = 0
        st.session_state.memory_feedback = ""


def start_game(game):
    st.session_state.page = game
    setup_question(game)


def go_home():
    st.session_state.page = "Home"


def next_question(game):
    setup_question(game)


# ================= ANSWER HANDLING =================

def answer(correct, game):
    if st.session_state.answered:
        return

    if correct:
        st.session_state.scores[game] += 1
        st.session_state.stars += 1
        st.session_state.feedback = "🎉 Correct! +1 Star!"
        st.session_state.last_celebration = True
    else:
        st.session_state.feedback = "😊 Good try! Try again!"
        st.session_state.last_celebration = False

    st.session_state.answered = True


def show_feedback():
    if st.session_state.feedback:
        if st.session_state.last_celebration:
            st.success(st.session_state.feedback)
            st.balloons()
        else:
            st.warning(st.session_state.feedback)


def home_button():
    if st.button("🏠 Back to Home", key="back_home"):
        go_home()
        st.rerun()


def show_next(game, label="➡️ Next Question"):
    if st.session_state.answered:
        if st.button(label, use_container_width=True):
            next_question(game)
            st.rerun()


# ================= HEADER =================

st.title("🌈 LITTLE MINDS")
st.markdown(
    "<p style='text-align:center;font-size:18px'>"
    "🎨 Play • 📚 Learn • 🌟 Grow</p>",
    unsafe_allow_html=True
)


# ================= HOME PAGE =================

if st.session_state.page == "Home":

    st.markdown("""
    <div class="game-card">
        <div style="font-size:55px">🧸 🌈 🦄</div>
        <h2>Welcome, Little Explorer!</h2>
        <p>Let's play, learn and earn stars!</p>
    </div>
    """, unsafe_allow_html=True)

    show_progress()

    st.divider()
    st.subheader("🎮 Choose Your Game")

    cards = [
        ("Colours", "🎨", "Learn colours"),
        ("Shapes", "🔺", "Explore shapes"),
        ("Counting", "🔢", "Count objects"),
        ("Memory", "🧠", "Match animal cards"),
        ("ABC", "🔤", "Learn A to Z"),
        ("Maths", "➕", "Solve sums"),
        ("Word Matching", "🧩", "Match words")
    ]

    for start in range(0, len(cards), 2):
        cols = st.columns(2)

        for j, (game, emoji, description) in enumerate(
            cards[start:start + 2]
        ):
            with cols[j]:
                st.markdown(
                    f"""
                    <div class="game-card">
                        <div style="font-size:42px">{emoji}</div>
                        <h3>{game}</h3>
                        <p>{description}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                if st.button(
                    f"Play {game} ▶️",
                    key=f"play_{game}",
                    use_container_width=True
                ):
                    start_game(game)
                    st.rerun()

    st.divider()
    st.subheader("📊 Your Practice Points")

    cols = st.columns(2)
    for i, game in enumerate(GAMES):
        with cols[i % 2]:
            st.metric(game, st.session_state.scores[game])

    st.caption(
        "🌟 Learn through play! Everyone learns at their own pace."
    )


# ================= COLOURS =================

elif st.session_state.page == "Colours":

    home_button()
    st.header("🎨 Colour Matching")

    target = st.session_state.target

    st.markdown(
        f"<div class='question-box'>"
        f"<h2>Find the {target} colour!</h2>"
        f"<p>Tap the correct colour below.</p></div>",
        unsafe_allow_html=True
    )

    options = list(COLOURS)
    random.Random(target).shuffle(options)
    cols = st.columns(2)

    for i, colour in enumerate(options):
        with cols[i % 2]:
            selected = st.session_state.selected_colour == colour

            # Show selection border without changing the colour.
            if selected:
                st.markdown(
                    f"""<style>
                    div.st-key-colour_{colour} button {{
                        border: 6px solid #30345B !important;
                        outline: 3px solid white !important;
                    }}
                    </style>""",
                    unsafe_allow_html=True
                )

            if st.button(
                " ",
                key=f"colour_{colour}",
                use_container_width=True,
                disabled=st.session_state.answered
            ):
                st.session_state.selected_colour = colour
                answer(colour == target, "Colours")
                st.rerun()

    show_feedback()
    show_next("Colours")


# ================= SHAPES =================

elif st.session_state.page == "Shapes":

    home_button()
    st.header("🔺 Shape Matching")

    target = st.session_state.shape_target

    st.markdown(
        f"<div class='question-box'><h3>"
        f"Find the {target} shape!</h3>"
        f"<div class='big-emoji'>{SHAPES[target]}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    cols = st.columns(2)

    for i, shape in enumerate(SHAPES):
        with cols[i % 2]:
            if st.button(
                f"{SHAPES[shape]} {shape}",
                key=f"shape_{shape}",
                use_container_width=True,
                disabled=st.session_state.answered
            ):
                answer(shape == target, "Shapes")
                st.rerun()

    show_feedback()
    show_next("Shapes", "➡️ Next Shape")


# ================= COUNTING =================

elif st.session_state.page == "Counting":

    home_button()
    st.header("🔢 Counting Fun")

    target = st.session_state.count_target
    item = st.session_state.count_item

    st.markdown(
        f"""<div class="question-box">
        <h3>Count the objects!</h3>
        <div style="font-size:43px;line-height:1.8">
        {" ".join([item] * target)}
        </div></div>""",
        unsafe_allow_html=True
    )

    st.write("How many objects are there?")
    cols = st.columns(5)

    for number in range(1, 6):
        with cols[number - 1]:
            if st.button(
                str(number),
                key=f"number_{number}",
                use_container_width=True,
                disabled=st.session_state.answered
            ):
                answer(number == target, "Counting")
                st.rerun()

    show_feedback()
    show_next("Counting")


# ================= MEMORY MATCH =================

elif st.session_state.page == "Memory":

    home_button()
    st.header("🧠 Memory Match")
    st.write("Find matching pairs of animal cards!")

    cards = st.session_state.memory_cards
    revealed = st.session_state.memory_revealed
    matched = st.session_state.memory_matched

    if len(matched) == len(cards):

        st.success("🏆 Amazing! You found all the pairs!")
        st.balloons()

        if st.button("🔄 Play Again", use_container_width=True):
            next_question("Memory")
            st.rerun()

    else:

        cols = st.columns(4)

        for i, card in enumerate(cards):
            with cols[i % 4]:
                if i in matched or i in revealed:
                    label = card
                else:
                    label = "❔"

                if st.button(
                    label,
                    key=f"memory_{i}",
                    use_container_width=True,
                    disabled=(i in matched)
                ):
                    if i not in matched and i not in revealed:

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
                                st.session_state.stars += 1
                                st.session_state.memory_feedback = (
                                    "🎉 Match found! +1 Star!"
                                )
                            else:
                                st.session_state.memory_feedback = (
                                    "Keep looking! Try another pair."
                                )

                    st.rerun()

        st.write(f"Pairs found: {len(matched) // 2} / 4")
        st.write(f"Turns: {st.session_state.memory_moves}")

        if st.session_state.memory_feedback:
            st.info(st.session_state.memory_feedback)

        if st.button("🔀 Restart Memory", use_container_width=True):
            next_question("Memory")
            st.rerun()


# ================= ABC ALPHABET =================

elif st.session_state.page == "ABC":

    home_button()
    st.header("🔤 ABC Alphabet Adventure")

    target = st.session_state.abc_target
    emoji, word = ALPHABET[target]

    st.markdown(
        f"""<div class="question-box">
        <h3>Find the letter {target}!</h3>
        <div style="font-size:60px">{emoji}</div>
        <h3>{word}</h3>
        <p>Which letter starts this word?</p>
        </div>""",
        unsafe_allow_html=True
    )

    cols = st.columns(2)

    for i, letter in enumerate(st.session_state.abc_options):
        with cols[i % 2]:
            if st.button(
                letter,
                key=f"abc_{letter}",
                use_container_width=True,
                disabled=st.session_state.answered
            ):
                answer(letter == target, "ABC")
                st.rerun()

    show_feedback()
    show_next("ABC", "➡️ Next Letter")


# ================= MATHS CHALLENGE =================

elif st.session_state.page == "Maths":

    home_button()
    st.header("➕ Maths Challenge")

    x = st.session_state.math_x
    y = st.session_state.math_y
    operator = st.session_state.math_operator

    st.markdown(
        f"""<div class="question-box">
        <h3>Solve this!</h3>
        <div style="font-size:55px;font-weight:900">
        {x} {operator} {y} = ?
        </div>
        <p>Choose the correct answer.</p>
        </div>""",
        unsafe_allow_html=True
    )

    cols = st.columns(2)

    for i, number in enumerate(st.session_state.math_options):
        with cols[i % 2]:
            if st.button(
                str(number),
                key=f"math_{number}",
                use_container_width=True,
                disabled=st.session_state.answered
            ):
                answer(number == st.session_state.math_target, "Maths")
                st.rerun()

    show_feedback()
    show_next("Maths", "➡️ Next Sum")


# ================= WORD MATCHING =================

elif st.session_state.page == "Word Matching":

    home_button()
    st.header("🧩 Word Matching")

    target = st.session_state.word_target
    emoji = WORDS[target]

    st.markdown(
        f"""<div class="question-box">
        <h3>Which word matches this picture?</h3>
        <div style="font-size:75px">{emoji}</div>
        <p>Choose the correct English word.</p>
        </div>""",
        unsafe_allow_html=True
    )

    cols = st.columns(2)

    for i, word in enumerate(st.session_state.word_options):
        with cols[i % 2]:
            if st.button(
                word,
                key=f"word_{word}",
                use_container_width=True,
                disabled=st.session_state.answered
            ):
                answer(word == target, "Word Matching")
                st.rerun()

    show_feedback()
    show_next("Word Matching", "➡️ Next Word")


# ================= FOOTER =================

st.divider()

st.markdown(
    "<p style='text-align:center'>"
    "🌈 Little Minds • Play • Learn • Grow ⭐"
    "</p>",
    unsafe_allow_html=True
)
