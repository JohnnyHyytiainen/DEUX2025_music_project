# Vår engine för att hålla oss till DRY principen.
# Kommentarer: Svenska
# Kod: Engelska
import duckdb
import pandas as pd
import streamlit as st
from pathlib import Path


# Scriptet gör EN endaste sak. Läser våra .parquet filer och är kopplingen


# Funktion för att slippa behöva .parent X 4. Mer stabil funktion för att lösa pathing åt oss.
def _get_project_root() -> Path:
    """
    Climbs up in folder structure until pyproject.toml file is found.
    """
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "pyproject.toml").exists():
            return parent
    raise FileNotFoundError("Couldnt find project root.")


# PRIVAT FUNKTION DONT TOUCH FAAFO
def _get_parquet_dir() -> Path:
    """Finds our parquet folder regardless if running locally or on Streamlit Cloud"""
    return _get_project_root() / "data" / "parquet"


@st.cache_resource
def _get_connection():
    """
    Creates A in memory DuckDB connection and registers ALL parquet files
    as VIEWS with same name as our original tables. Only runs ONCE per session
    thanks to cache_resource
    """
    parquet_dir = _get_parquet_dir()
    con = duckdb.connect()  # <-- in memory, ingen .duckdb fil behövs längre

    # table som är uppdelade i vår chunk folder istället för enskilda filer
    CHUNKED_TABLES = {"silver_historical_charts"}

    # Registrera våra ensamma .parquet filer som VIEWS
    for parquet_file in parquet_dir.glob("*.parquet"):
        table_name = parquet_file.stem
        con.execute(
            f"""CREATE VIEW {table_name} AS SELECT * FROM read_parquet('{parquet_file.as_posix()}')"""
        )

    # Registrera chunked tables via glob, dvs DuckDB läser ALLA delar som en enda table
    for table_name in CHUNKED_TABLES:
        chunk_glob = (parquet_dir / table_name / "*.parquet").as_posix()
        con.execute(
            f""" CREATE VIEW {table_name} AS SELECT * FROM read_parquet('{chunk_glob}')"""
        )

    return con


@st.cache_data(ttl=3600)
def fetch_data(query: str) -> pd.DataFrame:
    """
    Identical as our original. All pages works without changes.
    """
    try:
        con = _get_connection()
        df = con.execute(query).df()
        return df
    except Exception as e:
        st.error(f"Database Error: {e}")
        return pd.DataFrame()
