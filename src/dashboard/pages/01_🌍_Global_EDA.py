# Globala EDA trender
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st

# Så här sköter vi importen av vår databas motor OCH våra queries mot databasen. EXTREMT CLEANT.
from components.data_loader import fetch_data
from components.queries_global import get_top_explicit_query, get_mood_and_tempo_query

st.set_page_config(page_title="Global EDA", page_icon="🌍", layout="wide")

st.title("🌍 Kulturella Skillnader i Musik")
st.markdown("Utforska hur oliga regioner konsumerar musik baserat på Spotify-data.")

st.sidebar.header("Filtrera Data")
# === Lägg till "hela världen" som alternativ ===
selected_region = st.sidebar.selectbox(
    "Välj region att analysera:",
    ["Hela Världen", "Latinamerika", "Norden", "Nordamerika", "Asien"],
)

# ==========
# HÄMTA DATA (DRY och modulärt!)
# ==========
# 1) Hämta SQL str från query filen
query_explicit = get_top_explicit_query(selected_region)
query_mood = get_mood_and_tempo_query()

# 2) Skicka SQL str till vår databas engine
df = fetch_data(query_explicit)
df_mood = fetch_data(query_mood)

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
    st.bar_chart(df.set_index("country")["Explicit_Procent"], color="#AD0088")
else:
    st.warning("Ingen data hittades eller databasen kunde inte nås..")

# ====================
# Andra queryn, MOOD
# ====================
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
            st.bar_chart(
                top_happy.set_index("country")["happiness_score"], color="#3CFF00"
            )

        with col2:
            st.subheader("Topp 10: Melankoliska Nationerna")
            st.bar_chart(
                top_sad.set_index("country")["happiness_score"], color="#00294B"
            )

    # === FLIK: TEMPO ===
    with tab_tempo:
        st.subheader("Världens Tempo-kungar (Högst snitt-BPM)")
        top_fast = df_mood.sort_values(by="avg_bpm", ascending=False).head(15)

        # Här går det att använda sig av st.dataframe för en mer detaljerad view
        st.dataframe(
            top_fast[["country", "avg_bpm", "unique_songs_played"]],
            use_container_width=True,
            hide_index=True,
        )
        st.line_chart(top_fast.set_index("country")["avg_bpm"], color="#FF4B4B")

else:
    st.warning("Kunde inte hämta data för humör och tempo.")
