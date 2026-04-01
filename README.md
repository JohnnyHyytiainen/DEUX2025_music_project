# DEUX2025_music_project
Data Engineering and UX Class of 2025 at STI - Group Project

# TODO: FILL IN A PROPER README

```bash
datavis-project/
│
├── data/                   # Ignoreras av Git (.gitignore)
│   ├── bronze/             # Rådata från valt API/Kaggle (Parquet/CSV)
│   ├── silver/             # Tvättad data (DuckDB/Pandas)
│   └── gold/               # Aggregerad data exakt formaterad för UX/Dashboards
│
├── ingestion/              # motsvarar producers
│   └── fetch_data.py       # Hämtar data -> sparar till Bronze
│
├── transforms/             # 
│   ├── bronze_to_silver.py # Pandas/DuckDB: Rensning och standardisering
│   └── silver_to_gold.py   # Bygger de slutgiltiga vyerna för Streamlit/PowerBI
│
├── notebooks/              # Indivuduell analys
│   └── eda_NAMN.ipynb      # Din EDA i pandas och duckdb
│
├── serving/                # Frontend-lagret
│   ├── streamlit_app/      # Streamlit applikationen
│   │   └── app.py
│   └── storytelling/       # Data storytellinggrafer i matplotlib
│
├── docs/                   # Docs för ex, module_overviews, session tracking, todo etc.
│   ├── modeling/           # Plats för ERDs              
│   ├── modules/            # Plats för docs i form av module_overviews              
│   └── sessions/           # Plats för session tracking dag för dag för utvecklare
│
├── tests/                  # Unit tests + andra tests
│
│
├── .env.example
├── pyproject.toml          # uv för supersnabb pakethantering
└── README.md
```