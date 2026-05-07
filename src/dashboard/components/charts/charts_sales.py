import streamlit as st
import plotly.express as px

import duckdb
import pandas as pd

from components.data_loader import fetch_data
from components.queries.queries_sales import get_all_media_sales, get_format_lifespan_query


df = fetch_data(get_all_media_sales())

color_map = {
    'CD': '#85817B',
    'Cassette': '#CE917A',
    'Vinyl': '#C25A4F',
    '8-Track': '#784E50',
    'Download': '#77989C',
    'Streaming': '#DAB576',
    'Radio': '#B33A38'
}


def format_over_time_line_chart(metric, formats, years):
    """
    Renders a line chart showing format sales over time with historical fun facts.

    Args:
        metric (str): The metric to display. Options: 'Units', 'Value', 'Value (Adjusted)'.
        formats (list): List of format names to include, e.g. ['CD', 'Vinyl', 'Streaming'].
        years (tuple): Year range as (start, end), e.g. (1973, 2019).

    Example:
        format_over_time_line_chart('Value', ['CD', 'Vinyl'], (1980, 2010))
    """

    dff = df.query("metric == @metric and format in @formats and year >= @years[0] and year <= @years[1]")
    dff = dff.groupby(['year', 'format'])['value'].sum().reset_index()

    fun_facts = {
        1973: 'The 8-Track format peaks — over 40 million players sold in the US alone',
        1976: 'Cassette sales overtake 8-Track for the first time — the format never recovers',
        1977: 'Vinyl hits its golden era — Saturday Night Fever becomes one of the best-selling albums ever',
        1980: '8-Track is officially dead — no major label releases new titles on the format',
        1983: 'The CD is commercially launched — Dire Straits Brothers in Arms becomes first CD to sell 1 million copies',
        1988: 'Cassette outsells vinyl for the first time in history',
        1991: 'CD overtakes cassette in sales for the first time',
        1999: 'CD peaks — over 940 million units sold globally',
        2000: 'Napster reaches 80 million users before shutdown in 2001',
        2003: 'iTunes Store launches — 1 million songs sold in first week',
        2008: 'Streaming starts taking over physical media — Spotify launches in Europe',
        2012: 'Vinyl makes a comeback — sales up 745% since 2007',
        2015: 'Streaming revenue surpasses digital download revenue for the first time',
        2019: 'Streaming accounts for 80% of all music industry revenue',
    }

    dff['fun_fact'] = dff['year'].map(fun_facts).fillna('')
    dff['year'] = dff['year'].astype(str)

    # Filter for facts
    filtered_fun_facts = {year: fact for year, fact in fun_facts.items() if years[0] <= year <= years[1]}

    with st.container(border=True):
        st.markdown("Format over years")

        fig = px.line(dff, x='year', y='value', color='format',color_discrete_map=color_map, custom_data=['fun_fact'])

        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Value: %{y}<br>%{customdata[0]}<extra></extra>"
        )

        # Plotting fun facts on graph
        for year in filtered_fun_facts.keys():
            fig.add_shape(
                type="line",
                x0=str(year),
                x1=str(year),
                y0=0,
                y1=1,
                yref="paper",
                line=dict(dash="dot", color="grey", width=2),
                opacity=0.8,
            )

        #Makes the tooltip window bigger
        fig.update_layout(
            hoverlabel=dict(
                font_size=16,
                namelength=-1
            )
        )

        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)

def total_sales_kpi(metric, formats, years, label):
    """
    Renders a KPI metric showing total sales in units or revenue for selected filters.

    Args:
        metric (str): The metric to sum. Options: 'Units', 'Value', 'Value (Adjusted)'.
        formats (list): List of format names to include, e.g. ['CD', 'Streaming'].
        years (tuple): Year range as (start, end), e.g. (1990, 2010).
        label (str): The label displayed above the KPI value, e.g. 'Total revenue in USD'.

    Example:
        total_sales_kpi('Value', ['CD'], (1990, 2005), 'Total revenue in USD')
    """

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

    st.metric(label=label, value=f"{total_sales['total_sales']:,.0f} Million",border=True)

