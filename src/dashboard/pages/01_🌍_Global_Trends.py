# Globala EDA trender
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st
import plotly.express as px

# Så här sköter vi importen av vår databas motor OCH våra queries mot databasen. EXTREMT CLEANT.
from components.data_loader import fetch_data
from components.queries_global import (
    get_top_explicit_query,
    get_continent_list_query,
    get_mood_and_tempo_query,
    get_continent_bpm_stats_query,
)

st.set_page_config(page_title="Global EDA", page_icon="🌍", layout="wide")

st.title("🌍 Kulturella Skillnader i Musik")
st.markdown("Utforska hur olika regioner konsumerar musik baserat på Spotify-data.")

st.sidebar.header("Filtrera Data")

# ==========================================
# 1) DYNAMISK SIDOMENY
# ==========================================
# Hämta unika kontinenter från databasen istället för att hårdkoda!
df_continents = fetch_data(get_continent_list_query())

if not df_continents.empty:
    # Skapa en lista och lägg till "Alla" högst upp
    continent_list = ["Alla"] + df_continents["continent"].tolist()
else:
    # Fallback om db krånglar
    continent_list = ["Alla"]

selected_region = st.sidebar.selectbox(
    "Välj region att analysera:",
    options=continent_list,
)

# ==========
# HÄMTA DATA (DRY och modulärt!)
# Skicka in vald region till queryn
# ==========
# 1) Hämta listan för dropdown (denna behöver inte köras två gånger)
df_continents = fetch_data(get_continent_list_query())

# 2) Skapa SQL string
query_explicit = get_top_explicit_query(selected_region)
query_mood = get_mood_and_tempo_query()

# För kontinent jämförelsen vill jag se ALLA kontinenter för att kunna jämföra,
# så jag skickar inte med selected_region här.
query_bpm_continent = get_continent_bpm_stats_query()

# 3) Hämta faktiska DataFrames
df = fetch_data(query_explicit)
df_mood = fetch_data(query_mood)
df_bpm_stats = fetch_data(query_bpm_continent)  # <--- Ändrat namn för att undvika krock

# ====================
# Första queryn. EXPLICIT
# ====================
if not df.empty:
    st.subheader(f"Nyckeltal (Övergripande insikter)")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Mest Explicit Land", value=df.iloc[0]["country"], delta="Top #1"
        )
    with col2:
        st.metric(label="Snitt BPM (Top 10)", value=f"{df['Avg_BPM'].mean():.1f} BPM")
    with col3:
        st.metric(label="Totalt Analyserade länder", value=str(len(df)))

    st.divider()

    st.subheader("Andel Explicit Musik per Land")

    # --- PLOTLY UPGRADE: Explicit Musik ---
    # Skapar ett interaktivt stapeldiagram där färgen ändras baserat på procenten
    fig_explicit = px.bar(
        df,
        x="country",
        y="Explicit_Procent",
        color="Explicit_Procent",
        color_continuous_scale="Purples",  # Passar lila färgtema (bara ändra om lust finns)
        labels={"country": "Land", "Explicit_Procent": "Explicit Musik (%)"},
        title="Explicit Musik (%)",
    )
    # Göm legend för renare UI
    fig_explicit.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_explicit, use_container_width=True)

else:
    st.warning("Ingen data hittades eller databasen kunde inte nås..")

# ====================
# Andra queryn, MOOD
# ====================
st.divider()
st.title("🌍 Kulturella Skillnader: Glädje & Tempo")
st.markdown("Hur skiljer sig musiken åt mellan världens nationer?")

