import streamlit as st
from components.charts.charts_sales import peak_table, format_over_time_line_chart, total_sales_kpi, total_units_revenue_bar_chart
from components.filter.filters_sales import metrics_filter, year_filter, format_filter



st.set_page_config(page_title="Sales format over time",page_icon="💿", layout="wide")

st.title("💿 Music consumption: From Vinyl to Streaming")

cols = st.columns(2)
with cols[0]:
    metric = metrics_filter()
with cols[1]:
    formats = format_filter()
years = year_filter()

metrics = ["Units", "Value"]
labels = ["Total sales in units", "Total revenue in USD"]
cols = st.columns(len(metrics))

for col, m, label in zip(cols, metrics, labels):
    with col:
        total_sales_kpi(m, formats, years, label)

st.title("Linechart of total sales per year")
format_over_time_line_chart(metric, formats, years)

st.title("Barchart for revenue and units sold over time")
total_units_revenue_bar_chart(formats, years, metrics, labels)