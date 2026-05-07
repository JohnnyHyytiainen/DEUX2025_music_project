import streamlit as st
from components.data_loader import fetch_data
from utils.constants import MARKDOWN_PATH, STYLE_PATH
from utils.helpers import read_textfile, read_css
from components.queries.queries_geek_out import get_continent_list_query
from components.queries.queries_streams import get_countries_list_query, get_date_list_query, table_query
from components.filter.filters_streams import continent_filter, country_filter, date_filter, reset_filters_streams,format_streams_table
from components.charts.charts_streams import streams_over_time_line_chart


st.markdown(read_textfile(MARKDOWN_PATH / "streams_title.md"))

# create column for reset button
r_col1, r_col2 = st.columns([13, 1])

# collect data for continents and dates
df_cont = fetch_data(get_continent_list_query())
continents = ["All"] + df_cont["continent"].tolist()

df_dates = fetch_data(get_date_list_query())
dates = df_dates["snapshot_date"].tolist()

# add reset button in column
with r_col2:
    reset_filters_streams(dates)


# create columns for toplist and filters
col1, col2, col3 = st.columns([5, 1, 8])

# add filters to the page in column 3
with col3:
    with st.container(border=True):
        st.markdown("###### Filter by continent")
        selected_cont = continent_filter(continents)


        df_country = fetch_data(get_countries_list_query(selected_cont))
        countries = ["All"] + df_country["country"].tolist()
        selected_countries = country_filter(countries)

        if "selected_dates" not in st.session_state:
            st.session_state.selected_dates = (dates[0], dates[-1])

        start_date, end_date = date_filter(dates)

# add table to page in column one
with col1:
    st.markdown("### Top 5 most streamed")

    df = fetch_data(table_query(selected_cont, selected_countries, start_date, end_date))
    df.index = df.index + 1
    df['Streams'] = df['Streams'].apply(format_streams_table)
    st.table(df)

# add line chart
st.plotly_chart(streams_over_time_line_chart(selected_cont, selected_countries, start_date, end_date))

read_css(STYLE_PATH / "style.css")