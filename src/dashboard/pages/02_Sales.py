import streamlit as st
from components.charts.charts_sales import (
    format_over_time_line_chart,
    total_sales_kpi,
    total_units_revenue_bar_chart,
    dominate_format_kpi,
    format_lifespan_table,
    format_lifespan_chart
    )
from components.filter.filters_sales import metrics_filter, year_filter, format_filter
from utils.helpers import read_textfile, read_css
from utils.constants import MARKDOWN_PATH, STYLE_PATH


st.set_page_config(page_title="Sales format over time", layout="wide")

st.markdown(read_textfile(MARKDOWN_PATH / "sales_intro.md"))

st.markdown("""*Hover on the lines to see fun facts*""")
cols = st.columns([70, 30])
with cols[0]:
    chart_placeholder = st.empty()
with cols[1]:
    with st.container(border=True):
        formats = format_filter()
        years = year_filter()
        metric = metrics_filter()

with chart_placeholder:
    format_over_time_line_chart(metric, formats, years)
st.caption("""
    Fun fact sources:
    RIAA(Recording Industry Association of America) — riaa.com |
    BPI(British Phonographic Industry) — bpi.co.uk |
    Billboard — billboard.com |
    Rolling Stone — rollingstone.com |
    Spotify Newsroom — newsroom.spotify.com 
    """)

metrics = ["Value", "Units"]
labels = ["Total revenue in USD", "Total sales in units"]

st.title("Revenue and units sold total")
cols = st.columns([70,30])
with cols[0]:
    total_units_revenue_bar_chart(formats, years, metrics, labels)
with cols[1]:
    for m, label in zip(metrics, labels):
        total_sales_kpi(m, formats, years, label)

st.markdown(read_textfile(MARKDOWN_PATH / "sales_format_lifetime.md"))
format_lifespan_table()
format_lifespan_chart()

read_css(STYLE_PATH / "style.css")