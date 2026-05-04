# 01_🌍_Global_Trends.py
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st
from components.data_loader import fetch_data
from components.queries.queries_global import (
    get_top_explicit_query,
    get_continent_list_query,
    get_mood_and_tempo_query,
    get_dj_crate_query,
    get_dancefloor_songs_query,
    get_acoustic_loudness_query,
)
from components.charts.charts_global import (
    create_explicit_bar_chart,
    create_mood_bar_chart,
    create_tempo_bar_chart,
    create_dancefloor_scatter,
    create_acoustic_bar_chart,
)

st.set_page_config(page_title="Global Music Trends", page_icon="🌍", layout="wide")

# ==========================================
# Variabler
# ==========================================
# Initiera state variabler för varje separat graf
if "explicit_continent" not in st.session_state:
    st.session_state.explicit_continent = "Global"

if "mood_continent" not in st.session_state:
    st.session_state.mood_continent = "Global"

if "anatomy_continent" not in st.session_state:
    st.session_state.anatomy_continent = "Global"


# Callback-funktion för reset knapp högst upp
def reset_all_filters():
    st.session_state.explicit_continent = "Global"
    st.session_state.mood_continent = "Global"
    st.session_state.anatomy_continent = "Global"


# ==========================================
# HEADER & GLOBAL CONTROLS
# ==========================================
st.title("Cultural Differences in Music")
st.markdown("Explore how different regions consume music based on Spotify's data.")

# Hämta kontinentlistan en gång (används av alla selectboxes)
df_continents = fetch_data(get_continent_list_query())
continent_list = (
    ["Global"] + df_continents["continent"].tolist()
    if not df_continents.empty
    else ["Global"]
)

# Reset knapp i toppen
st.button("Reset ALL Region Filters", on_click=reset_all_filters, type="primary")
st.divider()

# ==========================================
# EXPLICIT MUSIK (Eget filter)
# ==========================================
st.subheader("Explicit Music")

# selectbox är en kopplad key direkt till session_state
selected_explicit = st.selectbox(
    "Select region for Explicit Music:",
    options=continent_list,
    key="explicit_continent",
)

df_explicit = fetch_data(get_top_explicit_query(selected_explicit))

if not df_explicit.empty:
    fig_explicit = create_explicit_bar_chart(df_explicit)
    st.plotly_chart(fig_explicit, use_container_width=True)

st.divider()

# ==========================================
# MOOD & TEMPO (Eget filter)
# ==========================================
st.subheader("Cultural Differences: Happiness & Tempo")

# Den här selectboxen är kopplad till sin egen session_state
selected_mood = st.selectbox(
    "Select region for Mood & Tempo:", options=continent_list, key="mood_continent"
)

df_mood = fetch_data(get_mood_and_tempo_query(selected_mood))

if not df_mood.empty:
    tab_happy, tab_tempo = st.tabs(["Happiness (Valence)", "Tempo (BPM)"])

    # === FLIK: GLÄDJE ===
    with tab_happy:
        col1, col2 = st.columns(2)
        top_happy = df_mood.sort_values(by="happiness_score", ascending=False).head(10)
        top_sad = df_mood.sort_values(by="happiness_score", ascending=True).head(10)

        with col1:
            st.markdown(f"**The Happiest Nations ({selected_mood})**")
            st.plotly_chart(
                create_mood_bar_chart(top_happy, is_happy=True),
                use_container_width=True,
            )

        with col2:
            st.markdown(f"**The Most Melancholic Nations ({selected_mood})**")
            st.plotly_chart(
                create_mood_bar_chart(top_sad, is_happy=False), use_container_width=True
            )

    # === FLIK: TEMPO ===
    with tab_tempo:
        col3, col4 = st.columns(2)
        top_fast = df_mood.sort_values(by="avg_bpm", ascending=False).head(10)
        top_slow = df_mood.sort_values(by="avg_bpm", ascending=True).head(10)

        with col3:
            st.markdown(f"**Fastest Tempo ({selected_mood})**")
            st.plotly_chart(
                create_tempo_bar_chart(top_fast, is_fast=True), use_container_width=True
            )

        with col4:
            st.markdown(f"**Slowest Tempo ({selected_mood})**")
            st.plotly_chart(
                create_tempo_bar_chart(top_slow, is_fast=False),
                use_container_width=True,
            )

# ==========================================
# Dancefloor, loudness queries + dess charts
# ==========================================
st.divider()
st.subheader("Deep Dive into Musical Anatomy")

selected_anatomy = st.selectbox(
    "Select region for Musical Anatomy", options=continent_list, key="anatomy_continent"
)

df_dance = fetch_data(get_dancefloor_songs_query(selected_anatomy))
df_acoustic = fetch_data(get_acoustic_loudness_query(selected_anatomy))

if not df_dance.empty and not df_acoustic.empty:
    tab_dance, tab_acoustic = st.tabs(["The Global Dancefloor", "Acoustic Vs Produced"])

    with tab_dance:
        st.markdown("**Does High energy equal danceable music?**")
        st.write(
            "The dots show the average per Country. The lines are the Global average."
        )
        st.plotly_chart(create_dancefloor_scatter(df_dance), use_container_width=True)

    with tab_acoustic:
        st.markdown("**The Aucustic sound VS The Electronic sound**")
        st.write(
            "Compare the nations that love stripped-down instruments with those that prefer heavily produced electronic beats."
        )
        col_ac1, col_ac2 = st.columns(2)

        # Sortera ut extremerna i båda columns
        top_acoustic = df_acoustic.sort_values(
            by="avg_acousticness", ascending=False
        ).head(10)
        top_produced = df_acoustic.sort_values(
            by="avg_acousticness", ascending=True
        ).head(10)

        with col_ac1:
            st.subheader("The Acoustic Lounge")
            st.plotly_chart(
                create_acoustic_bar_chart(top_acoustic, is_acoustic=True),
                use_container_width=True,
            )

        with col_ac2:
            st.subheader("The Electronic Club")
            st.plotly_chart(
                create_acoustic_bar_chart(top_produced, is_acoustic=False),
                use_container_width=True,
            )


# =============
# MUSIC MATCHER
# =============
st.divider()
st.header("DJ Music Matcher")
st.markdown("Find the perfect songs for your playlist based on technical parameters.")

# Kontrollpanel i kolumner
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)

with ctrl_col1:
    bpm_range = st.slider("Select BPM range:", 60, 200, (60, 200))
    is_explicit = st.checkbox("Show only Explicit songs", value=False)

with ctrl_col2:
    valence_range = st.slider("Happiness (Valence %):", 0, 100, (0, 100))
    limit_top = st.checkbox("Show only Top 20", value=True)


with ctrl_col3:
    energy_range = st.slider("Energy level (Energy %):", 0, 100, (0, 100))

# Hämta matchningar
query_dj = get_dj_crate_query(
    bpm_range,
    valence_range,
    energy_range,
    is_explicit,
    limit_top,
)
df_dj = fetch_data(query_dj)

if not df_dj.empty:
    st.success(f"Found {len(df_dj)} songs that match your criteria!")
    st.dataframe(df_dj, use_container_width=True, hide_index=True)
else:
    st.warning("No songs matched that combination. Try expanding your search!")
