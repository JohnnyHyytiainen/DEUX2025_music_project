import duckdb
from pathlib import Path
# Exporterar alla våra tables i music_warehouse.duckdb databasen till
# .parquet filer för att underlätta deployment av streamlit dashboarden
# nuvarande db fil är FÖR stor för att kunna deploya utan huvudvärk.

# ==========================
# KÖR SCRIPTET EN GÅNG BARA!
# ==========================

# Peka på och connecta till vår lokala DB
con = duckdb.connect("data/music_warehouse.duckdb", read_only=True)
# output directory för våra .parquet filer
output_dir = Path("data/parquet")
output_dir.mkdir(parents=True, exist_ok=True)

# Hämtar ALLA tables och view table
objects = con.execute("SHOW TABLES").fetchall()

for obj in objects:
    name = obj[0]
    out_path = output_dir / f"{name}.parquet"
    print(f"Exporting: {name} --> {out_path}")
    con.execute(
        f"COPY (SELECT * FROM {name}) TO '{out_path}' (FORMAT PARQUET, COMPRESSION ZSTD)"
    )

con.close()
print("Done!")
