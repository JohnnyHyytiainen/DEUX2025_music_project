from components.data_loader import fetch_data

def get_countries_list_query(selected_cont):
    """Create query to extract countries"""
    # continent not chosen -> return all countries
    if selected_cont is None or selected_cont == "All":
        return "SELECT DISTINCT country FROM silver_historical_charts WHERE country IS NOT NULL"

    # continent chosen -> return only countries in that continent
    else:
        return f"""
            SELECT DISTINCT h.country
            FROM silver_historical_charts h
            LEFT JOIN dim_geography d ON h.iso_code = d.iso_code
            WHERE d.continent = '{selected_cont}'
        """


def get_date_list_query():
    """Create query to extract dates"""
    # excluding december 2021 due to inconsistent/bad data
    return """SELECT DISTINCT SUBSTRING(snapshot_date, 1, 10) AS snapshot_date
            FROM silver_historical_charts
            WHERE snapshot_date NOT LIKE '2021-12-%'
            ORDER BY snapshot_date"""


def get_filter_condition(selected_cont, selected_countries, start_date, end_date):
    """Create conditions for filtering"""
    # list to collect filter conditions
    where = []

    # add continent if not "All"
    if selected_cont != "All":
        where.append(f"d.continent = '{selected_cont}'")

    # add country filter, if empty -> no filter added
    if len(selected_countries) == 1:
        where.append(f"h.country = '{selected_countries[0]}'")
    elif len(selected_countries) == 2:
        where.append(f"h.country IN ('{selected_countries[0]}', '{selected_countries[1]}')")

    # add date range filter
    if start_date and end_date:
        where.append(f"h.snapshot_date BETWEEN '{start_date}' AND '{end_date}'")

    # join conditions with AND or return true if no filters
    where_sql = " AND ".join(where) if where else "1=1"

    return where_sql


def table_query(selected_cont, selected_countries, start_date, end_date):
    """Create query for toplist table"""
    where_sql = get_filter_condition(selected_cont, selected_countries, start_date, end_date)

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
    """Create query for information in linechart"""
    where_sql = get_filter_condition(selected_cont, selected_countries, start_date, end_date)

    # countries not selected -> return all countries
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
    # country selected -> return country
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