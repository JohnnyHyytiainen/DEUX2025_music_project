# Mediaformat (Skivor, LPs etc)
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st
from components.data_loader import fetch_data
from components.queries.queries_physical_media import get_media_sales_query

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
        # Gör om åren till heltal istället för t.ex 2,008
        chart_data.index = chart_data.index.astype(str)

        # ========================================
        # 4. KPI-KORT (Snabba insikter i toppen)
        # ========================================
        st.subheader("KPI-Insikter")

        # Skapa tre kolumner bredvid varandra
        col1, col2, col3 = st.columns(3)

        # Insikt 1: Total volym/värde under vald period
        total_sum = df["value"].sum()

        # Insikt 2: Vilket format sålde bäst totalt?
        # Gruppera på format, summera, och plocka ut det med högst värde
        top_format_series = df.groupby("format")["value"].sum()
        top_format = top_format_series.idxmax()

        # Insikt 3: Vilket enskilt år (och format) var det absoluta rekordet?
        # Hitta index för raden med absolut högst 'value'
        peak_row_index = df["value"].idxmax()
        peak_year = df.loc[peak_row_index, "year"]
        peak_value = df.loc[peak_row_index, "value"]

        # ========== DYNAMISKA LABLES(ETIKETTER) ==========
        # Skapa en nice text-str beroende på vad man väljer i menyn
        # =================================================
        if metric == "Units":
            display_text = "Sålda Enheter (Miljoner Units sålda)"
        else:
            display_text = "Intäkter sett i $USD (Miljoner dollar)"

        # Rita ut med den dynamiska texten ovan
        with col1:
            st.metric(label=f"Totalt {display_text}", value=f"{total_sum:,.1f}")
        with col2:
            st.metric(label="Dominant Media Format", value=top_format)
        with col3:
            st.metric(
                label=f"Rekordår {display_text} ({peak_year})",
                value=f"{peak_value:,.1f} ({df.loc[peak_row_index, 'format']})",
            )

        st.divider()  # En snygg linje som separerar våra KPIer från graferna

        # Visa grafen
        st.area_chart(chart_data)

        # Exempel på en 'knapp' vi kan använda (Checkbox för raw data)
        if st.checkbox("Visa raw data"):
            st.dataframe(df, use_container_width=True)

    else:
        st.info("Ingen data hittades för vala filter.")
else:
    st.warning("Välj minst ETT format i sidopanelen för att börja.")
