import streamlit as st
import random
from fractions import Fraction

st.set_page_config(page_title="Fraction <-> Decimal Game", page_icon="🎮")

# ------------------------------
# Helper Functions
# ------------------------------

def fraction_to_decimal(frac):
    return round(frac.numerator / frac.denominator, 3)

def decimal_to_fraction(dec):
    return Fraction(dec).limit_denominator()

def generate_question(level):
    if level == 1:
        # Simple tenths / hundredths
        if random.choice([True, False]):
            # decimal to fraction
            dec = round(random.choice([0.1, 0.2, 0.25, 0.5, 0.75]), 2)
            return f"Convert {dec} to Fraction:", decimal_to_fraction(dec)
        else:
            # fraction to decimal
            frac = random.choice([Fraction(1,10), Fraction(1,4), Fraction(3,10), Fraction(1,2), Fraction(3,4)])
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
        decimals_list = [0.375, 0.625, 0.2, 0.4, 0.875]
        dec = random.choice(decimals_list)
        if random.choice([True, False]):
            return f"Convert {dec} to Fraction:", decimal_to_fraction(dec)
        else:
            frac = decimal_to_fraction(dec)
            return f"Convert {frac} to Decimal:", float(dec)

# ------------------------------
# Initialize State
# ------------------------------

if "score" not in st.session_state:
    st.session_state.score = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "question" not in st.session_state:
    st.session_state.question, st.session_state.answer = generate_question(1)

# ------------------------------
# UI Layout
# ------------------------------

st.title("🎮 Fraction ↔ Decimal Conversion Game")
st.subheader("👩‍🏫 Teacher: Answer the questions to go to the next level!")

st.write(f"### ⭐ Current Level: {st.session_state.level}")
st.write(f"### 🧮 Score: {st.session_state.score}")

st.markdown("---")

# Show the question
st.write(f"## **❓ {st.session_state.question}**")

# ------------------------------------------------
# User Answer Input
# ------------------------------------------------

user_answer = st.text_input("Your Answer:")

if st.button("Submit"):
    correct_answer = st.session_state.answer

    try:
        # Convert user input into comparable forms
        if isinstance(correct_answer, Fraction):  # expecting fraction
            user_fraction = Fraction(user_answer.replace(" ", ""))
            if user_fraction == correct_answer:
                st.success("🎉 Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct answer: {correct_answer}")

        else:  # expecting decimal
            if abs(float(user_answer) - float(correct_answer)) < 0.01:
                st.success("🎉 Correct!")
                st.session_state.score += 1
            else:
                st.error(f"❌ Wrong! Correct answer: {correct_answer}")

    except:
        st.error("⚠️ Invalid input! Try again.")

    # Level progression
    if st.session_state.score >= 5 and st.session_state.level == 1:
        st.session_state.level = 2
        st.success("🌟 Level Up! Welcome to Level 2")

    elif st.session_state.score >= 12 and st.session_state.level == 2:
        st.session_state.level = 3
        st.success("🔥 Level Up! Welcome to Level 3")

    # Generate new question
    st.session_state.question, st.session_state.answer = generate_question(st.session_state.level)

# Restart button
if st.button("🔄 Restart Game"):
    st.session_state.score = 0
    st.session_state.level = 1
    st.session_state.question, st.session_state.answer = generate_question(1)
    st.success("Game Restarted!")

