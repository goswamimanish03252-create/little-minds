
import random
import streamlit as st

st.set_page_config(
    page_title="Little Minds",
    page_icon="🌈",
    layout="centered"
)

st.markdown("""
<style>
.stApp {
    background-color: #F3F5FF;
}
h1 {
    color: #343A78;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

st.title("🌈 LITTLE MINDS")
st.markdown(
    "<p style='text-align:center'>Play • Learn • Grow</p>",
    unsafe_allow_html=True
)

st.subheader("Welcome, Little Explorer! ⭐")
st.write("Choose a colour game and have fun!")

COLOURS = {
    "RED": "#F04444",
    "BLUE": "#4285F4",
    "GREEN": "#36A66A",
    "YELLOW": "#F5C542"
}

if "target" not in st.session_state:
    st.session_state.target = random.choice(list(COLOURS))
    st.session_state.score = 0
    st.session_state.question = 1
    st.session_state.answered = False
    st.session_state.feedback = ""

def new_question():
    st.session_state.target = random.choice(list(COLOURS))
    st.session_state.question += 1
    st.session_state.answered = False
    st.session_state.feedback = ""

def choose_colour(colour):
    if st.session_state.answered:
        return

    if colour == st.session_state.target:
        st.session_state.score += 1
        st.session_state.feedback = "Correct! ⭐ Well done!"
    else:
        st.session_state.feedback = "Not quite! Try the next turn."

    st.session_state.answered = True

st.markdown("---")
st.subheader("🎨 Colour Matching")

st.write(
    f"Question {st.session_state.question} | "
    f"Score: {st.session_state.score}"
)

target = st.session_state.target
st.markdown(f"### Find the **{target}** colour!")

st.markdown(
    f"<div style='background:{COLOURS[target]};"
    "height:90px;border-radius:18px;margin:15px 0'></div>",
    unsafe_allow_html=True
)

options = list(COLOURS.keys())
random.Random(st.session_state.question).shuffle(options)
columns = st.columns(2)

for i, colour in enumerate(options):
    with columns[i % 2]:
        st.markdown(
            f"<div style='background:{COLOURS[colour]};"
            "padding:12px;border-radius:12px;"
            "text-align:center;font-weight:bold'>"
            f"{colour}</div>",
            unsafe_allow_html=True
        )
        st.button(
            f"Choose {colour}",
            key=f"colour_{colour}",
            use_container_width=True,
            disabled=st.session_state.answered,
            on_click=choose_colour,
            args=(colour,)
        )

if st.session_state.feedback:
    st.info(st.session_state.feedback)

if st.session_state.answered:
    st.button(
        "Next Question ➜",
        on_click=new_question,
        use_container_width=True
    )

st.caption(
    "Little Minds helps children practise through play. "
    "Game scores are not a measure of intelligence."
)

