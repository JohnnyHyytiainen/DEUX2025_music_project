import streamlit as st

def read_textfile(path):
    with open(path) as file:
        return file.read()

def read_css(path):
    css = read_textfile(path)
    st.write(
        f"<style>{css}</style>", unsafe_allow_html=True
    )