
import random
import streamlit as st

st.set_page_config(
    page_title="Little Minds",
    page_icon="🌈",
    layout="centered"
)

# ================= CSS DESIGN =================

st.markdown("""
<style>
.stApp,
[data-testid="stAppViewContainer"] {
    background: #F3F5FF !important;
    color: #26315F !important;
}

.stApp h1,
.stApp h2,
.stApp h3,
.stApp p,
.stApp label,
.stApp [data-testid="stMarkdownContainer"] {
    color: #26315F !important;
}

h1 {
    text-align: center;
}

div.stButton > button {
    background: #FFFFFF !important;
    color: #26315F !important;
    border: 2px solid #D8DDFC !important;
    border-radius: 14px !important;
    min-height: 45px;
    font-weight: bold;
}

div.stButton > button:hover {
    background: #E7EAFE !important;
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


# ================= SESSION STATE =================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "scores" not in st.session_state:
    st.session_state.scores = {
        "Colours": 0,
        "Shapes": 0,
        "Counting": 0,
        "Memory": 0
    }

if "selected_colour" not in st.session_state:
    st.session_state.selected_colour = None


# ================= QUESTION SETUP =================

def setup_question(game):
    st.session_state.answered = False
    st.session_state.feedback = ""

    if game == "Colours":
        st.session_state.target = random.choice(
            list(COLOURS.keys())
        )
        st.session_state.selected_colour = None

    elif game == "Shapes":
        st.session_state.shape_target = random.choice(
            list(SHAPES.keys())
        )

    elif game == "Counting":
        st.session_state.count_target = random.randint(1, 5)
        st.session_state.count_item = random.choice(
            ["🍎", "⭐", "🐻", "🍓", "🦋"]
        )

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


def answer(correct, game):
    if st.session_state.answered:
        return

    if correct:
        st.session_state.scores[game] += 1
        st.session_state.feedback = "🎉 Correct! Well done!"
    else:
        st.session_state.feedback = "😊 Good try! Try again!"

    st.session_state.answered = True


def home_button():
    if st.button("🏠 Back to Home"):
        go_home()
        st.rerun()


# ================= HOME PAGE =================

st.title("🌈 LITTLE MINDS")

st.markdown(
    "<p style='text-align:center'>Play • Learn • Grow</p>",
    unsafe_allow_html=True
)

if st.session_state.page == "Home":

    st.subheader("Welcome, Little Explorer! ⭐")
    st.write("Choose any game you want to play!")

    left, right = st.columns(2)

    with left:
        st.markdown("### 🎨 Colours")

        if st.button("Play Colours", use_container_width=True):
            start_game("Colours")
            st.rerun()

        st.markdown("### 🔢 Counting")

        if st.button("Play Counting", use_container_width=True):
            start_game("Counting")
            st.rerun()

    with right:
        st.markdown("### 🔺 Shapes")

        if st.button("Play Shapes", use_container_width=True):
            start_game("Shapes")
            st.rerun()

        st.markdown("### 🧠 Memory")

        if st.button("Play Memory", use_container_width=True):
            start_game("Memory")
            st.rerun()

    st.divider()
    st.subheader("⭐ Your Practice Points")

    a, b = st.columns(2)
    c, d = st.columns(2)

    a.metric("🎨 Colours", st.session_state.scores["Colours"])
    b.metric("🔺 Shapes", st.session_state.scores["Shapes"])
    c.metric("🔢 Counting", st.session_state.scores["Counting"])
    d.metric("🧠 Memory", st.session_state.scores["Memory"])


# ================= COLOUR MATCHING =================

elif st.session_state.page == "Colours":

    home_button()
    st.header("🎨 Colour Matching")

    target = st.session_state.target

    st.subheader(f"Find the {target} colour!")

    st.write(
        f"Points: {st.session_state.scores['Colours']}"
    )

    # Fixed order: boxes won't move when an answer is selected.
    options = list(COLOURS.keys())

    cols = st.columns(2)

    for i, colour in enumerate(options):

        with cols[i % 2]:

            selected = (
                st.session_state.selected_colour == colour
            )

            border = (
                "5px solid #26315F"
                if selected
                else "3px solid white"
            )

            # Coloured box with selection highlight.
            st.markdown(
                f"""
                <div style="
                    background-color: {COLOURS[colour]};
                    height: 110px;
                    border-radius: 18px;
                    border: {border};
                    box-shadow: 0 3px 8px #0002;
                    margin-bottom: 8px;
                    box-sizing: border-box;
                "></div>
                """,
                unsafe_allow_html=True
            )

            # Clickable answer control.
            if st.button(
                f"Select {colour}",
                key=f"colour_{colour}",
                use_container_width=True,
                disabled=st.session_state.answered
            ):
                st.session_state.selected_colour = colour
                answer(colour == target, "Colours")
                st.rerun()

    if st.session_state.feedback:
        if st.session_state.feedback.startswith("🎉"):
            st.success(st.session_state.feedback)
        else:
            st.warning(st.session_state.feedback)

    if st.session_state.answered:
        if st.button(
            "➡️ Next Question",
            use_container_width=True
        ):
            next_question("Colours")
            st.rerun()


# ================= SHAPES =================

elif st.session_state.page == "Shapes":

    home_button()
    st.header("🔺 Shape Matching")

    target = st.session_state.shape_target

    st.write(f"Find the {target} shape!")
    st.markdown(f"# {SHAPES[target]}")

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

    if st.session_state.feedback:
        if st.session_state.feedback.startswith("🎉"):
            st.success(st.session_state.feedback)
        else:
            st.warning(st.session_state.feedback)

    if st.session_state.answered:
        if st.button(
            "➡️ Next Shape",
            use_container_width=True
        ):
            next_question("Shapes")
            st.rerun()


# ================= COUNTING =================

elif st.session_state.page == "Counting":

    home_button()
    st.header("🔢 Counting Fun")

    target = st.session_state.count_target
    item = st.session_state.count_item

    st.write("Count the objects!")

    st.markdown(
        f"""
        <div style="
            font-size:42px;
            text-align:center;
            background:white;
            border-radius:18px;
            padding:20px;
        ">
            {" ".join([item] * target)}
        </div>
        """,
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

    if st.session_state.feedback:
        if st.session_state.feedback.startswith("🎉"):
            st.success(st.session_state.feedback)
        else:
            st.warning(st.session_state.feedback)

    if st.session_state.answered:
        if st.button(
            "➡️ Next Question",
            use_container_width=True
        ):
            next_question("Counting")
            st.rerun()


# ================= MEMORY MATCH =================

elif st.session_state.page == "Memory":

    home_button()
    st.header("🧠 Memory Match")

    st.write("Find two matching animal cards!")

    cards = st.session_state.memory_cards
    revealed = st.session_state.memory_revealed
    matched = st.session_state.memory_matched

    if len(matched) == len(cards):

        st.success("🏆 Amazing! You found all the pairs!")

        if st.button(
            "🔄 Play Again",
            use_container_width=True
        ):
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

                                st.session_state.memory_feedback = (
                                    "🎉 Match found!"
                                )
                            else:
                                st.session_state.memory_feedback = (
                                    "Keep looking! Select another card."
                                )

                    st.rerun()

        st.write(
            f"Pairs found: {len(matched) // 2} / 4"
        )
        st.write(
            f"Turns: {st.session_state.memory_moves}"
        )

        if st.session_state.memory_feedback:
            st.info(st.session_state.memory_feedback)

        if st.button(
            "🔀 Restart Memory",
            use_container_width=True
        ):
            next_question("Memory")
            st.rerun()


# ================= FOOTER =================

st.divider()

st.caption(
    "🌟 Learn through play! Practice points are for fun, "
    "not a measure of intelligence."
)
