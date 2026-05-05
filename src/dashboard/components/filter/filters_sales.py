import streamlit as st
from components.data_loader import fetch_data
from components.queries.queries_sales import get_all_media_sales

df = fetch_data(get_all_media_sales())

def metrics_filter():
    return st.selectbox(label='Select metric', options=df['metric'].unique())

def format_filter():
    options = df['format'].unique().tolist()
    return st.multiselect(label='Select formats', options=options, default=options)

def year_filter():
    return st.slider(
        label='Select years',
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=(int(df['year'].min()), int(df['year'].max())),
    )