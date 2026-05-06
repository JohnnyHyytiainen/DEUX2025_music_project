import streamlit as st


def read_textfile(path):
    with open(path) as file:
        return file.read()


def read_css(path):
    css = read_textfile(path)
    st.write(f"<style>{css}</style>", unsafe_allow_html=True)


# ===============================
# --- HELPERS GLOBAL SCRIPTS ---
def initialize_global_state():
    """initializes the overall state of the app."""
    if "global_continent" not in st.session_state:
        st.session_state.global_continent = "Global"
    if "global_explicit" not in st.session_state:
        st.session_state.global_explicit = True


def render_local_controls(section_id: str, continent_list: list):
    """
    Standardized control panel (Buttons + Explicit filter).
    Returns selected continent and explicit status.
    """
    col_filters, col_explicit = st.columns([3, 1])

    with col_filters:
        selected_cont = st.radio(
            "Select Region Focus:",
            options=continent_list,
            horizontal=True,
            key=f"radio_cont_{section_id}",
        )

    with col_explicit:
        is_explicit = st.checkbox(
            "Include Explicit Music",
            value=True,
            key=f"check_exp_{section_id}",
        )

    return selected_cont, is_explicit


# ===============================
