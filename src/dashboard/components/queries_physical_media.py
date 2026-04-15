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
