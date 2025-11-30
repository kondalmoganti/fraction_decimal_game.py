import streamlit as st
from streamlit_lottie import st_lottie
import json

def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

st.title("Lottie Test")

animation = load_lottie_file("teacher_writing.json")
if animation:
    st_lottie(animation, height=300)
else:
    st.error("Could not load teacher_writing.json")