def dominate_format_kpi(metric, formats, years):
    """
    Renders a KPI metric showing the format with the highest total sales for selected filters.

    Args:
        metric (str): The metric to rank by. Options: 'Units', 'Value', 'Value (Adjusted)'.
        formats (list): List of format names to include, e.g. ['CD', 'Cassette', 'Vinyl'].
        years (tuple): Year range as (start, end), e.g. (1973, 2019).

    Example:
        dominate_format_kpi('Value (Adjusted)', ['CD', 'Cassette', 'Vinyl'], (1973, 2019))
    """

    format_list = "', '".join(formats)
    dominant = duckdb.sql(f"""--sql
        SELECT
            format,
            SUM(value) as total_sales
        FROM df
        WHERE metric = '{metric}'
        AND year >= {years[0]}
        AND year <= {years[1]}
        AND format IN ('{format_list}')
        GROUP BY format
        ORDER BY total_sales DESC
        LIMIT 1
        """).df().iloc[0]

    st.metric(label="Dominate format", value=dominant['format'], border=True)

def total_units_revenue_bar_chart(formats, years, metrics, labels):
    """
    Renders a grouped horizontal bar chart comparing total units sold and revenue by format.

    Args:
        formats (list): List of format names to include, e.g. ['CD', 'Vinyl', 'Streaming'].
        years (tuple): Year range as (start, end), e.g. (1973, 2019).
        metrics (list): List of metric names. Options: 'Units', 'Value', 'Value (Adjusted)'.
        labels (list): Display labels for each metric, e.g. ['Total sales in units', 'Total revenue in USD'].

    Example:
        total_units_revenue_bar_chart(['CD', 'Vinyl'], (1980, 2010), ['Units', 'Value'], ['Total sales in units', 'Total revenue in USD'])
    """

    dfs = []
    for m, label in zip(metrics, labels):
        dff = df.query("metric == @m and format in @formats and year >= @years[0] and year <= @years[1]")
        dff = dff.groupby(['format'])['value'].sum().reset_index()
        dff['metric'] = label
        dfs.append(dff)

    dff_combined = pd.concat(dfs)

    format_order = dff_combined.groupby('format')['value'].sum().sort_values(ascending=False).index.tolist()

    color_map_bar = {
        'Total revenue in USD': '#DAB576',
        'Total sales in units': '#B33A38'
    }

    fig = px.bar(
        dff_combined,
        x='value',
        y='format',
        color='metric',
        color_discrete_map=color_map_bar,
        barmode='group',
        title='Total value USD and Units sold',
        labels={'value': 'Value in USD and units sold', 'format': 'Format'},
        category_orders={'format': format_order}
    )

    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)


def format_lifespan_chart():
    """Renders a horizontal bar chart showing the active lifespan of each music format."""

    dff = duckdb.sql(get_format_lifespan_query()).df()

    fig = px.bar(
        dff,
        x='lifespan',
        y='format',
        base='first_year',
        color='format',
        color_discrete_map=color_map,
        orientation='h',
        title='Format Lifespan',
        labels={'lifespan': 'Years active', 'format': 'Format'}
    )

    fig.update_layout(showlegend=False)

    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)

def format_lifespan_table():
    """Renders a table showing first year, last year, lifespan, peak year and peak revenue per format."""

    dff = duckdb.sql(get_format_lifespan_query()).df()
    dff['peak_value'] = dff['peak_value'].astype(int)
    st.table(dff.rename(columns={
        'format': 'Format',
        'first_year': 'First Year',
        'last_year': 'Last Year',
        'lifespan': 'Lifespan (years)',
        'peak_year': 'Peak Year',
        'peak_value': 'Peak Revenue USD (millions)',
    }))