if not df_mood.empty:
    # Skapa flikar för olika perspektiv
    tab_happy, tab_tempo = st.tabs(["😊 Glädje (Valence)", "⚡ Tempo (BPM)"])

    # === FLIK: GLÄDJE ===
    with tab_happy:
        col1, col2 = st.columns(2)

        # Sortera fram extremerna
        top_happy = df_mood.sort_values(by="happiness_score", ascending=False).head(10)
        top_sad = df_mood.sort_values(by="happiness_score", ascending=True).head(10)

        with col1:
            st.subheader("Topp 10: Gladaste Nationerna")
            # --- PLOTLY UPGRADE: Horisontellt diagram för läsbarhet ---
            fig_happy = px.bar(
                top_happy,
                x="happiness_score",
                y="country",
                orientation="h",
                color_discrete_sequence=["#059AA8"],
                labels={"country": "", "happiness_score": "Glädje Index (0-100)"},
            )
            fig_happy.update_layout(
                yaxis={"categoryorder": "total ascending"}
            )  # 1 är i toppen
            st.plotly_chart(fig_happy, use_container_width=True)

        with col2:
            st.subheader("Topp 10: Melankoliska Nationerna")
            fig_sad = px.bar(
                top_sad,
                x="happiness_score",
                y="country",
                orientation="h",
                color_discrete_sequence=["#00004B"],
                labels={"country": "", "happiness_score": "Glädje Index (0-100)"},
            )
            fig_sad.update_layout(
                yaxis={"categoryorder": "total descending"}
            )  # Lägst värde i toppen
            st.plotly_chart(fig_sad, use_container_width=True)

    # === FLIK: TEMPO ===
    with tab_tempo:
        st.subheader("Världens Tempo-kungar (Högst snitt-BPM)")
        top_fast = df_mood.sort_values(by="avg_bpm", ascending=False).head(15)

        # Datatabell
        st.dataframe(
            top_fast[["country", "avg_bpm", "unique_songs_played"]],
            use_container_width=True,
            hide_index=True,
        )

        # --- PLOTLY UPGRADE: Linjediagram med markörer ---
        fig_tempo = px.line(
            top_fast,
            x="country",
            y="avg_bpm",
            markers=True,  # Lägger till små punkter på linjen
            color_discrete_sequence=["#FF4B4B"],
            labels={"country": "Land", "avg_bpm": "Snitt Tempo (BPM)"},
        )
        # Sätt en rimlig Y-axel så linjen inte ser platt ut
        fig_tempo.update_yaxes(
            range=[top_fast["avg_bpm"].min() - 2, top_fast["avg_bpm"].max() + 2]
        )
        st.plotly_chart(fig_tempo, use_container_width=True)

else:
    st.warning("Kunde inte hämta data för humör och tempo.")

    # ====================
    # Tredje sektionen: REGIONAL PULSE
    # ====================
st.divider()
# En liten förklarande text
slowest_continent = df_bpm_stats.iloc[-1]["continent"]
fastest_continent = df_bpm_stats.iloc[0]["continent"]
st.info(
    f"**Analys:** Vi kan se att musiken i **{fastest_continent}** tenderar att ha högst tempo, medan **{slowest_continent}** har en mer tillbakalutad takt."
)
st.header("🥁 Regional Pulse: BPM per Kontinent")
st.markdown("Hur snabbt slår musikhjärtat i olika delar av världen?")


if not df_bpm_stats.empty:
    # Skapa en snygg bar chart med Plotly
    fig_bpm = px.bar(
        df_bpm_stats,
        x="continent",
        y="Avg_BPM",
        range_y=[100, 140],  # Fokusera på det intressanta intervallet
        color="Avg_BPM",
        color_continuous_scale="Reds",
        # Här lägger vi till "felmarginaler" för att visa spridningen (Min/Max BPM)
        error_y=df_bpm_stats["Max_BPM"] - df_bpm_stats["Avg_BPM"],
        error_y_minus=df_bpm_stats["Avg_BPM"] - df_bpm_stats["Min_BPM"],
        labels={"continent": "Kontinent", "Avg_BPM": "Genomsnittligt BPM"},
        title="Genomsnittligt Tempo med Spridning (Min/Max)",
    )

    # Gör grafen lite snyggare
    fig_bpm.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_bpm, use_container_width=True)

else:
    st.warning("Kunde inte hämta BPM-statistik för kontinenter.")
