# Script för att göra queries som ska synas på 02_📈_Historical_Trends.py
# Kommentarer: Svenska
# Kod: Engelska


def get_available_years_query() -> str:
    """
    Retrieves all unique years by cutting out the first 4 characters,
    from snapshot_date (YYYY) and converting to numbers.
    """
    return """
        SELECT DISTINCT CAST(SUBSTRING(snapshot_date, 1, 4) AS INTEGER) AS year 
        FROM silver_historical_charts 
        WHERE snapshot_date IS NOT NULL
        ORDER BY year DESC;
    """


def get_top_artists_by_year_query(year: int, top_n: int) -> str:
    """
    Calculates which artists were on the top list the most times.
    We map 'artists' to 'artist' so that the Plotly graph recognizes it.
    """
    return f"""
        SELECT 
            artists AS artist,
            COUNT(*) as total_chart_appearances
        FROM silver_historical_charts
        WHERE CAST(SUBSTRING(snapshot_date, 1, 4) AS INTEGER) = {year}
        GROUP BY artists
        ORDER BY total_chart_appearances DESC
        LIMIT {top_n};
    """
