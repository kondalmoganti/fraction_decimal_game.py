import streamlit as st
import random
import requests
from fractions import Fraction

st.set_page_config(page_title="Fraction <-> Decimal Game", page_icon="🎮", layout="centered")

# -------------------------
# Lottie Loader Function
# -------------------------
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

teacher_lottie = load_lottie_url(
    "https://assets4.lottiefiles.com/packages/lf20_p9vuwj4g.json"
)

# -------------------------
# Helper Functions
# -------------------------
def fraction_to_decimal(frac):
    return round(frac.numerator / frac.denominator, 3)

def decimal_to_fraction(dec):
    return Fraction(dec).limit_denominator()

def generate_question(level):
    if level == 1:
        if random.choice([True, False]):
            dec = round(random.choice([0.1, 0.2, 0.25, 0.5, 0.75]), 2)
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
            dec = fraction_to_decimal(frac)
            return f"Convert {dec} to Fraction:", frac

    elif level == 3:
        decimals_list = [0.375, 0.625, 0.875, 0.2, 0.4]
        dec = random.choice(decimals_list)
        if random.choice([True, False]):
            return f"Convert {dec} to Fraction:", decimal_to_fraction(dec)
        else:
            frac = decimal_to_fraction(dec)
            return f"Convert {frac} to Decimal:", float(dec)

# -------------------------
# Initial State
# -------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "level" not in st.session_state:
    st.session_state.level = 1
if "question" not in st.session_state:
    st.session_state.question, st.session_state.answer = generate_question(1)

# -------------------------
# UI Layout
# -------------------------

st.title("🎮 Fraction ↔ Decimal Conversion Game")

col1, col2 = st.columns([1,2])

with col1:
    st.write("### 👩‍🏫 Your Teacher")
    st.lottie(teacher_lottie, height=250)

with col2:
    st.subheader("Answer the math questions to level up!")
    st.write(f"### ⭐ Level: {st.session_state.level}")
    st.write(f"### 🧮 Score: {st.session_state.score}")

st.markdown("---")
st.write(f"## ❓ **{st.session_state.question}**")

# Answer Input
user_answer = st.text_input("Your Answer:")

# -------------------------
# Submit Button
# -------------------------

if st.button("Submit"):
    correct = st.session_state.answer
    try:
        if isinstance(correct, Fraction):      # expecting a fraction
            user_fraction = Fraction(user_answer.replace(" ", ""))
            if user_fraction == correct:
                st.success("🎉 Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Incorrect! Correct Answer: {correct}")

        else:                                  # expecting a decimal
            if abs(float(user_answer) - float(correct)) < 0.01:
                st.success("🎉 Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Incorrect! Correct Answer: {correct}")

    except:
        st.error("⚠️ Invalid input. Please try again!")

    # Level Up Logic
    if st.session_state.score >= 5 and st.session_state.level == 1:
        st.session_state.level = 2
        st.success("🌟 **LEVEL UP → Level 2**")

    elif st.session_state.score >= 12 and st.session_state.level == 2:
        st.session_state.level = 3
        st.success("🔥 **LEVEL UP → Level 3** (Hard Mode!)")

    # New Question
    st.session_state.question, st.session_state.answer = generate_question(st.session_state.level)

# Restart
if st.button("🔄 Restart Game"):
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.question, st.session_state.answer = generate_question(1)
    st.success("Game restarted!")

