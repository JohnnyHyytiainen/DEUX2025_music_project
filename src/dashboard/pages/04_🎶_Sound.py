import streamlit as st
from components.data_loader import fetch_data
from components.queries.queries_physical_media import get_media_sales_query
from components.charts.charts_sound import top_country_profile_chart

st.set_page_config(page_title="Sounds", page_icon="🎶", layout="wide")

top_country_profile_chart()

