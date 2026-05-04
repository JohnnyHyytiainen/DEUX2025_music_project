import streamlit as st

import duckdb

from components.data_loader import fetch_data
from components.queries.queries_physical_media import get_all_media_sales

df = fetch_data(get_all_media_sales())

df_peak_year = duckdb.sql("""--sql
    SELECT DISTINCT ON (format, metric)
        format,
        metric,
        year,
        value as peak_value
    FROM df
    ORDER BY format, metric, peak_value DESC
                                   """).df()

def peak_table(number_format = 10):
    with st.container(border=True):
        st.markdown("Top peak year by format")
        st.table(df_peak_year.head(number_format))