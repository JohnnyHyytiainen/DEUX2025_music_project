# Streamlits appens framsida
# Kommentarer: Svenska
# Kod: Engelska
import streamlit as st

# MÅSTE vara det första streamlit command på sidan om jag förstått rätt.
st.set_page_config(
    page_title="Global Music Trends",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("🎵 Global Music Trends & Cultural Insights")
st.markdown("### Välkommen till DEUX25 Musik Dashboard!")

st.write("""
Denna dashboard är byggd ovanpå vår lokala **Data Lakehouse-arkitektur**. 
I menyn till vänster kan du navigera mellan olika analyser som DE teamet har tagit fram:

* 🌍 **Global Trends:** Kulturella skillnader, i musiken världen över.
* 📈 **Historical Trends:** Hur de mest virala låtarna presterat över tid.
* 💿 **Physical Media:** Format skiftet från Vinyl till Streaming.

**Instruktioner:**
Använd sidofältet (sidebar) på respektive sida för att filtrera datan. 
         Dashboarden är uppkopplad live mot vår analytiska databas (DuckDB) som innehåller närmare 30 miljoner rader data.
""")

st.info("<- Välj en analys i menyn till vänster för att börja utforska datan!")
