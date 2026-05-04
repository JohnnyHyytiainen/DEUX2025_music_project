import streamlit as st
from components.data_loader import fetch_data
from components.queries.queries_physical_media import get_media_sales_query
from components.charts.charts_sound import top_country_profile_chart
from components.filter.filter_sound import procent_slider

st.set_page_config(page_title="Sounds", page_icon="🎶", layout="wide")

enery_slider = procent_slider(name="Energy")

top_country_profile_chart(enery_slider[0],enery_slider[1])

