# Historiska EDA trender
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st
import plotly.express as px

from components.data_loader import fetch_data
from components.queries.queries_historical import (
    get_available_years_query,
    get_top_artists_by_year_query,
)

# Sätt titlar, ikon och vilken typ av layout.
st.set_page_config(page_title="Historical Trends", page_icon="📈", layout="wide")
st.title("📈 Årets Dominanter på Topplistorna")
st.markdown("Upptäck vilka artister som presterat bäst under specifika år.")

# ==============================
# 1) HÄMTAR  DYNAMISKA FILTERVÄRDEN
# ==============================
# Hämta åren via vår nya query-funktion
df_years = fetch_data(get_available_years_query())

if not df_years.empty:
    # Gör om dataframe kolumnen till en vanlig Python list
    available_years = df_years["year"].tolist()

    # ==============================
    # 2) UI + FILTERS (Sidebar)
    # ==============================
    st.sidebar.header("Filtrera Trender")

    selected_year = st.sidebar.selectbox(
        "Välj År att analysera:", options=available_years
    )

    top_n = st.sidebar.slider(
        "Hur många artister vill du se?", min_value=5, max_value=20, value=10
    )

    # ==============================
    # 3) KÖR VÅR QUERY (via Component)
    # ==============================
    sql = get_top_artists_by_year_query(selected_year, top_n)
    df_trends = fetch_data(sql)

    # ==============================
    # --- KPI KORT FÖR EXTRA INSIGHT ---
    # ==============================
    winner = df_trends.iloc[0]["artist"]
    appearances = df_trends.iloc[0]["total_chart_appearances"]
    st.success(
        f"**Insikt:** Den absoluta vinnaren år {selected_year} var **{winner}** med totalt {appearances} placeringar!"
    )

    # ==============================
    # 4. VISUALISERING (Plotly)
    # ==============================
    st.subheader(f"👑 Topp {top_n} Artister år {selected_year}")

    if not df_trends.empty:
        # Skapa Plotly-grafen
        fig = px.bar(
            df_trends,
            x="total_chart_appearances",
            y="artist",
            orientation="h",
            title=f"Mest frekventa artisterna på topplistan ({selected_year})",
            labels={
                "total_chart_appearances": "Antal listplaceringar",
                "artist": "Artist",
            },
            color="total_chart_appearances",
            color_continuous_scale="blues",
        )

        # Vänd på Y AXIS så 1an (den med mest) hamnar högst upp
        fig.update_layout(yaxis={"categoryorder": "total ascending"})

        # Skicka in grafen i Streamlit
        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Ingen data hittades för detta år.")
else:
    st.error("Kunde inte ladda tillgängliga år. Kolla databasanslutningen.")
