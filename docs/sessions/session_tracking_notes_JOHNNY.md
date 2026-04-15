# Session tracking notes - Johnny H

## Daily tracking:
**Sunday 05/04-2026:**
*Goals for today*
- Branch out, start doing EDA on a few Spotify datasets from kaggle.
- https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated/versions/493
    - **Done**

- Do EDA on dataset
    - **Done**

- Write EDA insights about dataset
    - **Done**

- Write cleaned data and save it to Silver(Processed) layer in repo as .parquet file.
    - **Done**

- Do basic query with duckdb on .parquet file
    - **Done**

- Added 'bare bones' CI pipeline to run linting and formatting with Ruff.
    - **Done** NOTE: Didnt work as intended therefore removal was needed.

---

**Tuesday 07/04-2026:**
*Goals for today*
- Branch out, start doing national EDA for: https://www.kaggle.com/datasets/asaniczka/top-spotify-songs-in-73-countries-daily-updated/versions/493 
    - **Done**

- Make proper dateformat for Global data instead of month it should be yyyy/mm/dd.
    - Updated plots
    - Updated clean data
    - Updated with .csv and .parquet
        - **Done**
        - **Done**
        - **Done**



**Wednesday 08/04-2026**
*Goals for today*
- Make an ERD for how db could look like.
    - **Done**

- Start setting up a database for us to use
    - **Done**

- Ingest all clean and standardised datasets with matching column names across all datasets
    - **Done**

**Thursday 08/04-2026**
*Goals for today*
- Start setting up streamlit for repo so that we have it done
    - **Done**

**Monday 13/04-2026**
*Goals for today*
- Clean up repo, remove unnecessary folders.
    - **Done**

- Add proper README.md draft to show tech-stack and explain purpose with DEUX project.
    - **Done**

- Start setting up brief streamlit dashboard with few sample queries divided into:
    - Landing page:                     - **Done**
    - Pages:                            - **Done**
    - components with query functions:  - **Done**

- Download ISO country code dataset from Kaggle, clean it and only keep alpha-2 (iso with 2 letters) + country and create a dim table(view table to bypass JOINS)
    - **Done**

- Create a view table from `dim_geography` table to bypass having to JOIN when querying in streamlit dashboard.
    - **Done**

**Tuesday 14/04-2026**
*Goals for today*
- Migrate entire OLAP(duckdb) database to OLTP(SQLite) format for ease of use in PowerBI for group.
    - **Done**

**Wednesday 15/04-2026**
*Goals for today:*
- Expand on streamlit scripts, include more features with filters and sliders for group to use as template to build upon.
    - **Done**

**Wednesday 15/04-2026**
*Goals for today:*
- Expand on streamlit scripts, include more features with filters and sliders for group to use as template to build upon.
    - **Done**

- Update streamlit dashboard with more filtering, dynamic variables, att KPI insights.
    - **Done**


# Remaining datasets that MIGHT be needed / used if needed.

- https://www.kaggle.com/datasets/edumucelli/spotifys-worldwide-daily-song-ranking

- https://www.kaggle.com/datasets/brunoalarcon123/top-200-spotify-songs-dataset

    





