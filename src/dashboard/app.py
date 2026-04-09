# Kommentarer: Svenska
# Kod: Engelska
# Streamlit script
import streamlit as st
import duckdb
import pandas as pd
from pathlib import Path

# Hitta exakt var app.py ligger på din dator (src/dashboard/)
CURRENT_DIR = Path(__file__).parent

# Navigera bakåt till rooten och in i vår data folder
# .parent går upp ett steg. Två parents tar oss från dashboard -> src -> root
DB_PATH = CURRENT_DIR.parent.parent / "data" / "music_warehouse.duckdb"

# ==========
# 0) SIDINSTÄLLNINGAR
# ==========
st.set_page_config(page_title="Spotify Data Explorer", page_icon="🎵", layout="wide")

st.title("🎵 Spotify Global Data Explorer")
st.markdown(
    "Välkommen till DEUX plattformen. Denna dashboard är direktkopplad mot vår lokala **DuckDB Data Warehouse**."
)


# Cache'ar datan i 1 timme så appen är snabb
@st.cache_data(ttl=3600)
def load_data(query):
    """Connects to DuckDB, runs a SQL query and returns a DataFrame"""
    # read_only=True är viktigt i streamlit vi kan läsa data och ej modifiera den
    try:
        con = duckdb.connect(DB_PATH, read_only=True)
        df = con.execute(query).df()
        con.close()
        return df
    except Exception as e:
        st.error(f"Could not connect to DB. Reason: {e}")
        return pd.DataFrame()


# ==========
# 2) Bygga upp gränssnittet
# ==========
tab1, tab2 = st.tabs(["Historiska topp-låtar ", "Kulturella skillnader"])

# --- Tab 1, "Maria Carey joinen" ---
with tab1:
    st.subheader("Världens mest spelade låtar (Peak Streams)")
    st.markdown(
        "Här kombinerar vi historiska streams (2017+) med moderna audio features."
    )

    query_1 = """
    SELECT 
        h.name as Låt,
        h.artists as Artist,
        MAX(h.streams) as Max_Streams,
        AVG(d.valence) * 100 as Glädje
    FROM silver_historical_charts h
    JOIN silver_spotify_daily d 
      ON h.name = d.name AND h.artists = d.artists
    WHERE h.streams IS NOT NULL
    GROUP BY h.name, h.artists
    ORDER BY Max_Streams DESC
    LIMIT 10;
    """
    df_tab1 = load_data(query_1)

    if not df_tab1.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_tab1, use_container_width=True, hide_index=True)
        with col2:
            st.bar_chart(df_tab1.set_index("Låt")["Max_Streams"], color="#1DB954")

    # --- tab 2: EXPLICIT MUSIK ---
with tab2:
    st.subheader("Länder med mest 'explicit' musiksmak")
    st.markdown("Vilka länder lyssnar på högst andel Explicit/Barnförbjuden musik?")

    query_explicit = """
    SELECT 
        country,
        AVG(CAST(is_explicit AS INT)) * 100 as Explicit_Procent
    FROM silver_spotify_daily
    WHERE country != 'Global'
    GROUP BY country
    HAVING COUNT(*) > 100
    ORDER BY Explicit_Procent DESC
    LIMIT 15;
    """

    df_explicit = load_data(query_explicit)

    if not df_explicit.empty:
        # Fin barchart i streamlit
        st.bar_chart(
            df_explicit.set_index("country")["Explicit_Procent"], color="#FF5722"
        )
