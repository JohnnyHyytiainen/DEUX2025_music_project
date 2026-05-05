from components.data_loader import fetch_data

def get_country_list_query(selected_cont):
    if selected_cont == "Alla":
        return "SELECT DISTINCT country FROM silver_historical_charts WHERE country IS NOT NULL"
    else:
        return f"""
            SELECT DISTINCT h.country
            FROM silver_historical_charts h
            LEFT JOIN dim_geography d ON h.iso_code = d.iso_code
            WHERE d.continent = '{selected_cont}'
        """


def get_date_list_query():
    return "SELECT DISTINCT SUBSTRING(snapshot_date, 1, 10) as snapshot_date FROM silver_historical_charts ORDER BY snapshot_date"


def get_filtered_data_query(selected_cont, selected_country, start_date, end_date):
    where = []
    if selected_cont != "Alla":
        where.append(f"d.continent = '{selected_cont}'")
    if selected_country != "Alla":
        where.append(f"h.country = '{selected_country}'")
    if start_date and end_date:
        where.append(f"h.snapshot_date BETWEEN '{start_date}' AND '{end_date}'")

    where_sql = " AND ".join(where) if where else "1=1"

    return f"""
        SELECT 
            h.name AS "Song title",
            h.artists AS Artists,
            SUM(h.streams) as Streams
        FROM silver_historical_charts h
        LEFT JOIN dim_geography d ON h.iso_code = d.iso_code
        WHERE {where_sql}
        GROUP BY "Song title", Artists
        ORDER BY streams DESC
        LIMIT 10
    """


# Script för att göra queries som ska synas på 02_📈_Historical_Trends.py
# Kommentarer: Svenska
# Kod: Engelska
#
#
# def get_available_years_query() -> str:
#     """
#     Retrieves all unique years by cutting out the first 4 characters,
#     from snapshot_date (YYYY) and converting to numbers.
#     """
#     return """
#         SELECT DISTINCT CAST(SUBSTRING(snapshot_date, 1, 4) AS INTEGER) AS year
#         FROM silver_historical_charts
#         WHERE snapshot_date IS NOT NULL
#         ORDER BY year DESC;
#     """
#
#
# def get_top_artists_by_year_query(year: int, top_n: int) -> str:
#     """
#     Calculates which artists were on the top list the most times.
#     We map 'artists' to 'artist' so that the Plotly graph recognizes it.
#     """
#     return f"""
#         SELECT
#             artists AS artist,
#             COUNT(*) as total_chart_appearances
#         FROM silver_historical_charts
#         WHERE CAST(SUBSTRING(snapshot_date, 1, 4) AS INTEGER) = {year}
#         GROUP BY artists
#         ORDER BY total_chart_appearances DESC
#         LIMIT {top_n};
#     """
