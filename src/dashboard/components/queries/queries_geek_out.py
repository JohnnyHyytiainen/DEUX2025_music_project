# Script för att göra queries som ska synas på 04_Geek_Out.py sidan.
# Kommentarer: Svenska
# Kod: Engelska

# ========================
# Helper funktioner
# ========================
def _build_geo_where_clause(
    continent: str,
    main_table_alias: str = "s",
    geo_table_alias: str = "g",
    is_explicit: bool = True,
) -> str:
    """Helper function to build DYNAMIC WHERE clause for filtering geography."""
    where_clause = f"WHERE {main_table_alias}.country != 'Global'"

    if continent and continent != "Global":
        where_clause += f" AND {geo_table_alias}.continent = '{continent}'"

    if not is_explicit:
        where_clause += f" AND {main_table_alias}.is_explicit = 0"

    return where_clause


def get_countries_in_continent_query(continent: str) -> str:
    """Gets a list of countries for the selected continent THAT ACTUALLY HAVE SPOTIFY DATA."""

    where_clause = f"WHERE g.continent = '{continent}'" if continent != "Global" else ""

    # INNER JOIN så SQL att bara returnera de länder som matchar
    # (dvs de som har låtar) i gold_spotify_daily.
    return f"""--sql
    SELECT DISTINCT g.country_name 
    FROM dim_geography g
    INNER JOIN gold_spotify_daily s ON g.iso_code = s.country
    {where_clause}
    ORDER BY g.country_name ASC
    """


# =====================================
# Ren lista av kontinenter
# Syfte: filtrerar bort onödigt "skräp"
# =====================================
def get_continent_list_query() -> str:
    """Gets a clean list of continents. Filters away useless garbage."""
    return """--sql
    SELECT DISTINCT continent 
    FROM dim_geography 
    WHERE continent IS NOT NULL 
      AND continent NOT IN ('Antarctica', 'Other', 'Worldwide') 
    ORDER BY continent ASC
    """


# ==========================================
# Top Explicita länderna på varje kontinent
# ==========================================
def get_top_explicit_query(continent: str) -> str:
    """Returns query to get countries with most explicit music taste."""
    where_clause = _build_geo_where_clause(continent, is_explicit=True)
    return f"""--sql
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


# ==============================================================
# Glädje(Valence) och Tempo för varje kontinent och dess länder
# ==============================================================
def get_mood_and_tempo_query(continent: str, is_explicit: bool) -> str:
    """Returns query to get both Valence and tempo, can now filter by continent"""
    where_clause = _build_geo_where_clause(continent, is_explicit=is_explicit)
    return f"""--sql
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
    LIMIT 15
    """


# ===========================================
# Query för att hitta världens "dancefloor"
# Syfte: Hitta Danceability och Energy i låtar
# ============================================
def get_dancefloor_songs_query(continent: str, is_explicit: bool) -> str:
    """Retrieves the top songs in chosen region for a massive scatter plot"""
    where_clause = _build_geo_where_clause(continent, is_explicit=is_explicit)
    return f"""--sql
    SELECT
        s.name AS Song,
        s.artists AS Artist,
        MAX(s.energy) * 100 AS Energy,
        MAX(s.danceability) * 100 AS Danceability,
        MAX(s.popularity) AS Popularity
    FROM gold_spotify_daily s
    LEFT JOIN dim_geography g ON s.country = g.iso_code
    {where_clause}
    GROUP BY s.name, s.artists
    ORDER BY Popularity DESC
    LIMIT 450
    """


# ======================================================================
# Query för akustisk musik och/VS producerad musik
# Syfte: tt få fram "organisk" vs producerad musik(acousticness 0-1)
# =====================================================================
def get_acoustic_loudness_query(continent: str, is_explicit: bool) -> str:
    """Gets Acousticness to compare 'organic' vs produced music"""
    where_clause = _build_geo_where_clause(continent, is_explicit=is_explicit)
    return f"""--sql
    SELECT
        g.country_name AS country,
        AVG(s.acousticness) * 100 AS avg_acousticness,
        AVG(s.loudness) AS avg_loudness,
        COUNT(DISTINCT s.spotify_id) as track_count
    FROM silver_spotify_daily s
    LEFT JOIN dim_geography g ON s.country = g.iso_code
    {where_clause}
    GROUP BY g.country_name
    HAVING track_count > 100
    """


# ========================================================================
# Query för radar-chart för att jämföra valda regioner i gold_spotify_daily
# ========================================================================
def get_country_audio_signature_query(
    country1: str, country2: str, is_explicit: bool
) -> str:
    """Gets average audio DNA for TWO selected COUNTRIES, with explicit filter."""

    # Skapa filtret för explicit musik
    explicit_filter = "" if is_explicit else "AND is_explicit = 0"

    def build_country_select(country, alias):
        # Skydd mot identiska val
        is_duplicate = country1 == country2
        display_name = f"{country} ({alias})" if is_duplicate else country

        return f"""
        SELECT 
            '{display_name}' AS Region,
            AVG(danceability) * 100 AS Danceability,
            AVG(energy) * 100 AS Energy,
            AVG(valence) * 100 AS Happiness,
            AVG(acousticness) * 100 AS Acousticness,
            AVG(speechiness) * 100 AS Speechiness
        FROM gold_spotify_daily
        WHERE country_name = '{country}'
        {explicit_filter}
        """

    query1 = build_country_select(country1, "Val 1")
    query2 = build_country_select(country2, "Val 2")

    return f"{query1} \n UNION ALL \n {query2}"


# ================================================================
# ANVÄNDS EJ I GLOBAL
# Songfinder i PowerBI dashboarden fast i streamlit.
# Syfte: Hitta BÄST matchande låt/låtar beroende på sökparametrar
# ================================================================
def get_dj_crate_query(bpm_range, valence_range, energy_range, is_explicit, limit_top):
    """Queries UNIQUE songs based on 'dj filter(BPM, Mood, Energy)."""
    explicit_filter = "AND is_explicit = " + str(is_explicit).lower()
    sql_limit = "LIMIT 20" if limit_top else "LIMIT 500"

    return f"""--sql
    SELECT 
        name as Song, 
        artists as Artist, 
        MAX(tempo) as BPM, 
        MAX(valence * 100) as Happiness, 
        MAX(energy * 100) as Energy,
        COUNT(DISTINCT country) as "Nr of Countries" -- SE ÖVER X LÄNDER ELLER POPULÄR I 
    FROM gold_spotify_daily
    WHERE tempo BETWEEN {bpm_range[0]} AND {bpm_range[1]}
      AND valence * 100 BETWEEN {valence_range[0]} AND {valence_range[1]}
      AND energy * 100 BETWEEN {energy_range[0]} AND {energy_range[1]}
      {explicit_filter}
    GROUP BY name, artists
    
    ORDER BY MAX(popularity) DESC
    {sql_limit}
    """
