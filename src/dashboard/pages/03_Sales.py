from operator import concat

import streamlit as st
from components.charts.charts_sales import (
    peak_table,
    format_over_time_line_chart,
    total_sales_kpi,
    total_units_revenue_bar_chart,
    dominate_format_kpi,
    format_lifespan_table,
    format_lifespan_chart
    )
from components.filter.filters_sales import metrics_filter, year_filter, format_filter



st.set_page_config(page_title="Sales format over time",page_icon="💿", layout="wide")

st.title("Music consumption: From Vinyl to Streaming")

st.title("Linechart of total sales per year")

st.markdown("""**Hover on the lines to see fun facts**""")

def create_row_space(spaces=10):
    for i in range(spaces):
        st.write("")

cols = st.columns([70, 30])
with cols[0]:
    chart_placeholder = st.empty()
with cols[1]:
    kpi_placeholder = st.empty()
    create_row_space(6)
    years = year_filter()
    metric = metrics_filter()
    formats = format_filter()

with kpi_placeholder:
    dominate_format_kpi(metric, formats, years)
with chart_placeholder:
    format_over_time_line_chart(metric, formats, years)

metrics = ["Value", "Units"]
labels = ["Total revenue in USD", "Total sales in units"]

st.title("Barchart for revenue and units sold over time")
cols = st.columns([70,30])
with cols[0]:
    total_units_revenue_bar_chart(formats, years, metrics, labels)
with cols[1]:
    for m, label in zip(metrics, labels):
        total_sales_kpi(m, formats, years, label)

format_lifespan_table()
format_lifespan_chart()
