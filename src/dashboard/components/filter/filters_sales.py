import streamlit as st
from components.data_loader import fetch_data
from components.queries.queries_sales import get_all_media_sales

df = fetch_data(get_all_media_sales())

def metrics_filter():
    return st.selectbox(label='Select metric', options=df['metric'].unique(), )


def format_filter():
    options = df['format'].unique().tolist()

    all_selected = st.toggle('Select all', value=True)

    if all_selected:
        selected = st.pills(
            label='Select formats',
            options=options,
            default=options,
            selection_mode='multi'
        )
    else:
        selected = st.pills(
            label='Select formats',
            options=options,
            default=options[0],
            selection_mode='multi'
        )

    if not selected:
        st.warning('Select at least one format')
        return options[0:1]

    return selected

def year_filter():
    return st.slider(
        label='Select years',
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=(int(df['year'].min()), int(df['year'].max())),
    )