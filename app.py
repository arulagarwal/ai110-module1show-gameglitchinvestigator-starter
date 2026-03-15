import random
import streamlit as st
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
    load_high_score,
    save_high_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# All-time best score in sidebar
st.sidebar.divider()
st.sidebar.metric("🏆 All-Time Best Score", load_high_score())

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 1

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    # Each entry: {"Guess": ..., "Result": ..., "Score After": ...}
    st.session_state.history = []

# ---------------------------------------------------------------------------
# Main game area
# ---------------------------------------------------------------------------
st.subheader("Make a guess")

attempts_left = attempt_limit - st.session_state.attempts
st.info(
    f"Guess a number between **{low}** and **{high}**.  "
    f"Attempts left: **{attempts_left}**  |  Score: **{st.session_state.score}**"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

# ---------------------------------------------------------------------------
# New game reset
# ---------------------------------------------------------------------------
if new_game:
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.secret = random.randint(low, high)
    st.success("New game started.")
    st.rerun()

# ---------------------------------------------------------------------------
# End-state guard
# ---------------------------------------------------------------------------
if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

# ---------------------------------------------------------------------------
# Guess submission
# ---------------------------------------------------------------------------
if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append({
            "Guess": raw_guess,
            "Result": "Invalid",
            "Score After": st.session_state.score,
        })
        st.error(f"❌ {err}")
    else:
        outcome = check_guess(guess_int, st.session_state.secret)

        # Hot/cold proximity emoji
        distance = abs(guess_int - st.session_state.secret)
        if distance == 0:
            proximity = "🎯"
        elif distance <= 5:
            proximity = "🔥 Hot!"
        elif distance <= 15:
            proximity = "😐 Warm"
        else:
            proximity = "🧊 Cold"

        # Color-coded directional hint
        if show_hint:
            if outcome == "Win":
                st.success(f"🎉 Correct! {proximity}")
            elif outcome == "Too High":
                st.error(f"📉 Go LOWER!  {proximity}")
            else:
                st.warning(f"📈 Go HIGHER!  {proximity}")

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        st.session_state.history.append({
            "Guess": guess_int,
            "Result": outcome,
            "Score After": st.session_state.score,
        })

        if outcome == "Win":
            save_high_score(st.session_state.score)
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was **{st.session_state.secret}**.  "
                f"Final score: **{st.session_state.score}**"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                save_high_score(st.session_state.score)
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! The secret was **{st.session_state.secret}**.  "
                    f"Score: **{st.session_state.score}**"
                )

# ---------------------------------------------------------------------------
# Guess history table
# ---------------------------------------------------------------------------
if st.session_state.history:
    st.divider()
    st.subheader("📋 Guess History")
    valid_rows = [
        row for row in st.session_state.history if row["Result"] != "Invalid"
    ]
    if valid_rows:
        st.dataframe(
            valid_rows,
            use_container_width=True,
            hide_index=True,
        )

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
