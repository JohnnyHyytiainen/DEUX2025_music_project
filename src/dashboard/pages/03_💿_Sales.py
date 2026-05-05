import streamlit as st
from components.charts.charts_sales import peak_table, format_over_time_line_chart, total_sales_kpi
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
cols = st.columns(len(metrics))

for col, m in zip(cols, metrics):
    with col:
        total_sales_kpi(m, formats, years, m)

format_over_time_line_chart(metric, formats, years)