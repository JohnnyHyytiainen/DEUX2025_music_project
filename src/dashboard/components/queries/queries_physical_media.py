# Script för att göra queries som ska synas på 03_💿_Physical_Media.py sidan
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
           SELECT
               year, metric,
               value,
               CASE
               WHEN format IN ('CD', 'CD Single', 'SACD') THEN 'CD'
               WHEN format \
           IN ('Cassette', 'Cassette Single') THEN 'Cassette'
               WHEN format IN ('LP/EP', 'Vinyl Single') THEN 'Vinyl'
               WHEN format = '8 - Track' THEN '8-Track'
               WHEN format IN ('Music Video (Physical)', 'DVD Audio') THEN 'Video'
               WHEN format IN ('Download Single', 'Download Album', 'Download Music Video', 'Kiosk', 'Ringtones & Ringbacks') THEN 'Download'
               WHEN format IN ('Paid Subscriptions', 'Limited Tier Paid Subscription', 'Paid Subscription', 'On-Demand Streaming (Ad-Supported)', 'Other Ad-Supported Streaming') THEN 'Streaming'
               WHEN format IN ('SoundExchange Distributions', 'Synchronization', 'Other Digital') THEN 'Radio'
               ELSE 'Other'
           END AS format
        FROM silver_music_format_sales
           """