import streamlit as st
import plotly.express as px

import duckdb
import pandas as pd

from components.data_loader import fetch_data
from components.queries.queries_sales import get_all_media_sales


df = fetch_data(get_all_media_sales())


#TODO: Change to lifetime span of different formats
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

    #sources:
    #RIAA(Recording Industry Association of America) — riaa.com
    #BPI(British Phonographic Industry) — bpi.co.uk
    #Billboard — billboard.com
    #Rolling Stone — rollingstone.com
    #Spotify Newsroom — newsroom.spotify.com

    fun_facts = {
        1973: 'The 8-Track format peaks — over 40 million players sold in the US alone',
        1977: 'Vinyl hits its golden era — Saturday Night Fever becomes one of the best-selling albums ever',
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

        fig = px.line(dff, x='year', y='value', color='format', custom_data=['fun_fact'])

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
                line=dict(dash="dot", color="white", width=2),
                opacity=0.6,
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
    dfs = []
    for m, label in zip(metrics, labels):
        dff = df.query("metric == @m and format in @formats and year >= @years[0] and year <= @years[1]")
        dff = dff.groupby(['format'])['value'].sum().reset_index()
        dff['metric'] = label
        dfs.append(dff)

    dff_combined = pd.concat(dfs)

    format_order = dff_combined.groupby('format')['value'].sum().sort_values(ascending=False).index.tolist()

    fig = px.bar(
        dff_combined,
        x='value',
        y='format',
        color='metric',
        barmode='group',
        title='Total value USD and Units sold',
        labels={'value': 'Value in USD and units sold', 'format': 'Format'},
        category_orders={'format': format_order}
    )

    with st.container(border=True):
        st.plotly_chart(fig, use_container_width=True)

