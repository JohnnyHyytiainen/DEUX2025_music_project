# Script för att göra queries som ska synas på 02_Sales.py sidan
# Kommentarer: Svenska
# Kod: Engelska


# Dynamisk SQL query (String interpolation i python)
def get_media_sales_query(metric: str, year_range: tuple, formats: list) -> str:
    """
    Generates a dynamic SQL query based on chosen filters
    """
    # Hantera formatering för SQL IN-sats
    format_list = "', '".join(formats)

    return f"""
    SELECT 
        year,
        format,
        value
    FROM silver_music_format_sales
    WHERE metric = '{metric}'
    AND year BETWEEN {year_range[0]} AND {year_range[1]}
    AND format IN ('{format_list}')
    ORDER BY year ASC
    """

def get_all_media_sales() -> str:
    return """
           SELECT * FROM (
               SELECT
                   year, metric,
                   value,
                   CASE
                   WHEN format IN ('CD', 'CD Single', 'SACD') THEN 'CD'
                   WHEN format IN ('Cassette', 'Cassette Single') THEN 'Cassette'
                   WHEN format IN ('LP/EP', 'Vinyl Single') THEN 'Vinyl'
                   WHEN format = '8 - Track' THEN '8-Track'
                   WHEN format IN ('Download Single', 'Download Album', 'Download Music Video', 'Kiosk', 'Ringtones & Ringbacks') THEN 'Download'
                   WHEN format IN ('Paid Subscriptions', 'Limited Tier Paid Subscription', 'Paid Subscription', 'On-Demand Streaming (Ad-Supported)', 'Other Ad-Supported Streaming') THEN 'Streaming'
                   END AS format
               FROM silver_music_format_sales
               WHERE format NOT IN ('Music Video (Physical)', 'DVD Audio', 'SoundExchange Distributions', 'Synchronization', 'Other Digital') AND value > 0
           )
           WHERE format IS NOT NULL
           """

def get_format_lifespan_query():
    return """
    SELECT
        format,
        MIN(year) as first_year,
        MAX(year) as last_year,
        MAX(year) - MIN(year) as lifespan,
        FIRST(year ORDER BY value DESC) as peak_year,
        ROUND(MAX(value), 1) as peak_value
    FROM df
    WHERE metric = 'Units'
    AND format IN ('CD', '8-Track', 'Vinyl', 'Cassette', 'Download', 'Streaming')
    AND value > 0
    GROUP BY format
    ORDER BY first_year ASC
    """