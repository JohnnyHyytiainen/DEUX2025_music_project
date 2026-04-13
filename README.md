# Global Music Trends & Cultural Insights (DE25 x UX25)
Data Engineering and UX Class of 2025 at STI - Group Project

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![DuckDB](https://img.shields.io/badge/DuckDB-1.5.1-yellow.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56.0-red.svg)

## Project overview
This project is an agile collaboration between Data Engineering (DE25) and UX Design (UX25) at Stockholm Institute of Technology (STI). The aim of the project is to explore, clean and visualize massive amounts of music data to find cultural differences, historical trends and format shifts in the music industry.


Our DE team has built a robust, on-premises Data Lakehouse architecture that transforms millions of rows of messy raw data into a structured, fast analytical database. This is then used as the basis for our PowerBI and Streamlit dashboards and the UX team's final design concepts.

## Architecture & Dataflow (Tech Stack)

1. **Extraction & Transformation (Pandas):** Raw data from CSV is cleaned, type-converted and saved as compressed `.parquet` files in our Silver warehouse.

2. **Data Warehouse (DuckDB):** An idempotent Python script builds a local relational database where data from different sources can be joined lightning fast.

3. **Frontend / Prototyping (PowerBI + Streamlit):** Interactive dashboards to visualize insights around valence, tempo (BPM), genres and format sales.

## Project Structure
Our repo follows Best Practice for Data Science projects:

```text
DEUX2025_music_project/
├── data/                           # IGNORED IN GIT (Shared via Drive/Teams)
│   ├── plots/                      # Plots and graphs from initial EDA of our data
│   ├── raw/                        # Raw CSV data
│   ├── processed/                  # Cleaned and compressed .parquet data
│   └── music_warehouse.duckdb      # The local database
├── docs/                           # Documentation and diagrams
│   └── database_schema.mmd         # ER diagram of the database
├── notebooks/                      # Jupyter Notebooks for initial EDA
├── src/                            # All source code
│   ├── dashboard/                  # Streamlit frontend
│   │   ├── app.py                  # The main file for the application
│   │   └── pages/                  # Dashboard subpages
│   ├── database/                   # Database script
│   │   └── init_db.py              # Creates our tables and loads Parquet files
│   └── data_processing/            # ETL pipelines to clean raw data
├── pyproject.toml                  # Dependencies and project configuration
└── README.md                       # This file
```

## Get Started (Local Team Setup)

Since the database and raw data are too large for GitHub, the following steps are required to run the project locally:

**1. Download the code & install dependencies**
```bash
git clone <url-to-repot>
cd DEUX2025_music_project

# Install dependencies (via uv or pip)
uv sync # or pip install -r requirements.txt (if you generated one)
```

**2. Sync the data files**
* Download the shared `datasets` from our team's shared [data](https://stise.sharepoint.com/:f:/s/Workingname/IgCD6JKZebYWSpvIQ6Rr3Xg1AekPQ84G6WoabkFAGF-ZQkA?e=kwOmjI).
* Place the downloaded data in `data/` folder in the root of the project.

**3. Initialize the database**
Run this script to build the DuckDB database from the clean `.parquet` files.
```bash
python src/database/init_db.py
```

**4. Start the Streamlit Dashboard**
```bash
streamlit run src/dashboard/app.py
```

## Team (DE25)
* **[Anja](https://github.com/Anja-Sche)**    - Data Engineer
* **[Felix](https://github.com/FellanNokes)**   - Data Engineer
* **[Johnny](https://github.com/JohnnyHyytiainen)**  - Data Engineer
* **[Rikard](https://github.com/RikardOledal)**  - Data Engineer 
