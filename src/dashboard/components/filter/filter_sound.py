import streamlit as st

def bpm_slider():
    return st.slider("Choose BPM:", 60, 200, (60, 200))

def procent_slider(name:str):
    return st.slider(name, 0, 100, (0, 100))

def fifty_slider(name:str):
    return st.slider(name, 0, 1, (0, 100))