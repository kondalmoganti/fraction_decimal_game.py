import streamlit as st
from streamlit_lottie import st_lottie
import random
import json
from fractions import Fraction
from PIL import Image

st.set_page_config(page_title="Fraction Game", layout="centered")

# ----------------------------------------------------
# Load Lottie animation from LOCAL file
# ----------------------------------------------------
def load_lottie_file(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading animation file {filepath}: {e}")
        return None

# ----------------------------------------------------
# Avatars (local PNG files)
# ----------------------------------------------------
avatars = {
    "Boy Student": "avatar_boy1.png",
    "Girl Student": "avatar_girl1.png"
}

# Sidebar avatar selection
st.sidebar.title("🎓 Choose Your Avatar")
avatar_choice = st.sidebar.selectbox("Select Student Avatar:", list(avatars.keys()))

try:
    st.sidebar.image(avatars[avatar_choice], width=110)
except:
    st.sidebar.error("Avatar file missing!")

# ----------------------------------------------------
# Load teacher writing animation
# ----------------------------------------------------
teacher_animation = load_lottie_file("teacher_writing.json")

# ----------------------------------------------------
# Helper math functions
# ----------------------------------------------------
def fraction_to_decimal(frac):
    return round(frac.numerator / frac.denominator, 3)

def decimal_to_fraction(dec):
    return Fraction(dec).limit_denominator()

# ----------------------------------------------------
# Generate questions per level
# ----------------------------------------------------
def generate_question(level):
    if level == 1:
        if random.choice([True, False]):
            dec = random.choice([0.1, 0.2, 0.25, 0.5, 0.75])
            return f"Convert {dec} to Fraction:", decimal_to_fraction(dec)
        else:
            frac = random.choice([
                Fraction(1,10), Fraction(3,10), 
                Fraction(1,4), Fraction(1,2), Fraction(3,4)
            ])
            return f"Convert {frac} to Decimal:", fraction_to_decimal(frac)

    elif level == 2:
        frac = random.choice([
            Fraction(2,5), Fraction(3,8), Fraction(4,5),
            Fraction(7,10), Fraction(11,20)
        ])
        if random.choice([True, False]):
            return f"Convert {frac} to Decimal:", fraction_to_decimal(frac)
        else:
            return f"Convert {fraction_to_decimal(frac)} to Fraction:", frac

    elif level == 3:
        dec = random.choice([0.375, 0.625, 0.875])
        if random.choice([True, False]):
            return f"Convert {dec} to Fraction:", decimal_to_fraction(dec)
        else:
            return f"Convert {decimal_to_fraction(dec)} to Decimal:", float(dec)

# ----------------------------------------------------
# Session State Setup
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

col1, col2 = st.columns([1,2])

with col1:
    if teacher_animation:
        st_lottie(teacher_animation, height=250)
    else:
        st.error("Teacher animation missing!")

with col2:
    st.write(f"### ⭐ Level: {st.session_state.level}")
    st.write(f"### 🧮 Score: {st.session_state.score}")
    try:
        st.image(avatars[avatar_choice], width=120)
    except:
        st.warning("Avatar failed to load.")

st.info("""
### 📝 Instructions

1. A teacher will show a question on the board.  
2. Convert fraction ↔ decimal correctly.  
3. Type answers like: `1/2`, `3/4`, `0.25`, `0.5`  
4. **Correct answer = next question automatically**  
5. Wrong answer = try again  
""")

st.markdown("---")

# ----------------------------------------
# Show question
# ----------------------------------------
st.write(f"## ❓ {st.session_state.question}")

user_answer = st.text_input("Your Answer:")

# ----------------------------------------
# Submit Answer
# ----------------------------------------
if st.button("Submit"):
    correct = st.session_state.answer

    try:
        is_correct = False

        # Check fraction type
        if isinstance(correct, Fraction):
            if Fraction(user_answer.replace(" ", "")) == correct:
                is_correct = True
        else:
            if abs(float(user_answer) - float(correct)) < 0.01:
                is_correct = True

        if is_correct:
            st.success("🎉 Correct! Loading next question...")
            st.session_state.score += 1

            # Level up logic
            if st.session_state.score >= 5 and st.session_state.level == 1:
                st.session_state.level = 2
                st.success("⭐ Level Up → Level 2!")
            if st.session_state.score >= 12 and st.session_state.level == 2:
                st.session_state.level = 3
                st.success("🔥 Level Up → Level 3!")

            # Load new question
            st.session_state.question, st.session_state.answer = generate_question(
                st.session_state.level
            )

        else:
            st.error(f"❌ Wrong answer. Try again!")

    except:
        st.error("⚠️ Invalid input. Use formats like `1/2` or `0.25`.")

# ----------------------------------------
# Restart Game
# ----------------------------------------
if st.button("🔄 Restart Game"):
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.question, st.session_state.answer = generate_question(1)
    st.success("Game Restarted!")
