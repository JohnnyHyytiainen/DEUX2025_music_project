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

def format_over_time_line_chart():
    df_format_sales = df.groupby(['year', 'format'])['value'].sum().reset_index()

    df_format_sales['year'] = df_format_sales['year'].astype(str)

    with st.container(border=True):
        st.markdown("Format over years")
        st.line_chart(
            df_format_sales,
            x='year',
            y='value',
            color='format'
        )