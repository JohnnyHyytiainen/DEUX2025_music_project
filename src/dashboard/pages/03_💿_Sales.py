import streamlit as st
from components.charts.charts_sales import peak_table, format_over_time_line_chart, total_sales_kpi, total_units_revenue_bar_chart
from components.filter.filters_sales import metrics_filter, year_filter, format_filter



st.set_page_config(page_title="Sales format over time",page_icon="💿", layout="wide")

st.title("Music consumption: From Vinyl to Streaming")

st.title("Linechart of total sales per year")

def create_row_space(spaces=10):
    for _ in range(spaces):
        st.write("")

cols = st.columns([1, 3], vertical_alignment='center')
with cols[0]:
    years = year_filter()
    create_row_space(5)
    metric = metrics_filter()
    create_row_space(5)
    formats = format_filter()
with cols[1]:
    format_over_time_line_chart(metric, formats, years)

metrics = ["Units", "Value"]
labels = ["Total sales in units", "Total revenue in USD"]

st.title("Barchart for revenue and units sold over time")
cols = st.columns([75, 25], vertical_alignment='center')
with cols[0]:
    total_units_revenue_bar_chart(formats, years, metrics, labels)
with cols[1]:
    for m, label in zip(metrics, labels):
        total_sales_kpi(m, formats, years, label)




