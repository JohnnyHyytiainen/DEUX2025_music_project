# 01_🌍_Global_Trends.py
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st

# Så här löser vi våra imports
from components.data_loader import fetch_data
from components.queries_global import (
    get_top_explicit_query,
    get_continent_list_query,
    get_mood_and_tempo_query,
    get_continent_bpm_stats_query,
)
from components.charts_global import (
    create_explicit_bar_chart,
    create_mood_bar_chart,
    create_tempo_line_chart,
    create_continent_bpm_chart,
)

st.set_page_config(page_title="Globala Musiktrender", page_icon="🌍", layout="wide")

st.title("🌍 Kulturella Skillnader i Musik")
st.markdown("Utforska hur olika regioner konsumerar musik baserat på Spotify-data.")

# === En DYNAMISK sidomeny ===
df_continents = fetch_data(get_continent_list_query())
continent_list = (
    ["Alla"] + df_continents["continent"].tolist()
    if not df_continents.empty
    else ["Alla"]
)

selected_region = st.sidebar.selectbox(
    "Välj region att analysera:", options=continent_list
)

# === Hämtar vår data ===
df_explicit = fetch_data(get_top_explicit_query(selected_region))
df_mood = fetch_data(get_mood_and_tempo_query())
df_bpm_stats = fetch_data(get_continent_bpm_stats_query())

# ==================
# 1) EXPLICIT MUSIK
# ==================
if not df_explicit.empty:
    st.subheader("Nyckeltal (Övergripande insikter)")
    col1, col2, col3 = st.columns(3)
    col1.metric("Mest Explicit Land", df_explicit.iloc[0]["country"], "Top #1")
    col2.metric("Snitt BPM", f"{df_explicit['Avg_BPM'].mean():.1f} BPM")
    col3.metric("Analyserade länder", str(len(df_explicit)))

    st.divider()
    st.subheader("Andel Explicit Musik per Land")

    # Kallar på komponenten och ritar ut
    fig_explicit = create_explicit_bar_chart(df_explicit)
    st.plotly_chart(fig_explicit, use_container_width=True)

# =========================
# 2) MOOD & TEMPO i musiken
# =========================
st.divider()
st.title("🌍 Kulturella Skillnader: Glädje & Tempo")

if not df_mood.empty:
    tab_happy, tab_tempo = st.tabs(["😊 Glädje (Valence)", "⚡ Tempo (BPM)"])

    with tab_happy:
        col1, col2 = st.columns(2)
        top_happy = df_mood.sort_values(by="happiness_score", ascending=False).head(10)
        top_sad = df_mood.sort_values(by="happiness_score", ascending=True).head(10)

        with col1:
            st.subheader("Topp 10: Gladaste Nationerna")
            st.plotly_chart(
                create_mood_bar_chart(top_happy, is_happy=True),
                use_container_width=True,
            )

        with col2:
            st.subheader("Topp 10: Melankoliska Nationerna")
            st.plotly_chart(
                create_mood_bar_chart(top_sad, is_happy=False), use_container_width=True
            )

    with tab_tempo:
        st.subheader("Länder som lyssnar på musik med SNABBAST Tempo (Högst snitt-BPM)")
        top_fast = df_mood.sort_values(by="avg_bpm", ascending=False).head(15)
        st.dataframe(
            top_fast[["country", "avg_bpm", "unique_songs_played"]],
            use_container_width=True,
            hide_index=True,
        )

        st.plotly_chart(create_tempo_line_chart(top_fast), use_container_width=True)

# ===================================
# 3) Vilka länder har högst BPM/Tempo
# ====================================
st.divider()
if not df_bpm_stats.empty:
    st.info(
        f"**Analys:** Musiken i **{df_bpm_stats.iloc[0]['continent']}** tenderar att ha högst tempo, medan **{df_bpm_stats.iloc[-1]['continent']}** har en mer tillbakalutad takt."
    )
    st.header("🥁 Regional Pulse: BPM per Kontinent")

    st.plotly_chart(create_continent_bpm_chart(df_bpm_stats), use_container_width=True)
