import streamlit as st
import plotly.express as px

import duckdb

from components.data_loader import fetch_data
from components.queries.queries_sales import get_all_media_sales


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

    fun_facts = {
        1999: 'CD reached its all-time peak with 940 million units sold!',
        2001: 'Napster shutdown accelerated digital music shift',
        2008: 'Streaming starts taking over physical media',
    }

    dff['fun_fact'] = dff['year'].map(fun_facts).fillna('')
    dff['year'] = dff['year'].astype(str)

    with st.container(border=True):
        st.markdown("Format over years")

        fig = px.line(dff, x='year', y='value', color='format', custom_data=['fun_fact'])

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Value: %{y}<br>%{customdata[0]}<extra></extra>"
        )

        for year in fun_facts.keys():
            fig.add_shape(
                type="line",
                x0=str(year),
                x1=str(year),
                y0=0,
                y1=1,
                yref="paper",
                line=dict(dash="dot", color="grey", width=1),
                opacity=0.5,
            )
            fig.add_annotation(
                x=str(year),
                y=1,
                yref="paper",
                text="ℹ️",
                showarrow=False,
            )

        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

def total_sales_kpi(metric, formats, years, label):
    format_list = "', '".join(formats)
    total_sales = duckdb.sql(f"""--sql
        SELECT
            SUM(value) as total_sales
        FROM df
        WHERE metric like '{metric}'
        AND year >= {years[0]}
        AND year <= {years[1]}
        AND format IN ('{format_list}')
        """).df().iloc[0]

    st.metric(label=f"Total sales in {label}", value=f"{total_sales['total_sales']:,.0f} Million")

