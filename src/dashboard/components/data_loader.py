# Vår engine för att hålla oss till DRY principen.
# Kommentarer: Svenska
# Kod: Engelska
import duckdb
import pandas as pd
import streamlit as st
from pathlib import Path


# Det här scriptet gör EN grej. Pratar med databasen, cache'ar resultatet och skickar tillbaka en Pandas dataframe.
# Streamlit-caching gör appen snabb och sparar på vår databas.
@st.cache_data(ttl=3600)
def fetch_data(query: str) -> pd.DataFrame:
    """
    A DRY function to get data from DuckDB.
    Used by all pages in Dashboard.
    """
    # Hittar databasen dynamiskt(dynamisk sökväg)
    current_dir = Path(__file__).parent
    db_path = current_dir.parent.parent.parent / "data" / "music_warehouse.duckdb"

    try:
        con = duckdb.connect(str(db_path), read_only=True)
        df = con.execute(query).df()
        con.close()
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()  # Returnerar en TOM df så att appen inte kraschar totalt.
