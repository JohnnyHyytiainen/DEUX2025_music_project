# 01_🌍_Global_Trends.py
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st

# Hur vi löser våra imports per Kokchuns specs.
from components.data_loader import fetch_data
from components.queries.queries_global import (
    get_top_explicit_query,
    get_continent_list_query,
    get_mood_and_tempo_query,
    get_continent_bpm_stats_query,
    get_dj_crate_query,
)
from components.charts.charts_global import (
    create_explicit_bar_chart,
    create_mood_bar_chart,
    create_tempo_bar_chart,
)

st.set_page_config(page_title="Global Music Trends", page_icon="🌍", layout="wide")

st.title("Cultural Differences in Music")
st.markdown("Explore how different regions consume music based on Spotify's data.")
st.divider()

# =========================
# 1) FILTER DIREKT PÅ SIDAN
# =========================
st.markdown("### Filter Insights")
st.write("Select a continent below to update all top lists on the page.")

df_continents = fetch_data(get_continent_list_query())
continent_list = (
    ["Global"] + df_continents["continent"].tolist()
    if not df_continents.empty
    else ["Global"]
)

# Skapar två kolumner för filter för att hålla det snyggt
filt_col1, filt_col2 = st.columns(2)
with filt_col1:
    selected_region = st.selectbox("Select continent:", options=continent_list)
with filt_col2:
    # Plats för framtida filter (t.ex. datum eller genre) om vi vill använda det!
    st.info("Tip: By filtering by continent you can compare countries locally.")

st.divider()

# ==========================================
# 2) HÄMTA DATA (Nu reagerar mood & tempo på filtret!)
# ==========================================
df_explicit = fetch_data(get_top_explicit_query(selected_region))
df_mood = fetch_data(get_mood_and_tempo_query(selected_region))
df_bpm_stats = fetch_data(get_continent_bpm_stats_query())

# ==============
# EXPLICIT MUSIK
# ===============
if not df_explicit.empty:
    st.subheader(f"Explicit Music ({selected_region})")

    # Kalla på komponenten
    fig_explicit = create_explicit_bar_chart(df_explicit)
    st.plotly_chart(fig_explicit, use_container_width=True)

# =============
# MOOD & TEMPO
# =============
st.divider()
st.title(f"🎭 Cultural Differences: Happiness & Tempo ({selected_region})")

if not df_mood.empty:
    tab_happy, tab_tempo = st.tabs(["😊 Happiness (Valence)", "⚡ Tempo (BPM)"])

    # === FLIK: GLÄDJE ===
    with tab_happy:
        col1, col2 = st.columns(2)
        top_happy = df_mood.sort_values(by="happiness_score", ascending=False).head(10)
        top_sad = df_mood.sort_values(by="happiness_score", ascending=True).head(10)

        with col1:
            st.subheader("The Happiest Nations in the Region")
            st.plotly_chart(
                create_mood_bar_chart(top_happy, is_happy=True),
                use_container_width=True,
            )

        with col2:
            st.subheader("The Most Melancholic Nations in the Region")
            st.plotly_chart(
                create_mood_bar_chart(top_sad, is_happy=False), use_container_width=True
            )

    # === TEMPO med barcharts ===
    with tab_tempo:
        col3, col4 = st.columns(2)
        top_fast = df_mood.sort_values(by="avg_bpm", ascending=False).head(10)
        top_slow = df_mood.sort_values(by="avg_bpm", ascending=True).head(10)

        with col3:
            st.subheader("Fastest Tempo in the region")
            st.plotly_chart(
                create_tempo_bar_chart(top_fast, is_fast=True), use_container_width=True
            )

        with col4:
            st.subheader("Slowest Tempo in the region")
            st.plotly_chart(
                create_tempo_bar_chart(top_slow, is_fast=False),
                use_container_width=True,
            )

# =============
# MUSIC MATCHER
# =============
st.divider()
st.header("🎧 DJ Music Matcher")
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
