import streamlit as st
from streamlit_lottie import st_lottie
import json
import random
from fractions import Fraction

st.set_page_config(page_title="Fraction Game", layout="centered")

# -----------------------------
# Load Lottie animation (LOCAL)
# -----------------------------
def load_lottie_file(filepath: str):
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error loading animation file '{filepath}': {e}")
        return None

teacher_animation = load_lottie_file("teacher_writing.json")

# -----------------------------
# Math helper functions
# -----------------------------
def fraction_to_decimal(frac: Fraction) -> float:
    return round(frac.numerator / frac.denominator, 3)

def decimal_to_fraction(dec: float) -> Fraction:
    return Fraction(dec).limit_denominator()

# -----------------------------
# Question generator
# -----------------------------
def generate_question(level: int):
    # Level 1: simple fractions/decimals
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

    # Level 2: harder proper fractions
    elif level == 2:
        frac = random.choice([
            Fraction(2, 5), Fraction(3, 8),
            Fraction(4, 5), Fraction(7, 10), Fraction(11, 20)
        ])
        if random.choice([True, False]):
            return f"Convert {frac} to Decimal:", fraction_to_decimal(frac)
        else:
            return f"Convert {fraction_to_decimal(frac)} to Fraction:", frac

    # Level 3: more tricky decimals
    elif level == 3:
        dec = random.choice([0.375, 0.625, 0.875])
        if random.choice([True, False]):
            return f"Convert {dec} to Fraction:", decimal_to_fraction(dec)
        else:
            return f"Convert {decimal_to_fraction(dec)} to Decimal:", float(dec)

# -----------------------------
# Session state initialization
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "question" not in st.session_state:
    st.session_state.question, st.session_state.answer = generate_question(1)

if "answer_input" not in st.session_state:
    st.session_state.answer_input = ""

# -----------------------------
# UI layout
# -----------------------------
st.title("🎮 Fraction ↔ Decimal Conversion Game")

col1, col2 = st.columns([1, 2])

with col1:
    if teacher_animation:
        st_lottie(teacher_animation, height=250)
    else:
        st.error("Teacher animation not found. Make sure 'teacher_writing.json' is in the same folder.")

with col2:
    st.write(f"### ⭐ Level: {st.session_state.level}")
    st.write(f"### 🧮 Score: {st.session_state.score}")

st.info("""
### 📝 Instructions

1. Look at the question the teacher shows on the board.  
2. Convert **fraction ↔ decimal** correctly.  
3. Type answers like: `1/2`, `3/4`, `0.25`, `0.5`  
4. ✅ If your answer is **correct**, a **new question** appears.  
5. ❌ If it is **wrong**, you can try again with the **same question**.
""")

st.markdown("---")

# Show current question
st.write(f"## ❓ {st.session_state.question}")

# Answer input (stored in session_state)
user_answer = st.text_input(
    "Your Answer:",
    key="answer_input",        # very important for stable behavior
    placeholder="Example: 1/2 or 0.5"
)

# -----------------------------
# Answer checking
# -----------------------------
if st.button("Submit"):
    correct = st.session_state.answer

    if not user_answer.strip():
        st.warning("Please type an answer before submitting.")
    else:
        try:
            is_correct = False

            # Expecting a fraction like 1/2
            if isinstance(correct, Fraction):
                user_fraction = Fraction(user_answer.replace(" ", ""))
                if user_fraction == correct:
                    is_correct = True

            # Expecting a decimal like 0.5
            else:
                user_decimal = float(user_answer)
                if abs(user_decimal - float(correct)) < 0.01:
                    is_correct = True

            if is_correct:
                st.success("🎉 Correct! Next question coming...")
                st.session_state.score += 1

                # Level up rules
                if st.session_state.score >= 5 and st.session_state.level == 1:
                    st.session_state.level = 2
                    st.success("⭐ Level Up → Level 2!")
                if st.session_state.score >= 12 and st.session_state.level == 2:
                    st.session_state.level = 3
                    st.success("🔥 Level Up → Level 3!")

                # Generate new question
                st.session_state.question, st.session_state.answer = generate_question(
                    st.session_state.level
                )

                # Clear input and rerun so the old answer is not reused
                st.session_state.answer_input = ""
                st.experimental_rerun()

            else:
                st.error("❌ Wrong answer. Try again with this question.")

        except Exception:
            st.error("⚠️ Invalid input. Use `1/2` for fractions or `0.5` for decimals.")

# -----------------------------
# Restart game
# -----------------------------
if st.button("🔄 Restart Game"):
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.question, st.session_state.answer = generate_question(1)
    st.session_state.answer_input = ""
    st.success("Game restarted!")
    st.experimental_rerun()
