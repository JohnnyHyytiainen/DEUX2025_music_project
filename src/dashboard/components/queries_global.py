# Script för att göra queries som ska synas på 01_🌍_Global_EDA.py sidan.
# Kommentarer: Svenska
# Kod: Engelska


def get_top_explicit_query(region: str) -> str:
    """Returns query to get countries with most explicit music taste."""

    # En tillfällig 'Dimensionstabell' i Python
    region_map = {
        "Norden": "('SE', 'NO', 'DK', 'FI', 'IS')",
        "Nordamerika": "('US', 'CA')",
        "Latinamerika": "('BR', 'MX', 'AR', 'CL', 'CO')",
        "Asien": "('JP', 'KR', 'TW', 'HK', 'SG')",
    }

    # Bygga WHERE clause dynamiskt
    where_clause = "WHERE country != 'Global'"

    # Om användaren valt en specifik region (inte "Alla")
    if region in region_map:
        where_clause += f" AND country IN {region_map[region]}"

    # Läser ifrån 'gold_spotify_daily' och väljer 'country_name'
    # Döper det till 'country' i output (AS country) så streamlit koden behöver ej ändras öht.
    return f"""
    SELECT 
        country_name AS country, 
        AVG(CAST(is_explicit AS INT)) * 100 as Explicit_Procent,
        AVG(tempo) as Avg_BPM
    FROM gold_spotify_daily
    {where_clause}
    GROUP BY country_name
    HAVING COUNT(*) > 100
    ORDER BY Explicit_Procent DESC;
    """


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
