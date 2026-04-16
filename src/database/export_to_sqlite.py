# Script för att migrera .duckdb(OLAP) till en SQLite .db(OLTP) fil
# Kommentarer: Svenska
# Kod: Engelska
import duckdb


def export_duckdb_to_sqlite():
    print("Startar migrering från DuckDB till SQLite för PowerBI...")

    # 1. Ansluter till vår befintliga DuckDB fil
    con = duckdb.connect("./data/music_warehouse.duckdb")

    # 2. Installera och ladda SQLite tillägget, bör skötas automatiskt i bakgrunden
    con.execute("INSTALL sqlite;")
    con.execute("LOAD sqlite;")

    # 3. Skapa och anslut till en NY SQLite-fil
    sqlite_path = "./data/powerbi_warehouse_cleaned.db"
    con.execute(f"ATTACH '{sqlite_path}' AS sqlite_db (TYPE SQLITE);")

    print(f"Databas skapad: {sqlite_path}")
    print(
        "Kopierar tabeller (Detta kan ta lite tid för 30 miljoner rader, ha tålamod!)"
    )

    # 4. Kopiera in alla Silver tables och dimensioner in i SQLite-filen
    try:
        print(" -> Exporterar silver_spotify_daily...")
        con.execute(
            "CREATE TABLE sqlite_db.spotify_daily AS SELECT * FROM silver_spotify_daily;"
        )

        print(" -> Exporterar silver_historical_charts...")
        con.execute(
            "CREATE TABLE sqlite_db.historical_charts AS SELECT * FROM silver_historical_charts;"
        )

        print(" -> Exporterar silver_top_200_historical...")
        con.execute(
            "CREATE TABLE sqlite_db.top_200 AS SELECT * FROM silver_top_200_historical;"
        )

        print(" -> Exporterar dim_geography...")
        con.execute(
            "CREATE TABLE sqlite_db.dim_geography AS SELECT * FROM dim_geography;"
        )

        print("\nEXPORT KLAR! Ge filen 'powerbi_warehouse.db' till PowerBI.")

    except Exception as e:
        print(f"\nEtt fel uppstod vid kopieringen: {e}")
    finally:
        # Stäng anslutningen snyggt
        con.close()


if __name__ == "__main__":
    export_duckdb_to_sqlite()
