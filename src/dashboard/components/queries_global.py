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
    """Gets a clean list of continents. Filters away useless garbage."""
    return """
    SELECT DISTINCT continent 
    FROM dim_geography 
    WHERE continent IS NOT NULL 
      AND continent NOT IN ('Antarctica', 'Other', 'Worldwide') 
    ORDER BY continent ASC
    """


# Här efter kan vi lägga till flera queries som vi vill visa på sida 1 av vår dashboard.
# def get_vad_som_helst / def kings_of_valence / def ...... ....
def get_mood_and_tempo_query(continent: str) -> str:
    """Returns query to get both Valence and tempo, can now filter by continent"""
    where_clause = "WHERE country != 'Global'"

    # Om vi valt en specifik kontinent, filtrera på den
    if continent and continent != "Alla":
        where_clause += f" AND g.continent = '{continent}'"

    return f"""
    SELECT 
        g.country_name AS country,
        AVG(s.valence) * 100 as happiness_score,
        AVG(s.tempo) as avg_bpm,
        COUNT(DISTINCT s.spotify_id) as unique_songs_played
    FROM gold_spotify_daily s
    LEFT JOIN dim_geography g ON s.country = g.iso_code
    {where_clause}
    GROUP BY g.country_name
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


# sorterar på låtens högsta popularitet globalt så DJn får de största bangersen först
# Eftersom BPM, Happiness och Energy är samma för en och samma låt
# kan vi bara ta MAX() för att få ut värdet när vi grupperar.
def get_dj_crate_query(bpm_range, valence_range, energy_range, is_explicit):
    """Queries UNIQUE songs based on 'dj filter(BPM, Mood, Energy)."""
    explicit_filter = "AND is_explicit = " + str(is_explicit).lower()

    return f"""
    SELECT 
        name as Låt, 
        artists as Artist, 
        MAX(tempo) as BPM, 
        MAX(valence * 100) as Happiness, 
        MAX(energy * 100) as Energy,
        COUNT(DISTINCT country) as "Antal Länder"
    FROM gold_spotify_daily
    WHERE tempo BETWEEN {bpm_range[0]} AND {bpm_range[1]}
      AND valence * 100 BETWEEN {valence_range[0]} AND {valence_range[1]}
      AND energy * 100 BETWEEN {energy_range[0]} AND {energy_range[1]}
      {explicit_filter}
    GROUP BY name, artists
    
    ORDER BY MAX(popularity) DESC 
    LIMIT 20
    """
