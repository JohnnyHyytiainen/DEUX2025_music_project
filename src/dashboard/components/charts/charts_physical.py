import streamlit as st
import plotly.express as px

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

def format_over_time_line_chart(metric, formats, years):
    dff = df.query("metric == @metric and format in @formats and year >= @years[0] and year <= @years[1]")
    dff = dff.groupby(['year', 'format'])['value'].sum().reset_index()
    dff['year'] = dff['year'].astype(str)

    with st.container(border=True):
        st.markdown("Format over years")
        fig = px.line(dff, x='year', y='value', color='format')
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)