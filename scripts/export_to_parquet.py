import duckdb
from pathlib import Path
# Exporterar alla tables till .parquet för Streamlit Cloud deployment.
# silver_historical_charts chunkas separat pga storlek (>100MB).
# nuvarande db fil är FÖR stor för att kunna deploya utan huvudvärk.

# ==========================
# KÖR SCRIPTET EN GÅNG BARA!
# ==========================

con = duckdb.connect("data/music_warehouse.duckdb", read_only=True)
output_dir = Path("data/parquet")
output_dir.mkdir(parents=True, exist_ok=True)

# Tabeller som hanteras separat (för stora för en enskild fil)
CHUNKED_TABLES = {"silver_historical_charts"}

objects = con.execute("SHOW TABLES").fetchall()

for obj in objects:
    name = obj[0]

    # Skippa tabeller som chunkas separat nedan
    if name in CHUNKED_TABLES:
        print(f"Skipping (chunked separately): {name}")
        continue

    out_path = output_dir / f"{name}.parquet"
    print(f"Exporting: {name} --> {out_path}")
    con.execute(
        f"COPY (SELECT * FROM {name}) TO '{out_path}' (FORMAT PARQUET, COMPRESSION ZSTD)"
    )

# =====================================
# Chunkning av silver_historical_charts
# =====================================
chunk_size = 2_500_000
total_rows = con.execute("SELECT COUNT(*) FROM silver_historical_charts").fetchone()[0]
print(
    f"\nChunking silver_historical_charts ({total_rows:,} rows) into chunks of {chunk_size:,}"
)

chunk_dir = output_dir / "silver_historical_charts"
chunk_dir.mkdir(exist_ok=True)

for i, offset in enumerate(range(0, total_rows, chunk_size)):
    out_path = chunk_dir / f"part_{i:04d}.parquet"
    print(f"   CHUNK {i}: rows {offset:,} --> {offset + chunk_size:,}")
    con.execute(f"""
        COPY (
            SELECT * FROM silver_historical_charts
            LIMIT {chunk_size} OFFSET {offset}  
        ) TO '{out_path}' (FORMAT PARQUET, COMPRESSION ZSTD)
    """)
# OFFSET säkerställer unika rader per chunk
con.close()
print("\nDone!")
