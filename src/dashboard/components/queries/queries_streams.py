from components.data_loader import fetch_data

def get_countries_list_query(selected_cont):
    if selected_cont is None or selected_cont == "Alla":
        return "SELECT DISTINCT country FROM silver_historical_charts WHERE country IS NOT NULL"
    else:
        return f"""
            SELECT DISTINCT h.country
            FROM silver_historical_charts h
            LEFT JOIN dim_geography d ON h.iso_code = d.iso_code
            WHERE d.continent = '{selected_cont}'
        """


def get_date_list_query():
    return """SELECT DISTINCT SUBSTRING(snapshot_date, 1, 10) AS snapshot_date
            FROM silver_historical_charts
            WHERE snapshot_date NOT LIKE '2021-12-%'
            ORDER BY snapshot_date"""


def get_filter_query(selected_cont, selected_countries, start_date, end_date):
    where = []
    if selected_cont != "Alla":
        where.append(f"d.continent = '{selected_cont}'")

    if len(selected_countries) == 1:
        where.append(f"h.country = '{selected_countries[0]}'")
    elif len(selected_countries) == 2:
        where.append(f"h.country IN ('{selected_countries[0]}', '{selected_countries[1]}')")

    if start_date and end_date:
        where.append(f"h.snapshot_date BETWEEN '{start_date}' AND '{end_date}'")

    where_sql = " AND ".join(where) if where else "1=1"

    return where_sql

def table_query(selected_cont, selected_countries, start_date, end_date):
    where_sql = get_filter_query(selected_cont, selected_countries, start_date, end_date)

    return f"""
        SELECT 
            h.name AS "Song title",
            h.artists AS Artists,
            SUM(h.streams) AS Streams
        FROM silver_historical_charts h
        LEFT JOIN dim_geography d ON h.iso_code = d.iso_code
        WHERE {where_sql}
        GROUP BY "Song title", Artists
        ORDER BY streams DESC
        LIMIT 5
    """

def line_chart_query(selected_cont, selected_countries, start_date, end_date):
    where_sql = get_filter_query(selected_cont, selected_countries, start_date, end_date)

    if not selected_countries:
        return f"""
            SELECT
              SUBSTRING(h.snapshot_date, 1, 10) AS Date,
              SUM(h.streams) AS "Amount of streams",
            FROM silver_historical_charts h
            LEFT JOIN dim_geography d ON h.iso_code = d.iso_code
            WHERE {where_sql}
            GROUP BY Date
            ORDER BY Date
        """
    else:
        return f"""
            SELECT
              SUBSTRING(h.snapshot_date, 1, 10) AS Date,
              SUM(h.streams) AS "Amount of streams",
              h.country AS Country
            FROM silver_historical_charts h
            LEFT JOIN dim_geography d ON h.iso_code = d.iso_code
            WHERE {where_sql}
            GROUP BY Date, Country
            ORDER BY Date
        """