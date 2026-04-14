# Kommentarer: Svenska
# Kod: Engelska
# Script för att initiera vår databas
import duckdb


# ==========================================
# KONSTANTER RÖR EJ
# ==========================================
DB_PATH = "../data/music_warehouse.duckdb"
PARQUET_PATH_DAILY = (
    "../data/processed/spotify_daily_top_songs_clean_version608.parquet"
)
PARQUET_PATH_CHARTS = "../data/processed/spotify_historical_charts.parquet"
PARQUET_PATH_TOP = "../data/processed/spotify_top_200_historical.parquet"
PARQUET_PATH_SALES = "../data/processed/historical_media_sales.parquet"
PARQUET_PATH_DIM_TABLE = "../data/processed/dim_geography.parquet"


def init_database():
    """Creating database and loading(ingesting) data from processed folder."""

    print(f"Initiating database: {DB_PATH}")

    # Om filen inte finns, skapar DuckDB den. Om den finns, ansluter vi till den.
    con = duckdb.connect(DB_PATH)

    # ==========
    # IDEMPOTENS: 'CREATE OR REPLACE TABLE' raderar den gamla tabellen om den finns
    # och bygger upp den på nytt med den senaste Parquet-datan.
    # ==========
    query_a = f"""
    CREATE OR REPLACE TABLE silver_spotify_daily AS 
    SELECT * FROM '{PARQUET_PATH_DAILY}';
    """

    query_b = f""" 
    CREATE OR REPLACE TABLE silver_historical_charts AS
    SELECT * FROM '{PARQUET_PATH_CHARTS}';
    """

    query_c = f"""
    CREATE OR REPLACE TABLE silver_top_200_historical AS
    SELECT * FROM '{PARQUET_PATH_TOP}'
    """

    query_d = f"""
    CREATE OR REPLACE TABLE silver_music_format_sales AS
    SELECT * FROM '{PARQUET_PATH_SALES}'
    """

    query_e = f"""
    CREATE OR REPLACE TABLE dim_geography AS
    SELECT * FROM '{PARQUET_PATH_DIM_TABLE}'
    """

    try:
        print("Reading in .Parquet file and building table. This will go QUICK..")
        con.execute(query_a)
        con.execute(query_b)
        con.execute(query_c)
        con.execute(query_d)
        con.execute(query_e)

        # Validering: Kolla hur många rader som faktiskt gick in
        count_a = con.execute("SELECT COUNT(*) FROM silver_spotify_daily").fetchone()[0]

        print("SUCCESS!")
        print(f"Table 'silver_spotify_daily' is created with: {count_a} rows.")

        # Validering: Kolla hur många rader som faktiskt gick in
        count_b = con.execute(
            "SELECT COUNT(*) FROM silver_historical_charts"
        ).fetchone()[0]

        print("SUCCESS!")
        print(f"Table 'silver_historical_charts' is created with: {count_b} rows.")

        # Validering: Kolla hur många rader som faktiskt gick in
        count_c = con.execute(
            "SELECT COUNT (*) FROM silver_top_200_historical"
        ).fetchone()[0]

        print("SUCCESS!")
        print(f"Table 'silver_top_200_historical' is created with: {count_c} rows.")

        # Validering: Kolla hur många rader som faktiskt gick in
        count_d = con.execute(
            "SELECT COUNT (*) FROM silver_music_format_sales"
        ).fetchone()[0]

        print("SUCCESS!")
        print(f"Table 'silver_music_format_sales' is created with: {count_d} rows.")

        # Validering: Kolla hur många rader som faktiskt gick in
        count_e = con.execute("SELECT COUNT (*) FROM dim_geography").fetchone()[0]

        print("SUCESS!")
        print(f"Table 'dim_geography' is created with: {count_e} rows.")

        # GOLD LAYER: Skapa VIEW FÖR ISO KODER.
        con.execute("""
        CREATE OR REPLACE VIEW gold_spotify_daily AS 
        SELECT 
            s.*, 
            g.country_name 
        FROM silver_spotify_daily s
        LEFT JOIN dim_geography g ON s.country = g.iso_code;
        """)
        print("Database view created: gold_spotify_daily")

    except Exception as e:
        print(f"Error occured while setting up database: {e}")

    finally:
        # VIKTIGT: Stäng alltid anslutningen, best practice. Lämna ingen dörr öppen.
        con.close()
        print("Database connection closed.")


if __name__ == "__main__":
    init_database()
