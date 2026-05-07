# Streamlits appens framsida
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st
from utils.helpers import read_textfile, read_css
from utils.constants import MARKDOWN_PATH, STYLE_PATH

# MÅSTE vara det första streamlit command på sidan om jag förstått rätt.
st.set_page_config(
    page_title="Global Music Trends",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(read_textfile(MARKDOWN_PATH / "front_page.md"))

st.info("<- Choose a page in the side menu to start exploring!")
read_css(STYLE_PATH / "style.css")
