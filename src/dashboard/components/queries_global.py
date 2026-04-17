# Script för att göra queries som ska synas på 01_🌍_Global_EDA.py sidan.
# Kommentarer: Svenska
# Kod: Engelska


def get_top_explicit_query(continent: str) -> str:
    """Returns query to get countries with most explicit music taste."""

    # Bygga WHERE clause dynamiskt
    where_clause = "WHERE s.country != 'Global'"

    # Om användaren valt en specifik kontinent i Streamlit, lägg till filter
    if continent and continent != "Alla":
        where_clause += f" AND g.continent = '{continent}'"

    # Läser ifrån 'gold_spotify_daily' och väljer 'country_name'
    # Döper det till 'country' i output (AS country) så streamlit koden behöver ej ändras öht.
    return f"""
    SELECT 
        g.country_name AS country, 
        AVG(CAST(s.is_explicit AS INT)) * 100 as Explicit_Procent,
        AVG(s.tempo) as Avg_BPM
    FROM silver_spotify_daily s
    LEFT JOIN dim_geography g ON s.country = g.iso_code
    {where_clause}
    GROUP BY g.country_name
    HAVING COUNT(*) > 100
    ORDER BY Explicit_Procent DESC;
    """


def get_continent_list_query() -> str:
    """Collects a unique list on all Continents for our Dropdown menu."""
    return "SELECT DISTINCT continent FROM dim_geography WHERE continent IS NOT NULL ORDER BY continent ASC"


# Här efter kan vi lägga till flera queries som vi vill visa på sida 1 av vår dashboard.
# def get_vad_som_helst / def kings_of_valence / def ...... ....
def get_mood_and_tempo_query() -> str:
    """Returns query to get both Valence and tempo per Country"""
    return """
    SELECT 
        country_name AS country,
        AVG(valence) * 100 as happiness_score,
        AVG(tempo) as avg_bpm,
        COUNT(DISTINCT spotify_id) as unique_songs_played
    FROM gold_spotify_daily
    WHERE country != 'Global'
    GROUP BY country_name
    HAVING unique_songs_played > 100
    """


def get_continent_bpm_stats_query() -> str:
    """Returns BPM statistics (BPM) aggregated per continent."""
    return """
    SELECT 
        g.continent, 
        AVG(s.tempo) as Avg_BPM,
        MIN(s.tempo) as Min_BPM,
        MAX(s.tempo) as Max_BPM,
        COUNT(*) as track_count
    FROM silver_spotify_daily s
    LEFT JOIN dim_geography g ON s.country = g.iso_code
    WHERE g.continent IS NOT NULL AND s.country != 'Global'
    GROUP BY g.continent
    ORDER BY Avg_BPM DESC;
    """
