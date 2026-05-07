import streamlit as st
from components.data_loader import fetch_data
from components.queries.queries_sales import get_all_media_sales

df = fetch_data(get_all_media_sales())

def metrics_filter():
    """
    Renders a selectbox for choosing a metric.

    Returns:
        str: Selected metric, e.g. 'Units', 'Value' or 'Value (Adjusted)'.

    Example:
        metric = metrics_filter()
    """
    return st.selectbox(label='Select metric', options=df['metric'].unique(), )


def format_filter():
    """
    Renders a toggle for selecting all formats and pills for individual format selection.
    Returns a fallback of the first format if nothing is selected.

     Returns:
         list: List of selected format names, e.g. ['CD', 'Vinyl', 'Streaming'].

    Example:
        formats = format_filter()
    """
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
    """
    Renders a range slider for selecting a year interval.
    Min and max values are derived dynamically from the dataset.

    Returns:
        tuple: Selected year range as (start, end), e.g. (1973, 2019).

    Example:
         years = year_filter()
    """
    return st.slider(
        label='Select years',
        min_value=int(df['year'].min()),
        max_value=int(df['year'].max()),
        value=(int(df['year'].min()), int(df['year'].max())),
    )