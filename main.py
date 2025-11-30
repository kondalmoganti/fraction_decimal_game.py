import streamlit as st
from streamlit_lottie import st_lottie
import random
import json
from fractions import Fraction
from PIL import Image

st.set_page_config(page_title="Fraction Game", layout="centered")

# ----------------------------------------------------
# Load local Lottie animation
# ----------------------------------------------------
def load_lottie_file(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading {filepath}: {e}")
        return None

# ----------------------------------------------------
# Teacher animations (local JSON files)
# ----------------------------------------------------
teacher_files = ["teacher1.json", "teacher2.json", "teacher3.json"]

# ----------------------------------------------------
# Student Avatars
# ----------------------------------------------------
avatars = {
    "Boy Student": "avatar_boy1.png",
    "Girl Student": "avatar_girl1.png"
}

# Sidebar avatar selection
st.sidebar.title("🎓 Choose Your Avatar")
avatar_choice = st.sidebar.selectbox("Select Avatar:", list(avatars.keys()))
st.sidebar.image(avatars[avatar_choice], width=120)

# ----------------------------------------------------
# Helper functions: fraction + decimal
# ----------------------------------------------------
def fraction_to_decimal(frac):
    return round(frac.numerator / frac.denominator, 3)

def decimal_to_fraction(dec):
    return Fraction(dec).limit_denominator()

# ----------------------------------------------------
# Question generator
# ----------------------------------------------------
def generate_question(level):
    if level == 1:
        if random.choice([True, False]):
            dec = random.choice([0.1, 0.2, 0.25, 0.5, 0.75])
            return f"Convert {dec} to Fraction:", decimal_to_fraction(dec)
        else:
            frac = random.choice([
                Fraction(1, 10), Fraction(3, 10),
                Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)
            ])
            return f"Convert {frac} to Decimal:", fraction_to_decimal(frac)

    elif level == 2:
        fractions_list = [Fraction(2, 5), Fraction(3, 8),
                          Fraction(4, 5), Fraction(7, 10), Fraction(11, 20)]
        frac = random.choice(fractions_list)
        if random.choice([True, False]):
            return f"Convert {frac} to Decimal:", fraction_to_decimal(frac)
        else:
            return f"Convert {fraction_to_decimal(frac)} to Fraction:", frac

    elif level == 3:
        decimals_list = [0.375, 0.625, 0.875]
        dec = random.choice(decimals_list)
        if random.choice([True, False]):
            return f"Convert {dec} to Fraction:", decimal_to_fraction(dec)
        else:
            return f"Convert {decimal_to_fraction(dec)} to Decimal:", float(dec)

# ----------------------------------------------------
# Init session state
# ----------------------------------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "question" not in st.session_state:
    st.session_state.question, st.session_state.answer = generate_question(1)

# ----------------------------------------------------
# UI Layout
# ----------------------------------------------------
st.title("🎮 Fraction ↔ Decimal Conversion Game")

# Random teacher animation
selected_teacher = random.choice(teacher_files)
teacher_animation = load_lottie_file(selected_teacher)

col1, col2 = st.columns([1, 2])

with col1:
    if teacher_animation:
        st_lottie(teacher_animation, height=240)
    else:
        st.error("Teacher animation failed to load.")

with col2:
    st.write(f"### ⭐ Level: {st.session_state.level}")
    st.write(f"### 🧮 Score: {st.session_state.score}")
    st.image(avatars[avatar_choice], width=120)

st.markdown("---")

# Show Question
st.write(f"## ❓ {st.session_state.question}")

# User Answer
user_answer = st.text_input("Your Answer:")

# ----------------------------------------------------
# Submit
# ----------------------------------------------------
if st.button("Submit"):
    correct = st.session_state.answer

    try:
        if isinstance(correct, Fraction):
            if Fraction(user_answer.replace(" ", "")) == correct:
                st.success("🎉 Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct: {correct}")

        else:  # decimal
            if abs(float(user_answer) - float(correct)) < 0.01:
                st.success("🎉 Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct: {correct}")

    except:
        st.error("⚠️ Invalid input format.")

    # Leveling
    if st.session_state.score >= 5 and st.session_state.level == 1:
        st.session_state.level = 2
        st.success("⭐ Level Up → Level 2!")

    if st.session_state.score >= 12 and st.session_state.level == 2:
        st.session_state.level = 3
        st.success("🔥 Level Up → Level 3!")

    st.session_state.question, st.session_state.answer = generate_question(st.session_state.level)

# ----------------------------------------------------
# Restart Game
# ----------------------------------------------------
if st.button("🔄 Restart"):
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.question, st.session_state.answer = generate_question(1)
    st.success("Game Restarted!")
