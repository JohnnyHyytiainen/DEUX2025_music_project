# Global Music Trends & Cultural Insights (DE25 x UX25)

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![DuckDB](https://img.shields.io/badge/DuckDB-1.5.1-yellow.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.56.0-red.svg)
![Parquet](https://img.shields.io/badge/Data-Parquet-orange.svg)

## Project Overview
This project is an agile collaboration between Data Engineering (DE25) and UX Design (UX25) students at the Stockholm Institute of Technology (STI). The aim of the project is to explore, clean, and visualize massive amounts of music data to uncover cultural differences, historical listening trends, and physical format shifts within the music industry.

Our DE team has architected a robust Data Lakehouse solution. We transform millions of rows of raw music data into a highly structured, lightning-fast analytical environment, powering interactive PowerBI and Streamlit dashboards.

## Architecture & Tech Stack

To bypass platform storage limits and achieve maximum performance in our cloud deployment, we developed a decoupled storage/compute architecture:

1. **Extraction & Transformation:** Raw data is cleaned, type-converted, and processed using Python and Pandas.  

2. **Optimized Storage (Parquet):** The heavy DuckDB database is exported into highly compressed `.parquet` files. Massive tables (like `silver_historical_charts` with over 2.5 million rows) are dynamically chunked into smaller parts to bypass GitHub's 100MB file limit

3. **In-Memory Query Engine:** Our Streamlit application does not rely on a static database file. Instead, it instantiates an *in-memory* DuckDB connection on startup, dynamically registering all `.parquet` files and chunks as SQL `VIEWS`. This ensures lightning-fast queries with a minimal memory footprint.

4. **Data Storytelling & UI:** Interactive, caching-optimized Streamlit dashboards and Matplotlib/Seaborn visualizations to present complex data stories effectively.

## Project Structure
```text
DEUX2025_music_project/
├── assets/                         # UI Assets (Images, Icons)
├── data/                           
│   ├── parquet/                    # Deployment-ready compressed data (Tracked)
│   ├── plots/                      # Static EDA visualization outputs
│   └── storytelling_plots/         # High-fidelity graphs for presentations
├── docs/                           # Documentation, workflows, and ER diagrams
├── notebooks/                      # Jupyter Notebooks for EDA and prototyping
├── scripts/                        
│   └── export_to_parquet.py        # Automates the Parquet chunking pipeline
├── src/                            # Core Application Source Code
│   ├── dashboard/                  # Streamlit frontend application
│   │   ├── app.py                  # Main entry point for the dashboard
│   │   ├── pages/                  # Streamlit multi-page routing
│   │   └── components/             # Reusable UI charts and DRY SQL queries
│   └── database/                   # Database initialization scripts
├── pyproject.toml                  # Project dependencies
└── README.md                       # Project documentation
```
## Get Started (Local Environment)

Due to our in-memory Parquet architecture, running this project locally is incredibly straightforward. No heavy database downloads are required.

**1. Clone the repository**
```bash
git clone <url-to-repo>
cd DEUX2025_music_project
```

**2. Install dependencies**
We recommend using `uv` for lightning-fast dependency resolution, but standard `pip` works as well.
```bash
uv sync 
# OR: pip install -r requirements.txt
```

**3. Run the Streamlit Dashboard**
Our `data_loader` will automatically locate the `data/parquet/` directory and mount the data into a temporary DuckDB instance.
```bash
streamlit run src/dashboard/Rewind.py
```

## EDAs and Datasets


## Team (DE25)
* **[Anja](https://github.com/Anja-Sche)**    - Data Engineer
* **[Felix](https://github.com/FellanNokes)**   - Data Engineer
* **[Johnny](https://github.com/JohnnyHyytiainen)**  - Data Engineer
* **[Rikard](https://github.com/RikardOledal)**  - Data Engineer 
