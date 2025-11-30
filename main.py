import streamlit as st
from streamlit_lottie import st_lottie
import requests, random
from fractions import Fraction
from PIL import Image

st.set_page_config(page_title="Fraction Game", layout="wide")

# -----------------------------------------------------
# CUSTOM CSS FOR ANIMATED BACKGROUND
# -----------------------------------------------------
page_bg = """
<style>
body {
    background-image: url("https://i.gifer.com/ZZ5H.gif");
    background-size: cover;
    animation: fadein 2s;
}
@keyframes fadein {
    from {opacity: 0;} 
    to {opacity: 1;}
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

import json
import random
from streamlit_lottie import st_lottie

# ----------------------------------------------------
# Load Lottie animation from LOCAL file
# ----------------------------------------------------
def load_lottie_file(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception:
        return None

# ----------------------------------------------------
# Local teacher animation JSON files
# ----------------------------------------------------
teacher_list = [
    "teacher1.json",
    "teacher2.json",
    "teacher3.json"
]

# ----------------------------------------------------
# Choose and load animation
# ----------------------------------------------------
selected_animation = random.choice(teacher_list)
teacher_animation = load_lottie_file(selected_animation)

# ----------------------------------------------------
# Display animation
# ----------------------------------------------------
if teacher_animation:
    st_lottie(teacher_animation, height=250)
else:
    st.warning("⚠️ Teacher animation failed to load. Make sure JSON files exist!")

# -----------------------------------------------------
# SOUND EFFECTS
# -----------------------------------------------------
correct_sound = "https://assets.mixkit.co/sfx/preview/mixkit-video-game-win-2016.mp3"
wrong_sound = "https://assets.mixkit.co/sfx/preview/mixkit-wrong-answer-fail-notification-946.mp3"

def play_sound(url):
    st.markdown(f"""
    <audio autoplay>
        <source src="{url}">
    </audio>
    """, unsafe_allow_html=True)

# -----------------------------------------------------
# STUDENT AVATARS
# -----------------------------------------------------
student_avatars = {
    "Boy 1": "https://i.imgur.com/3x4Hf0b.png",
    "Boy 2": "https://i.imgur.com/aLX1Rr2.png",
    "Girl 1": "https://i.imgur.com/6a9nM8a.png",
    "Girl 2": "https://i.imgur.com/YL9fK1R.png"
}

st.sidebar.title("🧑‍🎓 Choose Your Avatar")
avatar_choice = st.sidebar.selectbox("Select:", list(student_avatars.keys()))
st.sidebar.image(student_avatars[avatar_choice], width=120)

# -----------------------------------------------------
# FRACTION/DECIMAL HELPERS
# -----------------------------------------------------
def fraction_to_decimal(frac):
    return round(frac.numerator / frac.denominator, 3)

def decimal_to_fraction(dec):
    return Fraction(dec).limit_denominator()

# -----------------------------------------------------
# QUESTION GENERATOR
# -----------------------------------------------------
def generate_question(level):
    if level == 1:
        if random.choice([True, False]):
            dec = random.choice([0.1, 0.2, 0.25, 0.5, 0.75])
            return f"Convert {dec} to Fraction:", decimal_to_fraction(dec)
        else:
            frac = random.choice([Fraction(1,10), Fraction(3,10), Fraction(1,4), Fraction(1,2), Fraction(3,4)])
            return f"Convert {frac} to Decimal:", fraction_to_decimal(frac)

    elif level == 2:
        fractions_list = [Fraction(2,5), Fraction(3,8), Fraction(4,5), Fraction(7,10), Fraction(11,20)]
        frac = random.choice(fractions_list)
        if random.choice([True, False]):
            return f"Convert {frac} to Decimal:", fraction_to_decimal(frac)
        else:
            return f"Convert {fraction_to_decimal(frac)} to Fraction:", frac

    elif level == 3:
        decimals_list = [0.375, 0.625, 0.875, 0.2, 0.4]
        dec = random.choice(decimals_list)
        if random.choice([True, False]):
            return f"Convert {dec} to Fraction:", decimal_to_fraction(dec)
        else:
            return f"Convert {decimal_to_fraction(dec)} to Decimal:", float(dec)

# -----------------------------------------------------
# SESSION STATE
# -----------------------------------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "question" not in st.session_state:
    st.session_state.question, st.session_state.answer = generate_question(1)

# -----------------------------------------------------
# UI HEADER
# -----------------------------------------------------

st.title("🎮 Fraction ↔ Decimal Conversion Game")

# Random teacher animation
teacher_animation = load_lottie_url(random.choice(teacher_list))

col1, col2 = st.columns([1,2])
with col1:
    st_lottie(teacher_animation, height=250)

with col2:
    st.write(f"### ⭐ Level: {st.session_state.level}")
    st.write(f"### 🧮 Score: {st.session_state.score}")
    st.write(f"### 👨‍🎓 Player: **{avatar_choice}**")
    st.image(student_avatars[avatar_choice], width=120)

st.markdown("---")
st.write(f"## ❓ {st.session_state.question}")

# -----------------------------------------------------
# ANSWER BOX
# -----------------------------------------------------
user_answer = st.text_input("Your Answer:")

if st.button("Submit"):
    correct = st.session_state.answer

    try:
        if isinstance(correct, Fraction):
            user_fraction = Fraction(user_answer.replace(" ", ""))
            if user_fraction == correct:
                st.success("🎉 Correct!")
                play_sound(correct_sound)
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct: {correct}")
                play_sound(wrong_sound)
        else:
            if abs(float(user_answer) - float(correct)) < 0.01:
                st.success("🎉 Correct!")
                play_sound(correct_sound)
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct: {correct}")
                play_sound(wrong_sound)

    except:
        st.error("⚠️ Invalid input!")

    # Level up rules
    if st.session_state.score >= 5 and st.session_state.level == 1:
        st.session_state.level = 2
        st.success("🌟 LEVEL UP → Level 2")
    elif st.session_state.score >= 12 and st.session_state.level == 2:
        st.session_state.level = 3
        st.success("🔥 LEVEL UP → Level 3 (Hard Mode!)")

    # Load new question + new teacher animation
    st.session_state.question, st.session_state.answer = generate_question(st.session_state.level)


if st.button("🔄 Restart Game"):
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.question, st.session_state.answer = generate_question(1)
    st.success("Game Restarted!")
