# Kommentarer: Svenska
# Kod: Engelska
# Script för att initiera vår databas
import duckdb
import os


# ==========================================
# KONSTANTER RÖR EJ
# ==========================================
DB_PATH = "../data/music_warehouse.duckdb"
PARQUET_PATH = "../data/processed/spotify_daily_top_songs_clean_version608.parquet"


def init_database():
    """Creating database and loading(ingesting) data from processed folder."""

    print(f"Initiating database: {DB_PATH}")

    # Om filen inte finns, skapar DuckDB den. Om den finns, ansluter vi till den.
    con = duckdb.connect(DB_PATH)

    # ==========
    # IDEMPOTENS: 'CREATE OR REPLACE TABLE' raderar den gamla tabellen om den finns
    # och bygger upp den på nytt med den senaste Parquet-datan.
    # ==========
    query = f"""
    CREATE OR REPLACE TABLE silver_spotify_daily AS 
    SELECT * FROM '{PARQUET_PATH}';
    """

    try:
        print("Reading in .Parquet file and building table. This will go QUICK..")
        con.execute(query)

        # Validering: Kolla hur många rader som faktiskt gick in
        count = con.execute("SELECT COUNT(*) FROM silver_spotify_daily").fetchone()[0]

        print("SUCCESS!")
        print(f"Table 'silver_spotify_daily' is created with: {count} rows.")

    except Exception as e:
        print(f"Error occured while setting up database: {e}")

    finally:
        # VIKTIGT: Stäng alltid anslutningen, best practice. Lämna ingen dörr öppen.
        con.close()
        print("Database connection closed.")


if __name__ == "__main__":
    init_database()
