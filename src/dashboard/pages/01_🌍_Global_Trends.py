# 01_🌍_Global_Trends.py
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st

# Hur vi löser våra imports per Kokchuns specs.
from components.data_loader import fetch_data
from components.queries_global import (
    get_top_explicit_query,
    get_continent_list_query,
    get_mood_and_tempo_query,
    get_continent_bpm_stats_query,
    get_dj_crate_query,
)
from components.charts_global import (
    create_explicit_bar_chart,
    create_mood_bar_chart,
    create_tempo_bar_chart,
    create_continent_bpm_chart,
)

st.set_page_config(page_title="Globala Musiktrender", page_icon="🌍", layout="wide")

st.title("🌍 Kulturella Skillnader i Musik")
st.markdown("Utforska hur olika regioner konsumerar musik baserat på Spotify-data.")
st.divider()

# =========================
# 1) FILTER DIREKT PÅ SIDAN
# =========================
st.markdown("### Filtrera Insikter")
st.write("Välj en kontinent nedan för att uppdatera alla topplistor på sidan.")

df_continents = fetch_data(get_continent_list_query())
continent_list = (
    ["Alla"] + df_continents["continent"].tolist()
    if not df_continents.empty
    else ["Alla"]
)

# Skapar två kolumner för filter för att hålla det snyggt
filt_col1, filt_col2 = st.columns(2)
with filt_col1:
    selected_region = st.selectbox("Välj Kontinent:", options=continent_list)
with filt_col2:
    # Plats för framtida filter (t.ex. datum eller genre) om vi vill använda det!
    st.info("Tips: Genom att filtrera på kontinent kan du jämföra länder lokalt.")

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
    st.subheader(f"🗣️ Andel Explicit Musik ({selected_region})")

    # Kalla på komponenten
    fig_explicit = create_explicit_bar_chart(df_explicit)
    st.plotly_chart(fig_explicit, use_container_width=True)

# =============
# MOOD & TEMPO
# =============
st.divider()
st.title(f"🎭 Kulturella Skillnader: Glädje & Tempo ({selected_region})")

if not df_mood.empty:
    tab_happy, tab_tempo = st.tabs(["😊 Glädje (Valence)", "⚡ Tempo (BPM)"])

    # === FLIK: GLÄDJE ===
    with tab_happy:
        col1, col2 = st.columns(2)
        top_happy = df_mood.sort_values(by="happiness_score", ascending=False).head(10)
        top_sad = df_mood.sort_values(by="happiness_score", ascending=True).head(10)

        with col1:
            st.subheader("De Gladaste Nationerna i regionen")
            st.plotly_chart(
                create_mood_bar_chart(top_happy, is_happy=True),
                use_container_width=True,
            )

        with col2:
            st.subheader("De mest Melankoliska Nationerna i regionen")
            st.plotly_chart(
                create_mood_bar_chart(top_sad, is_happy=False), use_container_width=True
            )

    # === TEMPO med barcharts ===
    with tab_tempo:
        col3, col4 = st.columns(2)
        top_fast = df_mood.sort_values(by="avg_bpm", ascending=False).head(10)
        top_slow = df_mood.sort_values(by="avg_bpm", ascending=True).head(10)

        with col3:
            st.subheader("Snabbast Tempo i regionen")
            st.plotly_chart(
                create_tempo_bar_chart(top_fast, is_fast=True), use_container_width=True
            )

        with col4:
            st.subheader("Långsammast Tempo i regionen")
            st.plotly_chart(
                create_tempo_bar_chart(top_slow, is_fast=False),
                use_container_width=True,
            )

# =============
# MUSIC MATCHER
# =============
st.divider()
st.header("🎧 DJ Music Matcher")
st.markdown(
    "Hitta de perfekta låtarna för din playlist baserat på tekniska parametrar."
)

# Kontrollpanel i kolumner
ctrl_col1, ctrl_col2, ctrl_col3 = st.columns(3)

with ctrl_col1:
    bpm_range = st.slider("Välj BPM-spann:", 60, 200, (120, 130))
    is_explicit = st.checkbox("Visa endast Explicit innehåll", value=False)

with ctrl_col2:
    valence_range = st.slider("Glädje (Valence %):", 0, 100, (40, 60))
    limit_top = st.checkbox("Visa endast Top 20", value=False)


with ctrl_col3:
    energy_range = st.slider("Energinivå (Energy %):", 0, 100, (60, 90))

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
    st.success(f"Hittade {len(df_dj)} låtar som matchar dina kriterier!")
    st.dataframe(df_dj, use_container_width=True, hide_index=True)
else:
    st.warning("Inga låtar matchade den kombinationen. Prova att vidga dina filter!")
