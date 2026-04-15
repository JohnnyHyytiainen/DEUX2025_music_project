# Mediaformat (Skivor, LPs etc)
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st
from components.data_loader import fetch_data
from components.queries_physical_media import get_media_sales_query

# Sätter sidans titel, ikon och vilken typ av layout vi vill använda.
st.set_page_config(page_title="Physical Media", page_icon="💿", layout="wide")
# Sätter titel PÅ sidan.
st.title("💿 Music consumption: From Vinyl to Streaming")

# === SIDEBAR / FILTERS ===
st.sidebar.header("Konfigurera Vy")

# 1) Slider för ÅR (Den returnerar en tuple (start, stop))
year_range = st.sidebar.slider(
    "Välj tidsperiod", min_value=1973, max_value=2019, value=(1980, 2010)
)

# 2) Radio för mätvärden
metric = st.sidebar.radio(
    "Välj mätvärde",
    options=["Units", "Value (Adjusted)"],
    format_func=lambda x: (
        "Antal Sålda Enheter(Miljoner)" if x == "Units" else "Värde(Miljoner dollar)"
    ),
)

# 3) Multiselect(Flera val) för format
all_formats = ["CD", "LP/EP", "Cassette", "Paid Subscription", "8 - Track"]
selected_formats = st.sidebar.multiselect(
    "Välj format att jämföra",
    options=all_formats,
    default=["CD", "LP/EP", "Paid Subscription"],
)

# === DATA EXEKVERINGEN ===
if selected_formats:
    # Hämta SQL strängen ifrån vår komponent(queryn)
    sql = get_media_sales_query(metric, year_range, selected_formats)

    # Kör queryn via data_loader scriptet(kontakten till vår db)
    df = fetch_data(sql)

    if not df.empty:
        # pivot datan för en finare graf
        chart_data = df.pivot(index="year", columns="format", values="value")

        # Visa grafen
        st.area_chart(chart_data)

        # Exempel på en 'knapp' vi kan använda (Checkbox för raw data)
        if st.checkbox("Visa raw data"):
            st.dataframe(df, use_container_width=True)

    else:
        st.info("Ingen data hittades för vala filter.")
else:
    st.warning("Välj minst ETT format i sidopanelen för att börja.")
